#!/usr/bin/env python3
"""
文章配图批量生成脚本
读取配图方案文件，批量生成所有插图
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict

# 添加 scripts 目录到路径
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from generate_unified import UnifiedImageGenerator

class PromptFile:
    """提示词文件管理"""

    @staticmethod
    def load_from_json(json_path: str) -> List[Dict]:
        """从 JSON 文件加载提示词"""
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def load_from_markdown(md_path: str) -> List[Dict]:
        """从 Markdown 配图方案提取提示词"""
        content = Path(md_path).read_text(encoding='utf-8')
        prompts = []

        lines = content.split('\n')
        current_prompt = None

        for line in lines:
            line = line.strip()

            # 检测图片条目
            if line.startswith('| **') and '** |' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    filename = parts[1].replace('**', '').strip()
                    description = parts[2]

                    if current_prompt and filename.startswith('image_'):
                        prompts.append({
                            'filename': filename,
                            'description': description,
                            'prompt': current_prompt
                        })
                        current_prompt = None

            # 检测提示词标记
            elif line.startswith('> **提示词**:'):
                current_prompt = line.split('**提示词**:', 1)[1].strip()

            # 检测多行提示词
            elif line.startswith('> ') and current_prompt:
                current_prompt += ' ' + line[1:].strip()

        return prompts

    @staticmethod
    def load_from_directory(dir_path: str) -> List[Dict]:
        """从目录加载所有 .prompt.md 文件"""
        prompt_dir = Path(dir_path)
        if not prompt_dir.exists():
            return []

        prompts = []
        for prompt_file in sorted(prompt_dir.glob('*.prompt.md')):
            content = prompt_file.read_text(encoding='utf-8')

            # 提取描述和提示词
            description = ""
            prompt = ""

            for line in content.split('\n'):
                if line.startswith('# ') and not description:
                    description = line[2:].strip()
                elif line.startswith('> **提示词**:'):
                    prompt = line.split('**提示词**:', 1)[1].strip()
                elif line.startswith('> ') and prompt:
                    prompt += ' ' + line[1:].strip()

            if prompt:
                prompts.append({
                    'filename': prompt_file.stem.replace('.prompt', ''),
                    'description': description,
                    'prompt': prompt
                })

        return prompts

class BatchIllustrationGenerator:
    """批量插图生成器"""

    def __init__(self, output_dir: str = "imgs", model: str = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model = model
        self.generator = UnifiedImageGenerator()

        # 重试配置
        self.max_retries = 2
        self.retry_delay = 5  # 秒

    def generate_with_retry(self, prompt: str, filename: str) -> bool:
        """带重试的生成"""
        for attempt in range(self.max_retries + 1):
            try:
                image_data, provider = self.generator.generate(prompt, self.model)

                if image_data:
                    # 保存图像
                    output_path = self.output_dir / f"{filename}.png"

                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    size_kb = len(image_data) / 1024
                    print(f"  ✅ 成功 - {filename}.png ({size_kb:.1f} KB) - 使用 {provider}")
                    return True

                if attempt < self.max_retries:
                    print(f"  ⚠️ 第 {attempt + 1} 次尝试失败，{self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"  ❌ 失败 - {filename} (已重试 {self.max_retries} 次)")

            except Exception as e:
                if attempt < self.max_retries:
                    print(f"  ⚠️ 错误: {e}，{self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"  ❌ 错误: {e} - {filename}")

        return False

    def generate_from_file(self, source: str, source_type: str = "auto") -> Dict:
        """从文件批量生成

        Args:
            source: 源文件路径 (JSON/Markdown) 或目录
            source_type: 源类型 (json/markdown/directory/auto)

        Returns:
            生成结果统计
        """
        # 自动检测类型
        if source_type == "auto":
            source_path = Path(source)
            if source_path.is_file():
                if source_path.suffix == '.json':
                    source_type = 'json'
                else:
                    source_type = 'markdown'
            elif source_path.is_dir():
                source_type = 'directory'
            else:
                return {'error': f'源路径不存在: {source}'}

        # 加载提示词
        print(f"📂 从 {source_type} 加载提示词...")

        if source_type == 'json':
            prompts = PromptFile.load_from_json(source)
        elif source_type == 'markdown':
            prompts = PromptFile.load_from_markdown(source)
        elif source_type == 'directory':
            prompts = PromptFile.load_from_directory(source)
        else:
            return {'error': f'不支持的源类型: {source_type}'}

        if not prompts:
            return {'error': '未找到提示词'}

        print(f"✅ 加载 {len(prompts)} 条提示词\n")

        # 批量生成
        results = {
            'total': len(prompts),
            'success': 0,
            'failed': 0,
            'files': []
        }

        for i, item in enumerate(prompts, 1):
            filename = item.get('filename', f'image_{i:03d}')
            description = item.get('description', '')
            prompt = item.get('prompt', '')

            print(f"[{i}/{len(prompts)}] {description}")
            print(f"     文件: {filename}")

            success = self.generate_with_retry(prompt, filename)

            if success:
                results['success'] += 1
                results['files'].append({
                    'filename': f"{filename}.png",
                    'description': description,
                    'status': 'success'
                })
            else:
                results['failed'] += 1
                results['files'].append({
                    'filename': filename,
                    'description': description,
                    'status': 'failed'
                })

            print()

        # 输出统计
        print("=" * 50)
        print("📊 生成统计")
        print("=" * 50)
        print(f"总计: {results['total']} 张")
        print(f"成功: {results['success']} 张")
        print(f"失败: {results['failed']} 张")
        print()
        print(f"📁 输出目录: {self.output_dir.absolute()}")
        print()

        # Vertex AI 和智谱的详细统计
        print("🎨 提供商统计:")
        print(f"  Vertex AI: {self.generator.stats['vertex_success']} 成功, {self.generator.stats['vertex_failed']} 失败")
        print(f"  智谱 CogView: {self.generator.stats['zhipu_success']} 成功, {self.generator.stats['zhipu_failed']} 失败")

        return results

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="文章配图批量生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从提示词目录生成
  python batch_generate.py imgs/prompts/

  # 从 Markdown 配图方案生成
  python batch_generate.py illustration_plan.md

  # 从 JSON 文件生成
  python batch_generate.py prompts.json

  # 指定输出目录
  python batch_generate.py imgs/prompts/ --output article_imgs/

  # 指定模型
  python batch_generate.py imgs/prompts/ --model vertex-ultra
        """
    )

    parser.add_argument("source", help="提示词源 (目录/JSON/Markdown)")
    parser.add_argument("-o", "--output", default="imgs",
                        help="输出目录 (默认: imgs)")
    parser.add_argument("--model",
                        choices=["vertex-ultra", "vertex-std", "vertex-fast", "zhipu"],
                        help="图像生成模型 (默认: 自动选择)")
    parser.add_argument("--max-retries", type=int, default=2,
                        help="最大重试次数 (默认: 2)")

    args = parser.parse_args()

    # 创建生成器
    generator = BatchIllustrationGenerator(
        output_dir=args.output,
        model=args.model
    )
    generator.max_retries = args.max_retries

    # 执行批量生成
    results = generator.generate_from_file(args.source)

    # 保存结果
    result_file = Path(args.output) / "generation_results.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"📝 结果已保存到: {result_file}")

if __name__ == "__main__":
    main()
