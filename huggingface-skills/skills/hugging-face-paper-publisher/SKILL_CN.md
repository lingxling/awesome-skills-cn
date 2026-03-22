---
name: hugging-face-paper-publisher
description: 在 Hugging Face Hub 上发布和管理研究论文。支持创建论文页面、将论文链接到模型/数据集、声明作者身份以及生成专业的基于 markdown 的研究文章。
---

# 概述
此技能为 AI 工程师和研究人员提供了在 Hugging Face Hub 上发布、管理和链接研究论文的综合工具。它简化了从论文创建到发布的工作流程,包括与 arXiv 的集成、模型/数据集链接和作者身份管理。

## 与 HF 生态系统的集成
- **论文页面**: 在 Hugging Face Hub 上索引和发现论文
- **arXiv 集成**: 从 arXiv ID 自动索引论文
- **模型/数据集链接**: 通过元数据将论文链接到相关工件
- **作者身份验证**: 声明和验证论文作者身份
- **研究文章模板**: 生成专业的、现代的科学论文

# 版本
1.0.0

# 依赖项
- huggingface_hub>=0.26.0
- pyyaml>=6.0.3
- requests>=2.32.5
- markdown>=3.5.0
- python-dotenv>=1.2.1

# 核心功能

## 1. 论文页面管理
- **索引论文**: 从 arXiv 将论文添加到 Hugging Face
- **声明作者身份**: 验证和声明已发表论文的作者身份
- **管理可见性**: 控制哪些论文出现在您的个人资料上
- **论文发现**: 在 HF 生态系统中查找和探索论文

## 2. 将论文链接到工件
- **模型卡片**: 将论文引用添加到模型元数据
- **数据集卡片**: 通过 README 将论文链接到数据集
- **自动标记**: Hub 自动生成 arxiv:<PAPER_ID> 标签
- **引用管理**: 维护适当的归属和引用

## 3. 研究文章创建
- **Markdown 模板**: 生成专业的论文格式
- **现代设计**: 干净、可读的研究文章布局
- **动态目录**: 自动生成目录
- **章节结构**: 标准的科学论文组织
- **LaTeX 数学**: 支持方程和技术符号

## 4. 元数据管理
- **YAML 前置数据**: 适当的模型/数据集卡片元数据
- **引用跟踪**: 在存储库之间维护论文引用
- **版本控制**: 跟踪论文更新和修订
- **多论文支持**: 将多个论文链接到单个工件

# 使用说明

该技能在 `scripts/` 中包含用于论文发布操作的 Python 脚本。

### 先决条件
- 安装依赖项: `uv add huggingface_hub pyyaml requests markdown python-dotenv`
- 设置 `HF_TOKEN` 环境变量,使用写访问令牌
- 激活虚拟环境: `source .venv/bin/activate`

> **所有路径都是相对于包含此 SKILL.md 文件的目录。**
> 在运行任何脚本之前,首先 `cd` 到该目录或使用完整路径。


### 方法 1: 从 arXiv 索引论文

从 arXiv 将论文添加到 Hugging Face 论文页面。

**基本用法:**
```bash
uv run scripts/paper_manager.py index \
  --arxiv-id "2301.12345"
```

**检查论文是否存在:**
```bash
uv run scripts/paper_manager.py check \
  --arxiv-id "2301.12345"
```

**直接 URL 访问:**
您也可以直接访问 `https://huggingface.co/papers/{arxiv-id}` 来索引论文。

### 方法 2: 将论文链接到模型/数据集

使用适当的 YAML 元数据将论文引用添加到模型或数据集 README。

**添加到模型卡片:**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-id "2301.12345"
```

**添加到数据集卡片:**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/dataset-name" \
  --repo-type "dataset" \
  --arxiv-id "2301.12345"
```

**添加多篇论文:**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-ids "2301.12345,2302.67890,2303.11111"
```

**使用自定义引用:**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-id "2301.12345" \
  --citation "$(cat citation.txt)"
```

#### 链接如何工作

当您将 arXiv 论文链接添加到模型或数据集 README 时:
1. Hub 从链接中提取 arXiv ID
2. 标签 `arxiv:<PAPER_ID>` 自动添加到存储库
3. 用户可以单击标签查看论文页面
4. 论文页面显示引用此论文的所有模型/数据集
5. 论文可通过过滤器和搜索发现

### 方法 3: 声明作者身份

验证您在 Hugging Face 上发布的论文的作者身份。

**开始声明流程:**
```bash
uv run scripts/paper_manager.py claim \
  --arxiv-id "2301.12345" \
  --email "your.email@institution.edu"
```

**手动流程:**
1. 导航到您的论文页面: `https://huggingface.co/papers/{arxiv-id}`
2. 在作者列表中找到您的姓名
3. 单击您的姓名并选择"声明作者身份"
4. 等待管理员团队验证

**检查作者身份状态:**
```bash
uv run scripts/paper_manager.py check-authorship \
  --arxiv-id "2301.12345"
```

### 方法 4: 管理论文可见性

控制哪些验证的论文出现在您的公共个人资料上。

**列出您的论文:**
```bash
uv run scripts/paper_manager.py list-my-papers
```

**切换可见性:**
```bash
uv run scripts/paper_manager.py toggle-visibility \
  --arxiv-id "2301.12345" \
  --show true
```

**在设置中管理:**
导航到您的帐户设置 → 论文部分,为每篇论文切换"在个人资料上显示"。

### 方法 5: 创建研究文章

使用现代模板生成专业的基于 markdown 的研究论文。

**从模板创建:**
```bash
uv run scripts/paper_manager.py create \
  --template "standard" \
  --title "Your Paper Title" \
  --output "paper.md"
```

**可用模板:**
- `standard` - 传统的科学论文结构
- `modern` - 受 Distill 启发的干净、Web 友好格式
- `arxiv` - arXiv 风格格式
- `ml-report` - 机器学习实验报告

**生成完整论文:**
```bash
uv run scripts/paper_manager.py create \
  --template "modern" \
  --title "Fine-Tuning Large Language Models with LoRA" \
  --authors "Jane Doe, John Smith" \
  --abstract "$(cat abstract.txt)" \
  --output "paper.md"
```

**转换为 HTML:**
```bash
uv run scripts/paper_manager.py convert \
  --input "paper.md" \
  --output "paper.html" \
  --style "modern"
```

### 论文模板结构

**标准研究论文章节:**
```markdown
---
title: Your Paper Title
authors: Jane Doe, John Smith
affiliations: University X, Lab Y
date: 2025-01-15
arxiv: 2301.12345
tags: [machine-learning, nlp, fine-tuning]
---

# Abstract
论文的简要摘要...

# 1. Introduction
背景和动机...

# 2. Related Work
先前研究和背景...

# 3. Methodology
方法和实现...

# 4. Experiments
设置、数据集和程序...

# 5. Results
发现和分析...

# 6. Discussion
解释和含义...

# 7. Conclusion
总结和未来工作...

# References
```

**现代模板功能:**
- 动态目录
- 用于 Web 查看的响应式设计
- 代码语法高亮
- 交互式图形和图表
- 数学方程渲染(LaTeX)
- 引用管理
- 作者隶属关系链接

### 命令参考

**索引论文:**
```bash
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
```

**链接到存储库:**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/repo-name" \
  --repo-type "model|dataset|space" \
  --arxiv-id "2301.12345" \
  [--citation "Full citation text"] \
  [--create-pr]
```

**声明作者身份:**
```bash
uv run scripts/paper_manager.py claim \
  --arxiv-id "2301.12345" \
  --email "your.email@edu"
```

**管理可见性:**
```bash
uv run scripts/paper_manager.py toggle-visibility \
  --arxiv-id "2301.12345" \
  --show true|false
```

**创建研究文章:**
```bash
uv run scripts/paper_manager.py create \
  --template "standard|modern|arxiv|ml-report" \
  --title "Paper Title" \
  [--authors "Author1, Author2"] \
  [--abstract "Abstract text"] \
  [--output "filename.md"]
```

**将 Markdown 转换为 HTML:**
```bash
uv run scripts/paper_manager.py convert \
  --input "paper.md" \
  --output "paper.html" \
  [--style "modern|classic"]
```

**检查论文状态:**
```bash
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
```

**列出您的论文:**
```bash
uv run scripts/paper_manager.py list-my-papers
```

**搜索论文:**
```bash
uv run scripts/paper_manager.py search --query "transformer attention"
```

### YAML 元数据格式

将论文链接到模型或数据集时,需要适当的 YAML 前置数据:

**模型卡片示例:**
```yaml
---
language:
  - en
license: apache-2.0
tags:
  - text-generation
  - transformers
  - llm
library_name: transformers
---

# Model Name

此模型基于 [Our Paper](https://arxiv.org/abs/2301.12345) 中描述的方法。

## Citation

```bibtex
@article{doe2023paper,
  title={Your Paper Title},
  author={Doe, Jane and Smith, John},
  journal={arXiv preprint arXiv:2301.12345},
  year={2023}
}
```
```

**数据集卡片示例:**
```yaml
---
language:
  - en
license: cc-by-4.0
task_categories:
  - text-generation
  - question-answering
size_categories:
  - 10K<n<100K
---

# Dataset Name

数据集在 [Our Paper](https://arxiv.org/abs/2301.12345) 中介绍。

有关更多详细信息,请参阅 [论文页面](https://huggingface.co/papers/2301.12345)。
```

Hub 自动从这些链接中提取 arXiv ID 并创建 `arxiv:2301.12345` 标签。

### 集成示例

**工作流程 1: 发布新研究**
```bash
# 1. 创建研究文章
uv run scripts/paper_manager.py create \
  --template "modern" \
  --title "Novel Fine-Tuning Approach" \
  --output "paper.md"

# 2. 编辑 paper.md 的内容

# 3. 提交到 arXiv(外部流程)
# 上传到 arxiv.org,获取 arXiv ID

# 4. 在 Hugging Face 上索引
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"

# 5. 链接到您的模型
uv run scripts/paper_manager.py link \
  --repo-id "your-username/your-model" \
  --repo-type "model" \
  --arxiv-id "2301.12345"

# 6. 声明作者身份
uv run scripts/paper_manager.py claim \
  --arxiv-id "2301.12345" \
  --email "your.email@edu"
```

**工作流程 2: 链接现有论文**
```bash
# 1. 检查论文是否存在
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"

# 2. 如需要则索引
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"

# 3. 链接到多个存储库
uv run scripts/paper_manager.py link \
  --repo-id "username/model-v1" \
  --repo-type "model" \
  --arxiv-id "2301.12345"

uv run scripts/paper_manager.py link \
  --repo-id "username/training-data" \
  --repo-type "dataset" \
  --arxiv-id "2301.12345"

uv run scripts/paper_manager.py link \
  --repo-id "username/demo-space" \
  --repo-type "space" \
  --arxiv-id "2301.12345"
```

**工作流程 3: 使用论文引用更新模型**
```bash
# 1. 获取当前 README
huggingface-cli download username/model-name README.md

# 2. 添加论文链接
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-id "2301.12345" \
  --citation "Full citation for the paper"

# 脚本将:
# - 如果缺少则添加 YAML 元数据
# - 在 README 中插入 arXiv 链接
# - 添加格式化的引用
# - 保留现有内容
```

### 最佳实践

1. **论文索引**
   - 在 arXiv 上发布论文后立即索引
   - 在模型/数据集卡片中包含完整的引用信息
   - 在相关存储库中使用一致的论文引用

2. **元数据管理**
   - 为所有模型/数据集卡片添加 YAML 前置数据
   - 包含适当的许可信息
   - 使用相关的任务类别和域进行标记

3. **作者身份**
   - 声明您作为作者列出的论文的作者身份
   - 使用机构电子邮件地址进行验证
   - 保持论文可见性设置更新

4. **存储库链接**
   - 将论文链接到所有相关的模型、数据集和 Spaces
   - 在 README 描述中包含论文背景
   - 添加 BibTeX 引用以便于参考

5. **研究文章**
   - 在项目中一致地使用模板
   - 在论文中包含代码和数据链接
   - 生成 Web 友好的 HTML 版本以进行共享

### 高级用法

**批量链接论文:**
```bash
# 将多篇论文链接到一个存储库
for arxiv_id in "2301.12345" "2302.67890" "2303.11111"; do
  uv run scripts/paper_manager.py link \
    --repo-id "username/model-name" \
    --repo-type "model" \
    --arxiv-id "$arxiv_id"
done
```

**提取论文信息:**
```bash
# 从 arXiv 获取论文元数据
uv run scripts/paper_manager.py info \
  --arxiv-id "2301.12345" \
  --format "json"
```

**生成引用:**
```bash
# 创建 BibTeX 引用
uv run scripts/paper_manager.py citation \
  --arxiv-id "2301.12345" \
  --format "bibtex"
```

**验证链接:**
```bash
# 检查存储库中的所有论文链接
uv run scripts/paper_manager.py validate \
  --repo-id "username/model-name" \
  --repo-type "model"
```

### 错误处理

- **论文未找到**: arXiv ID 不存在或尚未索引
- **权限被拒绝**: HF_TOKEN 缺少对存储库的写访问权限
- **无效的 YAML**: README 前置数据中的元数据格式错误
- **作者身份失败**: 电子邮件与论文作者记录不匹配
- **已声明**: 另一个用户已声明作者身份
- **速率限制**: 短时间内 API 请求过多

### 故障排除

**问题**: "Hugging Face 上未找到论文"
- **解决方案**: 访问 `hf.co/papers/{arxiv-id}` 以触发索引

**问题**: "作者身份声明未验证"
- **解决方案**: 等待管理员审查或联系 HF 支持并提供证明

**问题**: "arXiv 标记未出现"
- **解决方案**: 确保 README 包含适当的 arXiv URL 格式

**问题**: "无法链接到存储库"
- **解决方案**: 验证 HF_TOKEN 具有写权限

**问题**: "模板渲染错误"
- **解决方案**: 检查 markdown 语法和 YAML 前置数据格式

### 资源和参考

- **Hugging Face 论文页面**: [hf.co/papers](https://huggingface.co/papers)
- **模型卡片指南**: [hf.co/docs/hub/model-cards](https://huggingface.co/docs/hub/en/model-cards)
- **数据集卡片指南**: [hf.co/docs/hub/datasets-cards](https://huggingface.co/docs/hub/en/datasets-cards)
- **研究文章模板**: [tfrere/research-article-template](https://huggingface.co/spaces/tfrere/research-article-template)
- **arXiv 格式指南**: [arxiv.org/help/submit](https://arxiv.org/help/submit)

### 与 tfrere 的研究模板集成

此技能通过提供以下内容补充 [tfrere 的研究文章模板](https://huggingface.co/spaces/tfrere/research-article-template):

- 自动化论文索引工作流程
- 存储库链接功能
- 元数据管理工具
- 引用生成实用程序

您可以使用 tfrere 的模板进行编写,然后使用此技能在 Hugging Face Hub 上发布和链接论文。

### 常见模式

**模式 1: 新论文发布**
```bash
# 编写 → 发布 → 索引 → 链接
uv run scripts/paper_manager.py create --template modern --output paper.md
# (提交到 arXiv)
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
uv run scripts/paper_manager.py link --repo-id "user/model" --arxiv-id "2301.12345"
```

**模式 2: 现有论文发现**
```bash
# 搜索 → 检查 → 链接
uv run scripts/paper_manager.py search --query "transformers"
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
uv run scripts/paper_manager.py link --repo-id "user/model" --arxiv-id "2301.12345"
```

**模式 3: 作者作品集管理**
```bash
# 声明 → 验证 → 组织
uv run scripts/paper_manager.py claim --arxiv-id "2301.12345"
uv run scripts/paper_manager.py list-my-papers
uv run scripts/paper_manager.py toggle-visibility --arxiv-id "2301.12345" --show true
```

### API 集成

**Python 脚本示例:**
```python
from scripts.paper_manager import PaperManager

pm = PaperManager(hf_token="your_token")

# 索引论文
pm.index_paper("2301.12345")

# 链接到模型
pm.link_paper(
    repo_id="username/model",
    repo_type="model",
    arxiv_id="2301.12345",
    citation="Full citation text"
)

# 检查状态
status = pm.check_paper("2301.12345")
print(status)
```

### 未来增强功能

未来版本计划的功能:
- 支持非 arXiv 论文(会议论文集、期刊)
- 从 DOI 自动引用格式化
- 论文比较和版本控制工具
- 协作论文编写功能
- 与 LaTeX 工作流程集成
- 自动图形和表格提取
- 论文指标和影响跟踪
