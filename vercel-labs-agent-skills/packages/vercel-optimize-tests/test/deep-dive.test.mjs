import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { chmod, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import {
  specsForCandidate,
  mergeIntoEvidence,
  escapeODataString,
  odataEq,
  odataAnd,
  SPEC_GENERATORS,
  SCANNER_KINDS,
  TIME_WINDOW,
} from '../../../skills/vercel-optimize/lib/deep-dive.mjs';
import { gates } from '../../../skills/vercel-optimize/lib/gates/index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const FX = join(HERE, 'fixtures', 'real-cli-output', 'deep-dive');
const SCRIPT = join(HERE, '../../../skills/vercel-optimize/scripts/deep-dive.mjs');
const exec = promisify(execFile);

test('deep-dive: specsForCandidate(slow_route) is deterministic', () => {
  const c = { kind: 'slow_route', route: '/dashboard/[sessionId]' };
  const a = specsForCandidate(c);
  const b = specsForCandidate(c);
  assert.deepEqual(a, b, 'same input → same output');
  // 14 specs: latency (4 percentiles) + ttfb (4) + cpu + startType + status +
  // perDep + cacheBreakdown + bandwidthByCache. cacheBreakdown +
  // bandwidthByCache added May 2026 so static routes don't false-abstain when
  // latency lives on the cache-miss path.
  assert.equal(a.length, 14, 'slow_route spec count');
  const ids = new Set(a.map((s) => s.id));
  assert.ok(ids.has('cacheBreakdown'), 'cacheBreakdown spec included');
  assert.ok(ids.has('bandwidthByCache'), 'bandwidthByCache spec included');
  for (const s of a) assert.equal(s.since, TIME_WINDOW, `${s.id} window`);
  assert.equal(ids.size, a.length, 'ids unique');
});

test('deep-dive: specsForCandidate(uncached_route) covers cache + method + bot + bandwidth', () => {
  const specs = specsForCandidate({ kind: 'uncached_route', route: '/api/items' });
  const ids = specs.map((s) => s.id).sort();
  assert.deepEqual(ids, ['bandwidthByCache', 'botShare', 'cacheBreakdown', 'methodDistribution']);
});

test('deep-dive: specsForCandidate(cold_start) includes cold-only deployment slice', () => {
  const specs = specsForCandidate({ kind: 'cold_start', route: '/admin' });
  const colds = specs.find((s) => s.id === 'coldByDeployment');
  assert.ok(colds, 'coldByDeployment present');
  assert.match(colds.filter, /function_start_type eq 'cold'/);
  assert.match(colds.filter, /route eq '\/admin'/);
});

test('deep-dive: specsForCandidate(external_api_slow) uses origin_route as caller dim', () => {
  const specs = specsForCandidate({ kind: 'external_api_slow', hostname: 'api.example.com' });
  const callers = specs.find((s) => s.id === 'callersByRoute');
  assert.ok(callers);
  assert.deepEqual(callers.groupBy, ['origin_route'], 'caller dim is origin_route (NOT route/function_path)');
  assert.equal(callers.filter, "origin_hostname eq 'api.example.com'");
});

test('deep-dive: specsForCandidate(route_errors) emits per-status + per-deploy + error_code', () => {
  const specs = specsForCandidate({ kind: 'route_errors', route: '/api/checkout' });
  const ids = specs.map((s) => s.id).sort();
  assert.deepEqual(ids, ['errorCodes', 'errorStatusPattern', 'errorsByDeployment']);
  const pat = specs.find((s) => s.id === 'errorStatusPattern');
  assert.match(pat.filter, /http_status ge '500'/);
  assert.match(pat.filter, /route eq '\/api\/checkout'/);
});

test('deep-dive: specsForCandidate(unknown kind) returns []', () => {
  assert.deepEqual(specsForCandidate({ kind: 'this_kind_does_not_exist' }), []);
});

test('deep-dive: specsForCandidate(scanner kind) returns []', () => {
  for (const k of SCANNER_KINDS) {
    assert.deepEqual(specsForCandidate({ kind: k, route: '/x' }), [], `${k} skipped`);
  }
});

test('deep-dive: specsForCandidate({}) returns []', () => {
  assert.deepEqual(specsForCandidate({}), []);
  assert.deepEqual(specsForCandidate(null), []);
});

test('escapeODataString: doubles single quotes, leaves brackets alone', () => {
  assert.equal(escapeODataString("/dashboard/[sessionId]"), "/dashboard/[sessionId]");
  assert.equal(escapeODataString("/path/with'quote"), "/path/with''quote");
  assert.equal(escapeODataString("plain"), "plain");
});

test('odataEq: route literal with brackets is safe (matches captured CLI behaviour)', () => {
  const f = odataEq('route', '/dashboard/[sessionId]');
  assert.equal(f, "route eq '/dashboard/[sessionId]'");
});

test('odataAnd: drops empty strings, joins the rest with " and "', () => {
  assert.equal(odataAnd("a eq '1'", "b eq '2'"), "a eq '1' and b eq '2'");
  assert.equal(odataAnd("a eq '1'", "", "c eq '3'"), "a eq '1' and c eq '3'");
  assert.equal(odataAnd(""), "");
});

test('odataEq escapes embedded single quotes', () => {
  assert.equal(odataEq('route', "/o'reilly"), "route eq '/o''reilly'");
});

test('deep-dive: every non-scanner gate kind in lib/gates/index.mjs has a SPEC_GENERATORS entry', () => {
  const gateKinds = gates
    .map((g) => g.metadata?.id)
    .filter((id) => id && id !== 'scanner-driven');
  // scanner-driven exports id='scanner-driven' but emits 4 kinds tracked in SCANNER_KINDS.
  for (const k of gateKinds) {
    assert.ok(
      typeof SPEC_GENERATORS[k] === 'function',
      `kind=${k} has SPEC_GENERATORS entry`,
    );
  }
});

test('deep-dive: SCANNER_KINDS matches scanner-driven gate kinds', () => {
  // use_client_boundary removed May 2026 (0.3% conversion rate).
  assert.ok(SCANNER_KINDS.has('image_optimization'));
  assert.ok(SCANNER_KINDS.has('cache_header_gap'));
  assert.ok(SCANNER_KINDS.has('rendering_candidate'));
});

test('mergeIntoEvidence: scalar specs become numbers; group-by specs become arrays', () => {
  const results = [
    { spec: { id: 'startTypeSplit' }, ok: true, rows: [
      { function_start_type: 'hot', value: 4893 },
      { function_start_type: 'cold', value: 19 },
    ] },
    { spec: { id: 'latency.p95' }, ok: true, value: 1066.4623 },
    { spec: { id: 'latency.p50' }, ok: true, value: 120 },
  ];
  const merged = mergeIntoEvidence(results);
  assert.deepEqual(merged.startTypeSplit, [
    { function_start_type: 'hot', value: 4893 },
    { function_start_type: 'cold', value: 19 },
  ]);
  assert.equal(merged.latency.p95, 1066.4623);
  assert.equal(merged.latency.p50, 120);
});

test('mergeIntoEvidence: error entries surface as {error: code}', () => {
  const merged = mergeIntoEvidence([
    { spec: { id: 'cpu.p95' }, ok: false, error: 'FORBIDDEN' },
  ]);
  assert.deepEqual(merged.cpu, { p95: { error: 'FORBIDDEN' } });
});

test('mergeIntoEvidence: empty list → empty object', () => {
  assert.deepEqual(mergeIntoEvidence([]), {});
});

test('mergeIntoEvidence: ignores entries with no spec id', () => {
  const merged = mergeIntoEvidence([{ spec: {}, ok: true, value: 5 }]);
  assert.deepEqual(merged, {});
});

test('mergeIntoEvidence: scalar value=null stays null (does not leak entry/spec)', () => {
  // Regression: fixture-app 24-parallel-call rows missing the metric field
  // used to fall through and leak the whole {entry,spec,ok,value:null} wrapper
  // (~600 bytes per dead cell).
  const merged = mergeIntoEvidence([
    {
      // runner attaches these — must not leak into evidence.
      entry: { c: { kind: 'slow_route', route: '/x', files: [], massiveNoise: 'x'.repeat(500) }, group: 'toLaunch', i: 0 },
      spec: { id: 'latency.p95', metricId: 'vercel.function_invocation.function_duration_ms', aggregation: 'p95', groupBy: [], filter: "route eq '/x'", since: '14d' },
      ok: true,
      value: null,
    },
  ]);
  assert.deepEqual(merged.latency, { p95: null }, 'value=null surfaces as null leaf, not the wrapper');
});

test('mergeIntoEvidence: top-level scalar value=null surfaces as null', () => {
  const merged = mergeIntoEvidence([
    { entry: { huge: 'x'.repeat(500) }, spec: { id: 'transferBytes', metricId: 'x', aggregation: 'sum', groupBy: [] }, ok: true, value: null },
  ]);
  assert.equal(merged.transferBytes, null);
});

test('deep-dive: CLI fixture startTypeSplit round-trips through the runner-equivalent normalizer', async () => {
  // Mirrors scripts/deep-dive.mjs without the CLI shell-out.
  const raw = JSON.parse(await readFile(join(FX, 'slow_route_startTypeSplit.json'), 'utf-8'));
  const spec = {
    id: 'startTypeSplit',
    metricId: 'vercel.function_invocation.count',
    aggregation: 'sum',
    groupBy: ['function_start_type'],
  };
  const field = `${spec.metricId.replace(/\./g, '_')}_${spec.aggregation}`;
  const rows = raw.summary.map((row) => {
    const out = { value: row[field] };
    for (const dim of spec.groupBy) {
      if (row[dim] !== undefined) out[dim] = row[dim];
    }
    return out;
  });
  // Captured fixture-app values: hot=4893, cold=19, prewarmed=11.
  const hot = rows.find((r) => r.function_start_type === 'hot');
  const cold = rows.find((r) => r.function_start_type === 'cold');
  assert.ok(hot && cold);
  assert.equal(hot.value, 4893);
  assert.equal(cold.value, 19);
});

test('deep-dive: CLI fixture perDeployment surfaces the p95 split by deployment_id', async () => {
  const raw = JSON.parse(await readFile(join(FX, 'slow_route_perDeployment.json'), 'utf-8'));
  // Fixture has 2 deployments; the slower (deployment-regression) p95 ~1420ms.
  const ids = raw.summary.map((r) => r.deployment_id);
  assert.equal(ids.length, 2);
  const slow = raw.summary.find((r) => r.deployment_id === 'deployment-regression');
  assert.ok(slow.vercel_function_invocation_function_duration_ms_p95 > 1000);
});

test('deep-dive: slow_route fixture filter matches the spec generator output', async () => {
  const raw = JSON.parse(await readFile(join(FX, 'slow_route_perDeployment.json'), 'utf-8'));
  const specs = specsForCandidate({ kind: 'slow_route', route: '/dashboard/[sessionId]' });
  const perDep = specs.find((s) => s.id === 'perDeployment');
  assert.equal(perDep.filter, raw.query.filter);
});

test('deep-dive runner scopes metrics to the linked team slug', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-deep-dive-scope-'));
  const bin = join(scratch, 'bin');
  try {
    await mkdir(bin, { recursive: true });
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_scope',
      orgId: 'team_scope',
    }), 'utf-8');
    await writeFile(join(scratch, 'merged.json'), JSON.stringify({
      schemaVersion: '1.2',
      projectId: 'prj_scope',
      orgId: 'team_scope',
      metrics: {},
    }), 'utf-8');
    await writeFile(join(scratch, 'gate.json'), JSON.stringify({
      toLaunch: [{ kind: 'route_errors', scope: 'route', route: '/api/fail', priority: 10 }],
      platform: [],
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
if (args[0] === 'whoami' && args[1] === '--format') {
  json({
    username: 'test-user',
    team: { id: 'team_other', slug: 'other-team', name: 'Other Team' },
  });
}
if (args[0] === 'api' && args[1] === '/v2/teams/team_scope') {
  json({ id: 'team_scope', slug: 'team-scope', name: 'Team Scope' });
}
if (args[0] === 'metrics') {
  requireScope('team-scope');
  const metric = args[1];
  const aggIndex = args.indexOf('-a');
  const aggregation = aggIndex === -1 ? 'sum' : args[aggIndex + 1];
  const field = metric.replace(/\\./g, '_') + '_' + aggregation;
  json({
    summary: [{
      [field]: 5,
      http_status: '500',
      error_code: 'ERR_TEST',
      deployment_id: 'dpl_test',
    }],
  });
}
process.stderr.write('unexpected vercel call: ' + args.join(' ') + '\\n');
process.exit(66);
`, 'utf-8');
    await chmod(fakeVercel, 0o755);

    const { stdout, stderr } = await exec('node', [
      SCRIPT,
      join(scratch, 'merged.json'),
      join(scratch, 'gate.json'),
      '--cwd',
      scratch,
    ], {
      env: { ...process.env, PATH: `${bin}:${process.env.PATH}` },
      maxBuffer: 8 * 1024 * 1024,
    });

    const out = JSON.parse(stdout);
    assert.equal(out.queriesRun, 3);
    assert.deepEqual(out.errors, []);
    assert.equal(out.toLaunch[0].evidence.deepDive.errorStatusPattern[0].http_status, '500');
    assert.doesNotMatch(stderr, /unexpected vercel call/);
    assert.doesNotMatch(stderr, /missing expected scope/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('deep-dive runner stops when cwd scope differs from collected signals', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-deep-dive-scope-mismatch-'));
  try {
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_scope',
      orgId: 'team_other',
    }), 'utf-8');
    await writeFile(join(scratch, 'merged.json'), JSON.stringify({
      schemaVersion: '1.2',
      projectId: 'prj_scope',
      orgId: 'team_scope',
      commandScope: { ok: true, cliScope: 'team-scope', source: 'team-api' },
      metrics: {},
    }), 'utf-8');
    await writeFile(join(scratch, 'gate.json'), JSON.stringify({
      toLaunch: [{ kind: 'route_errors', scope: 'route', route: '/api/fail', priority: 10 }],
      platform: [],
    }), 'utf-8');

    let err;
    try {
      await exec('node', [
        SCRIPT,
        join(scratch, 'merged.json'),
        join(scratch, 'gate.json'),
        '--cwd',
        scratch,
      ], {
        maxBuffer: 8 * 1024 * 1024,
      });
    } catch (e) {
      err = e;
    }

    assert.ok(err, 'deep-dive should stop when cwd is linked to a different scope');
    assert.equal(err.code, 2);
    assert.equal(err.stdout, '');
    assert.match(err.stderr, /different Vercel scope/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test('deep-dive runner stops when commandScope account differs from cwd link', async () => {
  const scratch = await mkdtemp(join(tmpdir(), 'vo-deep-dive-command-scope-mismatch-'));
  try {
    await mkdir(join(scratch, '.vercel'), { recursive: true });
    await writeFile(join(scratch, '.vercel', 'project.json'), JSON.stringify({
      projectId: 'prj_scope',
      orgId: 'team_other',
    }), 'utf-8');
    await writeFile(join(scratch, 'merged.json'), JSON.stringify({
      schemaVersion: '1.2',
      projectId: 'prj_scope',
      commandScope: {
        ok: true,
        cliScope: 'team-scope',
        source: 'team-api',
        teamId: 'team_scope',
      },
      metrics: {},
    }), 'utf-8');
    await writeFile(join(scratch, 'gate.json'), JSON.stringify({
      toLaunch: [{ kind: 'route_errors', scope: 'route', route: '/api/fail', priority: 10 }],
      platform: [],
    }), 'utf-8');

    let err;
    try {
      await exec('node', [
        SCRIPT,
        join(scratch, 'merged.json'),
        join(scratch, 'gate.json'),
        '--cwd',
        scratch,
      ], {
        maxBuffer: 8 * 1024 * 1024,
      });
    } catch (e) {
      err = e;
    }

    assert.ok(err, 'deep-dive should stop when persisted commandScope targets another account');
    assert.equal(err.code, 2);
    assert.equal(err.stdout, '');
    assert.match(err.stderr, /different Vercel scope than commandScope/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});
