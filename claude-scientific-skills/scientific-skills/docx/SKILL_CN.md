---
name: docx
description: "当用户想要创建、读取、编辑或操作 Word 文档（.docx 文件）时使用此技能。触发条件包括：任何提及 'Word doc'、'word document'、'.docx'，或请求生成带有目录、标题、页码或信头的专业格式文档。也用于从 .docx 文件中提取或重新组织内容、在文档中插入或替换图像、在 Word 文件中执行查找和替换、处理修订或注释，或将内容转换为精美的 Word 文档。如果用户请求以 Word 或 .docx 文件形式提供 'report'、'memo'、'letter'、'template' 或类似的可交付成果，请使用此技能。不要用于 PDF、电子表格、Google Docs 或与文档生成无关的一般编码任务。"
license: 专有。LICENSE.txt 包含完整条款
---

# DOCX 创建、编辑和分析

## 概述

.docx 文件是一个包含 XML 文件的 ZIP 存档。

## 快速参考

| 任务 | 方法 |
|------|----------|
| 读取/分析内容 | `pandoc` 或解包以获取原始 XML |
| 创建新文档 | 使用 `docx-js` - 参见下面的创建新文档 |
| 编辑现有文档 | 解包 → 编辑 XML → 重新打包 - 参见下面的编辑现有文档 |

### 将 .doc 转换为 .docx

在编辑之前必须转换传统 `.doc` 文件：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# 带有修订的文本提取
pandoc --track-changes=all document.docx -o output.md

# 原始 XML 访问
python scripts/office/unpack.py document.docx unpacked/
```

### 转换为图像

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受修订

要生成包含所有已接受修订的干净文档（需要 LibreOffice）：

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 创建新文档

使用 JavaScript 生成 .docx 文件，然后验证。安装：`npm install -g docx`

### 设置

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');
const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证

创建文件后，验证它。如果验证失败，解包，修复 XML，然后重新打包。

```bash
python scripts/office/validate.py doc.docx
```

### 页面大小

```javascript
// 关键：docx-js 默认为 A4，不是 US Letter
// 始终明确设置页面大小以获得一致的结果
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5 英寸，单位为 DXA
        height: 15840   // 11 英寸，单位为 DXA
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 英寸边距
    }
  },
  children: [/* content */]
}]
```

**常见页面大小（DXA 单位，1440 DXA = 1 英寸）：**

| 纸张 | 宽度 | 高度 | 内容宽度（1" 边距） |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4（默认） | 11,906 | 16,838 | 9,026 |

**横向方向：**docx-js 在内部交换宽度/高度，因此传递纵向尺寸并让它处理交换：

```javascript
size: {
  width: 12240,   // 将短边作为宽度传递
  height: 15840,  // 将长边作为高度传递
  orientation: PageOrientation.LANDSCAPE  // docx-js 在 XML 中交换它们
},
// 内容宽度 = 15840 - 左边距 - 右边距（使用长边）
```

### 样式（覆盖内置标题）

使用 Arial 作为默认字体（普遍支持）。保持标题为黑色以提高可读性。

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt 默认值
    paragraphStyles: [
      // 重要：使用精确的 ID 覆盖内置样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // outlineLevel 是目录所必需的
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] }),
    ]
  }]
});
```

### 列表（永远不要使用 unicode 项目符号）

```javascript
// ❌ 错误 - 永远不要手动插入项目符号
new Paragraph({ children: [new TextRun("• Item")] })  // 错误
new Paragraph({ children: [new TextRun("\u2022 Item")] })  // 错误

// ✅ 正确 - 使用带有 LevelFormat.BULLET 的编号配置
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item")] }),
    ]
  }]
});

// ⚠️ 每个引用创建独立的编号
// 相同的引用 = 继续（1,2,3 然后 4,5,6）
// 不同的引用 = 重新开始（1,2,3 然后 1,2,3）
```

### 表格

**关键：表格需要双重宽度** - 在表格上设置 `columnWidths` 并在每个单元格上设置 `width`。如果没有两者，表格在某些平台上渲染不正确。

```javascript
// 关键：始终设置表格宽度以获得一致的渲染
// 关键：使用 ShadingType.CLEAR（而不是 SOLID）以防止黑色背景
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // 始终使用 DXA（百分比在 Google Docs 中会中断）
  columnWidths: [4680, 4680], // 必须总和为表格宽度（DXA：1440 = 1 英寸）
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // 也在每个单元格上设置
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR 而不是 SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // 单元格填充（内部，不添加到宽度）
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
]
})
```

**表格宽度计算：**

始终使用 `WidthType.DXA` — `WidthType.PERCENTAGE` 在 Google Docs 中会中断。

```javascript
// 表格宽度 = columnWidths 的总和 = 内容宽度
// 带有 1" 边距的 US Letter：12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // 必须总和为表格宽度
```

**宽度规则：**
- **始终使用 `WidthType.DXA`** — 永远不要使用 `WidthType.PERCENTAGE`（与 Google Docs 不兼容）
- 表格宽度必须等于 `columnWidths` 的总和
- 单元格 `width` 必须匹配相应的 `columnWidth`
- 单元格 `margins` 是内部填充 - 它们减少内容区域，而不是添加到单元格宽度
- 对于全宽表格：使用内容宽度（页面宽度减去左边距和右边距）

### 图像

```javascript
// 关键：type 参数是必需的
new Paragraph({
  children: [new ImageRun({
    type: "png", // 必需：png、jpg、jpeg、gif、bmp、svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // 所有三个都是必需的
  })]
})
```

### 分页符

```javascript
// 关键：PageBreak 必须在 Paragraph 内
new Paragraph({ children: [new PageBreak()] })

// 或使用 pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New page")] })
```

### 超链接

```javascript
// 外部链接
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Click here", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// 内部链接（书签 + 引用）
// 1. 在目标处创建书签
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("Chapter 1")] }),
]})
// 2. 链接到它
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "See Chapter1", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### 脚注

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("Source: Annual Report 2024")] },
    2: { children: [new Paragraph("See appendix for methodology")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("Revenue grew 15%"),
        new FootnoteReferenceRun(1),
        new TextRun(" using adjusted metrics"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### 制表符

```javascript
// 在同一行右对齐文本（例如，标题对面的日期）
new Paragraph({
  children: [
    new TextRun("Company Name"),
    new TextRun("\tJanuary 2025"),
  ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// 点前导符（例如，目录风格）
new Paragraph({
  children: [
    new TextRun("Introduction"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### 多列布局

```javascript
// 等宽列
sections: [{
  properties: {
    column: {
      count: 2,          // 列数
      space: 720,        // 列之间的间隙，单位为 DXA（720 = 0.5 英寸）
      equalWidth: true,
      separate: true,    // 列之间的垂直线
    },
  },
  children: [/* 内容自然流过列 */]
}]

// 自定义宽度列（equalWidth 必须为 false）
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* 内容 */]
}]
```

使用 `type: SectionType.NEXT_COLUMN` 的新部分强制列中断。

### 目录

```javascript
// 关键：标题必须仅使用 HeadingLevel - 没有自定义样式
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### 页眉/页脚

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1 英寸
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* content */]
}]
```

### docx-js 的关键规则

- **明确设置页面大小** - docx-js 默认为 A4；对于 US 文档使用 US Letter（12240 x 15840 DXA）
- **横向：传递纵向尺寸** - docx-js 在内部交换宽度/高度；将短边作为 `width` 传递，将长边作为 `height` 传递，并设置 `orientation: PageOrientation.LANDSCAPE`
- **永远不要使用 `\n`** - 使用单独的 Paragraph 元素
- **永远不要使用 unicode 项目符号** - 使用带有编号配置的 `LevelFormat.BULLET`
- **PageBreak 必须在 Paragraph 中** - 独立创建无效的 XML
- **ImageRun 需要 `type`** - 始终指定 png/jpg/etc
- **始终使用 DXA 设置表格 `width`** - 永远不要使用 `WidthType.PERCENTAGE`（在 Google Docs 中会中断）
- **表格需要双重宽度** - `columnWidths` 数组和单元格 `width`，两者必须匹配
- **表格宽度 = columnWidths 的总和** - 对于 DXA，确保它们完全相加
- **始终添加单元格边距** - 使用 `margins: { top: 80, bottom: 80, left: 120, right: 120 }` 以获得可读的填充
- **使用 `ShadingType.CLEAR`** - 对于表格着色永远不要使用 SOLID
- **永远不要将表格用作分隔符/规则** - 单元格具有最小高度并渲染为空框（包括在页眉/页脚中）；而是在 Paragraph 上使用 `border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }`。对于两列页脚，使用制表符（参见制表符部分），而不是表格
- **目录需要仅 HeadingLevel** - 标题段落上没有自定义样式
- **覆盖内置样式** - 使用精确的 ID："Heading1"、"Heading2" 等
- **包含 `outlineLevel`** - 目录所必需的（H1 为 0，H2 为 1 等）

---

## 编辑现有文档

**按顺序遵循所有 3 个步骤。**

### 步骤 1：解包

```bash
python scripts/office/unpack.py document.docx unpacked/
```

提取 XML、漂亮打印、合并相邻的运行，并将智能引号转换为 XML 实体（`&#x201C;` 等），以便它们在编辑中幸存。使用 `--merge-runs false` 跳过运行合并。

### 步骤 2：编辑 XML

在 `unpacked/word/` 中编辑文件。请参阅下面的 XML 参考以了解模式。

**使用 "Claude" 作为修订和注释的作者**，除非用户明确要求使用不同的名称。

**直接对字符串替换使用 Edit 工具。不要编写 Python 脚本。**脚本会引入不必要的复杂性。Edit 工具确切显示正在替换的内容。

**关键：对新内容使用智能引号。**当添加带有撇号或引号的文本时，使用 XML 实体生成智能引号：

```xml
<!-- 使用这些实体以实现专业排版 -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```

| 实体 | 字符 |
|--------|-----------|
| `&#x2018;` | '（左单引号） |
| `&#x2019;` | '（右单引号 / 撇号） |
| `&#x201C;` | "（左双引号） |
| `&#x201D;` | "（右双引号） |

**添加注释：**使用 `comment.py` 处理多个 XML 文件的样板：

```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # 回复到注释 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"  # 自定义作者名称
```

然后将标记添加到 document.xml（请参阅 XML 参考中的注释）。

### 步骤 3：打包

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

使用自动修复进行验证、压缩 XML 并创建 DOCX。使用 `--validate false` 跳过。

**自动修复将修复：**
- `durableId` >= 0x7FFFFFFF（重新生成有效的 ID）
- `<w:t>` 上缺少的 `xml:space="preserve"`，带有空格

**自动修复不会修复：**
- 格式错误的 XML、无效的元素嵌套、缺少的关系、架构违规

### 常见陷阱

- **替换整个 `<w:r>` 元素**：添加修订时，将整个 `<w:r>...</w:r>` 块替换为 `<w:del>...<w:ins>...` 作为兄弟节点。不要在运行内注入修订标记。
- **保留 `<w:rPr>` 格式**：将原始运行的 `<w:rPr>` 块复制到修订运行中，以保持粗体、字体大小等。

---

## XML 参考

### 架构合规性

- **`<w:pPr>` 中的元素顺序**：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`、`<w:rPr>` 最后
- **空格**：将 `xml:space="preserve"` 添加到带有前导/尾随空格的 `<w:t>`
- **RSIDs**：必须是 8 位十六进制（例如，`00AB1234`）

### 修订

**插入：**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

**删除：**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**在 `<w:del>` 内**：使用 `<w:delText>` 而不是 `<w:t>`，并使用 `<w:delInstrText>` 而不是 `<w:instrText>`。

**最小编辑** - 仅标记更改的内容：

```xml
<!-- 将 "30 days" 更改为 "60 days" -->
<w:r><w:t>The term is </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> days.</w:t></w:r>
```

**删除整个段落/列表项** - 当从段落中删除所有内容时，也将段落标记标记为已删除，以便与下一段落合并。在 `<w:pPr><w:rPr>` 内添加 `<w:del/>`：

```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- 如果存在列表编号 -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Entire paragraph content being deleted...</w:delText></w:r>
  </w:del>
</w:p>
```

如果没有 `<w:del/>` 在 `<w:pPr><w:rPr>` 内，接受更改会留下一个空段落/列表项。

**拒绝另一个作者的插入** - 在其插入内嵌套删除：

```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>their inserted text</w:delText></w:r>
  </w:del>
</w:ins>
```

**恢复另一个作者的删除** - 在其删除后添加插入（不要修改他们的删除）：

```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>deleted text</w:t></w:r>
</w:ins>
```

### 注释

运行 `comment.py` 后（请参阅步骤 2），将标记添加到 document.xml。对于回复，使用 `--parent` 标志并将标记嵌套在父标记内。

**关键：`<w:commentRangeStart>` 和 `<w:commentRangeEnd>` 是 `<w:r>` 的兄弟节点，永远不在 `<w:r>` 内。**

```xml
<!-- 注释标记是 w:p 的直接子节点，永远不在 w:r 内 -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted</w:delText></w:r>
</w:del>
<w:r><w:t> more text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- 注释 0 嵌套了回复 1 -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>text</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### 图像

1. 将图像文件添加到 `word/media/`
2. 将关系添加到 `word/_rels/document.xml.rels`：
```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```
3. 将内容类型添加到 `[Content_Types].xml`：
```xml
<Default Extension="png" ContentType="image/png"/>
```
4. 在 document.xml 中引用：
```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMUs：914400 = 1 英寸 -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

---

## 依赖项

- **pandoc**：文本提取
- **docx**：`npm install -g docx`（新文档）
- **LibreOffice**：PDF 转换（通过 `scripts/office/soffice.py` 自动配置为沙盒环境）
- **Poppler**：`pdftoppm` 用于图像
