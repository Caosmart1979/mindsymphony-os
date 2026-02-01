"""
Lightning Store - 中心化数据存储

核心职责:
1. Span 存储 - 追踪事件持久化
2. Episode 管理 - 完整任务序列
3. Prompt 版本 - APO 提示词历史
4. Metrics 聚合 - 性能指标统计

存储后端:
- 默认: SQLite (本地文件)
- 可选: PostgreSQL (集中式)
- 缓存: 内存 LRU
"""

import os
import json
import sqlite3
import threading
from typing import Any, Dict, List, Optional, Union
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
import hashlib


class LightningStore:
    """Lightning 数据存储中心

    类比: Agent Lightning 的 LightningStore
    功能: 任务、资源、轨迹的统一存储

    表结构:
    - spans: 原始追踪数据
    - episodes: 任务序列聚合
    - rewards: 奖励信号
    - prompt_versions: 提示词版本 (APO用)
    - metrics: 聚合指标

    示例:
        store = LightningStore()

        # 存储 span
        store.store_span(span)

        # 查询技能性能
        stats = store.get_skill_stats("cognitive-architect", days=7)

        # 存储提示词版本
        store.store_prompt_version("knowledge-explorer", prompt_template, performance_score)
    """

    def __init__(self, db_path: Optional[str] = None):
        # 默认存储路径
        if db_path is None:
            base_dir = Path.home() / ".claude" / "mindsymphony-v21" / "lightning"
            base_dir.mkdir(parents=True, exist_ok=True)
            db_path = base_dir / "store.db"

        self.db_path = str(db_path)
        self._local = threading.local()
        self._init_database()

    def _get_connection(self) -> sqlite3.Connection:
        """获取线程安全的数据库连接"""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _init_database(self):
        """初始化数据库表结构"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Spans 表 - 原始追踪数据
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spans (
                span_id TEXT PRIMARY KEY,
                trace_id TEXT NOT NULL,
                parent_id TEXT,
                span_type TEXT NOT NULL,
                name TEXT NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL,
                duration_ms REAL,
                input_hash TEXT,
                input_data TEXT,
                output_hash TEXT,
                output_data TEXT,
                latency_ms REAL,
                token_count INTEGER,
                metadata TEXT,
                tags TEXT,
                status TEXT DEFAULT 'ok',
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Episodes 表 - 任务序列聚合
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                episode_id TEXT PRIMARY KEY,
                trace_id TEXT UNIQUE NOT NULL,
                skill_sequence TEXT,  -- JSON array of skill names
                total_duration_ms REAL,
                success_count INTEGER DEFAULT 0,
                error_count INTEGER DEFAULT 0,
                final_status TEXT,
                user_feedback TEXT,
                aggregated_reward REAL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Rewards 表 - 奖励信号
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rewards (
                reward_id INTEGER PRIMARY KEY AUTOINCREMENT,
                episode_id TEXT,
                span_id TEXT,
                reward_type TEXT NOT NULL,  -- 'explicit', 'implicit', 'computed'
                reward_value REAL NOT NULL,
                confidence REAL DEFAULT 1.0,
                source TEXT,  -- 奖励来源说明
                timestamp REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (episode_id) REFERENCES episodes(episode_id),
                FOREIGN KEY (span_id) REFERENCES spans(span_id)
            )
        """)

        # Prompt versions 表 - APO 提示词版本管理
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_versions (
                version_id TEXT PRIMARY KEY,
                skill_name TEXT NOT NULL,
                prompt_template TEXT NOT NULL,
                prompt_hash TEXT UNIQUE NOT NULL,
                performance_score REAL,
                sample_count INTEGER DEFAULT 0,
                success_rate REAL,
                avg_latency_ms REAL,
                is_active BOOLEAN DEFAULT 0,
                is_candidate BOOLEAN DEFAULT 0,  -- A/B 测试候选
                ab_test_group TEXT,  -- 'control', 'treatment', NULL
                parent_version_id TEXT,
                optimization_strategy TEXT,  -- 'lightning-rag', 'cot', etc.
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_version_id) REFERENCES prompt_versions(version_id)
            )
        """)

        # Metrics 表 - 聚合指标（按时间窗口）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_type TEXT NOT NULL,  -- 'skill', 'system', 'apo'
                target_name TEXT,  -- skill_name or system_component
                time_window TEXT,  -- 'hourly', 'daily', 'weekly'
                timestamp TEXT NOT NULL,
                value REAL NOT NULL,
                count INTEGER DEFAULT 1,
                metadata TEXT,
                UNIQUE(metric_name, target_name, time_window, timestamp)
            )
        """)

        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_spans_trace ON spans(trace_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_spans_type ON spans(span_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_spans_name ON spans(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_spans_time ON spans(start_time)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rewards_episode ON rewards(episode_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_prompts_skill ON prompt_versions(skill_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_prompts_active ON prompt_versions(is_active)")

        conn.commit()

    def store_span(self, span) -> bool:
        """存储追踪事件

        Args:
            span: Span 对象 (来自 tracer.core)

        Returns:
            bool: 是否成功
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            span_dict = span.to_dict() if hasattr(span, 'to_dict') else span

            cursor.execute("""
                INSERT OR REPLACE INTO spans (
                    span_id, trace_id, parent_id, span_type, name,
                    start_time, end_time, duration_ms,
                    input_hash, input_data, output_hash, output_data,
                    latency_ms, token_count, metadata, tags, status, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                span_dict.get('span_id'),
                span_dict.get('trace_id'),
                span_dict.get('parent_id'),
                span_dict.get('span_type'),
                span_dict.get('name'),
                span_dict.get('start_time'),
                span_dict.get('end_time'),
                span_dict.get('duration_ms'),
                span_dict.get('input_hash'),
                span_dict.get('input_data'),
                span_dict.get('output_hash'),
                span_dict.get('output_data'),
                span_dict.get('latency_ms'),
                span_dict.get('token_count'),
                json.dumps(span_dict.get('metadata', {})),
                json.dumps(span_dict.get('tags', [])),
                span_dict.get('status', 'ok'),
                span_dict.get('error_message')
            ))

            conn.commit()
            return True

        except Exception as e:
            print(f"[Store] Error storing span: {e}")
            return False

    def store_episode(self, episode_data: Dict) -> bool:
        """存储任务序列 (Episode)

        Args:
            episode_data: 包含 trace_id, skill_sequence, rewards 等
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO episodes (
                    episode_id, trace_id, skill_sequence, total_duration_ms,
                    success_count, error_count, final_status, user_feedback,
                    aggregated_reward, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                episode_data.get('episode_id'),
                episode_data.get('trace_id'),
                json.dumps(episode_data.get('skill_sequence', [])),
                episode_data.get('total_duration_ms'),
                episode_data.get('success_count', 0),
                episode_data.get('error_count', 0),
                episode_data.get('final_status'),
                episode_data.get('user_feedback'),
                episode_data.get('aggregated_reward'),
                json.dumps(episode_data.get('metadata', {}))
            ))

            conn.commit()
            return True

        except Exception as e:
            print(f"[Store] Error storing episode: {e}")
            return False

    def store_reward(self, reward_data: Dict) -> bool:
        """存储奖励信号"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO rewards (
                    episode_id, span_id, reward_type, reward_value,
                    confidence, source, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                reward_data.get('episode_id'),
                reward_data.get('span_id'),
                reward_data.get('reward_type'),
                reward_data.get('reward_value'),
                reward_data.get('confidence', 1.0),
                reward_data.get('source'),
                reward_data.get('timestamp', datetime.now().timestamp())
            ))

            conn.commit()
            return True

        except Exception as e:
            print(f"[Store] Error storing reward: {e}")
            return False

    def store_prompt_version(
        self,
        skill_name: str,
        prompt_template: str,
        performance_score: Optional[float] = None,
        is_active: bool = False,
        is_candidate: bool = False,
        parent_version_id: Optional[str] = None,
        optimization_strategy: Optional[str] = None
    ) -> Optional[str]:
        """存储提示词版本 (APO用)

        Returns:
            version_id: 生成的版本ID
        """
        try:
            version_id = f"{skill_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(prompt_template.encode()).hexdigest()[:8]}"
            prompt_hash = hashlib.sha256(prompt_template.encode()).hexdigest()

            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO prompt_versions (
                    version_id, skill_name, prompt_template, prompt_hash,
                    performance_score, is_active, is_candidate,
                    parent_version_id, optimization_strategy
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                version_id, skill_name, prompt_template, prompt_hash,
                performance_score, is_active, is_candidate,
                parent_version_id, optimization_strategy
            ))

            conn.commit()
            return version_id

        except Exception as e:
            print(f"[Store] Error storing prompt version: {e}")
            return None

    def get_skill_stats(self, skill_name: str, days: int = 7) -> Dict:
        """获取技能性能统计"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            since = (datetime.now() - timedelta(days=days)).timestamp()

            cursor.execute("""
                SELECT
                    COUNT(*) as total_invocations,
                    SUM(CASE WHEN status = 'ok' THEN 1 ELSE 0 END) as success_count,
                    AVG(duration_ms) as avg_duration_ms,
                    AVG(latency_ms) as avg_latency_ms,
                    AVG(token_count) as avg_token_count
                FROM spans
                WHERE name = ? AND start_time > ? AND span_type = 'skill_invocation'
            """, (skill_name, since))

            row = cursor.fetchone()

            if row and row[0] > 0:
                total = row[0]
                success = row[1]
                return {
                    "skill_name": skill_name,
                    "total_invocations": total,
                    "success_count": success,
                    "error_count": total - success,
                    "success_rate": success / total if total > 0 else 0,
                    "avg_duration_ms": row[2] or 0,
                    "avg_latency_ms": row[3] or 0,
                    "avg_token_count": row[4] or 0,
                    "period_days": days
                }

            return {
                "skill_name": skill_name,
                "total_invocations": 0,
                "success_count": 0,
                "error_count": 0,
                "success_rate": 0,
                "period_days": days
            }

        except Exception as e:
            print(f"[Store] Error getting skill stats: {e}")
            return {}

    def get_active_prompt(self, skill_name: str) -> Optional[Dict]:
        """获取当前生效的提示词版本"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM prompt_versions
                WHERE skill_name = ? AND is_active = 1
                ORDER BY created_at DESC
                LIMIT 1
            """, (skill_name,))

            row = cursor.fetchone()

            if row:
                return {
                    "version_id": row[0],
                    "skill_name": row[1],
                    "prompt_template": row[2],
                    "performance_score": row[4],
                    "sample_count": row[5],
                    "success_rate": row[6],
                    "created_at": row[10]
                }

            return None

        except Exception as e:
            print(f"[Store] Error getting active prompt: {e}")
            return None

    def get_prompt_candidates(self, skill_name: str, limit: int = 5) -> List[Dict]:
        """获取 A/B 测试候选提示词"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM prompt_versions
                WHERE skill_name = ? AND is_candidate = 1
                ORDER BY performance_score DESC NULLS LAST
                LIMIT ?
            """, (skill_name, limit))

            candidates = []
            for row in cursor.fetchall():
                candidates.append({
                    "version_id": row[0],
                    "prompt_template": row[2],
                    "performance_score": row[4],
                    "sample_count": row[5],
                    "success_rate": row[6],
                    "optimization_strategy": row[9]
                })

            return candidates

        except Exception as e:
            print(f"[Store] Error getting prompt candidates: {e}")
            return []

    def set_active_prompt(self, version_id: str) -> bool:
        """设置生效的提示词版本"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # 先取消当前生效版本
            cursor.execute("""
                SELECT skill_name FROM prompt_versions WHERE version_id = ?
            """, (version_id,))

            row = cursor.fetchone()
            if not row:
                return False

            skill_name = row[0]

            cursor.execute("""
                UPDATE prompt_versions SET is_active = 0
                WHERE skill_name = ?
            """, (skill_name,))

            # 设置新版本
            cursor.execute("""
                UPDATE prompt_versions SET is_active = 1, is_candidate = 0
                WHERE version_id = ?
            """, (version_id,))

            conn.commit()
            return True

        except Exception as e:
            print(f"[Store] Error setting active prompt: {e}")
            return False

    def query_spans(
        self,
        skill_name: Optional[str] = None,
        span_type: Optional[str] = None,
        status: Optional[str] = None,
        since: Optional[float] = None,
        limit: int = 100
    ) -> List[Dict]:
        """查询追踪事件"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            conditions = []
            params = []

            if skill_name:
                conditions.append("name = ?")
                params.append(skill_name)

            if span_type:
                conditions.append("span_type = ?")
                params.append(span_type)

            if status:
                conditions.append("status = ?")
                params.append(status)

            if since:
                conditions.append("start_time > ?")
                params.append(since)

            where_clause = " AND ".join(conditions) if conditions else "1=1"

            cursor.execute(f"""
                SELECT * FROM spans
                WHERE {where_clause}
                ORDER BY start_time DESC
                LIMIT ?
            """, params + [limit])

            spans = []
            for row in cursor.fetchall():
                spans.append({
                    "span_id": row[0],
                    "trace_id": row[1],
                    "span_type": row[3],
                    "name": row[4],
                    "start_time": row[5],
                    "duration_ms": row[7],
                    "status": row[16],
                    "error_message": row[17]
                })

            return spans

        except Exception as e:
            print(f"[Store] Error querying spans: {e}")
            return []

    def get_metrics_summary(self, days: int = 7) -> Dict:
        """获取整体指标摘要"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            since = (datetime.now() - timedelta(days=days)).timestamp()

            # 总追踪数
            cursor.execute("SELECT COUNT(*) FROM spans WHERE start_time > ?", (since,))
            total_spans = cursor.fetchone()[0]

            # 成功率
            cursor.execute("""
                SELECT
                    SUM(CASE WHEN status = 'ok' THEN 1 ELSE 0 END),
                    COUNT(*)
                FROM spans
                WHERE start_time > ? AND span_type = 'skill_invocation'
            """, (since,))

            row = cursor.fetchone()
            success_rate = (row[0] / row[1]) if row and row[1] > 0 else 0

            # 活跃技能数
            cursor.execute("""
                SELECT COUNT(DISTINCT name) FROM spans
                WHERE start_time > ? AND span_type = 'skill_invocation'
            """, (since,))

            active_skills = cursor.fetchone()[0]

            # 提示词版本数
            cursor.execute("SELECT COUNT(*) FROM prompt_versions")
            prompt_versions = cursor.fetchone()[0]

            return {
                "period_days": days,
                "total_spans": total_spans,
                "success_rate": success_rate,
                "active_skills": active_skills,
                "prompt_versions": prompt_versions
            }

        except Exception as e:
            print(f"[Store] Error getting metrics summary: {e}")
            return {}

    def close(self):
        """关闭数据库连接"""
        if hasattr(self._local, 'conn') and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
