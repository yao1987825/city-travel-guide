# -*- coding: utf-8 -*-
"""获取英西峰林高德地图POI实景图片"""
import requests
import json

AMAP_KEY = 'acfa7f06d95fa28379922d5e0eadd754'

# 英西峰林相关POI
pois = [
    {'id': 'B02FB0P91Y', 'name': 'Yingxi Fenglin Dongtian Xianjing'},
    {'id': 'B0FFLEKEZ7', 'name': 'Yingxi Fenglin Fenglin Xiaozhen'},
    {'id': 'B0FFGHF491', 'name': 'Yingxi Fenglin Jiuchongtian'},
]

print('=== Get Yingxi Fenglin POI Images ===')
print()

for poi in pois:
    poi_id = poi['id']
    name = poi['name']
    
    # 获取POI详细信息（含图片）
    url = f'https://restapi.amap.com/v3/place/detail?id={poi_id}&key={AMAP_KEY}'
    resp = requests.get(url)
    data = resp.json()
    
    print(f'[{name}]')
    if data.get('data'):
        d = data['data']
        print(f'  Address: {d.get("address", "N/A")}')
        print(f'  Type: {d.get("type", "N/A")}')
        
        # 获取图片
        photos = d.get('photos', [])
        if photos:
            print(f'  Images: {len(photos)} found')
            for i, photo in enumerate(photos[:3]):
                photo_url = photo.get('url', '')
                print(f'  Image{i+1}: {photo_url}')
        else:
            print('  WARNING: No images')
    else:
        print('  WARNING: No detail data')
    print()

print()
print('=== Save images to file ===')
# Get first POI images
url = f'https://restapi.amap.com/v3/place/detail?id=B02FB0P91Y&key={AMAP_KEY}'
resp = requests.get(url)
data = resp.json()
if data.get('data'):
    photos = data['data'].get('photos', [])
    if photos:
        with open('yingxi_images.txt', 'w', encoding='utf-8') as f:
            f.write('英西峰林真实POI图片URL:\n\n')
            for i, photo in enumerate(photos):
                f.write(f'{i+1}. {photo.get("url", "")}\n')
        print(f'Saved {len(photos)} image URLs to yingxi_images.txt')
