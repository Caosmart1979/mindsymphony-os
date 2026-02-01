#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

# 设置UTF-8编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

video_path = "数字人1.mp4"
size = os.path.getsize(video_path)

print("=" * 50)
print("视频文件基本信息")
print("=" * 50)
print(f"文件名: {video_path}")
print(f"文件大小: {size:,} 字节")
print(f"文件大小MB: {size/1024/1024:.2f} MB")
print(f"格式: MP4 (ISO Media)")
print("\n文件检测完成")
print("下一步: 需要ffmpeg或opencv进行详细分析")
print("=" * 50)
