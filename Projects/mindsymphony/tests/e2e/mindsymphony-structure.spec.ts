import { test, expect } from '@playwright/test';
import { readFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join } from 'path';

test.describe('MindSymphony Project Structure', () => {
  const projectRoot = process.cwd();

  test('has required top-level directories', () => {
    const requiredDirs = ['core', 'extensions', 'gateway', 'integrations', 'router', 'registry', 'tests'];
    for (const dir of requiredDirs) {
      const dirPath = join(projectRoot, dir);
      expect(existsSync(dirPath), `Directory ${dir} should exist`).toBe(true);
      expect(statSync(dirPath).isDirectory(), `${dir} should be a directory`).toBe(true);
    }
  });

  test('has required configuration files', () => {
    const requiredFiles = ['package.json', 'playwright.config.ts', 'VERSION.yml', 'SKILL.md'];
    for (const file of requiredFiles) {
      const filePath = join(projectRoot, file);
      expect(existsSync(filePath), `File ${file} should exist`).toBe(true);
      expect(statSync(filePath).isFile(), `${file} should be a file`).toBe(true);
    }
  });

  test('has all core cognitive components', () => {
    const coreDir = join(projectRoot, 'core');
    const requiredCoreComponents = [
      'cognitive-architect.md',
      'knowledge-explorer.md',
      'brand-alchemist.md',
      'concept-singularity.md',
      'official-writer.md',
      'prompt-pharmacist.md'
    ];
    for (const component of requiredCoreComponents) {
      const filePath = join(coreDir, component);
      expect(existsSync(filePath), `Core component ${component} should exist`).toBe(true);
    }
  });

  test('has all gateway components', () => {
    const gatewayDir = join(projectRoot, 'gateway');
    const requiredGatewayComponents = [
      'security-gateway.md',
      'external-synapse.md',
      'egress-policy.md',
      'version-check.md'
    ];
    for (const component of requiredGatewayComponents) {
      const filePath = join(gatewayDir, component);
      expect(existsSync(filePath), `Gateway component ${component} should exist`).toBe(true);
    }
  });
});

test.describe('Documentation Quality', () => {
  const projectRoot = process.cwd();

  test('core components have proper frontmatter', () => {
    const coreDir = join(projectRoot, 'core');
    const files = readdirSync(coreDir).filter(f => f.endsWith('.md'));
    for (const file of files) {
      const content = readFileSync(join(coreDir, file), 'utf-8');
      expect(content, `${file} should start with frontmatter delimiter`).toMatch(/^---\s*$/m);
      expect(content, `${file} should have name field`).toMatch(/name:\s*\w+/);
    }
  });

  test('SKILL.md has required metadata', () => {
    const skillMdPath = join(projectRoot, 'SKILL.md');
    const content = readFileSync(skillMdPath, 'utf-8');
    expect(content).toMatch(/name:\s*mindsymphony/);
    expect(content).toMatch(/version:\s*"[\d.]+"/);
    expect(content).toContain('心智协奏系统');
  });

  test('documentation files have meaningful content', () => {
    const coreDir = join(projectRoot, 'core');
    const files = readdirSync(coreDir).filter(f => f.endsWith('.md'));
    for (const file of files) {
      const content = readFileSync(join(coreDir, file), 'utf-8');
      expect(content.length, `${file} should have substantial content`).toBeGreaterThan(500);
      expect(content, `${file} should have markdown headers`).toMatch(/#+\s+\w+/);
    }
  });
});

test.describe('Configuration Validation', () => {
  const projectRoot = process.cwd();

  test('package.json has correct structure', () => {
    const pkgPath = join(projectRoot, 'package.json');
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
    expect(pkg.name).toBe('mindsymphony');
    expect(pkg.version).toBeDefined();
    expect(pkg.scripts).toBeDefined();
    expect(pkg.scripts.test).toBeDefined();
    expect(pkg.devDependencies).toBeDefined();
    expect(pkg.devDependencies['@playwright/test']).toBeDefined();
  });

  test('playwright.config.ts exists and is valid', () => {
    const configPath = join(projectRoot, 'playwright.config.ts');
    const content = readFileSync(configPath, 'utf-8');
    expect(content).toContain('@playwright/test');
    expect(content).toContain('defineConfig');
    expect(content).toMatch(/testDir:\s*['"]/);
  });
});
