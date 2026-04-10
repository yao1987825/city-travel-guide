# -*- coding: utf-8 -*-
"""下载备用美食图片"""
import json, os, urllib.request

OUTPUT_DIR = r'd:\旅游skills\city-travel-guide\images'

def download_image(url, filepath, max_retries=2):
    for i in range(max_retries):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            req.add_header('Referer', 'https://restapi.amap.com/')
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                if len(data) > 1000:
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    return True, len(data)
        except Exception as e:
            print('  尝试 ' + str(i+1) + ' 失败: ' + str(e)[:50])
    return False, 0

# 备用图片列表
backup_images = [
    # 深圳早茶
    ('深圳', '早茶', 'shenzhen-zaocha.jpg', 'https://aos-comment.amap.com/B02F37UQ3F/comment/content_media_external_file_9288_1762154568066_31767414.jpg'),
    ('深圳', '早茶', 'shenzhen-zaocha.jpg', 'http://store.is.autonavi.com/showpic/164723477a29ff4b901071b9a242a4b4'),
    
    # 衡阳鱼粉
    ('衡阳', '鱼粉', 'hengyang-yufen.jpg', 'https://aos-comment.amap.com/B0FFGDVREJ/comment/%5B2024-11-05-21-07-21%5D0848917-1.jpg'),
    ('衡阳', '鱼粉', 'hengyang-yufen.jpg', 'https://aos-comment.amap.com/B0FFFT50UT/comment/content_media_external_file_100006407_1772792451058_62356642.jpg'),
    
    # 益阳皮蛋 (用桃江胡氏皮蛋粉的图片)
    ('益阳', '皮蛋', 'yiyang-pidan.jpg', 'https://store.is.autonavi.com/showpic/83c1e77788617ee734e0372342c01142'),
]

print('=== 下载备用美食图片 ===\n')

success_count = 0
fail_count = 0

for city, food, filename, url in backup_images:
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 检查是否已存在
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        print('[' + city + '] ' + food + ' (已存在，跳过)')
        continue
    
    print('[' + city + '] ' + food + '...')
    ok, size = download_image(url, filepath)
    
    if ok:
        print('  成功: ' + str(size) + ' bytes')
        success_count += 1
    else:
        print('  失败')
        fail_count += 1

print('\n=== 下载完成 ===')
print('成功: ' + str(success_count))
print('失败: ' + str(fail_count))
