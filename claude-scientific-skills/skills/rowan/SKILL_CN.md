---
name: rowan
description: Rowan 是一个云原生的分子建模与药物化学工作流平台，提供 Python API。可用于 pKa 和宏观 pKa（macropKa）预测、构象与互变异构体系综、分子对接与类似物对接、蛋白质-配体共折叠（cofolding）、MSA 生成、分子动力学、渗透性、描述符工作流，以及相关的小分子或蛋白质建模任务。非常适合程序化批量筛选、多步化学流程，以及原本需要维护本地 HPC/GPU 基础设施的工作流。
license: Proprietary (API key required)
compatibility: Python 3.12+ with rowan-python and its RDKit/stjames dependencies. Requires network access and ROWAN_API_KEY for hosted workflows.
metadata:
  version: "1.7"
  last-reviewed: "2026-09-30"
  upstream-version: "rowan-python 3.2.0"
  skill-author: Rowan Science
  trigger-keywords: pKa prediction, molecular docking, conformer search, chemistry workflow, drug discovery, SMILES, protein structure, batch molecular modeling, cloud chemistry
  openclaw:
    primaryEnv: ROWAN_API_KEY
    envVars:
    - name: ROWAN_API_KEY
      required: true
      description: Rowan computational chemistry API key.
---

# Rowan：云原生分子建模与药物设计工作流

## 概述

Rowan 是一个面向分子模拟、药物化学和基于结构的设计的云原生工作流平台。其 Python API 为小分子建模、性质预测、分子对接、分子动力学和 AI 结构工作流提供了统一的接口。

当你希望以编程方式运行药物化学或分子设计工作流，而又不想维护本地 HPC 基础设施、GPU 资源配置或一堆独立的建模工具时，请使用 Rowan。该服务管理托管计算资源和结果；可用的工作流取决于账户。

## 何时使用 Rowan

**Rowan 适用于：**

- 量子化学、半经验方法或神经网络势
- 批量性质预测（pKa、描述符、渗透性、溶解度）
- 构象和互变异构体系综生成
- 分子对接工作流（单配体、类似物系列、姿势优化）
- 蛋白质-配体共折叠和 MSA 生成
- 多步化学流程（例如：互变异构体搜索 → 分子对接 → 姿势分析）
- 需要一致、可扩展基础设施的批量药物化学项目

**Rowan 不适用于：**
- 简单的分子 I/O（直接使用 RDKit）
- 超出所选引擎文档支持范围的方法或元素/电荷体系

## 快速开始

```bash
uv pip install "rowan-python==3.2.0"
```

```python
import rowan
# 从环境变量中读取 ROWAN_API_KEY。

# 描述符需要三维 Molecule，而不是裸 SMILES 字符串。
mol = rowan.Molecule.from_smiles("CC(=O)Oc1ccccc1C(=O)O")
wf = rowan.submit_descriptors_workflow(mol, name="aspirin")
result = wf.result()

print(result.descriptors["MW"])       # 精确/单同位素质量
print(result.descriptors["SLogP"])
print(result.descriptors["TopoPSA"])  # 拓扑 PSA
```

这会提交一次托管计算并消耗积分。示例针对
[`rowan-python` 3.2.0](https://pypi.org/project/rowan-python/3.2.0/)，已于
2026-09-30 对照已发布的 SDK 和[官方参考文档](https://docs.rowansci.com/api/python/v3/)进行审核。
本地 schema/序列化冒烟测试使用的是 `stjames` 0.0.279。托管示例仅作说明之用：
此次更新未运行任何经过身份验证的工作流。为了项目的可复现性，
请锁定这两个包的版本。

## 安装

```bash
uv pip install "rowan-python==3.2.0"
# 在你自己的环境中锁定依赖；不要安装无关的 "rowan" 包。
```

## 身份验证与账户访问

### 身份验证

通过环境变量设置 API 密钥（推荐）：

```bash
export ROWAN_API_KEY="your_api_key_here"
```

或者直接在 Python 中设置：

```python
import rowan
rowan.api_key = "your_api_key_here"
```

验证身份：

```python
import rowan
user = rowan.whoami()  # 如果已通过身份验证，则返回用户信息
print(f"User: {user.email}")
print(f"Credits available: {user.credits_available_string()}")
print(user.enabled_workflows)  # 账户特定的后端工作流标识（slug）
```

## 分子输入格式

对基于拓扑的方法使用 SMILES，对基于几何结构的方法使用真实的三维结构。
SMARTS 是一种子结构查询语言，而不是通用的工作流分子输入；
InChI 需要先用化学工具包转换为受支持的输入后再传入。
记录立体化学、电荷、质子化状态和原始标识符。
仅靠规范化（canonicalization）并不能解决这些科学上的选择问题。

### SMILES 字符串与分子对象

- pKa：`starling` 和 `chemprop_nevolianis2025` 需要 SMILES 字符串；
  `gxtb_wagen2026`（默认）和 `aimnet2_wagen2024` 需要坐标。
- 构象搜索：SMILES 可用于 OpenConf（默认）或 ETKDG；CREST/MCMM
  需要三维分子。
- 膜渗透性：`gnn-mtl` 需要 SMILES；`pypermm` 需要三维分子。
- ADMET、LogP、macropKa 和溶解度基于 SMILES；姿势分析 MD 需要
  配体 SMILES **以及包含其结合姿势的蛋白质复合物**。
- 描述符、互变异构体、分子对接、类似物对接、BDE、NMR 和 Fukui 需要
  带有构象的 `rowan.Molecule`、`stjames.Molecule` 或 RDKit 分子。
  仅用 `Chem.MolFromSmiles()` 不会产生坐标。请使用
  `rowan.Molecule.from_smiles()` 显式生成坐标，或导入已有的几何结构。对于类似物
  对接，请在受体的坐标系中保留参考姿势。

**提示：**提交前使用 RDKit 验证 SMILES：

```python
from rdkit import Chem
smiles = "CCO"
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    raise ValueError(f"Invalid SMILES: {smiles}")
```

## 核心使用模式

大多数 Rowan 任务都遵循相同的三步模式：

1. **提交**工作流
2. **等待**完成（可选流式获取）
3. **获取**带有便捷属性的类型化结果

```python
import rowan

# 1. 提交 — 命名函数会构建并验证特定于工作流的负载
workflow = rowan.submit_descriptors_workflow(
    rowan.Molecule.from_smiles("CC(=O)Oc1ccccc1C(=O)O"),
    name="aspirin descriptors",
)

# 2. & 3. 等待并获取
result = workflow.result()  # 阻塞直到完成（默认：wait=True, poll_interval=5）
print(result.data)              # 原始字典
print(result.descriptors["MW"]) # 精确质量；没有 result.molecular_weight 属性
```

对于长时间运行的工作流，使用流式获取：

```python
for partial in workflow.stream_result(poll_interval=5):
    print(f"Complete: {partial.complete}")  # 布尔值，而不是百分比
    print(partial.data)
```

### result() 与 stream_result()

| 模式 | 适用场景 |
|---|---|
| `result()` | 进程可以阻塞等待完成 |
| `stream_result()` | 在作业运行期间轮询快照有用时 |

`stream_result()` 是轮询；它不是服务器推送的事件流。部分类型化属性
可能不可用，因此在 `.complete` 为 true 之前请检查 `.data`。
`result(wait=False)` 可能返回部分数据，或在尚无数据时抛出 `WorkflowError`。
`done()` 包括失败和已停止的运行，而不仅仅是成功的运行。

## 处理结果

Rowan 的 API 包含带有便捷属性的**类型化工作流结果对象**。

### 使用类型化属性和 .data

结果有两种访问模式：

1. **便捷属性**（建议优先使用）：`result.descriptors`、`result.best_pose`、`result.scores`。不同的结果类有所不同：构象搜索使用 `get_energies()` 和 `get_conformers()` 方法。
2. **原始数据回退**：`result.data` — 来自 API 的原始字典

示例：

```python
result = rowan.submit_descriptors_workflow(
    rowan.Molecule.from_smiles("CCO"),
    name="ethanol",
).result()

# 便捷属性（返回所有描述符）：
print(result.descriptors["MW"])       # 精确/单同位素质量
print(result.descriptors["SLogP"])
print(result.descriptors["TopoPSA"])  # 常用的拓扑 PSA

# 原始数据回退：
print(result.data["descriptors"])
```

**注意：**`DescriptorsResult` **没有** `molecular_weight` 属性。
`MW` 是精确/单同位素质量，而不是平均分子量。`TPSA` 是一个三维
带电表面描述符；在类药性规则中常用的拓扑极性表面积
请使用 `TopoPSA`。

### 缓存失效

某些结果属性是延迟加载的（例如构象几何结构、蛋白质结构）。要刷新：

```python
result.clear_cache()
new_structures = result.get_conformers()  # 对 ConformerSearchResult 重新获取
```

## 项目、文件夹与组织

对于不简单的项目，请使用项目和文件夹来保持工作有序。

### 项目

Rowan 3.2.0 存在一个未解析的 `Folder.created_at` 类型注解；在进行文件夹操作之前，
请按如下方式初始化一次模型（参见故障排除）。

```python
import rowan
from datetime import datetime
rowan.Folder.model_rebuild(_types_namespace={"datetime": datetime})

# 创建项目
project = rowan.create_project(name="CDK2 lead optimization")
rowan.project_uuid = project.uuid
folder = rowan.create_folder(name="descriptors", parent_uuid=project.root_folder_uuid)

# 提交时显式传入目标文件夹
wf = rowan.submit_descriptors_workflow(
    rowan.Molecule.from_smiles("CCO"), name="test compound", folder=folder
)

# parent_uuid 是文件夹 UUID，而不是项目 UUID。
project = rowan.retrieve_project(project.uuid)
workflows = rowan.list_workflows(parent_uuid=project.root_folder_uuid, page=0, size=50)
# 这只会列出直接位于根文件夹中的工作流。要查看上面的作业，请列出 folder.uuid。
```

### 文件夹

仅作说明：必须先准备好 `protein`、`pocket` 和三维 `ligand`。
先运行上面的 `Folder.model_rebuild` 初始化。`get_folder()` 会创建
缺失的路径段；`create_folder()` 只创建一个文件夹。

```python
# 创建层级文件夹结构
folder = rowan.get_folder("docking/batch_1/screening")

wf = rowan.submit_docking_workflow(
    protein=protein, pocket=pocket, initial_molecule=ligand,
    folder=folder,
    name="compound_001",
)

# 列出文件夹中的工作流
results = rowan.list_workflows(parent_uuid=folder.uuid, page=0, size=50)
```

列表辅助函数只返回一页。递增从零开始的 `page`，直到出现空页；
`size` 是页大小，而不是承诺返回所有匹配项。文件夹列表
不是递归的：在盘点一个项目时，需要分别遍历子文件夹。

## 工作流决策树

### pKa 与 MacropKa

**在以下情况使用微观 pKa：**

- 你需要单个可电离基团的 pKa
- 你关注的是酸碱转变和质子化热力学
- 分子有一到两个可电离位点
- 科学问题针对的是某个特定的微观转变

**在以下情况使用 macropKa：**

- 你需要在生理相关范围内（例如 0–14）的 pH 依赖行为
- 你需要跨 pH 的总电荷和质子化状态分布
- 分子有多个质子化相互耦合的可电离基团
- 你需要下游性质，例如不同 pH 下的水溶解度

**决策示例：**

```text
Phenol (pKa ~10): Use microscopic pKa
Amine (pKa ~9–10): Use microscopic pKa
Multi-ionizable drug (N, O, acidic group): Use macropKa
ADME assessment across GI pH: Use macropKa
```

### 构象搜索与互变异构体搜索

**在以下情况使用构象搜索：**

- 已知单一的互变异构形式
- 你需要多样化的三维系综用于分子对接、MD 或 SAR 分析
- 可旋转键主导化学空间

**在以下情况使用互变异构体搜索：**

- 互变异构平衡不确定（例如杂环、酮–烯醇体系）
- 你需要分子式相同的质子迁移异构体；电荷/质子化状态需单独枚举
- 下游计算（分子对接、pKa）依赖于互变异构形式

**组合工作流：**

```python
# 步骤 1：找到最佳互变异构体
taut_wf = rowan.submit_tautomer_search_workflow(
    initial_molecule=rowan.Molecule.from_smiles("O=c1cccc[nH]1"),
    name="2-pyridone tautomers",
)
best_taut = taut_wf.result().best_tautomer  # Molecule 或 None，而不是 SMILES
if best_taut is None:
    raise RuntimeError("No weighted tautomer structure was returned")

# 步骤 2：从最佳互变异构体生成构象
conf_wf = rowan.submit_conformer_search_workflow(
    initial_molecule=best_taut,
    name="2-pyridone conformers",
)
```

### 分子对接、类似物对接与共折叠

| 工作流 | 适用场景 | 输入 | 输出 |
|----------|----------|-------|--------|
| 分子对接 | 单个配体，已知口袋 | 蛋白质 + 三维配体 + 口袋坐标 | 姿势和打分记录 |
| 类似物对接 | 共享骨架的相关化合物 | 蛋白质 + SMILES 列表 + 结合态参考姿势 | 以 SMILES 为键的姿势和分数 |
| 蛋白质-配体共折叠 | 序列 + 配体，无晶体结构 | 蛋白质序列 + SMILES | 机器学习预测的结合复合物 |

## 蛋白质工具

### 上传蛋白质

下面的示例 API 调用需要已通过身份验证的账户和指定的本地文件；在本次文档修正中，它们未针对服务重新运行。在构建分子对接项目之前，请对照靶标核实每个 PDB 登录号：[1M17 是与厄洛替尼结合的 EGFR](https://www.rcsb.org/structure/1M17)。

```python
# 从本地 PDB 文件
protein = rowan.upload_protein(
    name="egfr_kinase_domain",
    file_path="egfr_kinase.pdb",
)

# 从 PDB 数据库
protein_from_pdb = rowan.create_protein_from_pdb_id(
    name="EGFR (1M17)",
    code="1M17",
)

# 获取之前上传的蛋白质
protein = rowan.retrieve_protein("protein-uuid")

# 列出第一页蛋白质
my_proteins = rowan.list_proteins(page=0, size=20)
```

### 蛋白质准备指南

- **文件格式**：`upload_protein` 对 `.cif`/`.mmcif` 选择 mmCIF，其他情况选择 PDB。
- **准备**：上传/导入只是存储结构；并不意味着已可用于分子对接。
  针对所选工作流，检查链的选择、替代位置、缺失的原子/残基、质子化、
  水分子、金属、辅因子以及保留的配体。
- **多链结构**：在适当时显式选择目标链。
- **准备工作流**：`submit_protein_preparation_workflow` 提供 pH、缺失原子
  补全和非聚合物保留等选项；在使用其默认值之前请检查这些设置。
- **口袋**：从准备好的受体或其结合配体推导坐标。任意的
  示例坐标不能在不同结构之间通用。通过对已知配体进行重对接并检查几何结构
  来验证分子对接；分数并不是测得的结合自由能。

## 工作流目录

九类常见工作流——描述符、微观 pKa、MacropKa、构象搜索、
互变异构体搜索、分子对接、类似物对接、MSA 生成和蛋白质-配体
共折叠——每类都附有提交代码和结果结构，另外还有一份
工作流函数目录（核心建模、基于结构的设计、高级计算
化学、反应化学、高级性质、结合自由能以及序列与
结构生物学），详见
[references/workflow_catalog.md](references/workflow_catalog.md)。

## 批量提交、Webhook 与异步工作

批量提交/轮询/获取、非阻塞的"提交后检查"模式、Webhook 设置、
密钥创建与轮换、签名验证（附 FastAPI
处理程序），以及已发布负载约定的限制，详见
[references/batch_and_webhooks.md](references/batch_and_webhooks.md)。

## 访问、定价与积分

账户访问、带日期的已发布积分费率以及项目预算指南，详见
[references/access_and_pricing.md](references/access_and_pricing.md)。

## 完整示例与故障排除

一个完整的先导化合物优化项目——项目设置、互变异构体、类似物系列的 pKa、
结果收集以及分子对接后续步骤——详见
[references/end_to_end_example.md](references/end_to_end_example.md)。

常见错误及其修复方法和调试技巧，详见
[references/troubleshooting.md](references/troubleshooting.md)。

## 推荐使用模式

- **优先使用 Rowan 原生工作流**，在存在原生工作流时不要用底层组件自行拼装
- 对任何不简单的项目（>5 个工作流）**使用项目和文件夹**
- **使用 `result()` 阻塞直到完成**（默认：`wait=True, poll_interval=5`）
- **优先使用类型化结果属性**，对于未映射的字段回退到 `.data`
- 对化合物库或类似物系列**使用批量提交**
- 对多步化学项目**串联工作流**：
  - `pKa → macropKa → permeability`（ADME 评估）
  - `tautomer search → docking → pose-analysis MD`（姿势优化）
  - `MSA generation → protein-ligand cofolding`（AI 结构预测）
- 对长时间运行的项目（>50 个工作流）或异步流程**使用 Webhook**
- 对大型构象/对接搜索**使用流式获取**以获得交互式反馈

## 总结

当你的工作流需要在云端执行分子设计任务时，请使用 Rowan，尤其是当你希望在小分子建模、蛋白质、分子对接、ADME 预测和机器学习结构生成之间使用统一的 API 和一致的结果处理方式时。

Rowan 是一个分子设计工作流平台，而不仅仅是一个远程化学引擎。它负责基础设施扩展、结果持久化和多步流程编排，让你可以专注于科学本身。
