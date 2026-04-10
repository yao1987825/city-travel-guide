"""
小红书图片数据获取脚本
用于获取七城旅游攻略所需的美食和景点图片
"""
import argparse
import asyncio
import json
import os
import re
import sys
import requests
from pathlib import Path
from urllib.parse import urlparse

# 修复Windows控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 导入xhs模块
sys.path.insert(0, str(Path(__file__).parent))
from xhs_utils.browser import XHSBrowser
from xhs_utils.api_handler import XHSApiHandler


# 七城搜索关键词配置
CITIES_KEYWORDS = {
    "郴州": {
        "food": ["郴州美食推荐", "郴州必吃美食", "郴州小吃"],
        "spots": ["郴州景点推荐", "郴州旅游攻略", "东江湖", "高椅岭", "仰天湖"]
    },
    "清远": {
        "food": ["清远美食推荐", "清远鸡", "清远小吃"],
        "spots": ["清远景点推荐", "清远旅游攻略", "英西峰林"]
    },
    "衡阳": {
        "food": ["衡阳美食推荐", "衡阳鱼粉", "衡阳小吃"],
        "spots": ["衡阳景点推荐", "衡阳旅游攻略", "南岳衡山"]
    },
    "长沙": {
        "food": ["长沙美食推荐", "长沙小吃", "五一广场美食"],
        "spots": ["长沙景点推荐", "长沙旅游攻略", "岳麓山", "橘子洲"]
    },
    "益阳": {
        "food": ["益阳美食推荐", "益阳小吃"],
        "spots": ["益阳景点推荐", "益阳旅游攻略"]
    },
    "韶关": {
        "food": ["韶关美食推荐", "韶关小吃"],
        "spots": ["韶关景点推荐", "韶关旅游攻略", "丹霞山"]
    },
    "深圳": {
        "food": ["深圳美食推荐", "深圳小吃", "深圳早茶"],
        "spots": ["深圳景点推荐", "深圳旅游攻略", "世界之窗", "深圳湾"]
    }
}


class XHSImageDownloader:
    """小红书图片下载器"""
    
    def __init__(self, output_dir: str = "images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.downloaded_images = {}  # {(city, category): [(name, url), ...]}
        
    def _sanitize_filename(self, name: str) -> str:
        """清理文件名"""
        # 移除特殊字符
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # 限制长度
        if len(name) > 30:
            name = name[:30]
        return name.strip() or "untitled"
    
    def _get_image_extension(self, url: str) -> str:
        """获取图片扩展名"""
        parsed = urlparse(url)
        path = parsed.path.lower()
        if '.jpeg' in path or '.jpg' in path:
            return '.jpg'
        elif '.png' in path:
            return '.png'
        elif '.webp' in path:
            return '.webp'
        return '.jpg'
    
    def download_images(self, images: list, city: str, category: str, base_name: str, max_images: int = 3) -> list:
        """批量下载图片"""
        downloaded = []
        images = images[:max_images]  # 限制数量
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for i, url in enumerate(images):
            # 处理URL，去掉大小限制参数获取原图
            url = re.sub(r'\\/w[0-9]+h[0-9]+', '', url)
            url = url.replace('&opacity=100', '')
            
            filename = f"{base_name}_{i+1}{self._get_image_extension(url)}"
            filepath = self.output_dir / filename
            
            if filepath.exists():
                print(f"  已存在，跳过: {filename}")
                downloaded.append((base_name, str(filepath)))
                continue
            
            print(f"  下载中: {filename}...", end=" ")
            try:
                resp = requests.get(url, headers=headers, timeout=30)
                if resp.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(resp.content)
                    print(f"成功 ({len(resp.content) // 1024}KB)")
                    downloaded.append((base_name, str(filepath)))
                else:
                    print(f"失败")
            except Exception as e:
                print(f"失败: {e}")
            
            import time
            time.sleep(0.5)  # 避免请求过快
        
        return downloaded
    
    async def fetch_and_download(self, city: str, keyword: str, category: str, max_notes: int = 5) -> list:
        """搜索并下载图片"""
        print(f"\n📍 [{city}] 搜索关键词: {keyword}")
        
        downloaded = []
        async with XHSBrowser(headless=True) as browser:
            api_handler = XHSApiHandler(browser.context)
            
            # 搜索
            results = await api_handler.search(keyword, limit=20)
            print(f"  获取到 {len(results.items)} 条帖子")
            
            # 按点赞数排序，取热门帖子
            sorted_items = sorted(results.items, key=lambda x: x.liked_count, reverse=True)
            top_items = sorted_items[:max_notes]
            
            for item in top_items:
                if item.liked_count < 100:  # 跳过低赞帖子
                    continue
                
                print(f"\n  📝 处理帖子: {item.title}")
                print(f"     赞: {item.liked_count} | 收藏: {item.collect_count}")
                
                try:
                    # 获取详情获取所有图片
                    detail = await api_handler.get_note_detail(item.note_id, item.xsec_token)
                    
                    if detail.note and detail.note.image_list:
                        images = detail.note.image_list
                        print(f"     获取到 {len(images)} 张图片")
                        
                        # 生成文件名
                        base_name = self._sanitize_filename(f"{city}-{item.title}")
                        
                        # 下载图片（同步方法）
                        downloaded.extend(
                            self.download_images(images, city, category, base_name, max_images=2)
                        )
                    else:
                        print(f"     无图片或获取失败")
                        
                except Exception as e:
                    print(f"     处理失败: {e}")
                
                await asyncio.sleep(1)  # 避免请求过快
        
        # 保存到内存
        key = (city, category)
        if key not in self.downloaded_images:
            self.downloaded_images[key] = []
        self.downloaded_images[key].extend(downloaded)
        
        return downloaded
    
    async def run(self, city: str = None, max_notes: int = 5):
        """运行下载任务"""
        cities = [city] if city else list(CITIES_KEYWORDS.keys())
        
        for city in cities:
            if city not in CITIES_KEYWORDS:
                print(f"❌ 未知城市: {city}")
                continue
                
            keywords = CITIES_KEYWORDS[city]
            
            # 下载美食图片
            for keyword in keywords["food"]:
                await self.fetch_and_download(city, keyword, "food", max_notes)
            
            # 下载景点图片
            for keyword in keywords["spots"]:
                await self.fetch_and_download(city, keyword, "spots", max_notes)
        
        # 保存下载记录
        self.save_download_log()
        
    def save_download_log(self):
        """保存下载记录"""
        log_file = self.output_dir / "xhs_download_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.downloaded_images, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 下载记录已保存: {log_file}")


async def main():
    parser = argparse.ArgumentParser(description="小红书图片下载脚本")
    parser.add_argument("--city", type=str, help="指定城市（默认全部）", 
                       choices=list(CITIES_KEYWORDS.keys()))
    parser.add_argument("--max-notes", type=int, default=3, help="每个关键词最多处理帖子数")
    parser.add_argument("--output", type=str, default="images", help="输出目录")
    args = parser.parse_args()
    
    downloader = XHSImageDownloader(output_dir=args.output)
    await downloader.run(city=args.city, max_notes=args.max_notes)


if __name__ == "__main__":
    asyncio.run(main())
