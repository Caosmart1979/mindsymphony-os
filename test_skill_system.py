#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import sys

def test_skill_system():
    """测试技能系统的基本功能"""
    registry_path = r"C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml"

    print("正在测试技能系统...")

    try:
        # 测试读取技能注册表
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = yaml.safe_load(f)
        print(f"✅ 成功读取技能注册表，包含 {len(registry.get('external_skills', {}))} 个外部技能和 {len(registry.get('internal_skills', {}))} 个内部技能")

        # 测试技能注册表结构
        required_fields = ['compound_intents', 'domain_routing', 'external_skills', 'internal_skills']
        for field in required_fields:
            if field not in registry:
                print(f"❌ 技能注册表缺少必要字段: {field}")
                return False
        print("✅ 技能注册表结构完整")

        # 测试外部技能
        external_skills = registry.get('external_skills', {})
        for skill_name, skill_info in external_skills.items():
            # 检查技能基本信息
            if 'description' not in skill_info or not skill_info['description']:
                print(f"❌ 外部技能 {skill_name} 缺少描述")
            if 'domains' not in skill_info or not skill_info['domains']:
                print(f"❌ 外部技能 {skill_name} 缺少领域配置")
            if 'path' not in skill_info or not skill_info['path']:
                print(f"❌ 外部技能 {skill_name} 缺少路径配置")

        # 测试内部技能
        internal_skills = registry.get('internal_skills', {})
        for skill_name, skill_info in internal_skills.items():
            # 检查技能基本信息
            if 'description' not in skill_info or not skill_info['description']:
                print(f"❌ 内部技能 {skill_name} 缺少描述")
            if 'domains' not in skill_info or not skill_info['domains']:
                print(f"❌ 内部技能 {skill_name} 缺少领域配置")
            if 'path' not in skill_info or not skill_info['path']:
                print(f"❌ 内部技能 {skill_name} 缺少路径配置")

        print("✅ 技能系统测试完成")
        return True

    except Exception as e:
        print(f"❌ 技能系统测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_skill_system()
    sys.exit(0 if success else 1)
