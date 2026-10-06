---
name: Excel Automation
description: "Excel 自动化：通过 Microsoft Excel 和 Google Sheets 集成创建工作簿、管理工作表、读写单元格数据以及格式化表格"
requires:
  mcp: [rube]
---

# Excel Automation

自动化电子表格操作，包括创建工作簿、写入数据、格式化单元格、更新插入（upsert）行以及管理工作表。支持 Microsoft Excel（OneDrive）和 Google Sheets。

**工具包文档：** [composio.dev/toolkits/excel](https://composio.dev/toolkits/excel)

---

## 设置

本技能需要连接 **Rube MCP 服务器**，地址为 `https://rube.app/mcp`。

在执行任何工具之前，请确保 `excel`（以及可选的 `googlesheets`）工具包已存在有效连接。如果没有活动连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起一个。

---

## 核心工作流

### 1. 创建新的 Excel 工作簿

使用 `EXCEL_CREATE_WORKBOOK` 生成一个新的 `.xlsx` 文件并上传到 OneDrive。

**工具：** `EXCEL_CREATE_WORKBOOK`

**步骤：**
1. 调用 `EXCEL_CREATE_WORKBOOK`，传入工作表名称和数据
2. 该工具会创建一个 `.xlsx` 文件并上传到 OneDrive
3. 使用返回的文件路径/URL 进行后续操作

---

### 2. 向表格写入数据

使用 `GOOGLESHEETS_BATCH_UPDATE` 将值写入指定范围或追加行。

**工具：** `GOOGLESHEETS_BATCH_UPDATE`

**关键参数：**
- `spreadsheet_id`（必填）—— 来自 URL 的表格 ID（44 位字母数字字符串）
- `sheet_name`（必填）—— 标签页名称，例如 `"Sheet1"`、`"Sales Data"`
- `values`（必填）—— 单元格值的二维数组，例如 `[["Name","Amount"],["Alice",100]]`
- `first_cell_location` —— A1 表示法的起始单元格（例如 `"A1"`、`"D3"`）。省略则追加行
- `valueInputOption` —— `"USER_ENTERED"`（默认，解析公式）或 `"RAW"`（原样存储）

**示例：**
```
Tool: GOOGLESHEETS_BATCH_UPDATE
Arguments:
  spreadsheet_id: "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
  sheet_name: "Sheet1"
  values: [["Item","Cost","Stocked"],["Wheel",20.50,true],["Screw",0.50,true]]
  first_cell_location: "A1"
```

---

### 3. 按键列更新插入（Upsert）行

使用 `GOOGLESHEETS_UPSERT_ROWS` 通过匹配键列来更新现有行，若未找到匹配项则追加新行。非常适合 CRM 同步、库存更新和去重。

**工具：** `GOOGLESHEETS_UPSERT_ROWS`

**关键参数：**
- `spreadsheetId`（必填）—— 表格 ID
- `sheetName`（必填）—— 标签页名称
- `rows`（必填）—— 数据行的二维数组（至少 1 行）。如果省略 `headers`，第一行将被视为表头
- `headers` —— 数据的列名，例如 `["Email","Phone","Status"]`
- `keyColumn` —— 用于匹配的列标题，例如 `"Email"`、`"SKU"`、`"Lead ID"`
- `strictMode` —— `true`（默认）在列不匹配时报错；`false` 则静默截断

**示例：**
```
Tool: GOOGLESHEETS_UPSERT_ROWS
Arguments:
  spreadsheetId: "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
  sheetName: "Contacts"
  keyColumn: "Email"
  headers: ["Email","Phone","Status"]
  rows: [["john@example.com","555-0101","Active"],["jane@example.com","555-0102","Pending"]]
```

---

### 4. 格式化单元格

使用 `GOOGLESHEETS_FORMAT_CELL` 对范围应用粗体、斜体、字号和背景颜色。

**工具：** `GOOGLESHEETS_FORMAT_CELL`

**关键参数：**
- `spreadsheet_id`（必填）—— 表格 ID
- `range` —— A1 表示法的单元格范围，例如 `"A1:D1"`、`"B2:B10"`（推荐优先于基于索引的方式）
- `sheet_name` —— 工作表名称，例如 `"Sheet1"`
- `bold` —— `true`/`false`
- `italic` —— `true`/`false`
- `fontSize` —— 字号（磅），例如 `12`
- `red`、`green`、`blue` —— 背景颜色分量（0.0--1.0 的浮点数范围，而非 0--255）

**示例（表头行加粗并设置蓝色背景）：**
```
Tool: GOOGLESHEETS_FORMAT_CELL
Arguments:
  spreadsheet_id: "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
  range: "A1:D1"
  sheet_name: "Sheet1"
  bold: true
  fontSize: 12
  red: 0.2
  green: 0.4
  blue: 0.9
```

---

### 5. 添加新工作表标签页

使用 `GOOGLESHEETS_ADD_SHEET` 在现有表格中创建新的标签页。

**工具：** `GOOGLESHEETS_ADD_SHEET`

**关键参数：**
- `spreadsheetId`（必填）—— 表格 ID
- `title` —— 新标签页的名称，例如 `"Q4 Report"`
- `forceUnique` —— `true`（默认）在名称已存在时自动追加后缀

**示例：**
```
Tool: GOOGLESHEETS_ADD_SHEET
Arguments:
  spreadsheetId: "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
  title: "Q4 Report"
  forceUnique: true
```

---

### 6. 读取数据并验证内容

使用 `GOOGLESHEETS_BATCH_GET` 从指定单元格范围检索数据以进行验证或进一步处理。

**工具：** `GOOGLESHEETS_BATCH_GET`

**步骤：**
1. 调用 `GOOGLESHEETS_BATCH_GET`，传入表格 ID 和目标范围
2. 验证表头和数据对齐情况
3. 使用结果来指导后续的写入或更新操作

**辅助工具：**
- `GOOGLESHEETS_GET_SHEET_NAMES` —— 列出表格中的所有标签页名称
- `GOOGLESHEETS_GET_SPREADSHEET_INFO` —— 获取元数据（工作表 ID、属性）
- `GOOGLESHEETS_FIND_WORKSHEET_BY_TITLE` —— 检查特定标签页是否存在

---

## 推荐执行计划

1. **创建或定位表格**，使用 `GOOGLESHEETS_CREATE_GOOGLE_SHEET1` 或复用现有的 `spreadsheetId`
2. **确认目标标签页**，使用 `GOOGLESHEETS_GET_SHEET_NAMES` 或 `GOOGLESHEETS_FIND_WORKSHEET_BY_TITLE`；若不存在则用 `GOOGLESHEETS_ADD_SHEET` 创建
3. **读取现有表头**（可选），使用 `GOOGLESHEETS_BATCH_GET` 对齐列
4. **写入或更新插入数据**，使用 `GOOGLESHEETS_BATCH_UPDATE` 或 `GOOGLESHEETS_UPSERT_ROWS`
5. **应用格式化**（可选），使用 `GOOGLESHEETS_FORMAT_CELL`
6. **验证结果**（可选），使用 `GOOGLESHEETS_BATCH_GET`
7. **回退方案：** 如果 Google Sheets 创建被阻止（HTTP 403），使用 `EXCEL_CREATE_WORKBOOK` 输出本地 `.xlsx` 文件

---

## 已知坑点

| 坑点 | 详情 |
|---------|--------|
| **创建表格时出现 HTTP 403** | 当缺少 Drive 创建权限（create scope）时，`GOOGLESHEETS_CREATE_GOOGLE_SHEET1` 会失败。请复用现有的 `spreadsheetId` 或回退到 `EXCEL_CREATE_WORKBOOK`。 |
| **单元格数量限制与限流** | 每个 Google 表格大约有 500 万个单元格的上限。写入频率过高会触发 HTTP 429。请批量处理变更，并将大批量写入分块（每次调用约 500 行）。 |
| **格式范围偏移一位** | 使用索引模式时，`GOOGLESHEETS_FORMAT_CELL` 采用从 0 开始、endIndex 不包含在内的范围。背景颜色使用 0--1 的浮点 RGB，而不是 0--255 的整数 RGB。 |
| **工作表标题唯一性** | 工作表标题在 API 响应中并不保证唯一。建议通过数字型 `sheetId` 操作，并在写入前验证已解析的标签页。 |
| **Upsert 数据格式** | `GOOGLESHEETS_UPSERT_ROWS` 需要表头加二维行数组。传入字典列表或空的 `rows` 会导致校验错误。请确保至少有 1 行数据。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `EXCEL_CREATE_WORKBOOK` | 创建一个新的 `.xlsx` 工作簿并上传到 OneDrive |
| `GOOGLESHEETS_BATCH_UPDATE` | 将值写入某个范围或追加新行 |
| `GOOGLESHEETS_UPSERT_ROWS` | 按键更新现有行或追加新行 |
| `GOOGLESHEETS_FORMAT_CELL` | 对单元格范围应用文本/背景格式 |
| `GOOGLESHEETS_ADD_SHEET` | 向表格添加新的工作表标签页 |
| `GOOGLESHEETS_CREATE_GOOGLE_SHEET1` | 在 Drive 中创建新的 Google 表格 |
| `GOOGLESHEETS_GET_SHEET_NAMES` | 列出表格中的所有工作表名称 |
| `GOOGLESHEETS_GET_SPREADSHEET_INFO` | 获取表格元数据 |
| `GOOGLESHEETS_FIND_WORKSHEET_BY_TITLE` | 按标题检查工作表是否存在 |
| `GOOGLESHEETS_BATCH_GET` | 从指定单元格范围读取数据 |

---

*Powered by [Composio](https://composio.dev)*
