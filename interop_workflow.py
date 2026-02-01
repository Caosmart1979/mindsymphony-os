#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import re

try:
    import yaml
except ImportError:
    print('Installing PyYAML...')
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyyaml'])
    import yaml

class InteropWorkflow:
    def __init__(self, skills_base: Path = Path('./skills/skills')):
        self.skills_base = skills_base
        self.skills: Dict[str, dict] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_skill(self, skill_path: Path) -> bool:
        interop_file = skill_path / 'INTEROP.yml'
        if not interop_file.exists():
            return False
        try:
            with open(interop_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.skills[skill_path.name] = config
                return True
        except Exception as e:
            self.errors.append(f'Failed to load: {e}')
            return False

    def load_all_skills(self) -> int:
        count = 0
        for skill_dir in self.skills_base.iterdir():
            if skill_dir.is_dir() and (skill_dir / 'skill.md').exists():
                if self.load_skill(skill_dir):
                    count += 1
        return count

    def validate_structure(self, skill_name: str, config: dict) -> bool:
        required_fields = ['skill', 'metadata', 'discovery']
        valid = True
        for field in required_fields:
            if field not in config:
                self.errors.append(f'{skill_name}: Missing {field}')
                valid = False
        if 'skill' in config:
            for field in ['name', 'version', 'category', 'priority']:
                if field not in config['skill']:
                    self.errors.append(f'{skill_name}: Missing skill.{field}')
                    valid = False
        return valid

    def validate_patterns(self, skill_name: str, config: dict) -> bool:
        valid = True
        if 'discovery' not in config:
            return True
        discovery = config['discovery']
        if 'routing_patterns' not in discovery:
            self.warnings.append(f'{skill_name}: No patterns')
            return True
        for i, pc in enumerate(discovery['routing_patterns']):
            if 'pattern' not in pc:
                self.errors.append(f'{skill_name}: Missing pattern')
                valid = False
                continue
            try:
                re.compile(pc['pattern'])
            except re.error as e:
                self.errors.append(f'{skill_name}: Bad regex: {e}')
                valid = False
            if 'confidence' in pc:
                if not 0 <= pc['confidence'] <= 1:
                    self.errors.append(f'{skill_name}: Bad confidence')
                    valid = False
        return valid

    def validate_skill(self, skill_name: str) -> bool:
        if skill_name not in self.skills:
            return False
        config = self.skills[skill_name]
        valid = self.validate_structure(skill_name, config)
        valid &= self.validate_patterns(skill_name, config)
        return valid

    def validate_all_skills(self) -> Tuple[int, int, int]:
        passed = failed = 0
        for skill_name in self.skills:
            if self.validate_skill(skill_name):
                passed += 1
            else:
                failed += 1
        return passed, len(self.warnings), failed

    def test_discovery(self, query: str, top_n: int = 5):
        results = []
        for skill_name, config in self.skills.items():
            score = self._calculate_score(query, config)
            if score > 0:
                results.append((skill_name, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]

    def _calculate_score(self, query: str, config: dict) -> float:
        if 'discovery' not in config:
            return 0.0
        discovery = config['discovery']
        if not discovery.get('auto_route', False):
            return 0.0
        patterns = discovery.get('routing_patterns', [])
        max_score = 0.0
        for pc in patterns:
            pattern = pc.get('pattern', '')
            confidence = pc.get('confidence', 0.5)
            try:
                if re.search(pattern, query, re.IGNORECASE):
                    priority = config.get('skill', {}).get('priority', 'medium')
                    weight = {'critical': 1.0, 'high': 0.8, 'medium': 0.6, 'low': 0.4}
                    score = confidence * weight.get(priority, 0.6)
                    max_score = max(max_score, score)
            except re.error:
                pass
        return max_score

def main():
    parser = argparse.ArgumentParser(description='Skill Interop Workflow Manager')
    parser.add_argument('--skills-base', type=Path, default=Path('./skills/skills'))
    parser.add_argument('--skill', type=str, help='Specific skill name')
    parser.add_argument('--action', type=str, required=True,
                        choices=['validate', 'test', 'report', 'discover'])
    parser.add_argument('--query', type=str, help='Query for discover')
    parser.add_argument('--top-n', type=int, default=5)
    args = parser.parse_args()

    workflow = InteropWorkflow(args.skills_base)

    if args.skill:
        skill_path = args.skills_base / args.skill
        if not workflow.load_skill(skill_path):
            print(f'Cannot load skill: {args.skill}')
            sys.exit(1)
    else:
        count = workflow.load_all_skills()
        print(f'Loaded {count} skills')

    if args.action == 'validate':
        passed, warnings, failed = workflow.validate_all_skills()
        print(f'\n[OK] Passed: {passed}')
        print(f'[WARN]  Warnings: {warnings}')
        print(f'[FAIL] Failed: {failed}')
        if failed == 0:
            print('\n[SUCCESS] All tests passed!')
        else:
            print('\n[ERROR] Errors found:')
            for error in workflow.errors[:10]:
                print(f'   - {error}')
            if len(workflow.errors) > 10:
                print(f'   ... and {len(workflow.errors) - 10} more')
            sys.exit(1)

    elif args.action == 'test':
        passed, warnings, failed = workflow.validate_all_skills()
        test_queries = [
            'Create a React component',
            'Design a logo',
            'Write API documentation',
            'Build a database schema',
        ]
        print('\n[SEARCH] Testing skill discovery:')
        for query in test_queries:
            results = workflow.test_discovery(query, top_n=3)
            print(f'\nQuery: "{query}"')
            if results:
                for skill, score in results:
                    print(f'  - {skill}: {score:.3f}')
            else:
                print('  (no matches)')

    elif args.action == 'report':
        print('\n' + '=' * 60)
        print('SKILL INTEROPERABILITY REPORT')
        print('=' * 60)
        print(f'\n[STATS] Total: {len(workflow.skills)} skills')
        if workflow.errors:
            print(f'\n[ERROR] Errors ({len(workflow.errors)}):')
            for error in workflow.errors[:5]:
                print(f'   - {error}')
        if workflow.warnings:
            print(f'\n[WARN]  Warnings ({len(workflow.warnings)}):')
            for warning in workflow.warnings[:5]:
                print(f'   - {warning}')
        print('\n[LIST] Configured skills:')
        for skill_name in sorted(workflow.skills.keys()):
            config = workflow.skills[skill_name]
            cat = config.get('skill', {}).get('category', 'unknown')
            pri = config.get('skill', {}).get('priority', 'unknown')
            print(f'   - {skill_name} ({cat}, {pri})')
        print()

    elif args.action == 'discover':
        if not args.query:
            print('[ERROR] Please provide --query parameter')
            sys.exit(1)
        results = workflow.test_discovery(args.query, top_n=args.top_n)
        print(f'\n[SEARCH] Query: "{args.query}"\n')
        if results:
            for skill, score in results:
                status = '[OK]' if score >= 0.7 else '[WARN] '
                print(f'{status} {skill}: {score:.3f}')
        else:
            print('No matching skills found')

if __name__ == '__main__':
    main()
