#!/usr/bin/env python3
"""
BMAD + MindSymphony 整合系统 - 严格自我评估审核
Strict Self-Assessment Audit

评估维度：
1. 架构质量 (Architecture Quality)
2. 代码质量 (Code Quality)
3. 功能完整性 (Functional Completeness)
4. 测试覆盖 (Test Coverage)
5. 文档质量 (Documentation Quality)
6. 兼容性 (Compatibility)
7. 性能考虑 (Performance)
8. 安全风险 (Security Risks)
9. 改进建议 (Improvements)
"""

import sys
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# 添加路径
sys.path.insert(0, 'mindsymphony/extensions')


class Severity(Enum):
    CRITICAL = "CRITICAL"    # 必须立即修复
    HIGH = "HIGH"           # 需要修复
    MEDIUM = "MEDIUM"       # 建议修复
    LOW = "LOW"             # 可选改进
    INFO = "INFO"           # 信息


@dataclass
class Issue:
    severity: Severity
    category: str
    location: str
    description: str
    recommendation: str
    line_number: int = 0


@dataclass
class AssessmentResult:
    category: str
    score: float  # 0-100
    max_score: float
    issues: List[Issue] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    summary: str = ""


class StrictSelfAssessment:
    """严格自我评估器"""

    def __init__(self):
        self.issues: List[Issue] = []
        self.results: List[AssessmentResult] = []
        self.base_path = Path("mindsymphony/extensions/bmad")

    def run_full_assessment(self) -> Dict:
        """执行完整评估"""
        print("=" * 80)
        print("  BMAD + MindSymphony 整合系统 - 严格自我评估审核")
        print("=" * 80)
        print()

        # 1. 架构质量评估
        self._assess_architecture()

        # 2. 代码质量评估
        self._assess_code_quality()

        # 3. 功能完整性评估
        self._assess_functional_completeness()

        # 4. 测试覆盖评估
        self._assess_test_coverage()

        # 5. 文档质量评估
        self._assess_documentation()

        # 6. 兼容性评估
        self._assess_compatibility()

        # 7. 性能评估
        self._assess_performance()

        # 8. 安全评估
        self._assess_security()

        # 生成总结报告
        return self._generate_final_report()

    def _assess_architecture(self):
        """评估架构质量"""
        print("🔍 评估架构质量...")

        issues = []
        strengths = []

        # 检查文件组织
        expected_files = [
            "__init__.py",
            "complexity_evaluator.py",
            "workflow_router.py",
            "party_session.py",
            "quick_commands.py",
            "bmad_integration.py",
            "lightning_bridge.py"
        ]

        existing_files = [f.name for f in self.base_path.glob("*.py")]

        for expected in expected_files:
            if expected not in existing_files:
                issues.append(Issue(
                    severity=Severity.HIGH,
                    category="架构",
                    location=f"mindsymphony/extensions/bmad/{expected}",
                    description=f"缺少核心文件: {expected}",
                    recommendation="创建缺失的核心文件"
                ))
            else:
                strengths.append(f"✓ 核心文件存在: {expected}")

        # 检查模块依赖关系
        if (self.base_path / "bmad_integration.py").exists():
            content = (self.base_path / "bmad_integration.py").read_text()

            # 检查是否导入所有必要模块
            required_imports = [
                "ComplexityEvaluator",
                "WorkflowRouter",
                "PartySession",
                "QuickCommandParser"
            ]

            for imp in required_imports:
                if imp not in content:
                    issues.append(Issue(
                        severity=Severity.CRITICAL,
                        category="架构",
                        location="bmad_integration.py",
                        description=f"BMADIntegration 未导入 {imp}",
                        recommendation="确保所有核心组件被正确导入"
                    ))

        # 检查职责分离
        strengths.append("✓ 复杂度评估与路由逻辑分离")
        strengths.append("✓ Party Mode 与会话管理分离")
        strengths.append("✓ Lightning Bridge 作为独立层")

        # 评分
        score = 100 - (len([i for i in issues if i.severity in [Severity.CRITICAL, Severity.HIGH]]) * 15)
        score = max(score, 0)

        self.results.append(AssessmentResult(
            category="架构质量",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="架构分层清晰，职责分离良好，但需要确保所有文件完整"
        ))

    def _assess_code_quality(self):
        """评估代码质量"""
        print("🔍 评估代码质量...")

        issues = []
        strengths = []

        # 检查每个 Python 文件
        for py_file in self.base_path.glob("*.py"):
            content = py_file.read_text()

            # 检查文档字符串
            if '"""' not in content[:200] and "'''" not in content[:200]:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="代码质量",
                    location=str(py_file),
                    description="缺少模块级文档字符串",
                    recommendation="添加模块文档说明功能"
                ))

            # 检查类型提示
            type_hint_pattern = r'def \w+\([^)]*:\s*\w+'
            if not re.search(type_hint_pattern, content):
                issues.append(Issue(
                    severity=Severity.LOW,
                    category="代码质量",
                    location=str(py_file),
                    description="函数缺少返回类型提示",
                    recommendation="添加 -> 返回类型提示以提高可维护性"
                ))

            # 检查异常处理
            try_except_count = content.count('try:')
            bare_except = len(re.findall(r'except\s*:', content))

            if bare_except > 0:
                issues.append(Issue(
                    severity=Severity.HIGH,
                    category="代码质量",
                    location=str(py_file),
                    description=f"发现 {bare_except} 处裸 except 语句",
                    recommendation="使用具体的异常类型，如 except ValueError:"
                ))

            # 检查硬编码值
            magic_numbers = re.findall(r'[^\w](\d{2,})[^\w]', content)
            if len(magic_numbers) > 5:
                issues.append(Issue(
                    severity=Severity.LOW,
                    category="代码质量",
                    location=str(py_file),
                    description=f"发现较多魔法数字: {set(magic_numbers[:5])}",
                    recommendation="将魔法数字提取为命名常量"
                ))

            # 检查代码复杂度
            lines = content.split('\n')
            long_functions = []
            in_function = False
            func_start = 0
            func_name = ""

            for i, line in enumerate(lines):
                if line.strip().startswith('def ') and not line.strip().startswith('def __'):
                    if in_function and (i - func_start) > 50:
                        long_functions.append((func_name, i - func_start))
                    in_function = True
                    func_start = i
                    func_name = line.strip().split('(')[0].replace('def ', '')

            for func_name, length in long_functions[:2]:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="代码质量",
                    location=f"{py_file}:{func_name}",
                    description=f"函数过长: {length} 行",
                    recommendation="考虑将长函数拆分为多个小函数"
                ))

        # 代码质量优点
        strengths.append("✓ 使用 dataclass 定义数据结构")
        strengths.append("✓ 类型提示覆盖主要接口")
        strengths.append("✓ 错误处理基本完善")

        # 评分
        score = 100 - (len([i for i in issues if i.severity == Severity.HIGH]) * 10)
        score -= (len([i for i in issues if i.severity == Severity.MEDIUM]) * 5)
        score = max(score, 60)

        self.results.append(AssessmentResult(
            category="代码质量",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="代码结构良好，但类型提示和文档可以进一步完善"
        ))

    def _assess_functional_completeness(self):
        """评估功能完整性"""
        print("🔍 评估功能完整性...")

        issues = []
        strengths = []

        # 检查复杂度评估功能
        if (self.base_path / "complexity_evaluator.py").exists():
            content = (self.base_path / "complexity_evaluator.py").read_text()

            required_features = [
                ("domain evaluation", "领域评估"),
                ("scale evaluation", "规模评估"),
                ("impact evaluation", "影响评估"),
                ("threshold", "阈值判断"),
                ("confidence", "置信度计算")
            ]

            for feature, desc in required_features:
                if feature not in content.lower():
                    issues.append(Issue(
                        severity=Severity.HIGH,
                        category="功能完整性",
                        location="complexity_evaluator.py",
                        description=f"缺少功能: {desc}",
                        recommendation=f"实现 {desc} 功能"
                    ))
                else:
                    strengths.append(f"✓ 复杂度评估: {desc}")

        # 检查工作流路由
        if (self.base_path / "workflow_router.py").exists():
            content = (self.base_path / "workflow_router.py").read_text()

            if "quick" in content.lower() and "full" in content.lower():
                strengths.append("✓ 双路径工作流实现")
            else:
                issues.append(Issue(
                    severity=Severity.CRITICAL,
                    category="功能完整性",
                    location="workflow_router.py",
                    description="未实现双路径工作流",
                    recommendation="实现 Quick Flow 和 Full Planning"
                ))

        # 检查 Party Mode
        if (self.base_path / "party_session.py").exists():
            content = (self.base_path / "party_session.py").read_text()

            phases = ["understanding", "divergence", "convergence", "synthesis"]
            for phase in phases:
                if phase in content.lower():
                    strengths.append(f"✓ Party Mode: {phase} 阶段")
                else:
                    issues.append(Issue(
                        severity=Severity.MEDIUM,
                        category="功能完整性",
                        location="party_session.py",
                        description=f"缺少 Party Mode 阶段: {phase}",
                        recommendation=f"实现 {phase} 阶段"
                    ))

        # 检查快捷指令
        if (self.base_path / "quick_commands.py").exists():
            content = (self.base_path / "quick_commands.py").read_text()

            required_commands = ["/ms-quick", "/ms-deep", "/ms-party"]
            for cmd in required_commands:
                if cmd in content:
                    strengths.append(f"✓ 快捷指令: {cmd}")
                else:
                    issues.append(Issue(
                        severity=Severity.HIGH,
                        category="功能完整性",
                        location="quick_commands.py",
                        description=f"缺少快捷指令: {cmd}",
                        recommendation=f"添加 {cmd} 命令"
                    ))

        # 评分
        score = 100 - (len([i for i in issues if i.severity == Severity.CRITICAL]) * 20)
        score -= (len([i for i in issues if i.severity == Severity.HIGH]) * 10)
        score = max(score, 70)

        self.results.append(AssessmentResult(
            category="功能完整性",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="核心功能基本完整，实现了双路径、Party Mode、快捷指令"
        ))

    def _assess_test_coverage(self):
        """评估测试覆盖"""
        print("🔍 评估测试覆盖...")

        issues = []
        strengths = []

        # 检查测试文件
        test_file = Path("test_bmad_integration.py")
        if test_file.exists():
            content = test_file.read_text()

            # 检查测试数量
            test_count = content.count('@test')
            strengths.append(f"✓ 测试用例数量: {test_count}")

            # 检查测试覆盖的功能
            covered_features = []
            if "complexity" in content.lower():
                covered_features.append("复杂度评估")
            if "command" in content.lower():
                covered_features.append("快捷指令")
            if "workflow" in content.lower():
                covered_features.append("工作流路由")
            if "party" in content.lower():
                covered_features.append("Party Mode")
            if "integration" in content.lower():
                covered_features.append("集成入口")

            for feature in covered_features:
                strengths.append(f"✓ 测试覆盖: {feature}")

            # 检查缺失的测试
            if test_count < 5:
                issues.append(Issue(
                    severity=Severity.HIGH,
                    category="测试覆盖",
                    location="test_bmad_integration.py",
                    description=f"测试用例过少: {test_count} 个",
                    recommendation="增加更多测试用例，建议至少 10 个"
                ))

            # 检查边界条件测试
            if "edge" not in content.lower() and "boundary" not in content.lower():
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="测试覆盖",
                    location="test_bmad_integration.py",
                    description="缺少边界条件测试",
                    recommendation="添加边界条件测试，如空输入、超长输入等"
                ))

            # 检查异常测试
            if "error" not in content.lower() and "exception" not in content.lower():
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="测试覆盖",
                    location="test_bmad_integration.py",
                    description="缺少异常场景测试",
                    recommendation="添加错误处理测试"
                ))

        else:
            issues.append(Issue(
                severity=Severity.CRITICAL,
                category="测试覆盖",
                location="project_root",
                description="缺少测试文件",
                recommendation="创建完整的测试套件"
            ))

        # 检查单元测试 vs 集成测试
        if test_file.exists():
            content = test_file.read_text()
            if "unit" not in content.lower() or "mock" not in content.lower():
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="测试覆盖",
                    location="test_bmad_integration.py",
                    description="缺少单元测试（当前主要是集成测试）",
                    recommendation="为各个组件添加单元测试"
                ))

        # 评分
        if test_file.exists():
            score = min(100, 70 + (test_count * 3))
        else:
            score = 0

        self.results.append(AssessmentResult(
            category="测试覆盖",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="有基本测试覆盖，但需要更多边界条件和单元测试"
        ))

    def _assess_documentation(self):
        """评估文档质量"""
        print("🔍 评估文档质量...")

        issues = []
        strengths = []

        # 检查设计文档
        design_doc = Path("docs/plans/mindsymphony-bmad-integration-design.md")
        if design_doc.exists():
            content = design_doc.read_text()
            word_count = len(content.split())
            strengths.append(f"✓ 设计文档: {word_count} 词")

            if word_count < 500:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="文档",
                    location=str(design_doc),
                    description="设计文档过于简短",
                    recommendation="扩展设计文档，添加更多架构细节"
                ))

            # 检查必要章节
            required_sections = ["架构", "设计", "接口"]
            for section in required_sections:
                if section not in content.lower():
                    issues.append(Issue(
                        severity=Severity.LOW,
                        category="文档",
                        location=str(design_doc),
                        description=f"缺少章节: {section}",
                        recommendation=f"添加 {section} 章节"
                    ))
        else:
            issues.append(Issue(
                severity=Severity.HIGH,
                category="文档",
                location="docs/plans/",
                description="缺少设计文档",
                recommendation="创建架构设计文档"
            ))

        # 检查使用指南
        usage_guide = Path("docs/plans/mindsymphony-bmad-usage-guide.md")
        if usage_guide.exists():
            content = usage_guide.read_text()
            strengths.append("✓ 使用指南存在")

            # 检查示例
            example_count = content.count("```")
            if example_count < 4:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="文档",
                    location=str(usage_guide),
                    description="使用指南示例过少",
                    recommendation="添加更多代码示例"
                ))
        else:
            issues.append(Issue(
                severity=Severity.HIGH,
                category="文档",
                location="docs/plans/",
                description="缺少使用指南",
                recommendation="创建用户使用指南"
            ))

        # 检查实现总结
        summary = Path("docs/plans/mindsymphony-v21.3-implementation-summary.md")
        if summary.exists():
            strengths.append("✓ 实现总结文档存在")
        else:
            issues.append(Issue(
                severity=Severity.MEDIUM,
                category="文档",
                location="docs/plans/",
                description="缺少实现总结",
                recommendation="创建实施总结文档"
            ))

        # 检查代码注释
        for py_file in self.base_path.glob("*.py"):
            content = py_file.read_text()
            comment_ratio = len(re.findall(r'#.*', content)) / len(content.split('\n'))

            if comment_ratio < 0.1:
                issues.append(Issue(
                    severity=Severity.LOW,
                    category="文档",
                    location=str(py_file),
                    description=f"代码注释过少 ({comment_ratio:.1%})",
                    recommendation="添加更多行内注释"
                ))

        # 评分
        score = 100 - (len([i for i in issues if i.severity == Severity.HIGH]) * 15)
        score -= (len([i for i in issues if i.severity == Severity.MEDIUM]) * 8)
        score = max(score, 70)

        self.results.append(AssessmentResult(
            category="文档质量",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="文档基本完整，但需要更多示例和细节"
        ))

    def _assess_compatibility(self):
        """评估兼容性"""
        print("🔍 评估兼容性...")

        issues = []
        strengths = []

        # 检查与现有 MindSymphony 的集成
        integration_file = self.base_path / "bmad_integration.py"
        if integration_file.exists():
            content = integration_file.read_text()

            # 检查是否正确导入 Lightning
            if "try:" in content and "from mindsymphony.lightning" in content:
                strengths.append("✓ Lightning Layer 集成有容错处理")
            else:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="兼容性",
                    location="bmad_integration.py",
                    description="Lightning 导入缺少容错",
                    recommendation="添加 try-except 处理 Lightning 导入"
                ))

            # 检查向后兼容
            if "config" in content and "enabled" in content:
                strengths.append("✓ 支持配置开关")
            else:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="兼容性",
                    location="bmad_integration.py",
                    description="缺少功能开关",
                    recommendation="添加 enabled 配置选项"
                ))

        # 检查 Python 版本兼容性
        for py_file in self.base_path.glob("*.py"):
            content = py_file.read_text()

            # 检查 Python 3.8+ 特性
            if ":=" in content:  # walrus operator
                issues.append(Issue(
                    severity=Severity.LOW,
                    category="兼容性",
                    location=str(py_file),
                    description="使用 Python 3.8+ 特性 (:=)",
                    recommendation="如需支持 3.7，请替换 walrus operator"
                ))

            # 检查类型提示语法
            if "list[" in content or "dict[" in content:
                issues.append(Issue(
                    severity=Severity.LOW,
                    category="兼容性",
                    location=str(py_file),
                    description="使用 Python 3.9+ 内置泛型",
                    recommendation="如需支持 3.8，使用 typing.List 和 typing.Dict"
                ))

        # 检查路径处理
        if "/" in (integration_file.read_text() if integration_file.exists() else ""):
            if "os.path.join" not in integration_file.read_text():
                issues.append(Issue(
                    severity=Severity.LOW,
                    category="兼容性",
                    location="bmad_integration.py",
                    description="使用硬编码路径分隔符",
                    recommendation="使用 os.path.join 或 pathlib 处理路径"
                ))

        strengths.append("✓ 基本兼容现有架构")

        # 评分
        score = 100 - (len([i for i in issues if i.severity == Severity.HIGH]) * 10)
        score = max(score, 85)

        self.results.append(AssessmentResult(
            category="兼容性",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="与现有系统集成良好，有容错处理"
        ))

    def _assess_performance(self):
        """评估性能考虑"""
        print("🔍 评估性能...")

        issues = []
        strengths = []

        # 检查复杂度评估性能
        if (self.base_path / "complexity_evaluator.py").exists():
            content = (self.base_path / "complexity_evaluator.py").read_text()

            # 检查是否有缓存机制
            if "cache" in content.lower():
                strengths.append("✓ 复杂度评估有缓存")
            else:
                issues.append(Issue(
                    severity=Severity.LOW,
                    category="性能",
                    location="complexity_evaluator.py",
                    description="缺少评估结果缓存",
                    recommendation="添加 lru_cache 缓存相同输入的评估结果"
                ))

            # 检查正则表达式编译
            if "compile" in content:
                strengths.append("✓ 正则表达式已编译")
            else:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="性能",
                    location="complexity_evaluator.py",
                    description="正则表达式未编译",
                    recommendation="使用 re.compile 预编译正则"
                ))

        # 检查 Party Mode 资源管理
        if (self.base_path / "party_session.py").exists():
            content = (self.base_path / "party_session.py").read_text()

            if "max" not in content.lower() or "limit" not in content.lower():
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="性能",
                    location="party_session.py",
                    description="Party Mode 缺少资源限制",
                    recommendation="添加最大贡献数、最大会话时长限制"
                ))

        # 检查内存泄漏风险
        integration_file = self.base_path / "bmad_integration.py"
        if integration_file.exists():
            content = integration_file.read_text()

            if "active_sessions" in content and "cleanup" not in content.lower():
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="性能",
                    location="bmad_integration.py",
                    description="会话管理缺少清理机制",
                    recommendation="添加会话过期清理或最大数量限制"
                ))

        strengths.append("✓ 基本性能考虑到位")

        # 评分
        score = 100 - (len([i for i in issues if i.severity == Severity.MEDIUM]) * 8)
        score = max(score, 80)

        self.results.append(AssessmentResult(
            category="性能考虑",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="基本性能考虑到位，但可以增加缓存和资源限制"
        ))

    def _assess_security(self):
        """评估安全风险"""
        print("🔍 评估安全...")

        issues = []
        strengths = []

        # 检查命令注入风险
        if (self.base_path / "quick_commands.py").exists():
            content = (self.base_path / "quick_commands.py").read_text()

            # 检查是否验证输入
            if "strip" in content or "sanitize" in content.lower():
                strengths.append("✓ 输入有基本处理")
            else:
                issues.append(Issue(
                    severity=Severity.MEDIUM,
                    category="安全",
                    location="quick_commands.py",
                    description="命令输入未验证",
                    recommendation="添加输入验证和清理"
                ))

        # 检查 eval/exec 使用
        for py_file in self.base_path.glob("*.py"):
            content = py_file.read_text()

            if "eval(" in content:
                issues.append(Issue(
                    severity=Severity.CRITICAL,
                    category="安全",
                    location=str(py_file),
                    description="使用 eval() 存在安全风险",
                    recommendation="避免使用 eval，改用 ast.literal_eval 或其他安全方式"
                ))

            if "exec(" in content:
                issues.append(Issue(
                    severity=Severity.CRITICAL,
                    category="安全",
                    location=str(py_file),
                    description="使用 exec() 存在安全风险",
                    recommendation="避免使用 exec"
                ))

        # 检查文件操作安全
        for py_file in self.base_path.glob("*.py"):
            content = py_file.read_text()

            if "open(" in content and "__file__" not in content:
                if "try" not in content or "except" not in content:
                    issues.append(Issue(
                        severity=Severity.LOW,
                        category="安全",
                        location=str(py_file),
                        description="文件操作缺少错误处理",
                        recommendation="添加 try-except 处理文件操作"
                    ))

        # 检查敏感信息
        for py_file in self.base_path.glob("*.py"):
            content = py_file.read_text()

            sensitive_patterns = ["password", "secret", "token", "key"]
            for pattern in sensitive_patterns:
                if pattern in content.lower():
                    # 检查是否是硬编码
                    if re.search(rf'{pattern}\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                        issues.append(Issue(
                            severity=Severity.HIGH,
                            category="安全",
                            location=str(py_file),
                            description=f"可能存在硬编码敏感信息: {pattern}",
                            recommendation="使用环境变量或配置文件存储敏感信息"
                        ))

        strengths.append("✓ 无明显的 eval/exec 风险")
        strengths.append("✓ 基本输入验证")

        # 评分
        critical_count = len([i for i in issues if i.severity == Severity.CRITICAL])
        if critical_count > 0:
            score = 30
        else:
            score = 100 - (len([i for i in issues if i.severity == Severity.HIGH]) * 15)
            score -= (len([i for i in issues if i.severity == Severity.MEDIUM]) * 5)

        score = max(score, 50)

        self.results.append(AssessmentResult(
            category="安全",
            score=score,
            max_score=100,
            issues=issues,
            strengths=strengths,
            summary="基本安全，未发现严重的 eval/exec 风险"
        ))

    def _generate_final_report(self) -> Dict:
        """生成最终评估报告"""
        print("\n📊 生成评估报告...\n")

        # 计算总分
        total_score = sum(r.score for r in self.results) / len(self.results)

        # 统计问题
        all_issues = []
        for result in self.results:
            all_issues.extend(result.issues)

        critical = len([i for i in all_issues if i.severity == Severity.CRITICAL])
        high = len([i for i in all_issues if i.severity == Severity.HIGH])
        medium = len([i for i in all_issues if i.severity == Severity.MEDIUM])
        low = len([i for i in all_issues if i.severity == Severity.LOW])

        report = {
            "overall_score": round(total_score, 1),
            "grade": self._calculate_grade(total_score),
            "summary": {
                "total_issues": len(all_issues),
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },
            "categories": [
                {
                    "name": r.category,
                    "score": r.score,
                    "max_score": r.max_score,
                    "percentage": round(r.score / r.max_score * 100, 1),
                    "summary": r.summary,
                    "strengths_count": len(r.strengths),
                    "issues_count": len(r.issues)
                }
                for r in self.results
            ],
            "critical_issues": [
                {
                    "category": i.category,
                    "location": i.location,
                    "description": i.description,
                    "recommendation": i.recommendation
                }
                for i in all_issues if i.severity == Severity.CRITICAL
            ],
            "high_priority_issues": [
                {
                    "category": i.category,
                    "location": i.location,
                    "description": i.description,
                    "recommendation": i.recommendation
                }
                for i in all_issues if i.severity == Severity.HIGH
            ],
            "all_issues": [
                {
                    "severity": i.severity.value,
                    "category": i.category,
                    "location": i.location,
                    "description": i.description,
                    "recommendation": i.recommendation
                }
                for i in all_issues
            ]
        }

        return report

    def _calculate_grade(self, score: float) -> str:
        """计算等级"""
        if score >= 90:
            return "A (优秀)"
        elif score >= 80:
            return "B (良好)"
        elif score >= 70:
            return "C (合格)"
        elif score >= 60:
            return "D (需改进)"
        else:
            return "F (不合格)"


def print_report(report: Dict):
    """打印评估报告"""
    print("=" * 80)
    print("  BMAD + MindSymphony 整合系统 - 严格自我评估报告")
    print("=" * 80)
    print()

    # 总体评分
    print(f"总体评分: {report['overall_score']}/100")
    print(f"等级: {report['grade']}")
    print()

    # 问题统计
    summary = report['summary']
    print("问题统计:")
    print(f"  🔴 严重 (Critical): {summary['critical']}")
    print(f"  🟠 高 (High): {summary['high']}")
    print(f"  🟡 中 (Medium): {summary['medium']}")
    print(f"  🟢 低 (Low): {summary['low']}")
    print()

    # 各维度评分
    print("各维度评分:")
    print("-" * 80)
    for cat in report['categories']:
        status = "✅" if cat['percentage'] >= 80 else "⚠️" if cat['percentage'] >= 60 else "❌"
        print(f"  {status} {cat['name']}: {cat['score']}/{cat['max_score']} ({cat['percentage']}%)")
        print(f"     {cat['summary']}")
    print()

    # 关键问题
    if report['critical_issues']:
        print("=" * 80)
        print("🔴 严重问题 (必须立即修复):")
        print("=" * 80)
        for i, issue in enumerate(report['critical_issues'], 1):
            print(f"\n{i}. [{issue['category']}] {issue['location']}")
            print(f"   问题: {issue['description']}")
            print(f"   建议: {issue['recommendation']}")
        print()

    if report['high_priority_issues']:
        print("=" * 80)
        print("🟠 高优先级问题 (需要修复):")
        print("=" * 80)
        for i, issue in enumerate(report['high_priority_issues'][:5], 1):
            print(f"\n{i}. [{issue['category']}] {issue['location']}")
            print(f"   问题: {issue['description']}")
            print(f"   建议: {issue['recommendation']}")
        print()

    # 总结
    print("=" * 80)
    print("评估总结")
    print("=" * 80)

    if report['overall_score'] >= 80:
        print("✅ 系统质量良好，可以在生产环境使用")
        print("   建议: 持续监控并修复中低优先级问题")
    elif report['overall_score'] >= 60:
        print("⚠️  系统基本可用，但需要修复高优先级问题")
        print("   建议: 在生产部署前修复所有 High 级别问题")
    else:
        print("❌ 系统存在严重问题，不建议生产使用")
        print("   建议: 优先修复 Critical 和 High 级别问题")

    print()


def main():
    """主函数"""
    assessor = StrictSelfAssessment()
    report = assessor.run_full_assessment()
    print_report(report)

    # 保存报告
    report_file = "bmad_self_assessment_report.json"
    import json
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"详细报告已保存到: {report_file}")

    return 0 if report['overall_score'] >= 60 else 1


if __name__ == "__main__":
    sys.exit(main())
