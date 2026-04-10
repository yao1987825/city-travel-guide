#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合数据获取脚本
功能：
1. 从高德地图API获取景点/美食实景图片
2. 从和风天气API获取天气预报
3. 生成带来源标注的价格数据

使用方式：
python fetch_data.py --city 郴州 --type attractions
python fetch_data.py --city 郴州 --type food
python fetch_data.py --city 郴州 --weather
python fetch_data.py --city 郴州 --all
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import base64
from datetime import datetime, timedelta

# 导入配置
from amap_config import AMAP_KEY
from weather_config import QWEATHER_KEY, QWEATHER_BASE_URL, CITY_CODE_MAP

# 尝试导入百度图片搜索库（可选）
try:
    from baiduspider import BaiduSpider
    BAIDU_SPIDER_AVAILABLE = True
except ImportError:
    BAIDU_SPIDER_AVAILABLE = False
    print("提示: pip install baiduspider 可启用百度图片搜索功能")

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "fetched_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_amap_place(keyword, city=None, types=None):
    """
    从高德地图API搜索地点
    types: 景点=旅游, 美食=餐饮服务
    """
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        "key": key,
        "keywords": keyword,
        "city": city,
        "citylimit": "true" if city else "false",
        "output": "json",
        "offset": 5,
    }
    if types:
        params["types"] = types
    
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(full_url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("status") == "1" and data.get("pois"):
                return data["pois"]
    except Exception as e:
        print(f"高德API请求失败: {e}")
    
    return []


def fetch_amap_images(poi_id):
    """
    通过高德POI ID获取图片
    高德地图提供官方图片API
    """
    url = "https://restapi.amap.com/v3/place/photo"
    params = {
        "key": key,
        "id": poi_id,
        "offset": 5,
    }
    
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(full_url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("status") == "1":
                return data.get("urls", [])
    except Exception as e:
        pass
    
    return []


def search_baidu_images(keyword, num=5):
    """
    从百度图片搜索获取图片URL
    """
    if not BAIDU_SPIDER_AVAILABLE:
        return []
    
    spider = BaiduSpider()
    try:
        result = spider.search_image(keyword=keyword, pn=1, rn=num)
        urls = []
        for item in result.get("items", []):
            if "middle_url" in item:
                urls.append(item["middle_url"])
        return urls
    except Exception as e:
        print(f"百度图片搜索失败: {e}")
        return []


def fetch_weather(city_name):
    """
    获取天气预报（和风天气API）
    返回实时天气+未来3天预报
    """
    city_code = CITY_CODE_MAP.get(city_name)
    if not city_code:
        print(f"不支持的城市: {city_name}")
        return None
    
    result = {
        "city": city_name,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "now": None,
        "forecast_3days": [],
        "life_index": None,
    }
    
    # 1. 获取实时天气
    try:
        url = f"{QWEATHER_BASE_URL}/weather/now"
        params = {"key": QWEATHER_KEY, "location": city_code}
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(full_url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("code") == "200":
                result["now"] = data.get("now", {})
    except Exception as e:
        print(f"实时天气获取失败: {e}")
    
    # 2. 获取3天预报
    try:
        url = f"{QWEATHER_BASE_URL}/weather/3d"
        params = {"key": QWEATHER_KEY, "location": city_code}
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(full_url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("code") == "200":
                result["forecast_3days"] = data.get("daily", [])
    except Exception as e:
        print(f"天气预报获取失败: {e}")
    
    # 3. 获取生活指数
    try:
        url = f"{QWEATHER_BASE_URL}/indices/1d"
        params = {"key": QWEATHER_KEY, "location": city_code, "type": "1,2,3,5,6,8,9,10"}
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(full_url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("code") == "200":
                result["life_index"] = data.get("daily", [])
    except Exception as e:
        print(f"生活指数获取失败: {e}")
    
    return result


def format_weather_report(weather_data):
    """
    格式化天气预报为可读文本
    """
    if not weather_data:
        return "无法获取天气数据"
    
    lines = []
    lines.append(f"\n{'='*50}")
    lines.append(f"📍 {weather_data['city']} 天气预报")
    lines.append(f"更新时间: {weather_data['update_time']}")
    lines.append(f"{'='*50}")
    
    # 实时天气
    if weather_data.get("now"):
        now = weather_data["now"]
        lines.append(f"\n🌡️ 当前天气:")
        lines.append(f"   温度: {now.get('temp', 'N/A')}°C (体感 {now.get('feelsLike', 'N/A')}°C)")
        lines.append(f"   天气: {now.get('text', 'N/A')}")
        lines.append(f"   风速: {now.get('windDir', 'N/A')} {now.get('windScale', 'N/A')}级")
        lines.append(f"   湿度: {now.get('humidity', 'N/A')}%")
        lines.append(f"   能见度: {now.get('vis', 'N/A')}km")
    
    # 3天预报
    if weather_data.get("forecast_3days"):
        lines.append(f"\n📅 未来3天预报:")
        for day in weather_data["forecast_3days"]:
            date = day.get("fxDate", "")
            lines.append(f"\n   {date} ({weekday_cn(date)}):")
            lines.append(f"   白天: {day.get('textDay', 'N/A')} | 夜间: {day.get('textNight', 'N/A')}")
            lines.append(f"   温度: {day.get('tempMin', 'N/A')}°C ~ {day.get('tempMax', 'N/A')}°C")
            lines.append(f"   降水概率: {day.get('pop', '0')}% | 风力: {day.get('windDirDay', 'N/A')} {day.get('windScaleDay', 'N/A')}级")
    
    # 生活指数
    if weather_data.get("life_index"):
        lines.append(f"\n💡 生活指数:")
        for index in weather_data["life_index"]:
            category = index.get("name", "")
            level = index.get("level", "")
            text = index.get("text", "")
            if category and level:
                lines.append(f"   {category}: {level} - {text}")
    
    return "\n".join(lines)


def weekday_cn(date_str):
    """转换日期为中文星期"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return weekdays[date.weekday()]
    except:
        return ""


def fetch_attraction_data(city_name, attractions):
    """
    获取景点数据（图片+基础信息）
    """
    results = []
    
    for attraction in attractions:
        name = attraction.get("name", "")
        print(f"正在获取: {name}...")
        
        item = {
            "name": name,
            "city": city_name,
            "amap_images": [],
            "baidu_images": [],
            "poi_info": None,
        }
        
        # 1. 高德地图搜索
        pois = fetch_amap_place(name, city_name, "旅游")
        if pois:
            poi = pois[0]
            item["poi_info"] = {
                "address": poi.get("address", ""),
                "location": poi.get("location", ""),
                "tel": poi.get("tel", ""),
                "rating": poi.get("rating", ""),
            }
            poi_id = poi.get("id", "")
            if poi_id:
                item["amap_images"] = fetch_amap_images(poi_id)
        
        # 2. 百度图片搜索作为备选
        if not item["amap_images"]:
            item["baidu_images"] = search_baidu_images(f"{city_name} {name} 景点", num=3)
        
        results.append(item)
        time.sleep(0.5)  # 避免请求过快
    
    return results


def fetch_food_data(city_name, foods):
    """
    获取美食数据（图片+基础信息）
    """
    results = []
    
    for food in foods:
        name = food.get("name", "")
        print(f"正在获取: {name}...")
        
        item = {
            "name": name,
            "city": city_name,
            "baidu_images": [],
            "recommended_shops": [],
        }
        
        # 高德地图搜索餐饮
        pois = fetch_amap_place(name, city_name, "餐饮服务")
        if pois:
            poi = pois[0]
            item["poi_info"] = {
                "name": poi.get("name", ""),
                "address": poi.get("address", ""),
                "type": poi.get("type", ""),
            }
        
        # 百度图片搜索
        item["baidu_images"] = search_baidu_images(f"{city_name} {name} 美食", num=3)
        
        results.append(item)
        time.sleep(0.5)
    
    return results


def generate_price_report(city_name, attractions, foods):
    """
    生成价格数据报告模板
    数据来源：携程、大众点评（用户需手动查询验证）
    """
    report = {
        "city": city_name,
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "attractions": [],
        "foods": [],
        "data_sources": [
            "携程 https://www.ctrip.com",
            "大众点评 https://www.dianping.com",
            "各景区官方公众号/官网",
        ],
    }
    
    for attr in attractions:
        report["attractions"].append({
            "name": attr.get("name", ""),
            "ticket_price": None,  # 需从携程/官网查询
            "opening_hours": None,  # 需从官网查询
            "suggested_duration": None,  # 建议游玩时长
            "data_source": None,  # 数据来源URL
            "last_verified": None,  # 最后验证时间
        })
    
    for food in foods:
        report["foods"].append({
            "name": food.get("name", ""),
            "price_range": None,  # 需从大众点评查询
            "recommended_shops": [],  # 需从大众点评查询
            "data_source": None,
            "last_verified": None,
        })
    
    return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="综合旅游数据获取工具")
    parser.add_argument("--city", required=True, choices=["郴州", "清远", "衡阳", "长沙", "益阳", "韶关", "深圳"], help="城市名称")
    parser.add_argument("--type", choices=["attractions", "food", "all"], default="all", help="数据类型")
    parser.add_argument("--weather", action="store_true", help="获取天气预报")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    city = args.city
    
    print(f"\n{'#'*50}")
    print(f"开始获取 {city} 旅游数据")
    print(f"{'#'*50}\n")
    
    # 获取天气
    if args.weather or args.type == "all":
        print("正在获取天气预报...")
        weather = fetch_weather(city)
        print(format_weather_report(weather))
        
        # 保存天气数据
        weather_file = os.path.join(OUTPUT_DIR, f"{city}_weather.json")
        with open(weather_file, "w", encoding="utf-8") as f:
            json.dump(weather, f, ensure_ascii=False, indent=2)
        print(f"\n天气数据已保存: {weather_file}")
    
    print("\n" + "="*50)
    print("数据获取完成!")


if __name__ == "__main__":
    main()
