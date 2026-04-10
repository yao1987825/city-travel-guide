#!/usr/bin/env python3
"""
更新 cities_data.md 中的图片路径，确保与 GitHub 仓库中的实际文件名匹配
"""

import re

# 图片路径映射表
IMAGE_MAPPING = {
    # 郴州景点
    '%E4%B8%9C%E6%B1%9F%E6%B9%96%E9%9B%BE%E6%BC%AB%E5%B0%8F%E4%B8%9C%E6%B1%9F_1.jpg': '%E9%83%B4%E5%B7%9E-%E4%B8%9C%E6%B1%9F%E6%B9%96.jpg',
    '%E9%AB%98%E6%A4%85%E5%B2%AD_1.jpg': '%E9%83%B4%E5%B7%9E-%E9%AB%98%E6%A4%85%E5%B2%AD.jpg',
    '%E8%8B%8F%E4%BB%99%E5%B2%AD_1.jpg': '%E9%83%B4%E5%B7%9E-%E8%8B%8F%E4%BB%99%E5%B2%AD.jpg',
    # 封面图
    '%E9%83%B4%E5%B7%9E-%E5%B0%81%E9%9D%A2.jpg': '%E9%83%B4%E5%B7%9E-%E5%B0%81%E9%9D%A2.jpg',
}

def update_image_paths(content):
    """更新图片路径"""
    for old_path, new_path in IMAGE_MAPPING.items():
        old_url = f'https://raw.githubusercontent.com/yao1987825/city-travel-guide/main/images/{old_path}'
        new_url = f'https://raw.githubusercontent.com/yao1987825/city-travel-guide/main/images/{new_path}'
        content = content.replace(old_url, new_url)
    return content

if __name__ == '__main__':
    input_file = 'references/cities_data.md'
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = update_image_paths(content)
    
    if content != original:
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'已更新 {input_file} 中的图片路径')
    else:
        print('未发现需要更新的图片路径')
