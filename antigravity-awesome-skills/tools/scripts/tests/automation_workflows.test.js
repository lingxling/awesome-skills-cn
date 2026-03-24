const assert = require("assert");
const fs = require("fs");
const path = require("path");

const repoRoot = path.resolve(__dirname, "..", "..", "..");

function readText(relativePath) {
  return fs.readFileSync(path.join(repoRoot, relativePath), "utf8");
}

const packageJson = JSON.parse(readText("package.json"));
const generatedFiles = JSON.parse(readText("tools/config/generated-files.json"));
const ciWorkflow = readText(".github/workflows/ci.yml");
const publishWorkflow = readText(".github/workflows/publish-npm.yml");
const releaseWorkflowScript = readText("tools/scripts/release_workflow.js");
const hygieneWorkflowPath = path.join(repoRoot, ".github", "workflows", "repo-hygiene.yml");

assert.ok(
  packageJson.scripts["sync:release-state"],
  "package.json should expose a deterministic release-state sync command",
);
assert.ok(
  packageJson.scripts["check:warning-budget"],
  "package.json should expose a warning-budget guardrail command",
);
assert.ok(
  packageJson.scripts["audit:maintainer"],
  "package.json should expose a maintainer audit command",
);
assert.ok(
  packageJson.scripts["sync:web-assets"],
  "package.json should expose a web-asset sync command for tracked web artifacts",
);
assert.match(
  packageJson.scripts["sync:release-state"],
  /sync:web-assets/,
  "sync:release-state should refresh tracked web assets before auditing release drift",
);
assert.match(
  packageJson.scripts["sync:release-state"],
  /check:warning-budget/,
  "sync:release-state should enforce the frozen validation warning budget",
);
assert.match(
  packageJson.scripts["sync:repo-state"],
  /sync:web-assets/,
  "sync:repo-state should refresh tracked web assets before maintainer audits",
);
assert.match(
  packageJson.scripts["sync:repo-state"],
  /check:warning-budget/,
  "sync:repo-state should enforce the frozen validation warning budget",
);
assert.strictEqual(
  packageJson.scripts["app:install"],
  "cd apps/web-app && npm ci",
  "app:install should use npm ci for deterministic web-app installs",
);

for (const filePath of [
  "apps/web-app/public/sitemap.xml",
  "apps/web-app/public/skills.json.backup",
]) {
  assert.ok(
    generatedFiles.derivedFiles.includes(filePath),
    `generated-files derivedFiles should include ${filePath}`,
  );
}

for (const filePath of [
  "README.md",
  "package.json",
  "docs/users/getting-started.md",
  "docs/users/bundles.md",
  "docs/users/claude-code-skills.md",
  "docs/users/gemini-cli-skills.md",
  "docs/users/usage.md",
  "docs/users/visual-guide.md",
  "docs/users/kiro-integration.md",
  "docs/maintainers/repo-growth-seo.md",
  "docs/maintainers/skills-update-guide.md",
  "docs/integrations/jetski-cortex.md",
  "docs/integrations/jetski-gemini-loader/README.md",
]) {
  assert.ok(
    generatedFiles.mixedFiles.includes(filePath),
    `generated-files mixedFiles should include ${filePath}`,
  );
}

assert.match(
  ciWorkflow,
  /- name: Run repo-state sync[\s\S]*?run: npm run sync:repo-state/,
  "main CI should use the unified repo-state sync command",
);
assert.match(
  ciWorkflow,
  /GH_TOKEN: \$\{\{ github\.token \}\}/,
  "main CI should provide GH_TOKEN for contributor synchronization",
);
assert.doesNotMatch(
  ciWorkflow,
  /^      - name: Generate index$/m,
  "main CI should not keep the old standalone Generate index step",
);
assert.doesNotMatch(
  ciWorkflow,
  /^      - name: Update README$/m,
  "main CI should not keep the old standalone Update README step",
);
assert.doesNotMatch(
  ciWorkflow,
  /^      - name: Build catalog$/m,
  "main CI should not keep the old standalone Build catalog step",
);

assert.ok(fs.existsSync(hygieneWorkflowPath), "repo hygiene workflow should exist");

const hygieneWorkflow = readText(".github/workflows/repo-hygiene.yml");
assert.match(hygieneWorkflow, /^on:\n  workflow_dispatch:\n  schedule:/m, "repo hygiene workflow should support schedule and manual runs");
assert.match(
  hygieneWorkflow,
  /GH_TOKEN: \$\{\{ github\.token \}\}/,
  "repo hygiene workflow should provide GH_TOKEN for gh-based contributor sync",
);
assert.match(
  hygieneWorkflow,
  /run: npm run sync:repo-state/,
  "repo hygiene workflow should run the unified repo-state sync command",
);
assert.match(
  hygieneWorkflow,
  /generated_files\.js --shell --include-mixed/,
  "repo hygiene workflow should stage the mixed generated files contract",
);

assert.match(publishWorkflow, /run: npm ci/, "npm publish workflow should install dependencies");
assert.match(
  publishWorkflow,
  /run: npm run app:install/,
  "npm publish workflow should install web-app dependencies before building",
);
assert.match(
  publishWorkflow,
  /run: npm run sync:release-state/,
  "npm publish workflow should verify canonical release artifacts",
);
assert.match(
  publishWorkflow,
  /run: git diff --exit-code/,
  "npm publish workflow should fail if canonical sync would leave release drift",
);
assert.match(publishWorkflow, /run: npm run test/, "npm publish workflow should run tests before publish");
assert.match(publishWorkflow, /run: npm run app:build/, "npm publish workflow should build the app before publish");
assert.match(
  releaseWorkflowScript,
  /runCommand\("npm", \["run", "app:install"\], projectRoot\);[\s\S]*runCommand\("npm", \["run", "app:build"\], projectRoot\);/,
  "release workflow should install web-app dependencies before building the app",
);
assert.match(
  publishWorkflow,
  /npm pack --dry-run --json/,
  "npm publish workflow should dry-run package creation before publishing",
);
