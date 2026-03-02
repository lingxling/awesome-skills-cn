import { readFile, mkdir, writeFile, cp, access, readdir } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
// After bun build: dist/index.js -> ../assets = cli/assets ✓
const ASSETS_DIR = join(__dirname, '..', 'assets');

export interface PlatformConfig {
  platform: string;
  displayName: string;
  installType: 'full' | 'reference';
  folderStructure: {
    root: string;
    skillPath: string;
    filename: string;
  };
  scriptPath: string;
  frontmatter: Record<string, string> | null;
  sections: {
    quickReference: boolean;
  };
  title: string;
  description: string;
  skillOrWorkflow: string;
}

// Map AIType to platform config file name
const AI_TO_PLATFORM: Record<string, string> = {
  claude: 'claude',
  cursor: 'cursor',
  windsurf: 'windsurf',
  antigravity: 'agent',
  copilot: 'copilot',
  kiro: 'kiro',
  opencode: 'opencode',
  roocode: 'roocode',
  codex: 'codex',
  qoder: 'qoder',
  gemini: 'gemini',
  trae: 'trae',
  continue: 'continue',
  codebuddy: 'codebuddy',
  droid: 'droid',
};

async function exists(path: string): Promise<boolean> {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

/**
 * Load platform configuration from JSON file
 */
export async function loadPlatformConfig(aiType: string): Promise<PlatformConfig> {
  const platformName = AI_TO_PLATFORM[aiType];
  if (!platformName) {
    throw new Error(`Unknown AI type: ${aiType}`);
  }

  const configPath = join(ASSETS_DIR, 'templates', 'platforms', `${platformName}.json`);
  const content = await readFile(configPath, 'utf-8');
  return JSON.parse(content) as PlatformConfig;
}

/**
 * Load all available platform configs
 */
export async function loadAllPlatformConfigs(): Promise<Map<string, PlatformConfig>> {
  const configs = new Map<string, PlatformConfig>();

  for (const [aiType, platformName] of Object.entries(AI_TO_PLATFORM)) {
    try {
      const config = await loadPlatformConfig(aiType);
      configs.set(aiType, config);
    } catch {
      // Skip if config doesn't exist
    }
  }

  return configs;
}

/**
 * Load a template file
 */
async function loadTemplate(templateName: string): Promise<string> {
  const templatePath = join(ASSETS_DIR, 'templates', templateName);
  return readFile(templatePath, 'utf-8');
}

/**
 * Render frontmatter section
 */
function renderFrontmatter(frontmatter: Record<string, string> | null): string {
  if (!frontmatter) return '';

  const lines = ['---'];
  for (const [key, value] of Object.entries(frontmatter)) {
    // Quote values that contain special characters
    if (value.includes(':') || value.includes('"') || value.includes('\n')) {
      lines.push(`${key}: "${value.replace(/"/g, '\\"')}"`);
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  lines.push('---', '');
  return lines.join('\n');
}

/**
 * Render skill file content from template
 */
export async function renderSkillFile(config: PlatformConfig): Promise<string> {
  // Load base template
  let content = await loadTemplate('base/skill-content.md');

  // Load quick reference if needed
  let quickReferenceContent = '';
  if (config.sections.quickReference) {
    quickReferenceContent = await loadTemplate('base/quick-reference.md');
  }

  // Build the final content
  const frontmatter = renderFrontmatter(config.frontmatter);

  // Replace placeholders
  // Add newline before quick reference content if it exists
  const quickRefWithNewline = quickReferenceContent ? '\n' + quickReferenceContent : '';

  content = content
    .replace(/\{\{TITLE\}\}/g, config.title)
    .replace(/\{\{DESCRIPTION\}\}/g, config.description)
    .replace(/\{\{SCRIPT_PATH\}\}/g, config.scriptPath)
    .replace(/\{\{SKILL_OR_WORKFLOW\}\}/g, config.skillOrWorkflow)
    .replace(/\{\{QUICK_REFERENCE\}\}/g, quickRefWithNewline);

  return frontmatter + content;
}

/**
 * Copy data and scripts to target directory
 */
async function copyDataAndScripts(targetSkillDir: string): Promise<void> {
  const dataSource = join(ASSETS_DIR, 'data');
  const scriptsSource = join(ASSETS_DIR, 'scripts');

  const dataTarget = join(targetSkillDir, 'data');
  const scriptsTarget = join(targetSkillDir, 'scripts');

  // Copy data
  if (await exists(dataSource)) {
    await mkdir(dataTarget, { recursive: true });
    await cp(dataSource, dataTarget, { recursive: true });
  }

  // Copy scripts
  if (await exists(scriptsSource)) {
    await mkdir(scriptsTarget, { recursive: true });
    await cp(scriptsSource, scriptsTarget, { recursive: true });
  }
}

/**
 * Generate platform files for a specific AI type
 * All platforms use self-contained installation with data and scripts
 */
export async function generatePlatformFiles(
  targetDir: string,
  aiType: string
): Promise<string[]> {
  const config = await loadPlatformConfig(aiType);
  const createdFolders: string[] = [];

  // Determine full skill directory path
  const skillDir = join(
    targetDir,
    config.folderStructure.root,
    config.folderStructure.skillPath
  );

  // Create directory structure
  await mkdir(skillDir, { recursive: true });

  // Render and write skill file
  const skillContent = await renderSkillFile(config);
  const skillFilePath = join(skillDir, config.folderStructure.filename);
  await writeFile(skillFilePath, skillContent, 'utf-8');
  createdFolders.push(config.folderStructure.root);

  // Copy data and scripts into the skill directory (self-contained)
  await copyDataAndScripts(skillDir);

  return createdFolders;
}

/**
 * Generate files for all AI types
 */
export async function generateAllPlatformFiles(targetDir: string): Promise<string[]> {
  const allFolders = new Set<string>();

  for (const aiType of Object.keys(AI_TO_PLATFORM)) {
    try {
      const folders = await generatePlatformFiles(targetDir, aiType);
      folders.forEach(f => allFolders.add(f));
    } catch {
      // Skip if generation fails for a platform
    }
  }

  return Array.from(allFolders);
}

/**
 * Get list of supported AI types
 */
export function getSupportedAITypes(): string[] {
  return Object.keys(AI_TO_PLATFORM);
}
