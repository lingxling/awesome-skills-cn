---
name: Coinbase Automation
description: "Coinbase 自动化：通过 Coinbase CDP SDK 列出并管理加密货币钱包、账户和投资组合数据"
requires:
  mcp: [rube]
---

# Coinbase 自动化

自动化 Coinbase 操作，包括列出加密货币钱包、对钱包集合进行分页遍历以及检索投资组合数据。

**工具包文档：** [composio.dev/toolkits/coinbase](https://composio.dev/toolkits/coinbase)

---

## 设置

此技能需要连接到 `https://rube.app/mcp` 的 **Rube MCP 服务器**。

在执行任何工具之前，请确保 `coinbase` 工具包存在有效连接。如果没有活动连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起连接。

---

## 核心工作流

### 1. 列出所有钱包

检索 Coinbase 中的所有钱包，支持分页。

**工具：** `COINBASE_LIST_WALLETS`

**关键参数：**
- `limit` -- 每页结果数（1--100，默认：25）
- `order` -- 排序方式：`"asc"`（升序）或 `"desc"`（降序，默认）
- `starting_after` -- 向前分页的游标：上一页最后一个钱包的 ID
- `ending_before` -- 向后分页的游标：上一页第一个钱包的 ID

**示例（第一页）：**
```
Tool: COINBASE_LIST_WALLETS
Arguments:
  limit: 50
  order: "desc"
```

**示例（下一页）：**
```
Tool: COINBASE_LIST_WALLETS
Arguments:
  limit: 50
  order: "desc"
  starting_after: "wallet_abc123_last_id_from_prev_page"
```

---

### 2. 分页遍历所有钱包

要检索完整的钱包清单，请逐页迭代。

**步骤：**
1. 使用所需的 `limit` 和 `order` 调用 `COINBASE_LIST_WALLETS`
2. 如果响应中包含更多结果，记下返回的最后一个钱包的 ID
3. 再次调用 `COINBASE_LIST_WALLETS`，将 `starting_after` 设置为该最后一个钱包 ID
4. 重复直到不再返回结果

---

### 3. 审计钱包投资组合

检索钱包数据，用于投资组合分析和报告。

**步骤：**
1. 使用 `limit: 100` 调用 `COINBASE_LIST_WALLETS`，以最大化每页结果数
2. 从每一页收集钱包余额和元数据
3. 汇总所有页面的数据，得到完整的投资组合视图

---

### 4. 监控钱包变化

定期列出钱包，以检测新增或变更。

**步骤：**
1. 使用 `order: "desc"` 调用 `COINBASE_LIST_WALLETS`，优先获取最新的钱包
2. 与之前存储的钱包 ID 比较，以识别新条目
3. 安排定期检查以实现持续监控

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| **必须分页** | 钱包列表是分页的。请始终使用基于游标的分页（`starting_after`/`ending_before`）检查是否有更多页面。 |
| **limit 范围** | `limit` 参数接受 1--100。超出此范围的值会导致错误。默认值为 25。 |
| **基于游标的分页** | 使用钱包 ID 作为游标，而不是页码。你必须从每个响应中提取最后一个/第一个钱包 ID 来翻页。 |
| **CDP SDK 范围** | 此工具使用 Coinbase CDP SDK。可用的操作取决于连接设置期间授予的 API 密钥权限。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `COINBASE_LIST_WALLETS` | 列出加密货币钱包，支持分页 |

---

*由 [Composio](https://composio.dev) 提供支持*
