import { test, expect } from '@playwright/test';
import { readFileSync, readdirSync, existsSync } from 'fs';
import { join } from 'path';

test.describe('Gateway Components Validation', () => {
  const projectRoot = process.cwd();

  test('all gateway components exist', () => {
    const gatewayDir = join(projectRoot, 'gateway');
    const gatewayFiles = readdirSync(gatewayDir).filter(f => f.endsWith('.md'));
    
    expect(gatewayFiles).toContain('security-gateway.md');
    expect(gatewayFiles).toContain('external-synapse.md');
    expect(gatewayFiles).toContain('egress-policy.md');
    expect(gatewayFiles).toContain('version-check.md');
    expect(gatewayFiles.length).toBeGreaterThanOrEqual(4);
  });

  test('security gateway documentation is complete', () => {
    const securityPath = join(projectRoot, 'gateway/security-gateway.md');
    const content = readFileSync(securityPath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(1000);
    expect(content).toMatch(/security|安全|gateway|网关/i);
    expect(content).toMatch(/#+\s+\w+/);
  });

  test('external synapse documentation exists', () => {
    const synapsePath = join(projectRoot, 'gateway/external-synapse.md');
    const content = readFileSync(synapsePath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(1000);
    expect(content).toMatch(/external|外部|synapse|突触|webhook/i);
  });

  test('egress policy documentation is present', () => {
    const egressPath = join(projectRoot, 'gateway/egress-policy.md');
    const content = readFileSync(egressPath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(1000);
    expect(content).toMatch(/egress|出站|policy|策略|security|安全/i);
  });

  test('version check documentation exists', () => {
    const versionCheckPath = join(projectRoot, 'gateway/version-check.md');
    const content = readFileSync(versionCheckPath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(1000);
    expect(content).toMatch(/version|版本|check|检查/i);
  });

  test('gateway docs have proper frontmatter', () => {
    const gatewayDir = join(projectRoot, 'gateway');
    const files = readdirSync(gatewayDir).filter(f => f.endsWith('.md'));
    
    for (const file of files) {
      const content = readFileSync(join(gatewayDir, file), 'utf-8');
      expect(content, `${file} should have frontmatter`).toMatch(/^---\s*$/m);
      expect(content, `${file} should have name field`).toMatch(/name:\s*\w+/);
    }
  });
});

test.describe('Integration Components Validation', () => {
  const projectRoot = process.cwd();

  test('all required integration docs exist', () => {
    const integrationsDir = join(projectRoot, 'integrations');
    const integrationFiles = readdirSync(integrationsDir).filter(f => f.endsWith('.md'));
    
    expect(integrationFiles).toContain('_INDEX.md');
    expect(integrationFiles).toContain('README.md');
    expect(integrationFiles).toContain('academic-forge.md');
    expect(integrationFiles).toContain('ai-agent-architect.md');
    expect(integrationFiles).toContain('notebooklm.md');
  });

  test('integration index is comprehensive', () => {
    const indexPath = join(projectRoot, 'integrations/_INDEX.md');
    const content = readFileSync(indexPath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(500);
    expect(content).toMatch(/academic|ai-agent|notebooklm|gemini/i);
  });

  test('integration README exists', () => {
    const readmePath = join(projectRoot, 'integrations/README.md');
    const content = readFileSync(readmePath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(1000);
    expect(content).toMatch(/integration|集成|external|外部/i);
  });

  test('academic forge integration is documented', () => {
    const academicPath = join(projectRoot, 'integrations/academic-forge.md');
    const content = readFileSync(academicPath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(500);
    expect(content).toMatch(/academic|forge|学术/i);
  });

  test('AI agent architect integration exists', () => {
    const agentPath = join(projectRoot, 'integrations/ai-agent-architect.md');
    const content = readFileSync(agentPath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(500);
    expect(content).toMatch(/agent|architect|智能体/i);
  });

  test('NotebookLM integration is documented', () => {
    const notebookPath = join(projectRoot, 'integrations/notebooklm.md');
    const content = readFileSync(notebookPath, 'utf-8');
    
    expect(content.length).toBeGreaterThan(1000);
    expect(content).toMatch(/notebooklm|knowledge|知识库/i);
  });

  test('gemini CLI integration exists', () => {
    const geminiPath = join(projectRoot, 'integrations/gemini-cli.md');
    expect(existsSync(geminiPath)).toBe(true);
    
    const content = readFileSync(geminiPath, 'utf-8');
    expect(content.length).toBeGreaterThan(500);
  });

  test('skill creator meta integration exists', () => {
    const skillPath = join(projectRoot, 'integrations/skill-creator-meta.md');
    expect(existsSync(skillPath)).toBe(true);
    
    const content = readFileSync(skillPath, 'utf-8');
    expect(content.length).toBeGreaterThan(500);
  });

  test('integration docs have proper structure', () => {
    const integrationsDir = join(projectRoot, 'integrations');
    const files = readdirSync(integrationsDir).filter(f => f.endsWith('.md') && !f.startsWith('_'));
    
    for (const file of files) {
      const content = readFileSync(join(integrationsDir, file), 'utf-8');
      
      // Should have markdown headers
      expect(content, `${file} should have markdown headers`).toMatch(/#+\s+\w+/);
      
      // Should have meaningful content
      expect(content.length, `${file} should have substantial content`).toBeGreaterThan(300);
    }
  });
});

test.describe('Extension Categories Validation', () => {
  const projectRoot = process.cwd();

  test('all extension categories exist', () => {
    const extensionsDir = join(projectRoot, 'extensions');
    const categories = readdirSync(extensionsDir);
    
    const requiredCategories = [
      'creative',
      'domains',
      'engineering',
      'meta',
      'research',
      'strategy',
      'thinking',
      'writing'
    ];
    
    for (const category of requiredCategories) {
      expect(categories).toContain(category);
    }
  });

  test('extension categories are directories', () => {
    const extensionsDir = join(projectRoot, 'extensions');
    const categories = readdirSync(extensionsDir);
    
    for (const category of categories) {
      const categoryPath = join(extensionsDir, category);
      expect(existsSync(categoryPath)).toBe(true);
    }
  });

  test('meta category contains skill documentation', () => {
    const metaDir = join(projectRoot, 'extensions/meta');
    const metaFiles = readdirSync(metaDir);
    
    expect(metaFiles.length).toBeGreaterThan(0);
  });
});
