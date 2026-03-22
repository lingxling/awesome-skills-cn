const assert = require("assert");
const fs = require("fs");
const path = require("path");

const { buildCatalog } = require("../build-catalog");

const repoRoot = path.resolve(__dirname, "..", "..", "..");
const bundlesPath = path.join(repoRoot, "data", "bundles.json");

buildCatalog();

const bundleData = JSON.parse(fs.readFileSync(bundlesPath, "utf8"));
const bundles = bundleData.bundles || {};

for (const bundleId of [
  "core-dev",
  "security-core",
  "k8s-core",
  "data-core",
  "ops-core",
  "automation-core",
  "azure-core",
  "commerce-core",
  "mobile-core",
  "seo-core",
  "docs-core",
]) {
  assert.ok(bundles[bundleId], `expected generated bundles to include ${bundleId}`);
}

assert.ok(
  bundles["automation-core"].skills.includes("workflow-automation"),
  "workflow-automation should be included in automation-core",
);
assert.ok(
  bundles["automation-core"].skills.includes("airtable-automation"),
  "airtable-automation should be included in automation-core",
);
assert.ok(
  bundles["azure-core"].skills.includes("azure-ai-openai-dotnet"),
  "azure-ai-openai-dotnet should be included in azure-core",
);
assert.ok(
  bundles["commerce-core"].skills.includes("stripe-automation") ||
    bundles["commerce-core"].skills.includes("plaid-fintech"),
  "commerce-core should include a representative commerce skill",
);
assert.ok(
  bundles["mobile-core"].skills.includes("expo-api-routes"),
  "expo-api-routes should be included in mobile-core",
);
assert.ok(
  bundles["seo-core"].skills.includes("seo-fundamentals"),
  "seo-fundamentals should be included in seo-core",
);
assert.ok(
  bundles["docs-core"].skills.includes("docx-official"),
  "docx-official should be included in docs-core",
);
