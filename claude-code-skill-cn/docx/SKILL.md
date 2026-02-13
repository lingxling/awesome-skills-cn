---
name: docx
description: "当用户想要创建、读取、编辑或操作Word文档（.docx文件）时使用此技能。触发条件包括：任何提及\"Word文档\"、\"word document\"、\".docx\"，或请求生成具有格式化（如目录、标题、页码或信头）的专业文档。也用于从.docx文件中提取或重新组织内容，在文档中插入或替换图像，在Word文件中执行查找和替换，处理修订或批注，或将内容转换为精美的Word文档。如果用户要求\"报告\"、\"备忘录\"、\"信函\"、\"模板\"或类似交付物作为Word或.docx文件，请使用此技能。不要用于PDF、电子表格、Google文档或与文档生成无关的一般编码任务。"
license: 完整条款见LICENSE.txt
---

# DOCX 创建、编辑和分析

## 概述

.docx文件是一个包含XML文件的ZIP存档。

## 快速参考

| 任务 | 方法 |
|------|----------|
| 读取/分析内容 | `pandoc`或解包以获取原始XML |
| 创建新文档 | 使用`docx-js` - 见下文创建新文档 |
| 编辑现有文档 | 解包 → 编辑XML → 重新打包 - 见下文编辑现有文档 |

### 将.doc转换为.docx

编辑之前必须转换旧的`.doc`文件：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# 带修订的文本提取
pandoc --track-changes=all document.docx -o output.md

# 原始XML访问
python scripts/office/unpack.py document.docx unpacked/
```

### 转换为图像

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受修订

要生成一个接受所有修订的干净文档（需要LibreOffice）：

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 创建新文档

使用JavaScript生成.docx文件，然后验证。安装：`npm install -g docx`

### 设置
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* 内容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证
创建文件后，验证它。如果验证失败，解包，修复XML，然后重新打包。
```bash
python scripts/office/validate.py doc.docx
```

### 页面大小

```javascript
// 关键：docx-js默认为A4，不是US Letter
// 始终显式设置页面大小以获得一致的结果
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5英寸，DXA单位
        height: 15840   // 11英寸，DXA单位
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1英寸边距
    }
  },
  children: [/* 内容 */]
}]
```

**常见页面大小（DXA单位，1440 DXA = 1英寸）：**

| 纸张 | 宽度 | 高度 | 内容宽度（1"边距） |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4（默认） | 11,906 | 16,838 | 9,026 |

**横向方向**：docx-js在内部交换宽度/高度，因此传递纵向尺寸并让它处理交换：
```javascript
size: {
  width: 12240,   // 将短边作为宽度传递
  height: 15840,  // 将长边作为高度传递
  orientation: PageOrientation.LANDSCAPE  // docx-js在XML中交换它们
},
// 内容宽度 = 15840 - 左边距 - 右边距（使用长边）
```

### 样式（覆盖内置标题）

使用Arial作为默认字体（通用支持）。保持标题为黑色以提高可读性。

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt默认
    paragraphStyles: [
      // 重要：使用精确ID覆盖内置样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // outlineLevel是目录所需的
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("标题")] }),
    ]
  }]
});
```

### 列表（绝不使用unicode项目符号）

```javascript
// ❌ 错误 - 永远不要手动插入项目符号字符
new Paragraph({ children: [new TextRun("• 项目")] })  // 坏
new Paragraph({ children: [new TextRun("\u2022 项目")] })  // 坏

// ✅ 正确 - 使用带有LevelFormat.BULLET的编号配置
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
        children: [new TextRun("项目符号项")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("编号项")] }),
    ]
  }]
});

// ⚠️ 每个reference创建独立的编号
// 相同reference = 继续（1,2,3然后4,5,6）
// 不同reference = 重新开始（1,2,3然后1,2,3）
```

### 表格

**关键：表格需要双重宽度** - 在表格上设置`columnWidths`，在每个单元格上设置`width`。没有两者，表格在某些平台上渲染不正确。

```javascript
// 关键：始终设置表格宽度以获得一致的渲染
// 关键：使用ShadingType.CLEAR（不是SOLID）以防止黑色背景
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // 始终使用DXA（百分比在Google Docs中中断）
  columnWidths: [4680, 4680], // 必须总和为表格宽度（DXA：1440 = 1英寸）
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // 也在每个单元格上设置
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR不是SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // 单元格内边距（内部，不添加到宽度）
          children: [new Paragraph({ children: [new TextRun("单元格")] })]
        })
      ]
    })
  ]
})
```

**表格宽度计算：**

始终使用`WidthType.DXA` — `WidthType.PERCENTAGE`在Google Docs中中断。

```javascript
// 表格宽度 = columnWidths的总和 = 内容宽度
// US Letter带有1"边距：12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // 必须总和为表格宽度
```

**宽度规则：**
- **始终使用`WidthType.DXA`** — 永远不要`WidthType.PERCENTAGE`（与Google Docs不兼容）
- 表格宽度必须等于`columnWidths`的总和
- 单元格`width`必须匹配相应的`columnWidth`
- 单元格`margins`是内部内边距 - 它们减少内容区域，而不是添加到单元格宽度
- 对于全宽表格：使用内容宽度（页面宽度减去左右边距）

### 图像

```javascript
// 关键：type参数是必需的
new Paragraph({
  children: [new ImageRun({
    type: "png", // 必需：png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "标题", description: "描述", name: "名称" } // 所有三个都是必需的
  })]
})
```

### 分页符

```javascript
// 关键：PageBreak必须在Paragraph内部
new Paragraph({ children: [new PageBreak()] })

// 或使用pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("新页面")] })
```

### 目录

```javascript
// 关键：标题必须仅使用HeadingLevel - 没有自定义样式
new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" })
```

### 页眉/页脚

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1英寸
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("页眉")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("页码 "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* 内容 */]
}]
```

### docx-js的关键规则

- **显式设置页面大小** - docx-js默认为A4；对于US文档使用US Letter（12240 x 15840 DXA）
- **横向：传递纵向尺寸** - docx-js在内部交换宽度/高度；将短边作为`width`传递，长边作为`height`传递，并设置`orientation: PageOrientation.LANDSCAPE`
- **绝不使用`\n`** - 使用单独的Paragraph元素
- **绝不使用unicode项目符号** - 使用带有编号配置的`LevelFormat.BULLET`
- **PageBreak必须在Paragraph中** - 独立创建无效XML
- **ImageRun需要`type`** - 始终指定png/jpg等
- **始终使用DXA设置表格`width`** - 永远不要使用`WidthType.PERCENTAGE`（在Google Docs中中断）
- **表格需要双重宽度** - `columnWidths`数组和单元格`width`，两者必须匹配
- **表格宽度 = columnWidths的总和** - 对于DXA，确保它们完全相加
- **始终添加单元格边距** - 使用`margins: { top: 80, bottom: 80, left: 120, right: 120 }`以获得可读的内边距
- **使用`ShadingType.CLEAR`** - 永远不要SOLID用于表格着色
- **TOC仅需要HeadingLevel** - 标题段落上没有自定义样式
- **覆盖内置样式** - 使用精确ID："Heading1"、"Heading2"等
- **包含`outlineLevel`** - 目录所需（H1为0，H2为1等）

---

## 编辑现有文档

**按顺序遵循所有3个步骤。**

### 步骤1：解包
```bash
python scripts/office/unpack.py document.docx unpacked/
```
提取XML，美化打印，合并相邻的运行，并将智能引号转换为XML实体（`&#x201C;`等），以便它们在编辑中幸存。使用`--merge-runs false`跳过运行合并。

### 步骤2：编辑XML

编辑`unpacked/word/`中的文件。见下文XML参考以获取模式。

**使用"Claude"作为作者**进行修订和批注，除非用户明确要求使用不同的名称。

**直接使用Edit工具进行字符串替换。不要编写Python脚本。**脚本引入不必要的复杂性。Edit工具确切显示正在替换的内容。

**关键：对新内容使用智能引号。**当添加带有撇号或引号的文本时，使用XML实体生成智能引号：
```xml
<!-- 使用这些实体以获得专业的排版 -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```
| 实体 | 字符 |
|--------|-----------|
| `&#x2018;` | '（左单引号） |
| `&#x2019;` | '（右单引号/撇号） |
| `&#x201C;` | "（左双引号） |
| `&#x201D;` | "（右双引号） |

**添加批注：**使用`comment.py`处理多个XML文件的样板（文本必须是预转义的XML）：
```bash
python scripts/comment.py unpacked/ 0 "带有&amp;和&#x2019;的批注文本"
python scripts/comment.py unpacked/ 1 "回复文本" --parent 0  # 回复批注0
python scripts/comment.py unpacked/ 0 "文本" --author "自定义作者"  # 自定义作者名称
```
然后将标记添加到document.xml（见XML参考中的批注）。

### 步骤3：打包
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
使用自动修复进行验证，压缩XML，并创建DOCX。使用`--validate false`跳过。

**自动修复将修复：**
- `durableId` >= 0x7FFFFFFF（重新生成有效ID）
- `<w:t>`上缺少`xml:space="preserve"`，带有空白

**自动修复不会修复：**
- 格式错误的XML、无效的元素嵌套、缺少的关系、模式违规

### 常见陷阱

- **替换整个`<w:r>`元素**：添加修订时，用`<w:del>...<w:ins>...`作为兄弟替换整个`<w:r>...</w:r>`块。不要在运行中注入修订标记。
- **保留`<w:rPr>`格式化**：将原始运行的`<w:rPr>`块复制到修订运行中以保持粗体、字体大小等。

---

## XML参考

### 模式合规性

- **`<w:pPr>`中的元素顺序**：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`、`<w:rPr>`最后
- **空白**：将`xml:space="preserve"`添加到带有前导/尾随空白的`<w:t>`
- **RSIDs**：必须是8位十六进制（例如：`00AB1234`）

### 修订

**插入：**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>插入的文本</w:t></w:r>
</w:ins>
```

**删除：**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>
```

**在`<w:del>`内部**：使用`<w:delText>`而不是`<w:t>`，并使用`<w:delInstrText>`而不是`<w:instrText>`。

**最小编辑** - 仅标记更改的内容：
```xml
<!-- 将"30天"更改为"60天" -->
<w:r><w:t>期限是 </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> 天。</w:t></w:r>
```

**删除整个段落/列表项** - 从段落中删除所有内容时，也将段落标记标记为已删除，以便它与下一段落合并。在`<w:pPr><w:rPr>`内添加`<w:del/>`：
```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- 列表编号（如果存在） -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>正在删除的整个段落内容...</w:delText></w:r>
  </w:del>
</w:p>
```
如果没有`<w:pPr><w:rPr>`中的`<w:del/>`，接受更改会留下一个空段落/列表项。

**拒绝另一个作者的插入** - 在他们的插入内嵌套删除：
```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>他们插入的文本</w:delText></w:r>
  </w:del>
</w:ins>
```

**恢复另一个作者的删除** - 在删除后添加插入（不要修改他们的删除）：
```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>删除的文本</w:t></w:r>
</w:ins>
```

### 批注

运行`comment.py`后（见步骤2），将标记添加到document.xml。对于回复，使用`--parent`标志并将标记嵌套在父标记内。

**关键：`<w:commentRangeStart>`和`<w:commentRangeEnd>`是`<w:r>`的兄弟，永远不在`<w:r>`内部。**

```xml
<!-- 批注标记是w:p的直接子元素，永远不在w:r内部 -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>已删除</w:delText></w:r>
</w:del>
<w:r><w:t> 更多文本</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- 批注0，其中嵌套了回复1 -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>文本</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### 图像

1. 将图像文件添加到`word/media/`
2. 将关系添加到`word/_rels/document.xml.rels`：
```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```
3. 将内容类型添加到`[Content_Types].xml`：
```xml
<Default Extension="png" ContentType="image/png"/>
```
4. 在document.xml中引用：
```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMU：914400 = 1英寸 -->
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
- **LibreOffice**：PDF转换（通过`scripts/office/soffice.py`为沙盒环境自动配置）
- **Poppler**：`pdftoppm`用于图像
