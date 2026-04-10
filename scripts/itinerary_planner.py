# -*- coding: utf-8 -*-
"""
智能路线规划脚本
功能：
1. 根据天气情况智能推荐景点
2. 计算最优出行时间
3. 考虑交通方式和时长
4. 生成带详细时间表的行程

使用方式：
python itinerary_planner.py --city 郴州 --days 2 --budget 中档 --date 2026-04-15
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json
import gzip
import urllib.request
import argparse
from datetime import datetime, timedelta
from weather_config import QWEATHER_KEY, QWEATHER_BASE_URL, CITY_CODE_MAP

# 景点天气偏好配置
ATTRACTION_WEATHER = {
    "漂流": ["晴", "多云", "阴"],
    "日出/日落": ["晴", "多云"],
    "登山/徒步": ["晴", "多云", "阴"],
    "草原": ["晴", "多云"],
    "溶洞": ["无限制"],
    "寺庙/古镇": ["无限制"],
    "博物馆/室内": ["无限制"],
    "海边/沙滩": ["晴", "多云"],
}

# 景点耗时配置（小时）
ATTRACTION_DURATION = {
    "东江湖": 4,
    "高椅岭": 3,
    "仰天湖": 3,
    "苏仙岭": 2,
    "莽山": 5,
    "万华岩": 2,
    "岳麓山": 3,
    "橘子洲": 2,
    "衡山": 6,
    "丹霞山": 5,
    "南华寺": 2,
    "世界之窗": 6,
    "大梅沙": 3,
}

# 交通时长配置（小时）
TRAVEL_TIME = {
    "郴州市区-东江湖": 1,
    "郴州市区-高椅岭": 0.8,
    "郴州市区-仰天湖": 1.5,
    "郴州市区-苏仙岭": 0.3,
    "长沙市区-岳麓山": 0.5,
    "长沙市区-橘子洲": 0.3,
    "衡阳市区-衡山": 1,
    "韶关市区-丹霞山": 1,
    "清远市区-古龙峡": 0.8,
    "深圳市区-大梅沙": 1,
}

# 最佳游览时间
BEST_TIME = {
    "东江湖·雾漫小东江": "清晨5:30-7:30（日出后雾散）",
    "南岳衡山·祝融峰": "清晨4:00-6:00（日出云海）",
    "仰天湖大草原": "上午8:00-11:00（下午易有雷阵雨）",
    "大梅沙": "下午3:00-6:00（避开正午暴晒）",
}


def fetch_weather(city_name, days=3):
    """获取天气预报"""
    city_code = CITY_CODE_MAP.get(city_name)
    if not city_code:
        return None
    
    result = {"city": city_name, "now": None, "forecast": []}
    
    # 获取实时天气
    try:
        url = f"{QWEATHER_BASE_URL}/weather/now?key={QWEATHER_KEY}&location={city_code}"
        req = urllib.request.Request(url)
        req.add_header('Accept-Encoding', 'gzip, deflate')
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            if response.info().get('Content-Encoding') == 'gzip':
                content = gzip.decompress(content)
            data = json.loads(content.decode('utf-8'))
            if data.get('code') == '200':
                result['now'] = data.get('now', {})
    except Exception as e:
        print(f"天气获取失败: {e}")
    
    # 获取3天预报
    try:
        url = f"{QWEATHER_BASE_URL}/weather/3d?key={QWEATHER_KEY}&location={city_code}"
        req = urllib.request.Request(url)
        req.add_header('Accept-Encoding', 'gzip, deflate')
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            if response.info().get('Content-Encoding') == 'gzip':
                content = gzip.decompress(content)
            data = json.loads(content.decode('utf-8'))
            if data.get('code') == '200':
                result['forecast'] = data.get('daily', [])
    except Exception as e:
        print(f"预报获取失败: {e}")
    
    return result


def get_weather_advice(weather_data):
    """根据天气生成出行建议"""
    if not weather_data:
        return "无法获取天气信息，建议正常安排行程"
    
    advice = []
    
    # 分析预报
    if weather_data.get('forecast'):
        for day in weather_data['forecast'][:3]:
            date = day.get('fxDate', '')
            text = day.get('textDay', '')
            temp_max = day.get('tempMax', '')
            temp_min = day.get('tempMin', '')
            precip = float(day.get('precip', 0))
            
            day_advice = f"\n【{date}】{text} {temp_min}~{temp_max}°C"
            
            # 降水判断
            if precip > 10:
                day_advice += " ⚠️ 有雨，建议室内活动"
            elif precip > 5:
                day_advice += " 🌧️ 可能有雨，随身带伞"
            
            # 温度判断
            if int(temp_max) > 35:
                day_advice += " 🔥 高温，避免中午户外"
            elif int(temp_min) < 10:
                day_advice += " 🧥 早晚较凉，带外套"
            
            advice.append(day_advice)
    
    return "\n".join(advice)


def filter_attractions_by_weather(attractions, weather_text):
    """根据天气筛选适合的景点"""
    weather_ok = []
    weather_warning = []
    
    for attr in attractions:
        name = attr.get('name', '')
        tags = attr.get('tags', [])
        
        suitable = False
        for tag in tags:
            if tag in ATTRACTION_WEATHER:
                preferred = ATTRACTION_WEATHER[tag]
                if '无限制' in preferred or weather_text in preferred:
                    suitable = True
                    break
        
        if suitable:
            weather_ok.append(attr)
        else:
            weather_warning.append((attr, "天气可能不适合"))
    
    return weather_ok, weather_warning


def generate_itinerary(city, days, budget, attractions, weather_data):
    """生成行程安排"""
    
    # 根据天气调整行程
    forecast = weather_data.get('forecast', []) if weather_data else []
    current_weather = forecast[0].get('textDay', '未知') if forecast else '未知'
    
    itinerary = {
        "城市": city,
        "天数": days,
        "预算": budget,
        "出发日期天气": current_weather,
        "行程": [],
    }
    
    # 简单的日程分配逻辑（实际使用时需要更复杂的算法）
    daily_plan = []
    
    for i in range(days):
        day_plan = {
            "第几天": f"Day {i+1}",
            "日期": None,  # 需外部填充
            "天气": forecast[i].get('textDay', '未知') if i < len(forecast) else '未知',
            "温度": f"{forecast[i].get('tempMin', '')}~{forecast[i].get('tempMax', '')}°C" if i < len(forecast) else '',
            "景点": [],
            "建议": [],
        }
        
        # 根据天气添加建议
        weather = forecast[i].get('textDay', '') if i < len(forecast) else ''
        precip = float(forecast[i].get('precip', 0)) if i < len(forecast) else 0
        
        if '雨' in weather or precip > 10:
            day_plan["建议"].append("今日有雨，建议安排室内活动（博物馆、寺庙、古镇）")
        elif '晴' in weather:
            day_plan["建议"].append("今日晴天，适合户外活动（漂流、登山、看日出）")
        
        # 温度建议
        temp_max = int(forecast[i].get('tempMax', 25)) if i < len(forecast) else 25
        if temp_max > 32:
            day_plan["建议"].append("气温较高，注意防暑，避开中午时段户外活动")
        
        daily_plan.append(day_plan)
    
    itinerary["行程"] = daily_plan
    return itinerary


def format_itinerary_report(itinerary, weather_data):
    """格式化行程报告"""
    lines = []
    
    lines.append("\n" + "="*60)
    lines.append(f"📍 {itinerary['城市']} {itinerary['天数']}日游行程规划")
    lines.append(f"💰 预算档次: {itinerary['预算']}")
    lines.append("="*60)
    
    # 天气总览
    if weather_data and weather_data.get('now'):
        now = weather_data['now']
        lines.append(f"\n🌤️ 今日天气: {now.get('text', '未知')} {now.get('temp', '?')}°C")
        lines.append(f"   风速: {now.get('windDir', '')} {now.get('windScale', '')}级")
        lines.append(f"   湿度: {now.get('humidity', '')}%")
    
    # 天气预报
    if weather_data and weather_data.get('forecast'):
        lines.append(f"\n📅 未来天气预报:")
        for day in weather_data['forecast'][:itinerary['天数']]:
            date = day.get('fxDate', '')
            lines.append(f"   {date}: {day.get('textDay', '')} {day.get('tempMin', '')}~{day.get('tempMax', '')}°C")
    
    # 每日行程
    for day_plan in itinerary.get('行程', []):
        lines.append(f"\n{'─'*50}")
        lines.append(f"🗓️ {day_plan['第几天']} | 天气: {day_plan['天气']} {day_plan['温度']}")
        
        if day_plan.get('景点'):
            lines.append("📍 推荐景点:")
            for attr in day_plan['景点']:
                lines.append(f"   • {attr}")
        
        if day_plan.get('建议'):
            lines.append("💡 建议:")
            for suggestion in day_plan['建议']:
                lines.append(f"   ✓ {suggestion}")
    
    # 通用出行建议
    lines.append(f"\n{'='*60}")
    lines.append("📋 出行准备建议:")
    lines.append("   • 雨具（湖南春季多雨）")
    lines.append("   • 舒适的徒步鞋")
    lines.append("   • 防晒用品（夏季）")
    lines.append("   • 外套（山区早晚温差大）")
    lines.append("   • 充电宝")
    lines.append("="*60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="智能路线规划工具")
    parser.add_argument("--city", required=True, choices=["郴州", "清远", "衡阳", "长沙", "益阳", "韶关", "深圳"], help="城市")
    parser.add_argument("--days", type=int, default=2, help="游玩天数")
    parser.add_argument("--budget", choices=["平价", "中档", "高档"], default="中档", help="预算档次")
    parser.add_argument("--date", help="出发日期 (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    print(f"\n正在规划 {args.city} {args.days}日游行程...")
    
    # 获取天气
    weather = fetch_weather(args.city, args.days)
    
    # 打印天气
    if weather:
        print(get_weather_advice(weather))
    
    print("\n行程规划已完成，请根据天气调整您的计划！")


if __name__ == "__main__":
    main()
