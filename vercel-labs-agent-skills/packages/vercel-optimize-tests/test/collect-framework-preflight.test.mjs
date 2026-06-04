import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { chmod, mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const exec = promisify(execFile);
const HERE = dirname(fileURLToPath(import.meta.url));
const COLLECT = join(HERE, '..', '..', '..', 'skills', 'vercel-optimize', 'scripts', 'collect-signals.mjs');

test('collect-signals: unsupported framework stops before Observability and usage calls', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-framework-preflight-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, 'package.json'), JSON.stringify({
      dependencies: { hono: '^4.7.0' },
    }), 'utf-8');
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_test',
      orgId: 'team_test',
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/bin/sh
if [ "$1" = "--version" ]; then
  echo "53.0.0"
  exit 0
fi
if [ "$1" = "whoami" ]; then
  echo "test-user"
  exit 0
fi
echo "unexpected vercel call: $*" >&2
exit 66
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    const { stdout, stderr } = await exec('node', [COLLECT], {
      cwd: scratch,
      env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
      maxBuffer: 8 * 1024 * 1024,
    });
    const out = JSON.parse(stdout);
    assert.equal(out.stack.framework, 'hono');
    assert.equal(out.frameworkSupportBlocker, 'unsupported_framework');
    assert.equal(out.observabilityPlus, null);
    assert.equal(out.usageError, 'NOT_COLLECTED_UNSUPPORTED_FRAMEWORK');
    assert.match(stderr, /framework=hono@4\.7\.0 support=unsupported/);
    assert.doesNotMatch(stderr, /unexpected vercel call/);
    assert.doesNotMatch(stderr, /checking Observability Plus configuration/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('collect-signals: uses Vercel account billing.plan before empty-contract heuristics', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-plan-preflight-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, 'package.json'), JSON.stringify({
      dependencies: { next: '^15.3.0' },
    }), 'utf-8');
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_test',
      orgId: 'team_hobby',
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/usr/bin/env node
const args = process.argv.slice(2);
function json(value, code = 0) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\\n');
  process.exit(code);
}
if (args[0] === '--version') {
  process.stdout.write('54.1.0\\n');
  process.exit(0);
}
if (args[0] === 'whoami') {
  process.stdout.write('test-user\\n');
  process.exit(0);
}
if (args[0] === 'api') {
  const path = args[1];
  if (path.startsWith('/v1/observability/manage/configuration/projects')) {
    json({ error: { code: 'not_found', message: 'Observability Plus is not enabled' } }, 1);
  }
  if (path === '/v9/projects/prj_test?teamId=team_hobby') {
    json({ id: 'prj_test', name: 'fixture-site' });
  }
  if (path === '/v2/teams/team_hobby') {
    json({ id: 'team_hobby', slug: 'fixture', billing: { plan: 'hobby' } });
  }
}
function requireScope(expected) {
  const i = args.indexOf('--scope');
  if (i === -1 || args[i + 1] !== expected) {
    process.stderr.write('missing expected scope ' + expected + ': ' + args.join(' ') + '\\n');
    process.exit(67);
  }
}
if (args[0] === 'contract') {
  requireScope('fixture');
  json({ context: 'fixture', commitments: [], totalCommitments: 0 });
}
if (args[0] === 'usage') {
  requireScope('fixture');
  json({
    context: 'fixture',
    groupBy: { dimension: 'project', data: [] },
    services: [],
    totals: { billedCost: 0 },
  });
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    const { stdout, stderr } = await exec('node', [COLLECT, '--continue-without-observability'], {
      cwd: scratch,
      env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
      maxBuffer: 8 * 1024 * 1024,
    });
    const out = JSON.parse(stdout);
    assert.equal(out.plan.plan, 'hobby');
    assert.match(out.plan.reason, /team\.billing\.plan=hobby/);
    assert.equal(out.commandScope.cliScope, 'fixture');
    assert.equal(out.commandScope.source, 'team-api');
    assert.deepEqual(out.contract, { context: 'fixture', commitments: [], totalCommitments: 0 });
    assert.equal(out.usageError, null);
    assert.doesNotMatch(stderr, /unexpected vercel call/);
    assert.doesNotMatch(stderr, /missing expected scope/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('collect-signals: scopes metrics, contract, and usage to the linked team slug', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-command-scope-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, 'package.json'), JSON.stringify({
      dependencies: { next: '^15.3.0' },
    }), 'utf-8');
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_scope',
      orgId: 'team_scope',
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/usr/bin/env node
const args = process.argv.slice(2);
function json(value, code = 0) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\\n');
  process.exit(code);
}
function requireScope(expected) {
  const i = args.indexOf('--scope');
  if (i === -1 || args[i + 1] !== expected || args.includes('team_scope')) {
    process.stderr.write('missing expected scope ' + expected + ': ' + args.join(' ') + '\\n');
    process.exit(67);
  }
}
if (args[0] === '--version') {
  process.stdout.write('54.1.0\\n');
  process.exit(0);
}
if (args[0] === 'whoami' && args[1] === '--format') {
  json({
    username: 'test-user',
    team: { id: 'team_other', slug: 'other-team', name: 'Other Team' },
  });
}
if (args[0] === 'whoami') {
  process.stdout.write('test-user\\n');
  process.exit(0);
}
if (args[0] === 'api') {
  const path = args[1];
  if (path.startsWith('/v1/observability/manage/configuration/projects')) {
    json({ disabledProjects: [] });
  }
  if (path === '/v9/projects/prj_scope?teamId=team_scope') {
    json({ id: 'prj_scope', name: 'fixture-site' });
  }
  if (path === '/v2/teams/team_scope') {
    json({ id: 'team_scope', slug: 'team-scope', billing: { plan: 'pro' } });
  }
}
if (args[0] === 'metrics') {
  requireScope('team-scope');
  json({ summary: [], data: [], statistics: {} });
}
if (args[0] === 'contract') {
  requireScope('team-scope');
  json({ context: 'team-scope', commitments: [], totalCommitments: 0 });
}
if (args[0] === 'usage') {
  requireScope('team-scope');
  json({
    context: 'team-scope',
    groupBy: {
      dimension: 'project',
      data: [{
        projectId: 'prj_scope',
        name: 'fixture-site',
        services: [{ name: 'Function Invocations', billedCost: 3 }],
        totals: { billedCost: 3 },
      }],
    },
    services: [{ name: 'Function Invocations', billedCost: 3 }],
    totals: { billedCost: 3 },
  });
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    const { stdout, stderr } = await exec('node', [COLLECT], {
      cwd: scratch,
      env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
      maxBuffer: 8 * 1024 * 1024,
    });
    const out = JSON.parse(stdout);
    assert.equal(out.commandScope.cliScope, 'team-scope');
    assert.equal(out.commandScope.source, 'team-api');
    assert.equal(out.usageScope, 'project');
    assert.equal(out.usageError, null);
    assert.equal(out.usage.project.projectId, 'prj_scope');
    assert.match(out.plan.reason, /team\.billing\.plan=pro/);
    assert.doesNotMatch(stderr, /unexpected vercel call/);
    assert.doesNotMatch(stderr, /missing expected scope/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('collect-signals: stops on project/team mismatch before Observability Plus checks', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-project-scope-mismatch-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, 'package.json'), JSON.stringify({
      dependencies: { next: '^15.3.0' },
    }), 'utf-8');
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_target',
      orgId: 'team_wrong',
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/usr/bin/env node
const args = process.argv.slice(2);
function json(value, code = 0) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\\n');
  process.exit(code);
}
if (args[0] === '--version') {
  process.stdout.write('54.1.0\\n');
  process.exit(0);
}
if (args[0] === 'whoami' && args[1] === '--format') {
  json({
    username: 'test-user',
    team: { id: 'team_other', slug: 'other-team', name: 'Other Team' },
  });
}
if (args[0] === 'whoami') {
  process.stdout.write('test-user\\n');
  process.exit(0);
}
if (args[0] === 'api') {
  const path = args[1];
  if (path === '/v2/teams/team_wrong') {
    json({ id: 'team_wrong', slug: 'wrong-team', billing: { plan: 'pro' } });
  }
  if (path === '/v9/projects/prj_target?teamId=team_wrong') {
    json({ error: { code: 'PROJECT_NOT_FOUND', message: 'Project not found' } }, 1);
  }
  if (path.startsWith('/v1/observability/manage/configuration/projects')) {
    process.stderr.write('observability should not be checked before project ownership is verified\\n');
    process.exit(68);
  }
}
if (args[0] === 'metrics' || args[0] === 'usage' || args[0] === 'contract') {
  process.stderr.write('scoped collection should not run before project ownership is verified: ' + args.join(' ') + '\\n');
  process.exit(69);
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    let err;
    try {
      await exec('node', [COLLECT], {
        cwd: scratch,
        env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
        maxBuffer: 8 * 1024 * 1024,
      });
    } catch (e) {
      err = e;
    }

    assert.ok(err, 'collector should stop when the resolved team cannot read the project');
    assert.equal(err.code, 1);
    assert.equal(err.stdout, '');
    assert.match(err.stderr, /PROJECT_SCOPE_MISMATCH/);
    assert.doesNotMatch(err.stderr, /observability should not be checked/);
    assert.doesNotMatch(err.stderr, /scoped collection should not run/);
    assert.doesNotMatch(err.stderr, /Observability Plus is NOT usable/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('collect-signals: user-owned projects use username scope without teamId query params', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-user-scope-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, 'package.json'), JSON.stringify({
      dependencies: { next: '^15.3.0' },
    }), 'utf-8');
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_user',
      orgId: 'usr_personal',
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/usr/bin/env node
const args = process.argv.slice(2);
function json(value, code = 0) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\\n');
  process.exit(code);
}
function requireScope(expected) {
  const i = args.indexOf('--scope');
  if (i === -1 || args[i + 1] !== expected || args.includes('usr_personal')) {
    process.stderr.write('missing expected scope ' + expected + ': ' + args.join(' ') + '\\n');
    process.exit(67);
  }
}
if (args[0] === '--version') {
  process.stdout.write('54.1.0\\n');
  process.exit(0);
}
if (args[0] === 'whoami' && args[1] === '--format') {
  json({
    user: { id: 'usr_personal', username: 'personal-user', billing: { plan: 'pro' } },
  });
}
if (args[0] === 'whoami') {
  process.stdout.write('personal-user\\n');
  process.exit(0);
}
if (args[0] === 'metrics' && args[1] === 'schema') {
  requireScope('personal-user');
  json({ error: { code: 'OPLUS_REQUIRED', message: 'Observability Plus is not enabled' } }, 1);
}
if (args[0] === 'api') {
  const path = args[1];
  if (path.startsWith('/v1/observability/manage/configuration/projects')) {
    process.stderr.write('unexpected team Observability configuration probe for user-owned project\\n');
    process.exit(68);
  }
  if (path.startsWith('/v9/projects/prj_user?teamId=')) {
    process.stderr.write('unexpected user project teamId query: ' + path + '\\n');
    process.exit(69);
  }
  if (path === '/v9/projects/prj_user') {
    json({ id: 'prj_user', name: 'personal-site' });
  }
  if (path === '/v2/user') {
    json({ user: { username: 'personal-user', billing: { plan: 'pro' } } });
  }
}
if (args[0] === 'contract') {
  requireScope('personal-user');
  json({ context: 'personal-user', commitments: [], totalCommitments: 0 });
}
if (args[0] === 'usage') {
  requireScope('personal-user');
  json({
    context: 'personal-user',
    groupBy: {
      dimension: 'project',
      data: [{
        projectId: 'prj_user',
        name: 'personal-site',
        services: [{ name: 'Function Invocations', billedCost: 4 }],
        totals: { billedCost: 4 },
      }],
    },
    services: [{ name: 'Function Invocations', billedCost: 4 }],
    totals: { billedCost: 4 },
  });
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    const { stdout, stderr } = await exec('node', [COLLECT, '--continue-without-observability'], {
      cwd: scratch,
      env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
      maxBuffer: 8 * 1024 * 1024,
    });
    const out = JSON.parse(stdout);
    assert.equal(out.commandScope.cliScope, 'personal-user');
    assert.equal(out.commandScope.source, 'whoami-user');
    assert.equal(out.usageScope, 'project');
    assert.equal(out.usageError, null);
    assert.equal(out.usage.project.projectId, 'prj_user');
    assert.equal(out.project.id, 'prj_user');
    assert.equal(out.plan.plan, 'pro');
    assert.match(out.observabilityPlusPreflight.detail, /user-owned project/);
    assert.doesNotMatch(stderr, /unexpected vercel call/);
    assert.doesNotMatch(stderr, /missing expected scope/);
    assert.doesNotMatch(stderr, /teamId query/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('collect-signals: missing orgId stops before scoped Vercel calls', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-missing-scope-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, 'package.json'), JSON.stringify({
      dependencies: { next: '^15.3.0' },
    }), 'utf-8');
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_test',
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/usr/bin/env node
const args = process.argv.slice(2);
function json(value, code = 0) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\\n');
  process.exit(code);
}
if (args[0] === '--version') {
  process.stdout.write('54.1.0\\n');
  process.exit(0);
}
if (args[0] === 'whoami' && args.length === 1) {
  process.stdout.write('test-user\\n');
  process.exit(0);
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    let err;
    try {
      await exec('node', [COLLECT, '--continue-without-observability'], {
        cwd: scratch,
        env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
        maxBuffer: 8 * 1024 * 1024,
      });
    } catch (e) {
      err = e;
    }
    assert.ok(err, 'collector should stop when project scope is ambiguous');
    assert.equal(err.code, 1);
    assert.equal(err.stdout, '');
    assert.match(err.stderr, /PROJECT_SCOPE_UNRESOLVED/);
    assert.doesNotMatch(err.stderr, /unexpected vercel call/);
    assert.doesNotMatch(err.stderr, /whoami --format/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('collect-signals: multi-project repo.json stops instead of choosing the first project', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-ambiguous-repo-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, '.vercel', 'repo.json'), JSON.stringify({
      projects: [
        { id: 'prj_first', orgId: 'team_first' },
        { id: 'prj_second', orgId: 'team_second' },
      ],
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/usr/bin/env node
const args = process.argv.slice(2);
if (args[0] === '--version') {
  process.stdout.write('54.1.0\\n');
  process.exit(0);
}
if (args[0] === 'whoami' && args.length === 1) {
  process.stdout.write('test-user\\n');
  process.exit(0);
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    let err;
    try {
      await exec('node', [COLLECT], {
        cwd: scratch,
        env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
        maxBuffer: 8 * 1024 * 1024,
      });
    } catch (e) {
      err = e;
    }
    assert.ok(err, 'collector should stop on ambiguous repo links');
    assert.equal(err.code, 1);
    assert.equal(err.stdout, '');
    assert.match(err.stderr, /AMBIGUOUS_PROJECT_LINK/);
    assert.doesNotMatch(err.stderr, /unexpected vercel call/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('collect-signals: explicit projectId resolves matching owner from multi-project repo.json', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-explicit-repo-project-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, 'package.json'), JSON.stringify({
      dependencies: { next: '^15.3.0' },
    }), 'utf-8');
    await writeFile(join(scratch, '.vercel', 'repo.json'), JSON.stringify({
      projects: [
        { id: 'prj_first', orgId: 'team_first' },
        { id: 'prj_second', orgId: 'team_second' },
      ],
    }), 'utf-8');
    const fakeVercel = join(bin, 'vercel');
    await writeFile(fakeVercel, `#!/usr/bin/env node
const args = process.argv.slice(2);
function json(value, code = 0) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\\n');
  process.exit(code);
}
function requireScope(expected) {
  const i = args.indexOf('--scope');
  if (i === -1 || args[i + 1] !== expected || args.includes('team_second')) {
    process.stderr.write('missing expected scope ' + expected + ': ' + args.join(' ') + '\\n');
    process.exit(67);
  }
}
if (args[0] === '--version') {
  process.stdout.write('54.1.0\\n');
  process.exit(0);
}
if (args[0] === 'whoami' && args[1] === '--format') {
  json({
    username: 'test-user',
    team: { id: 'team_first', slug: 'first-team', name: 'First Team' },
  });
}
if (args[0] === 'whoami') {
  process.stdout.write('test-user\\n');
  process.exit(0);
}
if (args[0] === 'api') {
  const path = args[1];
  if (path === '/v2/teams/team_second') {
    json({ id: 'team_second', slug: 'second-team', billing: { plan: 'pro' } });
  }
  if (path === '/v9/projects/prj_second?teamId=team_second') {
    json({ id: 'prj_second', accountId: 'team_second', name: 'second-site' });
  }
  if (path.startsWith('/v1/observability/manage/configuration/projects')) {
    json({ error: { code: 'not_found', message: 'Observability Plus is not enabled' } }, 1);
  }
}
if (args[0] === 'contract') {
  requireScope('second-team');
  json({ context: 'second-team', commitments: [], totalCommitments: 0 });
}
if (args[0] === 'usage') {
  requireScope('second-team');
  json({
    context: 'second-team',
    groupBy: {
      dimension: 'project',
      data: [{
        projectId: 'prj_second',
        name: 'second-site',
        services: [{ name: 'Function Invocations', billedCost: 2 }],
        totals: { billedCost: 2 },
      }],
    },
    services: [{ name: 'Function Invocations', billedCost: 2 }],
    totals: { billedCost: 2 },
  });
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    const { stdout, stderr } = await exec('node', [COLLECT, 'prj_second', '--continue-without-observability'], {
      cwd: scratch,
      env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
      maxBuffer: 8 * 1024 * 1024,
    });
    const out = JSON.parse(stdout);
    assert.equal(out.projectId, 'prj_second');
    assert.equal(out.orgId, 'team_second');
    assert.equal(out.projectIdSource, 'arg+repo.json');
    assert.equal(out.commandScope.cliScope, 'second-team');
    assert.equal(out.commandScope.source, 'team-api');
    assert.equal(out.project.accountId, 'team_second');
    assert.equal(out.usageScope, 'project');
    assert.equal(out.usage.project.projectId, 'prj_second');
    assert.doesNotMatch(stderr, /unexpected vercel call/);
    assert.doesNotMatch(stderr, /missing expected scope/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});
