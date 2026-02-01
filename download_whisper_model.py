"""
下载 Whisper large-v3 模型用于字幕生成
模型大小: 2.9GB
"""

import whisper

print("开始下载 Whisper large-v3 模型...")
print("这可能需要几分钟时间（取决于网络速度）")
print("模型大小: ~2.9GB\n")

# 下载模型（首次运行会自动下载到 ~/.cache/whisper/）
model = whisper.load_model("large-v3")

print("\n✅ Whisper large-v3 模型下载完成!")
print("模型已缓存到: ~/.cache/whisper/")
