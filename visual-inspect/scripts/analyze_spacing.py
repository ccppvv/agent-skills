# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
分析设计中的间距模式
输出常用的间距值和可能的间距系统
"""

import re
from collections import Counter


def analyze_spacing(values):
    """分析间距值并识别模式"""
    counter = Counter(values)

    # 检测是否为 4px/8px 基准
    base = min(v for v in values if v > 0)

    print(f'检测基准: {base}px')
    print(f'\n常用间距值:')
    for value, count in counter.most_common(10):
        print(f'  {value}px: 使用 {count} 次')

    return base


def extract_from_css(css_content):
    """从 CSS 中提取间距值"""
    pattern = r'(padding|margin|gap):\s*(\d+)px'
    matches = re.findall(pattern, css_content)
    return [int(m[1]) for m in matches]


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python analyze_spacing.py <style.css>')
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        css = f.read()

    spacing_values = extract_from_css(css)
    if spacing_values:
        analyze_spacing(spacing_values)
    else:
        print('未找到间距值')
