---
name: molfeat
description: 使用 Molfeat 对小分子进行特征化，用于 QSAR/QSPR、化学相似性、虚拟筛选和分子机器学习。涵盖 ECFP/MACCS 指纹、RDKit 描述符、药效团、预训练嵌入、配置持久化以及分子与标签的对齐。
license: Apache-2.0 license
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.11+ and molfeat 1.0.0 (RDKit, datamol, PyTorch). macOS Intel needs Python 3.11–3.12 and upstream platform-specific dependency pins. Optional extras and network access are needed for pretrained models; core fingerprints run offline.
metadata:
  version: "2.0"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-10-01"
  upstream-version: "1.0.0"
---

# Molfeat — 小分子特征化

## 何时使用

使用本技能可将 SMILES 或 RDKit 分子转换为指纹、描述符、药效团或预训练嵌入，用于分子机器学习和相似性检索。请在相同的分子划分和实验终点上比较各种表示。

本技能针对 **Molfeat 1.0.0**。此前针对 0.11 的运行时指导已经过时：1.x 支持现代 Python，并移除了 DGL/DGLLife、旧版 Graphormer 和蛋白质适配器。历史上的模型库卡片仍可能提到已被移除的适配器。带标签的 [1.0 迁移指南](https://github.com/datamol-io/molfeat/blob/1.0.0/docs/migration.md)和源码优先于文档 `stable` URL 下仍在提供的旧页面。

## 安装

创建一个隔离环境。核心示例在 Python 3.13.3/macOS Apple Silicon 上执行，使用 Molfeat 1.0.0、datamol 0.13.0、RDKit 2026.03.6 和 PyTorch 2.14.1。

```bash
uv venv --python 3.13 .venv-molfeat
uv pip install --python .venv-molfeat/bin/python "molfeat==1.0.0"
```

在 Windows 上，请使用 `.venv-molfeat\Scripts\python.exe` 作为解释器路径。上游支持 Python 3.11–3.14；macOS Intel 使用 Python 3.11–3.12、PyTorch 2.2.x、NumPy<2 和 Transformers<5。其他平台需要 PyTorch>=2.5。让 Molfeat 的平台标记来解析这些约束；不要将 Apple Silicon 的固定版本照搬到 Intel 上。

仅使用同一个解释器安装所需的 extras：`molfeat[transformer]==1.0.0` 用于 Hugging Face 模型，`[mordred]` 用于 mordredcommunity，`[pyg]` 用于图张量，`[fcd]` 用于 ChemNet 嵌入，`[selfies]` 用于 SELFIES 转换，`[cache]` 用于 HDF5/Parquet，`[viz]` 用于可视化，`[cloud]` 用于 S3/GCS 存储。DGL 和 Graphormer 的 extras 已不复存在。预训练推理可能会下载大量权重；请先检查模型许可、磁盘空间和设备要求。

## 工作流程

1. 保留源记录 ID、标签、原始结构，以及关于盐、立体化学、互变异构体、电荷和重复化合物的明确策略。标准化会改变化学身份；请对训练和预测应用相同的策略。
2. 从明确的 ECFP 基线开始。计算器（calculator）处理单个分子；`MoleculeTransformer` 对其进行批处理。`datamol.Mol` 是 RDKit 的分子类型。
3. 记录被拒绝的位置，并对齐每一个相关联的数组。单独检查描述符的 NaN/Inf：解析成功并不保证特征是有限值。
4. 在训练折内拟合任何特征选择、插补、缩放和模型。根据科学问题优先选择骨架/分组或时间划分；随机划分可能泄漏相近的类似物或重复测量。
5. 保存特征化器状态、有序的特征名称、包版本、分子预处理策略和输入 ID。迁移到 1.x 之后，请重新验证旧的状态。

### 指纹基线与无效记录

```python
import numpy as np
from molfeat.calc import FPCalculator
from molfeat.trans import MoleculeTransformer

smiles = ["CCO", "invalid", "CC(=O)O", "c1ccccc1"]
record_ids = np.array(["ethanol", "rejected", "acetate", "benzene"])
y = np.array([0.1, 9.9, 0.2, 0.3])  # toy labels only
calc = FPCalculator("ecfp", radius=2, fpSize=2048, includeChirality=True)
transformer = MoleculeTransformer(calc, n_jobs=1, dtype=np.float32)
X, valid_ids = transformer(smiles, ignore_errors=True)
assert X.shape == (3, 2048)
X_ids, y_valid = record_ids[valid_ids], y[valid_ids]
assert valid_ids == [0, 2, 3]
assert np.isfinite(X).all()
```

`ignore_errors` 属于调用，而不是构造函数。设为 `True` 时，`__call__` 返回经过滤的特征及原始输入位置；设为 `False` 时，遇到失败的分子会抛出异常。`transform(..., ignore_errors=True)` 通过对失败项使用 `None` 来保留位置。切勿对每个特征块单独过滤后再拼接。

ECFP 半径是键半径：`radius=2` 表示 ECFP4；radius 3 表示 ECFP6。在 1.0.0 中，`FPCalculator("ecfp")` 默认半径为 2、位数为 2048。`FPVecTransformer` 的默认长度*不同*，为 2000，因此使用它时请指定 `length=2048`。

### 配置往返

```python
transformer.to_state_yaml_file("featurizer.yml")
loaded = MoleculeTransformer.from_state_yaml_file("featurizer.yml")
np.testing.assert_array_equal(loaded(["CCO"]), transformer(["CCO"]))
```

仅加载可信的配置/制品。状态可以标识 Python 类和自定义的序列化可调用对象；YAML/JSON 并不会使任意第三方状态变得安全。状态保存的是配置，而不是实验标签、预处理决策或训练好的 QSAR 模型。

### 预训练嵌入

仅为示意；导入和签名已经检查过，但未下载任何模型权重：

```python
from molfeat.trans.pretrained import PretrainedHFTransformer

embedder = PretrainedHFTransformer(
    kind="ChemBERTa-77M-MLM", pooling="mean", concat_layers=-1,
    device="cpu", max_length=128, preload=False,
)
# First inference downloads/loads the model.
# embeddings = embedder(["CCO", "c1ccccc1"])
```

`PretrainedMolTransformer` 是基类，而不是按模型名称创建的工厂。请使用具体的适配器。嵌入的宽度取决于检查点、池化方式和所选层；不要假定是 768。请检查 token 长度：在 `max_length` 处截断可能会丢弃化学信息。请将模型修订版本、分词器、记号表示法、池化方式和最大长度与每个保存的嵌入缓存一并保留。

## 选择和发现表示

| 需求 | 起点 | 检查项 |
| --- | --- | --- |
| 指纹基线 | `FPCalculator("ecfp", radius=2, fpSize=2048)` | 手性、位碰撞、固定参数 |
| 结构键 | `FPCalculator("maccs")` | 167 项，包括未使用的第 0 位 |
| 命名描述符 | `RDKitDescriptors2D()` | 列取决于 RDKit；检查非有限值 |
| 药效团对 | `CATS()` | 距离分箱决定宽度；2D 默认为 189 |
| 3D 形状 | `USRDescriptors()` / `USRDescriptors("USRCAT")` | 需要构象；分别为 12 / 60 项 |
| 预训练语言模型 | `PretrainedHFTransformer(...)` | 权重、许可、分词、池化 |

有效名称和可选后端参见[可用特征化器](references/available_featurizers.md)，批处理/存储语义参见 [API 契约](references/api_reference.md)，预处理、拼接、3D 和相似性参见[示例演练](references/examples.md)，具备防泄漏意识的 QSAR 和有界内存筛选参见[模型选择](references/choosing_a_featurizer.md)。

对于发现，请构造 `ModelStore()` 并检查 `available_models`，或使用精确的 `search(name=...)`。首次发现调用会读取公开的 HTTPS 元数据。卡片的 `usage()` 以字符串形式返回代码；请审阅它，而不是自动执行。`store.load(...)` 返回 `(artifact, ModelInfo)`，而不是特征化器。历史卡片并不能证明某个适配器受支持。

## 性能与可复现性

对于小型作业和调试，请使用 `n_jobs=1`。请在实际工作负载上对有界并行进行基准测试；`n_jobs=-1` 可能成倍增加内存使用，并造成嵌套的 scikit-learn 并行。在继续之前，请持久化每个分块或对其评分；累积所有分块再调用 `vstack` 仍然需要将整个矩阵放入内存。缓存键必须包括分子身份、预处理、所有特征化器设置、包/模型版本以及行顺序。

## 来源与验证

于 2026-10-01 对照[发布版本](https://github.com/datamol-io/molfeat/releases/tag/1.0.0)、[包元数据](https://pypi.org/project/molfeat/1.0.0/)和[带标签的源码](https://github.com/datamol-io/molfeat/tree/1.0.0/molfeat)进行了审查。本地测试涵盖核心特征化契约和小型合成工作流；它们并不能确立预测有效性，也不能确立预训练/可选后端推理的支持情况。

## 引用 Scientific Agent Skills

本技能是 K-Dense 的 Scientific Agent Skills 的一部分。如果它对稿件、报告、演示文稿或代码发布有实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。该 DOI 和 https://arxiv.org/abs/2609.00065 会解析到最新的 arXiv 版本，因此切勿附加版本后缀，例如 `v1`。如果可以访问网络，请在撰写参考文献之前获取 https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中获取作者列表、年份和版本。如果该记录列出了期刊引用或出版商 DOI，则改为引用已发表的版本。
