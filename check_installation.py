"""
检查 videocut 环境安装状态
"""

import os
from pathlib import Path

def check_installation():
    print("=" * 60)
    print("📦 videocut 环境安装状态检查")
    print("=" * 60)

    # 检查 FunASR 模型
    print("\n🔍 检查 FunASR 模型 (~2GB)")
    modelscope_cache = Path.home() / ".cache" / "modelscope" / "hub" / "models"

    models = {
        "paraformer-zh": "iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "fsmn-vad": "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        "punc_ct": "iic/punc_ct-transformer_cn-en-common-vocab471067-large"
    }

    for name, path in models.items():
        model_path = modelscope_cache / path
        if model_path.exists():
            # 计算大小
            size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            print(f"  ✅ {name}: {size_mb:.1f} MB")
        else:
            print(f"  ⏳ {name}: 下载中...")

    # 检查 Whisper 模型
    print("\n🔍 检查 Whisper 模型 (~2.9GB)")
    whisper_cache = Path.home() / ".cache" / "whisper"
    whisper_model = whisper_cache / "large-v3.pt"

    if whisper_model.exists():
        size_mb = whisper_model.stat().st_size / (1024 * 1024)
        print(f"  ✅ large-v3: {size_mb:.1f} MB")
    else:
        print(f"  ⏳ large-v3: 下载中...")

    # 检查 FFmpeg
    print("\n🔍 检查 FFmpeg")
    import shutil
    if shutil.which("ffmpeg"):
        print(f"  ✅ FFmpeg: 已安装")
    else:
        print(f"  ❌ FFmpeg: 未找到")

    # 检查 Python 包
    print("\n🔍 检查 Python 包")
    packages = ["funasr", "modelscope", "whisper", "torchaudio"]
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_installation()
