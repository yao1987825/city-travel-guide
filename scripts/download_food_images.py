# -*- coding: utf-8 -*-
"""下载高德API获取的美食图片"""
import json, os, urllib.request, urllib.error

OUTPUT_DIR = r'd:\旅游skills\city-travel-guide\images'

def download_image(url, filepath, max_retries=2):
    """下载图片到指定路径"""
    for i in range(max_retries):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            req.add_header('Referer', 'https://restapi.amap.com/')
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                if len(data) > 1000:  # 确保图片有效
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    return True, len(data)
        except Exception as e:
            print(f'  尝试 {i+1} 失败: {str(e)[:50]}')
    return False, 0

# 图片映射表（高德API返回的数据）
images_data = [
    ('郴州', '坛子肉', 'chenzhou-tanzi.jpg', 'http://store.is.autonavi.com/showpic/67bbfe93f43955bb66fa5e6a16def25c'),
    ('郴州', '东江鱼干', 'chenzhou-dongjiangyugan.jpg', 'https://aos-comment.amap.com/B0K3YRJKCW/comment/content_media_external_file_100006407_1772792451058_62356642.jpg'),
    ('郴州', '桂东腊肉', 'chenzhou-guidonglarou.jpg', 'http://store.is.autonavi.com/showpic/99e9fa248b0d7981c92c34797132fff4'),
    ('郴州', '永兴冰糖橙', 'chenzhou-yongxingbingtangcheng.jpg', 'https://store.is.autonavi.com/showpic/85f5fb8621964ad0958b34f832c121e6'),
    ('长沙', '黑色经典臭豆腐', 'changsha-heisedian.jpg', 'https://aos-comment.amap.com/B0LUL18PKJ/comment/51313126_C305_4A86_B450_26EFE9456CA4_L0_001_1242_163_1768369634768_24586539.jpg'),
    ('长沙', '糖油粑粑', 'changsha-tangyoubaba.jpg', 'https://aos-comment.amap.com/B02DB0VWYV/comment/content_media_external_file_1000047984_ss__1759411019133_05340441.jpg'),
    ('长沙', '费大厨辣椒炒肉', 'changsha-feidayu.jpg', 'http://store.is.autonavi.com/query_pic?id=st58816a2f-9ad4-4e86-9e49-e4e874d66031&user=search&operate=original'),
    ('深圳', '椰子鸡', 'shenzhen-yeziji.jpg', 'https://aos-comment.amap.com/B0FFHDAZW7/comment/33389e7a27888da5e70b62fb67e329c1_2048_2048_80.jpg'),
    ('深圳', '早茶', 'shenzhen-zaocha.jpg', 'https://aos-comment.amap.com/B02F37VZYF/comment/content_media_external_images_media_38421_1762154442215_31767414.jpg'),
    ('深圳', '肠粉', 'shenzhen-changfen.jpg', 'https://aos-comment.amap.com/comment/20260320-1a5606fe7bd4ea1b4bb363e0-4xfDkfjw86T8OMLFcfPNs9.jpg'),
    ('清远', '英德红茶', 'qingyuan-yingdehongcha.jpg', 'https://store.is.autonavi.com/showpic/ffda4ecafc4d7618cc31bec6252cf410'),
    ('清远', '九龙豆腐花', 'qingyuan-jiulongdoufu.jpg', 'https://aos-comment.amap.com/B0GUL5T8HQ/comment/59B37E88_8384_4446_9B0A_2498F6102FDB_L0_001_2016_151_1745201232731_26389511.jpg'),
    ('清远', '客家酿豆腐', 'qingyuan-kejianiang.jpg', 'https://store.is.autonavi.com/showpic/dc5791d5e1fc7cdd6ebf4b5b7247edf8'),
    ('衡阳', '南岳素斋', 'hengyang-suzhai.jpg', 'https://aos-comment.amap.com/B0FFFVT3VW/comment/bc63dfdbe41b162a2d210adfae95cdaf_2048_2048_80.jpg'),
    ('衡阳', '衡东土菜', 'hengyang-tucai.jpg', 'https://aos-comment.amap.com/B0FFFWISYH/comment/content_media_external_images_media_1000020710_ss__1767542355864_62995263.jpg'),
    ('韶关', '宰相粉', 'shaoguan-zaixiangfen.jpg', 'https://aos-comment.amap.com/B0J3M7H9UX/comment/f6ea76cbd102f2d6af9137a06c0ecccc_2048_2048_80.jpg'),
    ('韶关', '山坑螺', 'shaoguan-shankengluo.jpg', 'https://aos-comment.amap.com/B0HAL55CWO/comment/1cd5d20839c3be33d10c719c8d71db0f_2048_2048_80.jpg'),
    ('韶关', '北江河鲜', 'shaoguan-beijiang.jpg', 'https://aos-comment.amap.com/B0FFIVBQUC/comment/a3fb494c3fc266a8ae7d6445075ed8f9_2048_2048_80.jpg'),
    ('益阳', '擂茶', 'yiyang-leicha.jpg', 'https://aos-comment.amap.com/B0FFKW9QNL/comment/content_media_external_images_media_1483_ss__1726999622665_87718024.jpg'),
    ('益阳', '茶油一杂鸡', 'yiyang-chayouji.jpg', 'http://store.is.autonavi.com/showpic/779a5a61a67061c93df3591a0353c203'),
]

print('=== 批量下载美食图片 ===\n')
os.makedirs(OUTPUT_DIR, exist_ok=True)

success_count = 0
fail_count = 0
failed_items = []

for city, food, filename, url in images_data:
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 检查是否已存在
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        print(f'[跳过] {city}-{food} (已存在)')
        success_count += 1
        continue
    
    print(f'[下载] {city}-{food}...')
    ok, size = download_image(url, filepath)
    
    if ok:
        print(f'  成功: {size} bytes -> {filename}')
        success_count += 1
    else:
        print(f'  失败: {url[:60]}...')
        fail_count += 1
        failed_items.append((city, food, url))

print(f'\n=== 下载完成 ===')
print(f'成功: {success_count}')
print(f'失败: {fail_count}')

if failed_items:
    print('\n失败的图片:')
    for city, food, url in failed_items:
        print(f'  {city}-{food}: {url}')
    
    # 保存失败列表
    with open(os.path.join(OUTPUT_DIR, 'failed_downloads.json'), 'w', encoding='utf-8') as f:
        json.dump(failed_items, f, ensure_ascii=False, indent=2)
    print('\n失败列表已保存到 failed_downloads.json')
