# -*- coding: utf-8 -*-
import json, gzip, urllib.request, urllib.parse, time

AMAP_KEY = 'acfa7f06d95fa28379922d5e0eadd754'
BASE_URL = 'https://restapi.amap.com/v3'

def fetch(url, max_retries=2):
    for i in range(max_retries):
        try:
            req = urllib.request.Request(url)
            req.add_header('Accept-Encoding', 'gzip, deflate')
            with urllib.request.urlopen(req, timeout=15) as r:
                c = r.read()
                if r.info().get('Content-Encoding') == 'gzip':
                    c = gzip.decompress(c)
                return json.loads(c.decode('utf-8'))
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(1)
    return {}

# 搜索更多图片
queries = [
    ('深圳', '早茶', 5),  
    ('衡阳', '鱼粉', 5),
    ('益阳', '松花皮蛋', 5),
    ('益阳', '皮蛋', 5),
]

print('=== 搜索备用图片 ===\n')
results = []

for city, food, num in queries:
    params = 'keywords=' + urllib.parse.quote(food) + '&types=050000&city=' + urllib.parse.quote(city) + '&citylimit=true&offset=' + str(num) + '&key=' + AMAP_KEY
    url = BASE_URL + '/place/text?' + params
    data = fetch(url)
    
    pois = data.get('pois', [])
    print('[' + city + '] ' + food + ' - 找到 ' + str(len(pois)) + ' 个POI')
    
    for poi in pois[:num]:
        photos = poi.get('photos', [])
        photo_url = photos[0].get('url', '') if photos else ''
        name = poi.get('name', '')
        print('  - ' + name + ': ' + (photo_url[:80] if photo_url else '无图') + '...')
        
        if photo_url:
            results.append({
                'city': city,
                'food': food,
                'name': name,
                'photo_url': photo_url
            })
    print()
    time.sleep(0.5)

# 保存结果
with open('backup_images_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('备用图片列表已保存')
