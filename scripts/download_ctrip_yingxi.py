# -*- coding: utf-8 -*-
"""
从携程下载英西峰林高质量图片
"""
import requests
import os
import time

SAVE_DIR = r"d:\旅游skills\city-travel-guide\images\yingxi"
os.makedirs(SAVE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'https://you.ctrip.com/',
}

# 从携程获取的英西峰林相关高质量图片URL
CTRIP_IMAGES = [
    # 峰林晓镇大图
    ('https://dimg04.c-ctrip.com/images/25t0e12000gkhucin9310_W_2048_1536.png_.webp', 'yingxi_fenglinxiaozhen_1.jpg'),
    ('https://dimg04.c-ctrip.com/images/0zg6f12000icnfw4q736D.jpg', 'yingxi_fenglinxiaozhen_2.jpg'),
    ('https://youimg1.c-ctrip.com/target/tg/446/335/960/ea47556baf1f4b96baf88f937aab05f7_D_10000_1200.jpg', 'yingxi_fenglinxiaozhen_3.jpg'),

    # 洞天仙境
    ('https://dimg04.c-ctrip.com/images/10041g000001h3bwvE01E_D_180_180.jpg', 'yingxi_dongtian_1.jpg'),
    ('https://dimg04.c-ctrip.com/images/100u1g000001h4blc68C0_D_180_180.jpg', 'yingxi_dongtian_2.jpg'),
    ('https://dimg04.c-ctrip.com/images/100m1g000001hdqgx2265_D_180_180.jpg', 'yingxi_dongtian_3.jpg'),
    ('https://dimg04.c-ctrip.com/images/10051g000001h6urtBB2B_D_180_180.jpg', 'yingxi_dongtian_4.jpg'),

    # 高清大图（修复尺寸）
    ('https://dimg04.c-ctrip.com/images/100h1g000001hauv71416_D_1000_750.jpg', 'yingxi_hd_1.jpg'),
    ('https://dimg04.c-ctrip.com/images/100w1g000001hfbh26769_D_1000_750.jpg', 'yingxi_hd_2.jpg'),
    ('https://dimg04.c-ctrip.com/images/10041g000001h89l04ED0_D_1000_750.jpg', 'yingxi_hd_3.jpg'),
]

def download_image(url, filename):
    """下载图片"""
    try:
        # 修复URL尺寸参数
        url = url.replace('_W_2048_1536', '_R_1920_1080')
        url = url.replace('_D_180_180', '_R_1920_1080')
        url = url.replace('_D_1000_750', '_R_1920_1080')

        resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if resp.status_code == 200:
            content_type = resp.headers.get('Content-Type', '')
            if 'image' in content_type or url.endswith(('.jpg', '.png', '.webp')):
                filepath = os.path.join(SAVE_DIR, filename)
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"OK: {filename} ({resp.headers.get('Content-Length', 'unknown')} bytes)")
                return True
            else:
                print(f"SKIP: {filename} (not image: {content_type})")
    except Exception as e:
        print(f"ERROR: {filename} - {e}")
    return False

def main():
    print("=== 下载携程英西峰林图片 ===\n")

    for i, (url, filename) in enumerate(CTRIP_IMAGES, 1):
        print(f"[{i}/{len(CTRIP_IMAGES)}] ", end="")
        download_image(url, filename)
        time.sleep(0.5)

    print(f"\n完成! 图片保存在: {SAVE_DIR}")

if __name__ == '__main__':
    main()
