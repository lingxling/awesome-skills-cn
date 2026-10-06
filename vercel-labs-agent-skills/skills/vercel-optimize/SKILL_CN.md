---
name: vercel-optimize
description: "用于已部署项目的 Vercel 成本与性能优化，尤其是 Next.js、SvelteKit、Nuxt，以及有限支持的 Astro 应用。先收集 Vercel 指标、用量、项目配置和代码扫描结果；只调查有指标支撑的候选项；基于已验证的文件和感知版本的 Vercel/框架文档，产出经过排序的建议。在以下请求时触发：降低 Vercel 账单、缓慢或昂贵的路由、缓存机会、Function Invocations、Build Minutes、Fast Data Transfer、Core Web Vitals、Bot Management、Fluid compute 或成本明细。"
metadata:
  version: "1.2.0"
---

# Vercel Optimize

执行一次以可观测性为先的 Vercel 优化审计。在 `signals.json` 存在、且确定性门控指向某个路由、文件或项目设置之前，不要检查源文件。

核心原则：如有任何规则不清楚，请阅读 [references/doctrine.md](references/doctrine.md)。

- 指标优先。建议从 Vercel 生产环境信号出发，而不是对整个仓库进行 grep。
- 确定性门控。由 `scripts/gate-investigations.mjs` 决定哪些内容值得调查。
- 范围受候选项约束。只读取候选项指定的文件或路由本地的导入链。
- 感知版本的引用。只使用 `references/docs-library.json`；无效或版本不匹配的引用会被剔除。
- 面向客户的文案。在撰写报告文本或聊天输出之前，阅读 [references/voice.md](references/voice.md)。

## 前提条件

- Vercel CLI v53+，具备 `vercel metrics`、`vercel usage`、`vercel contract` 和 `vercel api`。
- 已认证的 CLI 会话：`vercel login`。
- 已链接的应用目录：`vercel link`。`VERCEL_PROJECT_ID` 可以帮助解析项目配置，但 `vercel metrics` 仍然需要目录链接。链接或环境必须包含目标项目的 org/team/user 作用域，以便收集器能解析出 CLI 安全的 `--scope`，并使 `vercel metrics`、`vercel usage` 和 `vercel contract` 指向同一账户。
- Node.js 20+。
- Observability Plus，用于路由级、有指标支撑的建议。

切勿在 shell 命令中放入认证令牌。不要在可能被回显到聊天中的命令里输入 `VERCEL_TOKEN=...`、`--token ...` 或 `Authorization: Bearer ...`。

## 框架支持

预检会读取 `package.json`，并在指标扇出之前设定预期。

| 框架 | 状态 | 说明 |
|---|---|---|
| Next.js App Router | 支持 | 最强的路由映射、扫描器、操作手册和引用 |
| Next.js Pages Router | 支持 | 检测到时限定于 Pages Router 的惯用写法 |
| SvelteKit | 支持 | 针对 `src/routes` 文件的路由映射以及 SvelteKit 扫描器 |
| Nuxt | 支持 | 路由映射加通用/平台检查；框架特定的建议较少 |
| Astro | 有限支持 | 路由映射加通用检查；框架特定的建议较少 |
| Hono / Remix / 未知 | 默认阻止 | 仅在用户接受有限的平台/纯代码审计时才继续 |

如果不受支持，在扫描或门控之前停下并询问：

```text
This project uses <framework>. Vercel Optimize supports metric-backed code recommendations for Next.js, SvelteKit, and Nuxt. Astro support is limited. For <framework>, I can still run a limited platform/scanner audit, but route-level Vercel metrics may not map back to source files.

Do you want me to continue with the limited audit, or stop here?
```

如果用户选择继续，使用 `--continue-unsupported-framework` 重新运行收集。

## 运行目录

每次审计都使用一个全新的运行目录。不要在多次运行之间复用简报、子智能体输出或报告。

```bash
RUN_DIR="$(mktemp -d -t vercel-optimize-XXXXXX)"
```

## 流水线

### 1. 收集、扫描并合并信号

在已链接的应用目录中运行，或在脚本支持时传入 `--cwd`。将 stdout 的 JSON 与 stderr 日志分开。不要合并输出流。

```bash
node scripts/collect-signals.mjs [projectId] > "$RUN_DIR/vercel-signals.json" 2> "$RUN_DIR/collect.stderr"
node -e 'JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"))' "$RUN_DIR/vercel-signals.json"

node scripts/scan-codebase.mjs <repo-root> > "$RUN_DIR/codebase.json"
node scripts/merge-signals.mjs "$RUN_DIR/vercel-signals.json" "$RUN_DIR/codebase.json" --out "$RUN_DIR/signals.json"
```

收集细节、schema、指标 ID 和降级行为见 [references/data-collection.md](references/data-collection.md)。指标注册表是 [lib/queries.mjs](lib/queries.mjs)；所有查询都保持在共享的 14 天时间窗口内。

`collect-signals.mjs` 会将已链接项目的所有者解析为 `commandScope.cliScope`，并在检查 Observability Plus 之前验证所解析的账户能够读取所解析的项目。下游脚本会对每个接受 `--scope` 的 Vercel CLI 命令复用该作用域。不要在没有相同作用域的情况下手动运行 `vercel usage`、`vercel metrics` 或 `vercel contract`；未指定作用域的用量可能报告的是用户个人组织的数据，而路由指标却来自团队项目。

如果项目或作用域的解析存在歧义，停下来询问用户希望审计哪个 Vercel 项目以及团队/个人作用域。不要根据当前 `vercel whoami` 的团队推断目标作用域；在链接、`.vercel/repo.json` 中的精确项目匹配，或 `VERCEL_PROJECT_ID` + `VERCEL_ORG_ID` 确定目标账户之前，不要进行指标、用量或合同信息的收集。

遇到 `PROJECT_SCOPE_UNRESOLVED`、`SCOPE_UNRESOLVED` 或 `PROJECT_SCOPE_MISMATCH` 时使用以下提示：

```text
I can't safely identify the Vercel project and account for this audit yet.

Please confirm the Vercel project name or ID and the team slug/name, or tell me it's under your personal account. Once confirmed, I'll relink or rerun collection against that exact scope before checking metrics.
```

### 1.1 遇到阻塞项时停止

在门控之前检查阻塞项：

```bash
jq '{frameworkSupportBlocker, observabilityPlus, observabilityPlusUsable, observabilityPlusBlocker, observabilityPlusBlockerDetail}' "$RUN_DIR/signals.json"
```

必需的操作：

- `frameworkSupportBlocker === "unsupported_framework"`：使用上面的不支持框架提示。
- `PROJECT_SCOPE_UNRESOLVED`、`SCOPE_UNRESOLVED` 或 `PROJECT_SCOPE_MISMATCH`：停下来询问用户希望审计哪个 Vercel 项目以及团队/个人作用域。对于团队项目，在执行 `vercel link --yes --project <project-name-or-id> --team <team-slug>` 之后重新运行；对于个人项目，在目标用户账户下完成链接，或同时设置 `VERCEL_PROJECT_ID` 和 `VERCEL_ORG_ID` 之后重新运行。
- `observabilityPlusBlocker === null`：继续。
- `no_traffic`：告诉用户路由指标稀疏；仅在用户接受有限输出时才继续。
- `payment_required` 或 `no_oplus_probe`：原样呈现 [references/observability-plus.md](references/observability-plus.md) 并询问。
- `project_disabled`：告诉用户为该项目启用 Observability Plus，或接受有限审计。
- `daily_quota_exceeded`：停止，并告诉用户 Observability 查询配额已用尽；在下一个 UTC 午夜重置后重试，或询问是否继续进行有限的纯代码审计。
- `not_linked`：链接应用目录，然后重新运行第 1 步。如果已知应用路径和项目：

```bash
vercel link --yes --project <project-name-or-id> --cwd <app-dir>
# 已知时添加 --team <team-id-or-slug>
```

- `forbidden` 或 `project_not_found`：修复认证/团队作用域。不要推销 Observability Plus。
- `all_failed_other`：显示原始错误代码，并询问是否以有限的纯代码模式继续。

不要静默回退到纯代码模式。如果用户接受有限审计，使用以下命令重新运行收集：

```bash
node scripts/collect-signals.mjs [projectId] --continue-without-observability > "$RUN_DIR/vercel-signals.json" 2> "$RUN_DIR/collect.stderr"
```

然后再次扫描并合并。

### 2. 门控候选项

```bash
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" > "$RUN_DIR/gate.json"
```

输出结构：

- `toLaunch`：需要调查的代码范围候选项。
- `platform`：项目/账户范围的建议。
- `gated`：被跳过、已覆盖或被取消资格的候选项，它们仍必须出现在报告中。
- `budget`：候选项预算和选择模式。

默认预算为 6 个代码范围候选项，并带有多样性护栏。如需扩展：

```bash
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" --max-candidates 12 > "$RUN_DIR/gate.json"
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" --max-candidates all > "$RUN_DIR/gate.json"
```

生成的候选项文档：[references/candidates.md](references/candidates.md)。

### 2.1 必要时询问审计范围

在深入调查之前，运行：

```bash
node scripts/budget-summary.mjs "$RUN_DIR/gate.json" --format json > "$RUN_DIR/budget-summary.json"
```

如果 `shouldAsk` 为 false，继续。

如果 `shouldAsk` 为 true：

1. 完全按返回内容打印 `exactChatMessage.body`。不要概括、截断、重新排序或改写。
2. 然后在宿主支持结构化问题时，使用 `questionPayload` 提出 `questionText`。
3. 如果用户选择了不同的数量，使用 `--max-candidates <choice>` 重新运行门控。

切勿将较长的预览放入问题字段中。预览和问题是两个独立的呈现界面。

### 2.2 深入调查并核对

```bash
node scripts/deep-dive.mjs "$RUN_DIR/signals.json" "$RUN_DIR/gate.json" --cwd <project-dir> > "$RUN_DIR/investigation-evidence.json"

node scripts/reconcile-candidates.mjs "$RUN_DIR/investigation-evidence.json" \
  --gate "$RUN_DIR/gate.json" \
  --out "$RUN_DIR/reconciled-investigation.json"
```

`--cwd` 必须是已链接的项目目录，这样 `deep-dive.mjs` 才能验证相同的项目链接，并在后续任何 `vercel metrics` 调用中复用 `signals.json.commandScope.cliScope`。

在任何源代码调查之前，核对步骤会确定性地将已被证伪的候选项转换为观察结论：

- `metric_mismatch`
- `error_storm`
- `deployment_regression`
- `scanner_only_no_metric`

### 2.3 生成简报并调查

列出工作项：

```bash
node scripts/prepare-investigation-brief.mjs "$RUN_DIR/signals.json" "$RUN_DIR/reconciled-investigation.json" --list > "$RUN_DIR/briefs-manifest.json"
```

为 `briefs-manifest.json.briefs` 中的每个条目生成一份简报。`group` 可以是 `toLaunch` 或 `platform`；不要只生成 `toLaunch` 简报。

```bash
mkdir -p "$RUN_DIR/briefs" "$RUN_DIR/sub-agent-outputs"
node scripts/prepare-investigation-brief.mjs "$RUN_DIR/signals.json" "$RUN_DIR/reconciled-investigation.json" \
  --group <brief.group> --index <brief.index> --out "$RUN_DIR/briefs/<brief.group>-<brief.index>.md"
```

使用 `briefs-manifest.json.briefs[].label` 作为可见的工作者名称，例如 `Low cache-hit route on /docs/llm-digest/[...slug]`，而不是 `toLaunch-7`。

扇出规则：

- 1-2 份简报：内联调查。
- 3 份及以上简报：在宿主支持时，每份简报启动一个子智能体。
- 不支持子智能体的宿主：内联串行运行。

子智能体契约：

- 简报就是完整的提示。
- 只读取简报中列出的文件，必要时加上路由本地的导入。
- 按照 [references/recommendations.md](references/recommendations.md) 输出一条 JSON 建议或一条 JSON 无需更改的结论。
- 不要引用所提供引用子集之外的 URL。
- 不要推荐在检测到的版本中不可用的框架特性。

如果子智能体需要对整个仓库进行 grep，说明该候选项有缺陷；应丢弃或弃权，而不是扩大范围。

### 2.4 收集输出

将每个原始调查结果保存到 `$RUN_DIR/sub-agent-outputs/`，然后收集：

```bash
node scripts/collect-sub-agent-outputs.mjs \
  --manifest "$RUN_DIR/briefs-manifest.json" \
  --out "$RUN_DIR/recommendations.json" \
  "$RUN_DIR/sub-agent-outputs/"
```

收集器会提取 JSON、在前面加上预先解析的记录、强制使用清单顺序，并在 `candidateRef` 值缺失、重复、未知或不匹配时失败。

### 3. 验证建议

```bash
node scripts/verify-and-regen.mjs "$RUN_DIR/recommendations.json" \
  --signals "$RUN_DIR/signals.json" \
  --repo-root <project-dir> \
  --out "$RUN_DIR/verify.json"
```

该脚本会提取论断，验证文件/引用/版本适配性，对质量进行评分，应用清理器，输出 `verifiedRecommendations`、`withheldRecommendations`、`renderableRecommendations`，并为失败或不安全的建议创建 `regenPlan`。

建议 schema、写作规则、清理器顺序和评分规则：[references/recommendations.md](references/recommendations.md)。验证规则：[references/verification.md](references/verification.md)。

对于每个 `regenPlan` 条目，使用相同的简报重新运行，并附加一个 `Previous attempt failed these checks` 部分，列出 `topFailures`。只有在验证结果改善且没有删减引用的情况下，才保留重新生成的输出。

### 4. 渲染报告和最终消息

```bash
node scripts/render-report.mjs "$RUN_DIR/verify.json" "$RUN_DIR/gate.json" "$RUN_DIR/signals.json" \
  --project <name> \
  --out "$RUN_DIR/report.md" \
  --message-out "$RUN_DIR/final-message.json"
```

仅在开发本技能时使用 `--debug-out "$RUN_DIR/debug.json"`。面向客户的 Markdown 和聊天输出不得暴露 `passRate`、`quality`、清理器轨迹、原始子智能体名称或其他实现字段。

渲染完成后，原样打印 `final-message.json.body` 并停止。不要添加要点、调试说明、原始计数、子智能体摘要或额外解释。渲染时的去重、平台上限和硬性安全剔除可能会改变客户可见的数量，因此切勿根据原始 `verify.json` 进行概括。

报告结构和影响表述：[references/scoring.md](references/scoring.md)。

## 建议规则

每条建议都必须：

- 可追溯到已启动的候选项、平台候选项、预先解析的观察结论，或已验证的与流量无关的扫描器发现。
- 包含来自 `signals.json` 或 `evidence.deepDive` 的观测指标证据。
- 涉及代码时，引用已验证的文件并附带行号。
- 至少包含一条适用于检测到的框架/版本的允许引用。
- 使用精确的观测性能数值。
- 只使用成本量级的措辞；切勿给出面向客户的 `$N` 节省金额。
- 不要为 Vercel Workflow 运行时端点（`/.well-known/workflow/v1/*`）推荐缩短持续时间。这些是为持久化步骤/流程执行而生成的编排路由，应在调查之前被硬性门控排除。
- Workflow 相关建议必须指明所更改的边界。有效示例：将持久化工作入队并返回运行 ID 而不是等待完成、修复流的重放/关闭/锁问题，或减少经验证的多余 Workflow Steps/Storage。不要根据 Workflow 端点的挂钟时长推断成本节省。
- 对于流式传输、SSE、可恢复聊天或其他有意长时间存活的路由，不要将函数的挂钟时长本身视为问题。需要有以下证据：可避免的首字节前工作、较高的活跃 CPU、重复调用，或可以移出用户可见路径的响应后工作。
- 推荐缓存时，指明具体的缓存策略。
- 除非有证据证明可以安全缓存，否则保持不安全的响应为动态：对认证敏感的路径、错误、回退响应、缺失内容、无效请求、随地理位置/设备变化的输出，以及未加版本的动态 URL。

对于 `signals.project` 中已存在的事实，切勿建议"验证 X 已开启"，包括 Fluid compute 状态、内存档位、区域、函数内并发和超时。

## 扫描器规则

扫描器发现只是补充信息。丢弃标注为 `COLD-PATH` 或 `NO-ROUTE-MAPPING` 的发现，除非该扫描器声明了 `metadata.trafficIndependent === true`。

与流量无关的示例：middleware matcher、source maps、React Compiler 配置、构建设置。路由本地的缓存或数据获取模式需要路由级的流量证据。

扫描器文档：[references/scanner-patterns.md](references/scanner-patterns.md)。

## 最终面向客户的用语

使用：

- `recommendations ready`
- `observations from investigation`
- `investigated, no change recommended`
- `not investigated in this run`

避免使用：

- `sub-agent`
- `abstention`
- `passRate`
- `quality score`
- `gate`
- `LLM`

## 失败文案

使用以下消息，不要添加销售文案或流程细节。

**过去 14 天内没有流量：**

> 该项目在过去 14 天内没有有意义的流量，因此路由级指标较为稀疏。我仍然可以检查与流量无关的扫描器发现和项目设置，但在流量积累之前无法对路由修复进行排序。

**路由级指标不可用：**

> 使用 [references/observability-plus.md](references/observability-plus.md) 中的原文选择模板。不要静默回退到纯代码模式；提供两条路径供选择：启用 Observability Plus 并重新运行有指标支撑的审计，或接受有限的纯代码运行。

**项目未链接：**

> 此工作树未链接到 Vercel 项目。运行 `vercel link --yes --project <project-name-or-id> --cwd <app-dir>` 并重新运行审计。如果已知团队，添加 `--team <team-id-or-slug>`。

**大多数路由到文件的映射失败：**

> 路由清单匹配到的路由少于我们在可观测性数据中看到的路由的一半。这在使用自定义路由的 monorepo 中很常见。我已展示能够匹配的部分；其余部分出现在"本次运行未调查"部分中。
