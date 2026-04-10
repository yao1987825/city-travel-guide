"""
小红书价格信息获取脚本
"""
import asyncio
import json
import sys
from pathlib import Path

# 修复编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))
from xhs_utils.browser import XHSBrowser
from xhs_utils.api_handler import XHSApiHandler


async def search_notes(keyword, limit=10):
    """搜索帖子"""
    async with XHSBrowser(headless=True) as browser:
        api_handler = XHSApiHandler(browser.context)
        results = await api_handler.search(keyword, limit=limit)
        return results.items


async def get_note_detail(note_id, xsec_token):
    """获取帖子详情"""
    async with XHSBrowser(headless=True) as browser:
        api_handler = XHSApiHandler(browser.context)
        detail = await api_handler.get_note_detail(note_id, xsec_token)
        return detail


async def main():
    print('=== 小红书价格信息获取 ===\n')
    
    # 1. 郴州美食价格
    print('[1] 搜索郴州美食价格...')
    food_items = await search_notes('郴州必吃美食价格', limit=10)
    
    food_prices = []
    for item in food_items[:5]:
        if item.liked_count > 50:
            food_prices.append({
                'title': item.title,
                'liked': item.liked_count,
                'note_id': item.note_id,
                'token': item.xsec_token
            })
    
    print(f'找到 {len(food_prices)} 个美食帖子')
    
    # 2. 郴州景点门票
    print('\n[2] 搜索郴州景点门票价格...')
    spot_items = await search_notes('郴州景点门票价格', limit=10)
    
    spot_prices = []
    for item in spot_items[:5]:
        if item.liked_count > 50:
            spot_prices.append({
                'title': item.title,
                'liked': item.liked_count,
                'note_id': item.note_id,
                'token': item.xsec_token
            })
    
    print(f'找到 {len(spot_prices)} 个景点帖子')
    
    # 3. 获取详情提取价格
    print('\n[3] 获取详细价格信息...')
    
    all_prices = {'food': [], 'spots': []}
    
    for item in food_prices[:3]:
        print(f"\n美食: {item['title']}")
        try:
            detail = await get_note_detail(item['note_id'], item['token'])
            if detail.note:
                desc = detail.note.desc or ''
                # 提取价格信息
                import re
                prices = re.findall(r'[人均约]?[¥￥]?\d+[-到至]?\d*[元]?', desc)
                all_prices['food'].append({
                    'title': item['title'],
                    'desc_preview': desc[:200] if desc else '',
                    'prices': prices[:5],
                    'liked': item['liked']
                })
                print(f"  价格: {prices[:3] if prices else '未提取'}")
        except Exception as e:
            print(f"  错误: {e}")
    
    for item in spot_prices[:3]:
        print(f"\n景点: {item['title']}")
        try:
            detail = await get_note_detail(item['note_id'], item['token'])
            if detail.note:
                desc = detail.note.desc or ''
                import re
                prices = re.findall(r'[门票票]?[¥￥]?\d+[-到至]?\d*[元]?', desc)
                all_prices['spots'].append({
                    'title': item['title'],
                    'desc_preview': desc[:200] if desc else '',
                    'prices': prices[:5],
                    'liked': item['liked']
                })
                print(f"  价格: {prices[:3] if prices else '未提取'}")
        except Exception as e:
            print(f"  错误: {e}")
    
    # 保存结果
    output_file = Path(__file__).parent.parent / 'references' / 'xhs_price_data.json'
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_prices, f, ensure_ascii=False, indent=2)
    
    print(f'\n价格数据已保存: {output_file}')


if __name__ == '__main__':
    asyncio.run(main())
