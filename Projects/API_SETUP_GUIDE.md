# AI API 配置指南

## 📋 概述

本项目支持两个免费的AI服务提供商：
- **GLM-4-Flash** (智谱AI) - 推荐 ⭐
- **Gemini Flash** (Google)

## 🚀 快速开始

### 方案一：GLM-4-Flash (推荐)

**优势：**
- ✅ 免费258万tokens/天
- ✅ 响应速度快
- ✅ 中文支持优秀
- ✅ 适合生产环境

**注册步骤：**

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 进入 [API Keys页面](https://open.bigmodel.cn/usercenter/apikeys)
4. 创建新的API Key
5. 复制API Key

**配置方式：**

```bash
# 方式1: 环境变量（推荐）
export GLM_API_KEY="your_api_key_here"

# 方式2: .env文件
echo "GLM_API_KEY=your_api_key_here" > .env
```

**API测试：**

```bash
python -c "
import requests
response = requests.post(
    'https://open.bigmodel.cn/api/paas/v4/chat/completions',
    headers={'Authorization': 'Bearer YOUR_API_KEY'},
    json={'model': 'glm-4-flash', 'messages': [{'role': 'user', 'content': '你好'}]}
)
print(response.json())
"
```

### 方案二：Gemini Flash

**优势：**
- ✅ Google出品
- ✅ 免费15次/分钟
- ✅ 多语言支持好

**注册步骤：**

1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 使用Google账号登录
3. 创建新项目或选择现有项目
4. 生成API Key
5. 复制API Key

**配置方式：**

```bash
# 方式1: 环境变量（推荐）
export GEMINI_API_KEY="your_api_key_here"

# 方式2: .env文件
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**API测试：**

```bash
python -c "
import requests
response = requests.post(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=YOUR_API_KEY',
    json={'contents': [{'parts': [{'text': 'Hello'}]}]}
)
print(response.json())
"
```

## 🔧 Python代码示例

### GLM-4-Flash 客户端

```python
import requests
import os

class GLMClient:
    def __init__(self):
        self.api_key = os.getenv('GLM_API_KEY')
        self.base_url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
    
    def generate(self, prompt, temperature=0.7):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'glm-4-flash',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': temperature
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        return response.json()

# 使用示例
client = GLMClient()
result = client.generate('写一个关于咖啡的短视频脚本')
print(result['choices'][0]['message']['content'])
```

### Gemini Flash 客户端

```python
import requests
import os

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent'
    
    def generate(self, prompt, temperature=0.7):
        url = f'{self.base_url}?key={self.api_key}'
        data = {
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'temperature': temperature}
        }
        response = requests.post(url, json=data)
        return response.json()

# 使用示例
client = GeminiClient()
result = client.generate('写一个关于咖啡的短视频脚本')
print(result['candidates'][0]['content']['parts'][0]['text'])
```

## 📊 费用对比

| 服务商 | 免费额度 | 速度 | 中文支持 | 推荐度 |
|--------|----------|------|----------|--------|
| GLM-4-Flash | 258万tokens/天 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Gemini Flash | 15次/分钟 | ⚡⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🛡️ 安全建议

1. **不要将API Key提交到Git仓库**
   ```bash
   # 添加到.gitignore
   echo ".env" >> .gitignore
   ```

2. **使用环境变量**（推荐）
   ```bash
   # Linux/Mac
   export GLM_API_KEY="your_key"
   
   # Windows (PowerShell)
   $env:GLM_API_KEY="your_key"
   ```

3. **定期轮换API Key**
   - 每月更换一次API Key
   - 如有泄露，立即重新生成

## 🔍 故障排查

### 问题1: API Key无效

**错误信息：** `Invalid API Key`

**解决方案：**
- 检查API Key是否正确复制（不要有多余空格）
- 确认API Key未过期
- 重新生成API Key

### 问题2: 超出配额

**错误信息：** `Quota exceeded`

**解决方案：**
- GLM: 等待第二天重置（每天258万tokens）
- Gemini: 等待1分钟后重试（每分钟15次）

### 问题3: 网络连接失败

**错误信息：** `Connection timeout`

**解决方案：**
- 检查网络连接
- 尝试使用VPN
- 检查防火墙设置

## 📚 相关链接

- [智谱AI官方文档](https://open.bigmodel.cn/dev/api)
- [Google AI官方文档](https://ai.google.dev/gemini-api/docs)
- [本项目GitHub](https://github.com/your-repo)

## 💡 最佳实践

1. **优先使用GLM-4-Flash**：免费额度更大，适合开发测试
2. **添加重试机制**：网络不稳定时自动重试
3. **缓存结果**：避免重复调用相同请求
4. **监控用量**：定期检查API使用量

## 🎯 下一步

配置完成后，你可以：
1. 运行测试脚本验证配置
2. 开始使用AI Director功能
3. 生成你的第一个AI视频脚本

---

如有问题，请查看 [Issues](https://github.com/your-repo/issues) 或联系技术支持。
