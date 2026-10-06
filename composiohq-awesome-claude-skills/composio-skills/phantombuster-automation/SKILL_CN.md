---
name: PhantomBuster Automation
description: "通过 Composio 在 PhantomBuster 云平台上自动化潜在客户生成、网页抓取和社交媒体数据提取工作流"
requires:
  mcp:
    - rube
---

# PhantomBuster Automation

自动化基于云的数据提取和潜在客户生成——管理代理（agent）和脚本、监控组织资源和使用情况、追踪容器（container）执行情况，以及解决验证码挑战——全部通过 Composio MCP 集成编排完成。

**工具包文档：** [composio.dev/toolkits/phantombuster](https://composio.dev/toolkits/phantombuster)

---

## 设置

1. 通过 Composio MCP 服务器（`https://rube.app/mcp`）连接你的 PhantomBuster 账户
2. 如果没有活动连接，代理会提示你一个身份验证链接
3. 连接成功后，所有 `PHANTOMBUSTER_*` 工具即可供执行

---

## 核心工作流

### 1. 列出所有代理
获取与你的账户或组织相关联的每个代理，以清点自动化工作流。

**工具：** `PHANTOMBUSTER_GET_AGENTS_FETCH_ALL`

```
不需要参数——返回所有代理及其 ID 和元数据。
请先验证你的 API 密钥。
```

获取容器或监控特定自动化时，使用此响应中返回的代理 ID。

---

### 2. 列出所有脚本
检索你账户下所有可用的脚本（不含代码正文），用于脚本管理。

**工具：** `PHANTOMBUSTER_GET_SCRIPTS_FETCH_ALL`

```
不需要参数——仅返回脚本元数据，不含源代码。
```

---

### 3. 监控组织资源和配额
检查你组织当前的资源使用情况和配额限制，以规划自动化容量。

**工具：** `PHANTOMBUSTER_GET_ORGS_FETCH_RESOURCES`

```
不需要参数——返回资源分配和当前使用指标。
```

---

### 4. 检索代理容器
获取特定代理的所有执行容器，以监控运行历史和状态。

**工具：** `PHANTOMBUSTER_GET_CONTAINERS_FETCH_ALL`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `agentId` | string | 是 | 来自 `PHANTOMBUSTER_GET_AGENTS_FETCH_ALL` 的代理 ID |

---

### 5. 导出代理使用情况报告
下载包含你组织所有代理运行统计数据的 CSV 报告。

**工具：** `PHANTOMBUSTER_GET_ORGS_EXPORT_AGENT_USAGE`

```
返回一个可下载的 CSV 文件，包含全面的代理执行统计数据。
```

---

### 6. 解决 hCaptcha 挑战
为需要解决验证码的自动化表单提交或抓取流程获取有效的 hCaptcha 令牌。

**工具：** `PHANTOMBUSTER_POST_HCAPTCHA`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `siteKey` | string | 是 | hCaptcha 控件的公开站点密钥 |
| `pageUrl` | string | 是 | 包含验证码的页面完整 URL |
| `proxy` | string | 否 | 代理 URL（例如 `http://user:pass@host:port`） |
| `userAgent` | string | 否 | 要模拟的自定义 User-Agent 字符串 |

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|---------|
| **容器查询需要代理 ID** | `PHANTOMBUSTER_GET_CONTAINERS_FETCH_ALL` 需要一个有效的 `agentId`——请始终先通过 `PHANTOMBUSTER_GET_AGENTS_FETCH_ALL` 获取 |
| **API 密钥认证** | 所有 PhantomBuster 工具都需要有效的 API 密钥连接——调用任何工具前请先验证身份认证 |
| **不包含脚本正文** | `PHANTOMBUSTER_GET_SCRIPTS_FETCH_ALL` 仅返回元数据，不返回源代码 |
| **组织范围** | 资源和使用情况工具在与你 API 密钥绑定的组织级别运行——请确保定位到正确的组织 |
| **分支操作** | `PHANTOMBUSTER_GET_BRANCHES_FETCH_ALL` 和 `PHANTOMBUSTER_GET_BRANCHES_DIFF` 用于高级脚本版本控制——使用它们在部署前评估预发布与正式发布之间的差异 |

---

## 快速参考

| 工具 Slug | 用途 |
|-----------|---------|
| `PHANTOMBUSTER_GET_AGENTS_FETCH_ALL` | 列出你账户中的所有代理 |
| `PHANTOMBUSTER_GET_SCRIPTS_FETCH_ALL` | 列出所有脚本（仅元数据） |
| `PHANTOMBUSTER_GET_ORGS_FETCH_RESOURCES` | 检查组织的资源使用情况和配额 |
| `PHANTOMBUSTER_GET_CONTAINERS_FETCH_ALL` | 获取特定代理的所有容器 |
| `PHANTOMBUSTER_GET_ORGS_EXPORT_AGENT_USAGE` | 以 CSV 格式导出代理使用情况 |
| `PHANTOMBUSTER_POST_HCAPTCHA` | 为自动化解决 hCaptcha 挑战 |
| `PHANTOMBUSTER_GET_ORGS_FETCH` | 获取组织详情 |
| `PHANTOMBUSTER_GET_ORGS_FETCH_AGENT_GROUPS` | 获取代理分组及排序 |
| `PHANTOMBUSTER_GET_BRANCHES_FETCH_ALL` | 列出所有脚本分支 |
| `PHANTOMBUSTER_GET_BRANCHES_DIFF` | 比较预发布与正式发布分支 |

---

*由 [Composio](https://composio.dev) 提供支持*
