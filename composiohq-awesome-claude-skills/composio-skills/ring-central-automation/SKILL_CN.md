---
name: RingCentral Automation
description: "通过 Rube MCP 实现 RingCentral 自动化 -- 该工具包目前在 Composio 中不可用；未找到 RING_CENTRAL_ 工具"
requires:
  mcp:
    - rube
---

# RingCentral 自动化

> **状态：工具包不可用** -- RUBE_SEARCH_TOOLS 未返回任何 `ring_central` 专属工具。RingCentral 工具包目前不在 Composio 的工具目录中。搜索反而返回了来自不相关工具包（ClickSend、Telnyx、Slack）的工具。

**工具包文档:** [composio.dev/toolkits/ring_central](https://composio.dev/toolkits/ring_central)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 通过使用与 RingCentral 相关的查询调用 `RUBE_SEARCH_TOOLS` 来检查可用性
3. 如果将来出现 `RING_CENTRAL_*` 工具，请通过 `RUBE_MANAGE_CONNECTIONS` 连接，工具包为 `ring_central`

---

## 当前状态

截至最近一次工具发现扫描，RUBE_SEARCH_TOOLS 未返回任何 `RING_CENTRAL_*` 工具 slug。针对 RingCentral 消息、通话记录、传真和分机管理的查询，返回的都是其他工具包的工具：

- SMS/消息查询返回了 **ClickSend** 工具（`CLICKSEND_CREATE_SMS_SEND` 等）
- 通话管理查询返回了 **Pipedrive** 通话记录工具
- 电话/VoIP 查询返回了 **Telnyx** 通知工具
- 传真查询返回了 **ClickSend** 传真自动化工具

这表明 `ring_central` 工具包要么没有注册任何工具，要么尚未集成到 Composio 平台中。

---

## 替代方案

如果你需要电话、SMS 或通信自动化，可以考虑以下可用的工具包：

| 需求 | 替代工具包 | 示例工具 |
|------|-------------------|--------------|
| SMS 消息 | ClickSend | `CLICKSEND_CREATE_SMS_SEND` |
| VoIP/电话 | Telnyx | `TELNYX_CREATE_NOTIFICATION_CHANNEL` |
| 团队消息 | Slack / Webex | `SLACK_SEND_MESSAGE` / `WEBEX_MESSAGING_CREATE_MESSAGE` |

---

## 工具可用时

一旦 RingCentral 工具被添加到 Composio，应参照本集合中其他自动化技能的相同模式，使用真实的工具 slug、模式和陷阱来更新此技能。

---

*由 [Composio](https://composio.dev) 提供支持*
