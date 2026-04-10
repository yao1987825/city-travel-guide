# -*- coding: utf-8 -*-
"""
英西峰林图片爬虫
从各大旅游网站获取真实风景图片
"""
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import urllib.parse

# 创建保存目录
SAVE_DIR = r"d:\旅游skills\city-travel-guide\images\yingxi"
os.makedirs(SAVE_DIR, exist_ok=True)

# 浏览器Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.google.com',
}

AMAP_KEY = 'acfa7f06d95fa28379922d5e0eadd754'


def search_amap_poi(keyword, city='清远'):
    """搜索高德地图POI"""
    url = 'https://restapi.amap.com/v3/place/text'
    params = {
        'key': AMAP_KEY,
        'keywords': keyword,
        'city': city,
        'citylimit': 'true',
        'output': 'json',
        'offset': 10
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get('pois'):
            return data['pois']
    except Exception as e:
        print(f"高德API错误: {e}")
    return []


def get_ctrip_images():
    """携程攻略获取图片"""
    print("\n=== 携程攻略 ===")
    images = []
    try:
        # 携程景点页面
        url = 'https://you.ctrip.com/sight/yingde962/17601.html'
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 查找图片
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and ('yingxi' in src.lower() or 'fenglin' in src.lower() or
                       'ctrip' in src or 'qunar' in src):
                images.append(src)
                print(f"找到图片: {src[:100]}...")
    except Exception as e:
        print(f"携程错误: {e}")
    return images


def get_baidu_images():
    """百度图片搜索获取图片"""
    print("\n=== 百度图片 ===")
    images = []
    try:
        # 使用百度图片搜索API
        keyword = urllib.parse.quote('英西峰林 风景')
        url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&word={keyword}&pn=0&rn=20'

        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'

        # 提取图片URL
        pattern = r'"thumbURL":"([^"]+)"'
        matches = re.findall(pattern, resp.text)
        for match in matches[:10]:
            if match.startswith('http'):
                images.append(match)
                print(f"找到图片: {match[:100]}...")
    except Exception as e:
        print(f"百度图片错误: {e}")
    return images


def get_mafengwo_images():
    """马蜂窝获取图片"""
    print("\n=== 马蜂窝 ===")
    images = []
    try:
        url = 'https://www.mafengwo.cn/jd/17601/gonglve.html'
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and ('http' in src):
                images.append(src)
                print(f"找到图片: {src[:100]}...")
    except Exception as e:
        print(f"马蜂窝错误: {e}")
    return images


def save_image(url, filename):
    """下载并保存图片"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if resp.status_code == 200:
            filepath = os.path.join(SAVE_DIR, filename)
            with open(filepath, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"已保存: {filepath}")
            return True
    except Exception as e:
        print(f"下载失败: {e}")
    return False


def main():
    print("="*60)
    print("英西峰林图片爬虫")
    print("="*60)

    # 1. 搜索高德地图POI
    print("\n=== 搜索高德地图POI ===")
    pois = search_amap_poi('英西峰林')
    print(f"找到 {len(pois)} 个POI:")
    for poi in pois[:5]:
        print(f"  - {poi.get('name')}: {poi.get('address')}")

    # 2. 获取各网站图片
    all_images = []

    # 携程
    ctrip_imgs = get_ctrip_images()
    all_images.extend(ctrip_imgs[:5])

    # 百度图片
    baidu_imgs = get_baidu_images()
    all_images.extend(baidu_imgs[:5])

    # 马蜂窝
    mafengwo_imgs = get_mafengwo_images()
    all_images.extend(mafengwo_imgs[:5])

    print(f"\n=== 总计找到 {len(all_images)} 张图片 ===")

    # 3. 保存图片URL列表
    url_file = os.path.join(SAVE_DIR, 'image_urls.txt')
    with open(url_file, 'w', encoding='utf-8') as f:
        f.write("英西峰林真实图片URL列表\n")
        f.write("="*60 + "\n")
        for i, url in enumerate(all_images, 1):
            f.write(f"{i}. {url}\n")
    print(f"\n图片URL列表已保存到: {url_file}")

    # 4. 下载图片（可选）
    print("\n=== 下载前5张图片 ===")
    for i, url in enumerate(all_images[:5], 1):
        filename = f"yingxi_{i}.jpg"
        save_image(url, filename)
        time.sleep(1)  # 避免请求过快

    print("\n完成!")


if __name__ == '__main__':
    main()
