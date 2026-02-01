"""
GitHub Skills - MindSymphony适配器

将GitHub Skills Distiller整合到MindSymphony OS的【术】层

核心价值:
- 符合道法术器四层架构
- 支持蜂后协奏调度
- 遵循信息素协作协议
- 实现价值对齐与协同进化
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pathlib import Path
import json

# 导入核心组件
from .github_skill_distiller import GitHubSkillDistiller
from .skill_knowledge_graph import SkillKnowledgeGraph, SkillNode, RelationType
from .skill_dna import SkillDNA
from .dynamic_skill_generator import DynamicSkillGenerator, GenerationRequest


class Layer(Enum):
    """道法术器四层架构"""
    TAO = "道"      # 根基与世界观
    FA = "法"       # 战略与构想
    SHU = "术"      # 方法与创造
    QI = "器"       # 执行与交付


class PheromoneType(Enum):
    """
    信息素类型 - MindSymphony协作协议

    信息素是技能间传递的语义化信号，包含：
    - 意图信息素: 表达当前处理意图
    - 能力信息素: 宣告可提供的 capabilities
    - 成果信息素: 交付阶段性成果
    - 请求信息素: 请求其他技能协助
    """
    INTENT = "intent"           # 意图: 当前处理方向
    CAPABILITY = "capability"   # 能力: 可提供的功能
    DELIVERABLE = "deliverable" # 成果: 已完成产出
    REQUEST = "request"         # 请求: 需要帮助
    INSIGHT = "insight"         # 洞察: 发现的模式/知识
    EVOLUTION = "evolution"     # 进化: 系统改进建议


@dataclass
class Pheromone:
    """
    信息素 - 技能间协作的基本单元

    符合MindSymphony的信息素协作机制:
    - 类型: 信息素的语义类别
    - 强度: 0-1，表示信号强度/置信度
    - 时效: 信息素的有效时间窗口
    - 载荷: 携带的具体数据
    """
    type: PheromoneType
    source: str                 # 来源技能ID
    target: Optional[str]       # 目标技能ID (None表示广播)
    intensity: float = 1.0      # 强度 0-1
    ttl: int = 3600             # 生存时间(秒)
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            'type': self.type.value,
            'source': self.source,
            'target': self.target,
            'intensity': self.intensity,
            'ttl': self.ttl,
            'payload': self.payload,
            'timestamp': self.timestamp,
        }


@dataclass
class SkillManifest:
    """
    技能宣言 - MindSymphony标准技能定义

    符合道法术器四层定位:
    - 明确所属层级
    - 声明触发条件
    - 定义能力边界
    - 建立价值主张
    """
    name: str
    layer: Layer                # 道法术器层级
    version: str = "1.0.0"

    # 触发条件
    triggers: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)

    # 能力声明
    capabilities: List[str] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)

    # 价值主张
    value_proposition: str = ""

    # 协作属性
    is_composable: bool = True   # 是否可与其他技能组合
    is_autonomous: bool = False  # 是否支持自主执行模式

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'layer': self.layer.value,
            'version': self.version,
            'triggers': self.triggers,
            'keywords': self.keywords,
            'capabilities': self.capabilities,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'value_proposition': self.value_proposition,
            'is_composable': self.is_composable,
            'is_autonomous': self.is_autonomous,
        }


class GitHubSkillAdapter:
    """
    GitHub技能系统 - MindSymphony适配器

    【术】层技能: 提供从GitHub提取方法论的能力

    符合第一性原理:
    - 价值对齐: 将用户需求转化为技能获取
    - 协同进化: 技能库随使用不断优化
    - 和谐共情: 封装复杂性，提供简洁接口
    - 安全优先: 明确操作边界和确认机制

    蜂后协奏支持:
    - 可接收蜂后的战略分解指令
    - 可发射信息素请求协助
    - 可交付标准化成果
    """

    MANIFEST = SkillManifest(
        name="github-skills-distiller",
        layer=Layer.SHU,
        version="1.0.0",
        triggers=[
            "从GitHub学习",
            "蒸馏技能",
            "提取方法论",
            "构建技能库",
            "github技能",
            "超级技能库",
        ],
        keywords=[
            "github", "skill", "distill", "methodology",
            "extract", "knowledge", "pattern", "best practice"
        ],
        capabilities=[
            "github_repo_analysis",      # 分析GitHub仓库
            "skill_distillation",        # 蒸馏技能
            "knowledge_graph_mgmt",      # 知识图谱管理
            "personal_dna_tracking",     # 个人DNA追踪
            "dynamic_skill_generation",  # 动态技能生成
            "skill_recommendation",      # 技能推荐
        ],
        inputs=[
            "github_repo_url",           # GitHub仓库URL
            "task_description",          # 任务描述
            "user_profile",              # 用户画像
            "skill_query",               # 技能查询
        ],
        outputs=[
            "distilled_skill",           # 蒸馏的技能
            "skill_graph",               # 技能图谱
            "expertise_report",          # 专长报告
            "learning_path",             # 学习路径
            "pheromone_signal",          # 信息素信号
        ],
        value_proposition="将整个GitHub压缩成你的个人超级技能库",
        is_composable=True,
        is_autonomous=True,
    )

    def __init__(self, user_id: Optional[str] = None):
        """
        初始化适配器

        Args:
            user_id: 用户ID，用于个性化
        """
        self.user_id = user_id or "default"
        self.manifest = self.MANIFEST

        # 核心组件
        self._distiller: Optional[GitHubSkillDistiller] = None
        self._graph: Optional[SkillKnowledgeGraph] = None
        self._dna: Optional[SkillDNA] = None
        self._generator: Optional[DynamicSkillGenerator] = None

        # 信息素队列
        self._pheromone_queue: List[Pheromone] = []

        # 协作状态
        self._collaboration_context: Dict[str, Any] = {}

    @property
    def distiller(self) -> GitHubSkillDistiller:
        """延迟初始化蒸馏器"""
        if self._distiller is None:
            self._distiller = GitHubSkillDistiller()
        return self._distiller

    @property
    def graph(self) -> SkillKnowledgeGraph:
        """延迟初始化知识图谱"""
        if self._graph is None:
            self._graph = SkillKnowledgeGraph()
        return self._graph

    @property
    def dna(self) -> SkillDNA:
        """延迟初始化DNA"""
        if self._dna is None:
            storage_dir = Path(f"~/.mindsymphony/github_skills/dna/{self.user_id}").expanduser()
            self._dna = SkillDNA(user_id=self.user_id, storage_dir=str(storage_dir))
        return self._dna

    @property
    def generator(self) -> DynamicSkillGenerator:
        """延迟初始化生成器"""
        if self._generator is None:
            self._generator = DynamicSkillGenerator(
                skill_graph=self.graph,
                skill_dna=self._dna
            )
        return self._generator

    # ==================== 核心能力接口 ====================

    def execute(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行入口 - 蜂后调用接口

        符合蜂后协奏协议:
        1. 接收意图和上下文
        2. 路由到对应处理
        3. 返回标准化成果
        4. 发射必要信息素

        Args:
            intent: 执行意图
            context: 执行上下文

        Returns:
            执行结果和状态
        """
        # 记录执行意图
        self._emit_pheromone(PheromoneType.INTENT, {
            'action': 'execute',
            'intent': intent,
            'context_keys': list(context.keys()),
        })

        # 意图路由
        if intent in ["distill", "蒸馏", "提取"]:
            return self._handle_distill_intent(context)
        elif intent in ["search", "搜索", "查找"]:
            return self._handle_search_intent(context)
        elif intent in ["generate", "生成", "创建"]:
            return self._handle_generate_intent(context)
        elif intent in ["profile", "档案", "分析"]:
            return self._handle_profile_intent(context)
        elif intent in ["recommend", "推荐", "建议"]:
            return self._handle_recommend_intent(context)
        else:
            # 广播请求信息素，请求其他技能协助
            self._emit_pheromone(PheromoneType.REQUEST, {
                'unknown_intent': intent,
                'available_capabilities': self.manifest.capabilities,
            }, target="cognitive-architect")

            return {
                'success': False,
                'error': f"未知意图: {intent}",
                'suggestion': '请求蜂后重新分解任务',
            }

    def _handle_distill_intent(self, context: Dict) -> Dict:
        """处理蒸馏意图"""
        repo_url = context.get('repo_url') or context.get('github_repo')

        if not repo_url:
            return {'success': False, 'error': '缺少repo_url参数'}

        # 执行蒸馏
        result = self.distiller.distill(
            repo_url,
            extract_patterns=context.get('extract_patterns', True),
            include_code_examples=context.get('include_code_examples', True),
        )

        # 注册到知识图谱
        skill_node = SkillNode(
            name=result.skill_name,
            source=f"github:{result.source_repo}",
            description=result.metadata.get('source', {}).get('description', ''),
            type='distilled',
            tags=result.metadata.get('source', {}).get('topics', []),
            metadata={
                'confidence': result.confidence,
                'distilled_at': datetime.now().isoformat(),
            }
        )
        skill_id = self.graph.add_skill(skill_node)

        # 发射成果信息素
        self._emit_pheromone(PheromoneType.DELIVERABLE, {
            'skill_id': skill_id,
            'skill_name': result.skill_name,
            'confidence': result.confidence,
            'type': 'distilled_skill',
        })

        return {
            'success': True,
            'skill_id': skill_id,
            'skill_name': result.skill_name,
            'content': result.skill_content,
            'confidence': result.confidence,
        }

    def _handle_search_intent(self, context: Dict) -> Dict:
        """处理搜索意图"""
        query = context.get('query') or context.get('skill_query')
        limit = context.get('limit', 10)

        if not query:
            return {'success': False, 'error': '缺少query参数'}

        results = self.graph.search(query, limit=limit)

        # 发射洞察信息素
        self._emit_pheromone(PheromoneType.INSIGHT, {
            'search_query': query,
            'results_count': len(results),
            'top_match': results[0].name if results else None,
        })

        return {
            'success': True,
            'query': query,
            'results': [
                {
                    'id': s.id,
                    'name': s.name,
                    'source': s.source,
                    'type': s.type,
                    'tags': s.tags,
                }
                for s in results
            ],
        }

    def _handle_generate_intent(self, context: Dict) -> Dict:
        """处理生成意图"""
        task = context.get('task') or context.get('task_description')

        if not task:
            return {'success': False, 'error': '缺少task参数'}

        request = GenerationRequest(
            task_description=task,
            required_capabilities=context.get('required_capabilities', []),
            preferred_sources=context.get('preferred_sources', []),
        )

        skill = self.generator.generate(
            request,
            persist=context.get('persist', True)
        )

        # 发射成果信息素
        self._emit_pheromone(PheromoneType.DELIVERABLE, {
            'skill_id': skill.skill_id,
            'skill_name': skill.name,
            'confidence': skill.confidence,
            'type': 'generated_skill',
            'is_temporary': skill.is_temporary,
        })

        return {
            'success': True,
            'skill_id': skill.skill_id,
            'skill_name': skill.name,
            'content': skill.content,
            'confidence': skill.confidence,
            'sources': skill.sources,
        }

    def _handle_profile_intent(self, context: Dict) -> Dict:
        """处理档案分析意图"""
        github_username = context.get('github_username') or context.get('username')

        if not github_username:
            return {'success': False, 'error': '缺少github_username参数'}

        # 分析GitHub档案
        analysis = self.dna.analyze_github_profile(github_username)

        # 生成专长报告
        report = self.dna.get_expertise_report()

        # 发射洞察信息素
        self._emit_pheromone(PheromoneType.INSIGHT, {
            'github_user': github_username,
            'expertise_domains': list(report.get('expertise_domains', {}).keys()),
            'skill_diversity': report.get('skill_diversity', 0),
        })

        return {
            'success': True,
            'github_username': github_username,
            'analysis': analysis,
            'expertise_report': report,
        }

    def _handle_recommend_intent(self, context: Dict) -> Dict:
        """处理推荐意图"""
        domain = context.get('domain') or context.get('target_domain')

        if not domain:
            # 基于当前专长推荐
            report = self.dna.get_expertise_report()
            domains = list(report.get('expertise_domains', {}).keys())
            if not domains:
                return {'success': False, 'error': '未指定domain且无专长数据'}
            domain = domains[0]

        recommendations = self.dna.recommend_learning_path(domain)

        return {
            'success': True,
            'target_domain': domain,
            'recommendations': recommendations,
        }

    # ==================== 信息素协作接口 ====================

    def _emit_pheromone(
        self,
        pheromone_type: PheromoneType,
        payload: Dict,
        target: Optional[str] = None,
        intensity: float = 1.0
    ):
        """
        发射信息素

        符合MindSymphony信息素协作协议:
        - 向协作网络发送信号
        - 可被其他技能感知和响应
        - 支持广播和点对点通信
        """
        pheromone = Pheromone(
            type=pheromone_type,
            source=self.manifest.name,
            target=target,
            intensity=intensity,
            payload=payload,
        )

        self._pheromone_queue.append(pheromone)

        # 实际实现中，这里会将信息素写入共享存储或消息队列
        # 供其他技能消费

    def receive_pheromone(self, pheromone: Pheromone) -> bool:
        """
        接收信息素

        响应其他技能发来的协作请求
        """
        # 检查是否是发给自己的
        if pheromone.target and pheromone.target != self.manifest.name:
            return False

        # 处理不同类型的信息素
        if pheromone.type == PheromoneType.REQUEST:
            # 检查是否能提供帮助
            requested_capability = pheromone.payload.get('capability')
            if requested_capability in self.manifest.capabilities:
                # 发射能力信息素响应
                self._emit_pheromone(
                    PheromoneType.CAPABILITY,
                    {
                        'capability': requested_capability,
                        'provider': self.manifest.name,
                        'ready': True,
                    },
                    target=pheromone.source
                )
                return True

        elif pheromone.type == PheromoneType.DELIVERABLE:
            # 其他技能交付的成果，可能触发后续处理
            deliverable_type = pheromone.payload.get('type')
            if deliverable_type == 'github_repo':
                # 自动蒸馏接收到的GitHub仓库
                repo_url = pheromone.payload.get('repo_url')
                if repo_url:
                    self.execute('distill', {'repo_url': repo_url})
                    return True

        return False

    def get_pheromones(self, pheromone_type: Optional[PheromoneType] = None) -> List[Pheromone]:
        """获取信息素队列中的信息素"""
        if pheromone_type is None:
            return self._pheromone_queue.copy()
        return [p for p in self._pheromone_queue if p.type == pheromone_type]

    # ==================== 协同进化接口 ====================

    def evolve_from_feedback(self, feedback: Dict[str, Any]):
        """
        基于反馈进化

        符合协同进化第一性原理:
        - 从每次交互中学习
        - 将经验沉淀为系统改进
        - 持续优化技能库
        """
        # 记录反馈
        feedback_record = {
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback,
            'user_id': self.user_id,
        }

        # 存储反馈历史
        feedback_path = Path(f"~/.mindsymphony/github_skills/feedback.json").expanduser()
        feedback_path.parent.mkdir(parents=True, exist_ok=True)

        history = []
        if feedback_path.exists():
            with open(feedback_path, 'r', encoding='utf-8') as f:
                history = json.load(f)

        history.append(feedback_record)

        with open(feedback_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        # 发射进化信息素
        self._emit_pheromone(PheromoneType.EVOLUTION, {
            'type': 'feedback_integration',
            'improvement_area': feedback.get('improvement_area'),
            'confidence_change': feedback.get('confidence_delta', 0),
        })

        # 实际改进逻辑
        if feedback.get('skill_id') and feedback.get('success') is False:
            # 技能使用失败，降低相关技能的置信度
            skill_id = feedback['skill_id']
            # 这里可以调整知识图谱中的权重

    def export_evolution_report(self) -> Dict:
        """导出进化报告"""
        feedback_path = Path(f"~/.mindsymphony/github_skills/feedback.json").expanduser()

        if not feedback_path.exists():
            return {'evolution_stage': 'initial', 'feedback_count': 0}

        with open(feedback_path, 'r', encoding='utf-8') as f:
            history = json.load(f)

        # 分析反馈趋势
        success_count = sum(1 for h in history if h['feedback'].get('success', True))
        total_count = len(history)

        return {
            'evolution_stage': 'maturing' if total_count > 10 else 'learning',
            'feedback_count': total_count,
            'success_rate': success_count / total_count if total_count > 0 else 0,
            'recent_improvements': [
                h['feedback'].get('improvement_area')
                for h in history[-5:]
                if h['feedback'].get('improvement_area')
            ],
        }

    # ==================== 价值对齐接口 ====================

    def align_value(self, user_intent: str, explicit: bool = True) -> Dict:
        """
        价值对齐检查

        符合价值对齐第一性原理:
        - 理解显性意图
        - 挖掘隐性意图
        - 确保输出符合真实需求
        """
        alignment = {
            'explicit_intent': user_intent,
            'layer_alignment': self._identify_layer(user_intent),
            'capabilities_required': [],
            'suggested_approach': '',
        }

        # 分析意图所属层级
        layer = alignment['layer_alignment']

        if layer == Layer.TAO:
            alignment['suggested_approach'] = '先澄清价值目标，再进入技能蒸馏'
            alignment['capabilities_required'] = ['value_clarification']
        elif layer == Layer.FA:
            alignment['suggested_approach'] = '制定技能获取战略，规划学习路径'
            alignment['capabilities_required'] = ['strategic_planning', 'skill_recommendation']
        elif layer == Layer.SHU:
            alignment['suggested_approach'] = '直接执行技能蒸馏或生成'
            alignment['capabilities_required'] = ['skill_distillation', 'dynamic_skill_generation']
        elif layer == Layer.QI:
            alignment['suggested_approach'] = '提供可直接使用的技能文件'
            alignment['capabilities_required'] = ['skill_export', 'integration']

        return alignment

    def _identify_layer(self, intent: str) -> Layer:
        """识别意图所属道法术器层级"""
        intent_lower = intent.lower()

        # 道层关键词
        tao_keywords = ['为什么', '价值', '意义', '目标', '愿景', '为什么做']
        if any(kw in intent_lower for kw in tao_keywords):
            return Layer.TAO

        # 法层关键词
        fa_keywords = ['规划', '战略', '计划', '路线图', '如何规划', '做什么']
        if any(kw in intent_lower for kw in fa_keywords):
            return Layer.FA

        # 器层关键词
        qi_keywords = ['执行', '操作', '具体', '工具', '怎么用', '具体步骤']
        if any(kw in intent_lower for kw in qi_keywords):
            return Layer.QI

        # 默认术层
        return Layer.SHU

    # ==================== 安全优先接口 ====================

    def safety_check(self, operation: str, params: Dict) -> Dict:
        """
        安全检查

        符合安全优先第一性原理:
        - 明确操作影响
        - 请求必要确认
        - 提供回滚方案
        """
        check_result = {
            'operation': operation,
            'is_safe': True,
            'requires_confirmation': False,
            'risk_level': 'low',
            'impact_description': '',
            'suggested_precautions': [],
        }

        if operation == 'distill':
            repo_url = params.get('repo_url', '')
            check_result['impact_description'] = f'将从GitHub仓库 {repo_url} 提取内容并生成本地技能文件'
            check_result['risk_level'] = 'low'

        elif operation == 'persist_skill':
            check_result['requires_confirmation'] = True
            check_result['risk_level'] = 'medium'
            check_result['impact_description'] = '将修改本地技能图谱和文件系统'
            check_result['suggested_precautions'] = [
                '确保磁盘空间充足',
                '备份现有技能库（可选）',
            ]

        elif operation == 'clear_graph':
            check_result['requires_confirmation'] = True
            check_result['risk_level'] = 'high'
            check_result['impact_description'] = '将清空所有技能数据，此操作不可逆'
            check_result['suggested_precautions'] = [
                '强烈建议先备份',
                '确认理解数据丢失风险',
            ]

        return check_result


# ==================== 便捷函数 ====================

def create_github_skill_adapter(user_id: Optional[str] = None) -> GitHubSkillAdapter:
    """
    创建GitHub技能适配器实例

    符合MindSymphony的简洁创建模式
    """
    return GitHubSkillAdapter(user_id=user_id)


def distill_skill(repo_url: str, **kwargs) -> Dict:
    """
    快速蒸馏技能 - 便捷函数

    【术】层快速执行接口
    """
    adapter = create_github_skill_adapter()
    return adapter.execute('distill', {'repo_url': repo_url, **kwargs})


def search_skill_library(query: str, **kwargs) -> Dict:
    """
    搜索技能库 - 便捷函数
    """
    adapter = create_github_skill_adapter()
    return adapter.execute('search', {'query': query, **kwargs})


def generate_skill_for_task(task: str, **kwargs) -> Dict:
    """
    为任务生成技能 - 便捷函数
    """
    adapter = create_github_skill_adapter()
    return adapter.execute('generate', {'task': task, **kwargs})
