import { test, expect } from '@playwright/test';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

test.describe('YAML Configuration Validation', () => {
  const projectRoot = process.cwd();

  test('VERSION.yml exists and is readable', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    expect(existsSync(versionPath)).toBe(true);
  });

  test('VERSION.yml has system section', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    const content = readFileSync(versionPath, 'utf-8');
    
    expect(content).toMatch(/system:/);
    expect(content).toMatch(/name:\s*"MindSymphony"/);
    expect(content).toMatch(/version:\s*"[\d.]+"/);
  });

  test('VERSION.yml has required fields', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    const content = readFileSync(versionPath, 'utf-8');
    
    expect(content).toMatch(/name:\s*"MindSymphony"/);
    expect(content).toMatch(/full_name:/);
    expect(content).toMatch(/codename:/);
    expect(content).toMatch(/release_date:\s*"\d{4}-\d{2}-\d{2}"/);
  });

  test('VERSION.yml has components section', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    const content = readFileSync(versionPath, 'utf-8');
    
    expect(content).toMatch(/components:/);
    expect(content).toMatch(/core:/);
    expect(content).toMatch(/extensions:/);
    expect(content).toMatch(/integrations:/);
  });

  test('VERSION.yml version format is correct', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    const content = readFileSync(versionPath, 'utf-8');
    
    expect(content).toMatch(/version:\s*"\d+\.\d+\.\d+"/);
  });

  test('VERSION.yml has evolution history', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    const content = readFileSync(versionPath, 'utf-8');
    
    expect(content).toMatch(/evolution:/);
    expect(content).toMatch(/-\s*version:/);
  });

  test('registry/skills.yml exists', () => {
    const skillsPath = join(projectRoot, 'registry/skills.yml');
    expect(existsSync(skillsPath)).toBe(true);
  });

  test('registry/skills.yml has system section', () => {
    const skillsPath = join(projectRoot, 'registry/skills.yml');
    const content = readFileSync(skillsPath, 'utf-8');
    
    expect(content).toMatch(/system:/);
    expect(content).toMatch(/name:\s*mindsymphony/);
    expect(content).toMatch(/version:/);
    expect(content).toMatch(/default_router:/);
    expect(content).toMatch(/fallback_skill:/);
  });

  test('registry/skills.yml has internal_skills section', () => {
    const skillsPath = join(projectRoot, 'registry/skills.yml');
    const content = readFileSync(skillsPath, 'utf-8');
    
    expect(content).toMatch(/internal_skills:/);
    expect(content).toMatch(/cognitive-architect:/);
    expect(content).toMatch(/knowledge-explorer:/);
  });

  test('registry/skills.yml has core skills defined', () => {
    const skillsPath = join(projectRoot, 'registry/skills.yml');
    const content = readFileSync(skillsPath, 'utf-8');
    
    expect(content).toMatch(/cognitive-architect:/);
    expect(content).toMatch(/knowledge-explorer:/);
    expect(content).toMatch(/brand-alchemist:/);
    expect(content).toMatch(/concept-singularity:/);
  });

  test('version consistency across files', () => {
    const versionPath = join(projectRoot, 'VERSION.yml');
    const versionContent = readFileSync(versionPath, 'utf-8');
    
    const skillPath = join(projectRoot, 'SKILL.md');
    const skillContent = readFileSync(skillPath, 'utf-8');
    
    const versionMatch = versionContent.match(/version:\s*"(\d+\.\d+\.\d+)"/);
    const skillVersionMatch = skillContent.match(/version:\s*"(\d+\.\d+\.\d+)"/);
    
    if (versionMatch && skillVersionMatch) {
      expect(skillVersionMatch[1]).toBe(versionMatch[1]);
    }
  });

  test('YAML files have proper comments', () => {
    const yamlFiles = [
      'VERSION.yml',
      'registry/skills.yml'
    ];
    
    for (const file of yamlFiles) {
      const filePath = join(projectRoot, file);
      const content = readFileSync(filePath, 'utf-8');
      
      // Check for comments (YAML comments start with #)
      expect(content, `${file} should have explanatory comments`).toMatch(/#/);
    }
  });
});
