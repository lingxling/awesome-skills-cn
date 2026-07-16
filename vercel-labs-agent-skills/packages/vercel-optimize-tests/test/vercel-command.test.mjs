import { test } from 'node:test';
import assert from 'node:assert/strict';
import { win32 } from 'node:path';
import { resolveVercelCommand } from '../../../skills/vercel-optimize/lib/vercel.mjs';

const NODE = 'C:\\Program Files\\nodejs\\node.exe';

function fakeFs({ files = [], reads = {} } = {}) {
  const fileSet = new Set(files.map((file) => win32.normalize(file)));
  const readMap = new Map(
    Object.entries(reads).map(([file, text]) => [win32.normalize(file), text])
  );
  return {
    exists: (file) => fileSet.has(win32.normalize(file)),
    readText: (file) => {
      const key = win32.normalize(file);
      if (!readMap.has(key)) throw new Error(`missing fixture: ${file}`);
      return readMap.get(key);
    },
  };
}

test('resolveVercelCommand: POSIX keeps bare vercel command', () => {
  assert.deepEqual(
    resolveVercelCommand({
      platform: 'linux',
      env: { PATH: '/repo/node_modules/.bin:/usr/local/bin' },
      execPath: '/usr/local/bin/node',
      exists: () => false,
    }),
    { file: 'vercel', prefix: [] }
  );
});

test('resolveVercelCommand: Windows resolves npm global package entry', () => {
  const bin = 'C:\\Users\\me\\AppData\\Roaming\\npm';
  const entry = win32.join(bin, 'node_modules', 'vercel', 'dist', 'vc.js');
  const fs = fakeFs({ files: [entry] });

  assert.deepEqual(
    resolveVercelCommand({
      platform: 'win32',
      env: { PATH: bin },
      execPath: NODE,
      ...fs,
    }),
    { file: NODE, prefix: [entry] }
  );
});

test('resolveVercelCommand: Windows resolves local node_modules .bin package entry', () => {
  const bin = 'C:\\repo\\node_modules\\.bin';
  const entry = 'C:\\repo\\node_modules\\vercel\\dist\\vc.js';
  const fs = fakeFs({ files: [entry] });

  assert.deepEqual(
    resolveVercelCommand({
      platform: 'win32',
      env: { PATH: bin },
      execPath: NODE,
      ...fs,
    }),
    { file: NODE, prefix: [entry] }
  );
});

test('resolveVercelCommand: Windows parses vercel.cmd shim targets with spaces', () => {
  const bin = 'C:\\Users\\me\\App Data\\pnpm';
  const shim = win32.join(bin, 'vercel.cmd');
  const entry = win32.normalize(win32.join(bin, '..', 'store', 'vercel', 'dist', 'vc.js'));
  const fs = fakeFs({
    files: [shim, entry],
    reads: {
      [shim]: '@ECHO off\r\n"%_prog%" "%~dp0\\..\\store\\vercel\\dist\\vc.js" %*\r\n',
    },
  });

  assert.deepEqual(
    resolveVercelCommand({
      platform: 'win32',
      env: { Path: bin },
      execPath: NODE,
      ...fs,
    }),
    { file: NODE, prefix: [entry] }
  );
});

test('resolveVercelCommand: Windows reports missing instead of falling back to .cmd', () => {
  const bin = 'C:\\repo\\node_modules\\.bin';
  const fs = fakeFs();

  assert.deepEqual(
    resolveVercelCommand({
      platform: 'win32',
      env: { PATH: bin },
      execPath: NODE,
      ...fs,
    }),
    { file: NODE, prefix: [], missing: true }
  );
});
