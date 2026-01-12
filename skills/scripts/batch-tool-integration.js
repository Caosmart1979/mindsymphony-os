#!/usr/bin/env node

/**
 * skill-creator-meta v2.0 - Batch Tool Integration Script
 *
 * 此脚本演示如何使用批量工具操作来优化技能开发工作流
 * This script demonstrates how to use batch tool operations to optimize skill development workflow
 *
 * 功能 (Features):
 * - 批量读取模板文件 (Batch read template files)
 * - 批量验证技能配置 (Batch validate skill configurations)
 * - 批量生成技能文档 (Batch generate skill documentation)
 */

const fs = require('fs').promises;
const path = require('path');

/**
 * 批量文件操作工具类
 * Batch file operations utility class
 */
class BatchFileOperations {
  /**
   * 批量读取文件
   * Batch read files
   * @param {string[]} filePaths - 文件路径数组 (Array of file paths)
   * @returns {Promise<Map<string, string>>} 文件内容映射 (File content mapping)
   */
  static async batchRead(filePaths) {
    const results = new Map();
    const tasks = filePaths.map(async (filePath) => {
      try {
        const content = await fs.readFile(filePath, 'utf-8');
        results.set(filePath, content);
        return { success: true, filePath };
      } catch (error) {
        results.set(filePath, null);
        return { success: false, filePath, error: error.message };
      }
    });

    await Promise.all(tasks);
    return results;
  }

  /**
   * 批量写入文件
   * Batch write files
   * @param {Map<string, string>} fileContents - 文件路径到内容的映射
   * @returns {Promise<Array>} 操作结果数组 (Operation result array)
   */
  static async batchWrite(fileContents) {
    const results = [];
    const tasks = Array.from(fileContents.entries()).map(async ([filePath, content]) => {
      try {
        await fs.mkdir(path.dirname(filePath), { recursive: true });
        await fs.writeFile(filePath, content, 'utf-8');
        return { success: true, filePath };
      } catch (error) {
        return { success: false, filePath, error: error.message };
      }
    });

    return Promise.all(tasks);
  }

  /**
   * 批量验证文件存在性
   * Batch verify file existence
   * @param {string[]} filePaths - 文件路径数组
   * @returns {Promise<Map<string, boolean>>} 文件存在性映射
   */
  static async batchExists(filePaths) {
    const results = new Map();
    const tasks = filePaths.map(async (filePath) => {
      try {
        await fs.access(filePath);
        results.set(filePath, true);
      } catch {
        results.set(filePath, false);
      }
    });

    await Promise.all(tasks);
    return results;
  }
}

/**
 * 技能配置验证器
 * Skill configuration validator
 */
class SkillConfigValidator {
  /**
   * 批量验证技能配置
   * Batch validate skill configurations
   * @param {Map<string, string>} configs - 配置文件内容映射
   * @returns {Promise<Array>} 验证结果数组
   */
  static async batchValidate(configs) {
    const results = [];

    for (const [filePath, config] of configs.entries()) {
      if (!config) {
        results.push({
          valid: false,
          file: filePath,
          errors: ['配置文件为空 / Configuration file is empty']
        });
        continue;
      }

      const errors = [];

      try {
        const parsed = JSON.parse(config);

        // 验证必需字段 / Validate required fields
        if (!parsed.name) errors.push('缺少必需字段: name / Missing required field: name');
        if (!parsed.version) errors.push('缺少必需字段: version / Missing required field: version');
        if (!parsed.description) errors.push('缺少必需字段: description / Missing required field: description');

        // 验证互操作标准 / Validate interoperability standards
        if (parsed.metadata) {
          if (!parsed.metadata.apiVersion) {
            errors.push('缺少 metadata.apiVersion / Missing metadata.apiVersion');
          }
          if (!parsed.metadata.compatibility) {
            errors.push('缺少 metadata.compatibility / Missing metadata.compatibility');
          }
        }

        results.push({
          valid: errors.length === 0,
          file: filePath,
          errors,
          config: parsed
        });
      } catch (error) {
        results.push({
          valid: false,
          file: filePath,
          errors: [`JSON 解析失败 / JSON parse error: ${error.message}`]
        });
      }
    }

    return results;
  }
}

/**
 * 技能文档生成器
 * Skill documentation generator
 */
class SkillDocGenerator {
  /**
   * 批量生成技能文档
   * Batch generate skill documentation
   * @param {Array} validatedConfigs - 验证后的配置数组
   * @returns {Promise<Map<string, string>>} 生成的文档内容映射
   */
  static async batchGenerateDocs(validatedConfigs) {
    const docs = new Map();

    for (const { valid, file, config, errors } of validatedConfigs) {
      if (!valid) {
        docs.set(file, this._generateErrorDoc(file, errors));
        continue;
      }

      const doc = this._generateSkillDoc(config);
      docs.set(file, doc);
    }

    return docs;
  }

  /**
   * 生成技能文档
   * Generate skill documentation
   * @private
   */
  static _generateSkillDoc(config) {
    return `# ${config.name}

## 版本 / Version
${config.version}

## 描述 / Description
${config.description}

## 作者 / Author
${config.author || '未指定 / Not specified'}

## API 版本 / API Version
${config.metadata?.apiVersion || '未指定 / Not specified'}

## 兼容性 / Compatibility
${config.metadata?.compatibility ? JSON.stringify(config.metadata.compatibility, null, 2) : '未指定 / Not specified'}

## 配置 / Configuration
\`\`\`json
${JSON.stringify(config, null, 2)}
\`\`\`

---
*Generated by skill-creator-meta v2.0*
`;
  }

  /**
   * 生成错误文档
   * Generate error documentation
   * @private
   */
  static _generateErrorDoc(file, errors) {
    return `# 错误报告 / Error Report

## 文件 / File
${file}

## 错误 / Errors
${errors.map(e => `- ${e}`).join('\n')}

---
*Generated by skill-creator-meta v2.0*
`;
  }
}

/**
 * 主工作流程
 * Main workflow
 */
async function main() {
  console.log('🚀 skill-creator-meta v2.0 批量工具集成 / Batch Tool Integration\n');

  // 1. 定义要处理的文件 / Define files to process
  const templateDir = path.join(__dirname, '..', 'template');
  const configFiles = [
    path.join(templateDir, 'skill-config.json'),
  ];

  console.log('📁 批量读取配置文件 / Batch reading config files...');
  const configs = await BatchFileOperations.batchRead(configFiles);

  const readCount = Array.from(configs.values()).filter(c => c !== null).length;
  console.log(`✅ 读取成功 / Read successfully: ${readCount}/${configFiles.length}\n`);

  console.log('🔍 批量验证配置 / Batch validating configurations...');
  const validationResults = await SkillConfigValidator.batchValidate(configs);

  const validCount = validationResults.filter(r => r.valid).length;
  console.log(`✅ 验证通过 / Validated successfully: ${validCount}/${validationResults.length}\n`);

  console.log('📝 批量生成文档 / Batch generating documentation...');
  const docs = await SkillDocGenerator.batchGenerateDocs(validationResults);

  console.log(`✅ 生成文档 / Generated docs: ${docs.size}\n`);

  // 4. 输出结果示例 / Output sample results
  console.log('📊 结果摘要 / Results Summary:');
  console.log('='.repeat(50));

  for (const [file, doc] of docs.entries()) {
    const fileName = path.basename(file);
    console.log(`\n📄 ${fileName}`);
    console.log('-'.repeat(50));
    console.log(doc.split('\n').slice(0, 10).join('\n'));
    console.log('...\n');
  }

  console.log('='.repeat(50));
  console.log('\n✨ 批量处理完成 / Batch processing completed!\n');
}

// 运行脚本 / Run script
if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  BatchFileOperations,
  SkillConfigValidator,
  SkillDocGenerator
};
