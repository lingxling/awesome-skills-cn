import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const core = require('../../../tools/lib/aas-v1');
export function evidenceArgs(manifestDigest) {
  const descriptor = { schemaVersion: 1, files: [{ path: 'src/sample.js', size: 7, sha256: core.sha256('fixture') }] };
  return {
    manifestDigest,
    project: { ...descriptor, fingerprint: core.sha256(core.canonicalJson(descriptor)) },
    dimensions: core.evidence.DIMENSION_IDS.map((id) => ({ id, status: id === 'testing-quality' ? 'applicable' : 'not-applicable', capabilityIds: id === 'testing-quality' ? ['debugging'] : [] })),
    capabilities: [{ id: 'debugging', dimensionId: 'testing-quality', status: 'covered', selectedSkillIds: ['debugging-strategies'], evidence: [{ path: descriptor.files[0].path, sha256: descriptor.files[0].sha256 }] }],
  };
}
