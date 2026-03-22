---
name: denario
description: 用于科学研究辅助的多代理 AI 系统，可自动化从数据分析到发表的研究工作流。此技能应用于从数据集生成研究想法、开发研究方法、执行计算实验、进行文献检索或生成 LaTeX 格式的发表就绪论文时。支持带有可自定义代理编排的端到端研究管道。
license: GPL-3.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Denario

## 概述

Denario 是一个多代理 AI 系统，旨在自动化从初始数据分析到发表就绪手稿的科学研究工作流。基于 AG2 和 LangGraph 框架构建，它协调多个专业代理来处理假设生成、方法开发、计算分析和论文写作。

## 何时使用此技能

在以下情况下使用此技能：
- 分析数据集以生成新颖的研究假设
- 开发结构化的研究方法
- 执行计算实验并生成可视化
- 进行文献检索以获取研究背景
- 从研究结果编写期刊格式的 LaTeX 论文
- 自动化从数据到发表的完整研究管道

## 安装

使用 uv（推荐）安装 denario：

```bash
uv init
uv add "denario[app]"
```

或使用 pip：

```bash
uv pip install "denario[app]"
```

对于 Docker 部署或从源代码构建，请参阅 `references/installation.md`。

## LLM API 配置

Denario 需要来自支持的 LLM 提供商的 API 密钥。支持的提供商包括：
- Google Vertex AI
- OpenAI
- 其他与 AG2/LangGraph 兼容的 LLM 服务

使用环境变量或 `.env` 文件安全地存储 API 密钥。有关包括 Vertex AI 设置在内的详细配置说明，请参阅 `references/llm_configuration.md`。

## 核心研究工作流

Denario 遵循结构化的四阶段研究管道：

### 1. 数据描述

通过指定可用数据和工具来定义研究背景：

```python
from denario import Denario

den = Denario(project_dir="./my_research")
den.set_data_description("""
可用数据集：X 和 Y 的时间序列数据
工具：pandas、sklearn、matplotlib
研究领域：[指定领域]
""")
```

### 2. 想法生成

从数据描述生成研究假设：

```python
den.get_idea()
```

这将根据描述的数据产生研究问题或假设。或者，提供自定义想法：

```python
den.set_idea("自定义研究假设")
```

### 3. 方法开发

开发研究方法：

```python
den.get_method()
```

这创建调查假设的结构化方法。也可以接受带有自定义方法的 markdown 文件：

```python
den.set_method("path/to/methodology.md")
```

### 4. 结果生成

执行计算实验并生成分析：

```python
den.get_results()
```

这将运行方法、执行计算、创建可视化并产生发现。也可以提供预先计算的结果：

```python
den.set_results("path/to/results.md")
```

### 5. 论文生成

创建发表就绪的 LaTeX 论文：

```python
from denario import Journal

den.get_paper(journal=Journal.APS)
```

生成的论文包括为指定期刊的正确格式、集成图表和完整的 LaTeX 源代码。

## 可用期刊

Denario 支持多种期刊格式样式：
- `Journal.APS` - 美国物理学会格式
- 其他期刊可能可用；请参阅 `references/research_pipeline.md` 获取完整列表

## 启动 GUI

运行图形用户界面：

```bash
denario run
```

这将启动一个用于交互式研究工作流管理的基于 Web 的界面。

## 常见工作流

### 端到端研究管道

```python
from denario import Denario, Journal

# 初始化项目
den = Denario(project_dir="./research_project")

# 定义研究背景
den.set_data_description("""
数据集：[现象]的时间序列测量
可用工具：pandas、sklearn、scipy
研究目标：调查[研究问题]
""")

# 生成研究想法
den.get_idea()

# 开发方法
den.get_method()

# 执行分析
den.get_results()

# 创建发表物
den.get_paper(journal=Journal.APS)
```

### 混合工作流（自定义 + 自动化）

```python
# 提供自定义研究想法
den.set_idea("使用时间序列分析调查 X 和 Y 之间的相关性")

# 自动生成方法
den.get_method()

# 自动生成结果
den.get_results()

# 生成论文
den.get_paper(journal=Journal.APS)
```

### 文献检索集成

有关文献检索功能和额外工作流示例，请参阅 `references/examples.md`。

## 高级功能

- **多代理编排**：AG2 和 LangGraph 协调用于不同研究任务的专业代理
- **可重复研究**：所有阶段产生可版本控制的结构化输出
- **期刊集成**：自动格式化以适应目标发表场所
- **灵活输入**：每个管道阶段的手动或自动化
- **Docker 部署**：带有 LaTeX 和所有依赖项的容器化环境

## 详细参考

有关全面的文档：
- **安装选项**：`references/installation.md`
- **LLM 配置**：`references/llm_configuration.md`
- **完整 API 参考**：`references/research_pipeline.md`
- **示例工作流**：`references/examples.md`

## 故障排除

常见问题和解决方案：
- **API 密钥错误**：确保正确设置了环境变量（请参阅 `references/llm_configuration.md`）
- **LaTeX 编译**：安装 TeX 发行版或使用预安装 LaTeX 的 Docker 镜像
- **包冲突**：使用虚拟环境或 Docker 进行隔离
- **Python 版本**：需要 Python 3.12 或更高版本
