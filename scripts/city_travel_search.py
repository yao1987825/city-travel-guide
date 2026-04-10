#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
city_travel_search.py
用途：从 references/ 数据文件中按城市、类别快速检索旅游信息
执行方式：python city_travel_search.py --city 郴州 --type food
"""

import argparse
import os
import re
import sys


CITY_LIST = ["郴州", "清远", "衡阳", "长沙", "益阳", "韶关", "深圳"]

TYPE_MAP = {
    "attraction": ["必去景点", "推荐", "🗺️", "最值得去"],
    "food": ["美食", "特色美食", "🍜", "不容错过的餐厅"],
    "pitfall": ["避坑", "⚠️", "坑点", "深度避坑"],
    "recommend": ["推荐精选", "隐藏宝藏", "🌟", "🏆"],
    "budget": ["消费档次", "💰", "日均花费"],
    "all": [],   # 全部返回
}

REFERENCES_DIR = os.path.join(os.path.dirname(__file__), "..", "references")


def load_file(filename: str) -> str:
    path = os.path.join(REFERENCES_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_city_section(content: str, city: str) -> str:
    """从 Markdown 中提取指定城市的章节内容（二级标题到下一个二级标题）"""
    pattern = rf"(##\s+[一二三四五六七]、{city}.+?)(?=\n## [一二三四五六七]、|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    # 尝试推荐文件格式
    pattern2 = rf"(## {city}精选推荐.+?)(?=\n## \w+精选推荐|\Z)"
    match2 = re.search(pattern2, content, re.DOTALL)
    if match2:
        return match2.group(1).strip()
    return ""


def extract_pitfall_section(content: str, city: str) -> str:
    """从避坑文件中提取指定城市的避坑内容"""
    pattern = rf"(### {city}\n.+?)(?=\n### \w+\n|\n---|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def filter_by_type(section_text: str, query_type: str) -> str:
    """按类型过滤章节中的特定块"""
    if query_type == "all":
        return section_text

    keywords = TYPE_MAP.get(query_type, [])
    if not keywords:
        return section_text

    lines = section_text.split("\n")
    result_blocks = []
    current_block = []
    in_block = False

    for line in lines:
        # 检测标题行是否包含关键词
        is_header = line.startswith("#")
        if is_header:
            if current_block and in_block:
                result_blocks.append("\n".join(current_block))
            current_block = [line]
            in_block = any(kw in line for kw in keywords)
        else:
            current_block.append(line)

    if current_block and in_block:
        result_blocks.append("\n".join(current_block))

    return "\n\n".join(result_blocks) if result_blocks else section_text


def search(city: str = None, query_type: str = "all", keyword: str = None) -> str:
    """
    主搜索函数
    :param city: 城市名（可为None，搜索全部城市）
    :param query_type: attraction/food/pitfall/recommend/budget/all
    :param keyword: 自由搜索关键词
    :return: 格式化结果字符串
    """
    results = []

    cities_data = load_file("cities_data.md")
    pitfalls_data = load_file("pitfalls_and_tips.md")
    recommend_data = load_file("recommendations.md")

    target_cities = [city] if city else CITY_LIST

    for c in target_cities:
        city_result_parts = []

        # 从 cities_data 提取城市章节
        city_section = extract_city_section(cities_data, c)
        if city_section:
            if query_type in ("all", "attraction", "food", "budget"):
                city_result_parts.append(filter_by_type(city_section, query_type))

        # 从 recommendations 提取推荐
        if query_type in ("all", "recommend"):
            rec_section = extract_city_section(recommend_data, c)
            if not rec_section:
                # 尝试另一种格式
                rec_pattern = rf"(## {c}精选推荐.+?)(?=\n## |\Z)"
                rec_match = re.search(rec_pattern, recommend_data, re.DOTALL)
                rec_section = rec_match.group(1).strip() if rec_match else ""
            if rec_section:
                city_result_parts.append(rec_section)

        # 从 pitfalls 提取避坑
        if query_type in ("all", "pitfall"):
            pit_section = extract_pitfall_section(pitfalls_data, c)
            if pit_section:
                city_result_parts.append(pit_section)

        # 关键词过滤
        if keyword:
            filtered = []
            for part in city_result_parts:
                kw_lower = keyword.lower()
                lines = part.split("\n")
                matched_lines = []
                context_active = False
                for i, line in enumerate(lines):
                    if kw_lower in line.lower():
                        context_active = True
                    if context_active:
                        matched_lines.append(line)
                        if len(matched_lines) > 10:
                            context_active = False
                if matched_lines:
                    filtered.append("\n".join(matched_lines))
            city_result_parts = filtered

        if city_result_parts:
            results.append(f"\n{'='*60}\n# {c} 旅游信息\n{'='*60}\n")
            results.append("\n\n".join(city_result_parts))

    if not results:
        return f"未找到关于 {'、'.join(target_cities)} 的 [{query_type}] 类型信息。"

    return "\n".join(results)


def count_attractions(city: str = None) -> dict:
    """统计各城市景点数量，验证是否满足15个以上"""
    cities_data = load_file("cities_data.md")
    target_cities = [city] if city else CITY_LIST
    counts = {}
    for c in target_cities:
        section = extract_city_section(cities_data, c)
        # 统计以数字序号开头的景点条目
        matches = re.findall(r"^\d+\.\s+\*\*", section, re.MULTILINE)
        counts[c] = len(matches)
    return counts


def main():
    parser = argparse.ArgumentParser(
        description="七城旅游信息检索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python city_travel_search.py --city 郴州
  python city_travel_search.py --city 长沙 --type food
  python city_travel_search.py --city 韶关 --type pitfall
  python city_travel_search.py --type recommend
  python city_travel_search.py --keyword 温泉
  python city_travel_search.py --count
        """
    )
    parser.add_argument("--city", type=str, help=f"目标城市，可选：{'/'.join(CITY_LIST)}，不填=全部城市")
    parser.add_argument("--type", type=str, default="all",
                        choices=list(TYPE_MAP.keys()),
                        help="信息类型: attraction/food/pitfall/recommend/budget/all（默认all）")
    parser.add_argument("--keyword", type=str, help="自由搜索关键词")
    parser.add_argument("--count", action="store_true", help="统计各城市景点数量")

    args = parser.parse_args()

    if args.count:
        counts = count_attractions(args.city)
        print("\n各城市景点数量统计：")
        print("-" * 30)
        for city_name, cnt in counts.items():
            status = "✅" if cnt >= 15 else "❌"
            print(f"  {status} {city_name}: {cnt} 个景点")
        total = sum(counts.values())
        print(f"\n  合计：{total} 个景点")
        return

    result = search(
        city=args.city,
        query_type=args.type,
        keyword=args.keyword
    )
    print(result)


if __name__ == "__main__":
    main()
