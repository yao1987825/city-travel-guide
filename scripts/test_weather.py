# -*- coding: utf-8 -*-
"""测试天气API"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json
import gzip
import urllib.request
from weather_config import QWEATHER_KEY, QWEATHER_BASE_URL, CITY_CODE_MAP

def fetch_weather(city_code):
    """获取天气数据"""
    url = f"{QWEATHER_BASE_URL}/weather/now?key={QWEATHER_KEY}&location={city_code}"
    
    request = urllib.request.Request(url)
    request.add_header('Accept-Encoding', 'gzip, deflate')
    
    with urllib.request.urlopen(request, timeout=10) as response:
        content = response.read()
        # 解压gzip
        if response.info().get('Content-Encoding') == 'gzip':
            content = gzip.decompress(content)
        return json.loads(content.decode('utf-8'))

# 测试
print("测试城市: 长沙\n")
try:
    data = fetch_weather(CITY_CODE_MAP['长沙'])
    if data.get('code') == '200':
        now = data.get('now', {})
        print("天气API连接成功!")
        print(f"当前天气: {now.get('text')} {now.get('temp')}°C")
        print(f"体感温度: {now.get('feelsLike')}°C")
        print(f"风速: {now.get('windDir')} {now.get('windScale')}级")
        print(f"湿度: {now.get('humidity')}%")
    else:
        print(f"API返回错误: {data}")
except Exception as e:
    print(f"API测试失败: {e}")
