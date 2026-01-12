#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Planning with Files - 初始化脚本

自动创建 task_plan.md, findings.md, progress.md 文件
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 设置 Windows 控制台输出编码
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass


def get_timestamp():
    """获取当前时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_template_path(template_name):
    """获取模板文件路径"""
    script_dir = Path(__file__).parent
    return script_dir / "templates" / template_name


def load_template(template_name):
    """加载模板内容"""
    template_path = get_template_path(template_name)
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return None


def fill_template(template_content, **kwargs):
    """填充模板变量"""
    defaults = {
        "TASK_NAME": "任务名称",
        "OBJECTIVE": "任务目标",
        "TIMESTAMP": get_timestamp(),
        "LAST_UPDATE": get_timestamp(),
        "NEXT_STEPS": "待定",
    }
    defaults.update(kwargs)

    for key, value in defaults.items():
        template_content = template_content.replace(f"{{{{{key}}}}}", str(value))

    return template_content


def create_planning_directory(base_path="."):
    """创建 .planning 目录"""
    planning_dir = Path(base_path) / ".planning"
    planning_dir.mkdir(exist_ok=True)
    return planning_dir


def create_task_plan(planning_dir, task_name, objective):
    """创建 task_plan.md"""
    template = load_template("task_plan.md")
    if template is None:
        # 如果模板不存在，使用默认模板
        template = """# {TASK_NAME}

## 目标
{OBJECTIVE}

## 阶段
- [ ] Phase 1: 准备
- [ ] Phase 2: 执行
- [ ] Phase 3: 完成

## 尝试记录
| 尝试 | 方法 | 结果 | 下一步 |
|------|------|------|--------|
| 1 | | | |

## 阻塞问题
- [ ] 无

---
**创建时间:** {TIMESTAMP}
**最后更新:** {LAST_UPDATE}
"""

    content = fill_template(
        template,
        TASK_NAME=task_name,
        OBJECTIVE=objective,
    )

    task_plan_path = planning_dir / "task_plan.md"
    task_plan_path.write_text(content, encoding="utf-8")
    return task_plan_path


def create_findings(planning_dir):
    """创建 findings.md"""
    template = load_template("findings.md")
    if template is None:
        template = """# 研究发现

## 架构洞察

## 关键文件

## 技术栈

## 参考资料

---
**创建时间:** {TIMESTAMP}
**最后更新:** {LAST_UPDATE}
"""

    content = fill_template(template)

    findings_path = planning_dir / "findings.md"
    findings_path.write_text(content, encoding="utf-8")
    return findings_path


def create_progress(planning_dir, objective):
    """创建 progress.md"""
    template = load_template("progress.md")
    if template is None:
        template = """# 会话进度

## 操作历史
| 时间 | 操作 | 文件 | 状态 | 备注 |
|------|------|------|------|------|

## 测试结果
| 测试 | 结果 | 输出 |
|------|------|------|

## 会话摘要

### 会话 1 ({TIMESTAMP})
**目标:** {OBJECTIVE}
**完成:**
- [ ] 任务1
- [ ] 任务2
**下一步:** 待定

---
**会话开始:** {TIMESTAMP}
**最后更新:** {LAST_UPDATE}
"""

    content = fill_template(template, OBJECTIVE=objective)

    progress_path = planning_dir / "progress.md"
    progress_path.write_text(content, encoding="utf-8")
    return progress_path


def init_planning_files(task_name=None, objective=None, base_path="."):
    """
    初始化 planning 文件

    Args:
        task_name: 任务名称 (可选)
        objective: 任务目标 (可选)
        base_path: 基础路径 (默认: 当前目录)
    """
    # 创建目录
    planning_dir = create_planning_directory(base_path)
    print(f"✅ 创建目录: {planning_dir}")

    # 设置默认值
    if task_name is None:
        task_name = input("请输入任务名称: ").strip()
        if not task_name:
            task_name = "新任务"

    if objective is None:
        objective = input("请输入任务目标: ").strip()
        if not objective:
            objective = "待定义"

    # 创建文件
    task_plan_path = create_task_plan(planning_dir, task_name, objective)
    print(f"✅ 创建文件: {task_plan_path}")

    findings_path = create_findings(planning_dir)
    print(f"✅ 创建文件: {findings_path}")

    progress_path = create_progress(planning_dir, objective)
    print(f"✅ 创建文件: {progress_path}")

    print(f"\n🎉 Planning 文件已创建!")
    print(f"📁 位置: {planning_dir}")
    print(f"\n下一步:")
    print(f"  1. 编辑 {task_plan_path} 定义任务阶段")
    print(f"  2. 开始执行任务")
    print(f"  3. 定期更新 findings.md 和 progress.md")

    return planning_dir


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="初始化 Planning with Files 文件"
    )
    parser.add_argument(
        "-t", "--task",
        help="任务名称",
        default=None
    )
    parser.add_argument(
        "-o", "--objective",
        help="任务目标",
        default=None
    )
    parser.add_argument(
        "-p", "--path",
        help="基础路径",
        default="."
    )

    args = parser.parse_args()

    init_planning_files(
        task_name=args.task,
        objective=args.objective,
        base_path=args.path
    )


if __name__ == "__main__":
    main()
