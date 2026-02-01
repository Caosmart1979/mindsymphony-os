#!/usr/bin/env python3
"""
统一图像生成接口 - Article Illustrator 专用版
整合 Vertex AI Imagen 4 和 智谱 CogView，支持自动选择和批量生成
"""

import os
import sys
import argparse
import base64
import json
import requests
import time
import hmac
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Optional, Tuple

# ==================== 配置 ====================

class ImageGenConfig:
    """图像生成配置"""

    # Vertex AI Imagen 配置
    VERTEX_PROJECT = "iconic-nation-464314-n6"
    VERTEX_LOCATION = "us-central1"
    VERTEX_MODEL_ULTRA = "imagen-4.0-ultra-generate-001"
    VERTEX_MODEL_STANDARD = "imagen-4.0-generate-001"
    VERTEX_MODEL_FAST = "imagen-4.0-fast-generate-001"

    # 默认模型选择
    DEFAULT_MODEL = "vertex_ultra"  # options: vertex_ultra, vertex_standard, vertex_fast, zhipu

# ==================== Token 管理 ====================

class TokenManager:
    """Access Token 管理"""

    def __init__(self):
        self.vertex_token = None
        self.zhipu_api_key = None
        self._load_tokens()

    def _load_tokens(self):
        """加载所有 token"""
        # 多路径搜索 .env 文件
        possible_paths = [
            # 当前技能目录
            Path(__file__).parent.parent / ".env",
            # gemini-image-gen 技能目录
            Path("C:/Users/13466/.claude/skills/gemini-image-gen/.env"),
            Path.home() / ".claude" / "skills" / "gemini-image-gen" / ".env",
        ]

        for env_file in possible_paths:
            if env_file.exists():
                load_dotenv(env_file)
                print(f"✅ 加载配置: {env_file}")
                break

        # Vertex AI Token
        self.vertex_token = os.getenv("VERTEX_ACCESS_TOKEN")

        # 智谱 API Key
        zhipu_key = os.getenv("ZHIPU_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN", "")
        if zhipu_key and '.' in zhipu_key:
            self.zhipu_api_key = zhipu_key

    def get_vertex_token(self) -> Optional[str]:
        """获取 Vertex AI Token"""
        if not self.vertex_token:
            # 尝试从环境变量直接获取
            self.vertex_token = os.getenv("VERTEX_ACCESS_TOKEN")

        if self.vertex_token:
            # 简单验证 token 格式
            if not self.vertex_token.startswith("ya29."):
                print("⚠️ Vertex Token 格式可能无效，尝试刷新...")
                return None
        return self.vertex_token

    def get_zhipu_api_key(self) -> Optional[str]:
        """获取智谱 API Key"""
        if not self.zhipu_api_key:
            # 尝试从环境变量获取
            zhipu_key = os.getenv("ZHIPU_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN", "")
            if zhipu_key and '.' in zhipu_key:
                self.zhipu_api_key = zhipu_key
        return self.zhipu_api_key

# ==================== 图像生成器 ====================

class VertexImageGenerator:
    """Vertex AI Imagen 图像生成器"""

    def __init__(self, project: str, location: str, model: str = None):
        self.project = project
        self.location = location
        self.model = model or ImageGenConfig.VERTEX_MODEL_ULTRA

    def generate(self, prompt: str, token: str) -> Optional[bytes]:
        """生成图像"""
        url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project}/locations/{self.location}/publishers/google/models/{self.model}:predict"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1}
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=180)
            if response.status_code == 200:
                result = response.json()
                if "predictions" in result and result["predictions"]:
                    image_data = result["predictions"][0].get("bytesBase64Encoded")
                    if image_data:
                        return base64.b64decode(image_data)
            return None
        except Exception as e:
            print(f"Vertex AI 生成错误: {e}")
        return None

class ZhipuImageGenerator:
    """智谱 CogView 图像生成器"""

    def __init__(self):
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

    def _generate_jwt(self, api_key: str) -> str:
        """生成 JWT Token"""
        try:
            api_key_id, api_key_secret = api_key.split('.', 1)

            header = {"alg": "HS256", "sign_type": "SIGN"}
            payload = {
                "api_key": api_key_id,
                "exp": int(time.time()) + 3600,
                "timestamp": int(time.time())
            }

            def base64url_encode(data):
                if isinstance(data, str):
                    data = data.encode('utf-8')
                return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

            encoded_header = base64url_encode(json.dumps(header, separators=(',', ':')))
            encoded_payload = base64url_encode(json.dumps(payload, separators=(',', ':')))

            message = f"{encoded_header}.{encoded_payload}"
            signature = hmac.new(
                api_key_secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()

            encoded_signature = base64url_encode(signature)

            return f"{encoded_header}.{encoded_payload}.{encoded_signature}"
        except Exception as e:
            raise Exception(f"JWT 生成失败: {e}")

    def generate(self, prompt: str, api_key: str) -> Optional[bytes]:
        """生成图像"""
        jwt_token = self._generate_jwt(api_key)

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "cogview-3",
            "prompt": prompt
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=120)
            if response.status_code == 200:
                result = response.json()
                if "data" in result and result["data"]:
                    image_url = result["data"][0].get("url", "")
                    if image_url:
                        img_response = requests.get(image_url, timeout=60)
                        if img_response.status_code == 200:
                            return img_response.content
        except Exception as e:
            print(f"智谱生成错误: {e}")
        return None

# ==================== 主生成器 ====================

class UnifiedImageGenerator:
    """统一图像生成器"""

    def __init__(self, max_retries: int = 2, retry_delay: int = 5):
        self.token_manager = TokenManager()
        self.vertex_generator = VertexImageGenerator(
            ImageGenConfig.VERTEX_PROJECT,
            ImageGenConfig.VERTEX_LOCATION,
            ImageGenConfig.VERTEX_MODEL_ULTRA
        )
        self.zhipu_generator = ZhipuImageGenerator()

        # 统计信息
        self.stats = {
            "vertex_success": 0,
            "vertex_failed": 0,
            "zhipu_success": 0,
            "zhipu_failed": 0
        }

        # 重试配置
        self.max_retries = max_retries
        self.retry_delay = retry_delay  # 秒

    def _choose_provider(self) -> str:
        """选择最优图像生成方案"""
        # 优先级: Vertex Ultra > Vertex Standard > Zhipu
        if self.token_manager.get_vertex_token():
            return "vertex_ultra"
        if self.token_manager.get_zhipu_api_key():
            return "zhipu"
        raise Exception("没有可用的图像生成凭证")

    def generate(self, prompt: str, model: str = None, fallback: bool = True) -> Optional[Tuple[bytes, str]]:
        """
        生成图像（带重试机制）
        返回: (图像数据, 使用的提供者)
        """
        provider = model or self._choose_provider()
        last_error = None

        # 尝试 Vertex AI
        if provider.startswith("vertex"):
            token = self.token_manager.get_vertex_token()
            if token:
                for attempt in range(self.max_retries + 1):
                    try:
                        print(f"🎨 使用 Vertex AI Imagen ({provider})" +
                              (f" (尝试 {attempt + 1}/{self.max_retries + 1})" if attempt > 0 else ""))

                        image_data = self.vertex_generator.generate(prompt, token)
                        if image_data:
                            self.stats["vertex_success"] += 1
                            return image_data, provider

                        self.stats["vertex_failed"] += 1
                        last_error = "生成返回空结果"

                        # 还有重试次数，等待后重试
                        if attempt < self.max_retries:
                            import time
                            delay = self.retry_delay * (2 ** attempt)  # 指数退避
                            print(f"  ⚠️ {last_error}，{delay} 秒后重试...")
                            time.sleep(delay)

                    except Exception as e:
                        self.stats["vertex_failed"] += 1
                        last_error = str(e)

                        if attempt < self.max_retries:
                            import time
                            delay = self.retry_delay * (2 ** attempt)
                            print(f"  ⚠️ 错误: {e}，{delay} 秒后重试...")
                            time.sleep(delay)

                if not fallback:
                    return None, provider

        # 尝试智谱备用
        if provider == "zhipu" or (fallback and last_error):
            api_key = self.token_manager.get_zhipu_api_key()
            if api_key:
                for attempt in range(self.max_retries + 1):
                    try:
                        print(f"🎨 使用智谱 CogView" +
                              (f" (尝试 {attempt + 1}/{self.max_retries + 1})" if attempt > 0 else ""))

                        image_data = self.zhipu_generator.generate(prompt, api_key)
                        if image_data:
                            self.stats["zhipu_success"] += 1
                            return image_data, "zhipu"

                        self.stats["zhipu_failed"] += 1
                        last_error = "智谱生成返回空结果"

                        if attempt < self.max_retries:
                            import time
                            delay = self.retry_delay * (2 ** attempt)
                            print(f"  ⚠️ {last_error}，{delay} 秒后重试...")
                            time.sleep(delay)

                    except Exception as e:
                        self.stats["zhipu_failed"] += 1
                        last_error = str(e)

                        if attempt < self.max_retries:
                            import time
                            delay = self.retry_delay * (2 ** attempt)
                            print(f"  ⚠️ 错误: {e}，{delay} 秒后重试...")
                            time.sleep(delay)

        return None, provider

    def generate_batch(self, prompts: List[str], model: str = None, output_dir: str = "imgs") -> List[Dict]:
        """
        批量生成图像
        返回: 生成结果列表
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []

        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{len(prompts)}] 生成图像...")

            # 生成图像
            image_data, provider = self.generate(prompt, model)

            if image_data:
                # 保存图像
                filename = f"image_{i:03d}.png"
                file_path = output_path / filename

                with open(file_path, "wb") as f:
                    f.write(image_data)

                size_kb = len(image_data) / 1024

                print(f"✅ 成功 - {filename} ({size_kb:.1f} KB) - 使用 {provider}")

                results.append({
                    "index": i,
                    "filename": filename,
                    "path": str(file_path),
                    "size_kb": size_kb,
                    "provider": provider
                })
            else:
                print(f"❌ 失败 - 图像 {i}")

        # 输出统计
        print(f"\n=== 生成统计 ===")
        print(f"Vertex AI: {self.stats['vertex_success']} 成功, {self.stats['vertex_failed']} 失败")
        print(f"智谱: {self.stats['zhipu_success']} 成功, {self.stats['zhipu_failed']} 失败")
        print(f"总计: {len(results)}/{len(prompts)} 成功")

        return results

# ==================== CLI 接口 ====================

def main():
    parser = argparse.ArgumentParser(
        description="统一图像生成工具 - Article Illustrator 专用版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
模型选项:
  vertex-ultra   Vertex AI Imagen 4 Ultra (最高质量，推荐)
  vertex-std     Vertex AI Imagen 4 (标准质量)
  vertex-fast    Vertex AI Imagen 4 Fast (快速)
  zhipu          智谱 CogView (备用)

示例:
  python generate_unified.py "A beautiful sunset"
  python generate_unified.py "A cat" --model zhipu
  python generate_unified.py "Abstract art" --output art.png
        """
    )

    parser.add_argument("prompt", help="图像描述（必需）")
    parser.add_argument("-o", "--output", default="generated_image.png",
                        help="输出文件路径（默认: generated_image.png）")
    parser.add_argument("--model",
                        choices=["vertex-ultra", "vertex-std", "vertex-fast", "zhipu"],
                        help="图像生成模型（默认: vertex-ultra）")

    args = parser.parse_args()

    # 创建生成器
    generator = UnifiedImageGenerator()

    # 生成单张图像
    image_data, provider = generator.generate(args.prompt, args.model)

    if image_data:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(image_data)

        size_kb = len(image_data) / 1024
        print(f"\n✅ 图像已保存: {output_path.absolute()}")
        print(f"   大小: {size_kb:.1f} KB")
        print(f"   提供者: {provider}")
    else:
        print("\n❌ 图像生成失败")
        print("\n请检查:")
        print("1. Vertex AI Token 是否有效（运行 python scripts/get_token.py 刷新）")
        print("2. 智谱账户是否有余额")

if __name__ == "__main__":
    main()
