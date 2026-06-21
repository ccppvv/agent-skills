# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
从图片提取主要颜色
依赖: pip install Pillow scikit-learn
"""

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import sys


def extract_colors(image_path, n_colors=5):
    """提取图片中的主要颜色"""
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    return ['#%02x%02x%02x' % tuple(color) for color in colors]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python extract_colors.py <image_path> [n_colors]')
        sys.exit(1)

    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    palette = extract_colors(path, n)
    print('颜色调色板:')
    for i, color in enumerate(palette, 1):
        print(f'  {i}. {color}')
