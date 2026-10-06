---
name: Contentful Automation
description: "在 Contentful 中自动化无头 CMS 操作 -- 通过 Composio Contentful 集成列出空间、检索空间元数据以及更新空间配置。"
requires:
  mcp:
    - rube
---

# Contentful 自动化

直接在 Claude Code 中管理你的 **Contentful** 无头 CMS 空间。无需离开终端，即可列出空间、检索元数据并更新空间配置。

**工具包文档:** [composio.dev/toolkits/contentful](https://composio.dev/toolkits/contentful)

---

## 设置

1. 将 Composio MCP 服务器添加到你的配置中：
   ```
   https://rube.app/mcp
   ```
2. 在提示时连接你的 Contentful 账户。代理会提供一个认证链接。请确保你的访问令牌具有空间管理权限范围。

---

## 核心工作流

### 1. 列出所有空间

发现已认证账户可访问的所有 Contentful 空间。这通常是第一个操作，因为大多数其他操作都需要 `space_id`。

**工具:** `CONTENTFUL_LIST_SPACES`

关键参数：
- `limit` (1-1000) -- 返回的空间最大数量（默认值：100）
- `skip` -- 分页时要跳过的空间数量
- `order` -- 按字段排序，例如 `sys.createdAt` 或 `-sys.createdAt`（降序）

示例提示：*"List all my Contentful spaces"*

---

### 2. 获取空间详情

检索特定空间的详细元数据，包括其当前的 `sys.version`，更新时需要用到该值。

**工具:** `CONTENTFUL_GET_SPACE`

关键参数：
- `space_id`（必填） -- 要检索的空间 ID（字母数字，1-64 个字符）

示例提示：*"Get details for Contentful space abc123def"*

---

### 3. 更新空间名称

更新特定空间的名称。需要当前版本号以进行乐观锁定，防止并发修改冲突。

**工具:** `CONTENTFUL_UPDATE_SPACE`

关键参数：
- `space_id`（必填） -- 要更新的空间 ID
- `name`（必填） -- 空间的新名称（1-255 个字符）
- `version`（必填） -- 来自 `sys.version` 的当前空间版本（必须大于 0）

示例提示：*"Rename Contentful space abc123def to 'Production Content Hub'"*

---

### 4. 审计空间清单

结合空间列表和详情检索，审计你所在组织的 Contentful 空间。

**工具:** `CONTENTFUL_LIST_SPACES` 然后 `CONTENTFUL_GET_SPACE`

工作流：
1. 列出所有空间以获取 ID 和名称
2. 获取每个空间的详情，以获得版本信息、创建日期和元数据

示例提示：*"Audit all Contentful spaces -- list them with their creation dates and current versions"*

---

## 已知陷阱

- **更新时的版本冲突：** `CONTENTFUL_UPDATE_SPACE` 需要来自 `CONTENTFUL_GET_SPACE` 的最新 `sys.version`。如果在你读取和写入之间有其他人修改了该空间，更新将因版本冲突而失败。请务必在更新前立即获取该空间。
- **大量空间的分页：** `CONTENTFUL_LIST_SPACES` 使用 `limit` 和 `skip` 参数。当你拥有大量空间时，请递增 `skip` 进行迭代，直到不再返回结果，以免遗漏空间。
- **范围限制：** 这些工具只管理空间级别的元数据（名称）。它们无法创建或修改空间内的条目、内容类型或资源。
- **认证/权限不匹配：** 如果你的令牌缺少空间管理权限范围，即使通过 `CONTENTFUL_GET_SPACE` 的读取成功，通过 `CONTENTFUL_UPDATE_SPACE` 的更新也会失败。请确认你的令牌具有写入权限。
- **空间 ID 格式：** `space_id` 必须匹配模式 `^[a-zA-Z0-9-_.]{1,64}$`。无效字符将被拒绝。

---

## 快速参考

| 工具 Slug | 描述 |
|---|---|
| `CONTENTFUL_LIST_SPACES` | 列出你的账户可访问的所有空间 |
| `CONTENTFUL_GET_SPACE` | 检索单个空间的详细元数据 |
| `CONTENTFUL_UPDATE_SPACE` | 更新空间名称（需要版本号） |

---

*由 [Composio](https://composio.dev) 提供支持*
