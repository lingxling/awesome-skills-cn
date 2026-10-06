---
name: infographics
description: "通过 OpenRouter 使用 Nano Banana 2 创建并审查信息图表。用于统计摘要、时间线、比较、流程，以及基于所提供数据或可选 Sonar 研究的可视化解释。支持十种布局、八种风格预设、参考图像，以及无障碍调色板起点。"
compatibility: Requires Python 3.10+ with requests installed, network access, and OPENROUTER_API_KEY for generation, review, or research.
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.10"
  last-reviewed: "2026-10-01"
  skill-author: K-Dense Inc.
  openclaw:
    primaryEnv: OPENROUTER_API_KEY
    envVars:
    - name: OPENROUTER_API_KEY
      required: false
      description: OpenRouter API key for the skill's LLM-powered steps.
---

# Infographics

## 概述

信息图表是信息、数据或知识的可视化表示形式，旨在快速、清晰地呈现复杂内容。
**此技能使用 Nano Banana 2 AI 生成信息图表，配合 Gemini 3.7 Flash 进行质量
审查，并使用 Perplexity Sonar 进行研究。**

**工作原理：**
- （可选）**研究阶段**：使用 Perplexity Sonar Pro 收集候选事实和来源记录
- 用自然语言描述你的信息图表
- Nano Banana 2 根据你的内容生成栅格草图
- **Gemini 3.7 Flash 对照文档类型阈值审查质量**
- **智能迭代**：当审查要求改进时，在迭代预算内重新生成
- 以预期的显示尺寸检查每一张最终图像，并对照来源核实各项陈述

**按文档类型划分的质量阈值：**
| 文档类型 | 阈值 | 说明 |
|---------------|-----------|-------------|
| marketing（营销） | 8.5/10 | 营销材料——必须有吸引力 |
| report（报告） | 8.0/10 | 商业报告——专业质量 |
| presentation（演示） | 7.5/10 | 幻灯片、演讲——清晰且引人入胜 |
| social（社交媒体） | 7.0/10 | 社交媒体内容 |
| internal（内部使用） | 7.0/10 | 内部使用 |
| draft（草稿） | 6.5/10 | 工作草稿 |
| default（默认） | 7.5/10 | 通用场景 |

**只需描述你想要的内容，Nano Banana 2 就会将其创建出来。**

## 快速开始

在你选定的 Python 环境中安装唯一的运行时依赖
（`python -m pip install requests`），然后设置 `OPENROUTER_API_KEY`。下面
的示例展示了 CLI 用法；本次审查期间未执行付费生成。脚本只接受 PNG 输出
路径。

通过描述来生成一份草图：

```bash
# 生成列表信息图表（默认阈值 7.5/10）
python skills/infographics/scripts/generate_infographic.py \
  "5 benefits of regular exercise" \
  -o figures/exercise_benefits.png --type list

# 为营销场景生成（最高阈值：8.5/10）
python skills/infographics/scripts/generate_infographic.py \
  "Product features comparison" \
  -o figures/product_comparison.png --type comparison --doc-type marketing

# 使用企业风格生成
python skills/infographics/scripts/generate_infographic.py \
  "Company milestones 2010-2025" \
  -o figures/timeline.png --type timeline --style corporate

# 使用色盲安全调色板生成
python skills/infographics/scripts/generate_infographic.py \
  "Heart disease statistics worldwide" \
  -o figures/health_stats.png --type statistical --palette wong

# 配合研究生成，以获取准确、最新的数据
python skills/infographics/scripts/generate_infographic.py \
  "Global AI market size and growth projections" \
  -o figures/ai_market.png --type statistical --research
```

**幕后发生了什么：**
1. **（可选）研究**：Perplexity Sonar Pro 收集带来源注释的候选事实
2. **第一次生成**：Nano Banana 2 遵循设计最佳实践创建初始信息图表
3. **第一次审查**：**Gemini 3.7 Flash** 对照文档类型阈值评估质量
4. **决策**：当评分审查达到阈值且不再要求进一步修改时停止
5. **如果要求改进**：保留内容和来源上下文，优化提示词，重新生成
6. **重复**：直到质量达到阈值或达到迭代预算；在 API 失败时停止，并保留最新
   保存的草图

**智能迭代的好处：**
- ✅ 如果第一次生成就足够好，可以节省 API 调用
- ✅ 为营销材料设定更高的质量标准
- ✅ 为草稿/内部使用提供更快的周转
- ✅ 为每种使用场景提供合适的质量

**输出**：带版本号的 PNG，加上一份包含模型、评分、`quality_met` 和
`termination_reason` 的审查日志。一张已保存的图像（`success: true`）仍可能
未经审查或低于阈值。仍然需要人工进行事实核查和视觉检查。

## 何时使用此技能

在以下情况下使用 **infographics** 技能：
- 以可视化格式呈现数据或统计数字
- 为项目里程碑或历史创建时间线可视化
- 解释流程、工作流或分步指南
- 并排比较选项、产品或概念
- 以引人入胜的可视化格式总结要点
- 创建地理或基于地图的数据可视化
- 构建层级或组织架构图
- 设计社交媒体内容或营销材料

**对于以下情况，请改用 scientific-schematics：**
- 技术流程图和电路图
- 生物通路和分子图
- 神经网络架构图
- CONSORT/PRISMA 方法学图

---

## 研究集成

### 自动数据收集（`--research`）

当创建需要准确、最新数据的信息图表时，使用 `--research` 标志，通过
**Perplexity Sonar Pro** 收集候选事实和统计数据。该脚本会保留来源注释；
它不会独立验证陈述或来源的相关性。对于科学或医学出版物，在纳入最终数字
之前请先核实主要来源。

```bash
# 研究并生成统计信息图表
python skills/infographics/scripts/generate_infographic.py \
  "Global renewable energy adoption rates by country" \
  -o figures/renewable_energy.png --type statistical --research

# 为时间线信息图表进行研究
python skills/infographics/scripts/generate_infographic.py \
  "History of artificial intelligence breakthroughs" \
  -o figures/ai_history.png --type timeline --research

# 为比较信息图表进行研究
python skills/infographics/scripts/generate_infographic.py \
  "Electric vehicles vs hydrogen vehicles comparison" \
  -o figures/ev_hydrogen.png --type comparison --research
```

### 研究提供的内容

研究阶段会自动：

1. **收集关键事实**：有关该主题的 5-8 个相关事实和统计数据
2. **提供背景信息**：用于准确呈现的背景信息
3. **请求数据点**：带单位、总体、分母和日期的数字
4. **保留来源**：OpenRouter 的 URL 引用注释，以及可选的提供商引用字段
5. **标注请求日期**：使用当前日期，同时保留历史事件的日期

### 何时使用研究

**对以下场景启用研究（`--research`）：**
- 需要准确数字的统计信息图表
- 市场数据、行业统计数据，或趋势
- 科学或医学信息
- 时事或近期进展
- 任何准确性至关重要的主题

**对以下场景跳过研究：**
- 简单的概念性信息图表
- 内部流程文档
- 你已在提示词中提供了所有数据的主题
- 对速度要求严格的生成场景

### 研究输出

启用研究后，会创建额外的文件：
- `{name}_research.json` - 研究答案和返回的来源记录（当研究成功时）
- 研究内容和来源记录会保留在生成、审查和优化提示词中
- 失败的研究会被记录在审查日志中；生成过程会使用所提供的提示词继续进行

---

## 信息图表类型

通过 `--type` 支持十种类型：`statistical`、`timeline`、`process`、
`comparison`、`list`、`geographic`、`hierarchical`、`anatomical`、
`resume` 和 `social`。每种类型的用途、所需的数据形态，以及示例提示词，
参见
[references/infographic_type_catalog.md](references/infographic_type_catalog.md)
和 [references/infographic_types.md](references/infographic_types.md)。

## 风格预设

### 行业风格（`--style`）

| 风格 | 颜色 | 最适合 |
|-------|--------|----------|
| `corporate`（企业） | 海军蓝、钢蓝、金色 | 商业报告、金融 |
| `healthcare`（医疗） | 医疗蓝、青色、浅青色 | 医疗、健康 |
| `technology`（科技） | 科技蓝、石板灰、紫色 | 软件、数据、AI |
| `nature`（自然） | 森林绿、薄荷绿、泥土棕 | 环境、有机 |
| `education`（教育） | 学术蓝、浅蓝、珊瑚色 | 学习、学术 |
| `marketing`（营销） | 珊瑚色、青绿色、黄色 | 社交媒体、营销活动 |
| `finance`（金融） | 海军蓝、金色、绿色/红色 | 投资、银行业务 |
| `nonprofit`（非营利） | 暖橙色、鼠尾草绿、沙色 | 社会事业、慈善 |

```bash
# 企业风格
python skills/infographics/scripts/generate_infographic.py \
  "Q4 Results" -o q4.png --type statistical --style corporate

# 医疗风格
python skills/infographics/scripts/generate_infographic.py \
  "Patient Journey" -o journey.png --type process --style healthcare
```

---

## 色盲安全调色板

### 可用调色板（`--palette`）

| 调色板 | 颜色 | 说明 |
|---------|--------|-------------|
| `wong` | 七种彩色加黑色 | 由 Wong 推广的 Okabe-Ito 调色板 |
| `ibm` | 深蓝、紫红、洋红、橙色、金色 | 旧版五色预设 |
| `tol` | 九色柔和调色板 | 分类数据；浅灰色保留给缺失数据 |

```bash
# Wong 的色盲安全调色板
python skills/infographics/scripts/generate_infographic.py \
  "Survey results by category" -o survey.png --type statistical --palette wong
```

---

## 智能迭代优化与 CLI

生成-审查-优化循环、每一个命令行选项，以及配置，均在
[references/iterative_refinement.md](references/iterative_refinement.md) 中。

## 提示工程技巧

### 对内容要具体

✓ **好的提示词**（具体、详细）：
```
"5 benefits of meditation: reduces stress, improves focus, 
better sleep, lower blood pressure, emotional balance"
```

✗ **避免模糊的提示词**：
```
"meditation infographic"
```

### 包含数据点

✓ **好**：
```
"Synthetic example: market grows from USD 10B (2020) to USD 45B (2025), CAGR 35.1%; label illustrative"
```

✗ **模糊**：
```
"market is growing"
```

### 指定视觉元素

✓ **好**：
```
"Timeline showing 5 milestones with icons for each event"
```

---

## API 和模型契约

于 2026-10-01 对照 OpenRouter 文档及其公开模型目录进行了审查：

- 生成：`google/gemini-3.1-flash-image`（Nano Banana 2）、
  `POST /api/v1/images`、`prompt`、`n: 1`、可选的 `input_references`；读取
  `data[0].b64_json` 并验证 `media_type`/PNG 签名。Gemini 端点不公布
  `output_format`，因此该脚本检查返回的格式，而不是发送该选项。
- 审查：`google/gemini-3.7-flash`、`POST /api/v1/chat/completions`，文本
  后跟一个 `image_url` 数据 URL；读取 `choices[0].message.content`。
- 研究以及 Python 的 `web_search()` 辅助函数：`perplexity/sonar-pro`，
  使用相同的聊天端点；使用 `web_search_options.search_context_size`，并
  保留 `message.annotations[].url_citation`。这并不意味着存在一个独立的
  搜索 API 或学术模式保证。
- 所有付费调用都使用基于 `OPENROUTER_API_KEY` 的 bearer 身份验证；没有
  自动重试或分页。公开发现使用 `GET /api/v1/models`、
  `GET /api/v1/images/models`，以及每个图像模型的 `/endpoints` 记录。

参见[图像 API 指南](https://openrouter.ai/docs/guides/overview/multimodal/image-generation)、
[图像输入契约](https://openrouter.ai/docs/guides/overview/multimodal/image-understanding)、
[网络搜索选项和引用](https://openrouter.ai/docs/guides/features/plugins/web-search)，
以及[身份验证指南](https://openrouter.ai/docs/api_reference/authentication)。
离线测试涵盖了这些负载和失败路径；目录中存在条目并不能证明某次已通过身份
验证的生成或事实的准确性。当精确的数值几何关系、可复现性，或地图边界至关
重要时，请使用基于代码的绘图或 GIS 工具。

## 参考文件

有关详细指导，请加载这些参考文件：

- **`references/infographic_types.md`**：全部 10+ 种类型的扩展模板
- **`references/design_principles.md`**：视觉层级、布局、排版
- **`references/color_palettes.md`**：完整的调色板规格

---

## 故障排除

### 常见问题

**问题**：信息图表中的文字不可读
- **解决方案**：减少文字内容；使用 --type 指定布局类型

**问题**：颜色冲突或不易辨识
- **解决方案**：使用 `--palette wong` 获取色盲安全的颜色

**问题**：质量评分过低
- **解决方案**：检查评语和保留的草图；改进提示词，然后用
  `--iterations N`（默认为 3）明确选择迭代预算

**问题**：生成了错误的信息图表类型
- **解决方案**：始终指定 `--type` 标志以获得一致的结果

---

## 与其他技能的集成

此技能可与以下技能协同工作：

- **scientific-schematics**：用于技术图表和流程图
- **market-research-reports**：商业报告中的信息图表
- **scientific-slides**：演示文稿中的信息图表元素
- **generate-image**：用于非信息图表的视觉内容

---

## 快速参考清单

生成前：
- [ ] 清晰、具体的内容描述
- [ ] 已选择信息图表类型（`--type`）
- [ ] 风格适合受众（`--style`）
- [ ] 已指定输出路径（`-o`）
- [ ] 已配置 API 密钥

生成后：
- [ ] 审查生成的图像
- [ ] 检查审查日志中的评分
- [ ] 将图像中的每一个数字、单位、标签和来源与已验证的输入进行比较；AI
  质量评分不是事实核查
- [ ] 提供一段简短的替代文字说明，以及一个可读的数据表或长描述，涵盖关键
  数值和关系，遵循
  [W3C 关于复杂图像的指南](https://www.w3.org/WAI/tutorials/images/complex/)
- [ ] 如有需要，用更具体的提示词重新生成

---

利用此技能，借助 Nano Banana 2 AI 的强大能力和智能质量审查，创建专业、
无障碍且视觉上引人入胜的信息图表。

## 引用 Scientific Agent Skills

此技能是 K-Dense 的 Scientific Agent Skills 的一部分。如果它对论文、报告、
演示文稿或代码发布有实质性贡献，请将该论文添加到参考文献或软件部分，并告知
用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 会解析到最新
的 arXiv 版本，因此切勿附加版本后缀（如 `v1`）。如果可以访问网络，请在撰写
引用之前获取 https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中获取作者
列表、年份和版本。如果该记录列出了期刊引用或出版商 DOI，请改为引用已发表的
版本。
