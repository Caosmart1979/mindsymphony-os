#!/usr/bin/env python3
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
import httpx

console = Console()
BASE_URL = "http://localhost:8000"

def print_section(title: str):
    console.print(f"
{'='*60}", style="bold blue")
    console.print(f"  {title}", style="bold yellow")
    console.print(f"{'='*60}
")

def check_health():
    print_section("1️⃣  健康检查")
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            console.print("✅ API服务运行正常！", style="bold green")
            console.print(f"   状态: {data.get('status')}")
            console.print(f"   版本: {data.get('version')}")
            console.print(f"   模型: {data.get('model')}")
            return True
        else:
            console.print(f"❌ API返回错误状态码: {response.status_code}", style="bold red")
            return False
    except Exception as e:
        console.print(f"❌ 无法连接到API服务器", style="bold red")
        console.print(f"   错误: {e}", style="dim red")
        console.print(f"
   💡 请确保API服务器正在运行")
        return False

def list_projects():
    print_section("2️⃣  项目列表")
    try:
        response = httpx.get(f"{BASE_URL}/api/projects", timeout=10.0)
        if response.status_code == 200:
            projects = response.json()
            if not projects:
                console.print("📭 当前没有任何项目", style="yellow")
                return []
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=6)
            table.add_column("项目名称", style="cyan")
            table.add_column("描述", style="green")
            table.add_column("状态", style="yellow")
            table.add_column("创建时间", style="dim")
            for idx, project in enumerate(projects, 1):
                status_emoji = "🟢" if project.get('status') == 'active' else "⚪"
                table.add_row(str(idx), project.get('name', '-'), project.get('description', '-'), f"{status_emoji} {project.get('status', 'unknown')}", project.get('created_at', '-')[:10])
            console.print(table)
            return projects
        else:
            console.print(f"❌ 获取项目列表失败: {response.status_code}", style="bold red")
            return []
    except Exception as e:
        console.print(f"❌ 请求失败: {e}", style="bold red")
        return []

def main():
    console.print("""[bold blue]
╔══════════════════════════════════════════════════════════╗
║          🎬 Director AI API - 功能演示 🎬               ║
║              项目管理与AI协作平台                         ║
╚══════════════════════════════════════════════════════════╝
[/bold blue]
""")
    if not check_health():
        console.print("
❌ 演示终止：API服务未运行", style="bold red")
        return
    projects = list_projects()
    console.print("
[bold green]🎉 演示完成！[/bold green]
")

if __name__ == "__main__":
    main()
