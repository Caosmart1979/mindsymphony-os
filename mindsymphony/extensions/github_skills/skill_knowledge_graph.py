"""
Skill Knowledge Graph
技能知识图谱 - 管理技能间的关系和网络

功能:
- 技能节点管理
- 关系类型定义
- 图谱查询和搜索
- 推荐引擎
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Any, Tuple
from datetime import datetime
from enum import Enum
from pathlib import Path


class RelationType(Enum):
    """技能关系类型"""
    RELATED = "related"           # 相关
    COMPOSES = "composes"         # 组合（A组合B）
    DEPENDS = "depends"           # 依赖（A依赖B）
    EVOLVES_TO = "evolves_to"     # 演化为
    LEARNED_FROM = "learned_from" # 学习自
    REPLACES = "replaces"         # 替代


@dataclass
class SkillNode:
    """技能节点"""
    id: str                       # 唯一标识
    name: str                     # 技能名称
    source: str                   # 来源 (GitHub repo 或 'manual')
    version: str = "1.0.0"
    description: str = ""
    type: str = "general"         # skill, methodology, pattern, practice
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    usage_count: int = 0
    success_rate: float = 0.0

    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()

    def _generate_id(self) -> str:
        """生成唯一ID"""
        content = f"{self.name}:{self.source}:{self.created_at}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'SkillNode':
        return cls(**data)


@dataclass
class SkillRelation:
    """技能关系"""
    source_id: str                # 源技能ID
    target_id: str                # 目标技能ID
    relation_type: RelationType   # 关系类型
    strength: float = 1.0         # 关系强度 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'relation_type': self.relation_type.value,
            'strength': self.strength,
            'metadata': self.metadata,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SkillRelation':
        data = data.copy()
        data['relation_type'] = RelationType(data['relation_type'])
        return cls(**data)


class SkillKnowledgeGraph:
    """
    技能知识图谱

    管理技能的节点和关系，支持查询、推荐和演化追踪
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        初始化知识图谱

        Args:
            storage_path: 存储路径，默认为 ~/.mindsymphony/skill_graph.json
        """
        self.storage_path = storage_path or Path.home() / '.mindsymphony' / 'skill_graph.json'
        self.nodes: Dict[str, SkillNode] = {}
        self.relations: List[SkillRelation] = []
        self._index = {}  # 倒排索引

        # 加载已有数据
        self._load()

    def add_skill(self, skill: SkillNode) -> str:
        """
        添加技能节点

        Args:
            skill: 技能节点

        Returns:
            技能ID
        """
        self.nodes[skill.id] = skill
        self._update_index(skill)
        self._save()
        return skill.id

    def add_relation(
        self,
        source_id: str,
        target_id: str,
        relation_type: RelationType,
        strength: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        添加技能关系

        Args:
            source_id: 源技能ID
            target_id: 目标技能ID
            relation_type: 关系类型
            strength: 关系强度
            metadata: 元数据

        Returns:
            是否成功添加
        """
        # 验证节点存在
        if source_id not in self.nodes or target_id not in self.nodes:
            return False

        # 检查是否已存在相同关系
        for rel in self.relations:
            if (rel.source_id == source_id and
                rel.target_id == target_id and
                rel.relation_type == relation_type):
                # 更新强度
                rel.strength = max(rel.strength, strength)
                self._save()
                return True

        relation = SkillRelation(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            strength=strength,
            metadata=metadata or {}
        )
        self.relations.append(relation)
        self._save()
        return True

    def get_skill(self, skill_id: str) -> Optional[SkillNode]:
        """获取技能节点"""
        return self.nodes.get(skill_id)

    def find_skill_by_name(self, name: str) -> Optional[SkillNode]:
        """根据名称查找技能"""
        for skill in self.nodes.values():
            if skill.name.lower() == name.lower():
                return skill
        return None

    def get_related_skills(
        self,
        skill_id: str,
        relation_type: Optional[RelationType] = None,
        min_strength: float = 0.0
    ) -> List[Tuple[SkillNode, SkillRelation]]:
        """
        获取相关技能

        Args:
            skill_id: 技能ID
            relation_type: 关系类型过滤
            min_strength: 最小关系强度

        Returns:
            (技能, 关系) 元组列表
        """
        results = []

        for rel in self.relations:
            if rel.source_id == skill_id and rel.strength >= min_strength:
                if relation_type is None or rel.relation_type == relation_type:
                    target = self.nodes.get(rel.target_id)
                    if target:
                        results.append((target, rel))

        return sorted(results, key=lambda x: x[1].strength, reverse=True)

    def search(self, query: str, limit: int = 10) -> List[SkillNode]:
        """
        搜索技能

        Args:
            query: 搜索查询
            limit: 返回数量限制

        Returns:
            匹配的技能列表
        """
        query_lower = query.lower()
        results = []

        for skill in self.nodes.values():
            score = 0.0

            # 名称匹配
            if query_lower in skill.name.lower():
                score += 2.0

            # 描述匹配
            if skill.description and query_lower in skill.description.lower():
                score += 1.0

            # 标签匹配
            for tag in skill.tags:
                if query_lower in tag.lower():
                    score += 1.5

            # 来源匹配
            if query_lower in skill.source.lower():
                score += 0.5

            if score > 0:
                results.append((skill, score))

        # 按分数排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:limit]]

    def recommend_skills(
        self,
        skill_ids: List[str],
        context: Optional[Dict] = None
    ) -> List[SkillNode]:
        """
        推荐相关技能

        基于当前技能组合推荐可能相关的其他技能

        Args:
            skill_ids: 当前技能ID列表
            context: 上下文信息

        Returns:
            推荐的技能列表
        """
        context = context or {}
        scores = {}  # skill_id -> score

        for skill_id in skill_ids:
            skill = self.nodes.get(skill_id)
            if not skill:
                continue

            # 获取相关技能
            related = self.get_related_skills(skill_id)

            for related_skill, relation in related:
                if related_skill.id in skill_ids:
                    continue  # 跳过已有技能

                # 计算推荐分数
                score = relation.strength

                # 根据关系类型加权
                if relation.relation_type == RelationType.COMPOSES:
                    score *= 1.5
                elif relation.relation_type == RelationType.RELATED:
                    score *= 1.2

                # 考虑技能成功率
                score *= (0.5 + 0.5 * related_skill.success_rate)

                if related_skill.id in scores:
                    scores[related_skill.id] += score
                else:
                    scores[related_skill.id] = score

        # 排序并返回
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.nodes[sid] for sid, _ in sorted_scores[:10]]

    def find_skill_compositions(
        self,
        target_skill_id: str
    ) -> List[List[SkillNode]]:
        """
        查找技能组合

        找出可以组合成目标技能的前置技能组合

        Args:
            target_skill_id: 目标技能ID

        Returns:
            技能组合列表
        """
        compositions = []

        # 查找所有组合关系
        for rel in self.relations:
            if (rel.target_id == target_skill_id and
                rel.relation_type == RelationType.COMPOSES):
                source = self.nodes.get(rel.source_id)
                if source:
                    compositions.append([source])

        return compositions

    def get_skill_lineage(self, skill_id: str) -> Dict:
        """
        获取技能演化历史

        Args:
            skill_id: 技能ID

        Returns:
            演化历史字典
        """
        skill = self.nodes.get(skill_id)
        if not skill:
            return {}

        lineage = {
            'skill': skill.to_dict(),
            'ancestors': [],
            'descendants': [],
            'learned_from': []
        }

        for rel in self.relations:
            # 学习自
            if rel.source_id == skill_id and rel.relation_type == RelationType.LEARNED_FROM:
                source = self.nodes.get(rel.target_id)
                if source:
                    lineage['learned_from'].append({
                        'skill': source.to_dict(),
                        'strength': rel.strength
                    })

            # 演化为
            if rel.source_id == skill_id and rel.relation_type == RelationType.EVOLVES_TO:
                target = self.nodes.get(rel.target_id)
                if target:
                    lineage['descendants'].append(target.to_dict())

        return lineage

    def update_skill_usage(self, skill_id: str, success: bool):
        """
        更新技能使用统计

        Args:
            skill_id: 技能ID
            success: 是否成功
        """
        skill = self.nodes.get(skill_id)
        if not skill:
            return

        skill.usage_count += 1

        # 更新成功率 (指数移动平均)
        alpha = 0.3
        success_val = 1.0 if success else 0.0
        skill.success_rate = (1 - alpha) * skill.success_rate + alpha * success_val

        skill.updated_at = datetime.now().isoformat()
        self._save()

    def auto_create_relations(self):
        """
        自动创建技能关系

        基于技能标签、来源等自动推断关系
        """
        skills = list(self.nodes.values())
        new_relations = 0

        for i, skill1 in enumerate(skills):
            for skill2 in skills[i+1:]:
                # 计算相似度
                similarity = self._calculate_similarity(skill1, skill2)

                if similarity > 0.7:
                    # 创建相关关系
                    self.add_relation(
                        skill1.id,
                        skill2.id,
                        RelationType.RELATED,
                        strength=similarity
                    )
                    new_relations += 1

                # 检查来源关系
                if skill1.source == skill2.source and skill1.source != 'manual':
                    self.add_relation(
                        skill1.id,
                        skill2.id,
                        RelationType.RELATED,
                        strength=0.5,
                        metadata={'source': 'same_repo'}
                    )

        return new_relations

    def _calculate_similarity(self, skill1: SkillNode, skill2: SkillNode) -> float:
        """计算两个技能的相似度"""
        # 标签交集
        tags1 = set(t.lower() for t in skill1.tags)
        tags2 = set(t.lower() for t in skill2.tags)

        if not tags1 or not tags2:
            return 0.0

        intersection = tags1 & tags2
        union = tags1 | tags2

        return len(intersection) / len(union) if union else 0.0

    def export_to_dot(self, output_path: str):
        """
        导出为GraphViz格式

        Args:
            output_path: 输出文件路径
        """
        lines = ['digraph SkillGraph {']
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=box, style=rounded];')

        # 添加节点
        for skill in self.nodes.values():
            label = skill.name.replace('"', '\\"')
            lines.append(f'  "{skill.id}" [label="{label}"];')

        # 添加边
        for rel in self.relations:
            style = 'solid'
            if rel.relation_type == RelationType.DEPENDS:
                style = 'dashed'
            elif rel.relation_type == RelationType.EVOLVES_TO:
                style = 'dotted'

            lines.append(
                f'  "{rel.source_id}" -> "{rel.target_id}" '
                f'[label="{rel.relation_type.value}", style={style}];'
            )

        lines.append('}')

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def get_stats(self) -> Dict:
        """获取图谱统计"""
        return {
            'total_nodes': len(self.nodes),
            'total_relations': len(self.relations),
            'relation_types': {
                rt.value: len([r for r in self.relations if r.relation_type == rt])
                for rt in RelationType
            },
            'sources': list(set(s.source for s in self.nodes.values())),
            'avg_usage': sum(s.usage_count for s in self.nodes.values()) / max(len(self.nodes), 1),
        }

    def _update_index(self, skill: SkillNode):
        """更新倒排索引"""
        # 为标签创建索引
        for tag in skill.tags:
            tag_lower = tag.lower()
            if tag_lower not in self._index:
                self._index[tag_lower] = set()
            self._index[tag_lower].add(skill.id)

    def _load(self):
        """从存储加载数据"""
        if not Path(self.storage_path).exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 加载节点
            for skill_data in data.get('nodes', []):
                skill = SkillNode.from_dict(skill_data)
                self.nodes[skill.id] = skill
                self._update_index(skill)

            # 加载关系
            for rel_data in data.get('relations', []):
                self.relations.append(SkillRelation.from_dict(rel_data))

        except Exception as e:
            print(f"[SkillGraph] 加载失败: {e}")

    def _save(self):
        """保存到存储"""
        try:
            # 确保目录存在
            Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)

            data = {
                'nodes': [s.to_dict() for s in self.nodes.values()],
                'relations': [r.to_dict() for r in self.relations],
                'updated_at': datetime.now().isoformat()
            }

            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"[SkillGraph] 保存失败: {e}")
