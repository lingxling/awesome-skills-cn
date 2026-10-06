---
name: esm
description: 使用 Biohub esm Python SDK 进行 ESM3 蛋白质生成、ESMC 嵌入以及 ESMFold2 全原子折叠。适用于本地模型推理和 Biohub 托管客户端，包括以前的 Forge 工作流程；并与独立的旧版 fair-esm 发行版相区分。
license: MIT license
compatibility: Requires Python 3.12+ and esm 3.4.1.post1. Local pretrained inference needs model weights and sufficient RAM or GPU memory; hosted inference needs network access and ESM_API_KEY. Use an isolated environment, separate from fair-esm.
metadata:
  version: "2.0"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-09-30"
  upstream-version: "3.4.1.post1"
---

# ESM：蛋白质生成、嵌入与折叠

## 何时使用

用于 Biohub 的 `esm` SDK：ESM3 掩码多模态生成、ESMC 序列
表示以及 ESMFold2 全原子预测。以前的 Forge 平台
已迁移至 `https://biohub.ai`，包括 ESM3；SDK 类名仍包含
`Forge`。本技能面向已发布的 **esm 3.4.1.post1**，并已对照
其 wheel 包和当前官方文档进行验证。

`fair-esm` 是 Meta 独立的、较旧的 ESM2/ESMFold/ESM-IF 发行版。两个
软件包的导入名均为 `esm`；请将它们安装在不同的环境中。旧版
`esm.pretrained.esm2_*` 接口不是 Biohub ESMC 接口。Hugging Face
Transformers 原生的 ESMC 实现是另一套 API：不要将其
版本要求或输出类型与本 SDK 混用。

## 安装与模型选择

```bash
uv venv --python 3.12 .venv-esm
uv pip install --python .venv-esm/bin/python "esm==3.4.1.post1"
```

该版本声明要求 Python >=3.12、Torch >=2.11,<2.12 以及 Transformers
>=4.57.6,<5。已在 CPU 上测试了 Python 3.12、Torch 2.11.0 和 Transformers 4.57.6。
Linux x86_64 安装会包含 GPU 专用依赖；请使用受支持的
推理机器并预留磁盘空间。Flash Attention 是可选的；对于微型 CPU 测试
则不需要。不要将此技术栈安装到包含不兼容 Transformers 或 Torch 版本锁定的
共享环境中。

| 任务 | 本地模型/API | 托管客户端/模型 |
| --- | --- | --- |
| ESM3 序列/结构/功能生成 | `ESM3.from_pretrained("esm3-sm-open-v1")` | `client("esm3-medium-2024-08")`；small/large ID 见 ESM3 参考文档 |
| ESMC 嵌入 | `EsmcForMaskedLM` 和 `EsmcTokenizer`；`biohub/ESMC-300M`、`biohub/ESMC-600M`、`biohub/ESMC-6B` | `esmc_client("esmc-600m-2024-12")`；300M/6B 也有文档说明 |
| ESMFold2 全原子结构 | `EsmFold2Model`、`ESMFold2InputBuilder`；`biohub/ESMFold2` | `esmfold2_client("esmfold2-fast-2026-05")` |

ESMC 6B 权重现在可在本地使用。当前 Biohub 模型卡标明为
MIT 许可，ESMC 模型卡还链接了第三方声明；请查看
所选具体产物的模型卡和访问要求。
较旧的 `ESMC` 类仍作为已弃用的兼容性包装器保留。本地
模型大小、托管可用性和账户配额是不同的约束；
更大的模型并不能保证在特定实验上表现更好。

## 工作流程

1. 明确序列/链/残基映射，以及目标是
   生成、表示提取还是折叠。保留输入 ID 和
   来源信息。对于普通单链序列中意外出现的 `...`、空格、FASTA 标题行或空位（gap），
   应予以拒绝，而不是静默删除。
2. 选择本地检查点或明确的托管模型 ID。在支持的情况下，记录 SDK、检查点
   版本、模型设置、掩码位置和随机种子。
3. 检查每个 SDK 结果是否为 `ESMProteinError`。托管服务的失败可能
   作为返回值返回。使用有限的请求超时、上下文管理器和有界
   并发。参见 [托管服务约定](references/forge-api.md)。
4. 验证输出约定：序列长度和固定残基、仅含残基的
   嵌入轴，或链/原子映射及置信度。将模型预测
   与实验验证分开。
5. 将序列/结构与设置和标识符一起保存。当模型、结构、功能或生成设置不同时，
   避免使用仅以序列为键的缓存。

## ESM3 补全与全新结构预测

以下为预训练推理的示意；本次更新中未运行任何权重或托管作业。
此玩具序列仅演示 API 机制，并非功能性设计。

```python
import torch
from esm.models.esm3 import ESM3
from esm.sdk.api import ESMProtein, ESMProteinError, GenerationConfig

model = ESM3.from_pretrained("esm3-sm-open-v1", device=torch.device("cpu"))
prompt = "MPRT___KEND"
completed = model.generate(
    ESMProtein(sequence=prompt),
    GenerationConfig(track="sequence", num_steps=3, temperature=0.7),
)
if isinstance(completed, ESMProteinError):
    raise completed
assert completed.sequence is not None and len(completed.sequence) == len(prompt)
assert "_" not in completed.sequence
assert all(a == "_" or a == b for a, b in zip(prompt, completed.sequence))

# 使用全新的仅含序列的提示，防止旧坐标对此检查产生条件影响。
folded = model.generate(
    ESMProtein(sequence=completed.sequence),
    GenerationConfig(track="structure", num_steps=8),
)
if isinstance(folded, ESMProteinError):
    raise folded
assert folded.coordinates is not None
folded.to_pdb("candidate.pdb")
```

生成会填充被掩码的位置。在已补全的轨道上再次调用它
并不会实现精修或温度退火；请显式地重新掩码选定的
位置或清除该轨道。ESM3 结构生成与 ESMFold2 预测
使用不同的模型和结果类型。有关反向折叠、功能词表和坐标约定，
参见 [ESM3](references/esm3-api.md)。

## 使用正确残基池化的 ESMC 嵌入

以下为预训练加载的示意；相同的 API 和池化已在 CPU 上使用
随机初始化的微型模型执行过。导入随附的辅助模块时，请将本技能的 `scripts/` 目录添加到
`PYTHONPATH`。

```python
from esm.models.esmc import EsmcForMaskedLM, EsmcTokenizer
from esm_embeddings import embed_sequences

model = EsmcForMaskedLM.from_pretrained("biohub/ESMC-300M", device="cpu").eval()
tokenizer = EsmcTokenizer()
sequences = ["MPRTKEINDAGLIVHSPQWFYK", "ACDEFGHIK"]
features = embed_sequences(model, tokenizer, sequences)
assert features.shape == (2, 960)
```

`output.last_hidden_state` 的形状为 `(B,T,D)`，并包含 CLS、EOS 和填充；
`T` 不是原始残基数。[scripts/esm_embeddings.py](scripts/esm_embeddings.py)
执行一个真正的填充批次，排除特殊 token/填充 token，验证
残基数，并按输入顺序返回 `(B,D)` 的 CPU 特征。请根据序列长度和可用内存
选择批次大小。它不会截断序列、下载权重
或联系服务。有关托管输出类型、
逐残基提取、梯度行为和迁移细节，参见 [ESMC](references/esm-c-api.md)。

## 托管服务认证与折叠

只从环境中读取所需的凭据；显式传递它，以便
在创建客户端时进行解析。SDK 工厂函数的默认值会在导入时捕获
`ESM_API_KEY`。在
[Biohub 开发者控制台](https://biohub.ai/developer-console/api-keys)中创建密钥。

认证推理示意：

```python
import os
from esm.sdk import esmfold2_client
from esm.sdk.api import ESMProteinError, FoldingConfig
from esm.utils.structure.input_builder import ProteinInput, StructurePredictionInput

fold_input = StructurePredictionInput(
    sequences=[ProteinInput(id="A", sequence="MPRTKEINDAGLIVHSPQWFYK")]
)
with esmfold2_client(
    model="esmfold2-fast-2026-05", url="https://biohub.ai",
    token=os.environ["ESM_API_KEY"], request_timeout=300,
) as client:
    result = client.fold_all_atom(fold_input, config=FoldingConfig())
if isinstance(result, ESMProteinError):
    raise result
with open("candidate.cif", "w") as handle:
    handle.write(result.complex.to_mmcif())
```

有关 MSA、置信度和复合物输入约定，请使用 [Biohub/ESMFold2 参考](references/biohub-platform.md)。
快速托管模型会忽略 MSA。
公开源代码和模拟请求可验证客户端约定；但它们无法
确认账户访问权限、服务可用性或预测质量。

## 科学性检查

- 功能注释使用受支持的 tokenizer 标签和**从 1 开始、闭区间**的
  范围；诸如 `enzymatic_activity` 之类的任意标签不是有效的提示。
- ESM3 坐标是 atom37 布局的张量；缺失原子使用 NaN。张量
  复制使用 `.clone()`。请指定 PDB 链，而不要假设默认值
  会选择一条链；当前默认值为 `chain_id="all"`。
- 预测坐标、pLDDT 和 pTM 不能衡量热力学稳定性、
  结合亲和力或催化活性。反向折叠得到的序列需要重新
  预测、基于匹配残基的结构比较以及实验筛选。
- 嵌入相似性并不能保证同源性/功能。使用考虑同源性的划分
  来评估监督模型；在训练数据上拟合归一化和降维。
  报告不确定性和独立留出集指标。
- 参见 [完整工作流程示例](references/workflows.md)，了解变体文库、
  结构条件设计以及聚类，其中不使用缺乏依据的稳定性
  评分，也不使用会在微小数据集上失败的固定 PCA/t-SNE 设置。

## 验证与来源

[references/review.md](references/review.md) 记录了官方来源、已执行的
CPU 测试和局限性。在仓库中运行 `python tests/run_all.py --isolated esm`，
以测试合成本地模型、池化、输入序列化、
PDB 往返以及模拟的托管服务约定。预训练的 ESM3/ESMC/ESMFold2、
CUDA 推理和认证服务均未执行。

请遵守所选模型的条款以及
[Biohub 可接受使用政策](https://biohub.org/acceptable-use-policy/)。

## 引用 Scientific Agent Skills

本技能是 K-Dense 发布的 Scientific Agent Skills 的一部分。如果它对某份手稿、报告、演示文稿
或代码发布有实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。DOI 和 https://arxiv.org/abs/2609.00065 会解析到最新的 arXiv 版本，
因此切勿附加 `v1` 之类的版本后缀。在可以访问网络时，在撰写参考文献之前先获取
https://arxiv.org/abs/2609.00065（或 http://export.arxiv.org/api/query?id_list=2609.00065），
并从该记录中获取作者列表、年份和版本。如果该记录列出了期刊引用或出版商 DOI，
则改为引用已发表的版本。
