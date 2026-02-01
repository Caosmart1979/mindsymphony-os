"""
Skill Hub - Database Layer
SQLite 数据库操作
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from models import SkillMetadata, SourceType, SearchResult


class Database:
    """Skill Hub 数据库"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    @property
    def conn(self) -> sqlite3.Connection:
        """获取数据库连接（懒加载）"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _init_db(self):
        """初始化数据库表"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)

        with self.conn as conn:
            # 远程技能表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS remote_skills (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    source TEXT NOT NULL,
                    description TEXT,
                    author TEXT,
                    url TEXT,
                    repo_url TEXT,
                    metadata_json TEXT,
                    cached_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 本地技能表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS local_skills (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    description TEXT,
                    triggers_json TEXT,
                    tags_json TEXT,
                    last_scanned TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 搜索历史表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    sources TEXT,
                    result_count INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_remote_name ON remote_skills(name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_remote_source ON remote_skills(source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_local_name ON local_skills(name)")

            conn.commit()

    # ===== 远程技能操作 =====

    def save_remote_skill(self, metadata: SkillMetadata) -> None:
        """保存远程技能元数据"""
        skill_id = f"{metadata.source.value}:{metadata.name}"

        metadata_json = json.dumps({
            'triggers': metadata.triggers,
            'tags': metadata.tags,
            'file_list': metadata.file_list,
            'frontmatter': metadata.frontmatter,
            'github_stats': {
                'stars': metadata.github_stats.stars if metadata.github_stats else 0,
                'forks': metadata.github_stats.forks if metadata.github_stats else 0,
                'last_commit': metadata.github_stats.last_commit.isoformat() if metadata.github_stats and metadata.github_stats.last_commit else None,
                'license': metadata.github_stats.license if metadata.github_stats else None,
            } if metadata.github_stats else None,
            'user_rating': metadata.user_rating,
            'dependencies': metadata.dependencies,
        })

        with self.conn as conn:
            conn.execute("""
                INSERT OR REPLACE INTO remote_skills
                (id, name, source, description, author, url, repo_url, metadata_json, cached_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                skill_id,
                metadata.name,
                metadata.source.value,
                metadata.description,
                metadata.author,
                metadata.url,
                metadata.repo_url,
                metadata_json,
                datetime.now().isoformat()
            ))
            conn.commit()

    def get_remote_skill(self, name: str, source: SourceType) -> Optional[SkillMetadata]:
        """获取远程技能元数据"""
        skill_id = f"{source.value}:{name}"

        row = self.conn.execute(
            "SELECT * FROM remote_skills WHERE id = ?",
            (skill_id,)
        ).fetchone()

        if row:
            return self._row_to_metadata(row)
        return None

    def search_remote_skills(self, query: str, source: Optional[SourceType] = None) -> List[Dict]:
        """搜索远程技能"""
        sql = "SELECT * FROM remote_skills WHERE name LIKE ? OR description LIKE ?"
        params = [f"%{query}%", f"%{query}%"]

        if source:
            sql += " AND source = ?"
            params.append(source.value)

        rows = self.conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    def list_remote_skills(self, source: Optional[SourceType] = None) -> List[Dict]:
        """列出所有远程技能"""
        sql = "SELECT * FROM remote_skills"
        if source:
            sql += " WHERE source = ?"

        rows = self.conn.execute(sql, [source.value] if source else []).fetchall()
        return [dict(row) for row in rows]

    def _row_to_metadata(self, row: sqlite3.Row) -> SkillMetadata:
        """数据库行转为 SkillMetadata"""
        from models import GitHubStats

        meta_dict = json.loads(row['metadata_json'])

        return SkillMetadata(
            name=row['name'],
            source=SourceType(row['source']),
            description=row['description'] or "",
            author=row['author'] or "",
            url=row['url'] or "",
            repo_url=row['repo_url'] or "",
            triggers=meta_dict.get('triggers', {}),
            tags=meta_dict.get('tags', []),
            file_list=meta_dict.get('file_list', []),
            frontmatter=meta_dict.get('frontmatter', {}),
            github_stats=GitHubStats(**meta_dict['github_stats']) if meta_dict.get('github_stats') else None,
            user_rating=meta_dict.get('user_rating'),
            dependencies=meta_dict.get('dependencies', []),
        )

    # ===== 本地技能操作 =====

    def save_local_skill(self, skill_id: str, name: str, path: str,
                        description: str, triggers: Dict, tags: List[str]) -> None:
        """保存本地技能"""
        with self.conn as conn:
            conn.execute("""
                INSERT OR REPLACE INTO local_skills
                (id, name, path, description, triggers_json, tags_json, last_scanned)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                skill_id,
                name,
                path,
                description,
                json.dumps(triggers),
                json.dumps(tags),
                datetime.now().isoformat()
            ))
            conn.commit()

    def get_local_skill(self, name: str) -> Optional[Dict]:
        """获取本地技能"""
        row = self.conn.execute(
            "SELECT * FROM local_skills WHERE name = ?",
            (name,)
        ).fetchone()

        return dict(row) if row else None

    def list_local_skills(self) -> List[Dict]:
        """列出所有本地技能"""
        rows = self.conn.execute("SELECT * FROM local_skills").fetchall()
        return [dict(row) for row in rows]

    def search_local_skills(self, query: str) -> List[Dict]:
        """搜索本地技能"""
        rows = self.conn.execute(
            "SELECT * FROM local_skills WHERE name LIKE ? OR description LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        return [dict(row) for row in rows]

    # ===== 搜索历史 =====

    def save_search(self, query: str, sources: List[str], result_count: int) -> None:
        """保存搜索历史"""
        with self.conn as conn:
            conn.execute("""
                INSERT INTO search_history (query, sources, result_count)
                VALUES (?, ?, ?)
            """, (query, json.dumps(sources), result_count))
            conn.commit()

    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """获取最近搜索"""
        rows = self.conn.execute("""
            SELECT * FROM search_history
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]

    # ===== 维护操作 =====

    def cleanup_old_cache(self, days: int = 7) -> int:
        """清理旧缓存"""
        cutoff = datetime.now().replace(day=datetime.now().day - days).isoformat()

        with self.conn as conn:
            cursor = conn.execute(
                "DELETE FROM remote_skills WHERE cached_at < ?",
                (cutoff,)
            )
            conn.commit()
            return cursor.rowcount

    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        stats = {}

        stats['remote_skills'] = self.conn.execute(
            "SELECT COUNT(*) FROM remote_skills"
        ).fetchone()[0]

        stats['local_skills'] = self.conn.execute(
            "SELECT COUNT(*) FROM local_skills"
        ).fetchone()[0]

        stats['searches'] = self.conn.execute(
            "SELECT COUNT(*) FROM search_history"
        ).fetchone()[0]

        # 按来源统计
        for source in ['skillslm', '42plugin', 'github']:
            count = self.conn.execute(
                "SELECT COUNT(*) FROM remote_skills WHERE source = ?",
                (source,)
            ).fetchone()[0]
            stats[f'remote_{source}'] = count

        return stats

    def close(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()
            self._conn = None


def get_database(db_path: str) -> Database:
    """获取数据库实例的便捷函数"""
    return Database(db_path)
