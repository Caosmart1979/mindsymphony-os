import os
import yaml
import re

def main():
    # 1. 读取已注册的技能
    registry_file = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml'
    with open(registry_file, 'r', encoding='utf-8') as f:
        registry = yaml.safe_load(f)

    registered_skills = set()

    # 获取内部技能
    if 'internal_skills' in registry:
        for skill_name in registry['internal_skills']:
            registered_skills.add(skill_name)

    # 获取外部技能
    if 'external_skills' in registry:
        for skill_name in registry['external_skills']:
            registered_skills.add(skill_name)

    print(f"已注册技能数量: {len(registered_skills)}")
    print(f"已注册技能: {sorted(list(registered_skills))}")

    # 2. 扫描全局技能目录
    global_skills_dir = r'C:\Users\13466\.claude\skills'
    global_skills = set()

    if os.path.exists(global_skills_dir):
        for item in os.listdir(global_skills_dir):
            item_path = os.path.join(global_skills_dir, item)
            if os.path.isdir(item_path) and item != '.claude-plugin' and item != 'scripts' and item != 'spec' and item != 'template' and not item.startswith('.'):
                # 简化技能名称（处理一些特殊命名）
                skill_name = item.lower().replace(' ', '-').replace('_', '-')
                global_skills.add(skill_name)

    print(f"\n全局技能目录技能数量: {len(global_skills)}")
    print(f"全局技能目录: {sorted(list(global_skills))}")

    # 3. 扫描项目技能目录
    project_skills_dir = r'D:\Claudecode\skills\skills'
    project_skills = set()

    if os.path.exists(project_skills_dir):
        for item in os.listdir(project_skills_dir):
            item_path = os.path.join(project_skills_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                # 简化技能名称（处理一些特殊命名）
                skill_name = item.lower().replace(' ', '-').replace('_', '-')
                project_skills.add(skill_name)

    print(f"\n项目技能目录技能数量: {len(project_skills)}")
    print(f"项目技能目录: {sorted(list(project_skills))}")

    # 4. 找出未注册的技能
    all_skills = global_skills.union(project_skills)
    unregistered_skills = all_skills - registered_skills

    print(f"\n未注册技能数量: {len(unregistered_skills)}")
    print(f"未注册技能: {sorted(list(unregistered_skills))}")

    # 5. 创建未注册技能的注册模板
    print("\n" + "="*50)
    print("未注册技能的YAML注册模板:")
    print("="*50)

    for skill_name in sorted(list(unregistered_skills)):
        # 查找技能的实际路径
        skill_path = None

        # 先在全局目录查找
        possible_global_path = os.path.join(global_skills_dir, skill_name)
        if not os.path.exists(possible_global_path):
            # 尝试其他命名变体
            for item in os.listdir(global_skills_dir):
                if os.path.isdir(os.path.join(global_skills_dir, item)) and item.lower() == skill_name.lower():
                    possible_global_path = os.path.join(global_skills_dir, item)
                    break

        if os.path.exists(possible_global_path):
            skill_path = possible_global_path
        else:
            # 在项目目录查找
            possible_project_path = os.path.join(project_skills_dir, skill_name)
            if not os.path.exists(possible_project_path):
                # 尝试其他命名变体
                for item in os.listdir(project_skills_dir):
                    if os.path.isdir(os.path.join(project_skills_dir, item)) and item.lower() == skill_name.lower():
                        possible_project_path = os.path.join(project_skills_dir, item)
                        break

            if os.path.exists(possible_project_path):
                skill_path = possible_project_path

        # 生成注册条目
        print(f"\n  {skill_name}:")
        print(f"    path: {skill_path}")
        print(f"    type: domain")
        print(f"    triggers:")
        print(f"      zh: [{skill_name}]")
        print(f"      en: [{skill_name}]")
        print(f"    priority: 50")
        print(f"    description: {skill_name}")
        print(f"    domains: [general]")

    # 6. 保存未注册技能到文件
    output_file = 'unregistered_skills.yml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 未注册技能的YAML注册模板\n")
        f.write("# 请根据实际情况调整triggers和description\n")
        f.write("\n")

        for skill_name in sorted(list(unregistered_skills)):
            # 查找技能的实际路径
            skill_path = None

            # 先在全局目录查找
            possible_global_path = os.path.join(global_skills_dir, skill_name)
            if not os.path.exists(possible_global_path):
                # 尝试其他命名变体
                for item in os.listdir(global_skills_dir):
                    if os.path.isdir(os.path.join(global_skills_dir, item)) and item.lower() == skill_name.lower():
                        possible_global_path = os.path.join(global_skills_dir, item)
                        break

            if os.path.exists(possible_global_path):
                skill_path = possible_global_path
            else:
                # 在项目目录查找
                possible_project_path = os.path.join(project_skills_dir, skill_name)
                if not os.path.exists(possible_project_path):
                    # 尝试其他命名变体
                    for item in os.listdir(project_skills_dir):
                        if os.path.isdir(os.path.join(project_skills_dir, item)) and item.lower() == skill_name.lower():
                            possible_project_path = os.path.join(project_skills_dir, item)
                            break

                if os.path.exists(possible_project_path):
                    skill_path = possible_project_path

            # 写入到文件
            f.write(f"{skill_name}:\n")
            f.write(f"  path: {skill_path}\n")
            f.write(f"  type: domain\n")
            f.write(f"  triggers:\n")
            f.write(f"    zh: [{skill_name}]\n")
            f.write(f"    en: [{skill_name}]\n")
            f.write(f"  priority: 50\n")
            f.write(f"  description: {skill_name}\n")
            f.write(f"  domains: [general]\n")
            f.write("\n")

    print(f"\n未注册技能模板已保存到: {output_file}")

if __name__ == "__main__":
    main()