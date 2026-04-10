"""
小红书图片下载脚本
下载郴州美食和景点图片
"""
import asyncio
import json
import requests
import sys
from pathlib import Path

# 修复Windows控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))
from xhs_utils.browser import XHSBrowser
from xhs_utils.api_handler import XHSApiHandler

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

images_dir = Path(r'd:\旅游skills\city-travel-guide\images')
images_dir.mkdir(exist_ok=True)

def download_image(name, url):
    """下载单张图片"""
    filepath = images_dir / f'{name}.jpg'
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            size = len(resp.content) // 1024
            print(f'OK: {name} ({size}KB)')
            return True
    except Exception as e:
        print(f'FAIL: {name}: {e}')
    return False

async def main():
    print('=== 小红书图片下载 ===\n')
    
    # 从小红书搜索获取图片
    async with XHSBrowser(headless=True) as browser:
        api_handler = XHSApiHandler(browser.context)
        
        # 1. 郴州美食
        print('[1] 搜索郴州美食...')
        food_search = await api_handler.search('郴州美食推荐', limit=10)
        
        food_images = []
        for item in food_search.items:
            if item.cover and item.liked_count > 100:
                food_images.append((f'郴州-美食-{item.liked_count}赞', item.cover))
        
        print(f'找到 {len(food_images)} 个高赞美食帖子')
        
        # 2. 郴州景点
        print('\n[2] 搜索郴州景点...')
        spot_search = await api_handler.search('郴州景点推荐', limit=10)
        
        spot_images = []
        for item in spot_search.items:
            if item.cover and item.liked_count > 100:
                spot_images.append((f'郴州-景点-{item.liked_count}赞', item.cover))
        
        print(f'找到 {len(spot_images)} 个高赞景点帖子')
        
        # 3. 东江湖
        print('\n[3] 搜索东江湖...')
        djh_search = await api_handler.search('东江湖', limit=5)
        
        for item in djh_search.items:
            if item.cover and item.liked_count > 100:
                spot_images.append((f'郴州-东江湖-{item.liked_count}赞', item.cover))
        
        # 4. 高椅岭
        print('\n[4] 搜索高椅岭...')
        gyl_search = await api_handler.search('高椅岭', limit=5)
        
        for item in gyl_search.items:
            if item.cover and item.liked_count > 100:
                spot_images.append((f'郴州-高椅岭-{item.liked_count}赞', item.cover))
        
        # 下载美食图片
        print('\n=== 下载美食图片 ===')
        for name, url in food_images[:5]:
            download_image(name, url)
        
        # 下载景点图片
        print('\n=== 下载景点图片 ===')
        for name, url in spot_images[:5]:
            download_image(name, url)
        
        # 保存图片列表
        all_images = {
            'food': [(n, u) for n, u in food_images],
            'spots': [(n, u) for n, u in spot_images]
        }
        log_file = images_dir / 'xhs_images_list.json'
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(all_images, f, ensure_ascii=False, indent=2)
        
        print(f'\n图片列表已保存: {log_file}')

if __name__ == '__main__':
    asyncio.run(main())
