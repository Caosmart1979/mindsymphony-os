"""
Lightning Bridge - BMAD 与 Lightning Layer 的数据桥接
实现工作流追踪、自适应学习和 APO 集成
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class BMADLightningBridge:
    """
    BMAD - Lightning Layer 数据桥

    功能:
    1. 追踪 BMAD 工作流事件
    2. 收集成功率数据
    3. 驱动自适应优化
    4. 与 APO Pipeline 集成
    """

    def __init__(self, lightning_integration: Optional[Any] = None):
        """
        初始化桥接器

        Args:
            lightning_integration: Lightning Layer 集成对象
        """
        self.lightning = lightning_integration
        self.tracer = getattr(lightning_integration, 'tracer', None) if lightning_integration else None
        self.store = getattr(lightning_integration, 'store', None) if lightning_integration else None

        # 自适应配置
        self.adaptive_config = {
            "threshold_optimization_enabled": True,
            "min_samples_for_adjustment": 20,
            "target_success_rate": 0.85,
            "adjustment_delta": 0.5,
        }

    def emit_workflow_event(
        self,
        event_type: str,
        workflow_type: str,
        execution_id: str,
        data: Dict[str, Any]
    ):
        """
        发送工作流事件到 Lightning

        Args:
            event_type: 事件类型 (started, completed, stage_completed)
            workflow_type: 工作流类型 (quick, full, party)
            execution_id: 执行ID
            data: 事件数据
        """
        if not self.tracer:
            return

        try:
            event_data = {
                "bmad_event": True,
                "event_type": event_type,
                "workflow_type": workflow_type,
                "execution_id": execution_id,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }

            # 使用 tracer 记录
            if hasattr(self.tracer, 'emit_custom_event'):
                self.tracer.emit_custom_event("bmad_workflow", event_data)
            elif hasattr(self.tracer, 'emit_span'):
                self.tracer.emit_span("bmad", event_data)

        except Exception as e:
            print(f"[BMAD Lightning] Failed to emit event: {e}")

    def record_workflow_success(
        self,
        workflow_type: str,
        execution_id: str,
        complexity_score: int,
        duration_minutes: float,
        user_satisfaction: Optional[int] = None,
        success: bool = True
    ):
        """
        记录工作流执行结果

        Args:
            workflow_type: 工作流类型
            execution_id: 执行ID
            complexity_score: 复杂度评分
            duration_minutes: 执行时长
            user_satisfaction: 用户满意度 (1-5)
            success: 是否成功
        """
        if not self.store:
            return

        try:
            record = {
                "type": "bmad_workflow_result",
                "workflow_type": workflow_type,
                "execution_id": execution_id,
                "complexity_score": complexity_score,
                "duration_minutes": duration_minutes,
                "user_satisfaction": user_satisfaction,
                "success": success,
                "timestamp": datetime.now().isoformat()
            }

            # 存储到 store
            if hasattr(self.store, 'store_metric'):
                self.store.store_metric(f"bmad_{workflow_type}", record)

        except Exception as e:
            print(f"[BMAD Lightning] Failed to record result: {e}")

    def get_workflow_stats(
        self,
        workflow_type: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        获取工作流统计

        Args:
            workflow_type: 可选的工作流类型过滤
            days: 统计天数

        Returns:
            统计信息
        """
        if not self.store:
            return self._get_default_stats()

        try:
            # 从 store 查询数据
            if hasattr(self.store, 'get_metrics_summary'):
                metrics = self.store.get_metrics_summary(days=days)

                # 过滤 BMAD 相关指标
                bmad_metrics = {
                    k: v for k, v in metrics.items()
                    if k.startswith("bmad_")
                }

                return self._calculate_stats(bmad_metrics, workflow_type)

        except Exception as e:
            print(f"[BMAD Lightning] Failed to get stats: {e}")

        return self._get_default_stats()

    def _calculate_stats(
        self,
        metrics: Dict,
        workflow_type: Optional[str] = None
    ) -> Dict:
        """计算统计数据"""
        stats = {
            "quick": {"success_rate": 0.0, "avg_duration": 0, "count": 0},
            "full": {"success_rate": 0.0, "avg_duration": 0, "count": 0},
            "party": {"success_rate": 0.0, "avg_duration": 0, "count": 0},
        }

        # 处理指标数据
        for key, records in metrics.items():
            wf_type = key.replace("bmad_", "")
            if workflow_type and wf_type != workflow_type:
                continue

            if wf_type in stats and records:
                successes = sum(1 for r in records if r.get("success"))
                total = len(records)
                durations = [r.get("duration_minutes", 0) for r in records]

                stats[wf_type] = {
                    "success_rate": successes / total if total > 0 else 0.0,
                    "avg_duration": sum(durations) / len(durations) if durations else 0,
                    "count": total
                }

        return stats

    def _get_default_stats(self) -> Dict:
        """获取默认统计"""
        return {
            "quick": {"success_rate": 0.85, "avg_duration": 10, "count": 0},
            "full": {"success_rate": 0.80, "avg_duration": 35, "count": 0},
            "party": {"success_rate": 0.75, "avg_duration": 50, "count": 0},
        }

    def should_adjust_thresholds(self) -> Optional[Dict]:
        """
        检查是否需要调整复杂度阈值

        Returns:
            调整建议或 None
        """
        if not self.adaptive_config["threshold_optimization_enabled"]:
            return None

        stats = self.get_workflow_stats()
        adjustments = []

        # 检查 Quick Flow 成功率
        quick_stats = stats.get("quick", {})
        if quick_stats.get("count", 0) >= self.adaptive_config["min_samples_for_adjustment"]:
            success_rate = quick_stats.get("success_rate", 0)
            target = self.adaptive_config["target_success_rate"]

            if success_rate < target - 0.1:  # 低于目标10%
                adjustments.append({
                    "threshold": "quick_flow_max",
                    "action": "increase",
                    "reason": f"Quick Flow 成功率过低 ({success_rate:.1%})",
                    "delta": self.adaptive_config["adjustment_delta"]
                })
            elif success_rate > target + 0.1:  # 高于目标10%
                adjustments.append({
                    "threshold": "quick_flow_max",
                    "action": "decrease",
                    "reason": f"Quick Flow 成功率很高 ({success_rate:.1%})",
                    "delta": -self.adaptive_config["adjustment_delta"]
                })

        # 检查 Full Planning 成功率
        full_stats = stats.get("full", {})
        if full_stats.get("count", 0) >= self.adaptive_config["min_samples_for_adjustment"]:
            success_rate = full_stats.get("success_rate", 0)

            if success_rate > 0.9:  # 非常高，可以扩大范围
                adjustments.append({
                    "threshold": "full_flow_min",
                    "action": "decrease",
                    "reason": f"Full Planning 成功率很高 ({success_rate:.1%})",
                    "delta": -self.adaptive_config["adjustment_delta"]
                })

        return {
            "should_adjust": len(adjustments) > 0,
            "adjustments": adjustments,
            "current_stats": stats
        } if adjustments else None

    def get_optimal_party_roles(
        self,
        domain: str,
        min_samples: int = 10
    ) -> List[str]:
        """
        获取最优的 Party 角色组合

        Args:
            domain: 领域名称
            min_samples: 最小样本数

        Returns:
            推荐的角色列表
        """
        # 默认推荐
        default_roles = ["architect", "developer"]

        if not self.store:
            return default_roles

        try:
            # 查询历史 Party 会话
            if hasattr(self.store, 'query'):
                results = self.store.query(
                    metric_type="bmad_party",
                    filters={"domain": domain},
                    limit=100
                )

                if len(results) >= min_samples:
                    # 分析最佳角色组合
                    role_combinations = {}
                    for r in results:
                        roles = tuple(sorted(r.get("roles", [])))
                        if roles not in role_combinations:
                            role_combinations[roles] = {"successes": 0, "total": 0}

                        role_combinations[roles]["total"] += 1
                        if r.get("success"):
                            role_combinations[roles]["successes"] += 1

                    # 找成功率最高的组合
                    best_combo = None
                    best_rate = 0.0
                    for roles, counts in role_combinations.items():
                        if counts["total"] >= min_samples:
                            rate = counts["successes"] / counts["total"]
                            if rate > best_rate:
                                best_rate = rate
                                best_combo = roles

                    if best_combo:
                        return list(best_combo)

        except Exception as e:
            print(f"[BMAD Lightning] Failed to get optimal roles: {e}")

        return default_roles

    def export_learning_report(self, days: int = 30) -> str:
        """
        导出学习报告

        Args:
            days: 统计天数

        Returns:
            报告文本
        """
        stats = self.get_workflow_stats(days=days)
        threshold_adjustments = self.should_adjust_thresholds()

        report = f"""
# BMAD 学习报告 ({days}天)

## 工作流统计

| 工作流 | 成功率 | 平均时长 | 执行次数 |
|--------|--------|----------|----------|
| Quick Flow | {stats['quick']['success_rate']:.1%} | {stats['quick']['avg_duration']:.0f}分钟 | {stats['quick']['count']} |
| Full Planning | {stats['full']['success_rate']:.1%} | {stats['full']['avg_duration']:.0f}分钟 | {stats['full']['count']} |
| Party Mode | {stats['party']['success_rate']:.1%} | {stats['party']['avg_duration']:.0f}分钟 | {stats['party']['count']} |

## 优化建议
"""

        if threshold_adjustments and threshold_adjustments["should_adjust"]:
            report += "\n### 阈值调整\n"
            for adj in threshold_adjustments["adjustments"]:
                report += f"- {adj['reason']}\n"
                report += f"  建议: {adj['action']} {adj['threshold']} by {adj['delta']}\n"
        else:
            report += "\n当前阈值配置运行良好，无需调整。\n"

        report += """
## 最佳实践

基于历史数据分析：

"""
        # 添加成功率最高的工作流类型
        best_workflow = max(stats.items(), key=lambda x: x[1].get('success_rate', 0))
        report += f"- {best_workflow[0].title()} 表现最佳，成功率 {best_workflow[1]['success_rate']:.1%}\n"

        return report


# 便捷函数
def get_lightning_bridge(lightning_integration: Optional[Any] = None) -> BMADLightningBridge:
    """获取 Lightning Bridge 实例"""
    return BMADLightningBridge(lightning_integration)
