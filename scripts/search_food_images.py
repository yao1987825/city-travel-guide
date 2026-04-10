# -*- coding: utf-8 -*-
import json, gzip, urllib.request, urllib.parse, time

AMAP_KEY = 'acfa7f06d95fa28379922d5e0eadd754'
BASE_URL = 'https://restapi.amap.com/v3'

def fetch(url, max_retries=2):
    for i in range(max_retries):
        try:
            req = urllib.request.Request(url)
            req.add_header('Accept-Encoding', 'gzip, deflate')
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=15) as r:
                c = r.read()
                if r.info().get('Content-Encoding') == 'gzip':
                    c = gzip.decompress(c)
                return json.loads(c.decode('utf-8'))
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(1)
            else:
                return {'status': '0', 'error': str(e)}

# 待搜索的美食和城市
foods = [
    ('郴州', '坛子肉'),
    ('郴州', '东江鱼干'),
    ('郴州', '桂东腊肉'),
    ('郴州', '永兴冰糖橙'),
    ('长沙', '黑色经典臭豆腐'),
    ('长沙', '糖油粑粑'),
    ('长沙', '费大厨辣椒炒肉'),
    ('深圳', '椰子鸡'),
    ('深圳', '早茶'),
    ('深圳', '肠粉'),
    ('清远', '英德红茶'),
    ('清远', '九龙豆腐花'),
    ('清远', '客家酿豆腐'),
    ('衡阳', '衡阳鱼粉'),
    ('衡阳', '南岳素斋'),
    ('衡阳', '衡东土菜'),
    ('韶关', '宰相粉'),
    ('韶关', '山坑螺'),
    ('韶关', '北江河鲜'),
    ('益阳', '擂茶'),
    ('益阳', '松花皮蛋'),
    ('益阳', '茶油一杂鸡'),
]

print('=== 高德地图API美食搜索 ===')
print()

results = []
for city, food in foods:
    params = f'keywords={urllib.parse.quote(food)}&types=050000&city={urllib.parse.quote(city)}&citylimit=true&offset=5&key={AMAP_KEY}'
    url = f'{BASE_URL}/place/text?{params}'
    data = fetch(url)
    
    if data.get('pois') and len(data['pois']) > 0:
        poi = data['pois'][0]
        name = poi.get('name', '')
        location = poi.get('location', '')
        photos = poi.get('photos', [])
        photo_url = photos[0].get('url', '') if photos else ''
        
        print(f'[{city}] {food}')
        print(f'  店铺: {name}')
        print(f'  坐标: {location}')
        if photo_url:
            print(f'  图片: {photo_url[:100]}...')
        else:
            print('  图片: 无')
        
        results.append({
            'city': city,
            'food': food,
            'name': name,
            'location': location,
            'photo_url': photo_url
        })
    else:
        print(f'[{city}] {food} - 未找到POI')
        results.append({
            'city': city,
            'food': food,
            'name': '',
            'location': '',
            'photo_url': ''
        })
    print()
    time.sleep(0.3)

# 保存结果
with open('food_images_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('结果已保存到 food_images_result.json')
