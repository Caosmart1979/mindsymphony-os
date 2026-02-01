"""
验证 videocut 环境是否安装完成并可以正常使用
"""

import sys
from pathlib import Path

def check_environment():
    print("=" * 60)
    print("🔍 videocut 环境验证")
    print("=" * 60)

    all_good = True

    # 1. 检查 Python 包
    print("\n1️⃣  检查 Python 包")
    packages = {
        "funasr": "FunASR (口误识别)",
        "modelscope": "ModelScope (模型下载)",
        "whisper": "Whisper (字幕生成)",
        "torchaudio": "TorchAudio (音频处理)"
    }

    for pkg, desc in packages.items():
        try:
            __import__(pkg)
            print(f"  ✅ {desc}")
        except ImportError as e:
            print(f"  ❌ {desc}: {e}")
            all_good = False

    # 2. 检查 FunASR 模型
    print("\n2️⃣  检查 FunASR 模型")
    modelscope_cache = Path.home() / ".cache" / "modelscope" / "hub" / "models"

    required_models = {
        "paraformer-zh": "iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "fsmn-vad": "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        "punc_ct": "iic/punc_ct-transformer_cn-en-common-vocab471067-large"
    }

    for name, path in required_models.items():
        model_path = modelscope_cache / path
        if model_path.exists() and (model_path / "model.pt").exists():
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name}: 模型未完全下载")
            all_good = False

    # 3. 检查 Whisper 模型
    print("\n3️⃣  检查 Whisper 模型")
    whisper_cache = Path.home() / ".cache" / "whisper"
    whisper_model = whisper_cache / "large-v3.pt"

    if whisper_model.exists():
        size_gb = whisper_model.stat().st_size / (1024**3)
        print(f"  ✅ large-v3 ({size_gb:.2f} GB)")
    else:
        print(f"  ❌ large-v3: 模型未下载")
        all_good = False

    # 4. 检查 FFmpeg
    print("\n4️⃣  检查 FFmpeg")
    import shutil
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"  ✅ FFmpeg: {ffmpeg_path}")
    else:
        print(f"  ❌ FFmpeg: 未安装或不在 PATH 中")
        all_good = False

    # 总结
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 环境验证通过！videocut 已就绪。")
        print("\n可以开始使用：")
        print("  - /videocut:剪口播  (转录 + 口误识别)")
        print("  - /videocut:剪辑    (执行剪辑)")
        print("  - /videocut:字幕    (生成字幕)")
        return 0
    else:
        print("⚠️  环境未完全就绪，请检查上述错误项。")
        return 1

if __name__ == "__main__":
    sys.exit(check_environment())
