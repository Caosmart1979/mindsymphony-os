#!/usr/bin/env python3
"""
AI API连接测试脚本
支持GLM-4-Flash和Gemini Flash
"""

import os
import sys
import json
import requests
from datetime import datetime

def test_glm_api():
    """测试GLM-4-Flash API"""
    api_key = os.getenv('GLM_API_KEY')
    
    if not api_key:
        print("❌ GLM_API_KEY环境变量未设置")
        return False
    
    print(f"🔑 GLM API Key: {api_key[:10]}...{api_key[-4:]}")
    print("📡 测试GLM-4-Flash API连接...")
    
    try:
        response = requests.post(
            'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'glm-4-flash',
                'messages': [
                    {
                        'role': 'user',
                        'content': '你好！请用一句话介绍你自己。'
                    }
                ],
                'temperature': 0.7
            },
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200:
            content = result['choices'][0]['message']['content']
            print(f"✅ GLM API连接成功！")
            print(f"📝 AI回复: {content}")
            return True
        else:
            print(f"❌ GLM API返回错误: {response.status_code}")
            print(f"📄 错误详情: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        return False


def test_gemini_api():
    """测试Gemini Flash API"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY环境变量未设置")
        return False
    
    print(f"🔑 Gemini API Key: {api_key[:10]}...{api_key[-4:]}")
    print("📡 测试Gemini Flash API连接...")
    
    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}',
            json={
                'contents': [
                    {
                        'parts': [
                            {'text': 'Hello! Please introduce yourself in one sentence.'}
                        ]
                    }
                ]
            },
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200:
            content = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Gemini API连接成功！")
            print(f"📝 AI回复: {content}")
            return True
        else:
            print(f"❌ Gemini API返回错误: {response.status_code}")
            print(f"📄 错误详情: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🤖 AI API 连接测试")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试结果
    results = {}
    
    # 测试GLM API
    print("-" * 60)
    print("📊 测试1: GLM-4-Flash (智谱AI)")
    print("-" * 60)
    results['glm'] = test_glm_api()
    print()
    
    # 测试Gemini API
    print("-" * 60)
    print("📊 测试2: Gemini Flash (Google)")
    print("-" * 60)
    results['gemini'] = test_gemini_api()
    print()
    
    # 总结
    print("=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    print(f"GLM-4-Flash: {'✅ 成功' if results['glm'] else '❌ 失败'}")
    print(f"Gemini Flash: {'✅ 成功' if results['gemini'] else '❌ 失败'}")
    print()
    
    if results['glm'] or results['gemini']:
        print("🎉 至少有一个API可用！你可以开始使用AI Director功能了。")
        return 0
    else:
        print("⚠️  所有API测试失败。请检查:")
        print("   1. API Key是否正确设置")
        print("   2. 网络连接是否正常")
        print("   3. API Key是否有效")
        print(f"\n📚 查看配置指南: cat API_SETUP_GUIDE.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())
