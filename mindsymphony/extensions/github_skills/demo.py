"""
GitHub Skills Distiller - 功能演示

演示如何使用GitHub技能系统的各个组件
"""

import json
from pathlib import Path


def demo_distiller():
    """演示技能蒸馏器"""
    print("=" * 60)
    print("演示 1: GitHub技能蒸馏器")
    print("=" * 60)

    from github_skill_distiller import GitHubSkillDistiller

    distiller = GitHubSkillDistiller()

    # 模拟蒸馏一个仓库
    print("\n🔬 蒸馏仓库: bmad-code-org/BMAD-METHOD")
    result = distiller.distill("bmad-code-org/BMAD-METHOD")

    print(f"\n✅ 蒸馏完成!")
    print(f"   技能名称: {result.skill_name}")
    print(f"   置信度: {result.confidence:.1%}")
    print(f"   提取模式: {len(result.patterns)} 个")
    print(f"   内容长度: {len(result.skill_content)} 字符")

    # 保存技能文件
    output_dir = Path("./demo_output")
    output_dir.mkdir(exist_ok=True)

    skill_file = output_dir / f"{result.skill_name}.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(result.skill_content)

    print(f"\n💾 技能文件已保存: {skill_file}")

    return result


def demo_knowledge_graph():
    """演示技能知识图谱"""
    print("\n" + "=" * 60)
    print("演示 2: 技能知识图谱")
    print("=" * 60)

    from skill_knowledge_graph import SkillKnowledgeGraph, SkillNode, RelationType

    graph = SkillKnowledgeGraph()

    # 添加技能节点
    print("\n📦 添加技能节点...")
    skill1 = SkillNode(
        name="Python数据分析",
        source="manual",
        description="使用Python进行数据分析的技能",
        tags=["python", "data-analysis", "pandas"]
    )
    id1 = graph.add_skill(skill1)
    print(f"   添加: {skill1.name} (ID: {id1})")

    skill2 = SkillNode(
        name="机器学习基础",
        source="manual",
        description="机器学习入门技能",
        tags=["machine-learning", "python", "sklearn"]
    )
    id2 = graph.add_skill(skill2)
    print(f"   添加: {skill2.name} (ID: {id2})")

    skill3 = SkillNode(
        name="深度学习",
        source="manual",
        description="深度学习进阶",
        tags=["deep-learning", "pytorch", "neural-networks"]
    )
    id3 = graph.add_skill(skill3)
    print(f"   添加: {skill3.name} (ID: {id3})")

    # 建立关系
    print("\n🔗 建立技能关系...")
    graph.add_relation(id2, id1, RelationType.DEPENDS, strength=0.8)
    print(f"   {skill2.name} → 依赖 → {skill1.name}")

    graph.add_relation(id3, id2, RelationType.DEPENDS, strength=0.9)
    print(f"   {skill3.name} → 依赖 → {skill2.name}")

    graph.add_relation(id1, id2, RelationType.RELATED, strength=0.6)
    print(f"   {skill1.name} → 相关 → {skill2.name}")

    # 搜索技能
    print("\n🔍 搜索技能: 'machine learning'")
    results = graph.search("machine learning", limit=5)
    for skill in results:
        print(f"   找到: {skill.name}")

    # 推荐技能
    print("\n📊 基于Python数据分析推荐相关技能...")
    recommendations = graph.recommend_skills([id1], limit=5)
    for skill in recommendations:
        print(f"   推荐: {skill.name}")

    # 统计
    stats = graph.get_stats()
    print(f"\n📈 图谱统计:")
    print(f"   总节点: {stats['total_nodes']}")
    print(f"   总关系: {stats['total_relations']}")


def demo_skill_dna():
    """演示技能DNA"""
    print("\n" + "=" * 60)
    print("演示 3: 个人技能DNA")
    print("=" * 60)

    import tempfile
    from skill_dna import SkillDNA

    with tempfile.TemporaryDirectory() as temp_dir:
        dna = SkillDNA(user_id="demo_user", storage_dir=temp_dir)

        # 模拟GitHub分析
        print("\n👤 分析GitHub档案: demo_user")
        analysis = dna.analyze_github_profile("demo_user")
        print(f"   Starred: {len(analysis['starred_repos'])} 个仓库")
        print(f"   语言: {', '.join(analysis['top_languages'])}")
        print(f"   兴趣: {', '.join(analysis['interests'])}")

        # 记录技能使用
        print("\n📝 记录技能使用...")
        dna.record_skill_usage(
            skill_id="python_001",
            skill_name="Python编程",
            success=True,
            context={'tags': ['coding', 'backend']}
        )
        dna.record_skill_usage(
            skill_id="python_001",
            skill_name="Python编程",
            success=True,
            context={'tags': ['coding', 'scripting']}
        )
        dna.record_skill_usage(
            skill_id="ml_001",
            skill_name="机器学习",
            success=False,
            context={'tags': ['modeling', 'tensorflow']}
        )

        # 获取报告
        print("\n📊 生成专长报告...")
        report = dna.get_expertise_report()
        print(f"   技能多样性: {report['skill_diversity']}")
        print(f"   总体成功率: {report['success_rate']:.1%}")
        print(f"   学习速度: {report['learning_velocity']:.2f}")

        if report['top_skills']:
            print(f"\n   常用技能:")
            for skill in report['top_skills'][:3]:
                print(f"      - {skill['skill_name']}: {skill['use_count']}次")

        # 推荐学习路径
        print("\n📚 推荐学习路径 (data_science)...")
        recommendations = dna.recommend_learning_path("data_science")
        for rec in recommendations[:3]:
            print(f"   [{rec['priority']}] {rec['name']}: {rec['reason']}")


def demo_generator():
    """演示动态技能生成器"""
    print("\n" + "=" * 60)
    print("演示 4: 动态技能生成器")
    print("=" * 60)

    from dynamic_skill_generator import DynamicSkillGenerator, GenerationRequest

    generator = DynamicSkillGenerator()

    # 创建生成请求
    print("\n🎯 生成任务技能...")
    request = GenerationRequest(
        task_description="分析生物信息学数据集并生成可视化报告",
        required_capabilities=["bioinformatics", "data_analysis", "visualization"]
    )

    # 生成技能
    skill = generator.generate(request, persist=False)

    print(f"\n✅ 技能生成完成!")
    print(f"   技能ID: {skill.skill_id}")
    print(f"   技能名称: {skill.name}")
    print(f"   置信度: {skill.confidence:.1%}")
    print(f"   参考来源: {len(skill.sources)} 个项目")

    # 保存生成的技能
    output_dir = Path("./demo_output")
    output_dir.mkdir(exist_ok=True)

    skill_file = output_dir / f"{skill.skill_id}.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(skill.content)

    print(f"\n💾 技能文件已保存: {skill_file}")


def demo_integration():
    """演示系统集成"""
    print("\n" + "=" * 60)
    print("演示 5: MindSymphony集成")
    print("=" * 60)

    import tempfile
    from integration import GitHubSkillsIntegration

    with tempfile.TemporaryDirectory() as temp_dir:
        # 初始化系统
        print("\n🚀 初始化GitHub技能系统...")
        integration = GitHubSkillsIntegration(
            config={'storage_dir': temp_dir}
        )
        integration.initialize_for_user("demo_user")

        # 添加一些示例技能
        from skill_knowledge_graph import SkillNode

        print("\n📦 添加示例技能到知识图谱...")
        skills = [
            SkillNode(name="Web开发", source="demo", tags=["web", "frontend"]),
            SkillNode(name="数据库设计", source="demo", tags=["database", "sql"]),
            SkillNode(name="API开发", source="demo", tags=["api", "backend"]),
        ]

        for skill in skills:
            skill_id = integration.skill_graph.add_skill(skill)
            print(f"   添加: {skill.name} (ID: {skill_id[:8]}...)")

        # 为项目推荐技能
        print("\n📊 为项目推荐技能组合...")
        recommendations = integration.recommend_skills_for_project(
            "构建一个Web应用",
            tech_stack=["React", "Node.js"]
        )

        for rec in recommendations[:5]:
            skill_name = rec['skill']['name'] if hasattr(rec['skill'], 'name') else rec['skill']['name']
            print(f"   推荐: {skill_name}")
            print(f"      原因: {rec['reason']}")

        # 获取统计
        print("\n📈 系统统计...")
        stats = integration.get_stats()
        print(f"   技能节点: {stats['knowledge_graph']['total_nodes']}")
        print(f"   关系数量: {stats['knowledge_graph']['total_relations']}")
        print(f"   存储大小: {stats['storage']['size_mb']:.2f} MB")


def main():
    """主入口"""
    print("\n" + "=" * 60)
    print("GitHub Skills Distiller - 功能演示")
    print("=" * 60)

    demos = [
        ("技能蒸馏器", demo_distiller),
        ("知识图谱", demo_knowledge_graph),
        ("技能DNA", demo_skill_dna),
        ("动态生成器", demo_generator),
        ("系统集成", demo_integration),
    ]

    print("\n可用演示:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. 运行全部")

    try:
        choice = input("\n选择演示 (0-5): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n使用默认选择: 运行全部")
        choice = "0"

    if choice == "0":
        for name, func in demos:
            try:
                func()
            except Exception as e:
                print(f"\n❌ {name}演示出错: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(demos):
        try:
            demos[int(choice) - 1][1]()
        except Exception as e:
            print(f"\n❌ 演示出错: {e}")
    else:
        print("无效选择")

    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
