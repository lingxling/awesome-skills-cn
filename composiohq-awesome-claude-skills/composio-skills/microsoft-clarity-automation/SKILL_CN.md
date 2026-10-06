---
name: Microsoft Clarity Automation
description: "通过 Composio 的 Microsoft Clarity 集成自动化用户行为分析——导出热力图数据、会话指标，以及按浏览器、设备、国家、来源等维度细分的参与度分析。"
requires:
  mcp:
    - rube
---

# Microsoft Clarity Automation

直接从 Claude Code 导出 **Microsoft Clarity** 用户行为分析数据。无需离开终端即可提取热力图数据、会话指标和按多个维度细分的参与度洞察。

**工具包文档：** [composio.dev/toolkits/microsoft_clarity](https://composio.dev/toolkits/microsoft_clarity)

---

## 设置

1. 将 Composio MCP 服务器添加到你的配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Microsoft Clarity 账户。代理会提供一个身份验证链接。
3. 确保你的 Clarity 项目为想要分析的维度开启了足够的数据收集。

---

## 核心工作流

### 1. 导出近期分析数据

导出最近 1-3 天的 Clarity 分析数据，可同时按最多三个维度细分。

**工具：** `MICROSOFT_CLARITY_DATA_EXPORT`

关键参数：
- `numOfDays`（必填）-- 导出的天数：`1`（最近 24 小时）、`2`（最近 48 小时）或 `3`（最近 72 小时）
- `dimension1` -- 第一个细分维度
- `dimension2` -- 第二个细分维度（可选）
- `dimension3` -- 第三个细分维度（可选）

可用维度：
- `Browser` -- Chrome、Firefox、Safari、Edge 等
- `Device` -- 桌面端、移动端、平板
- `Country/Region` -- 用户的地理位置
- `OS` -- Windows、macOS、iOS、Android 等
- `Source` -- 流量来源（例如 google、direct、referral）
- `Medium` -- 流量媒介（organic、cpc、referral 等）
- `Campaign` -- 营销活动名称
- `Channel` -- 流量渠道分组
- `URL` -- 特定页面 URL

示例提示词：*“导出最近 24 小时按 Device 和 Country/Region 细分的 Clarity 数据”*

---

### 2. 设备性能分析

分析不同设备类型下的用户行为差异，以优化响应式设计。

**工具：** `MICROSOFT_CLARITY_DATA_EXPORT`

配置：`numOfDays: 3`、`dimension1: "Device"`、`dimension2: "Browser"`

示例提示词：*“显示最近 3 天按 Device 和 Browser 细分的 Clarity 指标”*

---

### 3. 流量来源细分

了解哪些流量来源带来了参与度最高的用户。

**工具：** `MICROSOFT_CLARITY_DATA_EXPORT`

配置：`numOfDays: 2`、`dimension1: "Source"`、`dimension2: "Medium"`

示例提示词：*“导出最近 48 小时按 Source 和 Medium 细分的 Clarity 数据”*

---

### 4. 地理用户行为

分析不同国家和地区的用户参与模式。

**工具：** `MICROSOFT_CLARITY_DATA_EXPORT`

配置：`numOfDays: 3`、`dimension1: "Country/Region"`、`dimension2: "Device"`

示例提示词：*“获取最近 72 小时按 Country/Region 和 Device 类型细分的 Clarity 数据”*

---

### 5. 页面级性能

检查哪些特定 URL 具有最高或最低的参与度指标。

**工具：** `MICROSOFT_CLARITY_DATA_EXPORT`

配置：`numOfDays: 1`、`dimension1: "URL"`、`dimension2: "Device"`

示例提示词：*“导出昨天按 URL 和 Device 细分的 Clarity 数据”*

---

### 6. 营销活动归因分析

通过用户行为指标评估营销活动的有效性。

**工具：** `MICROSOFT_CLARITY_DATA_EXPORT`

配置：`numOfDays: 3`、`dimension1: "Campaign"`、`dimension2: "Channel"`、`dimension3: "Device"`

示例提示词：*“显示最近 3 天按 Campaign、Channel 和 Device 细分的 Clarity 参与度数据”*

---

## 常见陷阱

- **时间窗口有限：** 数据导出仅限最近 1、2 或 3 天。`numOfDays` 参数只接受 1、2 或 3 这几个值。若需要更长的历史分析，需要定期运行导出并在外部进行汇总。
- **维度名称需精确匹配：** 维度值必须与列表中完全一致（例如 `Country/Region` 而非 `country` 或 `region`）。大小写和斜杠都很重要。
- **最多三个维度：** 每次导出最多可按三个维度细分。若需要更复杂的分析，请使用不同的维度组合运行多次导出。
- **数据可用性延迟：** Clarity 数据可能存在短暂的处理延迟。非常近期的会话（最近几分钟）可能不会出现在导出结果中。
- **单一工具限制：** Clarity 集成目前只提供数据导出工具。如需热力图可视化和会话录屏，请直接使用 Clarity 网页仪表盘。
- **响应体大小：** 像 `URL` 这样的高基数维度与其他维度组合使用时，可能产生较大的响应负载。可考虑缩小时间窗口或减少使用的维度数量。

---

## 快速参考

| 工具 Slug | 描述 |
|---|---|
| `MICROSOFT_CLARITY_DATA_EXPORT` | 导出带有最多 3 个维度细分的分析数据 |

**可用维度：**

| 维度 | 描述 |
|---|---|
| `Browser` | 网页浏览器（Chrome、Firefox、Safari 等） |
| `Device` | 设备类型（桌面端、移动端、平板） |
| `Country/Region` | 地理位置 |
| `OS` | 操作系统 |
| `Source` | 流量来源 |
| `Medium` | 流量媒介 |
| `Campaign` | 营销活动 |
| `Channel` | 流量渠道分组 |
| `URL` | 特定页面 URL |

---

*由 [Composio](https://composio.dev) 提供支持*
