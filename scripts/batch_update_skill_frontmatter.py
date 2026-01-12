#!/usr/bin/env python3
"""批量更新SKILL.md文件的frontmatter，添加interop_metadata"""

from pathlib import Path

# Top 20技能列表及其interop配置
TOP_20_SKILLS = {
    "cli-companion": """interop_metadata:
  skill_id: corechan.cli_companion
  api_version: v1
  endpoints:
    - /execute
    - /validate
  authentication: none
  rate_limit:
    requests_per_minute: 60""",
    "context-builder": """interop_metadata:
  skill_id: corechan.context_builder
  api_version: v1
  endpoints:
    - /build
    - /validate
  authentication: none
  rate_limit:
    requests_per_minute: 30""",
    "conversation-coach": """interop_metadata:
  skill_id: corechan.conversation_coach
  api_version: v1
  endpoints:
    - /analyze
    - /suggest
  authentication: none
  rate_limit:
    requests_per_minute: 20""",
    "creative-catalyst": """interop_metadata:
  skill_id: corechan.creative_catalyst
  api_version: v1
  endpoints:
    - /generate
    - /evaluate
  authentication: none
  rate_limit:
    requests_per_minute: 15""",
    "debugger-detective": """interop_metadata:
  skill_id: corechan.debugger_detective
  api_version: v1
  endpoints:
    - /analyze
    - /suggest
    - /trace
  authentication: none
  rate_limit:
    requests_per_minute: 40""",
    "emotion-engine": """interop_metadata:
  skill_id: corechan.emotion_engine
  api_version: v1
  endpoints:
    - /analyze
    - /respond
  authentication: none
  rate_limit:
    requests_per_minute: 25""",
    "environment-explorer": """interop_metadata:
  skill_id: corechan.environment_explorer
  api_version: v1
  endpoints:
    - /scan
    - /inspect
  authentication: none
  rate_limit:
    requests_per_minute: 10""",
    "file-fluent": """interop_metadata:
  skill_id: corechan.file_fluent
  api_version: v1
  endpoints:
    - /read
    - /write
    - /search
  authentication: none
  rate_limit:
    requests_per_minute: 100""",
    "git-genius": """interop_metadata:
  skill_id: corechan.git_genius
  api_version: v1
  endpoints:
    - /analyze
    - /suggest
  authentication: none
  rate_limit:
    requests_per_minute: 20""",
    "hype-hunter": """interop_metadata:
  skill_id: corechan.hype_hunter
  api_version: v1
  endpoints:
    - /search
    - /validate
  authentication: none
  rate_limit:
    requests_per_minute: 30""",
    "insight-incubator": """interop_metadata:
  skill_id: corechan.insight_incubator
  api_version: v1
  endpoints:
    - /analyze
    - /incubate
  authentication: none
  rate_limit:
    requests_per_minute: 15""",
    "integration-impresario": """interop_metadata:
  skill_id: corechan.integration_impresario
  api_version: v1
  endpoints:
    - /connect
    - /test
  authentication: none
  rate_limit:
    requests_per_minute: 10""",
    "log-logic": """interop_metadata:
  skill_id: corechan.log_logic
  api_version: v1
  endpoints:
    - /analyze
    - /parse
  authentication: none
  rate_limit:
    requests_per_minute: 50""",
    "memory-matrix": """interop_metadata:
  skill_id: corechan.memory_matrix
  api_version: v1
  endpoints:
    - /store
    - /retrieve
  authentication: none
  rate_limit:
    requests_per_minute: 40""",
    "meta-mediator": """interop_metadata:
  skill_id: corechan.meta_mediator
  api_version: v1
  endpoints:
    - /mediate
    - /optimize
  authentication: none
  rate_limit:
    requests_per_minute: 20""",
    "pattern-pilot": """interop_metadata:
  skill_id: corechan.pattern_pilot
  api_version: v1
  endpoints:
    - /detect
    - /suggest
  authentication: none
  rate_limit:
    requests_per_minute: 30""",
    "project-pilot": """interop_metadata:
  skill_id: corechan.project_pilot
  api_version: v1
  endpoints:
    - /analyze
    - /plan
    - /track
  authentication: none
  rate_limit:
    requests_per_minute: 20""",
    "research-ranger": """interop_metadata:
  skill_id: corechan.research_ranger
  api_version: v1
  endpoints:
    - /search
    - /analyze
  authentication: none
  rate_limit:
    requests_per_minute: 30""",
    "sql-scout": """interop_metadata:
  skill_id: corechan.sql_scout
  api_version: v1
  endpoints:
    - /analyze
    - /optimize
  authentication: none
  rate_limit:
    requests_per_minute: 25""",
    "style-symphonist": """interop_metadata:
  skill_id: corechan.style_symphonist
  api_version: v1
  endpoints:
    - /analyze
    - /transform
  authentication: none
  rate_limit:
    requests_per_minute: 20"""
}

def update_skill_frontmatter(skill_path: Path, skill_name: str, interop_yaml: str):
    """更新单个技能的SKILL.md frontmatter"""
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        print(f"⚠️  {skill_name}: SKILL.md不存在")
        return False
    
    # 读取文件内容
    content = skill_md.read_text()
    
    # 检查是否已有interop_metadata
    if "interop_metadata:" in content:
        print(f"✓ {skill_name}: 已存在interop_metadata，跳过")
        return True
    
    # 提取现有的frontmatter
    lines = content.split('\n')
    
    # 找到frontmatter的结束位置
    if lines[0] != '---':
        print(f"⚠️  {skill_name}: 没有frontmatter")
        return False
    
    frontmatter_end = 1
    for i, line in enumerate(lines[1:], 1):
        if line == '---':
            frontmatter_end = i
            break
    
    # 插入interop_metadata（按行分割）
    interop_lines = interop_yaml.strip().split('\n')
    
    # 在frontmatter结束前插入
    new_lines = lines[:frontmatter_end] + interop_lines + ['---'] + lines[frontmatter_end+1:]
    
    # 写回文件
    skill_md.write_text('\n'.join(new_lines))
    print(f"✅ {skill_name}: 已更新frontmatter")
    return True

def main():
    """主函数"""
    base_path = Path("skills")
    
    success_count = 0
    fail_count = 0
    
    for skill_name, interop_yaml in TOP_20_SKILLS.items():
        skill_path = base_path / skill_name
        
        if not skill_path.exists():
            print(f"❌ {skill_name}: 技能目录不存在")
            fail_count += 1
            continue
        
        if update_skill_frontmatter(skill_path, skill_name, interop_yaml):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n📊 批量更新完成:")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失败: {fail_count}")
    print(f"   📁 总计: {len(TOP_20_SKILLS)}")

if __name__ == "__main__":
    main()
