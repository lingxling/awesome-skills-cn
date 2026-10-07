---
name: bilig-workpaper
description: 使用公式支持的 WorkPaper JSON 和 MCP 工具进行代理电子表格任务，无需驾驶 Excel 或浏览器 UI。
risk: critical
source: community
date_added: "2026-05-21"
tags:
  - spreadsheets
  - formulas
  - mcp
  - xlsx
  - typescript
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Bilig WorkPaper

## 概述

Bilig WorkPaper 为代理提供代码优先的工作簿运行时，用于电子表格风格的业务逻辑。当任务更容易建模为表和公式时使用，但可靠的路径是通过 API 编辑单元格、重新计算、读取计算值并保持 JSON 工作簿文档。

主要用例是用确定性工具调用替换脆弱的电子表格 UI 自动化。它对报价计算器、支付模型、预算检查、导入验证和减少 XLSX 公式错误报告很有用。

## 何时使用此技能

当用户需要以下操作时使用此技能：

- 从 Node.js 服务、路由、测试或代理工具与电子表格公式一起工作；
- 编写工作簿输入并验证带有读回证明的计算输出；
- 将公式工作簿保留为可审查的 WorkPaper JSON；
- 通过 MCP 工具公开文件支持的工作簿；
- 调查 XLSX 公式重新计算问题，而无需自动化 Excel、LibreOffice 或浏览器网格。

不要将其用于手动电子表格编辑、VBA/宏、数据透视表、图表、COM 自动化或精确的桌面 Excel 行为，除非用户明确要求与 Excel 作为预言进行比较。

## 更安全的命令模式

在 MCP/客户端配置中优先使用参数数组。不要 shell 连接用户提供的路径、工作表名称、公式或单元格地址。在用命令使用前拒绝包含换行符、反引号、`$(`、`;`、`&`、`|`、`<` 或 `>` 的路径或单元格输入。

MCP 示例执行公开的 `@bilig/workpaper` npm 包。将其视为第三方代码执行：固定您审查的包版本、仅在受信任项目中运行它，并在启动可写 MCP 服务器之前获得明确的用户批准。

## 快速 MCP 设置

首先证明包所有的挑战有效：

```json
{
  "command": "npm",
  "args": ["exec", "--package", "@bilig/workpaper@<reviewed-version>", "--", "bilig-mcp-challenge"]
}
```

然后运行可写文件支持的 MCP 服务器：

```json
{
  "command": "npm",
  "args": [
    "exec",
    "--package",
    "@bilig/workpaper@<reviewed-version>",
    "--",
    "bilig-workpaper-mcp",
    "--workpaper",
    "./pricing.workpaper.json",
    "--init-demo-workpaper",
    "--writable"
  ]
}
```

MCP 服务器公开的有用工具：

- `list_sheets`
- `read_range`
- `read_cell`
- `set_cell_contents`
- `get_cell_display_value`
- `export_workpaper_document`
- `validate_formula`

每次写入后，读取依赖输出单元格并导出 WorkPaper 文档。不要仅从写调用中声称成功。

## 直接 TypeScript 模式

当工作簿逻辑属于应用程序代码时直接使用包：

```ts
import {
  WorkPaper,
  exportWorkPaperDocument,
  serializeWorkPaperDocument,
} from "@bilig/workpaper";

const workbook = WorkPaper.buildFromSheets({
  Inputs: [
    ["Metric", "Value"],
    ["Customers", 20],
    ["Average revenue", 1200],
  ],
  Summary: [
    ["Metric", "Value"],
    ["Revenue", "=Inputs!B2*Inputs!B3"],
  ],
});

const inputs = workbook.getSheetId("Inputs");
const summary = workbook.getSheetId("Summary");
if (inputs === undefined || summary === undefined) {
  throw new Error("Workbook is missing required sheets");
}

workbook.setCellContents({ sheet: inputs, row: 1, col: 1 }, 32);
const revenue = workbook.getCellDisplayValue({ sheet: summary, row: 1, col: 1 });
const saved = serializeWorkPaperDocument(
  exportWorkPaperDocument(workbook, { includeConfig: true }),
);

console.log({ revenue, savedBytes: saved.length });
```

## 必需的验证

良好的代理响应应包括：

- 编辑的精确工作表名称和 A1 单元格；
- 重要输入和依赖输出的之前值；
- 从重新计算的工作簿读取的之后值；
- 来自导出或序列化 WorkPaper JSON 的持久性证据；
- 当文件边界很重要时的恢复或重新导入证明；
- 对不支持的公式或仅 Excel 行为的明确限制。

如果任何验证步骤失败，报告阻止程序而不是说工作簿已更新。

## 限制

- WorkPaper 行为不是桌面 Excel、VBA、数据透视表、图表或 UI 自动化的完全替代品。
- 公式兼容性取决于 Bilig 运行时，当精确奇偶性很重要时应针对 Excel 进行验证。
- MCP 写入应保持范围在受信任的工作簿路径内，必须遵循读回验证。

## 参考资料

- 存储库：https://github.com/proompteng/bilig
- 紧凑文档地图：https://proompteng.github.io/bilig/llms.txt
- 代理手册：https://proompteng.github.io/bilig/headless-workpaper-agent-handbook.html
- MCP 服务器指南：https://proompteng.github.io/bilig/mcp-workpaper-tool-server.html
- XLSX 公式诊所：https://proompteng.github.io/bilig/formula-bug-clinic.html
- 兼容性限制：https://proompteng.github.io/bilig/where-bilig-is-not-excel-compatible-yet.html
