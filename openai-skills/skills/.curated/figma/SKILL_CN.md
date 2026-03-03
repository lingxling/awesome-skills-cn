---
name: figma
description: "使用 Figma MCP 服务器获取设计上下文、截图、变量和资产，并将 Figma 节点转换为生产代码。当任务涉及 Figma URL、节点 ID、设计到代码实现或 Figma MCP 设置和故障排除时触发。"
---

# Figma MCP

使用 Figma MCP 服务器进行 Figma 驱动的实现。有关设置和调试详细信息（环境变量、配置、验证），请参阅 `references/figma-mcp-config.md`。

## Figma MCP 集成规则

这些规则定义了如何将 Figma 输入转换为此项目的代码，并且必须为每个 Figma 驱动的更改遵循。

### 必需流程（不要跳过）

1. 首先运行 get_design_context 以获取要实现的确切节点的结构化表示。
2. 如果响应太大或被截断，运行 get_metadata 获取高级节点映射，然后仅使用 get_design_context 重新获取所需的节点。
3. 运行 get_screenshot 以获取要实现的节点变体的视觉参考。
4. 只有在您同时拥有 get_design_context 和 get_screenshot 后，下载任何需要的资产并开始实现。
5. 将输出（通常是 React + Tailwind）转换为此项目的约定、样式和框架。尽可能重用项目的颜色令牌、组件和排版。
6. 针对 Figma 以 1:1 的外观和行为进行验证，然后再标记为完成。

### 实现规则

- 将 Figma MCP 输出（通常是 React + Tailwind）视为设计和行为的表示，而不是最终代码样式。
- 在适用时，用项目首选的工具/设计系统令牌替换 Tailwind 实用类。
- 重用现有组件（例如，按钮、输入、排版、图标包装器），而不是重复功能。
- 一致地使用项目的颜色系统、排版比例和间距令牌。
- 尊重项目已采用的路由、状态管理和数据获取模式。
- 当出现冲突时，优先考虑设计系统令牌并最小化调整间距或大小以匹配视觉效果。
- 针对 Figma 截图验证最终 UI 的外观和行为。

### 资产处理

Figma MCP 服务器提供一个资产端点，可以提供图像和 SVG 资产。

**重要：** 如果 Figma MCP 服务器为图像或 SVG 返回 localhost 源，请直接使用该图像或 SVG 源。
**重要：** 不要导入或添加新的图标包，所有资产应来自 Figma 负载。
**重要：** 如果提供了 localhost 源，不要使用或创建占位符。

### 基于链接的提示

服务器是基于链接的：复制 Figma 帧/图层链接并将该 URL 提供给 MCP 客户端，当请求实现帮助时。
- 客户端无法浏览 URL 但从链接中提取节点 ID；始终确保链接指向您想要的确切节点/变体。

## 参考

- `references/figma-mcp-config.md` — 设置、验证、故障排除和基于链接的使用提醒。
- `references/figma-tools-and-prompts.md` — 工具目录和用于选择框架/组件以及获取元数据的提示模式。
