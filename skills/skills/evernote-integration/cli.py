#!/usr/bin/env python3
"""
印象笔记 CLI 工具 - 完整版
提供命令行接口，支持所有高级功能
"""

import argparse
import sys
import os
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from evernote_client import (
    create_client,
    EvernoteIntegrationError,
    EvernoteConfig,
    THRIFT_AVAILABLE
)


def cmd_search(args):
    """搜索笔记"""
    try:
        client = create_client(china=args.china)
        notes = client.search_notes_advanced(
            query=args.query or "",
            notebook=args.notebook,
            tags=args.tags.split(",") if args.tags else None,
            limit=args.limit,
            order=args.order or "UPDATED",
            ascending=args.ascending if hasattr(args, 'ascending') else False,
            min_length=args.min_length,
            max_length=args.max_length,
            created_after=args.created_after,
            created_before=args.created_before,
            updated_after=args.updated_after,
            updated_before=args.updated_before,
            untagged=args.untagged if hasattr(args, 'untagged') else False,
        )

        if args.json:
            print(json.dumps(notes, ensure_ascii=False, indent=2))
        else:
            print(f"找到 {len(notes)} 条笔记：\n")
            for i, note in enumerate(notes, 1):
                tags_str = f" [{', '.join(note['tags'])}]" if note.get('tags') else ""
                print(f"{i}. {note['title']}{tags_str}")
                print(f"   更新时间: {note['updated']}")
                print(f"   内容: {note['content'][:150]}...")
                print()

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_get(args):
    """获取单个笔记"""
    try:
        client = create_client(china=args.china)
        note = client.get_note(args.guid)

        if args.json:
            print(json.dumps(note, ensure_ascii=False, indent=2))
        elif args.format == "md":
            content = client.export_note(args.guid, "md")
            print(content)
        elif args.format == "html":
            content = client.export_note(args.guid, "html")
            print(content)
        else:
            print(f"标题: {note['title']}")
            print(f"创建时间: {note['created']}")
            print(f"更新时间: {note['updated']}")
            if note.get('tags'):
                print(f"标签: {', '.join(note['tags'])}")
            print(f"\n内容:\n{'-' * 60}")
            print(note['content'])

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """列出笔记本"""
    try:
        client = create_client(china=args.china)
        notebooks = client.list_notebooks()

        if args.json:
            print(json.dumps(notebooks, ensure_ascii=False, indent=2))
        else:
            print(f"共有 {len(notebooks)} 个笔记本：\n")
            for i, nb in enumerate(notebooks, 1):
                stack = f" [栈: {nb['stack']}]" if nb.get('stack') else ""
                default = " [默认]" if nb.get('default_notebook') else ""
                print(f"{i}. {nb['name']}{stack}{default}")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_create(args):
    """创建笔记"""
    try:
        client = create_client(china=args.china)

        # 从文件或标准输入读取内容
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        elif args.content:
            content = args.content
        else:
            print("请提供内容 (-c) 或文件 (-f)", file=sys.stderr)
            sys.exit(1)

        tags = args.tags.split(",") if args.tags else None
        result = client.create_note(
            title=args.title,
            content=content,
            notebook=args.notebook,
            tags=tags
        )

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✓ 笔记创建成功!")
            print(f"  标题: {result['title']}")
            print(f"  GUID: {result['guid']}")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_config(args):
    """配置认证信息"""
    config_manager = EvernoteConfig()

    if args.token:
        config = config_manager.load_config()
        config['developer_token'] = args.token
        config['china'] = not getattr(args, 'international', False)
        config_manager.save_config(config)
        print("✓ 配置已保存")
    else:
        print("请提供开发者令牌 (-t)")
        sys.exit(1)


def cmd_verify(args):
    """验证连接"""
    try:
        client = create_client(china=args.china)

        if client.verify_connection():
            print("✓ 连接成功")

            user_info = client.get_user_info()
            print(f"\n用户信息:")
            print(f"  用户名: {user_info['username']}")
            print(f"  邮箱: {user_info.get('email', 'N/A')}")

            notebooks = client.list_notebooks()
            print(f"\n笔记本数量: {len(notebooks)}")
        else:
            print("✗ 连接失败")
            sys.exit(1)

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


# ==================== 新增命令 ====================

def cmd_tags(args):
    """标签管理"""
    try:
        client = create_client(china=args.china)

        if args.action == "list":
            tags = client.list_tags()
            if args.json:
                print(json.dumps(tags, ensure_ascii=False, indent=2))
            else:
                print(f"共有 {len(tags)} 个标签：\n")
                for i, tag in enumerate(tags, 1):
                    print(f"{i}. {tag['name']}")

        elif args.action == "create":
            result = client.create_tag(args.name)
            print(f"✓ 标签创建成功: {result['name']}")

        elif args.action == "delete":
            client.delete_tag(args.name)
            print(f"✓ 标签已删除: {args.name}")

        elif args.action == "add":
            client.add_tags_to_note(args.guid, args.tags.split(","))
            print(f"✓ 标签已添加到笔记")

        elif args.action == "remove":
            client.remove_tags_from_note(args.guid, args.tags.split(","))
            print(f"✓ 标签已从笔记移除")

        elif args.action == "stats":
            stats = client.get_tag_stats()
            if args.json:
                print(json.dumps(stats, ensure_ascii=False, indent=2))
            else:
                print("标签使用统计：\n")
                for i, stat in enumerate(stats[:20], 1):  # 只显示前20个
                    print(f"{i}. {stat['name']}: {stat['count']} 条笔记")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_notebook(args):
    """笔记本管理"""
    try:
        client = create_client(china=args.china)

        if args.action == "create":
            result = client.create_notebook(args.name, args.stack)
            print(f"✓ 笔记本创建成功: {result['name']}")

        elif args.action == "delete":
            client.delete_notebook(args.name)
            print(f"✓ 笔记本已删除: {args.name}")

        elif args.action == "usage":
            usage = client.get_notebook_usage()
            if args.json:
                print(json.dumps(usage, ensure_ascii=False, indent=2))
            else:
                print("笔记本使用统计：\n")
                for i, nb in enumerate(usage, 1):
                    stack = f" ({nb['stack']})" if nb.get('stack') else ""
                    print(f"{i}. {nb['name']}{stack}: {nb['count']} 条笔记")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_batch(args):
    """批量操作"""
    try:
        client = create_client(china=args.china)

        if args.action == "move":
            result = client.move_notes(args.source, args.target, args.query or "")
            print(f"✓ 移动完成: {result['moved']} 个成功, {result['failed']} 个失败")

        elif args.action == "tag":
            add_tags = args.add.split(",") if args.add else None
            remove_tags = args.remove.split(",") if args.remove else None
            result = client.batch_tag(
                query=args.query or "",
                tags_to_add=add_tags,
                tags_to_remove=remove_tags,
                notebook=args.notebook,
                limit=args.limit
            )
            print(f"✓ 标签操作完成: {result['processed']} 个笔记处理")
            print(f"  添加: {result['added']} 个")
            print(f"  移除: {result['removed']} 个")
            print(f"  失败: {result['failed']} 个")

        elif args.action == "delete":
            result = client.batch_delete(
                query=args.query or "",
                notebook=args.notebook,
                limit=args.limit,
                permanent=args.permanent
            )
            print(f"✓ 删除完成: {result['deleted']} 个成功, {result['failed']} 个失败")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_export(args):
    """导出功能"""
    try:
        client = create_client(china=args.china)

        if args.type == "note":
            content = client.export_note(args.guid, args.format)
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ 笔记已导出到: {args.output}")
            else:
                print(content)

        elif args.type == "notebook":
            result = client.export_notebook(args.name, args.output, args.format)
            print(f"✓ 笔记本导出完成:")
            print(f"  导出: {result['exported']} 个")
            print(f"  失败: {result['failed']} 个")
            print(f"  输出目录: {result['output_dir']}")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_import_cmd(args):
    """导入功能"""
    try:
        client = create_client(china=args.china)
        tags = args.tags.split(",") if args.tags else None
        result = client.import_markdown(args.file, args.notebook, tags)
        print(f"✓ 导入成功!")
        print(f"  笔记 GUID: {result['note_guid']}")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_stats(args):
    """统计分析"""
    try:
        client = create_client(china=args.china)

        if args.action == "overview":
            stats = client.get_stats()
            if args.json:
                print(json.dumps(stats, ensure_ascii=False, indent=2))
            else:
                print("=== 印象笔记统计 ===\n")
                print(f"笔记本数量: {stats['total_notebooks']}")
                print(f"标签数量: {stats['total_tags']}")
                print(f"笔记总数: {stats['total_notes']}")
                if stats.get('sync_time'):
                    print(f"最后同步: {stats['sync_time']}")

        elif args.action == "activity":
            result = client.get_recent_activity(days=args.days)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"=== 最近 {result['period_days']} 天活动 ===\n")
                print(f"创建笔记: {result['total_created']} 条")
                print(f"更新笔记: {result['total_updated']} 条")
                if result.get('created_by_date'):
                    print("\n按日期统计:")
                    for date, count in sorted(result['created_by_date'].items()):
                        print(f"  {date}: {count} 条")

        elif args.action == "usage":
            usage = client.get_notebook_usage()
            if args.json:
                print(json.dumps(usage, ensure_ascii=False, indent=2))
            else:
                print("=== 笔记本使用情况 ===\n")
                for i, nb in enumerate(usage, 1):
                    stack = f" ({nb['stack']})" if nb.get('stack') else ""
                    print(f"{i}. {nb['name']}{stack}: {nb['count']} 条笔记")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_link(args):
    """获取笔记链接"""
    try:
        client = create_client(china=args.china)

        if args.type == "web":
            link = client.get_note_link(args.guid)
            print(f"Web 链接: {link}")
        elif args.type == "app":
            link = client.get_app_link(args.guid)
            print(f"应用链接: {link}")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_attachments(args):
    """附件管理"""
    try:
        client = create_client(china=args.china)

        if args.action == "list":
            attachments = client.list_attachments(args.guid)
            if args.json:
                print(json.dumps(attachments, ensure_ascii=False, indent=2))
            else:
                if not attachments:
                    print("此笔记没有附件")
                else:
                    print(f"共有 {len(attachments)} 个附件：\n")
                    for i, att in enumerate(attachments, 1):
                        filename = att.get('filename', '未命名')
                        print(f"{i}. {filename}")
                        print(f"   类型: {att['mime']}")
                        print(f"   大小: {att['length']} 字节")

        elif args.action == "download":
            if args.output:
                client.download_attachment(args.note_guid, args.attachment_guid, args.output)
                print(f"✓ 附件已下载到: {args.output}")
            else:
                print("请指定输出文件 (-o)")

    except EvernoteIntegrationError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="印象笔记 CLI 工具 - 完整版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础操作
  python cli.py search "AI"
  python cli.py list
  python cli.py create -t "标题" -c "内容"

  # 标签管理
  python cli.py tags list
  python cli.py tags create "新标签"
  python cli.py tags add <GUID> --tags "标签1,标签2"

  # 高级搜索
  python cli.py search "AI" --order CREATED --ascending
  python cli.py search --untagged --min-length 1000
  python cli.py search --created-after "2024-01-01"

  # 批量操作
  python cli.py batch move --source "笔记本A" --target "笔记本B"
  python cli.py batch tag --query "AI" --add "精选"

  # 导出导入
  python cli.py export note <GUID> --format md -o note.md
  python cli.py export notebook "AI知识库" --output ./backup/
  python cli.py import note.md --notebook "学习"

  # 统计分析
  python cli.py stats overview
  python cli.py stats activity --days 30
  python cli.py stats usage

获取开发者令牌:
  中国区: https://app.yinxiang.com/api/DeveloperToken.action
  国际区: https://www.evernote.com/api/DeveloperToken.action
        """
    )

    parser.add_argument("--china", action="store_true", default=True, help="使用中国区（默认）")
    parser.add_argument("--international", action="store_false", dest="china", help="使用国际区")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 搜索命令（增强版）
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("query", nargs="?", help="搜索关键词")
    search_parser.add_argument("-n", "--notebook", help="笔记本名称")
    search_parser.add_argument("-t", "--tags", help="标签（逗号分隔）")
    search_parser.add_argument("-l", "--limit", type=int, default=100, help="返回数量限制")
    search_parser.add_argument("--order", choices=["CREATED", "UPDATED", "RELEVANCE", "TITLE"], help="排序方式")
    search_parser.add_argument("--ascending", action="store_true", help="升序排列")
    search_parser.add_argument("--min-length", type=int, help="最小内容长度")
    search_parser.add_argument("--max-length", type=int, help="最大内容长度")
    search_parser.add_argument("--created-after", help="创建时间起点 (ISO格式)")
    search_parser.add_argument("--created-before", help="创建时间终点 (ISO格式)")
    search_parser.add_argument("--updated-after", help="更新时间起点 (ISO格式)")
    search_parser.add_argument("--updated-before", help="更新时间终点 (ISO格式)")
    search_parser.add_argument("--untagged", action="store_true", help="只显示无标签笔记")

    # 获取笔记命令（增强版）
    get_parser = subparsers.add_parser("get", help="获取笔记详情")
    get_parser.add_argument("guid", help="笔记 GUID")
    get_parser.add_argument("--format", choices=["md", "html", "json"], default="text", help="输出格式")

    # 笔记本管理
    subparsers.add_parser("list", help="列出笔记本")

    # 创建笔记命令
    create_parser = subparsers.add_parser("create", help="创建笔记")
    create_parser.add_argument("-t", "--title", required=True, help="笔记标题")
    create_parser.add_argument("-c", "--content", help="笔记内容")
    create_parser.add_argument("-f", "--file", help="从文件读取内容")
    create_parser.add_argument("-n", "--notebook", help="笔记本名称")
    create_parser.add_argument("--tags", help="标签（逗号分隔）")

    # 配置命令
    config_parser = subparsers.add_parser("config", help="配置认证信息")
    config_parser.add_argument("-t", "--token", help="开发者令牌")

    # 验证命令
    subparsers.add_parser("verify", help="验证连接")

    # 标签管理
    tags_parser = subparsers.add_parser("tags", help="标签管理")
    tags_parser.add_argument("action", choices=["list", "create", "delete", "add", "remove", "stats"], help="操作类型")
    tags_parser.add_argument("--name", help="标签名称（create/delete）")
    tags_parser.add_argument("--guid", help="笔记 GUID（add/remove）")
    tags_parser.add_argument("--tags", help="标签列表（逗号分隔）")
    tags_parser.set_defaults(func=cmd_tags)

    # 笔记本管理
    nb_parser = subparsers.add_parser("notebook", help="笔记本管理")
    nb_parser.add_argument("action", choices=["create", "delete", "usage"], help="操作类型")
    nb_parser.add_argument("--name", help="笔记本名称")
    nb_parser.add_argument("--stack", help="笔记本栈")
    nb_parser.set_defaults(func=cmd_notebook)

    # 批量操作
    batch_parser = subparsers.add_parser("batch", help="批量操作")
    batch_parser.add_argument("action", choices=["move", "tag", "delete"], help="操作类型")
    batch_parser.add_argument("--query", help="搜索查询")
    batch_parser.add_argument("--notebook", help="笔记本名称")
    batch_parser.add_argument("--source", help="源笔记本（move）")
    batch_parser.add_argument("--target", help="目标笔记本（move）")
    batch_parser.add_argument("--add", help="要添加的标签（逗号分隔）")
    batch_parser.add_argument("--remove", help="要移除的标签（逗号分隔）")
    batch_parser.add_argument("-l", "--limit", type=int, default=100, help="操作数量限制")
    batch_parser.add_argument("--permanent", action="store_true", help="永久删除")
    batch_parser.set_defaults(func=cmd_batch)

    # 导出功能
    export_parser = subparsers.add_parser("export", help="导出功能")
    export_parser.add_argument("type", choices=["note", "notebook"], help="导出类型")
    export_parser.add_argument("--guid", help="笔记 GUID（note）")
    export_parser.add_argument("--name", help="笔记本名称（notebook）")
    export_parser.add_argument("--format", choices=["md", "txt", "html", "json"], default="md", help="导出格式")
    export_parser.add_argument("--output", help="输出文件/目录")
    export_parser.set_defaults(func=cmd_export)

    # 导入功能
    import_parser = subparsers.add_parser("import", help="导入功能")
    import_parser.add_argument("file", help="要导入的文件")
    import_parser.add_argument("--notebook", help="目标笔记本")
    import_parser.add_argument("--tags", help="标签（逗号分隔）")
    import_parser.set_defaults(func=cmd_import_cmd)

    # 统计分析
    stats_parser = subparsers.add_parser("stats", help="统计分析")
    stats_parser.add_argument("action", choices=["overview", "activity", "usage"], nargs="?", default="overview", help="统计类型")
    stats_parser.add_argument("--days", type=int, default=7, help="统计天数（activity）")
    stats_parser.set_defaults(func=cmd_stats)

    # 笔记链接
    link_parser = subparsers.add_parser("link", help="获取笔记链接")
    link_parser.add_argument("guid", help="笔记 GUID")
    link_parser.add_argument("--type", choices=["web", "app"], default="web", help="链接类型")
    link_parser.set_defaults(func=cmd_link)

    # 附件管理
    att_parser = subparsers.add_parser("attachments", help="附件管理")
    att_parser.add_argument("action", choices=["list", "download"], help="操作类型")
    att_parser.add_argument("--guid", help="笔记 GUID")
    att_parser.add_argument("--note-guid", help="笔记 GUID（download）")
    att_parser.add_argument("--attachment-guid", help="附件 GUID（download）")
    att_parser.add_argument("-o", "--output", help="输出文件路径（download）")
    att_parser.set_defaults(func=cmd_attachments)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行对应命令
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # 兼容旧版本命令
        commands = {
            "search": cmd_search,
            "get": cmd_get,
            "list": cmd_list,
            "create": cmd_create,
            "config": cmd_config,
            "verify": cmd_verify,
        }
        command_func = commands.get(args.command)
        if command_func:
            command_func(args)
        else:
            parser.print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
