---
name: perplexity-search
description: 通过LiteLLM和OpenRouter使用Perplexity模型执行AI驱动的网络搜索，获取实时信息。当进行网络搜索以获取当前信息、查找最近的科学文献、获取带来源引用的基于事实的答案，或访问超出模型知识截止日期的信息时，应使用此技能。通过单个OpenRouter API密钥提供对多个Perplexity模型的访问，包括Sonar Pro、Sonar Pro Search（高级智能体搜索）和Sonar Reasoning Pro。
license: MIT license
compatibility: 使用Perplexity搜索需要OpenRouter API密钥
metadata:
    skill-author: K-Dense Inc.
---

# Perplexity搜索

## 概述

通过LiteLLM和OpenRouter使用Perplexity模型执行AI驱动的网络搜索。Perplexity提供实时、基于网络的答案，并带有来源引用，非常适合查找当前信息、最近的科学文献以及模型训练数据截止日期之后的事实。

此技能通过OpenRouter提供对所有Perplexity模型的访问，只需一个API密钥（不需要单独的Perplexity账户）。

## 何时使用此技能

当以下情况时使用此技能：
- 搜索当前信息或最新发展（2024年及以后）
- 查找最新的科学出版物和研究
- 获取基于网络来源的实时答案
- 通过来源引用验证事实
- 跨多个领域进行文献搜索
- 访问超出模型知识截止日期的信息
- 进行特定领域的研究（生物医学、技术、临床）
- 比较当前方法或技术

**不要用于：**
- 简单计算或逻辑问题（直接使用）
- 需要代码执行的任务（使用标准工具）
- 模型训练数据中已有的问题（除非需要验证）

## 快速开始

### 设置（一次性）

1. **获取OpenRouter API密钥**：
   - 访问 https://openrouter.ai/keys
   - 创建账户并生成API密钥
   - 向账户添加 credits（建议最低$5）

2. **配置环境**：
   ```bash
   # 设置API密钥
   export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

   # 或使用设置脚本
   python scripts/setup_env.py --api-key sk-or-v1-your-key-here
   ```

3. **安装依赖**：
   ```bash
   uv pip install litellm
   ```

4. **验证设置**：
   ```bash
   python scripts/perplexity_search.py --check-setup
   ```

有关详细的设置说明、故障排除和安全最佳实践，请参阅`references/openrouter_setup.md`。

### 基本使用

**简单搜索：**
```bash
python scripts/perplexity_search.py "CRISPR基因编辑的最新发展是什么？"
```

**保存结果：**
```bash
python scripts/perplexity_search.py "最近的CAR-T疗法临床试验" --output results.json
```

**使用特定模型：**
```bash
python scripts/perplexity_search.py "比较mRNA和病毒载体疫苗" --model sonar-pro-search
```

**详细输出：**
```bash
python scripts/perplexity_search.py "用于药物发现的量子计算" --verbose
```

## 可用模型

通过`--model`参数访问模型：

- **sonar-pro**（默认）：通用搜索，成本和质量的最佳平衡
- **sonar-pro-search**：最先进的智能体搜索，具有多步推理
- **sonar**：基础模型，简单查询的最具成本效益
- **sonar-reasoning-pro**：具有逐步分析的高级推理
- **sonar-reasoning**：基础推理能力

**模型选择指南：**
- 默认查询 → `sonar-pro`
- 复杂多步分析 → `sonar-pro-search`
- 需要明确推理 → `sonar-reasoning-pro`
- 简单事实查询 → `sonar`
- 对成本敏感的批量查询 → `sonar`

有关详细比较、用例、定价和性能特征，请参阅`references/model_comparison.md`。

## 构建有效的查询

### 具体且详细

**好的例子：**
- "2024年发表的关于CAR-T细胞疗法治疗B细胞淋巴瘤的最新临床试验结果是什么？"
- "比较mRNA疫苗与病毒载体疫苗在COVID-19中的有效性和安全性特征"
- "解释AlphaFold3与AlphaFold2相比的改进，包括2023-2024年研究中的具体准确性指标"

**坏的例子：**
- "告诉我关于癌症治疗"（太宽泛）
- "CRISPR"（太模糊）
- "疫苗"（缺乏特异性）

### 包含时间限制

Perplexity搜索实时网络数据：
- "2024年在Nature Medicine上发表的关于长期COVID的论文有哪些？"
- "大型语言模型效率的最新发展（过去6个月）是什么？"
- "NeurIPS 2023关于AI安全的宣布是什么？"

### 指定领域和来源

为获得高质量结果，提及来源偏好：
- "根据高影响因子期刊的同行评审出版物..."
- "基于FDA批准的治疗..."
- "来自clinicaltrials.gov等临床试验注册中心..."

### 构建复杂查询

将复杂问题分解为清晰的组件：
1. **主题**：主要主题
2. **范围**：感兴趣的特定方面
3. **上下文**：时间框架、领域、约束
4. **输出**：期望的格式或答案类型

**示例：**
"根据2023年至2024年发表的研究，AlphaFold3在蛋白质结构预测方面与AlphaFold2相比有哪些改进？包括具体的准确性指标和基准测试。"

有关查询设计、特定领域模式和高级技术的全面指导，请参阅`references/search_strategies.md`。

## 常见用例

### 科学文献搜索

```bash
python scripts/perplexity_search.py \
  "最近的研究（2023-2024）关于肠道微生物组在帕金森病中的作用说了什么？重点关注同行评审研究并包括已识别的特定细菌种类。" \
  --model sonar-pro
```

### 技术文档

```bash
python scripts/perplexity_search.py \
  "如何使用Python实现从Kafka到PostgreSQL的实时数据流？包括处理背压和确保恰好一次语义的考虑。" \
  --model sonar-reasoning-pro
```

### 比较分析

```bash
python scripts/perplexity_search.py \
  "比较PyTorch与TensorFlow在实现Transformer模型方面的易用性、性能和生态系统支持。包括最近研究的基准测试。" \
  --model sonar-pro-search
```

### 临床研究

```bash
python scripts/perplexity_search.py \
  "间歇性禁食在成人2型糖尿病管理中的证据是什么？重点关注随机对照试验并报告HbA1c变化和体重减轻结果。" \
  --model sonar-pro
```

### 趋势分析

```bash
python scripts/perplexity_search.py \
  "过去5年单细胞RNA测序技术的关键趋势是什么？强调在通量、成本和分辨率方面的改进，并提供具体示例。" \
  --model sonar-pro
```

## 处理结果

### 程序化访问

将`perplexity_search.py`用作模块：

```python
from scripts.perplexity_search import search_with_perplexity

result = search_with_perplexity(
    query="CRISPR的最新发展是什么？",
    model="openrouter/perplexity/sonar-pro",
    max_tokens=4000,
    temperature=0.2,
    verbose=False
)

if result["success"]:
    print(result["answer"])
    print(f"使用的tokens: {result['usage']['total_tokens']}")
else:
    print(f"错误: {result['error']}")
```

### 保存和处理结果

```bash
# 保存为JSON
python scripts/perplexity_search.py "查询" --output results.json

# 使用jq处理
cat results.json | jq '.answer'
cat results.json | jq '.usage'
```

### 批量处理

创建脚本处理多个查询：

```bash
#!/bin/bash
queries=(
  "CRISPR发展2024"
  "mRNA疫苗技术进步"
  "AlphaFold3准确性改进"
)

for query in "${queries[@]}"; do
  echo "搜索: $query"
  python scripts/perplexity_search.py "$query" --output "results_$(echo $query | tr ' ' '_').json"
  sleep 2  # 速率限制

done
```

## 成本管理

Perplexity模型有不同的定价层级：

**每个查询的大致成本：**
- Sonar: $0.001-0.002（最具成本效益）
- Sonar Pro: $0.002-0.005（推荐默认）
- Sonar Reasoning Pro: $0.005-0.010
- Sonar Pro Search: $0.020-0.050+（最全面）

**成本优化策略：**
1. 对简单事实查询使用`sonar`
2. 对大多数查询默认使用`sonar-pro`
3. 对复杂分析保留`sonar-pro-search`
4. 设置`--max-tokens`限制响应长度
5. 在https://openrouter.ai/activity监控使用情况
6. 在OpenRouter仪表板设置支出限制

## 故障排除

### API密钥未设置

**错误**："OpenRouter API key not configured"

**解决方案**：
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
# 或运行设置脚本
python scripts/setup_env.py --api-key sk-or-v1-your-key-here
```

### LiteLLM未安装

**错误**："LiteLLM not installed"

**解决方案**：
```bash
uv pip install litellm
```

### 速率限制

**错误**："Rate limit exceeded"

**解决方案**：
- 等待几秒钟后重试
- 在https://openrouter.ai/keys增加速率限制
- 在批量处理中在请求之间添加延迟

###  credits不足

**错误**："Insufficient credits"

**解决方案**：
- 在https://openrouter.ai/account添加credits
- 启用自动充值以防止中断

有关全面的故障排除指南，请参阅`references/openrouter_setup.md`。

## 与其他技能的集成

此技能与其他科学技能互补：

### 文献综述

与`literature-review`技能一起使用：
1. 使用Perplexity查找最近的论文和预印本
2. 用实时网络结果补充PubMed搜索
3. 验证引用并找到相关工作
4. 发现数据库索引后的最新发展

### 科学写作

与`scientific-writing`技能一起使用：
1. 为引言/讨论部分查找最近的参考文献
2. 验证当前的技术状态
3. 检查最新的术语和约定
4. 识别最近的竞争方法

### 假设生成

与`hypothesis-generation`技能一起使用：
1. 搜索最新的研究发现
2. 识别当前知识差距
3. 发现最近的方法学进步
4. 发现新兴研究方向

### 批判性思维

与`scientific-critical-thinking`技能一起使用：
1. 寻找支持和反对假设的证据
2. 定位方法学批评
3. 识别领域内的争议
4. 用当前证据验证声明

## 最佳实践

### 查询设计

1. **具体**：包括领域、时间框架和约束
2. **使用术语**：领域适当的关键词和短语
3. **指定来源**：提及首选的出版物类型或期刊
4. **结构化问题**：具有明确上下文的清晰组件
5. **迭代**：基于初始结果进行改进

### 模型选择

1. **从sonar-pro开始**：对大多数查询的良好默认选择
2. **为复杂性升级**：对多步分析使用sonar-pro-search
3. **为简单性降级**：对基本事实使用sonar
4. **使用推理模型**：当需要逐步分析时

### 成本优化

1. **选择合适的模型**：将模型与查询复杂性匹配
2. **设置token限制**：使用`--max-tokens`控制成本
3. **监控使用情况**：定期检查OpenRouter仪表板
4. **高效批量处理**：在可能的情况下组合相关的简单查询
5. **缓存结果**：保存并重用重复查询的结果

### 安全

1. **保护API密钥**：永远不要提交到版本控制
2. **使用环境变量**：将密钥与代码分开
3. **设置支出限制**：在OpenRouter仪表板中配置
4. **监控使用情况**：观察意外活动
5. **轮换密钥**：定期更改密钥

## 资源

### 捆绑资源

**脚本：**
- `scripts/perplexity_search.py`：带有CLI界面的主要搜索脚本
- `scripts/setup_env.py`：环境设置和验证助手

**参考：**
- `references/search_strategies.md`：全面的查询设计指南
- `references/model_comparison.md`：详细的模型比较和选择指南
- `references/openrouter_setup.md`：完整的设置、故障排除和安全指南

**资产：**
- `assets/.env.example`：环境文件模板示例

### 外部资源

**OpenRouter：**
- 仪表板：https://openrouter.ai/account
- API密钥：https://openrouter.ai/keys
- Perplexity模型：https://openrouter.ai/perplexity
- 使用监控：https://openrouter.ai/activity
- 文档：https://openrouter.ai/docs

**LiteLLM：**
- 文档：https://docs.litellm.ai/
- OpenRouter提供商：https://docs.litellm.ai/docs/providers/openrouter
- GitHub：https://github.com/BerriAI/litellm

**Perplexity：**
- 官方文档：https://docs.perplexity.ai/

## 依赖

### 必需

```bash
# 用于API访问的LiteLLM
uv pip install litellm
```

### 可选

```bash
# 用于.env文件支持
uv pip install python-dotenv

# 用于JSON处理（通常预安装）
uv pip install jq
```

### 环境变量

必需：
- `OPENROUTER_API_KEY`：您的OpenRouter API密钥

可选：
- `DEFAULT_MODEL`：默认使用的模型（默认：sonar-pro）
- `DEFAULT_MAX_TOKENS`：默认最大tokens（默认：4000）
- `DEFAULT_TEMPERATURE`：默认温度（默认：0.2）

## 摘要

此技能提供：

1. **实时网络搜索**：访问超出训练数据截止日期的当前信息
2. **多个模型**：从成本效益高的Sonar到先进的Sonar Pro Search
3. **简单设置**：单个OpenRouter API密钥，无需单独的Perplexity账户
4. **全面指导**：关于查询设计和模型选择的详细参考
5. **成本效益**：按使用付费的定价，带有使用监控
6. **科学焦点**：为研究、文献搜索和技术查询优化
7. **易于集成**：与其他科学技能无缝协作

执行AI驱动的网络搜索，以查找当前信息、最近的研究和带有来源引用的基于事实的答案。