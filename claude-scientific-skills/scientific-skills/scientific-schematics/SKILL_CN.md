---
name: scientific-schematics
description: 使用Nano Banana 2 AI创建 publication 质量的科学图表，具有智能迭代改进功能。使用Gemini 3.1 Pro Preview进行质量审查。仅当质量低于您的文档类型阈值时才会重新生成。专门用于神经网络架构、系统图表、流程图、生物通路和复杂科学可视化。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 科学示意图和图表

## 概述

科学示意图和图表将复杂概念转化为清晰的视觉表示，用于发表。**此技能使用Nano Banana 2 AI进行图表生成，并使用Gemini 3.1 Pro Preview进行质量审查。**

**工作原理：**
- 用自然语言描述您的图表
- Nano Banana 2自动生成 publication 质量的图像
- **Gemini 3.1 Pro Preview根据文档类型阈值评估质量**
- **智能迭代**：仅当质量低于阈值时才会重新生成
- 几分钟内即可获得 publication 就绪的输出
- 无需编码、模板或手动绘制

**按文档类型的质量阈值：**
| 文档类型 | 阈值 | 描述 |
|---------|------|------|
| journal | 8.5/10 | Nature、Science、同行评审期刊 |
| conference | 8.0/10 | 会议论文 |
| thesis | 8.0/10 | 学位论文、论文 |
| grant | 8.0/10 | 资助提案 |
| preprint | 7.5/10 | arXiv、bioRxiv等 |
| report | 7.5/10 | 技术报告 |
| poster | 7.0/10 | 学术海报 |
| presentation | 6.5/10 | 幻灯片、演讲 |
| default | 7.5/10 | 通用目的 |

**只需描述您想要的内容，Nano Banana 2就会创建它。** 所有图表都存储在figures/子文件夹中，并在论文/海报中引用。

## 快速开始：生成任何图表

只需描述即可创建任何科学图表。Nano Banana 2通过**智能迭代**自动处理所有内容：

```bash
# 为期刊论文生成（最高质量阈值：8.5/10）
python scripts/generate_schematic.py "CONSORT参与者流程图，500人筛选，150人排除，350人随机化" -o figures/consort.png --doc-type journal

# 为演示生成（较低阈值：6.5/10 - 更快）
python scripts/generate_schematic.py "显示多头注意力的Transformer编码器-解码器架构" -o figures/transformer.png --doc-type presentation

# 为海报生成（中等阈值：7.0/10）
python scripts/generate_schematic.py "从EGFR到基因转录的MAPK信号通路" -o figures/mapk_pathway.png --doc-type poster

# 自定义最大迭代次数（最多2次）
python scripts/generate_schematic.py "带有运算放大器、电阻器和电容器的复杂电路图表" -o figures/circuit.png --iterations 2 --doc-type journal
```

**背后发生的事情：**
1. **生成1**：Nano Banana 2创建遵循科学图表最佳实践的初始图像
2. **审查1**：**Gemini 3.1 Pro Preview**根据文档类型阈值评估质量
3. **决策**：如果质量 >= 阈值 → **完成**（不需要更多迭代！）
4. **如果低于阈值**：基于批评改进提示，重新生成
5. **重复**：直到质量达到阈值或达到最大迭代次数

**智能迭代优势：**
- ✅ 如果第一次生成足够好，节省API调用
- ✅ 期刊论文的更高质量标准
- ✅ 演示/海报的更快周转
- ✅ 每个用例的适当质量

**输出**：版本化图像加上详细的审查日志，包含质量分数、批评和提前停止信息。

### 配置

设置您的OpenRouter API密钥：
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

在以下位置获取API密钥：https://openrouter.ai/keys

### AI生成最佳实践

**科学图表的有效提示：**

✓ **好的提示**（具体、详细）：
- "CONSORT流程图，显示参与者从筛选（n=500）到随机化再到最终分析的流程"
- "Transformer神经网络架构，左侧编码器堆栈，右侧解码器堆栈，显示多头注意力和交叉注意力连接"
- "生物信号级联：EGFR受体 → RAS → RAF → MEK → ERK → 细胞核，标记磷酸化步骤"
- "物联网系统框图：传感器 → 微控制器 → WiFi模块 → 云服务器 → 移动应用"

✗ **避免模糊提示**：
- "制作流程图"（过于通用）
- "神经网络"（哪种类型？什么组件？）
- "通路图"（哪个通路？什么分子？）

**要包含的关键元素：**
- **类型**：流程图、架构图、通路、电路等
- **组件**：要包含的特定元素
- **流程/方向**：元素如何连接（从左到右，从上到下）
- **标签**：要包含的关键注释或文本
- **风格**：任何特定的视觉要求

**科学质量指南**（自动应用）：
- 干净的白色/浅色背景
- 高对比度以提高可读性
- 清晰、可读的标签（最小10pt）
- 专业排版（无衬线字体）
- 色盲友好的颜色（Okabe-Ito调色板）
- 适当的间距以防止拥挤
- 适当的比例尺、图例、坐标轴

## 何时使用此技能

当您需要以下操作时，应使用此技能：
- 创建神经网络架构图（Transformer、CNN、RNN等）
- 说明系统架构和数据流图
- 绘制研究设计的方法流程图（CONSORT、PRISMA）
- 可视化算法工作流程和处理管道
- 创建电路图表和电气示意图
- 描绘生物通路和分子相互作用
- 生成网络拓扑和层次结构
- 说明概念框架和理论模型
- 为技术论文设计框图

## 如何使用此技能

**只需用自然语言描述您的图表。** Nano Banana 2会自动生成：

```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

**就是这样！** AI处理：
- ✓ 布局和构图
- ✓ 标签和注释
- ✓ 颜色和样式
- ✓ 质量审查和完善
- ✓ publication 就绪的输出

**适用于所有图表类型：**
- 流程图（CONSORT、PRISMA等）
- 神经网络架构
- 生物通路
- 电路图表
- 系统架构
- 框图
- 任何科学可视化

**无需编码，无需模板，无需手动绘制。**

---

# AI生成模式（Nano Banana 2 + Gemini 3.1 Pro Preview审查）

## 智能迭代改进工作流程

AI生成系统使用**智能迭代** - 仅当质量低于您的文档类型阈值时才会重新生成：

### 智能迭代如何工作

```
┌─────────────────────────────────────────────────────┐
│  1. 使用Nano Banana 2生成图像                      │
│                    ↓                                │
│  2. 使用Gemini 3.1 Pro Preview审查质量              │
│                    ↓                                │
│  3. 分数 >= 阈值？                                  │
│       是 → 完成！（提前停止）                      │
│       否 → 改进提示，转到步骤1                      │
│                    ↓                                │
│  4. 重复直到达到质量或最大迭代次数                  │
└─────────────────────────────────────────────────────┘
```

### 迭代1：初始生成
**提示构建：**
```
科学图表指南 + 用户请求
```

**输出：** `diagram_v1.png`

### Gemini 3.1 Pro Preview质量审查

Gemini 3.1 Pro Preview从以下方面评估图表：
1. **科学准确性**（0-2分）- 正确的概念、符号、关系
2. **清晰度和可读性**（0-2分）- 易于理解，清晰的层次结构
3. **标签质量**（0-2分）- 完整、可读、一致的标签
4. **布局和构图**（0-2分）- 逻辑流程，平衡，无重叠
5. **专业外观**（0-2分）- Publication就绪质量

**审查输出示例：**
```
分数：8.0

优势：
- 从上到下的清晰流程
- 所有阶段都正确标记
- 专业排版

问题：
- 参与者计数略小
- 排除框上的轻微重叠

结论：可接受（对于海报，阈值7.0）
```

### 决策点：继续或停止？

| 如果分数... | 操作 |
|------------|------|
| >= 阈值 | **停止** - 质量对此文档类型足够好 |
| < 阈值 | 继续下一次迭代，改进提示 |

**示例：**
- 对于**海报**（阈值7.0）：分数7.5 → **1次迭代后完成！**
- 对于**期刊**（阈值8.5）：分数7.5 → 继续改进

### 后续迭代（仅在需要时）

如果质量低于阈值，系统：
1. 从Gemini 3.1 Pro Preview的审查中提取具体问题
2. 用改进说明增强提示
3. 使用Nano Banana 2重新生成
4. 再次使用Gemini 3.1 Pro Preview审查
5. 重复直到达到阈值或达到最大迭代次数

### 审查日志
所有迭代都保存有JSON审查日志，包括提前停止信息：
```json
{
  "user_prompt": "CONSORT参与者流程图...",
  "doc_type": "poster",
  "quality_threshold": 7.0,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "score": 7.5,
      "needs_improvement": false,
      "critique": "分数：7.5\n优势：..."
    }
  ],
  "final_score": 7.5,
  "early_stop": true,
  "early_stop_reason": "质量分数7.5满足海报阈值7.0"
}
```

**注意：** 使用智能迭代，如果早期达到质量，您可能只看到1次迭代而不是完整的2次！

## 高级AI生成用法

### Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# 初始化生成器
generator = ScientificSchematicGenerator(
    api_key="your_openrouter_key",
    verbose=True
)

# 生成带有迭代改进（最多2次迭代）
results = generator.generate_iterative(
    user_prompt="Transformer架构图",
    output_path="figures/transformer.png",
    iterations=2
)

# 访问结果
print(f"最终分数：{results['final_score']}/10")
print(f"最终图像：{results['final_image']}")

# 审查各个迭代
for iteration in results['iterations']:
    print(f"迭代 {iteration['iteration']}：{iteration['score']}/10")
    print(f"批评：{iteration['critique']}")
```

### 命令行选项

```bash
# 基本用法（默认阈值7.5/10）
python scripts/generate_schematic.py "图表描述" -o output.png

# 指定文档类型以获得适当的质量阈值
python scripts/generate_schematic.py "图表" -o out.png --doc-type journal      # 8.5/10
python scripts/generate_schematic.py "图表" -o out.png --doc-type conference   # 8.0/10
python scripts/generate_schematic.py "图表" -o out.png --doc-type poster       # 7.0/10
python scripts/generate_schematic.py "图表" -o out.png --doc-type presentation # 6.5/10

# 自定义最大迭代次数（1-2）
python scripts/generate_schematic.py "复杂图表" -o diagram.png --iterations 2

# 详细输出（查看所有API调用和审查）
python scripts/generate_schematic.py "流程图" -o flow.png -v

# 通过标志提供API密钥
python scripts/generate_schematic.py "图表" -o out.png --api-key "sk-or-v1-..."

# 组合选项
python scripts/generate_schematic.py "神经网络" -o nn.png --doc-type journal --iterations 2 -v
```

### 提示工程技巧

**1. 具体说明布局：**
```
✓ "垂直流的流程图，从上到下"
✓ "左侧编码器，右侧解码器的架构图"
✓ "顺时针流的圆形通路图"
```

**2. 包含定量细节：**
```
✓ "输入层（784个节点）、隐藏层（128个节点）、输出（10个节点）的神经网络"
✓ "显示n=500筛选，n=150排除，n=350随机化的流程图"
✓ "带有1kΩ电阻、10µF电容器、5V电源的电路"
```

**3. 指定视觉风格：**
```
✓ "带有干净线条的简约框图"
✓ "带有蛋白质结构的详细生物通路"
✓ "带有工程符号的技术示意图"
```

**4. 请求特定标签：**
```
✓ "用激活/抑制标记所有箭头"
✓ "在每个框中包含层维度"
✓ "用时间戳显示时间进展"
```

**5. 提及颜色要求：**
```
✓ "使用色盲友好的颜色"
✓ "灰度兼容设计"
✓ "按功能编码颜色：输入为蓝色，处理为绿色，输出为红色"
```

## AI生成示例

### 示例1：CONSORT流程图
```bash
python scripts/generate_schematic.py \
  "随机对照试验的CONSORT参与者流程图。\
   顶部开始为'评估资格（n=500）'。\
   显示'排除（n=150）'，原因：年龄<18（n=80），拒绝（n=50），其他（n=20）。\
   然后'随机化（n=350）'分为两个组：\
   '治疗组（n=175）'和'对照组（n=175）'。\
   每组显示'失访'（n=15和n=10）。\
   以'分析'结束（n=160和n=165）。\
   处理步骤使用蓝色框，排除使用橙色，最终分析使用绿色。" \
  -o figures/consort.png
```

### 示例2：神经网络架构
```bash
python scripts/generate_schematic.py \
  "Transformer编码器-解码器架构图。\
   左侧：编码器堆栈，包含输入嵌入、位置编码、\
   多头自注意力、添加与归一化、前馈、添加与归一化。\
   右侧：解码器堆栈，包含输出嵌入、位置编码、\
   掩码自注意力、添加与归一化、交叉注意力（接收来自编码器）、\
   添加与归一化、前馈、添加与归一化、线性与softmax。\
   用虚线显示从编码器到解码器的交叉注意力连接。\
   编码器使用浅蓝色，解码器使用浅红色。\
   清晰标记所有组件。" \
  -o figures/transformer.png --iterations 2
```

### 示例3：生物通路
```bash
python scripts/generate_schematic.py \
  "MAPK信号通路图。\
   顶部细胞膜处开始于EGFR受体。\
   向下箭头到RAS（带有GTP标签）。\
   箭头到RAF激酶。\
   箭头到MEK激酶。\
   箭头到ERK激酶。\
   最终箭头到显示基因转录的细胞核。\
   用'磷酸化'或'激活'标记每个箭头。\
   蛋白质使用圆角矩形，每个使用不同颜色。\
   顶部包含膜边界线。" \
  -o figures/mapk_pathway.png
```

### 示例4：系统架构
```bash
python scripts/generate_schematic.py \
  "物联网系统架构框图。\
   底层：传感器（温度、湿度、运动）在绿色框中。\
   中层：微控制器（ESP32）在蓝色框中。\
   连接到WiFi模块（橙色框）和显示器（紫色框）。\
   顶层：云服务器（灰色框）连接到移动应用（浅蓝色框）。\
   显示所有组件之间的数据流箭头。\
   用协议标记连接：I2C、UART、WiFi、HTTPS。" \
  -o figures/iot_architecture.png
```

---

## 命令行使用

生成科学示意图的主要入口点：

```bash
# 基本用法
python scripts/generate_schematic.py "图表描述" -o output.png

# 自定义迭代次数（最多2次）
python scripts/generate_schematic.py "复杂图表" -o diagram.png --iterations 2

# 详细模式
python scripts/generate_schematic.py "图表" -o out.png -v
```

**注意：** Nano Banana 2 AI生成系统在其迭代改进过程中包含自动质量审查。每次迭代都会评估科学准确性、清晰度和可访问性。

## 最佳实践摘要

### 设计原则

1. **清晰胜于复杂** - 简化，移除不必要的元素
2. **一致的样式** - 使用模板和样式文件
3. **色盲可访问性** - 使用Okabe-Ito调色板，冗余编码
4. **适当的排版** - 无衬线字体，最小7-8 pt
5. **矢量格式** - 始终使用PDF/SVG用于发表

### 技术要求

1. **分辨率** - 首选矢量，或300+ DPI的光栅
2. **文件格式** - LaTeX使用PDF，网络使用SVG，PNG作为备选
3. **色彩空间** - 数字使用RGB，印刷使用CMYK（必要时转换）
4. **线宽** - 最小0.5 pt，典型1-2 pt
5. **文本大小** - 最终大小至少7-8 pt

### 集成指南

1. **包含在LaTeX中** - 使用`\includegraphics{}`插入生成的图像
2. **详细说明** - 描述所有元素和缩写
3. **在文本中引用** - 在叙述流程中解释图表
4. **保持一致性** - 论文中所有图表使用相同样式
5. **版本控制** - 在存储库中保留提示和生成的图像

## 常见问题故障排除

### AI生成问题

**问题**：文本或元素重叠
- **解决方案**：AI生成自动处理间距
- **解决方案**：增加迭代次数：`--iterations 2`以获得更好的改进

**问题**：元素连接不正确
- **解决方案**：使您的提示更具体地说明连接和布局
- **解决方案**：增加迭代次数以获得更好的改进

### 图像质量问题

**问题**：导出质量差
- **解决方案**：AI生成自动生成高质量图像
- **解决方案**：增加迭代次数以获得更好的结果：`--iterations 2`

**问题**：生成后元素重叠
- **解决方案**：AI生成自动处理间距
- **解决方案**：增加迭代次数：`--iterations 2`以获得更好的改进
- **解决方案**：使您的提示更具体地说明布局和间距要求

### 质量检查问题

**问题**：假阳性重叠检测
- **解决方案**：调整阈值：`detect_overlaps(image_path, threshold=0.98)`
- **解决方案**：手动审查视觉报告中的标记区域

**问题**：生成的图像质量低
- **解决方案**：AI生成默认生成高质量图像
- **解决方案**：增加迭代次数以获得更好的结果：`--iterations 2`

**问题**：色盲模拟显示对比度差
- **解决方案**：在代码中明确切换到Okabe-Ito调色板
- **解决方案**：添加冗余编码（形状、图案、线条样式）
- **解决方案**：增加颜色饱和度和亮度差异

**问题**：检测到高严重性重叠
- **解决方案**：查看overlap_report.json获取精确位置
- **解决方案**：增加这些特定区域的间距
- **解决方案**：使用调整后的参数重新运行并再次验证

**问题**：视觉报告生成失败
- **解决方案**：检查Pillow和matplotlib安装
- **解决方案**：确保图像文件可读：`Image.open(path).verify()`
- **解决方案**：检查报告生成的足够磁盘空间

### 可访问性问题

**问题**：灰度中颜色无法区分
- **解决方案**：运行可访问性检查器：`verify_accessibility(image_path)`
- **解决方案**：添加图案、形状或线条样式以增加冗余
- **解决方案**：增加相邻元素之间的对比度

**问题**：打印时文本太小
- **解决方案**：运行分辨率验证器：`validate_resolution(image_path)`
- **解决方案**：以最终大小设计，使用最小7-8 pt字体
- **解决方案**：在分辨率报告中检查物理尺寸

**问题**：可访问性检查一致失败
- **解决方案**：查看accessibility_report.json获取具体失败原因
- **解决方案**：将颜色对比度至少增加20%
- **解决方案**：在最终确定前使用实际灰度转换进行测试

## 资源和参考

### 详细参考

加载这些文件以获取特定主题的综合信息：

- **`references/best_practices.md`** - 发表标准和可访问性指南

### 外部资源

**Python库**
- Schemdraw文档：https://schemdraw.readthedocs.io/
- NetworkX文档：https://networkx.org/documentation/
- Matplotlib文档：https://matplotlib.org/

**发表标准**
- Nature图表指南：https://www.nature.com/nature/for-authors/final-submission
- Science图表指南：https://www.science.org/content/page/instructions-preparing-initial-manuscript
- CONSORT图表：http://www.consort-statement.org/consort-statement/flow-diagram

## 与其他技能集成

此技能与以下技能协同工作：

- **科学写作** - 图表遵循图表最佳实践
- **科学可视化** - 共享调色板和样式
- **LaTeX海报** - 为海报演示生成图表
- **研究资助** - 提案的方法学图表
- **同行评审** - 评估图表清晰度和可访问性

## 快速参考清单

提交图表前，验证：

### 视觉质量
- [ ] 高质量图像格式（AI生成的PNG）
- [ ] 无重叠元素（AI自动处理）
- [ ] 所有组件之间有足够的间距（AI优化）
- [ ] 干净、专业的对齐
- [ ] 所有箭头正确连接到预期目标

### 可访问性
- [ ] 使用色盲安全调色板（Okabe-Ito）
- [ ] 在灰度下工作（使用可访问性检查器测试）
- [ ] 元素之间有足够的对比度（已验证）
- [ ] 适当的冗余编码（形状 + 颜色）
- [ ] 色盲模拟通过所有检查

### 排版和可读性
- [ ] 最终大小的文本最小7-8 pt
- [ ] 所有元素都清晰完整地标记
- [ ] 一致的字体系列和大小
- [ ] 无文本重叠或截断
- [ ] 适用时包含单位

### 发表标准
- [ ] 与手稿中其他图表一致的样式
- [ ] 全面的说明，定义所有缩写
- [ ] 在手稿文本中适当引用
- [ ] 满足期刊特定的尺寸要求
- [ ] 以期刊要求的格式导出（PDF/EPS/TIFF）

### 质量验证（必需）
- [ ] 运行`run_quality_checks()`并获得PASS状态
- [ ] 审查重叠检测报告（零高严重性重叠）
- [ ] 通过可访问性验证（灰度和色盲）
- [ ] 以目标DPI验证分辨率（打印300+）
- [ ] 生成并审查视觉质量报告
- [ ] 所有质量报告与图表文件一起保存

### 文档和版本控制
- [ ] 保存源文件（.tex, .py）以便将来修订
- [ ] 质量报告存档在`quality_reports/`目录中
- [ ] 记录配置参数（颜色、间距、大小）
- [ ] Git提交包括源、输出和质量报告
- [ ] README或注释解释如何重新生成图表

### 最终集成检查
- [ ] 图表在编译的手稿中正确显示
- [ ] 交叉引用工作（`\ref{}`指向正确的图表）
- [ ] 图表编号与文本引用匹配
- [ ] 说明出现在相对于图表的正确页面上
- [ ] 无与图表相关的编译警告或错误

## 环境设置

```bash
# 必需
export OPENROUTER_API_KEY='your_api_key_here'

# 在以下位置获取密钥：https://openrouter.ai/keys
```

## 入门

**最简单的使用方式：**
```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

---

使用此技能创建清晰、可访问、 publication 质量的图表，有效传达复杂的科学概念。带有迭代改进的AI驱动工作流程确保图表满足专业标准。