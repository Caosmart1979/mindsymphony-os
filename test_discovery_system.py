#!/usr/bin/env python3
"""技能发现与路由系统测试脚本"""

import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

class SkillDiscoveryTest:
    def __init__(self, skills_path: str = "./skills/skills"):
        self.skills_path = Path(skills_path)
        self.skills = {}
        self.test_results = {'passed': 0, 'failed': 0, 'warnings': 0}
    
    def load_all_interop_configs(self):
        print("Loading INTEROP.yml configurations...")
        for skill_dir in self.skills_path.iterdir():
            if not skill_dir.is_dir():
                continue
            interop_file = skill_dir / "INTEROP.yml"
            if not interop_file.exists():
                continue
            try:
                with open(interop_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    self.skills[skill_dir.name] = config
                    print(f"  Loaded: {skill_dir.name}")
            except Exception as e:
                print(f"  Error loading {skill_dir.name}: {e}")
                self.test_results['failed'] += 1
        print(f"Loaded {len(self.skills)} skill configurations\n")
        return len(self.skills) > 0
    
    def test_routing_patterns(self):
        print("Testing routing patterns...")
        all_valid = True
        for skill_name, config in self.skills.items():
            patterns = config.get('discovery', {}).get('routing_patterns', [])
            if not patterns:
                print(f"  WARNING: {skill_name}: No routing patterns")
                self.test_results['warnings'] += 1
                continue
            for pattern_config in patterns:
                pattern = pattern_config.get('pattern', '')
                confidence = pattern_config.get('confidence', 0)
                try:
                    re.compile(pattern)
                    print(f"  OK {skill_name}: pattern={pattern[:30]}... confidence={confidence}")
                except re.error as e:
                    print(f"  FAIL {skill_name}: Invalid regex: {e}")
                    all_valid = False
                    self.test_results['failed'] += 1
        print()
        return all_valid
    
    def discover_skills(self, user_input: str, top_n: int = 3):
        matches = []
        priority_weights = {'critical': 1.0, 'high': 0.8, 'medium': 0.6, 'low': 0.4}
        for skill_name, config in self.skills.items():
            if not config.get('discovery', {}).get('auto_route', True):
                continue
            patterns = config.get('discovery', {}).get('routing_patterns', [])
            priority = config.get('skill', {}).get('priority', 'medium')
            threshold = config.get('discovery', {}).get('confidence_threshold', 0.7)
            max_pattern_confidence = 0
            for pattern_config in patterns:
                pattern = pattern_config.get('pattern', '')
                confidence = pattern_config.get('confidence', 0.5)
                if re.search(pattern, user_input, re.IGNORECASE):
                    max_pattern_confidence = max(max_pattern_confidence, confidence)
            if max_pattern_confidence > 0:
                priority_weight = priority_weights.get(priority, 0.6)
                final_score = max_pattern_confidence * priority_weight
                if final_score >= threshold:
                    matches.append((skill_name, final_score))
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]
    
    def test_discovery(self, test_queries):
        print("Testing skill discovery with queries...\n")
        for query in test_queries:
            print(f"Query: \"{query}\"")
            matches = self.discover_skills(query)
            if not matches:
                print(f"  No matches found\n")
                self.test_results['warnings'] += 1
                continue
            print(f"  Top matches:")
            for i, (skill_name, score) in enumerate(matches[:3], 1):
                print(f"    {i}. {skill_name}: {score:.3f}")
            if matches[0][1] > 1.0 or matches[0][1] < 0:
                print(f"  FAIL: Invalid score: {matches[0][1]}")
                self.test_results['failed'] += 1
            else:
                self.test_results['passed'] += 1
            print()
    
    def print_summary(self):
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Passed: {self.test_results['passed']}")
        print(f"Warnings: {self.test_results['warnings']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Total: {sum(self.test_results.values())}")
        if self.test_results['failed'] == 0:
            print("\nAll tests passed!")
        else:
            print(f"\n{self.test_results['failed']} test(s) failed")
        print("=" * 60)
    
    def run_all_tests(self):
        print("\n" + "=" * 60)
        print("SKILL DISCOVERY SYSTEM TEST SUITE")
        print("=" * 60 + "\n")
        if not self.load_all_interop_configs():
            print("Failed to load configurations")
            return False
        self.test_routing_patterns()
        test_queries = [
            "Create a React component with bold design",
            "Write documentation for my API",
            "Design a poster for the event",
            "Build an MCP server for GitHub",
            "Refactor this legacy code"
        ]
        self.test_discovery(test_queries)
        self.print_summary()
        return self.test_results['failed'] == 0

if __name__ == "__main__":
    tester = SkillDiscoveryTest()
    success = tester.run_all_tests()
    exit(0 if success else 1)
