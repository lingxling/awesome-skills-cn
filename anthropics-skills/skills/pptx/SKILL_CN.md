---
name: pptx
description: "只要以任何方式涉及 .pptx 或 .potx 文件——作为输入、输出或两者兼有——就使用此技能。这包括：创建幻灯片、路演文稿或演示文稿；从任何 .pptx 或 .potx 文件中读取、解析或提取文本（即使提取的内容将用于其他地方，例如电子邮件或摘要）；编辑、修改或更新现有演示文稿；合并或拆分幻灯片文件；处理模板（.potx）、版式、演讲者备注或批注。只要用户提到\"deck\"、\"slides\"、\"presentation\"，或提及 .pptx 或 .potx 文件名，无论之后打算如何使用这些内容，都应触发此技能。如果需要打开、创建或改动 .pptx 或 .potx 文件，请使用此技能。"
license: 专有许可。完整条款见 LICENSE.txt
---

# PPTX 创建、编辑和分析

`.pptx` 是一个由 XML 文件组成的 ZIP 压缩包。根据任务选择方法：

| 任务 | 方法 |
|---|---|
| **创建**新的演示文稿 | 编写一个 `pptxgenjs` 脚本——参见下面的注意事项 |
| **编辑**现有演示文稿，或基于模板构建 | 解压 → 编辑 `ppt/slides/slideN.xml` → 压缩 |
| **读取**内容 | `markitdown deck.pptx`（每张幻灯片一个块，位于 `<!-- Slide number: N -->` 标记之下）；可视化网格：`python scripts/thumbnail.py deck.pptx` |

## 脚本

路径都是相对于此技能目录的。其他一切都是普通的 Python、`node` 或 shell。

| 脚本 | 作用 |
|---|---|
| `scripts/thumbnail.py deck.pptx [prefix]` | 生成带标签的所有幻灯片网格图，用于挑选模板版式。仅支持 `.pptx`。请传入 `prefix`——它默认为 `thumbnails`，会覆盖同一目录中其他演示文稿生成的网格图 |
| `scripts/add_slide.py unpacked/ slide2.xml [--after slideN.xml]` | 复制一张幻灯片（或一个 `slideLayoutN.xml`），并完成所有包内登记工作。也可以配合 `-o out.pptx` 直接处理 `.pptx` |
| `scripts/clean.py unpacked/` | 删除不再被引用的幻灯片、媒体和关系文件。在 `<p:sldIdLst>` 最终确定**之后**运行 |
| `scripts/office/validate.py deck.pptx [--original src.pptx]` | 检查 schema、关系、内容类型、图表和幻灯片；每个失败项都会给出修复方法。对于任何基于模板生成的演示文稿，都要传入 `--original`——它会以模板为基线进行 schema 检查，这样模板自身的 XSD 错误就不会被当成你的错误 |
| `scripts/office/soffice.py --headless --convert-to pdf deck.pptx` | LibreOffice 包装器——直接运行 `soffice` 在此沙箱中会挂起 |

## 使用 pptxgenjs 创建——注意事项

`pptxgenjs` 已预先安装——不要先运行 `npm install`；直接编写脚本并 `require('pptxgenjs')`。只有当 require 失败时才执行：`npm install pptxgenjs`。模型了解该 API；以下是容易踩的坑：

- **在添加幻灯片之前设置 `pres.layout`。** 默认画布是 `LAYOUT_16x9` = **10" × 5.625"**，而不是 13.3" 宽。超出边缘的坐标会被照样写入，而不会被截断——形状只是不在幻灯片上而已。（`LAYOUT_WIDE` 是 13.3" × 7.5"。）
- **十六进制颜色：绝不加 `#`，绝不用 8 位。** `color: "FF0000"`。`"#FF0000"` 以及把透明度写进十六进制值（`"00000020"`）这两种写法都会**损坏文件**。要实现半透明：填充和图片使用 `transparency: 0-100`，阴影使用 `opacity: 0.0-1.0`——用在对方身上都会被静默忽略。
- **pptxgenjs 会原地修改选项对象**（首次使用时会把数值转换为 EMU）。绝不要在两次 `add*` 调用之间共用同一个 `shadow`/选项对象——每次都新建一个对象。
- **阴影的 `offset` 必须 ≥ 0**——负的 offset 会损坏文件。要让阴影向上投射，使用 `angle: 270` 配合正的 offset。
- **`letterSpacing` 会被静默忽略**——真正的选项是 `charSpacing`。
- **列表：** 在每个条目上设置 `bullet: true`，绝不要使用字面的 `•`（会渲染出双重项目符号）。除最后一个条目外，在每个数组条目上设置 `breakLine: true`。用 `paraSpaceAfter` 而不是 `lineSpacing`（会产生巨大间隙）来调整带项目符号段落之间的间距。
- **每个输出文件一个 `new pptxgen()`**——绝不要重复使用同一个实例。
- **`rectRadius` 只对 `ROUNDED_RECTANGLE` 有效**，对 `RECTANGLE` 无效。
- **不支持渐变填充**——改用一张渐变图片作为背景。
- **文本框自带内边距**——当文字必须与同一 x 坐标上的形状、线条或图标对齐时，设置 `margin: 0`。
- **演讲者备注放在 `slide.addNotes("...")` 中**（纯文本，每张幻灯片一次），绝不要放在幻灯片上的文本框里。
- **保持图表为原生图表。** 对于 PowerPoint 能绘制的一切图表都使用 `addChart()`（组合图表传入一个 `{type, data, options}` 数组）。对于该库没有暴露的 PowerPoint 原生功能（趋势线、误差线），自己计算额外的数据系列，或对生成的 OOXML 进行后处理——不要退而使用渲染好的图片。只有 PowerPoint 没有原生形式的图表类型（桑基图、网络图、弦图）才以图片形式插入。
- **默认图表渲染得很简陋**——没有标题、没有数据标签、配色过时。设置 `showTitle` + `title`、`showValue: true` + `dataLabelPosition`、来自你调色板的 `chartColors: [...]`，并让图框保持低调（`catAxisLabelColor`/`valAxisLabelColor`、`valGridLine: { color, size }`、`catGridLine: { style: "none" }`，单一数据系列时设置 `showLegend: false`）。
- **在堆积条形图或堆积柱形图上，`dataLabelPosition` 必须是 `ctr`、`inEnd` 或 `inBase`。** `outEnd` 会**损坏文件**。
- **使用 `secondaryValAxis`/`secondaryCatAxis` 的组合图表系列，需要在图表选项中同时提供 `valAxes` 和 `catAxes`，且各有两个条目。** 如果没有，pptxgenjs 会写入从未声明过的坐标轴 *id*，PowerPoint 会**丢弃该图表**并报告文件已损坏。只提供 `valAxes` 是不够的。
- **在 `writeFile()` 之后，运行 `python scripts/office/validate.py deck.pptx`。** 它会报告上面两个图表问题以及 PowerPoint 拒绝接受的幻灯片 XML 缺陷，并为每个问题给出修复方法。在生成器中修复它们，而不是手动编辑打包后的 XML。
- **绝不要调整 `<p:presentation>` 子元素的顺序。** pptxgenjs 会把 `<p:notesMasterIdLst>` 写在 `<p:sldIdLst>` 之后，并让两个母版指向同一个主题部件。PowerPoint 能正常读取——但移动这个元素，同一个演示文稿就会无法打开。
- **图标：** 将 `react-icons` 渲染为 SVG（`ReactDOMServer.renderToStaticMarkup`），用 `sharp` 以 ≥256px 栅格化，然后通过 `addImage({ data: "image/png;base64," + buf.toString("base64") })` 插入——`image/png;base64,` 前缀是必需的（`react-icons`、`react`、`react-dom` 和 `sharp` 都已预装——只有当 require 失败时才执行 `npm install react-icons react react-dom sharp`）。

## 编辑现有演示文稿和模板

先挑选版式：`python scripts/thumbnail.py template.pptx template-thumbs` 会生成带标签的所有幻灯片网格图，并打印出它创建的文件——`template-thumbs.jpg`，超过 12 张幻灯片时会拆分为 `template-thumbs-N.jpg`。**始终传入第二个参数，并以演示文稿的名字命名。** 它默认为 `thumbnails`，所以在同一目录中为两个演示文稿生成缩略图时，会静默覆盖彼此的网格图——第一个演示文稿的网格图就直接没了（仅用于模板分析——视觉质检需要[转换为图片](#转换为图片)中的全分辨率渲染图；它只接受 `.pptx`，所以要先把 `.potx` 复制为 `.pptx` 文件名）。把它和 `markitdown` 一起使用，将每个内容部分映射到一张模板幻灯片上，并让版式多样化——不要把每个部分都放在同一种"标题加项目符号"的幻灯片上。

```bash
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" deck.pptx
python scripts/add_slide.py unpacked/ slide2.xml --after slide2.xml   # 复制一张幻灯片（或 slideLayoutN.xml）；打印新幻灯片的路径
# 调整顺序 / 删除幻灯片 = 编辑 ppt/presentation.xml 中的 <p:sldIdLst>
python scripts/clean.py unpacked/                                     # 删除之后：移除孤立的幻灯片、媒体、关系文件
# 在 ppt/slides/slideN.xml 中编辑幻灯片内容
(cd unpacked && rm -f ../out.pptx && zip -Xr ../out.pptx .)           # 在目录内部进行压缩；先 rm，否则已删除的部件会残留
python scripts/office/validate.py out.pptx --original deck.pptx
```

- **在编辑任何幻灯片的内容之前，完成所有结构性工作——添加、删除、调整顺序。** `add_slide.py` 会原样复制幻灯片文件，所以在编辑之后再复制会克隆已编辑的内容；而 `clean.py` 会删除任何不在 `<p:sldIdLst>` 中的幻灯片，包括你刚刚写好的那张。
- **绝不要手动复制幻灯片文件**——`add_slide.py` 会完成新幻灯片所需的全部登记，并报告它创建了什么（`Created ppt/slides/slide17.xml from slide2.xml`）。它也可以直接处理文件：`add_slide.py deck.pptx slide2.xml -o out.pptx`——**一定要传入 `-o`，否则它会原地重写输入的演示文稿。** 被复制的幻灯片仍然*引用*源幻灯片的图表/SmartArt/嵌入对象部件，而不是克隆它们，所以编辑其中一张幻灯片的图表会改变另一张的图表。
- **如果你使用 `python-pptx`**，有三件事它做不到：复制幻灯片（它唯一的入口是 `add_slide(layout)`）、通过 `text_frame.text = "..."` 保留格式（这会把段落合并成一个没有样式的 run——应改为给 `run.text` 赋值），以及读取大多数模板美术素材所用的 SVG/EMF（`add_picture` 会抛出 `UnidentifiedImageError`）。
- 旧版 `.ppt` 必须先转换：`python scripts/office/soffice.py --headless --convert-to pptx file.ppt`。`.potx` 模板的解包和打包方式完全相同——输出文件保留 `.potx` 扩展名。
- 要复用模板中的某个图标或图片，复制一张已经包含它的幻灯片或版式。

填充模板时：

- 如果你用脚本进行 XML 转换，请使用 `defusedxml.minidom` 解析——通过 `xml.etree.ElementTree` 往返处理 OOXML 会重写命名空间前缀并损坏演示文稿。
- **模板槽位 ≠ 源内容条目。** 如果模板展示了 4 位团队成员而你只有 3 位，就删除第 4 位成员的整个组合（图片 + 文本框），而不只是删除其文字——然后在质检时检查是否有孤立的视觉元素。
- 每个列表条目一个 `<a:p>`——绝不要把多个条目拼接到一个段落中。复制相邻的 `<a:pPr>` 以保留间距，并在标题、章节标题和行内标签（`Status:`、`Owner:`）的 `<a:rPr>` 上设置 `b="1"`。
- 让项目符号从版式继承；只有在需要覆盖时才添加 `<a:buChar>`、`<a:buAutoNum>`（编号）或 `<a:buNone>`——绝不要在文本中使用字面的 `•`。
- 带有前导或尾随空格的文本，需要在其 `<a:t>` 上设置 `xml:space="preserve"`。

## 设计思路

**不要做无聊的幻灯片。** 白色背景上的普通项目符号打动不了任何人。为每张幻灯片考虑以下列表中的思路。

### 开始之前

- **选择大胆、贴合内容的配色**：调色板应该让人感觉是专门为这个主题设计的。如果把你的配色换到一份完全不同的演示文稿上仍然"可行"，说明你的选择还不够具体。
- **主次分明而非平均分配**：一种颜色应占主导（60-70% 的视觉比重），搭配 1-2 种辅助色调和一种鲜明的强调色。绝不要让所有颜色比重相同。
- **深浅对比**：标题页和结论页使用深色背景，内容页使用浅色背景（"三明治"结构）。或者全程使用深色，营造高级感。
- **确定一个视觉母题**：选择一个独特的元素并重复使用——圆角图片框、彩色圆圈中的图标。在每张幻灯片上贯彻它。**不要用色条或强调条纹作为母题**（参见"避免"列表）。

### 配色方案

选择与主题相符的颜色——不要默认使用千篇一律的蓝色。可以把这些调色板作为灵感：

| 主题 | 主色 | 辅助色 | 强调色 |
|-------|---------|-----------|--------|
| **午夜高管（Midnight Executive）** | `1E2761`（海军蓝） | `CADCFC`（冰蓝） | `FFFFFF`（白色） |
| **森林与苔藓（Forest & Moss）** | `2C5F2D`（森林绿） | `97BC62`（苔藓绿） | `F5F5F5`（奶油色） |
| **珊瑚活力（Coral Energy）** | `F96167`（珊瑚色） | `F9E795`（金色） | `2F3C7E`（海军蓝） |
| **暖陶土（Warm Terracotta）** | `B85042`（陶土色） | `E7E8D1`（沙色） | `A7BEAE`（鼠尾草绿） |
| **海洋渐变（Ocean Gradient）** | `065A82`（深蓝） | `1C7293`（蓝绿） | `21295C`（午夜蓝） |
| **炭灰极简（Charcoal Minimal）** | `36454F`（炭灰） | `F2F2F2`（米白） | `212121`（黑色） |
| **蓝绿信任（Teal Trust）** | `028090`（蓝绿） | `00A896`（海沫绿） | `02C39A`（薄荷绿） |
| **浆果与奶油（Berry & Cream）** | `6D2E46`（浆果色） | `A26769`（灰玫瑰色） | `ECE2D0`（奶油色） |
| **鼠尾草宁静（Sage Calm）** | `84B59F`（鼠尾草绿） | `69A297`（桉树绿） | `50808E`（石板灰） |
| **樱桃醒目（Cherry Bold）** | `990011`（樱桃红） | `FCF6F5`（米白） | `2F3C7E`（海军蓝） |

### 针对每张幻灯片

**每张幻灯片都需要一个视觉元素**——图片、图表、图标或形状。纯文字的幻灯片令人过目即忘。

**版式选项：**
- 两栏（左侧文字，右侧插图）
- 图标 + 文字行（彩色圆圈中的图标、粗体标题、下方说明）
- 2x2 或 2x3 网格（一侧图片，另一侧为内容块网格）
- 半出血图片（占满左侧或右侧）并叠加内容

**数据展示：**
- 大号统计数字标注（60-72pt 的大数字，下方配小标签）
- 对比栏（前/后、优/缺点、并排选项）
- 时间线或流程图（编号步骤、箭头）

**视觉润色：**
- 章节标题旁边放置小彩色圆圈中的图标
- 用斜体强调文字突出关键数据或标语

### 字体

**你写入 .pptx 的字体名称，是由用户的 PowerPoint 渲染的，而不是由当前环境渲染的。** 你的视觉质检通过 LibreOffice 渲染，它会替换掉自己没有的字体——而对于某些字体，替代字体的宽度不同，因此你的质检预览可能会显示出真实演示文稿中并不存在的文字溢出（或恰好放得下）。为了让质检结果可信：

- **安全字体**（在质检中按真实宽度渲染，*并且*随 Office 一起提供）：**Arial、Calibri、Cambria、Times New Roman、Courier New、Bookman Old Style、Century Schoolbook**。正文以及任何需要考虑是否放得下的地方都使用这些字体。
- **零质检风险、又有个性的标题**：用安全列表中的衬线字体做标题（Cambria、Bookman Old Style、Century Schoolbook），搭配安全列表中的无衬线字体做正文（Calibri 或 Arial）。这样既能获得视觉对比，又不会牺牲可靠的溢出检查。
- **如果用户要求使用安全列表之外的字体**（例如 Georgia 或 Trebuchet MS）：在用户要求的地方使用它，但为这些容器预留额外空间（约 10%），并且不要相信质检对这些元素文字是否放得下的判断——该字体的预览只是近似的。如果用户没有指定，正文优先使用安全列表中的字体。
- **质检不可靠的字体**（替代字体宽度不同——溢出检查可能出错）：Georgia、Trebuchet MS、Impact、Arial Black、Garamond、Consolas、Palatino Linotype。Calibri Light 的替代效果因环境而异；视为质检不可靠。在留有余量的情况下用于标题/强调没问题；但不要相信质检对这些字体文字是否放得下的判断。
- **绝不要默认使用 Aptos**——这是 Office 在 2023 年之后的默认字体，在这里没有度量兼容的替代字体，*而且*旧版 Office 中也没有它，所以两头都不可靠。

| 元素 | 字号 |
|---------|------|
| 幻灯片标题 | 36-44pt 粗体 |
| 章节标题 | 20-24pt 粗体 |
| 正文 | 14-16pt |
| 说明文字 | 10-12pt 柔和色 |

### 间距

- 最小页边距 0.5"
- 内容块之间 0.3-0.5"
- 留出呼吸空间——不要填满每一寸

### 避免（常见错误）

- **不要重复使用同一种版式**——在不同幻灯片之间变换分栏、卡片和标注
- **不要居中正文**——段落和列表左对齐；只有标题居中
- **不要在字号对比上吝啬**——标题需要 36pt 以上，才能从 14-16pt 的正文中脱颖而出
- **不要默认使用蓝色**——选择能体现具体主题的颜色
- **不要随意混用间距**——选择 0.3" 或 0.5" 的间隔并保持一致
- **不要只精心设计一张幻灯片而让其余的保持朴素**——要么全面投入，要么全程保持简洁
- **不要制作纯文字幻灯片**——添加图片、图标、图表或其他视觉元素；避免单纯的标题 + 项目符号
- **不要忘记文本框的内边距**——在让线条或形状与文字边缘对齐时，在文本框上设置 `margin: 0`，或偏移形状以抵消内边距
- **不要使用低对比度的元素**——图标和文字都需要与背景形成强烈对比；避免浅色背景上的浅色文字或深色背景上的深色文字
- **绝不要在标题下使用强调线**——这是 AI 生成幻灯片的标志性特征；改用留白或背景色
- **绝不要添加装饰性的色条或强调条纹**——这包括：横跨幻灯片宽度的页眉/页脚色条、沿幻灯片一侧边缘的竖直侧边条纹、沿卡片或内容块一侧边缘的细强调条纹，以及矩形上的"单侧边框"。这些看起来就像 AI 生成的填充物。如果想让某张卡片与众不同，使用淡淡的背景色调、投影或图标——而不是边缘条纹。
- **不要默认使用奶油色/米色背景**——在没有指定背景时，使用白色（`FFFFFF`）或用户的品牌配色；避免 `F5F5DC`、`FAF0E6`、`FAEBD7`、`FFF8E1` 这类暖中性色的默认值
- **不要交付文字溢出其形状的文件**——如果文字放不下，就缩小字号、拆分到多张幻灯片，或放大容器；绝不要让内容被截断或溢出边界

## 质检（必需）

你的首次渲染通常会有几个真实存在的问题——重叠、溢出、未对齐。找到并修复它们，只重新渲染你修改过的幻灯片，然后就停止。

### 内容质检

```bash
markitdown output.pptx
```

检查是否有内容缺失、拼写错误、顺序错误。

**使用模板时，检查是否有残留的占位文字：**

```bash
markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|this.*(page|slide).*layout"
```

如果 grep 返回了结果，在宣布完成之前先修复它们。

### 文件质检（必需）

```bash
python scripts/office/validate.py output.pptx                      # 从零构建
python scripts/office/validate.py output.pptx --original src.pptx  # 基于模板构建
```

**如果演示文稿来自模板，始终传入 `--original`。** 模板本身可能包含 XSD 拒绝的部件，
因此不带该参数运行时，可能会报告出并非由你造成的失败——而真正的回归问题可能就隐藏在其中。
`--original` 会以模板为基线进行 schema 和幻灯片检查，屏蔽模板原本就有的错误。
结构性检查——关系、内容类型、图表——会忽略 `--original`，无论如何都会报告从模板继承的问题，
所以要根据这些问题本身的情况来判断。

pptxgenjs 会生成 PowerPoint 拒绝打开、但其他所有工具都能接受的图表 XML：
python-pptx 能打开这些演示文稿，LibreOffice 能渲染它们，XSD 也能通过。
每个失败项都会给出修复方法。在生成器中修复，然后重新构建。

### 视觉质检

将幻灯片转换为图片（参见[转换为图片](#转换为图片)），并逐张检查。盯着生成代码看了一段时间之后，你往往会看到自己预期的东西，而不是实际渲染出来的东西，所以要以全新的眼光看这些图片（如果你有子代理，用子代理来做这件事效果很好）。需要查找的用户可见缺陷：

- **文字溢出，或文字在文本框或幻灯片边界处被截断——首先检查这一项。** 这是最常见的缺陷，而且总是用户可见的。（对于"字体"一节中提到的预览渲染不可靠的字体，预览只是近似的：相信你预留的约 10% 余量，而不是它表面上是否放得下。）
- 元素重叠（文字穿过形状、线条穿过文字、元素堆叠在一起）
- 来源引用或页脚与上方内容相互碰撞
- 元素之间过近（间隔 < 0.3"），或卡片/区块几乎挨在一起
- 间隔不均匀（某处大片空白，另一处却很拥挤）
- 与幻灯片边缘的边距不足（< 0.5"）
- 分栏或同类元素没有一致地对齐
- 低对比度的文字（例如奶油色背景上的浅灰色文字）
- 替换文字后模板装饰位置错乱——例如标题下划线是按一行标题定位的，但替换后的标题换成了两行
- 低对比度的图标（例如深色背景上的深色图标，且没有对比色圆圈衬托）
- 文本框太窄导致过度换行
- 残留的占位内容

## 转换为图片

将演示文稿转换为单张幻灯片图片，以便进行视觉检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

**将上面打印出的绝对路径直接传给查看工具。** `rm` 用于清除之前运行留下的旧图片。`pdftoppm` 会根据页数补零：少于 10 页的演示文稿为 `slide-1.jpg`，10-99 页为 `slide-01.jpg`，100 页以上为 `slide-001.jpg`。

**修复之后，重新运行上面全部四条命令**——必须先从编辑后的 `.pptx` 重新生成 PDF，`pdftoppm` 才能反映你的修改。

## 依赖项

`pptxgenjs`（npm，已预装——仅当 `require('pptxgenjs')` 失败时才安装）· `markitdown[pptx]`、`Pillow`、`defusedxml`、`lxml`（pip——文本导出、缩略图、清理、验证）· LibreOffice（`soffice`，通过 `scripts/office/soffice.py` 为沙箱环境自动配置）· `pdftoppm`（Poppler）
