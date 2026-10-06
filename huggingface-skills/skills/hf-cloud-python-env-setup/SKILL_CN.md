---
name: hf-cloud-python-env-setup
description: '为 SageMaker / AWS 相关工作搭建一个隔离的 Python 环境，使用正确的 Python 版本和最新的 boto3。每当需要为 SageMaker 部署、训练任务或任何 AWS 自动化任务执行 Python 代码时使用此技能——包括即将运行 `pip install`、即将调用 `boto3`、创建或激活一个虚拟环境，或用户要求"搭建环境"的时候。永远不要使用系统 Python，也永远不要往系统 Python 里 `pip install`。始终做隔离。此技能可以防止最常见的几种失败模式：Python 版本错误、依赖冲突，以及过时的 SDK。'
---

# SageMaker 的 Python 环境搭建

许多看起来像是 AWS 问题的 SageMaker 部署失败，实际上是 Python 环境问题：Python 版本错误、依赖解析出错、SDK 过时而不认识当前的 API。此技能让环境搭建变得枯燥但正确。

## 核心规则

1. **永远不要使用系统 Python。** 始终在一个隔离的环境中工作。
2. **固定 Python 版本，而不是固定软件包版本。** 使用 3.10、3.11 或 3.12。避免使用 3.13 及以上版本——机器学习库的 wheel 包可用性会滞后，依赖解析会以令人困惑的方式出错。
3. **安装每个软件包的最新版本。** 不要出于防御性心理固定 `boto3` 或 `awscli` 的版本。更新的版本拥有当前的 API 接口和安全修复。只有当用户明确要求特定版本时才固定版本。
4. **正确检查已安装的版本。** 使用 `importlib.metadata.version("package-name")`，永远不要用 `module.__version__`。后者在不同软件包之间表现不一致。
5. **随附的脚本直接使用 `boto3`。** SageMaker Python SDK 是一个合理的替代方案——参见下面的"boto3 与 SageMaker SDK 的对比"。

## boto3 与 SageMaker SDK 的对比

随附的部署脚本（`deploy.py`、`deploy_async.py`、`teardown.py`）直接使用 `boto3`，并从 [AWS 发布的深度学习容器目录](https://aws.github.io/deep-learning-containers/reference/available_images/) 中读取镜像 URI。这符合本工作流显式分阶段的设计——每个技能产出一个具体的值（区域、角色 ARN、镜像 URI），供下一个技能使用——而 `boto3` 是稳定的底层 API 客户端。

当用户更倾向于使用 SageMaker Python SDK（v3），或他们的项目已经在用它时，使用它也没问题。自 [PR #5960](https://github.com/aws/sagemaker-python-sdk/pull/5960)（2026 年 6 月）以来，`ModelBuilder` 会自动将 HuggingFace 模型路由到当前的容器（文本生成 → HuggingFace vLLM，多模态 → vLLM-Omni，嵌入模型 → TEI）。不要因为担心镜像过时或容器选错而回避使用该 SDK——这一路由规则已经固定下来了。

仍需注意的两个具体 SDK 场景：

- **生成式重排序器**：该 SDK 会无条件将 `text-ranking` 任务路由到 TEI，这对于像 Qwen3-Reranker 这样的因果语言模型重排序器来说是错误的——这类模型需要 vLLM（参见 `hf-cloud-serving-image-selection`）。对这些模型要显式指定容器。
- **SSO 假设角色凭证**：v3 版本中 `ModelTrainer` / `FrameworkProcessor` 在 SSO 配置文件下存在凭证解析方面的回归问题。如果 SDK 调用因凭证错误失败，而同一个 shell 中 `aws sts get-caller-identity` 却能成功，请先怀疑这个问题，而不是你的 AWS 配置。

如果你使用该 SDK，请像其他软件包一样把它安装到隔离环境中（`.venv/bin/python -m pip install sagemaker`）。随附的脚本并不需要它。

## 如何搭建

最快的方式是使用随附的脚本——它是 Python 写的，因此在 Windows、macOS 和 Linux 上运行方式相同：

```bash
python3 scripts/setup_env.py        # macOS / Linux
python  scripts/setup_env.py        # Windows (PowerShell / cmd)
```

该脚本会检测是否有 `uv`，如果有就使用它（速度更快），否则回退到标准库的 `venv` 模块，用 Python 3.12 创建 `.venv/`（可用 `python3 setup_env.py .venv 3.11` 覆盖版本），拒绝不受支持的 Python 版本，从随附的 `requirements.txt` 安装依赖，并且是幂等的。它还会打印出适用于当前主机操作系统的正确解释器路径（见下文）。

手动等效操作：

```bash
# 首选：uv
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python --upgrade boto3 awscli   # Windows: .venv\Scripts\python.exe

# 备选：标准库 venv
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip boto3 awscli
```

搭建完成后，**显式调用该环境的 Python**，而不要激活虚拟环境。解释器路径因平台而异：

```bash
.venv/bin/python deploy.py            # macOS / Linux
.venv\Scripts\python.exe deploy.py    # Windows
```

无论是在脚本、交互式 shell，还是在代理工具调用中，这种做法效果都一样。为简洁起见，本技能的其余部分都写作 `.venv/bin/python`——在 Windows 上请替换为 `.venv\Scripts\python.exe`。

## 验证

```bash
.venv/bin/python scripts/check_versions.py
```

打印出 `boto3`、`botocore`、`awscli` 的版本。它使用 `importlib.metadata.version()`，因此对任何软件包都适用，包括没有 `__version__` 的软件包。可以传入任意名称：`... check_versions.py transformers huggingface_hub`。

## 部署相关的额外依赖

默认的 `requirements.txt` 涵盖了 SageMaker 编排所需的内容。某些部署需要额外的依赖（用于模型检查的 `huggingface_hub`，用于分词器验证的 `transformers`）。将这些依赖添加到项目中一个针对特定部署的 requirements 文件里，用该环境的 Python 安装，除非有理由，否则不要固定版本。

## 常见陷阱

**莫名其妙的 `pip install` 解析错误**
几乎总是因为 Python 3.13+ 尝试安装还没有 wheel 包的软件包，或者安装到了一个被污染的系统 Python 中。重新在 3.12 上创建：删除 `.venv` 并重新运行 `python3 setup_env.py .venv 3.12`（该脚本在版本不匹配时会重新创建环境，因此你也可以直接重新运行它）。

**`pip install` 成功了，但脚本报"module not found"**
你安装到了与运行脚本时不同的解释器中。始终显式调用 Python：`.venv/bin/python -m pip install ...` 以及 `.venv/bin/python deploy.py`。

**内联的 `python -c "..."` 单行命令在 PowerShell 中失败**
PowerShell 的引号规则会破坏内联 Python 中嵌套/转义的引号。不要去调试引号问题——把代码片段写到一个小的 `.py` 文件中再运行。（随附的所有辅助工具正是出于这个原因才都写成文件的。）

**boto3 调用失败，报"unknown parameter"**
你的 boto3 版本比 API 接口更旧。用 `.venv/bin/python -m pip install --upgrade boto3` 升级。不要为了匹配旧版本而降级脚本。

**安装了 `sagemaker`（该 SDK），但随附的脚本仍然失败**
随附的脚本不使用该 SDK——它们只需要 `requirements.txt` 中的 `boto3`/`awscli`。同时安装 `sagemaker` 并无害处，但它不能替代 requirements 的安装。
