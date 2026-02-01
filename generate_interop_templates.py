#!/usr/bin/env python3
"""批量生成Top 20核心技能的INTEROP.yml模板"""

TOP_20_SKILLS = [
    "mindsymphony", "skill-creator", "cognitive-architect",
    "frontend-design", "doc-coauthoring", "docx", "pdf", "pptx",
    "mcp-builder", "api-integration-designer", "code-refactoring-expert",
    "database-schema-architect", "devops-workflow-designer", "gemini-cli-integration",
    "brand-guidelines", "canvas-design", "algorithmic-art", "theme-factory",
    "internal-comms", "knowledge-explorer",
]

CATEGORIES = {
    "mindsymphony": "meta", "skill-creator": "create", "cognitive-architect": "cognitive",
    "frontend-design": "design", "doc-coauthoring": "workflow", "docx": "document",
    "pdf": "document", "pptx": "document", "mcp-builder": "engineering",
    "api-integration-designer": "engineering", "code-refactoring-expert": "engineering",
    "database-schema-architect": "engineering", "devops-workflow-designer": "engineering",
    "gemini-cli-integration": "integration", "brand-guidelines": "design",
    "canvas-design": "design", "algorithmic-art": "creative", "theme-factory": "design",
    "internal-comms": "communication", "knowledge-explorer": "research",
}

PRIORITIES = {
    "mindsymphony": "critical", "skill-creator": "critical", "cognitive-architect": "high",
    "frontend-design": "high", "doc-coauthoring": "high", "docx": "medium",
    "pdf": "medium", "pptx": "medium", "mcp-builder": "high",
    "api-integration-designer": "medium", "code-refactoring-expert": "medium",
    "database-schema-architect": "medium", "devops-workflow-designer": "medium",
    "gemini-cli-integration": "medium", "brand-guidelines": "medium",
    "canvas-design": "medium", "algorithmic-art": "low", "theme-factory": "low",
    "internal-comms": "medium", "knowledge-explorer": "medium",
}

INTEROP_TEMPLATE = """# INTEROP.yml - 技能互操作性配置
skill:
  name: {skill_name}
  version: 1.0.0
  category: {category}
  priority: {priority}
  status: active

metadata:
  display_name: {display_name}
  description: Auto-generated INTEROP.yml for {skill_name}
  author: Anthropic / Community
  license: See LICENSE.txt
  created_at: 2025-01-08
  updated_at: 2025-01-08

capabilities:
  provides: []
  consumes: []
  tags: []

compatibility:
  claude_code_minimum: "1.0"
  required_features: []
  optional_features: []

performance:
  avg_execution_time: null
  avg_success_rate: null
  total_invocations: 0
  last_invocation: null

ab_testing:
  enabled: true
  variants: []
  metrics: ["success_rate", "execution_time", "user_satisfaction"]

discovery:
  auto_route: true
  confidence_threshold: 0.7
  routing_patterns:
    - pattern: "{skill_keywords}"
      confidence: 0.8
  related_skills: []
"""

def generate_interop_yml(skill_name: str) -> str:
    category = CATEGORIES.get(skill_name, "general")
    priority = PRIORITIES.get(skill_name, "medium")
    display_name = skill_name.replace("-", " ").replace("_", " ").title()
    skill_keywords = skill_name.replace("-", " ").replace("_", " ")
    
    return INTEROP_TEMPLATE.format(
        skill_name=skill_name, category=category, priority=priority,
        display_name=display_name, skill_keywords=skill_keywords
    )

def main():
    from pathlib import Path
    base_path = Path("./skills/skills")
    
    for skill_name in TOP_20_SKILLS:
        skill_path = base_path / skill_name
        if not skill_path.exists():
            print(f"⚠️  技能目录不存在: {skill_path}")
            continue
        
        interop_path = skill_path / "INTEROP.yml"
        content = generate_interop_yml(skill_name)
        
        with open(interop_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已生成: {interop_path}")
    
    print("\n🎉 所有INTEROP.yml模板生成完成！")

if __name__ == "__main__":
    main()
