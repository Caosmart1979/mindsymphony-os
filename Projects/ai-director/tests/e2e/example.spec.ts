import { test, expect } from '@playwright/test';
import { readFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join } from 'path';

/**
 * MindSymphony E2E Test Suite
 * 
 * Tests for the MindSymphony AI cognitive system architecture.
 * Validates project structure, documentation integrity, and system configuration.
 */

test.describe('MindSymphony System Validation', () => {
  const projectRoot = process.cwd();

  test('system has all required components', () => {
    const requiredDirs = ['core', 'gateway', 'integrations', 'extensions'];
    for (const dir of requiredDirs) {
      expect(existsSync(join(projectRoot, dir))).toBe(true);
    }
  });

  test('core cognitive skills are documented', () => {
    const coreDir = join(projectRoot, 'core');
    const coreSkills = readdirSync(coreDir).filter(f => f.endsWith('.md'));
    expect(coreSkills.length).toBeGreaterThanOrEqual(6);
    
    const requiredSkills = [
      'cognitive-architect.md',
      'knowledge-explorer.md',
      'brand-alchemist.md'
    ];
    
    for (const skill of requiredSkills) {
      expect(coreSkills).toContain(skill);
    }
  });

  test('gateway security components exist', () => {
    const gatewayDir = join(projectRoot, 'gateway');
    const gatewayFiles = readdirSync(gatewayDir).filter(f => f.endsWith('.md'));
    
    expect(gatewayFiles).toContain('security-gateway.md');
    expect(gatewayFiles).toContain('external-synapse.md');
    expect(gatewayFiles).toContain('egress-policy.md');
  });

  test('integration documentation is complete', () => {
    const integrationsDir = join(projectRoot, 'integrations');
    const integrationFiles = readdirSync(integrationsDir).filter(f => f.endsWith('.md'));
    
    expect(integrationFiles).toContain('_INDEX.md');
    expect(integrationFiles).toContain('README.md');
    expect(integrationFiles.length).toBeGreaterThan(5);
  });

  test('SKILL.md has proper metadata', () => {
    const skillPath = join(projectRoot, 'SKILL.md');
    const content = readFileSync(skillPath, 'utf-8');
    
    expect(content).toMatch(/name:\s*mindsymphony/);
    expect(content).toMatch(/version:\s*"[\d.]+"/);
    expect(content).toMatch(/description:\s*"/);
    expect(content).toContain('心智协奏系统');
  });

  test('VERSION.yml has system section', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    const content = readFileSync(versionPath, 'utf-8');
    
    expect(content).toMatch(/system:/);
    expect(content).toMatch(/name:\s*"MindSymphony"/);
    expect(content).toMatch(/version:\s*"[\d.]+"/);
  });

  test('documentation has proper frontmatter', () => {
    const coreDir = join(projectRoot, 'core');
    const files = readdirSync(coreDir).filter(f => f.endsWith('.md'));
    
    for (const file of files) {
      const content = readFileSync(join(coreDir, file), 'utf-8');
      expect(content).toMatch(/^---\s*$/m);
      expect(content).toMatch(/name:\s*\w+/);
    }
  });

  test('package.json has correct dependencies', () => {
    const pkgPath = join(projectRoot, 'package.json');
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
    
    expect(pkg.name).toBe('mindsymphony');
    expect(pkg.scripts.test).toBeDefined();
    expect(pkg.devDependencies['@playwright/test']).toBeDefined();
  });

  test('playwright configuration is valid', () => {
    const configPath = join(projectRoot, 'playwright.config.ts');
    const content = readFileSync(configPath, 'utf-8');
    
    expect(content).toContain('@playwright/test');
    expect(content).toContain('defineConfig');
  });

  test('extension categories exist', () => {
    const extensionsDir = join(projectRoot, 'extensions');
    const categories = readdirSync(extensionsDir);
    
    const requiredCategories = [
      'creative', 'research', 'strategy', 'engineering', 'writing'
    ];
    
    for (const category of requiredCategories) {
      expect(categories).toContain(category);
    }
  });

  test('documentation quality check', () => {
    const coreDir = join(projectRoot, 'core');
    const files = readdirSync(coreDir).filter(f => f.endsWith('.md'));
    
    for (const file of files) {
      const content = readFileSync(join(coreDir, file), 'utf-8');
      expect(content.length).toBeGreaterThan(500);
      expect(content).toMatch(/#+\s+\w+/);
    }
  });
});
