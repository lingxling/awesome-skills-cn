import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { redactSensitiveText } from '../../../skills/vercel-optimize/lib/vercel.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..', '..', 'skills', 'vercel-optimize');

test('redactSensitiveText: removes auth tokens from CLI-visible text', () => {
  const raw = [
    'VERCEL_TOKEN=vercel_secret_1234567890abcdef vercel metrics',
    'vercel metrics --token vercel_secret_abcdef1234567890',
    'Authorization: Bearer abcdefghijklmnopqrstuvwxyz.1234567890',
    '{"token":"secret-json-token-abcdef123456"}',
    'x-vercel-id: sfo1::w45r5-1778646511413-d7c8c3cb26cb',
    'project prj_1234567890abcdef team team_1234567890abcdef user usr_1234567890abcdef',
  ].join('\n');

  const redacted = redactSensitiveText(raw);

  assert.doesNotMatch(redacted, /vercel_secret|abcdefghijklmnopqrstuvwxyz|secret-json-token/);
  assert.doesNotMatch(redacted, /w45r5-1778646511413|prj_1234567890abcdef|team_1234567890abcdef|usr_1234567890abcdef/);
  assert.match(redacted, /VERCEL_TOKEN=\[REDACTED\]/);
  assert.match(redacted, /--token \[REDACTED\]/);
  assert.match(redacted, /Authorization: \[REDACTED\]/);
  assert.match(redacted, /x-vercel-id: \[REDACTED\]/);
  assert.match(redacted, /project prj_\[REDACTED\] team team_\[REDACTED\] user usr_\[REDACTED\]/);
  assert.match(redacted, /"token":"\[REDACTED\]"/);
});

test('collect-signals status logs do not print raw project or team IDs', async () => {
  const src = await readFile(join(ROOT, 'scripts', 'collect-signals.mjs'), 'utf-8');

  assert.doesNotMatch(src, /projectId=\$\{project\.projectId\}/);
  assert.doesNotMatch(src, /orgId=\$\{project\.orgId/);
  assert.doesNotMatch(src, /matched \$\{project\.projectId\}/);
  assert.match(src, /project link resolved/);
});

test('deep-dive status logs do not print raw linked project IDs', async () => {
  const src = await readFile(join(ROOT, 'scripts', 'deep-dive.mjs'), 'utf-8');

  assert.doesNotMatch(src, /project \$\{link\.projectId\}/);
  assert.doesNotMatch(src, /\$\{merged\.projectId\}/);
  assert.match(src, /dir-linked-to-the-collected-project/);
});
