#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Gemini API 分析视频文件
"""
import os
import sys
import io
import requests
import base64
import mimetypes

# 设置 stdout 为 UTF-8 编码（Windows 兼容）
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API 配置
API_KEY = "AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg"
MODEL = "gemini-2.5-flash"  # 支持多模态的模型

# 代理设置
PROXIES = {
    "https": "http://127.0.0.1:7897",
    "http": "http://127.0.0.1:7897",
}

def analyze_video(video_path: str):
    """分析视频文件"""

    # 读取视频文件
    print(f"正在读取视频文件: {video_path}")
    with open(video_path, "rb") as f:
        video_data = f.read()

    file_size = len(video_data)
    print(f"文件大小: {file_size / 1024 / 1024:.2f} MB")

    # Gemini API 需要 base64 编码的 MIME 类型
    mime_type, _ = mimetypes.guess_type(video_path)
    if not mime_type:
        mime_type = "video/mp4"

    # 构建 API 请求
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [
                {
                    "text": "请详细分析这个视频的内容，包括：1) 视频主题和主要内容 2) 关键场景和人物 3) 任何可见的文字信息 4) 视频风格和制作质量 5) 其他值得注意的细节。请用中文回答。"
                },
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": base64.b64encode(video_data).decode('utf-8')
                    }
                }
            ]
        }]
    }

    print("正在调用 Gemini API...")
    try:
        response = requests.post(url, json=payload, proxies=PROXIES, timeout=300)

        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "API 返回了空响应"
        else:
            return f"API 错误 ({response.status_code}): {response.text}"

    except Exception as e:
        return f"请求失败: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_video.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "video_analysis_result.txt"

    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        sys.exit(1)

    result = analyze_video(video_path)

    # 保存到文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("视频分析结果\n")
        f.write("="*60 + "\n\n")
        f.write(result)

    print(f"Analysis complete! Results saved to: {output_file}")
