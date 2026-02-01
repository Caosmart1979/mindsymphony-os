#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能持续优化机制
定期评估技能质量，提供优化建议，支持定时任务
"""

import os
import sys
import time
import schedule
import argparse
from datetime import datetime
from skill_assessor import SkillAssessor
from skill_deduplicator import SkillDeduplicator
from skill_guide_generator import SkillUsageGuideGenerator
from skill_recommender import SkillRecommendationEngine

def run_daily_optimization():
    """
    每日优化任务
    """
    print(f"=== 开始每日技能优化任务 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")

    try:
        # 运行技能评估
        assessor = SkillAssessor()
        results = assessor.assess_all_skills()
        assessment_report = f"daily_assessment_{datetime.now().strftime('%Y%m%d')}.md"
        assessor.generate_report(results, assessment_report)
        print(f"✅ 技能评估完成: {assessment_report}")

        # 运行技能去重
        deduplicator = SkillDeduplicator()
        deduplication_report = f"daily_deduplication_{datetime.now().strftime('%Y%m%d')}.md"
        deduplicator.generate_report(deduplicator.find_similar_skills(), deduplication_report)
        print(f"✅ 技能去重完成: {deduplication_report}")

        # 生成技能使用指南
        guide_generator = SkillUsageGuideGenerator()
        guide_dir = f"skill_guides_{datetime.now().strftime('%Y%m%d')}"
        guide_generator.generate_index(output_dir=guide_dir)
        print(f"✅ 技能使用指南生成完成: {guide_dir}")

        print(f"=== 每日技能优化任务完成 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    except Exception as e:
        print(f"❌ 每日技能优化任务失败: {e}")

def run_weekly_optimization():
    """
    每周优化任务
    """
    print(f"=== 开始每周技能优化任务 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")

    try:
        # 运行技能评估
        assessor = SkillAssessor()
        results = assessor.assess_all_skills()
        assessment_report = f"weekly_assessment_{datetime.now().strftime('%Y%m%d')}.md"
        assessor.generate_report(results, assessment_report)
        print(f"✅ 技能评估完成: {assessment_report}")

        # 运行技能去重
        deduplicator = SkillDeduplicator()
        deduplication_report = f"weekly_deduplication_{datetime.now().strftime('%Y%m%d')}.md"
        deduplicator.generate_report(deduplicator.find_similar_skills(), deduplication_report)
        print(f"✅ 技能去重完成: {deduplication_report}")

        # 生成技能使用指南
        guide_generator = SkillUsageGuideGenerator()
        guide_dir = f"skill_guides_{datetime.now().strftime('%Y%m%d')}"
        guide_generator.generate_index(output_dir=guide_dir)
        print(f"✅ 技能使用指南生成完成: {guide_dir}")

        # 运行技能推荐
        recommender = SkillRecommendationEngine()
        recommendations = recommender.recommend_skills("机器学习", num_recommendations=5)
        recommendation_report = f"weekly_recommendation_{datetime.now().strftime('%Y%m%d')}.md"
        report = recommender.generate_recommendation_report("机器学习", recommendations)
        with open(recommendation_report, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 技能推荐完成: {recommendation_report}")

        print(f"=== 每周技能优化任务完成 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    except Exception as e:
        print(f"❌ 每周技能优化任务失败: {e}")

def run_monthly_optimization():
    """
    每月优化任务
    """
    print(f"=== 开始每月技能优化任务 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")

    try:
        # 运行技能评估
        assessor = SkillAssessor()
        results = assessor.assess_all_skills()
        assessment_report = f"monthly_assessment_{datetime.now().strftime('%Y%m')}.md"
        assessor.generate_report(results, assessment_report)
        print(f"✅ 技能评估完成: {assessment_report}")

        # 运行技能去重
        deduplicator = SkillDeduplicator()
        deduplication_report = f"monthly_deduplication_{datetime.now().strftime('%Y%m')}.md"
        deduplicator.generate_report(deduplicator.find_similar_skills(), deduplication_report)
        print(f"✅ 技能去重完成: {deduplication_report}")

        # 生成技能使用指南
        guide_generator = SkillUsageGuideGenerator()
        guide_dir = f"skill_guides_{datetime.now().strftime('%Y%m')}"
        guide_generator.generate_index(output_dir=guide_dir)
        print(f"✅ 技能使用指南生成完成: {guide_dir}")

        # 运行技能推荐
        recommender = SkillRecommendationEngine()
        recommendations = recommender.recommend_skills("数据分析", num_recommendations=5)
        recommendation_report = f"monthly_recommendation_{datetime.now().strftime('%Y%m')}.md"
        report = recommender.generate_recommendation_report("数据分析", recommendations)
        with open(recommendation_report, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 技能推荐完成: {recommendation_report}")

        print(f"=== 每月技能优化任务完成 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    except Exception as e:
        print(f"❌ 每月技能优化任务失败: {e}")

def run_immediate_optimization():
    """
    立即运行优化任务
    """
    print(f"=== 开始立即技能优化任务 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")

    try:
        # 运行技能评估
        assessor = SkillAssessor()
        results = assessor.assess_all_skills()
        assessment_report = f"immediate_assessment_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        assessor.generate_report(results, assessment_report)
        print(f"✅ 技能评估完成: {assessment_report}")

        # 运行技能去重
        deduplicator = SkillDeduplicator()
        deduplication_report = f"immediate_deduplication_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        deduplicator.generate_report(deduplicator.find_similar_skills(), deduplication_report)
        print(f"✅ 技能去重完成: {deduplication_report}")

        # 生成技能使用指南
        guide_generator = SkillUsageGuideGenerator()
        guide_dir = f"skill_guides_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        guide_generator.generate_index(output_dir=guide_dir)
        print(f"✅ 技能使用指南生成完成: {guide_dir}")

        print(f"=== 立即技能优化任务完成 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    except Exception as e:
        print(f"❌ 立即技能优化任务失败: {e}")

def start_scheduled_optimization():
    """
    启动定时优化任务
    """
    print("=== 启动技能持续优化机制 ===")

    # 每日优化任务（每天凌晨2点）
    schedule.every().day.at("02:00").do(run_daily_optimization)

    # 每周优化任务（每周日凌晨3点）
    schedule.every().sunday.at("03:00").do(run_weekly_optimization)

    # 每月优化任务（每月1日凌晨4点）
    schedule.every().month.at("04:00").do(run_monthly_optimization)

    print("定时优化任务已启动:")
    print("- 每日优化: 每天凌晨2点")
    print("- 每周优化: 每周日凌晨3点")
    print("- 每月优化: 每月1日凌晨4点")
    print("\n按 Ctrl+C 停止定时任务")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n定时优化任务已停止")

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="技能持续优化机制")
    parser.add_argument("--run", action="store_true", help="立即运行优化任务")
    parser.add_argument("--schedule", action="store_true", help="启动定时优化任务")
    parser.add_argument("--config", type=str, help="使用自定义配置文件")
    args = parser.parse_args()

    if args.run:
        run_immediate_optimization()
    elif args.schedule:
        start_scheduled_optimization()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()