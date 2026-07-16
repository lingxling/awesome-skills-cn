import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import chalk from 'chalk';
import ora from 'ora';
import { getLatestRelease } from '../utils/github.js';
import { logger } from '../utils/logger.js';
import { initCommand } from './init.js';
import type { AIType } from '../types/index.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI_PACKAGE_NAME = 'ui-ux-pro-max-cli';

interface UpdateOptions {
  ai?: AIType;
  token?: string;
}

async function getPackageVersion(): Promise<string> {
  const packagePath = join(__dirname, '..', 'package.json');
  const pkg = JSON.parse(await readFile(packagePath, 'utf-8')) as { version: string };
  return pkg.version;
}

function normalizeTagVersion(tagName: string): string {
  return tagName.replace(/^v/i, '');
}

export async function updateCommand(options: UpdateOptions): Promise<void> {
  logger.title('UI/UX Pro Max Updater');

  const spinner = ora('Checking for updates...').start();

  try {
    const release = await getLatestRelease(options.token);
    const currentVersion = await getPackageVersion();
    const latestVersion = normalizeTagVersion(release.tag_name);
    spinner.succeed(`Latest version: ${chalk.cyan(release.tag_name)}`);

    if (currentVersion !== latestVersion) {
      console.log();

      // Only auto-run with a well-formed semver, so nothing unexpected can
      // reach the shell that npm.cmd requires on Windows.
      if (!/^\d+\.\d+\.\d+([.-][0-9A-Za-z.-]+)?$/.test(latestVersion)) {
        logger.warn(`Installed CLI is ${chalk.cyan(currentVersion)}; latest release is ${chalk.cyan(release.tag_name)}.`);
        logger.info(`Update the CLI package: ${chalk.cyan(`npm install -g ${CLI_PACKAGE_NAME}@${latestVersion}`)}`);
        logger.info('Then rerun: uipro init --ai <platform> --force');
        return;
      }

      logger.info(`Updating CLI from ${chalk.cyan(currentVersion)} to ${chalk.cyan(latestVersion)}...`);
      console.log();

      const isWindows = process.platform === 'win32';
      try {
        // execFileSync with an explicit args array — no shell string to expand.
        // On Windows npm is npm.cmd, which Node only spawns via a shell.
        execFileSync(
          isWindows ? 'npm.cmd' : 'npm',
          ['install', '-g', `${CLI_PACKAGE_NAME}@${latestVersion}`],
          { stdio: 'inherit', shell: isWindows }
        );
      } catch {
        console.log();
        logger.error('Automatic update failed (you may need elevated/admin permissions).');
        logger.info(`Update manually: ${chalk.cyan(`npm install -g ${CLI_PACKAGE_NAME}@${latestVersion}`)}`);
        process.exit(1);
      }

      console.log();
      logger.success(`Updated to ${chalk.cyan(latestVersion)}.`);
      logger.info(`Now rerun ${chalk.cyan('uipro init --ai <platform> --force')} to refresh your skill files.`);
      return;
    }

    console.log();
    logger.info('Refreshing installed skill files from this CLI package...');
    console.log();

    await initCommand({
      ai: options.ai,
      force: true,
      token: options.token,
    });
  } catch (error) {
    spinner.fail('Update check failed');
    if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
}
