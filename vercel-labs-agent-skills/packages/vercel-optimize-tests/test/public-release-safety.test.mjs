import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { test } from 'node:test';
import assert from 'node:assert/strict';

const ROOT = join(import.meta.dirname, '..', '..', '..');
const SKILL_DIR = join(ROOT, 'skills', 'vercel-optimize');

test('public release safety: metadata version matches skill frontmatter', async () => {
  const skill = await readFile(join(SKILL_DIR, 'SKILL.md'), 'utf8');
  const metadata = JSON.parse(await readFile(join(SKILL_DIR, 'metadata.json'), 'utf8'));
  const version = skill.match(/metadata:\s*\n\s*version:\s*"([^"]+)"/)?.[1];
  assert.equal(metadata.version, version);
});

test('public release safety: docs avoid private customer names and stale artifact names', async () => {
  const files = await listFiles(SKILL_DIR);
  const publicDocs = files.filter((file) => /\.(?:md|json)$/.test(file));
  const forbidden = /\/Users\/[A-Za-z0-9._-]+|\bteam-[a-z-]*engineering\b|\bship-\d{4}\b|gated\.json/;

  for (const file of publicDocs) {
    const text = await readFile(file, 'utf8');
    assert.doesNotMatch(text, forbidden, file);
  }
});

test('public release safety: shipped source and fixtures avoid private-run artifacts', async () => {
  const files = [
    ...await listFiles(SKILL_DIR),
    ...await listFiles(join(ROOT, 'packages', 'vercel-optimize-tests', 'test')),
  ];
  const publicFiles = files.filter((file) =>
    /\.(?:mjs|md|json|txt)$/.test(file) && !file.endsWith('public-release-safety.test.mjs')
  );
  const sourceForbidden = /\/Users\/[A-Za-z0-9._-]+|\bteam-[a-z-]*engineering\b|\bship-\d{4}\b|\b[a-z]+-dashboard\b|Field benchmark:/;
  const unredactedVercelId = /^x-vercel-id:\s+(?!\[REDACTED\]$).+$/m;

  for (const file of publicFiles) {
    const text = await readFile(file, 'utf8');
    assert.doesNotMatch(text, sourceForbidden, file);
    if (file.endsWith('.txt')) {
      assert.doesNotMatch(text, unredactedVercelId, file);
    }
  }
});

test('public release safety: public docs do not imply project ID replaces linkage', async () => {
  const files = [
    join(SKILL_DIR, 'README.md'),
    join(SKILL_DIR, 'AGENTS.md'),
    join(SKILL_DIR, 'SKILL.md'),
  ];

  for (const file of files) {
    const text = await readFile(file, 'utf8');
    assert.doesNotMatch(text, /Linked Vercel project(?:,| directory) or `VERCEL_PROJECT_ID`/, file);
    assert.doesNotMatch(text, /Linked Vercel project, or `VERCEL_PROJECT_ID`/, file);
  }
});

test('public release safety: compact skill keeps blocker and platform brief instructions', async () => {
  const skill = await readFile(join(SKILL_DIR, 'SKILL.md'), 'utf8');

  assert.match(skill, /daily_quota_exceeded/);
  assert.match(skill, /The `group` can be `toLaunch` or `platform`/);
});

test('public release safety: docs library uses verified current URLs', async () => {
  const text = await readFile(join(SKILL_DIR, 'references', 'docs-library.json'), 'utf8');
  const staleUrls = [
    'https://vercel.com/docs/functions/fluid-compute',
    'https://vercel.com/docs/functions/serverless-functions',
    'https://vercel.com/docs/functions/regions',
    'https://vercel.com/docs/observability/anomaly-detection',
    'https://vercel.com/docs/edge-network/bandwidth',
    'https://vercel.com/docs/security/bot-protection',
    'https://vercel.com/docs/limits/limits-and-quotas',
    'https://nextjs.org/docs/app/api-reference/functions/dynamic',
  ];

  for (const url of staleUrls) {
    assert.doesNotMatch(text, new RegExp(escapeRegExp(url)), url);
  }
});

async function listFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const out = [];
  for (const entry of entries) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...await listFiles(path));
    else out.push(path);
  }
  return out;
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
