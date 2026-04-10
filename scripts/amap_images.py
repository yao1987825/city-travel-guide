"""
高德地图 POI 图片获取工具
========================
使用高德地图 Web 服务 API 搜索景点/美食 POI，提取并下载实景图片。

使用方法：
    python scripts/amap_images.py --city 郴州 --keyword 东江湖
    python scripts/amap_images.py --city 郴州 --keyword 栖凤渡鱼粉 --save-img

API Key 配置：
    1. 前往 https://console.amap.com/dev/key/app 创建应用，获取 Web 服务 Key
    2. 将 Key 填入下方 AMAP_KEY 常量
"""

import urllib.request
import urllib.parse
import json
import os
import ssl

# ════════════════════════════════════════════════════
# ⚠️  请在此处填入您的高德地图 Web 服务 Key
# ════════════════════════════════════════════════════
# 从 amap_config.py 读取 Key（优先）
try:
    import sys, os
    _cfg_path = os.path.join(os.path.dirname(__file__), "amap_config.py")
    if os.path.exists(_cfg_path):
        with open(_cfg_path) as _f:
            for _line in _f:
                if _line.strip().startswith("AMAP_KEY") and "=" in _line:
                    AMAP_KEY = _line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
except Exception:
    pass

if not AMAP_KEY:
    print("⚠️ 未配置高德地图 API Key，无法获取实时图片")

# API 基础地址
BASE_URL = "https://restapi.amap.com/v3/place/text"

# 图片保存目录（相对于 Skill 根目录）
IMG_DIR = "references/images"


def search_poi(keyword, city="", citylimit=True, offset=5):
    """搜索 POI，返回前 N 条结果（含图片 URL）"""
    if not AMAP_KEY:
        print("⚠️ 未配置高德地图 API Key，无法获取实时图片")
        print("   请前往 https://console.amap.com/dev/key/app 申请 Key 并填入脚本顶部 AMAP_KEY")
        return []

    params = {
        "key": AMAP_KEY,
        "keywords": keyword,
        "city": city,
        "citylimit": "true" if citylimit else "false",
        "offset": offset,
        "page": 1,
        "output": "json",
        "types": "",  # 可填如"风景名胜|餐饮服务"等，留空全匹配
    }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}?{query}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            data = json.loads(r.read())

        if data.get("status") != "1":
            print(f"❌ API 错误: {data.get('info', 'Unknown error')}")
            return []

        pois = data.get("pois", [])
        results = []
        for poi in pois:
            photos = poi.get("photos", [])
            photo_urls = [p.get("url", "") for p in photos if p.get("url")]
            results.append({
                "name": poi.get("name", ""),
                "address": poi.get("address", ""),
                "location": poi.get("location", ""),
                "type": poi.get("type", ""),
                "photos": photo_urls,
                "photo_count": len(photo_urls),
                "id": poi.get("id", ""),
            })
        return results

    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []


def download_image(url, save_path):
    """下载图片到本地"""
    if not url:
        return False
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            data = r.read()
        with open(save_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"  ⚠️ 下载失败: {e}")
        return False


def search_and_save(keyword, city, save_dir=None, max_photos=2):
    """
    搜索 POI 并打印图片 URL（用于查看/调试）
    如果传入 save_dir，则下载图片到本地
    """
    print(f"\n🔍 搜索: [{city}] {keyword}")
    results = search_poi(keyword, city)

    if not results:
        print("  未找到结果")
        return

    for poi in results:
        print(f"\n📍 {poi['name']}")
        if poi.get("address"):
            print(f"   地址: {poi['address']}")
        if poi.get("location"):
            print(f"   坐标: {poi['location']}")
        print(f"   图片数量: {poi['photo_count']}")

        for i, url in enumerate(poi["photos"][:max_photos]):
            print(f"   📷 [{i+1}] {url}")
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
                safe_name = "".join(c for c in poi["name"] if c.isalnum() or c in (" ", "-", "_")).strip()
                fname = f"{safe_name}_{i+1}.jpg"
                fpath = os.path.join(save_dir, fname)
                ok = download_image(url, fpath)
                if ok:
                    print(f"   ✅ 已保存: {fpath}")


def get_poi_images(keyword, city=""):
    """
    获取 POI 图片 URL 列表
    返回格式: [{"name": "...", "url": "..."}, ...]
    供 Skill 调用，返回第一张图片 URL
    """
    results = search_poi(keyword, city, offset=3)
    images = []
    for poi in results:
        for photo_url in poi.get("photos", []):
            images.append({
                "name": poi["name"],
                "url": photo_url,
            })
    return images


# ════════════════════════════════════════════════════
# 命令行入口
# ════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="高德地图 POI 图片获取工具")
    parser.add_argument("--city", default="", help="城市名（可选，精确匹配）")
    parser.add_argument("--keyword", default="", help="搜索关键词（景点/美食名）")
    parser.add_argument("--save-img", action="store_true", help="是否下载图片到本地")
    parser.add_argument("--list", help="关键词列表文件（每行一个），批量搜索")
    args = parser.parse_args()

    if args.list and os.path.exists(args.list):
        with open(args.list, encoding="utf-8") as f:
            keywords = [line.strip() for line in f if line.strip()]
    elif args.keyword:
        keywords = [args.keyword]
    else:
        print("请提供 --keyword 或 --list 参数")
        exit(1)

    save_dir = IMG_DIR if args.save_img else None

    for kw in keywords:
        search_and_save(kw, args.city, save_dir)

    print("\n✅ 全部完成")
