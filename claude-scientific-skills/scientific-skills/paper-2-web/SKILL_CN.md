---
name: paper-2-web
description: 此技能应用于将学术论文转换为促销和展示格式，包括交互式网站（Paper2Web）、演示视频（Paper2Video）和会议海报（Paper2Poster）。用于涉及论文传播、会议准备、创建可探索的学术主页、生成视频摘要或从 LaTeX 或 PDF 源生成可打印的海报的任务。
allowed-tools: Read Write Edit Bash
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Paper2All：学术论文转换管道

## 概述

此技能通过 Paper2All 自主管道将学术论文转换为多种促销和展示格式。该系统将研究论文（LaTeX 或 PDF）转换为三种主要输出：

1. **Paper2Web**：具有布局感知设计的交互式、可探索的学术主页
2. **Paper2Video**：带有旁白、幻灯片和可选讲解人的专业演示视频
3. **Paper2Poster**：具有专业布局的可打印会议海报

该管道使用 LLM 驱动的内容提取、设计生成和迭代改进，创建适合会议、期刊、预印本存储库和学术推广的高质量输出。

## 何时使用此技能

当您需要以下情况时使用此技能：

- **创建会议材料**：学术会议的海报、演示视频和配套网站
- **推广研究**：将已发表的论文或预印本转换为可访问、引人入胜的网络格式
- **准备演示**：从论文内容生成视频摘要或完整的演示视频
- **传播发现**：为社交媒体、实验室网站或机构展示创建促销材料
- **增强预印本**：为 bioRxiv、arXiv 或其他预印本提交添加交互式主页
- **批处理**：同时为多篇论文生成促销材料

**触发短语**：
- "将此论文转换为网站"
- "从我的 LaTeX 论文生成会议海报"
- "从此研究创建视频演示"
- "为我的论文制作交互式主页"
- "将我的论文转换为促销材料"
- "为我的会议演讲生成海报和视频"

## 科学示意图的视觉增强

**使用此技能创建文档时，始终考虑添加科学图表和示意图以增强视觉交流。**

如果您的文档尚未包含示意图或图表：
- 使用 **scientific-schematics** 技能生成 AI 驱动的出版质量图表
- 只需用自然语言描述您想要的图表
- Nano Banana Pro 将自动生成、审查和完善示意图

**对于新文档**：应默认生成科学示意图，以可视化文本中描述的关键概念、工作流程、架构或关系。

**如何生成示意图**：
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

AI 将自动：
- 创建具有适当格式的出版质量图像
- 通过多次迭代进行审查和完善
- 确保可访问性（色盲友好、高对比度）
- 将输出保存在 figures/ 目录中

**何时添加示意图**：
- 论文转换管道图
- 网站布局架构图
- 视频制作工作流程插图
- 海报设计流程图表
- 内容提取图
- 系统架构可视化
- 任何受益于可视化的复杂概念

有关创建示意图的详细指导，请参考 scientific-schematics 技能文档。

---

## 核心功能

### 1. Paper2Web：交互式网站生成

将论文转换为布局感知、交互式学术主页，超越简单的 HTML 转换。

**关键功能**：
- 响应式、多部分布局，适应论文内容
- 交互式图表、表格和引用
- 带导航的移动友好设计
- 自动徽标发现（使用 Google Search API）
- 美学改进和质量评估

**最适合**：出版后推广、预印本增强、实验室网站、永久研究展示

→ **详见 `references/paper2web.md` 获取详细文档**

---

### 2. Paper2Video：演示视频生成

生成带有幻灯片、旁白、光标移动和可选讲解人视频的专业演示视频。

**关键功能**：
- 从论文结构自动生成幻灯片
- 自然声音合成
- 同步光标移动和高亮显示
- 可选使用 Hallo2 的讲解人视频（需要 GPU）
- 多语言支持

**最适合**：视频摘要、会议演示、在线讲座、课程材料、YouTube 推广

→ **详见 `references/paper2video.md` 获取详细文档**

---

### 3. Paper2Poster：会议海报生成

创建具有专业布局和视觉设计的可打印学术海报。

**关键功能**：
- 自定义海报尺寸（任何大小）
- 专业设计模板
- 机构品牌支持
- 链接的二维码生成
- 高分辨率输出（300+ DPI）

**最适合**：会议海报展示、研讨会、学术展览、虚拟会议

→ **详见 `references/paper2poster.md` 获取详细文档**

---

## 快速开始

### 先决条件

1. **安装 Paper2All**：
   ```bash
   git clone https://github.com/YuhangChen1/Paper2All.git
   cd Paper2All
   conda create -n paper2all python=3.11
   conda activate paper2all
   pip install -r requirements.txt
   ```

2. **配置 API 密钥**（创建 `.env` 文件）：
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   # 可选：GOOGLE_API_KEY 和 GOOGLE_CSE_ID 用于徽标搜索
   ```

3. **安装系统依赖**：
   - LibreOffice（文档转换）
   - Poppler 工具（PDF 处理）
   - NVIDIA GPU 48GB（可选，用于讲解人视频）

→ **详见 `references/installation.md` 获取完整安装指南**

---

### 基本用法

**生成所有组件**（网站 + 海报 + 视频）：
```bash
python pipeline_all.py \
  --input-dir "path/to/paper" \
  --output-dir "path/to/output" \
  --model-choice 1
```

**仅生成网站**：
```bash
python pipeline_all.py \
  --input-dir "path/to/paper" \
  --output-dir "path/to/output" \
  --model-choice 1 \
  --generate-website
```

**生成自定义尺寸的海报**：
```bash
python pipeline_all.py \
  --input-dir "path/to/paper" \
  --output-dir "path/to/output" \
  --model-choice 1 \
  --generate-poster \
  --poster-width-inches 60 \
  --poster-height-inches 40
```

**生成视频**（轻量级管道）：
```bash
python pipeline_light.py \
  --model_name_t gpt-4.1 \
  --model_name_v gpt-4.1 \
  --result_dir "path/to/output" \
  --paper_latex_root "path/to/paper"
```

→ **详见 `references/usage_examples.md` 获取综合工作流程示例**

---

## 工作流程决策树

使用此决策树确定要生成哪些组件：

```
用户需要论文的促销材料？
│
├─ 需要永久在线存在？
│  └─→ 生成 Paper2Web（交互式网站）
│
├─ 需要实体会议材料？
│  ├─→ 海报展示？ → 生成 Paper2Poster
│  └─→ 口头演示？ → 生成 Paper2Video
│
├─ 需要视频内容？
│  ├─→ 期刊视频摘要？ → 生成 Paper2Video（5-10 分钟）
│  ├─→ 会议演讲？ → 生成 Paper2Video（15-20 分钟）
│  └─→ 社交媒体？ → 生成 Paper2Video（1-3 分钟）
│
└─ 需要完整包？
   └─→ 生成所有三个组件
```

## 输入要求

### 支持的输入格式

**1. LaTeX 源**（推荐）：
```
paper_directory/
├── main.tex              # 主论文文件
├── sections/             # 可选：拆分章节
├── figures/              # 所有图表文件
├── tables/               # 表格文件
└── bibliography.bib      # 参考文献
```

**2. PDF**：
- 高质量 PDF，嵌入字体
- 可选择文本（非扫描图像）
- 高分辨率图表（首选 300+ DPI）

### 输入组织

**单篇论文**：
```bash
input/
└── paper_name/
    ├── main.tex (或 paper.pdf)
    ├── figures/
    └── bibliography.bib
```

**多篇论文**（批处理）：
```bash
input/
├── paper1/
│   └── main.tex
├── paper2/
│   └── main.tex
└── paper3/
    └── main.tex
```

## 常见参数

### 模型选择
- `--model-choice 1`：GPT-4（质量和成本的最佳平衡）
- `--model-choice 2`：GPT-4.1（最新功能，成本更高）
- `--model_name_t gpt-3.5-turbo`：更快，成本更低（质量可接受）

### 组件选择
- `--generate-website`：启用网站生成
- `--generate-poster`：启用海报生成
- `--generate-video`：启用视频生成
- `--enable-talking-head`：在视频中添加讲解人（需要 GPU）

### 自定义
- `--poster-width-inches [width]`：自定义海报宽度
- `--poster-height-inches [height]`：自定义海报高度
- `--video-duration [seconds]`：目标视频长度
- `--enable-logo-search`：自动机构徽标发现

## 输出结构

生成的输出按论文和组件组织：

```
output/
└── paper_name/
    ├── website/
    │   ├── index.html
    │   ├── styles.css
    │   └── assets/
    ├── poster/
    │   ├── poster_final.pdf
    │   ├── poster_final.png
    │   └── poster_source/
    └── video/
        ├── final_video.mp4
        ├── slides/
        ├── audio/
        └── subtitles/
```

## 最佳实践

### 输入准备
1. **尽可能使用 LaTeX**：提供最佳的内容提取和结构
2. **正确组织文件**：将所有资产（图表、表格、参考文献）保存在论文目录中
3. **高质量图表**：使用矢量格式（PDF、SVG）或高分辨率光栅（300+ DPI）
4. **干净的 LaTeX**：移除编译产物，确保源代码成功编译

### 模型选择策略
- **GPT-4**：最适合生产质量输出、会议、出版物
- **GPT-4.1**：当您需要最新功能或最佳可能质量时使用
- **GPT-3.5-turbo**：用于快速草稿、测试或简单论文

### 组件优先级
对于紧迫的截止日期，按以下顺序生成：
1. **网站**（最快，最多功能，约 15-30 分钟）
2. **海报**（中等速度，用于打印截止日期，约 10-20 分钟）
3. **视频**（最慢，可以稍后生成，约 20-60 分钟）

### 质量保证
在最终确定输出之前：
1. **网站**：在多个设备上测试，验证所有链接正常工作，检查图表质量
2. **海报**：打印测试页，验证 3-6 英尺距离的文本可读性，检查颜色
3. **视频**：观看整个视频，验证音频同步，在不同设备上测试

## 资源要求

### 处理时间
- **网站**：每篇论文 15-30 分钟
- **海报**：每篇论文 10-20 分钟
- **视频（无讲解人）**：每篇论文 20-60 分钟
- **视频（有讲解人）**：每篇论文 60-120 分钟

### 计算要求
- **CPU**：多核处理器，用于并行处理
- **RAM**：最低 16GB，大型论文推荐 32GB
- **GPU**：标准输出可选，讲解人需要（NVIDIA A6000 48GB）
- **存储**：每篇论文 1-5GB，取决于组件和质量设置

### API 成本（近似）
- **网站**：每篇论文 $0.50-2.00（GPT-4）
- **海报**：每篇论文 $0.30-1.00（GPT-4）
- **视频**：每篇论文 $1.00-3.00（GPT-4）
- **完整包**：每篇论文 $2.00-6.00（GPT-4）

## 故障排除

### 常见问题

**LaTeX 解析错误**：
- 确保 LaTeX 源成功编译：`pdflatex main.tex`
- 检查所有引用的文件是否存在
- 验证没有自定义包阻止解析

**图表质量差**：
- 使用矢量格式（PDF、SVG、EPS）代替光栅
- 确保光栅图像为 300+ DPI
- 检查图表在编译的 PDF 中正确渲染

**视频生成失败**：
- 验证有足够的磁盘空间（推荐 5GB+）
- 检查所有依赖项已安装（LibreOffice、Poppler）
- 查看输出目录中的错误日志

**海报布局问题**：
- 验证海报尺寸合理（24"-72" 范围）
- 检查内容长度（非常长的论文可能需要手动整理）
- 确保图表具有适合海报尺寸的适当分辨率

**API 错误**：
- 验证 `.env` 文件中的 API 密钥
- 检查 API 信用余额
- 确保没有速率限制（等待并重试）

## 平台特定功能

### 社交媒体优化

系统自动检测目标平台：

**Twitter/X**（英文，数字文件夹名称）：
```bash
mkdir -p input/001_twitter/
# 生成英文促销内容
```

**Xiaohongshu/小红书**（中文，字母数字文件夹名称）：
```bash
mkdir -p input/xhs_paper/
# 生成中文促销内容
```

### 会议特定格式

指定会议要求：
- 标准海报尺寸（4'×3'，5'×4'，A0，A1）
- 视频摘要长度限制（通常 3-5 分钟）
- 机构品牌要求
- 配色方案偏好

## 集成和部署

### 网站部署
将生成的网站部署到：
- **GitHub Pages**：带有自定义域名的免费托管
- **学术托管**：大学网络服务器
- **个人服务器**：AWS、DigitalOcean 等
- **Netlify/Vercel**：带有 CI/CD 的现代托管

### 海报打印
可打印文件适用于：
- 专业海报印刷服务
- 大学印刷店
- 在线服务（例如 Spoonflower、VistaPrint）
- 大幅面打印机（如果可用）

### 视频分发
在以下平台分享视频：
- **YouTube**：公开或未列出以获得最大覆盖范围
- **机构存储库**：大学视频平台
- **会议平台**：虚拟会议系统
- **社交媒体**：Twitter、LinkedIn、ResearchGate

## 高级用法

### 批处理
高效处理多篇论文：
```bash
# 在批处理目录中组织论文
for paper in paper1 paper2 paper3; do
    python pipeline_all.py \
      --input-dir input/$paper \
      --output-dir output/$paper \
      --model-choice 1 &
done
wait
```

### 自定义品牌
应用机构或实验室品牌：
- 在论文目录中提供徽标文件
- 在配置中指定配色方案
- 使用自定义模板（高级）
- 匹配会议主题要求

### 多语言支持
生成不同语言的内容：
- 在配置中指定目标语言
- 系统适当地翻译内容
- 为视频旁白选择适当的语音
- 使设计约定适应文化

## 参考资料和资源

此技能包括全面的参考文档：

- **`references/installation.md`**：完整的安装和配置指南
- **`references/paper2web.md`**：详细的 Paper2Web 文档，包含所有功能
- **`references/paper2video.md`**：综合的 Paper2Video 指南，包括讲解人设置
- **`references/paper2poster.md`**：完整的 Paper2Poster 文档，包含设计模板
- **`references/usage_examples.md`**：真实示例和工作流程模式

**外部资源**：
- GitHub 仓库：https://github.com/YuhangChen1/Paper2All
- 精选数据集：可在 Hugging Face 上获得（13 个研究类别）
- 基准套件：参考网站和评估指标

## 评估和质量指标

Paper2All 系统包括内置的质量评估：

### 内容质量
- **完整性**：论文内容的覆盖范围
- **准确性**：研究结果的忠实表示
- **清晰度**：可访问性和可理解性
- **信息性**：关键信息的突出性

### 设计质量
- **美学**：视觉吸引力和专业性
- **布局**：平衡、层次结构和组织
- **可读性**：文本清晰度和图表清晰度
- **一致性**：统一的样式和品牌

### 技术质量
- **性能**：加载时间、响应性
- **兼容性**：跨浏览器、跨设备支持
- **可访问性**：WCAG 合规性、屏幕阅读器支持
- **标准**：有效的 HTML/CSS、可打印的 PDF

所有输出在生成完成前都经过自动质量检查。