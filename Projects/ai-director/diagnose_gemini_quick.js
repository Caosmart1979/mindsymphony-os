const https = require('https');
const fs = require('fs');

// 读取 .env 文件
let apiKey = '';
try {
  const envContent = fs.readFileSync('.env', 'utf8');
  const match = envContent.match(/GEMINI_API_KEY=(.+)/);
  if (match) apiKey = match[1].trim();
} catch(e) {
  console.log('无法读取 .env 文件');
}

console.log('=== Gemini API 详细诊断 ===\n');
console.log('API Key 配置:', apiKey ? '✅ 已配置' : '❌ 未配置');
console.log('API Key 长度:', apiKey ? apiKey.length : 0);
console.log('API Key 格式:', apiKey?.startsWith('AIza') ? '✅ 正确' : '⚠️ 可能不正确');
console.log('API Key:', apiKey ? apiKey.substring(0, 15) + '...' : 'N/A');

if (!apiKey) {
  console.log('\n❌ 未找到 API Key，请检查 .env 文件');
  process.exit(1);
}

// 测试连接
const testData = JSON.stringify({
  contents: [{ parts: [{ text: 'Hello' }] }]
});

console.log('\n正在测试连接到 generativelanguage.googleapis.com...');
const startTime = Date.now();

const req = https.request({
  hostname: 'generativelanguage.googleapis.com',
  path: '/v1beta/models/gemini-pro:generateContent?key=' + apiKey,
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
}, (res) => {
  const elapsed = Date.now() - startTime;
  console.log('响应时间:', elapsed + 'ms');
  console.log('HTTP 状态码:', res.statusCode);
  
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200) {
      console.log('\n✅ API 连接成功！');
      try {
        const response = JSON.parse(data);
        const text = response.candidates?.[0]?.content?.parts?.[0]?.text;
        console.log('响应内容:', text?.substring(0, 100));
      } catch(e) {
        console.log('响应:', data.substring(0, 200));
      }
    } else {
      console.log('\n❌ API 返回错误');
      try {
        const error = JSON.parse(data);
        console.log('\n错误详情:');
        console.log(JSON.stringify(error, null, 2));
        
        if (error.error?.message) {
          console.log('\n💡 错误分析:', error.error.message);
          if (error.error.message.includes('API key')) {
            console.log('   建议: API Key 可能无效或过期');
          }
        }
      } catch(e) {
        console.log('响应:', data);
      }
    }
  });
});

req.on('error', (error) => {
  const elapsed = Date.now() - startTime;
  console.log('连接时间:', elapsed + 'ms');
  console.log('\n❌ 网络错误:', error.message);
  console.log('错误代码:', error.code);
  
  console.log('\n💡 可能的原因:');
  if (error.code === 'ETIMEDOUT') {
    console.log('   - 网络连接超时');
    console.log('   - 可能需要配置代理');
    console.log('   - 防火墙可能阻止了访问');
  } else if (error.code === 'ECONNREFUSED') {
    console.log('   - 连接被拒绝');
    console.log('   - 网络可能无法访问 Google 服务');
  } else {
    console.log('   - 网络连接问题');
    console.log('   - DNS 解析失败');
  }
  
  console.log('\n🔧 解决方案:');
  console.log('   1. 检查网络连接');
  console.log('   2. 配置代理服务器');
  console.log('   3. 或暂时使用智谱 GLM API（已正常工作）');
});

req.on('timeout', () => {
  req.destroy();
  console.log('\n❌ 请求超时');
  console.log('💡 网络可能无法访问 Google API，建议配置代理');
});

req.setTimeout(10000);
req.write(testData);
req.end();
