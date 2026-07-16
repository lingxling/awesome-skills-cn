#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const isWindows = process.platform === 'win32';
const localBin = (name) => join('node_modules', '.bin', isWindows ? `${name}.cmd` : name);

function run(command, args) {
  const result = spawnSync(command, args, { stdio: 'inherit', shell: false });
  if (result.error && result.error.code === 'ENOENT') {
    return { missing: true, status: 127 };
  }
  return { missing: false, status: result.status ?? 1 };
}

const bunResult = run('bun', ['build', 'src/index.ts', '--outdir', 'dist', '--target', 'node']);
if (!bunResult.missing) {
  process.exit(bunResult.status);
}

const tsc = localBin('tsc');
if (!existsSync(tsc)) {
  console.error('Build failed: neither bun nor local TypeScript compiler is available.');
  console.error('Run `npm ci` first, or install Bun from https://bun.sh/docs/installation.');
  process.exit(127);
}

console.warn('bun not found; falling back to TypeScript compiler output.');
const tscResult = run(tsc, []);
process.exit(tscResult.status);
