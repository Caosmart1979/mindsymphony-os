"""
技能路由引擎
根据用户输入智能路由到合适的技能
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from skill_index import SkillIndex


class RouteResult:
    """路由结果类"""

    def __init__(
        self,
        primary: Optional[str] = None,
        collaborators: List[str] = None,
        confidence: float = 0.0,
        reasoning: str = ""
    ):
        self.primary = primary
        self.collaborators = collaborators or []
        self.confidence = confidence
        self.reasoning = reasoning

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'primary': self.primary,
            'collaborators': self.collaborators,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
        }


class SkillRouter:
    """技能路由引擎"""

    def __init__(self, skill_index: SkillIndex):
        self.index = skill_index
        self._category_map = self._build_category_map()

    def _build_category_map(self) -> Dict[str, str]:
        """构建分类关键词映射"""
        return {
            'design': '设计 前端 UI 界面 视觉 样式 美化 component react vue html css',
            'create': '创建 构建 生成 开发 工具 框架',
            'document': '文档 写作 报告 规范 说明 书写',
            'workflow': '流程 工作流 规划 任务 项目 分解',
            'analysis': '分析 研究 调研 探索 数据',
            'meta': '技能 skill 元 认知 架构',
        }

    def route(self, user_input: str) -> RouteResult:
        """
        智能路由到合适的技能

        Args:
            user_input: 用户输入

        Returns:
            RouteResult 对象
        """
        # 1. 关键词匹配（高置信度）
        keyword_result = self._match_by_keywords(user_input)
        if keyword_result and keyword_result.confidence >= 80:
            # 推理协作链
            collaborators = self._infer_collaboration_chain(keyword_result.primary)
            keyword_result.collaborators = collaborators
            keyword_result.reasoning += f"\n协作技能: {', '.join(collaborators)}"
            return keyword_result

        # 2. 分类匹配（中等置信度）
        category_result = self._match_by_category(user_input)
        if category_result:
            collaborators = self._infer_collaboration_chain(category_result.primary)
            category_result.collaborators = collaborators
            category_result.reasoning += f"\n协作技能: {', '.join(collaborators)}"
            return category_result

        # 3. 标签匹配（低置信度）
        tag_result = self._match_by_tags(user_input)
        if tag_result:
            collaborators = self._infer_collaboration_chain(tag_result.primary)
            tag_result.collaborators = collaborators
            tag_result.reasoning += f"\n协作技能: {', '.join(collaborators)}"
            return tag_result

        # 4. 搜索匹配
        search_result = self._match_by_search(user_input)
        if search_result:
            collaborators = self._infer_collaboration_chain(search_result.primary)
            search_result.collaborators = collaborators
            search_result.reasoning += f"\n协作技能: {', '.join(collaborators)}"
            return search_result

        # 无匹配
        return RouteResult(
            reasoning="未找到匹配的技能",
            confidence=0.0
        )

    def _match_by_keywords(self, user_input: str) -> Optional[RouteResult]:
        """根据关键词匹配"""
        matches = []

        for name, metadata in self.index.skills.items():
            score = 0
            matched_keywords = []

            for trigger in metadata.triggers():
                level = trigger.get('level', 'low')
                keywords = trigger.get('keywords', [])

                for keyword in keywords:
                    if keyword.lower() in user_input.lower():
                        # 根据级别计分
                        if level == 'high':
                            score += 20
                        elif level == 'medium':
                            score += 10
                        else:
                            score += 5
                        matched_keywords.append(keyword)

            if score > 0:
                confidence = trigger.get('confidence', score)
                matches.append((name, score, confidence, matched_keywords))

        # 按分数排序
        if matches:
            matches.sort(key=lambda x: x[1], reverse=True)
            best = matches[0]
            return RouteResult(
                primary=best[0],
                confidence=best[2],
                reasoning=f"关键词匹配: {', '.join(best[3])}"
            )

        return None

    def _match_by_category(self, user_input: str) -> Optional[RouteResult]:
        """根据分类匹配"""
        for category, keywords in self._category_map.items():
            for keyword in keywords.split():
                if keyword in user_input:
                    skills = self.index.get_by_category(category)
                    if skills:
                        return RouteResult(
                            primary=skills[0],
                            confidence=50,
                            reasoning=f"分类匹配: {category}"
                        )
        return None

    def _match_by_tags(self, user_input: str) -> Optional[RouteResult]:
        """根据标签匹配"""
        best_match = None
        best_score = 0

        for tag in self.index.get_all_tags():
            if tag.lower() in user_input.lower():
                skills = self.index.get_by_tag(tag)
                if skills and len(skills) > best_score:
                    best_match = skills[0]
                    best_score = len(skills)

        if best_match:
            return RouteResult(
                primary=best_match,
                confidence=40,
                reasoning=f"标签匹配"
            )

        return None

    def _match_by_search(self, user_input: str) -> Optional[RouteResult]:
        """根据搜索匹配"""
        results = self.index.search(user_input)
        if results:
            return RouteResult(
                primary=results[0],
                confidence=30,
                reasoning=f"搜索匹配"
            )
        return None

    def _infer_collaboration_chain(self, target_skill: str) -> List[str]:
        """
        推理协作链

        Args:
            target_skill: 目标技能名称

        Returns:
            协作技能列表（按执行顺序）
        """
        if not target_skill:
            return []

        chain = []
        metadata = self.index.get_by_name(target_skill)

        if not metadata:
            return []

        # 检查消耗的资源
        for consumes in metadata.consumes():
            # 找到提供这个资源的技能
            providers = self.index.get_providers(consumes)
            if providers:
                # 选择最佳提供者（优先选择相关的）
                related_providers = [
                    p for p in providers
                    if p in metadata.get('related', [])
                ]
                if related_providers:
                    chain.append(related_providers[0])
                elif providers:
                    chain.append(providers[0])

        # 检查 INTEROP.yml 中的协作配置
        interop_path = f"{metadata.get('_path')}/INTEROP.yml"
        import os
        if os.path.exists(interop_path):
            try:
                import yaml
                with open(interop_path, 'r', encoding='utf-8') as f:
                    interop = yaml.safe_load(f)
                    collaboration = interop.get('collaboration', {})
                    sequential = collaboration.get('sequential', [])
                    for item in sequential:
                        if isinstance(item, dict):
                            skill = item.get('skill')
                            if skill and skill not in chain:
                                chain.insert(0, skill)  # 插入到开头
            except:
                pass

        return list(set(chain))  # 去重

    def suggest_combination(self, task_type: str) -> Dict[str, Any]:
        """
        推荐技能组合

        Args:
            task_type: 任务类型描述

        Returns:
            技能组合方案
        """
        result = self.route(task_type)

        if not result.primary:
            return {
                'error': '未找到匹配的技能',
                'suggestion': '请提供更具体的任务描述'
            }

        # 构建组合方案
        combination = {
            'primary': result.primary,
            'collaborators': result.collaborators,
            'execution_order': self._determine_execution_order(
                result.primary,
                result.collaborators
            ),
            'reasoning': result.reasoning,
            'confidence': result.confidence,
        }

        return combination

    def _determine_execution_order(
        self,
        primary: str,
        collaborators: List[str]
    ) -> List[str]:
        """确定执行顺序"""
        order = []

        # 协作技能先执行
        order.extend(collaborators)

        # 主技能最后执行
        if primary:
            order.append(primary)

        return order


if __name__ == '__main__':
    # 测试代码
    import os
    skills_root = os.path.join(os.path.dirname(__file__), '..', 'skills')
    index = SkillIndex(skills_root)
    router = SkillRouter(index)

    test_inputs = [
        "创建一个有品牌风格的前端组件",
        "写一个技术文档",
        "设计一个 landing page",
        "构建 React dashboard",
    ]

    for test_input in test_inputs:
        print(f"\n🔍 输入: {test_input}")
        result = router.route(test_input)
        print(f"  主技能: {result.primary}")
        print(f"  协作技能: {result.collaborators}")
        print(f"  置信度: {result.confidence}%")
        print(f"  推理: {result.reasoning}")
