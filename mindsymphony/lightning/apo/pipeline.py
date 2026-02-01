"""
APO Pipeline - 自动提示词优化管道

受 Agent Lightning 和 APE (Automatic Prompt Engineering) 启发
实现提示词的自动优化、A/B 测试和版本管理。

核心流程:
1. Monitor - 监控技能性能
2. Identify - 识别待优化技能
3. Generate - 生成候选提示词
4. Evaluate - 离线评估
5. ABTest - A/B 测试验证
6. Deploy - 部署新版本

优化策略:
- lightning-rag: 基于成功案例检索增强
- chain-of-thought: 添加推理步骤
- constraint-clarification: 明确化约束
- example-augmentation: 添加 Golden Examples
"""

import re
import json
import time
import random
from typing import Any, Dict, List, Optional, Callable, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class OptimizationStrategy(Enum):
    """优化策略"""
    LIGHTNING_RAG = "lightning-rag"  # 基于成功案例
    CHAIN_OF_THOUGHT = "chain-of-thought"  # 思维链
    CONSTRAINT_CLARIFICATION = "constraint-clarification"  # 约束明确化
    EXAMPLE_AUGMENTATION = "example-augmentation"  # 示例增强
    STYLE_REFINEMENT = "style-refinement"  # 风格精炼


@dataclass
class PromptCandidate:
    """提示词候选"""
    version_id: str
    skill_name: str
    prompt_template: str
    strategy: OptimizationStrategy
    parent_version: Optional[str]
    performance_score: Optional[float] = None
    sample_count: int = 0
    success_rate: Optional[float] = None


class APOPipeline:
    """自动提示词优化管道

    实现完整的 APO 流程，自动改进技能提示词

    示例:
        apo = APOPipeline()

        # 手动触发优化
        apo.optimize_skill("knowledge-explorer")

        # 获取优化建议
        candidates = apo.get_candidates("knowledge-explorer")

        # A/B 测试
        apo.start_ab_test("knowledge-explorer", candidates[0].version_id)
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

        # 触发阈值
        self.trigger_config = {
            "min_samples": self.config.get('min_samples', 20),
            "success_rate_threshold": self.config.get('success_rate_threshold', 0.7),
            "performance_drop_threshold": self.config.get('performance_drop_threshold', -0.1)
        }

        # A/B 测试配置
        self.ab_test_config = {
            "traffic_split": self.config.get('ab_traffic_split', 0.3),
            "min_test_duration_hours": self.config.get('min_test_duration', 24),
            "significance_level": self.config.get('significance_level', 0.05)
        }

        # 存储后端（延迟初始化）
        self._store = None
        self._tracer = None

        # 优化策略注册
        self._strategies: Dict[OptimizationStrategy, Callable] = {
            OptimizationStrategy.LIGHTNING_RAG: self._apply_lightning_rag,
            OptimizationStrategy.CHAIN_OF_THOUGHT: self._apply_cot,
            OptimizationStrategy.CONSTRAINT_CLARIFICATION: self._apply_constraint_clarification,
            OptimizationStrategy.EXAMPLE_AUGMENTATION: self._apply_example_augmentation,
            OptimizationStrategy.STYLE_REFINEMENT: self._apply_style_refinement
        }

        # 活跃测试
        self._active_ab_tests: Dict[str, Dict] = {}

    def _get_store(self):
        """获取存储实例"""
        if self._store is None:
            from ..store.core import LightningStore
            self._store = LightningStore()
        return self._store

    def _get_tracer(self):
        """获取追踪器实例"""
        if self._tracer is None:
            from ..tracer.core import LightningTracer
            self._tracer = LightningTracer()
        return self._tracer

    def check_optimization_trigger(self, skill_name: str) -> Tuple[bool, str]:
        """检查是否需要优化

        Returns:
            (should_optimize, reason)
        """
        store = self._get_store()
        stats = store.get_skill_stats(skill_name, days=7)

        if stats.get('total_invocations', 0) < self.trigger_config['min_samples']:
            return False, f"样本不足: {stats.get('total_invocations')} < {self.trigger_config['min_samples']}"

        success_rate = stats.get('success_rate', 0)

        if success_rate < self.trigger_config['success_rate_threshold']:
            return True, f"成功率低: {success_rate:.2%} < {self.trigger_config['success_rate_threshold']:.2%}"

        # 检查性能下降趋势
        old_stats = store.get_skill_stats(skill_name, days=14)
        old_success_rate = old_stats.get('success_rate', success_rate)

        if success_rate < old_success_rate + self.trigger_config['performance_drop_threshold']:
            return True, f"性能下降: {old_success_rate:.2%} -> {success_rate:.2%}"

        return False, f"性能良好: {success_rate:.2%}"

    def optimize_skill(
        self,
        skill_name: str,
        strategies: Optional[List[OptimizationStrategy]] = None
    ) -> List[PromptCandidate]:
        """优化指定技能的提示词

        Args:
            skill_name: 技能名称
            strategies: 优化策略列表（默认全部）

        Returns:
            生成的候选列表
        """
        store = self._get_store()

        # 获取当前活跃提示词
        current = store.get_active_prompt(skill_name)
        if not current:
            return []

        current_prompt = current['prompt_template']
        current_version = current['version_id']

        # 确定优化策略
        if strategies is None:
            strategies = list(self._strategies.keys())

        candidates = []

        for strategy in strategies:
            try:
                # 应用优化策略
                optimizer = self._strategies.get(strategy)
                if not optimizer:
                    continue

                new_prompt = optimizer(current_prompt, skill_name)

                if new_prompt and new_prompt != current_prompt:
                    # 存储候选版本
                    version_id = store.store_prompt_version(
                        skill_name=skill_name,
                        prompt_template=new_prompt,
                        is_active=False,
                        is_candidate=True,
                        parent_version_id=current_version,
                        optimization_strategy=strategy.value
                    )

                    if version_id:
                        candidates.append(PromptCandidate(
                            version_id=version_id,
                            skill_name=skill_name,
                            prompt_template=new_prompt,
                            strategy=strategy,
                            parent_version=current_version
                        ))

            except Exception as e:
                print(f"[APO] Strategy {strategy.value} failed: {e}")

        return candidates

    def _apply_lightning_rag(self, current_prompt: str, skill_name: str) -> str:
        """Lightning RAG 策略 - 基于成功案例检索增强"""
        store = self._get_store()

        # 获取成功案例
        from datetime import datetime, timedelta
        since = (datetime.now() - timedelta(days=30)).timestamp()

        success_spans = store.query_spans(
            skill_name=skill_name,
            status='ok',
            since=since,
            limit=10
        )

        if not success_spans:
            return current_prompt

        # 提取成功模式
        patterns = []
        for span in success_spans:
            if span.get('input_data'):
                try:
                    input_data = json.loads(span['input_data'])
                    patterns.append(input_data)
                except:
                    pass

        if not patterns:
            return current_prompt

        # 生成示例
        examples_section = "\n## Successful Examples\n"
        for i, pattern in enumerate(patterns[:3], 1):
            example_str = json.dumps(pattern, ensure_ascii=False, indent=2)[:500]
            examples_section += f"\nExample {i}:\n{example_str}\n"

        # 插入到提示词中
        if "## Successful Examples" in current_prompt:
            # 替换现有示例
            return re.sub(
                r'## Successful Examples.*?(?=##|$)',
                examples_section,
                current_prompt,
                flags=re.DOTALL
            )
        else:
            # 追加示例
            return current_prompt + examples_section

    def _apply_cot(self, current_prompt: str, skill_name: str) -> str:
        """Chain-of-Thought 策略 - 添加推理步骤"""
        cot_section = """
## Thinking Process
Before responding, please think through this step by step:
1. Understand the user's core intent
2. Identify key constraints and requirements
3. Consider relevant knowledge and context
4. Formulate a structured response
5. Verify completeness and accuracy
"""

        # 避免重复添加
        if "Thinking Process" in current_prompt or "step by step" in current_prompt:
            return current_prompt

        return current_prompt + cot_section

    def _apply_constraint_clarification(self, current_prompt: str, skill_name: str) -> str:
        """约束明确化策略"""
        # 从当前提示词提取约束
        constraints = []

        # 常见约束模式
        constraint_patterns = [
            r'(?:must|should|need to|required).*?(?=\n|$)',
            r'(?:don\'t|never|avoid|strictly).*?(?=\n|$)',
            r'(?:always|ensure|verify).*?(?=\n|$)'
        ]

        for pattern in constraint_patterns:
            matches = re.findall(pattern, current_prompt, re.IGNORECASE)
            constraints.extend(matches)

        if len(constraints) < 3:
            return current_prompt  # 约束已足够明确

        # 整理约束
        constraint_section = "\n## Constraints (Strictly Follow)\n"
        for i, constraint in enumerate(constraints[:10], 1):
            constraint_section += f"{i}. {constraint.strip()}\n"

        # 替换或追加
        if "## Constraints" in current_prompt:
            return re.sub(
                r'## Constraints.*?(?=##|$)',
                constraint_section,
                current_prompt,
                flags=re.DOTALL
            )
        else:
            return current_prompt + constraint_section

    def _apply_example_augmentation(self, current_prompt: str, skill_name: str) -> str:
        """示例增强策略"""
        # 这与 lightning-rag 类似，但更关注输入-输出对
        return self._apply_lightning_rag(current_prompt, skill_name)

    def _apply_style_refinement(self, current_prompt: str, skill_name: str) -> str:
        """风格精炼策略"""
        # 添加风格指导
        style_section = """
## Output Style
- Be concise and precise
- Use structured formatting (bullet points, numbered lists)
- Provide actionable insights
- Avoid generic or vague statements
"""

        if "Output Style" in current_prompt:
            return current_prompt

        return current_prompt + style_section

    def start_ab_test(
        self,
        skill_name: str,
        candidate_version_id: str
    ) -> bool:
        """启动 A/B 测试"""
        store = self._get_store()

        # 获取候选版本
        candidates = store.get_prompt_candidates(skill_name)
        candidate = next(
            (c for c in candidates if c['version_id'] == candidate_version_id),
            None
        )

        if not candidate:
            return False

        # 记录测试开始
        self._active_ab_tests[skill_name] = {
            "candidate_version": candidate_version_id,
            "start_time": time.time(),
            "control_samples": 0,
            "treatment_samples": 0,
            "control_success": 0,
            "treatment_success": 0
        }

        return True

    def get_ab_test_assignment(self, skill_name: str) -> Tuple[str, str]:
        """获取 A/B 测试分组

        Returns:
            (version_id, group) - group is 'control' or 'treatment'
        """
        if skill_name not in self._active_ab_tests:
            # 未在测试中，返回当前活跃版本
            store = self._get_store()
            current = store.get_active_prompt(skill_name)
            return current['version_id'] if current else None, 'control'

        test = self._active_ab_tests[skill_name]

        # 流量分配
        if random.random() < self.ab_test_config['traffic_split']:
            # 治疗组
            return test['candidate_version'], 'treatment'
        else:
            # 对照组
            store = self._get_store()
            current = store.get_active_prompt(skill_name)
            return current['version_id'], 'control'

    def evaluate_ab_test(self, skill_name: str) -> Optional[Dict]:
        """评估 A/B 测试结果"""
        if skill_name not in self._active_ab_tests:
            return None

        test = self._active_ab_tests[skill_name]
        store = self._get_store()

        # 检查测试时长
        elapsed_hours = (time.time() - test['start_time']) / 3600
        if elapsed_hours < self.ab_test_config['min_test_duration_hours']:
            return {
                "status": "running",
                "elapsed_hours": elapsed_hours,
                "min_required": self.ab_test_config['min_test_duration_hours']
            }

        # 获取候选版本性能
        candidate_stats = store.get_skill_stats(skill_name, days=1)

        # 简单比较（实际应用需要统计显著性检验）
        if candidate_stats.get('success_rate', 0) > self.trigger_config['success_rate_threshold']:
            return {
                "status": "success",
                "recommendation": "deploy_candidate",
                "candidate_success_rate": candidate_stats.get('success_rate'),
                "test_duration_hours": elapsed_hours
            }
        else:
            return {
                "status": "inconclusive",
                "recommendation": "continue_test_or_discard",
                "candidate_success_rate": candidate_stats.get('success_rate'),
                "test_duration_hours": elapsed_hours
            }

    def deploy_candidate(self, skill_name: str, version_id: str) -> bool:
        """部署候选提示词为正式版本"""
        store = self._get_store()

        # 设置新版本为活跃
        success = store.set_active_prompt(version_id)

        if success and skill_name in self._active_ab_tests:
            # 结束 A/B 测试
            del self._active_ab_tests[skill_name]

        return success

    def run_optimization_cycle(self) -> List[Dict]:
        """运行完整的优化周期"""
        results = []

        # 1. 扫描所有技能
        store = self._get_store()
        metrics = store.get_metrics_summary(days=7)

        # 获取活跃技能列表
        active_skills = [
            "cognitive-architect",
            "knowledge-explorer",
            "concept-singularity",
            "brand-alchemist",
            "official-writer"
        ]

        for skill_name in active_skills:
            try:
                # 2. 检查触发条件
                should_optimize, reason = self.check_optimization_trigger(skill_name)

                if not should_optimize:
                    results.append({
                        "skill": skill_name,
                        "action": "skip",
                        "reason": reason
                    })
                    continue

                # 3. 生成候选
                candidates = self.optimize_skill(skill_name)

                if not candidates:
                    results.append({
                        "skill": skill_name,
                        "action": "no_candidates",
                        "reason": "所有策略未产生新候选"
                    })
                    continue

                # 4. 启动 A/B 测试
                if candidates:
                    self.start_ab_test(skill_name, candidates[0].version_id)

                results.append({
                    "skill": skill_name,
                    "action": "ab_test_started",
                    "candidate_count": len(candidates),
                    "test_version": candidates[0].version_id
                })

            except Exception as e:
                results.append({
                    "skill": skill_name,
                    "action": "error",
                    "error": str(e)
                })

        return results

    def get_candidates(self, skill_name: str) -> List[Dict]:
        """获取技能的候选提示词"""
        store = self._get_store()
        return store.get_prompt_candidates(skill_name)

    def get_active_tests(self) -> Dict[str, Dict]:
        """获取当前活跃的 A/B 测试"""
        return self._active_ab_tests.copy()
