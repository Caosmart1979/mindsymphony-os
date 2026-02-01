#!/usr/bin/env python3
"""
重新生成技能索引脚本
"""

import os
import sys
import json
from pathlib import Path
from datetime import date, datetime

# 添加项目路径到系统路径
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir / "skills" / "skill_discovery"))

from skill_index import SkillIndex
from skill_metadata import load_all_skills


def json_serial(obj):
    """JSON 序列化处理函数"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def main():
    print("🎯 重新生成技能索引...")

    # 技能根目录
    skills_root = project_dir / "skills" / "skills"
    print(f"📁 技能目录: {skills_root}")

    # 检查目录是否存在
    if not skills_root.exists():
        print(f"❌ 技能目录不存在: {skills_root}")
        return 1

    # 加载所有技能
    print("\n📚 加载技能元数据...")
    try:
        skills = load_all_skills(str(skills_root))
        print(f"✅ 成功加载 {len(skills)} 个技能")
    except Exception as e:
        print(f"❌ 加载技能失败: {e}")
        return 1

    # 创建技能索引
    print("\n🏗️  创建技能索引...")
    try:
        index = SkillIndex(str(skills_root))
        print(f"✅ 索引创建完成")
    except Exception as e:
        print(f"❌ 创建索引失败: {e}")
        return 1

    # 保存技能索引到文件
    output_file = project_dir / "skill_index.json"

    print(f"\n💾 保存索引到: {output_file}")
    try:
        # 转换为字典并处理日期类型
        index_dict = index.to_dict()

        # 递归处理日期类型
        def convert(obj):
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(v) for v in obj]
            elif isinstance(obj, (date, datetime)):
                return obj.isoformat()
            else:
                return obj

        # 处理技能数据
        processed_index = convert(index_dict)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "_version": "1.0",
                    "_cache_time": os.path.getmtime(__file__),
                    "index": processed_index,
                },
                f,
                ensure_ascii=False,
                indent=2,
                default=json_serial,
            )
        print(f"✅ 保存成功")
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        import traceback
        print(traceback.format_exc())
        return 1

    # 显示统计信息
    stats = index.get_statistics()
    print("\n📊 技能索引统计:")
    print(f"  总技能数量: {stats['total_skills']}")
    print(f"  分类数量: {len(stats['categories'])}")
    print(f"  标签数量: {stats['tags_count']}")
    print(f"  资源类型数量: {stats['resources_count']}")

    print("\n🎉 技能索引重新生成完成！")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)