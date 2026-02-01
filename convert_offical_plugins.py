#!/usr/bin/env python3
"""
官方插件重制为本地SKILLS执行脚本

这个脚本帮助自动化执行将官方插件重制为本地SKILLS的过程。
"""

import os
import sys
import subprocess
import yaml
import argparse
from pathlib import Path

def read_k_dense_plugins(file_path):
    """读取 k-dense-plugins.txt 文件，获取需要重制的插件列表"""
    plugins = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析文件内容，提取插件信息
        lines = content.strip().split('\n')

        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and 'k-dense-ai/claude-scientific-skills/' in line:
                # 提取插件名称，格式为: k-dense-ai/claude-scientific-skills/plugin-name
                plugin_name = line.split(' ')[0].strip()
                plugin_name = plugin_name.replace('k-dense-ai/claude-scientific-skills/', '')
                plugins.append(plugin_name)

    except Exception as e:
        print(f"读取插件列表失败: {e}")

    return plugins

def filter_plugins(plugins, keywords=None):
    """根据关键词过滤插件列表"""
    if not keywords:
        return plugins

    filtered_plugins = []
    for plugin in plugins:
        for keyword in keywords:
            if keyword.lower() in plugin.lower():
                filtered_plugins.append(plugin)
                break

    return filtered_plugins

def create_skill_directory(plugin_name, destination_path):
    """使用 init_skill.py 脚本创建技能目录"""
    init_skill_script = Path(__file__).parent / "skills" / "skills" / "skill-creator" / "scripts" / "init_skill.py"

    if not init_skill_script.exists():
        print(f"未找到 init_skill.py 脚本: {init_skill_script}")
        return False

    command = [
        sys.executable, str(init_skill_script),
        plugin_name,
        "--path", destination_path
    ]

    try:
        print(f"正在创建技能目录: {plugin_name}")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            print(f"技能目录创建成功: {plugin_name}")
            return True
        else:
            print(f"技能目录创建失败: {plugin_name}")
            print(f"错误输出: {result.stderr}")
            return False

    except Exception as e:
        print(f"创建技能目录时出错: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="将官方插件重制为本地SKILLS的执行脚本"
    )

    parser.add_argument(
        "--plugin-list",
        type=str,
        default="k-dense-plugins.txt",
        help="官方插件列表文件路径"
    )

    parser.add_argument(
        "--destination",
        type=str,
        default="skills/skills",
        help="技能目录的目标路径"
    )

    parser.add_argument(
        "--keywords",
        type=str,
        default="",
        help="过滤插件的关键词，多个关键词用逗号分隔"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="重制插件的数量限制"
    )

    args = parser.parse_args()

    print("官方插件重制为本地SKILLS执行脚本")
    print("=" * 60)

    # 读取插件列表
    print(f"正在读取插件列表: {args.plugin_list}")
    plugins = read_k_dense_plugins(args.plugin_list)
    print(f"找到 {len(plugins)} 个官方插件")

    # 过滤插件
    if args.keywords:
        keywords = args.keywords.split(',')
        plugins = filter_plugins(plugins, keywords)
        print(f"过滤后找到 {len(plugins)} 个插件")

    # 限制数量
    if args.limit > 0 and len(plugins) > args.limit:
        plugins = plugins[:args.limit]
        print(f"限制重制数量为 {args.limit} 个插件")

    # 创建技能目录
    success_count = 0
    failed_count = 0

    for i, plugin in enumerate(plugins, 1):
        print(f"\n{i}/{len(plugins)}. 处理插件: {plugin}")

        if create_skill_directory(plugin, args.destination):
            success_count += 1
        else:
            failed_count += 1

    print("\n" + "=" * 60)
    print(f"处理完成: 成功 {success_count} 个，失败 {failed_count} 个")

    if success_count > 0:
        print("\n技能目录已创建在以下位置:")
        print(f"  {os.path.abspath(args.destination)}")
        print("\n下一步操作:")
        print("1. 复制官方插件内容到对应的技能目录")
        print("2. 适配本地网络和API环境")
        print("3. 测试技能功能")
        print("4. 更新技能索引")

if __name__ == "__main__":
    main()