# -*- coding: utf-8 -*-
"""测试3天天气预报"""
import sys, os, json, gzip, urllib.request
sys.path.insert(0, '.')
from weather_config import QWEATHER_KEY, QWEATHER_BASE_URL, CITY_CODE_MAP

def fetch(url):
    req = urllib.request.Request(url)
    req.add_header('Accept-Encoding', 'gzip, deflate')
    with urllib.request.urlopen(req, timeout=10) as r:
        c = r.read()
        if r.info().get('Content-Encoding') == 'gzip':
            c = gzip.decompress(c)
        return json.loads(c.decode('utf-8'))

city_code = CITY_CODE_MAP['长沙']
data = fetch(f'{QWEATHER_BASE_URL}/weather/3d?key={QWEATHER_KEY}&location={city_code}')
print(json.dumps(data, indent=2, ensure_ascii=False))
