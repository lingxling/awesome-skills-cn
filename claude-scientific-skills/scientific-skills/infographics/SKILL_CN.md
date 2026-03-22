---
name: infographics
description: "使用Nano Banana Pro AI创建专业信息图表，具有智能迭代优化功能。使用Gemini 3 Pro进行质量审查。集成research-lookup和网络搜索以获取准确数据。支持10种信息图表类型、8种行业风格和色盲安全调色板。"
allowed-tools: Read Write Edit Bash
---

# 信息图表

## 概述

信息图表是信息、数据或知识的可视化表示，旨在快速清晰地呈现复杂内容。**此技能使用Nano Banana Pro AI进行信息图表生成，具有Gemini 3 Pro质量审查和Perplexity Sonar研究功能。**

**工作原理：**
- （可选）**研究阶段**：使用Perplexity Sonar收集准确的事实和统计数据
- 用自然语言描述您的信息图表
- Nano Banana Pro自动生成出版质量的信息图表
- **Gemini 3 Pro根据文档类型阈值审查质量**
- **智能迭代**：仅当质量低于阈值时才重新生成
- 专业就绪的输出，仅需几分钟
- 无需设计技能

**按文档类型的质量阈值：**
| 文档类型 | 阈值 | 描述 |
|---------------|-----------|-------------|
| marketing | 8.5/10 | 营销材料 - 必须引人注目 |
| report | 8.0/10 | 商业报告 - 专业质量 |
| presentation | 7.5/10 | 幻灯片、演讲 - 清晰且吸引人 |
| social | 7.0/10 | 社交媒体内容 |
| internal | 7.0/10 | 内部使用 |
| draft | 6.5/10 | 工作草稿 |
| default | 7.5/10 | 通用目的 |

**只需描述您想要的内容，Nano Banana Pro就会创建它。**

## 快速开始

只需描述即可生成任何信息图表：

```bash
# 生成列表信息图表（默认阈值7.5/10）
python skills/infographics/scripts/generate_infographic.py \
  "5 benefits of regular exercise" \
  -o figures/exercise_benefits.png --type list

# 为营销生成（最高阈值：8.5/10）
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

# 带有研究生成以获取准确、最新的数据
python skills/infographics/scripts/generate_infographic.py \
  "Global AI market size and growth projections" \
  -o figures/ai_market.png --type statistical --research
```

**幕后发生的事情：**
1. **（可选）研究**：Perplexity Sonar收集准确的事实、统计数据和数据
2. **生成1**：Nano Banana Pro按照设计最佳实践创建初始信息图表
3. **审查1**：**Gemini 3 Pro**根据文档类型阈值评估质量
4. **决策**：如果质量 ≥ 阈值 → **完成**（无需更多迭代！）
5. **如果低于阈值**：根据批评改进提示，重新生成
6. **重复**：直到质量满足阈值或达到最大迭代次数

**智能迭代的好处：**
- ✅ 如果第一次生成足够好，则节省API调用
- ✅ 营销材料有更高的质量标准
- ✅ 草稿/内部使用的更快周转
- ✅ 适合每种用例的适当质量

**输出**：版本化图像以及详细的审查日志，包含质量评分、批评和提前停止信息。

## 何时使用此技能

在以下情况下使用**信息图表**技能：
- 以可视化格式呈现数据或统计数据
- 为项目里程碑或历史创建时间线可视化
- 解释流程、工作流程或分步指南
- 并排比较选项、产品或概念
- 以吸引人的可视化格式总结关键点
- 创建基于地理或地图的数据可视化
- 构建分层或组织结构图
- 设计社交媒体内容或营销材料

**请改用scientific-schematics进行：**
- 技术流程图和电路图
- 生物学通路和分子图
- 神经网络架构图
- CONSORT/PRISMA方法论图

---

## 研究集成

### 自动数据收集（`--research`）

当创建需要准确、最新数据的信息图表时，使用`--research`标志自动使用**Perplexity Sonar Pro**收集事实和统计数据。

```bash
# 研究并生成统计信息图表
python skills/infographics/scripts/generate_infographic.py \
  "Global renewable energy adoption rates by country" \
  -o figures/renewable_energy.png --type statistical --research

# 为时间线信息图表研究
python skills/infographics/scripts/generate_infographic.py \
  "History of artificial intelligence breakthroughs" \
  -o figures/ai_history.png --type timeline --research

# 为比较信息图表研究
python skills/infographics/scripts/generate_infographic.py \
  "Electric vehicles vs hydrogen vehicles comparison" \
  -o figures/ev_hydrogen.png --type comparison --research
```

### 研究提供的内容

研究阶段自动：

1. **收集关键事实**：关于主题的5-8个相关事实和统计数据
2. **提供背景**：准确表示的背景信息
3. **查找数据点**：具体数字、百分比和日期
4. **引用来源**：提及主要研究或来源
5. **优先考虑最新性**：专注于2023-2026年的信息

### 何时使用研究

**启用研究（`--research`）用于：**
- 需要准确数字的统计信息图表
- 市场数据、行业统计或趋势
- 科学或医学信息
- 当前事件或最新发展
- 准确性至关重要的任何主题

**跳过研究用于：**
- 简单的概念信息图表
- 内部流程文档
- 您在提示中提供所有数据的主题
- 速度关键的生成

### 研究输出

启用研究时，会创建其他文件：
- `{name}_research.json` - 原始研究数据和来源
- 研究内容自动合并到信息图表提示中

---

## 信息图表类型

### 1. 统计/数据驱动（`--type statistical`）

最适合：呈现数字、百分比、调查结果和定量数据。

**关键元素：** 图表（条形图、饼图、折线图、环形图）、大数字标注、数据比较、趋势指示器。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Global internet usage 2025: 5.5 billion users (68% of population), \
   Asia Pacific 53%, Europe 15%, Americas 20%, Africa 12%" \
  -o figures/internet_stats.png --type statistical --style technology
```

---

### 2. 时间线（`--type timeline`）

最适合：历史事件、项目里程碑、公司历史、概念演变。

**关键元素：** 时间流程、日期标记、事件节点、连接线。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "History of AI: 1950 Turing Test, 1956 Dartmouth Conference, \
   1997 Deep Blue, 2016 AlphaGo, 2022 ChatGPT" \
  -o figures/ai_history.png --type timeline --style technology
```

---

### 3. 流程/操作指南（`--type process`）

最适合：分步说明、工作流程、程序、教程。

**关键元素：** 编号步骤、方向箭头、操作图标、清晰流程。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "How to start a podcast: 1. Choose your niche, 2. Plan content, \
   3. Set up equipment, 4. Record episodes, 5. Publish and promote" \
  -o figures/podcast_process.png --type process --style marketing
```

---

### 4. 比较（`--type comparison`）

最适合：产品比较、优缺点、前后对比、选项评估。

**关键元素：** 并排布局、匹配类别、勾选/叉号指示器。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Electric vs Gas Cars: Fuel cost (lower vs higher), \
   Maintenance (less vs more), Range (improving vs established)" \
  -o figures/ev_comparison.png --type comparison --style nature
```

---

### 5. 列表/信息（`--type list`）

最适合：提示、事实、关键点、摘要、快速参考指南。

**关键元素：** 编号或项目符号、图标、清晰层次结构。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "7 Habits of Highly Effective People: Be Proactive, \
   Begin with End in Mind, Put First Things First, Think Win-Win, \
   Seek First to Understand, Synergize, Sharpen the Saw" \
  -o figures/habits.png --type list --style corporate
```

---

### 6. 地理（`--type geographic`）

最适合：区域数据、人口统计、基于位置的统计、全球趋势。

**关键元素：** 地图可视化、颜色编码、数据叠加、图例。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Renewable energy adoption by region: Iceland 100%, Norway 98%, \
   Germany 50%, USA 22%, India 20%" \
  -o figures/renewable_map.png --type geographic --style nature
```

---

### 7. 分层/金字塔（`--type hierarchical`）

最适合：组织结构、优先级级别、重要性排名。

**关键元素：** 金字塔或树结构、不同级别、大小递进。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Maslow's Hierarchy: Physiological, Safety, Love/Belonging, \
   Esteem, Self-Actualization" \
  -o figures/maslow.png --type hierarchical --style education
```

---

### 8. 解剖/视觉隐喻（`--type anatomical`）

最适合：使用熟悉的视觉隐喻解释复杂系统。

**关键元素：** 中心隐喻图像、标记部分、连接线。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Business as a human body: Brain=Leadership, Heart=Culture, \
   Arms=Sales, Legs=Operations, Skeleton=Systems" \
  -o figures/business_body.png --type anatomical --style corporate
```

---

### 9. 简历/专业（`--type resume`）

最适合：个人品牌、CV、作品集亮点、专业成就。

**关键元素：** 照片区域、技能可视化、时间线、联系信息。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "UX Designer resume: Skills - User Research 95%, Wireframing 90%, \
   Prototyping 85%. Experience - 2020-2022 Junior, 2022-2025 Senior" \
  -o figures/resume.png --type resume --style technology
```

---

### 10. 社交媒体（`--type social`）

最适合：Instagram、LinkedIn、Twitter/X帖子、可分享的图形。

**关键元素：** 大胆标题、最少文本、最大影响、鲜艳颜色。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Save Water, Save Life: 2.2 billion people lack safe drinking water. \
   Tips: shorter showers, fix leaks, full loads only" \
  -o figures/water_social.png --type social --style marketing
```

---

## 风格预设

### 行业风格（`--style`）

| 风格 | 颜色 | 最适合 |
|-------|--------|----------|
| `corporate` | 海军蓝、钢蓝、金色 | 商业报告、金融 |
| `healthcare` | 医疗蓝、青色、浅青色 | 医疗、健康 |
| `technology` | 科技蓝、板岩蓝、紫色 | 软件、数据、AI |
| `nature` | 森林绿、薄荷绿、土褐色 | 环境、有机 |
| `education` | 学术蓝、浅蓝、珊瑚色 | 学习、学术 |
| `marketing` | 珊瑚色、青色、黄色 | 社交媒体、活动 |
| `finance` | 海军蓝、金色、绿/红色 | 投资、银行 |
| `nonprofit` | 暖橙色、鼠尾草绿、沙色 | 社会事业、慈善机构 |

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

| 调色板 | 颜色 | 描述 |
|---------|--------|-------------|
| `wong` | 橙色、天蓝色、绿色、蓝色、朱红色 | 最广泛推荐 |
| `ibm` | 群青色、靛蓝色、品红色、橙色、金色 | IBM的可访问调色板 |
| `tol` | 12色扩展调色板 | 用于许多类别 |

```bash
# Wong的色盲安全调色板
python skills/infographics/scripts/generate_infographic.py \
  "Survey results by category" -o survey.png --type statistical --palette wong
```

---

## 智能迭代优化

### 工作原理

```
┌─────────────────────────────────────────────────────┐
│  1. 使用Nano Banana Pro生成信息图表       │
│                    ↓                                │
│  2. 使用Gemini 3 Pro审查质量                │
│                    ↓                                │
│  3. 评分 ≥ 阈值？                             │
│       是 → 完成！（提前停止）                      │
│       否  → 改进提示，转到步骤1            │
│                    ↓                                │
│  4. 重复直到质量满足或达到最大迭代      │
└─────────────────────────────────────────────────────┘
```

### 质量审查标准

Gemini 3 Pro根据以下标准评估每个信息图表：

1. **视觉层次和布局**（0-2分）
   - 清晰的视觉层次
   - 逻辑阅读流程
   - 平衡的构图

2. **排版和可读性**（0-2分）
   - 可读的文本
   - 粗体标题
   - 无重叠

3. **数据可视化**（0-2分）
   - 突出的数字
   - 清晰的图表/图标
   - 适当的标签

4. **颜色和可访问性**（0-2分）
   - 专业的颜色
   - 充足的对比度
   - 色盲友好

5. **整体影响**（0-2分）
   - 专业外观
   - 无视觉错误
   - 实现沟通目标

### 审查日志

每次生成都会生成JSON审查日志：
```json
{
  "user_prompt": "5 benefits of exercise...",
  "infographic_type": "list",
  "style": "healthcare",
  "doc_type": "marketing",
  "quality_threshold": 8.5,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/exercise_v1.png",
      "score": 8.7,
      "needs_improvement": false,
      "critique": "SCORE: 8.7\nSTRENGTHS:..."
    }
  ],
  "final_score": 8.7,
  "early_stop": true,
  "early_stop_reason": "质量评分8.7满足阈值8.5"
}
```

---

## 命令行参考

```bash
python skills/infographics/scripts/generate_infographic.py [OPTIONS] PROMPT

参数：
  PROMPT                    信息图表内容的描述

选项：
  -o, --output PATH         输出文件路径（必需）
  -t, --type TYPE           信息图表类型预设
  -s, --style STYLE         行业风格预设
  -p, --palette PALETTE     色盲安全调色板
  -b, --background COLOR    背景颜色（默认：白色）
  --doc-type TYPE           质量阈值的文档类型
  --iterations N            最大优化迭代次数（默认：3）
  --api-key KEY             OpenRouter API密钥
  -v, --verbose             详细输出
  --list-options            列出所有可用选项
```

### 列出所有选项

```bash
python skills/infographics/scripts/generate_infographic.py --list-options
```

---

## 配置

### API密钥设置

设置您的OpenRouter API密钥：
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

在https://openrouter.ai/keys获取API密钥

---

## 提示工程技巧

### 对内容要具体

✓ **好的提示**（具体、详细）：
```
"5 benefits of meditation: reduces stress, improves focus,
better sleep, lower blood pressure, emotional balance"
```

✗ **避免模糊提示**：
```
"meditation infographic"
```

### 包含数据点

✓ **好的**：
```
"Market growth from $10B (2020) to $45B (2025), CAGR 35%"
```

✗ **模糊**：
```
"market is growing"
```

### 指定视觉元素

✓ **好的**：
```
"Timeline showing 5 milestones with icons for each event"
```

---

## 参考文件

有关详细指导，请加载这些参考文件：

- **`references/infographic_types.md`**：所有10+种类型的扩展模板
- **`references/design_principles.md`**：视觉层次、布局、排版
- **`references/color_palettes.md`**：完整调色板规范

---

## 故障排除

### 常见问题

**问题**：信息图表中的文本不可读
- **解决方案**：减少文本内容；使用--type指定布局类型

**问题**：颜色冲突或不可访问
- **解决方案**：使用`--palette wong`获取色盲安全颜色

**问题**：质量评分太低
- **解决方案**：使用`--iterations 3`增加迭代次数；使用更具体的提示

**问题**：生成了错误的信息图表类型
- **解决方案**：始终指定`--type`标志以获得一致的结果

---

## 与其他技能的集成

此技能与以下技能协同工作：

- **scientific-schematics**：用于技术图表和流程图
- **market-research-reports**：商业报告的信息图表
- **scientific-slides**：演示文稿的信息图表元素
- **generate-image**：用于非信息图表视觉内容

---

## 快速参考清单

生成之前：
- [ ] 清晰、具体的内容描述
- [ ] 已选择信息图表类型（`--type`）
- [ ] 风格适合受众（`--style`）
- [ ] 已指定输出路径（`-o`）
- [ ] 已配置API密钥

生成之后：
- [ ] 审查生成的图像
- [ ] 检查审查日志的评分
- [ ] 如有需要，使用更具体的提示重新生成

---

使用此技能利用Nano Banana Pro AI的强大功能和智能质量审查，创建专业、可访问且视觉上引人注目的信息图表。
