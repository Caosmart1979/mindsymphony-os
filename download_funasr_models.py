"""
下载 FunASR 模型用于口误识别
模型总计约 2GB:
- paraformer-zh: 953MB (语音识别)
- punc_ct: 1.1GB (标点预测)
- fsmn-vad: 4MB (语音活动检测)
"""

from funasr import AutoModel

print("开始下载 FunASR 模型...")
print("这可能需要几分钟时间（取决于网络速度）")
print("模型大小: ~2GB\n")

# 下载模型（首次运行会自动下载到 ~/.cache/modelscope/）
model = AutoModel(
    model="paraformer-zh",
    vad_model="fsmn-vad",
    punc_model="ct-punc",
)

print("\n✅ FunASR 模型下载完成!")
print("模型已缓存到: ~/.cache/modelscope/")
