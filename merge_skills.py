import yaml
import os

def merge_skills():
    # 读取现有注册表
    registry_file = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml'
    with open(registry_file, 'r', encoding='utf-8') as f:
        registry = yaml.safe_load(f)

    # 读取未注册技能模板
    unregistered_file = 'unregistered_skills.yml'
    with open(unregistered_file, 'r', encoding='utf-8') as f:
        unregistered_skills = yaml.safe_load(f)

    # 确保 external_skills 部分存在
    if 'external_skills' not in registry:
        registry['external_skills'] = {}

    # 合并未注册技能到 external_skills 部分
    added_count = 0
    for skill_name, skill_config in unregistered_skills.items():
        # 跳过路径为 None 的技能
        if skill_config.get('path') is None:
            continue

        # 只添加不存在的技能
        if skill_name not in registry['external_skills'] and skill_name not in registry.get('internal_skills', {}):
            registry['external_skills'][skill_name] = skill_config
            added_count += 1
            print(f"✅ 已添加技能: {skill_name}")
        else:
            print(f"⚠️ 技能已存在: {skill_name}")

    # 保存更新后的注册表
    with open(registry_file, 'w', encoding='utf-8') as f:
        yaml.dump(registry, f, default_flow_style=False, allow_unicode=True, indent=2)

    print(f"\n✅ 技能注册完成！共添加 {added_count} 个技能")
    print(f"📄 更新后的文件: {registry_file}")

if __name__ == "__main__":
    merge_skills()