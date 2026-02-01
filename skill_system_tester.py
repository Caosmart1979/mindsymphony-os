#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindSymphony 技能系统整合测试与优化脚本
"""

import os
import sys
import subprocess
import datetime
import json
from typing import Dict, List, Any


class SkillSystemTester:
    """技能系统整合测试器"""

    def __init__(self):
        """初始化测试器"""
        self.test_results = []
        self.tools = [
            {
                "name": "技能自动评估系统",
                "command": ["python", "skill_assessor.py", "--output", "test_assessment_report.md"],
                "description": "评估技能质量和完整性"
            },
            {
                "name": "技能去重与合并工具",
                "command": ["python", "skill_deduplicator.py", "--plan"],
                "description": "检测和合并重复或相似的技能"
            },
            {
                "name": "新技能引入管理工具",
                "command": ["python", "skill_introducer.py", "--validate"],
                "description": "验证现有技能配置"
            },
            {
                "name": "技能推荐引擎",
                "command": ["python", "skill_recommender.py", "--query", "数据分析", "--num", "3"],
                "description": "测试技能推荐功能"
            },
            {
                "name": "技能使用指南生成工具",
                "command": ["python", "skill_guide_generator.py", "--index-only"],
                "description": "生成技能使用指南索引"
            },
            {
                "name": "技能持续优化机制",
                "command": ["python", "skill_optimizer.py", "--run", "--report", "test_optimization_report.md"],
                "description": "运行技能优化任务"
            }
        ]

    def run_test(self, tool_name: str, command: List[str], description: str) -> Dict:
        """运行单个工具测试"""
        result = {
            "tool": tool_name,
            "description": description,
            "start_time": datetime.datetime.now().isoformat(),
            "success": False,
            "output": "",
            "error": "",
            "execution_time": 0
        }

        print(f"正在测试: {tool_name}")
        print(f"描述: {description}")

        try:
            # 运行命令
            start_time = datetime.datetime.now()
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60
            )
            end_time = datetime.datetime.now()

            result["output"] = process.stdout
            result["error"] = process.stderr
            result["execution_time"] = (end_time - start_time).total_seconds()

            if process.returncode == 0:
                result["success"] = True
                print(f"✅ 测试成功")
            else:
                print(f"❌ 测试失败 (返回码: {process.returncode})")

        except subprocess.TimeoutExpired:
            result["error"] = "测试超时"
            print(f"⏱️ 测试超时")

        except Exception as e:
            result["error"] = str(e)
            print(f"❌ 测试失败: {e}")

        print(f"执行时间: {result['execution_time']:.2f}秒")
        print()

        return result

    def run_all_tests(self) -> List[Dict]:
        """运行所有工具测试"""
        print("=" * 60)
        print("MindSymphony 技能系统整合测试")
        print("=" * 60)
        print(f"测试开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        self.test_results = []

        for tool in self.tools:
            result = self.run_test(tool["name"], tool["command"], tool["description"])
            self.test_results.append(result)

        print("=" * 60)
        print(f"测试完成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()

        return self.test_results

    def generate_test_report(self, output_file: str = "skill_system_test_report.md") -> str:
        """生成测试报告"""
        report = []

        report.append("# MindSymphony 技能系统整合测试报告")
        report.append("")
        report.append(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # 统计信息
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - successful_tests
        total_execution_time = sum(result["execution_time"] for result in self.test_results)

        report.append("## 测试统计")
        report.append("")
        report.append(f"- **总测试数**: {total_tests}")
        report.append(f"- **成功测试**: {successful_tests}")
        report.append(f"- **失败测试**: {failed_tests}")
        report.append(f"- **成功率**: {successful_tests / total_tests * 100:.1f}%")
        report.append(f"- **总执行时间**: {total_execution_time:.2f}秒")
        report.append("")

        # 测试详情
        report.append("## 测试详情")
        report.append("")
        report.append("| 工具名称 | 描述 | 执行时间 | 状态 |")
        report.append("|----------|------|----------|------|")

        for result in self.test_results:
            status = "✅ 成功" if result["success"] else "❌ 失败"
            report.append(f"| {result['tool']} | {result['description']} | {result['execution_time']:.2f}秒 | {status} |")

        report.append("")

        # 失败测试详情
        if failed_tests > 0:
            report.append("## 失败测试详情")
            report.append("")

            for result in self.test_results:
                if not result["success"]:
                    report.append(f"### {result['tool']}")
                    report.append("")
                    report.append(f"**错误信息**: {result['error']}")
                    report.append("")

                    if result["output"]:
                        report.append("**输出**:")
                        report.append("")
                        report.append("```")
                        report.append(result["output"])
                        report.append("```")
                        report.append("")

        # 优化建议
        report.append("## 优化建议")
        report.append("")

        if failed_tests > 0:
            report.append("- **修复失败的工具**: 优先修复失败的测试项目")

        # 检查执行时间过长的测试
        slow_tests = [result for result in self.test_results if result["execution_time"] > 30]
        if slow_tests:
            report.append("- **优化性能**: 有测试项目执行时间过长，建议优化")

        # 检查是否有未使用的技能
        if os.path.exists("skill_optimization_report.md"):
            report.append("- **分析技能使用**: 查看技能优化报告，了解未使用和低质量技能")

        report.append("- **定期测试**: 建议定期运行整合测试，确保系统健康")
        report.append("- **监控性能**: 关注工具的执行时间和资源使用情况")

        report_text = "\n".join(report)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_text)

        print(f"测试报告已保存到: {output_file}")
        return output_file

    def clean_up_test_files(self):
        """清理测试文件"""
        test_files = [
            "test_assessment_report.md",
            "test_optimization_report.md",
            "skill_guides/index.md"
        ]

        for file_path in test_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"已删除测试文件: {file_path}")
                except Exception as e:
                    print(f"无法删除文件 {file_path}: {e}")

        # 删除临时生成的技能指南目录
        if os.path.exists("skill_guides"):
            try:
                import shutil
                shutil.rmtree("skill_guides")
                print("已删除技能指南目录")
            except Exception as e:
                print(f"无法删除技能指南目录: {e}")


def main():
    """主函数"""
    tester = SkillSystemTester()

    try:
        # 运行所有测试
        results = tester.run_all_tests()

        # 生成测试报告
        report_file = tester.generate_test_report()

        # 显示测试结果摘要
        print("测试结果摘要:")
        print(f"总测试数: {len(results)}")
        print(f"成功: {sum(1 for r in results if r['success'])}")
        print(f"失败: {sum(1 for r in results if not r['success'])}")
        print(f"报告已保存到: {report_file}")

    except KeyboardInterrupt:
        print("测试被用户中断")

    except Exception as e:
        print(f"测试过程中发生错误: {e}")

    finally:
        # 清理测试文件
        tester.clean_up_test_files()


if __name__ == "__main__":
    main()