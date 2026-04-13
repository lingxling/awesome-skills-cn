---
name: hypogenic
description: 基于表格数据集的自动化LLM驱动假设生成和测试。用于系统性地探索关于经验数据模式的假设（例如，欺骗检测、内容分析）。结合文献见解与数据驱动的假设测试。对于手动假设制定使用hypothesis-generation；对于创意构思使用scientific-brainstorming。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Hypogenic

## 概述

Hypogenic使用大型语言模型提供自动化假设生成和测试，以加速科学发现。该框架支持三种方法：HypoGeniC（数据驱动的假设生成）、HypoRefine（文献和数据协同整合）以及联合方法（文献和数据驱动假设的机制性组合）。

## 快速开始

在几分钟内开始使用Hypogenic：

```bash
# 安装软件包
uv pip install hypogenic

# 克隆示例数据集
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# 运行基本假设生成
hypogenic_generation --config ./data/your_task/config.yaml --method hypogenic --num_hypotheses 20

# 对生成的假设运行推理
hypogenic_inference --config ./data/your_task/config.yaml --hypotheses output/hypotheses.json
```

**或使用Python API：**

```python
from hypogenic import BaseTask

# 使用您的配置创建任务
task = BaseTask(config_path="./data/your_task/config.yaml")

# 生成假设
task.generate_hypotheses(method="hypogenic", num_hypotheses=20)

# 运行推理
results = task.inference(hypothesis_bank="./output/hypotheses.json")
```

## 何时使用此技能

在处理以下工作时使用此技能：
- 从观察数据集生成科学假设
- 系统性地测试多个竞争假设
- 将文献见解与经验模式结合
- 通过自动化假设构思加速研究发现
- 需要假设驱动分析的领域：欺骗检测、AI生成内容识别、心理健康指标、预测建模或其他经验研究

## 关键功能

**自动化假设生成**
- 在几分钟内从数据生成10-20+个可测试假设
- 基于验证性能的迭代优化
- 支持基于API（OpenAI、Anthropic）和本地LLM

**文献整合**
- 通过PDF处理从研究论文中提取见解
- 将理论基础与经验模式结合
- 使用GROBID进行系统的文献到假设流程

**性能优化**
- Redis缓存减少重复实验的API成本
- 大规模假设测试的并行处理
- 自适应优化专注于具有挑战性的示例

**灵活配置**
- 基于模板的提示工程与变量注入
- 特定于领域的自定义标签提取
- 模块化架构便于扩展

**经过验证的结果**
- 比少样本基线提高8.97%
- 比仅文献方法提高15.75%
- 80-84%的假设多样性（非冗余见解）
- 人类评估者报告显著的决策改进

## 核心功能

### 1. HypoGeniC：数据驱动的假设生成

仅通过迭代优化从观察数据生成假设。

**过程：**
1. 使用小数据子集初始化以生成候选假设
2. 基于性能迭代优化假设
3. 用来自具有挑战性示例的新假设替换性能不佳的假设

**最适合：** 没有现有文献的探索性研究、新数据集中的模式发现

### 2. HypoRefine：文献和数据整合

通过代理框架将现有文献与经验数据协同结合。

**过程：**
1. 从相关研究论文中提取见解（通常10篇论文）
2. 从文献生成基于理论的假设
3. 从观察模式生成数据驱动的假设
4. 通过迭代改进优化两个假设库

**最适合：** 具有既定理论基础的研究、验证或扩展现有理论

### 3. 联合方法

机制性地组合仅文献假设与框架输出。

**变体：**
- **Literature ∪ HypoGeniC**：结合文献假设与数据驱动生成
- **Literature ∪ HypoRefine**：结合文献假设与整合方法

**最适合：** 全面的假设覆盖、消除冗余同时保持多样化视角

## 安装

通过pip安装：
```bash
uv pip install hypogenic
```

**可选依赖项：**
- **Redis服务器**（端口6832）：启用LLM响应的缓存，以显著降低迭代假设生成期间的API成本
- **s2orc-doc2json**：在HypoRefine工作流中处理文献PDF所需
- **GROBID**：PDF预处理所需（参见文献处理部分）

**克隆示例数据集：**
```bash
# 对于HypoGeniC示例
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# 对于HypoRefine/Union示例
git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data
```

## 数据集格式

数据集必须遵循HuggingFace数据集格式，并具有特定的命名约定：

**必需文件：**
- `<TASK>_train.json`：训练数据
- `<TASK>_val.json`：验证数据
- `<TASK>_test.json`：测试数据

**JSON中的必需键：**
- `text_features_1`到`text_features_n`：包含特征值的字符串列表
- `label`：包含基本真值标签的字符串列表

**示例（标题点击预测）：**
```json
{
  "headline_1": [
    "What Up, Comet? You Just Got *PROBED*",
    "Scientists Made a Breakthrough in Quantum Computing"
  ],
  "headline_2": [
    "Scientists Everywhere Were Holding Their Breath Today. Here's Why.",
    "New Quantum Computer Achieves Milestone"
  ],
  "label": [
    "Headline 2 has more clicks than Headline 1",
    "Headline 1 has more clicks than Headline 2"
  ]
}
```

**重要说明：**
- 所有列表必须具有相同的长度
- 标签格式必须与您的`extract_label()`函数输出格式匹配
- 特征键可以自定义以匹配您的领域（例如，`review_text`、`post_content`等）

## 配置

每个任务需要一个`config.yaml`文件，指定：

**必需元素：**
- 数据集路径（train/val/test）
- 以下内容的提示模板：
  - 观察生成
  - 批量假设生成
  - 假设推理
  - 相关性检查
  - 自适应方法（用于HypoRefine）

**模板功能：**
- 数据集占位符用于动态变量注入（例如，`${text_features_1}`、`${num_hypotheses}`）
- 特定于领域的自定义标签提取函数
- 基于角色的提示结构（系统、用户、助手角色）

**配置结构：**
```yaml
task_name: your_task_name

train_data_path: ./your_task_train.json
val_data_path: ./your_task_val.json
test_data_path: ./your_task_test.json

prompt_templates:
  # 可重用提示组件的额外键
  observations: |
    特征1：${text_features_1}
    特征2：${text_features_2}
    观察：${label}

  # 必需模板
  batched_generation:
    system: "您的系统提示在此"
    user: "您的用户提示，带有${num_hypotheses}占位符"

  inference:
    system: "您的推理系统提示"
    user: "您的推理用户提示"

  # 高级功能的可选模板
  few_shot_baseline: {...}
  is_relevant: {...}
  adaptive_inference: {...}
  adaptive_selection: {...}
```

有关完整示例配置，请参阅`references/config_template.yaml`。

## 文献处理（HypoRefine/Union方法）

要使用基于文献的假设生成，必须预处理PDF论文。

> **注意：** 以下命令在克隆的 [HypoGenic 仓库](https://github.com/ChicagoHAI/hypothesis-generation) 中运行，而不是在此技能目录中。

**步骤1：设置GROBID**（仅首次）
```bash
bash ./modules/setup_grobid.sh
```

**步骤2：添加PDF文件**
将研究论文放在`literature/YOUR_TASK_NAME/raw/`中

**步骤3：处理PDF**
```bash
# 启动GROBID服务
bash ./modules/run_grobid.sh

# 为您的任务处理PDF
cd examples
python pdf_preprocess.py --task_name YOUR_TASK_NAME
```

这将PDF转换为结构化格式以进行假设提取。未来的版本将支持自动文献搜索。

## CLI使用

### 假设生成

```bash
hypogenic_generation --help
```

**关键参数：**
- 任务配置文件路径
- 模型选择（基于API或本地）
- 生成方法（HypoGeniC、HypoRefine或Union）
- 要生成的假设数量
- 假设库的输出目录

### 假设推理

```bash
hypogenic_inference --help
```

**关键参数：**
- 任务配置文件路径
- 假设库文件路径
- 测试数据集路径
- 推理方法（默认或多假设）
- 结果的输出文件

## Python API使用

对于编程控制和自定义工作流，直接在Python代码中使用Hypogenic：

### 基本HypoGeniC生成

```python
from hypogenic import BaseTask

# 首先克隆示例数据集
# git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# 使用自定义extract_label函数加载您的任务
task = BaseTask(
    config_path="./data/your_task/config.yaml",
    extract_label=lambda text: extract_your_label(text)
)

# 生成假设
task.generate_hypotheses(
    method="hypogenic",
    num_hypotheses=20,
    output_path="./output/hypotheses.json"
)

# 运行推理
results = task.inference(
    hypothesis_bank="./output/hypotheses.json",
    test_data="./data/your_task/your_task_test.json"
)
```

### HypoRefine/Union方法

```python
# 对于文献整合方法
# git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data

# 使用HypoRefine生成
task.generate_hypotheses(
    method="hyporefine",
    num_hypotheses=15,
    literature_path="./literature/your_task/",
    output_path="./output/"
)
# 这生成3个假设库：
# - HypoRefine（整合方法）
# - 仅文献假设
# - Literature∪HypoRefine（联合）
```

### 多假设推理

```python
from examples.multi_hyp_inference import run_multi_hypothesis_inference

# 同时测试多个假设
results = run_multi_hypothesis_inference(
    config_path="./data/your_task/config.yaml",
    hypothesis_bank="./output/hypotheses.json",
    test_data="./data/your_task/your_task_test.json"
)
```

### 自定义标签提取

`extract_label()`函数对于解析LLM输出至关重要。根据您的任务实施它：

```python
def extract_label(llm_output: str) -> str:
    """从LLM推理文本中提取预测的标签。

    默认行为：搜索'final answer:\s+(.*)'模式。
    为您的特定于领域的输出格式进行自定义。
    """
    import re
    match = re.search(r'final answer:\s+(.*)', llm_output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return llm_output.strip()
```

**重要：** 提取的标签必须与数据集`label`值中的格式匹配，以便正确计算准确性。

## 工作流示例

### 示例1：数据驱动的假设生成（HypoGeniC）

**场景：** 在没有既定理论框架的情况下检测AI生成的内容

**步骤：**
1. 准备带有文本样本和标签的数据集（人类vs AI生成）
2. 创建带有适当提示模板的`config.yaml`
3. 运行假设生成：
   ```bash
   hypogenic_generation --config config.yaml --method hypogenic --num_hypotheses 20
   ```
4. 在测试集上运行推理：
   ```bash
   hypogenic_inference --config config.yaml --hypotheses output/hypotheses.json --test_data data/test.json
   ```
5. 分析结果以查找正式性、语法精确度和语气差异等模式

### 示例2：文献告知的假设测试（HypoRefine）

**场景：** 基于现有研究进行酒店评论中的欺骗检测

**步骤：**
1. 收集10篇关于语言欺骗线索的相关论文
2. 准备带有真实和欺诈评论的数据集
3. 配置带有文献处理和数据生成模板的`config.yaml`
4. 运行HypoRefine：
   ```bash
   hypogenic_generation --config config.yaml --method hyporefine --papers papers/ --num_hypotheses 15
   ```
5. 测试检查代词频率、细节特异性和其他语言模式的假设
6. 比较基于文献和数据驱动的假设性能

### 示例3：全面的假设覆盖（联合方法）

**场景：** 最大化假设多样性的心理压力检测

**步骤：**
1. 从心理健康研究论文生成文献假设
2. 从社交媒体帖子生成数据驱动假设
3. 运行联合方法以组合和去重：
   ```bash
   hypogenic_generation --config config.yaml --method union --literature_hypotheses lit_hyp.json
   ```
4. 推理捕获理论构建（发布行为变化）和数据模式（情感语言转变）

## 性能优化

**缓存：** 启用Redis缓存以减少重复LLM调用的API成本和计算时间

**并行处理：** 利用多个工作程序进行大规模假设生成和测试

**自适应优化：** 使用具有挑战性的示例迭代改进假设质量

## 预期结果

使用hypogenic的研究已证明：
- AI内容检测任务的准确性提高14.19%
- 欺骗检测任务的准确性提高7.44%
- 80-84%的假设对提供独特、非冗余的见解
- 人类评估者在多个研究领域的帮助度评分很高

## 故障排除

**问题：** 生成的假设太通用
**解决方案：** 在`config.yaml`中优化提示模板，以请求更具体、可测试的假设

**问题：** 推理性能差
**解决方案：** 确保数据集有足够的训练示例，调整假设生成参数，或增加假设数量

**问题：** 标签提取失败
**解决方案：** 实施特定于领域的自定义`extract_label()`函数以进行输出解析

**问题：** GROBID PDF处理失败
**解决方案：** 确保GROBID服务正在运行（`bash ./modules/run_grobid.sh`）并且PDF是有效的研究论文

## 创建自定义任务

要向Hypogenic添加新任务或数据集：

### 步骤1：准备您的数据集

按照所需格式创建三个JSON文件：
- `your_task_train.json`
- `your_task_val.json`
- `your_task_test.json`

每个文件必须包含文本特征（`text_features_1`等）和`label`的键。

### 步骤2：创建config.yaml

使用以下内容定义您的任务配置：
- 任务名称和数据集路径
- 观察、生成、推理的提示模板
- 可重用提示组件的任何额外键
- 占位符变量（例如，`${text_features_1}`、`${num_hypotheses}`）

### 步骤3：实施extract_label函数

创建一个自定义标签提取函数，为您的领域解析LLM输出：

```python
from hypogenic import BaseTask

def extract_my_label(llm_output: str) -> str:
    """您的任务的自定义标签提取。

    必须以与数据集'label'字段相同的格式返回标签。
    """
    # 示例：从特定格式提取
    if "Final prediction:" in llm_output:
        return llm_output.split("Final prediction:")[-1].strip()

    # 回退到默认模式
    import re
    match = re.search(r'final answer:\s+(.*)', llm_output, re.IGNORECASE)
    return match.group(1).strip() if match else llm_output.strip()

# 使用您的自定义任务
task = BaseTask(
    config_path="./your_task/config.yaml",
    extract_label=extract_my_label
)
```

### 步骤4：（可选）处理文献

对于HypoRefine/Union方法：
1. 创建`literature/your_task_name/raw/`目录
2. 添加相关研究论文PDF
3. 运行GROBID预处理
4. 使用`pdf_preprocess.py`处理

### 步骤5：生成和测试

使用CLI或Python API运行假设生成和推理：

```bash
# CLI方法
hypogenic_generation --config your_task/config.yaml --method hypogenic --num_hypotheses 20
hypogenic_inference --config your_task/config.yaml --hypotheses output/hypotheses.json

# 或使用Python API（参见Python API使用部分）
```

## 仓库结构

了解仓库布局：

```
hypothesis-generation/
├── hypogenic/              # 核心软件包代码
├── hypogenic_cmd/          # CLI入口点
├── hypothesis_agent/       # HypoRefine代理框架
├── literature/            # 文献处理工具
├── modules/               # GROBID和预处理模块
├── examples/              # 示例脚本
│   ├── generation.py      # 基本HypoGeniC生成
│   ├── union_generation.py # HypoRefine/Union生成
│   ├── inference.py       # 单个假设推理
│   ├── multi_hyp_inference.py # 多个假设推理
│   └── pdf_preprocess.py  # 文献PDF处理
├── data/                  # 示例数据集（单独克隆）
├── tests/                 # 单元测试
└── IO_prompting/          # 提示模板和实验
```

**关键目录：**
- **hypogenic/**：带有BaseTask和生成逻辑的主要软件包
- **examples/**：常见工作流的参考实施
- **literature/**：用于PDF处理和文献提取的工具
- **modules/**：外部工具集成（GROBID等）

## 相关出版物

### HypoBench (2025)

Liu, H., Huang, S., Hu, J., Zhou, Y., & Tan, C. (2025). HypoBench: Towards Systematic and Principled Benchmarking for Hypothesis Generation. arXiv预印本 arXiv:2504.11524.

- **论文：** https://arxiv.org/abs/2504.11524
- **描述：** 假设生成方法的系统性和原则性基准测试框架

**BibTeX：**
```bibtex
@misc{liu2025hypobenchsystematicprincipledbenchmarking,
      title={HypoBench: Towards Systematic and Principled Benchmarking for Hypothesis Generation},
      author={Haokun Liu and Sicong Huang and Jingyu Hu and Yangqiaoyu Zhou and Chenhao Tan},
      year={2025},
      eprint={2504.11524},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2504.11524},
}
```

### Literature Meets Data (2024)

Liu, H., Zhou, Y., Li, M., Yuan, C., & Tan, C. (2024). Literature Meets Data: A Synergistic Approach to Hypothesis Generation. arXiv预印本 arXiv:2410.17309.

- **论文：** https://arxiv.org/abs/2410.17309
- **代码：** https://github.com/ChicagoHAI/hypothesis-generation
- **描述：** 介绍HypoRefine并展示基于文献和数据驱动假设生成的协同组合

**BibTeX：**
```bibtex
@misc{liu2024literaturemeetsdatasynergistic,
      title={Literature Meets Data: A Synergistic Approach to Hypothesis Generation},
      author={Haokun Liu and Yangqiaoyu Zhou and Mingxuan Li and Chenfei Yuan and Chenhao Tan},
      year={2024},
      eprint={2410.17309},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2410.17309},
}
```

### Hypothesis Generation with Large Language Models (2024)

Zhou, Y., Liu, H., Srivastava, T., Mei, H., & Tan, C. (2024). Hypothesis Generation with Large Language Models. In Proceedings of EMNLP Workshop of NLP for Science.

- **论文：** https://aclanthology.org/2024.nlp4science-1.10/
- **描述：** 用于数据驱动假设生成的原始HypoGeniC框架

**BibTeX：**
```bibtex
@inproceedings{zhou2024hypothesisgenerationlargelanguage,
      title={Hypothesis Generation with Large Language Models},
      author={Yangqiaoyu Zhou and Haokun Liu and Tejes Srivastava and Hongyuan Mei and Chenhao Tan},
      booktitle = {Proceedings of EMNLP Workshop of NLP for Science},
      year={2024},
      url={https://aclanthology.org/2024.nlp4science-1.10/},
}
```

## 其他资源

### 官方链接

- **GitHub仓库：** https://github.com/ChicagoHAI/hypothesis-generation
- **PyPI软件包：** https://pypi.org/project/hypogenic/
- **许可证：** MIT许可证
- **问题和支持：** https://github.com/ChicagoHAI/hypothesis-generation/issues

### 示例数据集

克隆这些仓库以获取即用型示例：

```bash
# HypoGeniC示例（仅数据驱动）
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# HypoRefine/Union示例（文献+数据）
git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data
```

### 社区与贡献

- **贡献者：** 7+个活跃贡献者
- **星标：** GitHub上89+个
- **主题：** research-tool、interpretability、hypothesis-generation、scientific-discovery、llm-application

有关贡献或问题，请访问GitHub仓库并查看问题页面。

## 本地资源

### references/

`config_template.yaml` - 完整的示例配置文件，包含所有必需的提示模板和参数。这包括：
- 任务配置的完整YAML结构
- 所有方法的示例提示模板
- 占位符变量文档
- 基于角色的提示示例

### scripts/

scripts目录可用于：
- 自定义数据准备工具
- 格式转换工具
- 分析和评估脚本
- 与外部工具集成

### assets/

assets目录可用于：
- 示例数据集和模板
- 示例假设库
- 可视化输出
- 文档补充材料
