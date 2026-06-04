import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import {
  applyHardGates,
  FLAGS_ENDPOINT,
  WORKFLOW_ENDPOINT_PREFIXES,
  isFlagsEndpointCandidate,
  isWorkflowRuntimeEndpointCandidate,
} from '../../../skills/vercel-optimize/lib/gates/hard-gates.mjs';
import { detectStack } from '../../../skills/vercel-optimize/lib/vercel.mjs';

const exec = promisify(execFile);
const HERE = dirname(fileURLToPath(import.meta.url));
const GATE_SCRIPT = join(HERE, '..', '..', '..', 'skills', 'vercel-optimize', 'scripts', 'gate-investigations.mjs');

test('isFlagsEndpointCandidate: detects the exact Vercel Flags endpoint', () => {
  assert.equal(isFlagsEndpointCandidate({ scope: 'route', route: FLAGS_ENDPOINT }), true);
  assert.equal(isFlagsEndpointCandidate({ scope: 'route', route: `${FLAGS_ENDPOINT}/` }), true);
  assert.equal(isFlagsEndpointCandidate({ scope: 'route', route: '/api/flags' }), false);
  assert.equal(isFlagsEndpointCandidate({ scope: 'account' }), false);
});

test('applyHardGates: gates the Vercel Flags endpoint with package context', () => {
  const flags = { kind: 'slow_route', scope: 'route', route: FLAGS_ENDPOINT, priority: 100 };
  const other = { kind: 'slow_route', scope: 'route', route: '/api/orders', priority: 90 };
  const out = applyHardGates([flags, other], {
    stack: { hasVercelFlagsPackage: true, vercelFlagsPackages: ['@vercel/flags'] },
  });
  assert.deepEqual(out.allowed, [other]);
  assert.equal(out.gated.length, 1);
  assert.match(out.gated[0].gatedReason, /Vercel Flags endpoint/);
  assert.match(out.gated[0].gatedReason, /@vercel\/flags/);
});

test('isWorkflowRuntimeEndpointCandidate: detects Vercel Workflow runtime endpoints', () => {
  assert.deepEqual(WORKFLOW_ENDPOINT_PREFIXES, ['/.well-known/workflow', '/api/.well-known/workflow']);
  assert.equal(isWorkflowRuntimeEndpointCandidate({ scope: 'route', route: '/.well-known/workflow/v1/step' }), true);
  assert.equal(isWorkflowRuntimeEndpointCandidate({ scope: 'route', route: '/.well-known/workflow/v1/flow/' }), true);
  assert.equal(isWorkflowRuntimeEndpointCandidate({ scope: 'route', route: '/api/.well-known/workflow/v1/step' }), true);
  assert.equal(isWorkflowRuntimeEndpointCandidate({ scope: 'route', route: '/.well-known/vercel/flags' }), false);
  assert.equal(isWorkflowRuntimeEndpointCandidate({ scope: 'route', route: '/api/projects/ai/chat/[id]/stream' }), false);
  assert.equal(isWorkflowRuntimeEndpointCandidate({ scope: 'account' }), false);
});

test('applyHardGates: gates Vercel Workflow runtime endpoints with package context', () => {
  const workflow = { kind: 'slow_route', scope: 'route', route: '/.well-known/workflow/v1/step', priority: 100 };
  const other = { kind: 'slow_route', scope: 'route', route: '/api/orders', priority: 90 };
  const out = applyHardGates([workflow, other], {
    stack: { hasWorkflowPackage: true, workflowPackages: ['workflow', '@workflow/next'] },
  });
  assert.deepEqual(out.allowed, [other]);
  assert.equal(out.gated.length, 1);
  assert.match(out.gated[0].gatedReason, /Vercel Workflow runtime endpoint/);
  assert.match(out.gated[0].gatedReason, /long-running step\/flow requests are expected/);
  assert.match(out.gated[0].gatedReason, /@workflow\/next/);
});

test('gate-investigations: hard-gates /.well-known/vercel/flags before launch budget', async () => {
  const root = await mkdtemp(join(tmpdir(), 'vo-flags-gate-'));
  try {
    const signalsPath = join(root, 'signals.json');
    await writeFile(signalsPath, JSON.stringify({
      stack: { framework: 'next', hasVercelFlagsPackage: true, vercelFlagsPackages: ['@vercel/flags'] },
      project: { defaultResourceConfig: { fluid: true } },
      metrics: {
        fnDurationP95ByRoute: {
          ok: true,
          rows: [{ route: FLAGS_ENDPOINT, value: 1800 }],
        },
        requestsByRouteCache: {
          ok: true,
          rows: [{ route: FLAGS_ENDPOINT, cache_result: 'MISS', value: 3000 }],
        },
        requestsByRouteStatus: { ok: true, rows: [] },
      },
      codebase: { findings: [] },
    }), 'utf-8');
    const { stdout } = await exec('node', [GATE_SCRIPT, signalsPath, '--max-candidates=all']);
    const out = JSON.parse(stdout);
    assert.ok(!out.toLaunch.some((c) => c.route === FLAGS_ENDPOINT));
    const gated = out.gated.find((c) => c.route === FLAGS_ENDPOINT);
    assert.ok(gated, 'flags endpoint should appear in gated list');
    assert.match(gated.gatedReason, /hardGated/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('gate-investigations: hard-gates Workflow runtime endpoints before launch budget', async () => {
  const root = await mkdtemp(join(tmpdir(), 'vo-workflow-gate-'));
  try {
    const signalsPath = join(root, 'signals.json');
    await writeFile(signalsPath, JSON.stringify({
      stack: { framework: 'next', hasWorkflowPackage: true, workflowPackages: ['workflow'] },
      project: { defaultResourceConfig: { fluid: true } },
      metrics: {
        fnDurationP95ByRoute: {
          ok: true,
          rows: [
            { route: '/.well-known/workflow/v1/step', value: 12000 },
            { route: '/api/orders', value: 1800 },
          ],
        },
        requestsByRouteCache: {
          ok: true,
          rows: [
            { route: '/.well-known/workflow/v1/step', cache_result: 'MISS', value: 8000 },
            { route: '/api/orders', cache_result: 'MISS', value: 3000 },
          ],
        },
        requestsByRouteStatus: { ok: true, rows: [] },
        fnStatusByRoute: { ok: true, rows: [] },
      },
      codebase: { findings: [] },
    }), 'utf-8');
    const { stdout } = await exec('node', [GATE_SCRIPT, signalsPath, '--max-candidates=all']);
    const out = JSON.parse(stdout);
    assert.ok(!out.toLaunch.some((c) => c.route === '/.well-known/workflow/v1/step'));
    assert.ok(out.toLaunch.some((c) => c.route === '/api/orders'));
    const gated = out.gated.find((c) => c.route === '/.well-known/workflow/v1/step');
    assert.ok(gated, 'Workflow endpoint should appear in gated list');
    assert.match(gated.gatedReason, /Vercel Workflow runtime endpoint/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('detectStack: records @vercel/flags packages from package.json', async () => {
  const root = await mkdtemp(join(tmpdir(), 'vo-flags-stack-'));
  try {
    await mkdir(join(root, 'src', 'app'), { recursive: true });
    await writeFile(join(root, 'package.json'), JSON.stringify({
      dependencies: {
        next: '16.0.0',
        '@vercel/flags': '^4.0.0',
      },
      devDependencies: {
        '@vercel/flags/next': '1.0.0',
      },
    }), 'utf-8');
    const stack = await detectStack(root);
    assert.equal(stack.framework, 'next');
    assert.equal(stack.hasVercelFlagsPackage, true);
    assert.deepEqual(stack.vercelFlagsPackages, ['@vercel/flags', '@vercel/flags/next']);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('detectStack: records Workflow SDK packages from package.json', async () => {
  const root = await mkdtemp(join(tmpdir(), 'vo-workflow-stack-'));
  try {
    await mkdir(join(root, 'app'), { recursive: true });
    await writeFile(join(root, 'package.json'), JSON.stringify({
      dependencies: {
        next: '16.0.0',
        workflow: '^4.2.0',
      },
      devDependencies: {
        '@workflow/next': '4.2.0',
      },
    }), 'utf-8');
    const stack = await detectStack(root);
    assert.equal(stack.framework, 'next');
    assert.equal(stack.hasWorkflowPackage, true);
    assert.deepEqual(stack.workflowPackages, ['@workflow/next', 'workflow']);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('detectStack: recognizes Hono as unsupported framework input', async () => {
  const root = await mkdtemp(join(tmpdir(), 'vo-hono-stack-'));
  try {
    await writeFile(join(root, 'package.json'), JSON.stringify({
      dependencies: { hono: '^4.7.0' },
    }), 'utf-8');
    const stack = await detectStack(root);
    assert.equal(stack.framework, 'hono');
    assert.equal(stack.frameworkVersion, '4.7.0');
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('detectStack: records Next cacheComponents from next.config', async () => {
  const root = await mkdtemp(join(tmpdir(), 'vo-cache-components-stack-'));
  try {
    await mkdir(join(root, 'app'), { recursive: true });
    await writeFile(join(root, 'package.json'), JSON.stringify({
      dependencies: { next: '16.0.0' },
    }), 'utf-8');
    await writeFile(join(root, 'next.config.ts'), 'export default { cacheComponents: true };\n', 'utf-8');
    const stack = await detectStack(root);
    assert.equal(stack.framework, 'next');
    assert.equal(stack.cacheComponents, true);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
