---
name: docx
description: "当用户想要创建、读取、编辑或操作 Word 文档（.docx 文件）或 Word 模板（.dotx 文件）时使用此技能。触发条件包括：任何提及 'Word doc'、'word document'、'.docx'、'.dotx'，或请求生成带有目录、标题、页码或信头等格式的专业文档。在从 .docx 或 .dotx 文件中提取或重组内容、在文档中插入或替换图片、在 Word 文件中执行查找和替换、处理修订（tracked changes）或批注，或将内容转换为精美的 Word 文档时，也应使用此技能。如果用户要求以 Word 或 .docx 文件形式提供'报告'、'备忘录'、'信函'、'模板'或类似交付物，请使用此技能。不要用于 PDF、电子表格、Google Docs 或与文档生成无关的一般编码任务。"
license: 专有许可。完整条款见 LICENSE.txt
---

# DOCX 创建、编辑和分析

`.docx` 是一个由 XML 文件组成的 ZIP 压缩包。根据任务选择方法：

| 任务 | 方法 |
|---|---|
| **创建**新文档 | 编写一个 `docx`（npm）脚本——参见下面的注意事项 |
| **编辑**现有文档 | `unzip` → 编辑 `word/document.xml` → `zip`（docx-js 无法打开现有文件） |
| **读取**内容 | `pandoc -t markdown file.docx` |

> 下文中的脚本路径都是相对于此技能目录的。

## 使用 docx-js 创建——注意事项

`docx` 已预先安装——不要先运行 `npm install`；直接编写脚本并 `require('docx')`。只有当 require 失败时才执行：`npm install docx`。模型了解该 API；以下是容易踩的坑：

- **页面尺寸默认为 A4。** 如需美国信纸（US Letter），设置 `page: { size: { width: 12240, height: 15840 } }`（单位为 DXA；1440 = 1 英寸）。
- **横向：** 传入纵向尺寸并设置 `orientation: PageOrientation.LANDSCAPE`——docx-js 会在内部交换宽高。
- **表格需要双重宽度：** 在表格上设置 `columnWidths`，并且在每个单元格上设置 `width`，两者都使用 `WidthType.DXA`（PERCENTAGE 在 Google Docs 中会出问题）。各列宽度之和必须等于表格宽度。
- **表格底纹：** 使用 `ShadingType.CLEAR`，绝不要使用 `SOLID`（会渲染成黑色）。
- **列表：** 绝不要直接插入 `•` 字符；使用带有 `LevelFormat.BULLET` 的 `numbering` 配置。
- **`ImageRun` 必须提供 `type:`**（`"png"`、`"jpg"` 等）。
- **`PageBreak` 必须放在 `Paragraph` 内部。**
- **绝不要使用 `\n`**——改用多个独立的 `Paragraph` 元素。
- **目录（TOC）：** 标题必须使用内置的 `HeadingLevel.*`；自定义标题样式需要设置 `outlineLevel`，否则不会出现在目录中。
- **不要用表格充当水平线**——改用段落的下边框。
- **点状前导符 / 同一行右对齐：** 在 `TextRun` 中使用 `PositionalTab`（`alignment: PositionalTabAlignment.RIGHT`，`leader: PositionalTabLeader.DOT`），而不是用字面的 `.` 或空格来填充。

## 验证输出

写好 `.docx` 后，将其渲染出来并查看：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 100 output.pdf page
ls page-*.jpg   # 然后读取这些图片
```

`pdftoppm` 会按照总页数的位数为页码补零（`page-01.jpg`…`page-12.jpg`）。

## 编辑现有文档

旧版 `.doc` 文件必须先转换：`python scripts/office/soffice.py --headless --convert-to docx file.doc`。

```bash
unzip -q doc.docx -d unpacked/
find unpacked -type l -delete   # 删除符号链接条目——来自外部的 docx 不可信
python scripts/merge_runs.py unpacked/   # 合并碎片化的 run，以便能查找到文本
# 原地编辑 unpacked/word/document.xml——不要重新格式化或美化输出
(cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
python scripts/office/validate.py out.docx --original doc.docx   # XSD 检查；--auto-repair 可修复常见问题
# 做修订标记（redlining）？添加 --author "<你做修订时使用的名字>"，以检查每一处编辑都被跟踪
```

Word 会把文本拆分到许多 `<w:r>` run 中（修订 ID、拼写检查标记等），因此你在文档中看到的一个短语，在 XML 中往往并不是一个连续的字符串。`merge_runs.py` 会合并 `word/document.xml` 中相邻且格式相同的 run，而不改变内容或渲染效果；它也可以直接接受 `.docx` 文件（`python scripts/merge_runs.py doc.docx -o merged.docx`）。

**修订（Tracked changes）：** 做修订标记时，使用 `--author "<你做修订时使用的名字>"` 进行验证（需要 `--original`）——它会报告任何你修改了但外面没有 `<w:ins>`/`<w:del>` 包裹的文本，这种情况很容易无意中发生，并且在"接受修订"视图中是看不出来的。用带有 `w:id`、`w:author`、`w:date` 属性的 `<w:ins>`/`<w:del>` 包裹 run。在 `<w:del>` 内部，文本元素是 `<w:delText>`，而不是 `<w:t>`。被删除的段落标记（`<w:pPr><w:rPr><w:del w:id=".." w:author=".." w:date=".."/></w:rPr></w:pPr>`）表示"将此段落合并到下一段"——因此要彻底删除一个段落，就需要这个标记，再加上在每个 run 外面包裹 `<w:del>`。`<w:del/>` 必须位于 rPr 其他子元素之前；它们的顺序由 schema 强制规定。

要生成接受了所有修订的干净副本：`python scripts/accept_changes.py in.docx out.docx`。

接受一个被删除的段落标记时，应将该段落与其下方的段落合并，因此一个所有 run *全部*被删除的段落会消失。Word 是这样处理的；而 `accept_changes.py` 和 `pandoc --track-changes=accept` 并不总是如此。两者的失败方式相同——它们删除了被删除的文本，但留下了被清空的段落，如果该段落是自动编号的，看起来就像一个多余的空项目符号：

- `pandoc --track-changes=accept` 从不合并段落。
- `accept_changes.py`（LibreOffice）能正确合并，除非被删除的段落后面紧跟着一个空的间隔段落。

在这两种视图中出现的空项目符号是该视图造成的伪影，而不是文档本身的缺陷。请在 XML 中检查段落删除情况。

## 批注

批注需要六个相互关联的文件。请使用辅助脚本——如果你还要编辑 `document.xml`，使用目录模式（可省去一次解压/重新压缩）；否则使用直接处理 `.docx` 的模式：

```bash
# 针对已解压的目录（同时需要放置标记时首选）
python scripts/comment.py unpacked/ "Fees & expenses cap is too low"
python scripts/comment.py unpacked/ "Agreed" --parent 0

# 直接针对 .docx
python scripts/comment.py contract.docx "This cap is too low" -o annotated.docx
```

该脚本会写入 `comments.xml`、`commentsExtended.xml`、`commentsIds.xml`、`commentsExtensible.xml`、相关的关系文件以及内容类型覆盖项。批注 ID 会自动分配。然后它会打印出需要添加到 `word/document.xml` 中的 `<w:commentRangeStart>`/`<w:commentRangeEnd>`/`<w:commentReference>` 代码片段，以便将批注锚定到特定文本——在你放置这些标记之前，批注虽然存在，但不可见。

## 依赖项

`docx`（npm，已预装——仅当 `require('docx')` 失败时才安装）· `pandoc` · LibreOffice（`soffice`）· `pdftoppm`（Poppler）
