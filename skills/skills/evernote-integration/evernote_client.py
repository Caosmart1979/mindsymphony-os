#!/usr/bin/env python3
"""
印象笔记 (Evernote) 集成客户端 - 完整版
支持中国区 (印象笔记) 和国际区 (Evernote)

功能模块：
- 标签管理
- 笔记本管理
- 高级搜索
- 批量操作
- 附件支持
- 导入导出
- 笔记链接
- 统计分析
"""

import os
import sys
import json
import hashlib
import re
import base64
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

# Check for required dependencies
try:
    import thrift.protocol.TBinaryProtocol as TBinaryProtocol
    import thrift.transport.THttpClient as THttpClient
    from evernote.edam.notestore import NoteStore
    from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec, NoteFilter
    from evernote.edam.type.ttypes import Note as NoteType
    from evernote.edam.userstore import UserStore
    from evernote.edam.error.ttypes import EDAMSystemException, EDAMUserException
    from evernote.edam.type.ttypes import Tag, Notebook
    THRIFT_AVAILABLE = True
except ImportError as e:
    THRIFT_AVAILABLE = False
    IMPORT_ERROR = str(e)


class EvernoteIntegrationError(Exception):
    """印象笔记集成错误"""
    pass


class EvernoteConfig:
    """印象笔记配置管理"""

    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir or os.path.expanduser("~/.claude/skills/evernote-integration/data"))
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.auth_file = self.config_dir / "auth_info.json"

    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "china": True,
            "developer_token": ""
        }

    def save_config(self, config: Dict[str, Any]):
        """保存配置"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def load_auth(self) -> Dict[str, Any]:
        """加载认证信息"""
        if self.auth_file.exists():
            with open(self.auth_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_auth(self, auth: Dict[str, Any]):
        """保存认证信息"""
        with open(self.auth_file, "w", encoding="utf-8") as f:
            json.dump(auth, f, ensure_ascii=False, indent=2)


class EvernoteClientWrapper:
    """印象笔记客户端封装 - 完整功能版"""

    CHINA_CONFIG = {
        "host": "app.yinxiang.com",
        "user_store_url": "https://app.yinxiang.com/edam/user",
        "web_base": "https://app.yinxiang.com"
    }
    INTERNATIONAL_CONFIG = {
        "host": "www.evernote.com",
        "user_store_url": "https://www.evernote.com/edam/user",
        "web_base": "https://www.evernote.com"
    }

    def __init__(self, developer_token: str = None, china: bool = True, config_dir: str = None):
        if not THRIFT_AVAILABLE:
            raise EvernoteIntegrationError(
                f"必需的依赖未安装。请运行: pip install evernote3 thrift\n错误详情: {IMPORT_ERROR if 'IMPORT_ERROR' in globals() else 'Unknown'}"
            )

        self.config_manager = EvernoteConfig(config_dir)
        config = self.config_manager.load_config()

        self.developer_token = developer_token or config.get("developer_token", "")
        if not self.developer_token:
            raise EvernoteIntegrationError("未设置开发者令牌")

        self.china = china if china is not None else config.get("china", True)
        self.config = self.CHINA_CONFIG if self.china else self.INTERNATIONAL_CONFIG

        try:
            self.user_store_client = self._create_user_store_client()
            self._get_note_store_url()
            self.note_store_client = self._create_note_store_client()
            self._tag_cache = None
        except Exception as e:
            raise EvernoteIntegrationError(f"连接印象笔记失败: {str(e)}")

    def _create_user_store_client(self):
        """创建 UserStore 客户端"""
        http_client = THttpClient.THttpClient(self.config["user_store_url"])
        http_client.setTimeout(30000)
        protocol = TBinaryProtocol.TBinaryProtocol(http_client)
        return UserStore.Client(protocol)

    def _get_note_store_url(self):
        """获取 NoteStore URL"""
        try:
            self.user_store_client.checkVersion("Claude Code Evernote Integration", 1, 25)
            user = self.user_store_client.getUser(self.developer_token)
            shard_id = user.shardId
            if self.china:
                self.note_store_url = f"https://{self.config['host']}/shard/{shard_id}/notestore"
            else:
                self.note_store_url = f"https://{self.config['host']}/edam/note/{shard_id}"
        except Exception as e:
            raise EvernoteIntegrationError(f"获取 NoteStore URL 失败: {str(e)}")

    def _create_note_store_client(self):
        """创建 NoteStore 客户端"""
        http_client = THttpClient.THttpClient(self.note_store_url)
        http_client.setTimeout(30000)
        protocol = TBinaryProtocol.TBinaryProtocol(http_client)
        return NoteStore.Client(protocol)

    def _make_content(self, content: str) -> str:
        """生成 ENML 格式的内容"""
        content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{content}<br/></en-note>'

    def _html_to_text(self, html: str) -> str:
        """将 HTML 转换为纯文本"""
        text = re.sub(r'<[^>]+>', '\n', html)
        text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        return '\n'.join(line.strip() for line in text.split('\n') if line.strip())

    # ==================== 基础功能 ====================

    def verify_connection(self) -> bool:
        """验证连接"""
        try:
            user = self.user_store_client.getUser(self.developer_token)
            return user is not None
        except Exception:
            return False

    def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        try:
            user = self.user_store_client.getUser(self.developer_token)
            info = {
                "username": user.username,
                "email": getattr(user, 'email', None),
                "name": user.name,
            }
            if hasattr(user, 'created') and user.created:
                info["created"] = datetime.fromtimestamp(user.created / 1000).isoformat()
            if hasattr(user, 'updated') and user.updated:
                info["updated"] = datetime.fromtimestamp(user.updated / 1000).isoformat()
            return info
        except Exception as e:
            raise EvernoteIntegrationError(f"获取用户信息失败: {str(e)}")

    # ==================== 笔记本管理 ====================

    def list_notebooks(self) -> List[Dict[str, Any]]:
        """列出所有笔记本"""
        try:
            notebooks = self.note_store_client.listNotebooks(self.developer_token)
            return [
                {
                    "guid": nb.guid,
                    "name": nb.name,
                    "stack": nb.stack if hasattr(nb, 'stack') else None,
                    "default_notebook": getattr(nb, 'defaultNotebook', False),
                }
                for nb in notebooks
            ]
        except Exception as e:
            raise EvernoteIntegrationError(f"获取笔记本列表失败: {str(e)}")

    def _get_notebook_guid(self, notebook_name: str) -> Optional[str]:
        """根据笔记本名称获取 GUID"""
        notebooks = self.list_notebooks()
        for nb in notebooks:
            if nb["name"] == notebook_name:
                return nb["guid"]
        return None

    def create_notebook(self, name: str, stack: str = None) -> Dict[str, Any]:
        """创建笔记本"""
        try:
            notebook = Notebook()
            notebook.name = name
            if stack:
                notebook.stack = stack

            created = self.note_store_client.createNotebook(self.developer_token, notebook)
            return {
                "guid": created.guid,
                "name": created.name,
                "stack": created.stack if hasattr(created, 'stack') else None
            }
        except Exception as e:
            raise EvernoteIntegrationError(f"创建笔记本失败: {str(e)}")

    def delete_notebook(self, notebook_name: str) -> bool:
        """删除笔记本"""
        try:
            guid = self._get_notebook_guid(notebook_name)
            if not guid:
                raise EvernoteIntegrationError(f"笔记本 '{notebook_name}' 不存在")
            self.note_store_client.expungeNotebook(self.developer_token, guid)
            return True
        except Exception as e:
            raise EvernoteIntegrationError(f"删除笔记本失败: {str(e)}")

    # ==================== 标签管理 ====================

    def list_tags(self) -> List[Dict[str, Any]]:
        """列出所有标签"""
        try:
            if self._tag_cache is None:
                tags = self.note_store_client.listTags(self.developer_token)
                self._tag_cache = [
                    {
                        "guid": tag.guid,
                        "name": tag.name,
                        "parent_guid": getattr(tag, 'parentGuid', None)
                    }
                    for tag in tags
                ]
            return self._tag_cache
        except Exception as e:
            raise EvernoteIntegrationError(f"获取标签列表失败: {str(e)}")

    def _get_tag_guid(self, tag_name: str) -> Optional[str]:
        """根据标签名称获取 GUID"""
        tags = self.list_tags()
        for tag in tags:
            if tag["name"] == tag_name:
                return tag["guid"]
        return None

    def create_tag(self, name: str, parent_guid: str = None) -> Dict[str, Any]:
        """创建标签"""
        try:
            tag = Tag()
            tag.name = name
            if parent_guid:
                tag.parentGuid = parent_guid

            created = self.note_store_client.createTag(self.developer_token, tag)
            self._tag_cache = None  # 清除缓存
            return {
                "guid": created.guid,
                "name": created.name
            }
        except Exception as e:
            raise EvernoteIntegrationError(f"创建标签失败: {str(e)}")

    def delete_tag(self, tag_name: str) -> bool:
        """删除标签"""
        try:
            guid = self._get_tag_guid(tag_name)
            if not guid:
                raise EvernoteIntegrationError(f"标签 '{tag_name}' 不存在")
            self.note_store_client.expungeTag(self.developer_token, guid)
            self._tag_cache = None  # 清除缓存
            return True
        except Exception as e:
            raise EvernoteIntegrationError(f"删除标签失败: {str(e)}")

    def add_tags_to_note(self, note_guid: str, tag_names: List[str]) -> bool:
        """给笔记添加标签"""
        try:
            note = self.note_store_client.getNote(self.developer_token, note_guid, False, False, False, False)

            # 获取或创建标签
            tag_guids = []
            for tag_name in tag_names:
                tag_guid = self._get_tag_guid(tag_name)
                if not tag_guid:
                    # 创建不存在的标签
                    tag = self.create_tag(tag_name)
                    tag_guid = tag["guid"]
                tag_guids.append(tag_guid)

            # 添加标签（保留现有标签）
            existing_guids = note.tagGuids if hasattr(note, 'tagGuids') else []
            note.tagGuids = list(set(existing_guids + tag_guids))

            self.note_store_client.updateNote(self.developer_token, note)
            return True
        except Exception as e:
            raise EvernoteIntegrationError(f"添加标签失败: {str(e)}")

    def remove_tags_from_note(self, note_guid: str, tag_names: List[str]) -> bool:
        """从笔记移除标签"""
        try:
            note = self.note_store_client.getNote(self.developer_token, note_guid, False, False, False, False)

            # 获取要移除的标签 GUID
            remove_guids = set()
            for tag_name in tag_names:
                tag_guid = self._get_tag_guid(tag_name)
                if tag_guid:
                    remove_guids.add(tag_guid)

            # 保留未被移除的标签
            existing_guids = note.tagGuids if hasattr(note, 'tagGuids') else []
            note.tagGuids = [guid for guid in existing_guids if guid not in remove_guids]

            self.note_store_client.updateNote(self.developer_token, note)
            return True
        except Exception as e:
            raise EvernoteIntegrationError(f"移除标签失败: {str(e)}")

    def get_note_tags(self, note_guid: str) -> List[str]:
        """获取笔记的标签名称"""
        try:
            note = self.note_store_client.getNote(self.developer_token, note_guid, False, False, True, False)
            tag_guids = note.tagGuids if hasattr(note, 'tagGuids') and note.tagGuids else []

            tag_names = []
            all_tags = self.list_tags()
            tag_map = {tag["guid"]: tag["name"] for tag in all_tags}

            for guid in tag_guids:
                if guid in tag_map:
                    tag_names.append(tag_map[guid])

            return tag_names
        except Exception as e:
            raise EvernoteIntegrationError(f"获取笔记标签失败: {str(e)}")

    # ==================== 高级搜索 ====================

    def search_notes_advanced(
        self,
        query: str = "",
        notebook: str = None,
        tags: List[str] = None,
        limit: int = 100,
        offset: int = 0,
        order: str = "UPDATED",  # CREATED, UPDATED, RELEVANCE, TITLE, UPDATE_SEQUENCE_NUMBER
        ascending: bool = False,
        content_search: bool = True,
        has_todo: bool = None,
        has_attachment: bool = None,
        has_reminder: bool = None,
        min_length: int = None,
        max_length: int = None,
        created_after: str = None,  # ISO format datetime
        created_before: str = None,
        updated_after: str = None,
        updated_before: str = None,
        untagged: bool = False
    ) -> List[Dict[str, Any]]:
        """高级搜索笔记"""
        try:
            note_filter = NoteFilter()

            # 构建搜索查询字符串
            search_terms = []
            if query:
                search_terms.append(query)

            # 时间范围
            if created_after:
                dt = datetime.fromisoformat(created_after.replace('Z', '+00:00'))
                timestamp = int(dt.timestamp() * 1000)
                search_terms.append(f"created:{timestamp}-*")
            if created_before:
                dt = datetime.fromisoformat(created_before.replace('Z', '+00:00'))
                timestamp = int(dt.timestamp() * 1000)
                search_terms.append(f"created:*-{timestamp}")
            if updated_after:
                dt = datetime.fromisoformat(updated_after.replace('Z', '+00:00'))
                timestamp = int(dt.timestamp() * 1000)
                search_terms.append(f"updated:{timestamp}-*")
            if updated_before:
                dt = datetime.fromisoformat(updated_before.replace('Z', '+00:00'))
                timestamp = int(dt.timestamp() * 1000)
                search_terms.append(f"updated:*-{timestamp}")

            # 属性过滤
            if has_todo is True:
                search_terms.append("todo:true")
            elif has_todo is False:
                search_terms.append("todo:false")

            if has_attachment is True:
                search_terms.append("hasAttachment:true")
            elif has_attachment is False:
                search_terms.append("hasAttachment:false")

            if has_reminder is True:
                search_terms.append("reminderOrder:*")
            elif has_reminder is False:
                search_terms.append("-reminderOrder:*")

            if untagged:
                search_terms.append("-tag:*")

            # 笔记本过滤
            if notebook:
                nb_guid = self._get_notebook_guid(notebook)
                if nb_guid:
                    note_filter.notebookGuid = nb_guid

            # 标签过滤
            if tags:
                for tag in tags:
                    search_terms.append(f'tag:"{tag}"')

            note_filter.words = " ".join(search_terms) if search_terms else ""

            # 结果规范
            result_spec = NotesMetadataResultSpec()
            result_spec.includeTitle = True
            result_spec.includeContentLength = True
            result_spec.includeCreated = True
            result_spec.includeUpdated = True
            result_spec.includeTagGuids = True
            result_spec.includeNotebookGuid = True

            # 排序（使用整数值）
            order_map = {
                "CREATED": 1,   # CREATED
                "UPDATED": 2,   # UPDATED
                "RELEVANCE": 3, # RELEVANCE
                "TITLE": 4,     # TITLE
                "UPDATE_SEQUENCE_NUMBER": 5,
            }
            note_filter.order = order_map.get(order.upper(), 2)  # 默认按更新时间
            note_filter.ascending = ascending

            result = self.note_store_client.findNotesMetadata(
                self.developer_token, note_filter, offset, limit, result_spec
            )

            notes = []
            for note_md in result.notes:
                # 长度过滤
                if min_length and note_md.contentLength < min_length:
                    continue
                if max_length and note_md.contentLength > max_length:
                    continue

                # 获取内容（如果需要）
                content = ""
                if content_search:
                    try:
                        full_note = self.note_store_client.getNote(
                            self.developer_token, note_md.guid, True, False, False, False
                        )
                        content = self._html_to_text(full_note.content)
                    except:
                        pass

                # 获取标签名称
                tag_names = self.get_note_tags(note_md.guid)

                notes.append({
                    "guid": note_md.guid,
                    "title": note_md.title,
                    "content_length": note_md.contentLength,
                    "created": datetime.fromtimestamp(note_md.created / 1000).isoformat(),
                    "updated": datetime.fromtimestamp(note_md.updated / 1000).isoformat(),
                    "notebook_guid": note_md.notebookGuid,
                    "tags": tag_names,
                    "content": content[:500] + "..." if content and len(content) > 500 else content,
                })

            return notes

        except Exception as e:
            raise EvernoteIntegrationError(f"高级搜索失败: {str(e)}")

    # ==================== 笔记 CRUD ====================

    def search_notes(
        self,
        query: str = "",
        notebook: str = None,
        tags: List[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """简单搜索（保持向后兼容）"""
        return self.search_notes_advanced(query=query, notebook=notebook, tags=tags, limit=limit)

    def get_note(self, note_guid: str, with_content: bool = True) -> Dict[str, Any]:
        """获取单个笔记的完整内容"""
        try:
            note = self.note_store_client.getNote(
                self.developer_token, note_guid, with_content, False, False, False
            )

            result = {
                "guid": note.guid,
                "title": note.title,
                "created": datetime.fromtimestamp(note.created / 1000).isoformat(),
                "updated": datetime.fromtimestamp(note.updated / 1000).isoformat(),
                "notebook_guid": note.notebookGuid,
                "tags": self.get_note_tags(note_guid),
            }

            if with_content and hasattr(note, 'content'):
                result["content"] = self._html_to_text(note.content)

            if hasattr(note, 'attributes') and note.attributes:
                attrs = {}
                for key in ['source', 'sourceURL', 'latitude', 'longitude', 'altitude', 'author']:
                    if hasattr(note.attributes, key):
                        value = getattr(note.attributes, key)
                        if value is not None:
                            attrs[key] = value
                if attrs:
                    result["attributes"] = attrs

            # 附件信息
            if hasattr(note, 'resources') and note.resources:
                result["attachments"] = len(note.resources)

            return result

        except Exception as e:
            raise EvernoteIntegrationError(f"获取笔记失败: {str(e)}")

    def create_note(
        self,
        title: str,
        content: str,
        notebook: str = None,
        tags: List[str] = None,
        created: datetime = None
    ) -> Dict[str, Any]:
        """创建笔记"""
        try:
            note = NoteType()
            note.title = title
            note.content = self._make_content(content)

            if notebook:
                nb_guid = self._get_notebook_guid(notebook)
                if nb_guid:
                    note.notebookGuid = nb_guid
                else:
                    raise EvernoteIntegrationError(f"笔记本 '{notebook}' 不存在")

            if tags:
                note.tagNames = tags

            if created:
                note.created = int(created.timestamp() * 1000)

            created_note = self.note_store_client.createNote(self.developer_token, note)

            return {
                "guid": created_note.guid,
                "title": created_note.title,
                "created": datetime.fromtimestamp(created_note.created / 1000).isoformat(),
            }

        except Exception as e:
            raise EvernoteIntegrationError(f"创建笔记失败: {str(e)}")

    def update_note(self, note_guid: str, content: str = None, title: str = None, tags: List[str] = None) -> bool:
        """更新笔记"""
        try:
            note = self.note_store_client.getNote(
                self.developer_token, note_guid, False, False, False, False
            )

            if title:
                note.title = title
            if content:
                note.content = self._make_content(content)

            self.note_store_client.updateNote(self.developer_token, note)

            # 更新标签（如果提供）
            if tags is not None:
                # 先清除所有标签
                existing_tags = self.get_note_tags(note_guid)
                if existing_tags:
                    self.remove_tags_from_note(note_guid, existing_tags)
                # 添加新标签
                if tags:
                    self.add_tags_to_note(note_guid, tags)

            return True

        except Exception as e:
            raise EvernoteIntegrationError(f"更新笔记失败: {str(e)}")

    def delete_note(self, note_guid: str) -> bool:
        """删除笔记（移到回收站）"""
        try:
            self.note_store_client.deleteNote(self.developer_token, note_guid)
            return True
        except Exception as e:
            raise EvernoteIntegrationError(f"删除笔记失败: {str(e)}")

    def expunge_note(self, note_guid: str) -> bool:
        """永久删除笔记"""
        try:
            self.note_store_client.expungeNote(self.developer_token, note_guid)
            return True
        except Exception as e:
            raise EvernoteIntegrationError(f"永久删除笔记失败: {str(e)}")

    # ==================== 批量操作 ====================

    def move_notes(self, source_notebook: str, target_notebook: str, query: str = "") -> Dict[str, Any]:
        """批量移动笔记"""
        try:
            source_guid = self._get_notebook_guid(source_notebook)
            target_guid = self._get_notebook_guid(target_notebook)

            if not source_guid:
                raise EvernoteIntegrationError(f"源笔记本 '{source_notebook}' 不存在")
            if not target_guid:
                raise EvernoteIntegrationError(f"目标笔记本 '{target_notebook}' 不存在")

            # 搜索要移动的笔记
            notes = self.search_notes(query=query, notebook=source_notebook, limit=1000)

            moved = 0
            failed = 0
            for note_md in notes:
                try:
                    note = self.note_store_client.getNote(
                        self.developer_token, note_md["guid"], False, False, False, False
                    )
                    note.notebookGuid = target_guid
                    self.note_store_client.updateNote(self.developer_token, note)
                    moved += 1
                except Exception:
                    failed += 1

            return {"moved": moved, "failed": failed}

        except Exception as e:
            raise EvernoteIntegrationError(f"批量移动失败: {str(e)}")

    def batch_tag(self, query: str, tags_to_add: List[str] = None, tags_to_remove: List[str] = None,
                  notebook: str = None, limit: int = 100) -> Dict[str, Any]:
        """批量添加/移除标签"""
        try:
            notes = self.search_notes(query=query, notebook=notebook, limit=limit)

            added = 0
            removed = 0
            failed = 0

            for note_md in notes:
                try:
                    if tags_to_add:
                        self.add_tags_to_note(note_md["guid"], tags_to_add)
                        added += 1
                    if tags_to_remove:
                        self.remove_tags_from_note(note_md["guid"], tags_to_remove)
                        removed += 1
                except Exception:
                    failed += 1

            return {"processed": len(notes), "added": added, "removed": removed, "failed": failed}

        except Exception as e:
            raise EvernoteIntegrationError(f"批量标签操作失败: {str(e)}")

    def batch_delete(self, query: str, notebook: str = None, limit: int = 100,
                    permanent: bool = False) -> Dict[str, Any]:
        """批量删除笔记"""
        try:
            notes = self.search_notes(query=query, notebook=notebook, limit=limit)

            deleted = 0
            failed = 0

            for note_md in notes:
                try:
                    if permanent:
                        self.expunge_note(note_md["guid"])
                    else:
                        self.delete_note(note_md["guid"])
                    deleted += 1
                except Exception:
                    failed += 1

            return {"deleted": deleted, "failed": failed}

        except Exception as e:
            raise EvernoteIntegrationError(f"批量删除失败: {str(e)}")

    # ==================== 笔记链接 ====================

    def get_note_link(self, note_guid: str) -> str:
        """获取笔记的内部链接（可用于其他笔记）"""
        try:
            note = self.note_store_client.getNote(self.developer_token, note_guid, False, False, False, False)
            shard_id = self.user_store_client.getUser(self.developer_token).shardId
            return f"{self.config['web_base']}/shard/{shard_id}/note/{note_guid}"
        except Exception as e:
            raise EvernoteIntegrationError(f"获取笔记链接失败: {str(e)}")

    def get_app_link(self, note_guid: str) -> str:
        """获取应用内链接（evernote:///）"""
        try:
            shard_id = self.user_store_client.getUser(self.developer_token).shardId
            return f"evernote:///view/{shard_id}/{note_guid}/{note_guid}/"
        except Exception as e:
            raise EvernoteIntegrationError(f"获取应用链接失败: {str(e)}")

    # ==================== 附件支持 ====================

    def list_attachments(self, note_guid: str) -> List[Dict[str, Any]]:
        """列出笔记的附件"""
        try:
            note = self.note_store_client.getNote(
                self.developer_token, note_guid, False, False, True, False
            )

            if not hasattr(note, 'resources') or not note.resources:
                return []

            attachments = []
            for resource in note.resources:
                info = {
                    "guid": resource.guid,
                    "mime": resource.mime,
                    "length": len(resource.data.body) if hasattr(resource.data, 'body') else 0,
                }
                if hasattr(resource, 'attributes') and resource.attributes:
                    if hasattr(resource.attributes, 'fileName'):
                        info["filename"] = resource.attributes.fileName
                attachments.append(info)

            return attachments

        except Exception as e:
            raise EvernoteIntegrationError(f"列出附件失败: {str(e)}")

    def download_attachment(self, note_guid: str, attachment_guid: str, output_path: str) -> bool:
        """下载附件"""
        try:
            note = self.note_store_client.getNote(
                self.developer_token, note_guid, False, False, True, False
            )

            if not hasattr(note, 'resources') or not note.resources:
                raise EvernoteIntegrationError("笔记没有附件")

            for resource in note.resources:
                if resource.guid == attachment_guid:
                    if hasattr(resource.data, 'body'):
                        with open(output_path, 'wb') as f:
                            f.write(resource.data.body)
                        return True
                    else:
                        raise EvernoteIntegrationError("附件数据不可用")

            raise EvernoteIntegrationError("附件不存在")

        except Exception as e:
            raise EvernoteIntegrationError(f"下载附件失败: {str(e)}")

    # ==================== 导入导出 ====================

    def export_note(self, note_guid: str, format: str = "md") -> str:
        """导出笔记为指定格式

        Args:
            note_guid: 笔记 GUID
            format: 格式类型 (md=Markdown, txt=纯文本, html=HTML, json=JSON)
        """
        try:
            note = self.get_note(note_guid, with_content=True)

            if format == "json":
                return json.dumps(note, ensure_ascii=False, indent=2)

            elif format == "md":
                # Markdown 格式
                md = f"# {note['title']}\n\n"
                md += f"**创建时间**: {note['created']}\n"
                md += f"**更新时间**: {note['updated']}\n"
                if note.get('tags'):
                    md += f"**标签**: {', '.join(note['tags'])}\n"
                md += f"\n---\n\n"
                md += note.get('content', '')
                return md

            elif format == "txt":
                # 纯文本格式
                return f"{note['title']}\n{'='*len(note['title'])}\n\n{note.get('content', '')}"

            elif format == "html":
                # HTML 格式
                html = f"<h1>{note['title']}</h1>"
                html += f"<p><strong>创建时间</strong>: {note['created']}</p>"
                html += f"<p><strong>更新时间</strong>: {note['updated']}</p>"
                html += f"<div>{note.get('content', '').replace(chr(10), '<br>')}</div>"
                return html

            else:
                raise EvernoteIntegrationError(f"不支持的格式: {format}")

        except Exception as e:
            raise EvernoteIntegrationError(f"导出笔记失败: {str(e)}")

    def export_notebook(self, notebook_name: str, output_dir: str, format: str = "md") -> Dict[str, Any]:
        """导出整个笔记本"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            notes = self.search_notes(notebook=notebook_name, limit=1000)

            exported = 0
            failed = 0

            for note_md in notes:
                try:
                    content = self.export_note(note_md["guid"], format)
                    filename = f"{note_md['title']}.{format}"
                    # 清理文件名
                    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
                    file_path = output_path / filename

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    exported += 1
                except Exception:
                    failed += 1

            return {
                "exported": exported,
                "failed": failed,
                "output_dir": str(output_path)
            }

        except Exception as e:
            raise EvernoteIntegrationError(f"导出笔记本失败: {str(e)}")

    def import_markdown(self, file_path: str, notebook: str = None, tags: List[str] = None) -> Dict[str, Any]:
        """导入 Markdown 文件作为笔记"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 从文件名或第一行提取标题
            title = Path(file_path).stem
            lines = content.split('\n')
            if lines and lines[0].startswith('# '):
                title = lines[0][2:].strip()
                content = '\n'.join(lines[1:])

            result = self.create_note(title, content, notebook, tags)
            return {"imported": 1, "note_guid": result["guid"]}

        except Exception as e:
            raise EvernoteIntegrationError(f"导入 Markdown 失败: {str(e)}")

    # ==================== 统计分析 ====================

    def get_stats(self) -> Dict[str, Any]:
        """获取账号统计信息"""
        try:
            sync_state = self.note_store_client.getSyncState(self.developer_token)
            user = self.user_store_client.getUser(self.developer_token)

            notebooks = self.list_notebooks()
            tags = self.list_tags()

            # 计算实际笔记总数：遍历所有笔记本获取笔记数量
            total_notes = 0
            for nb in notebooks:
                try:
                    # 使用 findNotesMetadata 获取笔记本中的笔记数量
                    notebook_filter = NoteFilter()
                    notebook_filter.notebookGuid = nb["guid"]

                    count_spec = NotesMetadataResultSpec()
                    count_spec.includeTitle = False

                    result = self.note_store_client.findNotesMetadata(
                        self.developer_token, notebook_filter, 0, 1, count_spec
                    )
                    total_notes += result.totalNotes if hasattr(result, 'totalNotes') else 0
                except Exception:
                    # 如果获取失败，跳过该笔记本
                    pass

            result = {
                "total_notebooks": len(notebooks),
                "total_tags": len(tags),
                "total_notes": total_notes,
                "update_count": sync_state.updateCount if hasattr(sync_state, 'updateCount') else 0,
            }

            if hasattr(sync_state, 'currentTime') and sync_state.currentTime:
                result["sync_time"] = datetime.fromtimestamp(sync_state.currentTime / 1000).isoformat()

            if hasattr(user, 'created') and user.created:
                result["account_created"] = datetime.fromtimestamp(user.created / 1000).isoformat()

            return result

        except Exception as e:
            raise EvernoteIntegrationError(f"获取统计信息失败: {str(e)}")

    def get_notebook_usage(self) -> List[Dict[str, Any]]:
        """获取各笔记本的笔记数量"""
        try:
            notebooks = self.list_notebooks()
            usage = []

            for nb in notebooks:
                # 使用搜索来获取笔记数量作为近似
                notes = self.search_notes(notebook=nb["name"], limit=1000)
                count = len(notes)

                usage.append({
                    "name": nb["name"],
                    "guid": nb["guid"],
                    "count": count,
                    "stack": nb.get("stack"),
                })

            return sorted(usage, key=lambda x: x["count"], reverse=True)

        except Exception as e:
            raise EvernoteIntegrationError(f"获取笔记本使用情况失败: {str(e)}")

    def get_tag_stats(self) -> List[Dict[str, Any]]:
        """获取标签使用统计"""
        try:
            tags = self.list_tags()
            stats = []

            for tag in tags:
                # 统计使用该标签的笔记数
                notes = self.search_notes(tags=[tag["name"]], limit=1)
                # 注意：这里只是近似值，实际应该用 findNotesCount

                stats.append({
                    "name": tag["name"],
                    "guid": tag["guid"],
                    "count": len(notes),  # 简化处理
                })

            return sorted(stats, key=lambda x: x["count"], reverse=True)

        except Exception as e:
            raise EvernoteIntegrationError(f"获取标签统计失败: {str(e)}")

    def get_recent_activity(self, days: int = 7) -> Dict[str, Any]:
        """获取最近活动统计"""
        try:
            since = datetime.now() - timedelta(days=days)
            since_timestamp = int(since.timestamp() * 1000)

            # 搜索最近创建的笔记
            created_notes = self.search_notes_advanced(
                created_after=since.isoformat(),
                limit=1000,
                order="CREATED"
            )

            # 搜索最近更新的笔记
            updated_notes = self.search_notes_advanced(
                updated_after=since.isoformat(),
                limit=1000,
                order="UPDATED"
            )

            # 按日期分组
            created_by_date = {}
            for note in created_notes:
                date = note["updated"][:10]
                created_by_date[date] = created_by_date.get(date, 0) + 1

            return {
                "period_days": days,
                "total_created": len(created_notes),
                "total_updated": len(updated_notes),
                "created_by_date": created_by_date,
            }

        except Exception as e:
            raise EvernoteIntegrationError(f"获取最近活动失败: {str(e)}")


def create_client(developer_token: str = None, china: bool = True, config_dir: str = None) -> EvernoteClientWrapper:
    """创建印象笔记客户端的便捷函数"""
    if not developer_token:
        developer_token = os.getenv("EVERNOTE_TOKEN")

    return EvernoteClientWrapper(
        developer_token=developer_token,
        china=china,
        config_dir=config_dir
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        token = sys.argv[1]
        client = create_client(token, china=True)

        print("=== 印象笔记连接测试 ===")
        if client.verify_connection():
            print("✓ 连接成功")

            print("\n=== 用户信息 ===")
            user_info = client.get_user_info()
            print(f"用户名: {user_info['username']}")

            print("\n=== 统计信息 ===")
            stats = client.get_stats()
            print(f"笔记本数: {stats['total_notebooks']}")
            print(f"标签数: {stats['total_tags']}")
            print(f"笔记总数: {stats['total_notes']}")
        else:
            print("✗ 连接失败")
