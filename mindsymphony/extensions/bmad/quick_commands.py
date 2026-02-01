"""
快捷指令系统
提供 /ms-xxx 格式的快捷命令，快速启动BMAD工作流
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Any
from enum import Enum


class CommandType(Enum):
    """命令类型"""
    WORKFLOW = "workflow"
    PARTY = "party"
    HELP = "help"
    STATUS = "status"
    CANCEL = "cancel"


@dataclass
class ParsedCommand:
    """解析后的命令"""
    raw_input: str
    command: str
    command_type: CommandType
    args: List[str]
    flags: Dict[str, str]
    description: str
    should_execute: bool
    execution_params: Dict[str, Any]


class QuickCommandParser:
    """
    快捷指令解析器

    支持的命令:
    - /ms-quick [描述] [--complexity=N] - 快速流程
    - /ms-deep [描述] [--plan-only] - 深度规划
    - /ms-party [描述] [--roles=r1,r2] - Party模式
    - /ms-help [主题] - 自适应帮助
    - /ms-status - 系统状态
    - /ms-cancel [execution_id] - 取消工作流

    兼容BMAD命令:
    - /fix, /patch -> /ms-quick
    - /plan, /arch -> /ms-deep
    - /collab -> /ms-party
    """

    # 命令定义
    COMMANDS = {
        # BMAD MindSymphony 命令
        "/ms-quick": {
            "type": CommandType.WORKFLOW,
            "workflow": "quick",
            "aliases": ["/fix", "/patch", "/docs", "/tweak"],
            "description": "快速流程 - 适合bug修复、小功能、文档更新",
            "flags": {
                "--complexity": "强制指定复杂度 (1-10)",
                "--skip-check": "跳过复杂度检查",
                "--skill": "指定使用哪个技能"
            }
        },
        "/ms-deep": {
            "type": CommandType.WORKFLOW,
            "workflow": "full",
            "aliases": ["/plan", "/arch", "/design", "/implement"],
            "description": "深度规划 - 适合产品功能、架构设计、复杂重构",
            "flags": {
                "--plan-only": "只生成计划，不执行",
                "--estimates": "包含工作量估算",
                "--risks": "包含风险分析"
            }
        },
        "/ms-party": {
            "type": CommandType.PARTY,
            "workflow": "party",
            "aliases": ["/collab", "/discuss", "/brainstorm"],
            "description": "启动多Agent协作会话",
            "flags": {
                "--roles": "指定参与角色 (comma-separated)",
                "--duration": "限制会话时长(分钟)",
                "--focus": "聚焦特定领域"
            }
        },
        "/ms-help": {
            "type": CommandType.HELP,
            "aliases": ["/help", "/?"],
            "description": "自适应帮助系统",
            "flags": {
                "--verbose": "详细输出",
                "--examples": "包含示例"
            }
        },
        "/ms-status": {
            "type": CommandType.STATUS,
            "aliases": ["/status"],
            "description": "查看当前系统状态",
            "flags": {}
        },
        "/ms-cancel": {
            "type": CommandType.CANCEL,
            "aliases": ["/cancel", "/stop"],
            "description": "取消正在运行的工作流",
            "flags": {
                "--all": "取消所有工作流"
            }
        }
    }

    def __init__(self):
        """初始化命令解析器"""
        self._build_alias_map()
        self._compile_patterns()

    def _build_alias_map(self):
        """构建别名映射"""
        self.alias_map = {}
        for cmd, config in self.COMMANDS.items():
            self.alias_map[cmd] = cmd
            for alias in config.get("aliases", []):
                self.alias_map[alias] = cmd

    def _compile_patterns(self):
        """编译正则表达式"""
        # 命令格式: /cmd [args...] [--flag=value]
        self.command_pattern = re.compile(
            r'^(/[\w-]+)'           # 命令名
            r'(?:\s+(.+?))?'        # 描述 (可选)
            r'(?:\s+--(\w+)(?:=(\S+))?)*'  # 标志 (可选)
            r'$',
            re.IGNORECASE
        )

    def parse(self, user_input: str) -> ParsedCommand:
        """
        解析用户输入

        Args:
            user_input: 用户输入的文本

        Returns:
            ParsedCommand: 解析结果
        """
        user_input = user_input.strip()

        # 检查是否是命令
        if not user_input.startswith('/'):
            return self._create_non_command(user_input)

        # 解析命令结构
        parts = user_input.split()
        cmd_token = parts[0].lower()

        # 检查是否是别名，转换为标准命令
        canonical_cmd = self.alias_map.get(cmd_token)
        if not canonical_cmd:
            return self._create_unknown_command(user_input, cmd_token)

        # 获取命令配置
        cmd_config = self.COMMANDS[canonical_cmd]

        # 解析参数和标志
        args, flags = self._parse_args_flags(parts[1:])

        # 构建执行参数
        execution_params = self._build_execution_params(
            canonical_cmd, cmd_config, args, flags
        )

        return ParsedCommand(
            raw_input=user_input,
            command=canonical_cmd,
            command_type=cmd_config["type"],
            args=args,
            flags=flags,
            description=cmd_config["description"],
            should_execute=True,
            execution_params=execution_params
        )

    def _parse_args_flags(self, parts: List[str]) -> tuple[List[str], Dict[str, str]]:
        """解析参数和标志"""
        args = []
        flags = {}

        i = 0
        while i < len(parts):
            part = parts[i]

            if part.startswith('--'):
                # 处理标志
                flag_parts = part[2:].split('=', 1)
                flag_name = flag_parts[0]
                flag_value = flag_parts[1] if len(flag_parts) > 1 else "true"
                flags[flag_name] = flag_value
            elif part.startswith('-') and len(part) > 1:
                # 处理短标志 (如 -v)
                flags[part[1:]] = "true"
            else:
                # 普通参数
                args.append(part)

            i += 1

        return args, flags

    def _build_execution_params(
        self,
        cmd: str,
        config: Dict,
        args: List[str],
        flags: Dict[str, str]
    ) -> Dict[str, Any]:
        """构建执行参数"""
        params = {
            "command": cmd,
            "type": config["type"].value,
        }

        # 根据命令类型构建参数
        if config["type"] == CommandType.WORKFLOW:
            params["workflow"] = config["workflow"]
            params["description"] = ' '.join(args) if args else ""
            params["force_path"] = config["workflow"] if "--skip-check" in flags else None

        elif config["type"] == CommandType.PARTY:
            params["workflow"] = "party"
            params["description"] = ' '.join(args) if args else ""
            params["roles"] = flags.get("roles", "architect,developer").split(',')
            params["duration_limit"] = int(flags.get("duration", 30))

        elif config["type"] == CommandType.HELP:
            params["topic"] = args[0] if args else None
            params["verbose"] = "verbose" in flags
            params["examples"] = "examples" in flags

        elif config["type"] == CommandType.STATUS:
            params["include_metrics"] = True

        elif config["type"] == CommandType.CANCEL:
            params["execution_id"] = args[0] if args else None
            params["cancel_all"] = "all" in flags

        return params

    def _create_non_command(self, user_input: str) -> ParsedCommand:
        """创建非命令解析结果"""
        return ParsedCommand(
            raw_input=user_input,
            command="",
            command_type=CommandType.WORKFLOW,  # 默认走工作流
            args=[user_input],
            flags={},
            description="自然语言输入，使用自动路由",
            should_execute=True,
            execution_params={
                "auto_route": True,
                "description": user_input
            }
        )

    def _create_unknown_command(self, user_input: str, cmd_token: str) -> ParsedCommand:
        """创建未知命令解析结果"""
        return ParsedCommand(
            raw_input=user_input,
            command=cmd_token,
            command_type=CommandType.HELP,
            args=[],
            flags={},
            description=f"未知命令: {cmd_token}",
            should_execute=False,
            execution_params={
                "error": f"未知命令: {cmd_token}",
                "suggestion": "使用 /ms-help 查看可用命令"
            }
        )

    def get_help_text(self, topic: Optional[str] = None) -> str:
        """
        获取帮助文本

        Args:
            topic: 可选的主题

        Returns:
            帮助文本
        """
        if topic:
            # 查找特定主题的帮助
            for cmd, config in self.COMMANDS.items():
                if topic.lower() in [cmd.lower()] + [a.lower() for a in config.get("aliases", [])]:
                    return self._format_command_help(cmd, config)

            return f"未找到主题 '{topic}' 的帮助信息。"

        # 返回总体帮助
        return self._format_general_help()

    def _format_command_help(self, cmd: str, config: Dict) -> str:
        """格式化单个命令的帮助"""
        help_text = f"""
## {cmd}

{config['description']}

**类型**: {config['type'].value}

**别名**: {', '.join(config.get('aliases', []))}

**可用选项**:
"""
        for flag, desc in config.get("flags", {}).items():
            help_text += f"\n- `{flag}`: {desc}"

        return help_text

    def _format_general_help(self) -> str:
        """格式化总体帮助"""
        help_text = """
# MindSymphony + BMAD 快捷指令

## 工作流命令

| 命令 | 别名 | 描述 |
|------|------|------|
"""
        for cmd, config in self.COMMANDS.items():
            if config["type"] == CommandType.WORKFLOW:
                aliases = ', '.join(config.get('aliases', [])[:2])
                help_text += f"| `{cmd}` | {aliases} | {config['description'][:40]}... |\n"

        help_text += """
## 协作命令

| 命令 | 别名 | 描述 |
|------|------|------|
"""
        for cmd, config in self.COMMANDS.items():
            if config["type"] in [CommandType.PARTY]:
                aliases = ', '.join(config.get('aliases', [])[:2])
                help_text += f"| `{cmd}` | {aliases} | {config['description'][:40]}... |\n"

        help_text += """
## 系统命令

| 命令 | 描述 |
|------|------|
"""
        for cmd, config in self.COMMANDS.items():
            if config["type"] in [CommandType.HELP, CommandType.STATUS, CommandType.CANCEL]:
                help_text += f"| `{cmd}` | {config['description'][:40]}... |\n"

        help_text += """
## 使用示例

```
/ms-quick 修复登录bug --skill=debug
/ms-deep 设计新的用户系统 --plan-only
/ms-party 重构核心模块 --roles=architect,developer,tester
/ms-help party
```

## 自动路由

如果不使用命令前缀，系统将自动评估复杂度并选择合适的工作流。
"""
        return help_text

    def is_command(self, user_input: str) -> bool:
        """检查输入是否是命令"""
        return user_input.strip().startswith('/')

    def get_suggestion(self, partial: str) -> List[str]:
        """
        获取命令建议

        Args:
            partial: 部分输入

        Returns:
            建议列表
        """
        partial = partial.lower()
        suggestions = []

        for cmd in self.COMMANDS.keys():
            if cmd.startswith(partial):
                suggestions.append(cmd)

        for alias, canonical in self.alias_map.items():
            if alias.startswith(partial) and alias not in suggestions:
                suggestions.append(f"{alias} -> {canonical}")

        return suggestions[:5]


# 便捷函数
def parse_command(user_input: str) -> ParsedCommand:
    """便捷函数：解析命令"""
    parser = QuickCommandParser()
    return parser.parse(user_input)


def get_help(topic: Optional[str] = None) -> str:
    """便捷函数：获取帮助"""
    parser = QuickCommandParser()
    return parser.get_help_text(topic)
