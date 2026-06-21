# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Design Tokens 更新脚本
功能：检测新 Tokens 并追加到 design-tokens.md
"""

import re
import sys
from datetime import datetime
from pathlib import Path


# Token 类别和规则
TOKEN_RULES = {
    'color': {
        'pattern': r'#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})',
        'min_count': 2,
        'prefix': 'color',
        'unit': '',
    },
    'spacing': {
        'pattern': r'(\d+)px',
        'min_count': 1,
        'prefix': 'spacing',
        'unit': 'px',
        'valid_values': [4, 8, 12, 16, 20, 24, 32, 40, 48, 64],
    },
    'font-size': {
        'pattern': r'font-size:\s*(\d+)px',
        'min_count': 1,
        'prefix': 'font-size',
        'unit': 'px',
        'valid_values': [12, 14, 16, 18, 20, 24, 28, 32],
    },
    'radius': {
        'pattern': r'border-radius:\s*(\d+)px',
        'min_count': 1,
        'prefix': 'radius',
        'unit': 'px',
        'valid_values': [4, 8, 12, 16, 20, 24],
    },
}


def parse_design_tokens_md(filepath):
    """解析现有的 design-tokens.md，提取已记录的 Tokens"""
    if not Path(filepath).exists():
        return {}

    content = Path(filepath).read_text()
    tokens = {}

    # 匹配 `token.name` = value
    pattern = r'`([a-z-]+)\.\w+`\s*=\s*([#\w\d()]+)'
    for match in re.finditer(pattern, content):
        name, value = match.groups()
        tokens[value] = name

    return tokens


def extract_tokens_from_css(css_content):
    """从 CSS 内容中提取潜在的 Tokens"""
    extracted = {}

    for category, rules in TOKEN_RULES.items():
        found = re.findall(rules['pattern'], css_content)
        found = [int(f) if f.isdigit() else f for f in found]

        # 过滤有效值
        if 'valid_values' in rules:
            found = [f for f in found if f in rules['valid_values']]

        # 计数
        from collections import Counter
        counts = Counter(found)

        # 只保留达到最小出现次数的值
        for value, count in counts.items():
            if count >= rules['min_count']:
                str_value = f"{value}{rules.get('unit', '')}"
                if category not in extracted:
                    extracted[category] = {}
                extracted[category][str_value] = count

    return extracted


def generate_token_name(category, value, existing_tokens, index):
    """生成 Token 名称"""
    if category == 'color':
        # 尝试根据颜色推断用途
        color_names = {
            '#FFFFFF': 'white', '#000000': 'black',
            '#FF0000': 'red', '#00FF00': 'green', '#0000FF': 'blue',
        }
        if value in color_names:
            base = color_names[value]
        else:
            base = f"accent-{index}"
    elif category == 'spacing':
        size_names = {4: 'xs', 8: 'sm', 16: 'md', 24: 'lg', 32: 'xl'}
        base = size_names.get(int(value), f'{index}')
    elif category == 'font-size':
        size_names = {12: 'xs', 14: 'sm', 16: 'md', 18: 'lg', 20: 'xl', 24: '2xl'}
        base = size_names.get(int(value), f'{index}')
    elif category == 'radius':
        size_names = {4: 'sm', 8: 'md', 12: 'lg', 16: 'xl'}
        base = size_names.get(int(value), f'{index}')
    else:
        base = f'{index}'

    token_name = f"{category}.{base}"

    # 检查是否已存在
    while token_name in existing_tokens.values():
        base = f"{base}-{index}"
        token_name = f"{category}.{base}"
        index += 1

    return token_name


def append_new_tokens(token_file, new_tokens):
    """追加新 Tokens 到 design-tokens.md"""
    content = Path(token_file).read_text()

    # 找到对应的分类并追加
    lines = content.split('\n')
    category_sections = {}

    for i, line in enumerate(lines):
        if line.startswith('## '):
            category = line[3:].split()[0].lower()
            category_sections[category] = i

    # 在每个分类下追加新 Tokens
    for category, tokens in new_tokens.items():
        section_key = None
        for key in category_sections:
            if key in category or category in key:
                section_key = key
                break

        if section_key:
            insert_pos = category_sections[section_key] + 1
            # 跳过标题和空行
            while insert_pos < len(lines) and not lines[insert_pos].startswith('- '):
                insert_pos += 1

            # 插入新 Tokens
            for token_name, token_value in tokens:
                lines.insert(insert_pos, f"- `{token_name}` = {token_value} - 新增")
                insert_pos += 1

    # 更新记录
    today = datetime.now().strftime('%Y-%m-%d')
    record_added = False
    for i, line in enumerate(lines):
        if line.startswith('| ' + today):
            # 在现有记录中添加
            lines[i] = line.rstrip() + f', {len(new_tokens)} 个新 Tokens |'
            record_added = True
            break

    if not record_added:
        # 找到记录表格位置
        for i, line in enumerate(lines):
            if line.startswith('| 日期'):
                table_start = i
                # 跳过表头
                while table_start < len(lines) and lines[table_start].startswith('|'):
                    table_start += 1
                lines.insert(table_start, f"| {today} | {', '.join(new_tokens.keys())} | 自动提取 |")
                break

    Path(token_file).write_text('\n'.join(lines))


def main():
    if len(sys.argv) < 2:
        print('Usage: python update_tokens.py <design-tokens.md> [--extract-from <css_file>]')
        sys.exit(1)

    token_file = Path(sys.argv[1])
    css_file = None

    if '--extract-from' in sys.argv:
        idx = sys.argv.index('--extract-from')
        if idx + 1 < len(sys.argv):
            css_file = Path(sys.argv[idx + 1])

    # 解析现有 Tokens
    existing = parse_design_tokens_md(token_file)

    new_tokens = {}

    if css_file and css_file.exists():
        # 从 CSS 提取
        css_content = css_file.read_text()
        extracted = extract_tokens_from_css(css_content)

        for category, values in extracted.items():
            for value, count in values.items():
                if value not in existing:
                    if category not in new_tokens:
                        new_tokens[category] = []
                    token_name = generate_token_name(category, value, existing, len(new_tokens.get(category, [])) + 1)
                    new_tokens[category].append((token_name, value))

    # 如果有新 Tokens，追加到文件
    if new_tokens:
        append_new_tokens(token_file, new_tokens)
        print(f'✅ 已追加 {sum(len(v) for v in new_tokens.values())} 个新 Tokens 到 {token_file}')
        for category, tokens in new_tokens.items():
            print(f'\n  {category}:')
            for name, value in tokens:
                print(f'    - {name} = {value}')
    else:
        print('ℹ️  没有发现新的 Tokens')


if __name__ == '__main__':
    main()
