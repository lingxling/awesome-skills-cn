---
name: "security-ownership-map"
description: "分析 git 仓库以构建安全所有权拓扑（人员到文件），计算总线系数和敏感代码所有权，并导出 CSV/JSON 用于图形数据库和可视化。仅当用户明确想要基于 git 历史的安全导向所有权或总线系数分析时触发（例如：孤立的敏感代码、安全维护者、CODEOWNERS 现实检查以进行风险、敏感热点或所有权集群）。不要为一般维护者列表或非安全所有权问题触发。"
---

# 安全所有权映射

## 概述

从 git 历史构建人员和文件的双部分图，然后计算所有权风险并导出图形工件以用于 Neo4j/Gephi。还构建文件共同更改图（共享提交上的 Jaccard 相似性）以按它们如何一起移动来聚类文件，同时忽略大型、嘈杂的提交。

## 要求

- Python 3
- `networkx`（必需；默认启用社区检测）

使用以下方式安装：

```bash
pip install networkx
```

## 工作流程

1. 范围界定仓库和时间窗口（可选 `--since/--until`）。
2. 决定敏感性规则（使用默认值或提供 CSV 配置）。
3. 使用 `scripts/run_ownership_map.py` 构建所有权映射（默认启用共同更改图；使用 `--cochange-max-files` 忽略超级节点提交）。
4. 默认计算社区；graphml 输出是可选的（`--graphml`）。
5. 使用 `scripts/query_ownership.py` 查询输出以获取有界的 JSON 切片。
6. 持久化和可视化（见 `references/neo4j-import.md`）。

默认情况下，共同更改图忽略常见的"胶水"文件（锁定文件、`.github/*`、编辑器配置），以便聚类反映实际的代码移动而不是共享的基础设施编辑。使用 `--cochange-exclude` 或 `--no-default-cochange-excludes` 覆盖。默认情况下排除 Dependabot 提交；使用 `--no-default-author-excludes` 覆盖或通过 `--author-exclude-regex` 添加模式。

如果您想从共同更改聚类中排除 Linux 构建胶水（如 `Kbuild`），请传递：

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo /path/to/linux \
  --out ownership-map-out \
  --cochange-exclude "**/Kbuild"
```

## 快速开始

从仓库根目录运行：

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --since "12 months ago" \
  --emit-commits
```

默认值：排除作者身份、作者日期和合并提交。如果需要，请使用 `--identity committer`、`--date-field committer` 或 `--include-merges`。

示例（覆盖共同更改排除）：

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --cochange-exclude "**/Cargo.lock" \
  --cochange-exclude "**/.github/**" \
  --no-default-cochange-excludes
```

默认情况下计算社区。要禁用：

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --no-communities
```

## 敏感性规则

默认情况下，脚本标记常见的身份验证/加密/机密路径。通过提供 CSV 文件来覆盖：

```
# pattern,tag,weight
**/auth/**,auth,1.0
**/crypto/**,crypto,1.0
**/*.pem,secrets,1.0
```

将其与 `--sensitive-config path/to/sensitive.csv` 一起使用。

## 输出工件

`ownership-map-out/` 包含：

- `people.csv`（节点：人员）
- `files.csv`（节点：文件）
- `edges.csv`（边：接触）
- `cochange_edges.csv`（文件到文件共同更改边，带有 Jaccard 权重；使用 `--no-cochange` 省略）
- `summary.json`（安全所有权发现）
- `commits.jsonl`（可选，如果 `--emit-commits`）
- `communities.json`（默认情况下从可用的共同更改边计算；包括每个社区的 `maintainers`；使用 `--no-communities` 禁用）
- `cochange.graph.json`（NetworkX 节点-链接 JSON，带有 `community_id` + `community_maintainers`；如果没有共同更改边，则回退到 `ownership.graph.json`）
- `ownership.graphml` / `cochange.graphml`（可选，如果 `--graphml`）

`people.csv` 包括基于作者提交偏移的时区检测：`primary_tz_offset`、`primary_tz_minutes` 和 `timezone_offsets`。

## LLM 查询辅助程序

使用 `scripts/query_ownership.py` 返回小的、有界的 JSON 切片，而无需将完整图加载到上下文中。

示例：

```bash
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out people --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out person --person alice@corp --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out file --file crypto/tls
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out cochange --file crypto/tls --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section orphaned_sensitive_code
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out community --id 3
```

使用 `--community-top-owners 5`（默认）控制每个社区存储多少维护者。

## 基本安全查询

运行这些以使用有界输出回答常见的安全所有权问题：

```bash
# 孤立的敏感代码（过时 + 低总线系数）
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section orphaned_sensitive_code

# 敏感标签的隐藏所有者
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section hidden_owners

# 总线系数低的敏感热点
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section bus_factor_hotspots

# 总线系数 <= 1 的身份验证/加密文件
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag crypto --bus-factor-max 1

# 谁最常接触敏感代码
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out people --sort sensitive_touches --limit 10

# 共同更改邻居（所有权漂移的聚类提示）
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out cochange --file path/to/file --min-jaccard 0.05 --limit 20

# 社区维护者（针对集群）
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out community --id 3

# 包含文件的社区的月度维护者
python skills/skills/security-ownership-map/scripts/community_maintainers.py \
  --data-dir ownership-map-out \
  --file network/card.c \
  --since 2025-01-01 \
  --top 5

# 季度存储桶而不是月度
python skills/skills/security-ownership-map/scripts/community_maintainers.py \
  --data-dir ownership-map-out \
  --file network/card.c \
  --since 2025-01-01 \
  --bucket quarter \
  --top 5
```

注意：
- 触摸默认为一次作者提交（不是每个文件）。使用 `--touch-mode file` 计算每个文件的触摸。
- 使用 `--window-days 90` 或 `--weight recency --half-life-days 180` 平滑流失。
- 使用 `--ignore-author-regex '(bot|dependabot)'` 过滤机器人。
- 使用 `--min-share 0.1` 仅显示稳定的维护者。
- 使用 `--bucket quarter` 进行日历季度分组。
- 使用 `--identity committer` 或 `--date-field committer` 从作者归属切换。
- 使用 `--include-merges` 包括合并提交（默认情况下排除）。

### 摘要格式（默认）

使用此结构，根据需要添加字段：

```json
{
  "orphaned_sensitive_code": [
    {
      "path": "crypto/tls/handshake.rs",
      "last_security_touch": "2023-03-12T18:10:04+00:00",
      "bus_factor": 1
    }
  ],
  "hidden_owners": [
    {
      "person": "alice@corp",
      "controls": "63% of auth code"
    }
  ]
}
```

## 图持久化

当您需要将 CSV 加载到 Neo4j 时，使用 `references/neo4j-import.md`。它包括约束、导入 Cypher 和可视化提示。

## 注意事项

- `summary.json` 中的 `bus_factor_hotspots` 列出具有低总线系数的敏感文件；`orphaned_sensitive_code` 是过时子集。
- 如果 `git log` 太大，请使用 `--since` 或 `--until` 缩小。
- 将 `summary.json` 与 CODEOWNERS 进行比较以突出所有权漂移。
