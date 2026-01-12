"""
技能协作测试脚本
测试技能发现系统和协作链推理
"""

import os
import sys

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加 skill_discovery 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skill_discovery'))

from skill_discovery import SkillDiscovery


def print_section(title: str):
    """打印分节标题"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def test_basic_discovery(discovery: SkillDiscovery):
    """测试基本发现功能"""
    print_section("测试 1: 基本发现功能")

    # 测试按名称查找
    print("\n📌 按名称查找 'frontend-design':")
    skill = discovery.find_by_name('frontend-design')
    if skill:
        print(f"  ✅ 找到: {skill.get('name')}")
        print(f"  分类: {skill.get('category')}")
        print(f"  标签: {skill.get('tags', [])}")
    else:
        print("  ❌ 未找到")

    # 测试按分类查找
    print("\n📂 按分类 'design' 查找:")
    design_skills = discovery.find_by_category('design')
    print(f"  找到 {len(design_skills)} 个技能:")
    for s in design_skills:
        print(f"    - {s}")

    # 测试搜索
    print("\n🔍 搜索 'brand':")
    results = discovery.search('brand')
    print(f"  找到 {len(results)} 个技能:")
    for s in results:
        print(f"    - {s}")


def test_provider_consumer(discovery: SkillDiscovery):
    """测试提供者-消费者关系"""
    print_section("测试 2: 提供者-消费者关系")

    # 测试查找提供者
    print("\n🎁 查找 'design-tokens' 的提供者:")
    providers = discovery.find_providers('design-tokens')
    print(f"  找到 {len(providers)} 个提供者:")
    for p in providers:
        print(f"    - {p}")

    # 测试查找消费者
    print("\n🔄 查找 'brand-guidelines' 的消费者:")
    consumers = discovery.find_consumers('brand-guidelines')
    print(f"  找到 {len(consumers)} 个消费者:")
    for c in consumers:
        print(f"    - {c}")


def test_collaboration_chain(discovery: SkillDiscovery):
    """测试协作链推理"""
    print_section("测试 3: 协作链推理")

    test_skills = [
        ('frontend-design', '前端设计技能'),
        ('doc-coauthoring', '文档协作技能'),
        ('brand-guidelines', '品牌规范技能'),
    ]

    for skill_name, description in test_skills:
        print(f"\n🔗 {description} ({skill_name}):")
        collaborators = discovery.find_collaborators(skill_name)
        if collaborators:
            print(f"  协作技能 ({len(collaborators)}):")
            for c in collaborators:
                print(f"    → {c}")
        else:
            print("  无协作技能")


def test_intelligent_routing(discovery: SkillDiscovery):
    """测试智能路由"""
    print_section("测试 4: 智能路由")

    test_cases = [
        "创建一个有品牌风格的前端组件",
        "写一个技术规范文档",
        "设计一个 landing page 界面",
        "构建 React dashboard",
        "协作编写 API 文档",
    ]

    for test_input in test_cases:
        print(f"\n🎯 输入: {test_input}")
        result = discovery.route(test_input)

        if result.primary:
            print(f"  ✓ 主技能: {result.primary}")
            if result.collaborators:
                print(f"  ✓ 协作技能: {', '.join(result.collaborators)}")
            print(f"  ✓ 置信度: {result.confidence}%")
            print(f"  ✓ 推理: {result.reasoning}")
        else:
            print(f"  ✗ 未找到匹配的技能")


def test_skill_combination(discovery: SkillDiscovery):
    """测试技能组合推荐"""
    print_section("测试 5: 技能组合推荐")

    test_tasks = [
        "品牌视觉设计项目",
        "技术文档协作编写",
        "前端界面开发",
    ]

    for task in test_tasks:
        print(f"\n📋 任务: {task}")
        combination = discovery.suggest_combination(task)

        if 'error' in combination:
            print(f"  ✗ {combination['error']}")
        else:
            print(f"  ✓ 主技能: {combination['primary']}")
            print(f"  ✓ 协作技能: {combination['collaborators']}")
            print(f"  ✓ 执行顺序:")
            for i, skill in enumerate(combination['execution_order'], 1):
                print(f"      {i}. {skill}")
            print(f"  ✓ 推理: {combination['reasoning']}")
            print(f"  ✓ 置信度: {combination['confidence']}%")


def test_metadata_integrity(discovery: SkillDiscovery):
    """测试元数据完整性"""
    print_section("测试 6: 元数据完整性")

    all_skills = discovery.index.skills

    print(f"\n📊 检查 {len(all_skills)} 个技能的元数据:")

    issues = []

    for name, metadata in all_skills.items():
        # 检查必需字段
        if not metadata.get('name'):
            issues.append(f"{name}: 缺少 name 字段")

        if not metadata.get('description'):
            issues.append(f"{name}: 缺少 description 字段")

        # 检查互操作元数据
        if metadata.get('category'):
            if not metadata.get('tags'):
                issues.append(f"{name}: 有 category 但无 tags")

        # 检查 INTEROP.yml
        interop_path = os.path.join(metadata.get('_path', ''), 'INTEROP.yml')
        if os.path.exists(interop_path):
            # 有 INTEROP.yml，检查是否与 SKILL.md 一致
            if not metadata.get('category'):
                issues.append(f"{name}: 有 INTEROP.yml 但 frontmatter 无 category")

    if issues:
        print(f"  ⚠️  发现 {len(issues)} 个问题:")
        for issue in issues[:10]:  # 只显示前10个
            print(f"    - {issue}")
        if len(issues) > 10:
            print(f"    ... 还有 {len(issues) - 10} 个问题")
    else:
        print(f"  ✅ 所有技能元数据完整")


def main():
    """主测试函数"""
    print("\n" + "="*70)
    print("  🧪 技能协作测试套件")
    print("="*70)

    # 获取技能根目录
    skills_root = os.path.join(os.path.dirname(__file__), 'skills')

    print(f"\n📁 技能目录: {skills_root}")

    # 创建发现系统
    print("\n⚙️  初始化技能发现系统...")
    discovery = SkillDiscovery(skills_root)

    # 显示统计信息
    stats = discovery.get_statistics()
    print(f"\n📈 加载了 {stats['total_skills']} 个技能")
    print(f"📂 {len(stats.get('categories', {}))} 个分类")
    print(f"🏷️  {stats['tags_count']} 个标签")
    print(f"🔌 {stats['resources_count']} 种资源类型")

    # 运行测试
    try:
        test_basic_discovery(discovery)
        test_provider_consumer(discovery)
        test_collaboration_chain(discovery)
        test_intelligent_routing(discovery)
        test_skill_combination(discovery)
        test_metadata_integrity(discovery)

        print_section("测试完成")
        print("\n✅ 所有测试通过！\n")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
