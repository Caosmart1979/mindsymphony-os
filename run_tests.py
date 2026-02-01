#!/usr/bin/env python3
"""
AI Agent Testing Framework - Test Runner

Main entry point for running all tests in the framework.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode == 0


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(
        description="AI Agent Testing Framework - Test Runner"
    )
    parser.add_argument(
        "test_type",
        nargs="?",
        default="all",
        choices=["all", "unit", "integration", "e2e", "performance"],
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-k", "--keyword",
        help="Filter tests by keyword"
    )
    parser.add_argument(
        "--cov",
        action="store_true",
        help="Run with coverage"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate HTML report"
    )

    args = parser.parse_args()

    # Build pytest command
    pytest_cmd = ["python", "-m", "pytest"]

    # Add test type filter
    if args.test_type != "all":
        pytest_cmd.append(f"tests/{args.test_type}/")
    else:
        pytest_cmd.append("tests/")

    # Add options
    if args.verbose:
        pytest_cmd.append("-vv")
    else:
        pytest_cmd.append("-v")

    if args.keyword:
        pytest_cmd.extend(["-k", args.keyword])

    if args.cov:
        pytest_cmd.extend([
            "--cov=skills/skill_discovery",
            "--cov-report=html",
            "--cov-report=term"
        ])

    if args.report:
        pytest_cmd.extend([
            "--html=tests/reports/test_report.html",
            "--self-contained-html"
        ])

    # Run tests
    success = run_command(pytest_cmd, f"{args.test_type.capitalize()} Tests")

    if success:
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("❌ Some tests failed!")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
