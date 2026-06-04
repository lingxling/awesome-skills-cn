// Plan inference source order: Vercel account billing.plan first, then
// commitment-category fallback, then usage>$0 legacy fallback.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { extractBillingPlan, filterUsageByProject, inferPlan } from '../../../skills/vercel-optimize/lib/vercel.mjs';

test('extractBillingPlan: reads team billing.plan from Vercel API response', () => {
  assert.deepEqual(
    extractBillingPlan({ billing: { plan: 'enterprise' } }),
    { plan: 'enterprise', rawPlan: 'enterprise' },
  );
});

test('extractBillingPlan: reads user billing.plan from /v2/user response wrapper', () => {
  assert.deepEqual(
    extractBillingPlan({ user: { billing: { plan: 'hobby' } } }),
    { plan: 'hobby', rawPlan: 'hobby' },
  );
});

test('extractBillingPlan: ignores unknown plan strings', () => {
  assert.equal(extractBillingPlan({ billing: { plan: 'custom' } }), null);
});

test('inferPlan: account billing.plan=hobby is exact', () => {
  const r = inferPlan({ commitments: [{ commitmentCategory: 'Spend' }] }, {
    accountPlan: { plan: 'hobby', source: 'user.billing.plan' },
    usageTotalCost: 100,
  });
  assert.equal(r.plan, 'hobby');
  assert.match(r.reason, /user\.billing\.plan=hobby/);
});

test('inferPlan: account billing.plan=pro is exact', () => {
  const r = inferPlan({ commitments: [] }, {
    accountPlan: { plan: 'pro', source: 'team.billing.plan' },
    usageTotalCost: 0,
  });
  assert.equal(r.plan, 'pro');
  assert.match(r.reason, /team\.billing\.plan=pro/);
});

test('inferPlan: account billing.plan=enterprise is exact', () => {
  const r = inferPlan({ commitments: [{ commitmentCategory: 'Spend' }] }, {
    accountPlan: { plan: 'enterprise', source: 'team.billing.plan' },
  });
  assert.equal(r.plan, 'enterprise');
  assert.match(r.reason, /team\.billing\.plan=enterprise/);
});

test('inferPlan: string account plan is accepted for callers with a direct plan value', () => {
  const r = inferPlan({ commitments: [] }, { accountPlan: 'hobby' });
  assert.equal(r.plan, 'hobby');
  assert.match(r.reason, /billing\.plan=hobby/);
});

test('inferPlan: unknown account plan falls back to contract category', () => {
  const r = inferPlan({ commitments: [{ commitmentCategory: 'Usage' }] }, {
    accountPlan: { plan: 'unknown', reason: 'team.billing.plan unavailable' },
  });
  assert.equal(r.plan, 'enterprise');
  assert.match(r.reason, /category=Usage/);
});

test('inferPlan: commitment category=Spend → Pro', () => {
  const r = inferPlan({ commitments: [{ category: 'Spend' }] });
  assert.equal(r.plan, 'pro');
  assert.match(r.reason, /category=Spend/);
});

test('inferPlan: commitment category=Usage → Enterprise', () => {
  const r = inferPlan({ commitments: [{ category: 'Usage' }] });
  assert.equal(r.plan, 'enterprise');
  assert.match(r.reason, /category=Usage/);
});

test('inferPlan: commitment with alternate field names (commitmentCategory)', () => {
  const r = inferPlan({ commitments: [{ commitmentCategory: 'Spend' }] });
  assert.equal(r.plan, 'pro');
});

test('inferPlan: commitments=[] + usage > $0 → Pro pay-as-you-go', () => {
  // Live failure reproduced: contract.commitments=[] but the team had billed usage.
  const r = inferPlan({ commitments: [] }, { usageTotalCost: 1800 });
  assert.equal(r.plan, 'pro');
  assert.match(r.reason, /pay-as-you-go/);
  assert.match(r.reason, /1800/);
});

test('inferPlan: commitments=[] + usage=$0 → uncertain (Hobby or unbilled Pro)', () => {
  const r = inferPlan({ commitments: [] }, { usageTotalCost: 0 });
  assert.equal(r.plan, 'uncertain');
  assert.match(r.reason, /could be Hobby/);
});

test('inferPlan: commitments=[] + usage unavailable → uncertain (lower fidelity)', () => {
  const r = inferPlan({ commitments: [] }, { usageTotalCost: null });
  assert.equal(r.plan, 'uncertain');
  assert.match(r.reason, /usage unavailable/);
});

test('inferPlan: no opts arg backwards-compat → uncertain when commitments=[]', () => {
  const r = inferPlan({ commitments: [] });
  assert.equal(r.plan, 'uncertain');
});

test('inferPlan: usage fallback does NOT override an explicit commitment', () => {
  const r = inferPlan(
    { commitments: [{ category: 'Usage' }] },
    { usageTotalCost: 1000 },
  );
  assert.equal(r.plan, 'enterprise', 'commitment category wins over usage fallback');
});

test('inferPlan: unknown commitment category → uncertain (with the category in reason)', () => {
  const r = inferPlan({ commitments: [{ category: 'Mystery' }] });
  assert.equal(r.plan, 'uncertain');
  assert.match(r.reason, /Mystery/);
});

test('inferPlan: null/undefined contract → uncertain', () => {
  assert.equal(inferPlan(null).plan, 'uncertain');
  assert.equal(inferPlan(undefined).plan, 'uncertain');
});

test('filterUsageByProject: supports current CLI --group-by project shape', () => {
  const usage = {
    groupBy: {
      dimension: 'project',
      data: [
        {
          name: 'other-app',
          services: [{ name: 'Edge Requests', billedCost: 10 }],
          totals: { billedCost: 10 },
        },
        {
          name: 'fixture-site',
          services: [{ name: 'Function Invocations', billedCost: 42 }],
          totals: { billedCost: 42 },
        },
      ],
    },
    services: [{ name: 'Function Invocations', billedCost: 52 }],
    totals: { billedCost: 52 },
  };

  const r = filterUsageByProject(usage, 'prj_123', 'fixture-site');
  assert.equal(r.matched, true);
  assert.equal(r.filtered.totals.billedCost, 42);
  assert.deepEqual(r.filtered.services, [{ name: 'Function Invocations', billedCost: 42 }]);
  assert.equal(r.filtered.groupBy.data.length, 1);
});
