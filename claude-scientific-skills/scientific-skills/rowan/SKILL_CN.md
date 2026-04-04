---
name: rowan
description: Rowan 是一个云原生分子建模和药物化学工作流平台，带有 Python API。用于 pKa 和 macropKa 预测、构象和互变异构体集合、对接和类似物对接、蛋白质-配体共折叠、MSA 生成、分子动力学、通透性、描述符工作流，以及相关的小分子或蛋白质建模任务。非常适合程序化批量筛选、多步化学管道，以及原本需要维护本地 HPC/GPU 基础设施的工作流。
license: Proprietary (API key required)
compatibility: Python 3.12+, API key required
metadata:
  skill-author: Rowan Science
  trigger-keywords: ["pKa prediction", "molecular docking", "conformer search", "chemistry workflow", "drug discovery", "SMILES", "protein structure", "batch molecular modeling", "cloud chemistry"]
---

# Rowan：云原生分子建模和药物设计工作流

## 概述

Rowan 是一个云原生工作流平台，用于分子模拟、药物化学和基于结构的设计。其 Python API 为小分子建模、属性预测、对接、分子动力学和 AI 结构工作流提供统一接口。

当您希望以编程方式运行药物化学或分子设计工作流，而无需维护本地 HPC 基础设施、GPU 配置或单独的建模工具集合时，使用 Rowan。Rowan 处理所有基础设施、结果管理和计算扩展。

## 何时使用 Rowan

**Rowan 适合：**

- 量子化学、半经验方法或神经网络势能
- 批量属性预测（pKa、描述符、通透性、溶解度）
- 构象和互变异构体集合生成
- 对接工作流（单配体、类似物系列、构象优化）
- 蛋白质-配体共折叠和 MSA 生成
- 多步化学管道（例如，互变异构体搜索 → 对接 → 构象分析）
- 批量药物化学活动，需要一致、可扩展的基础设施

**Rowan 不适合：**
- 简单的分子 I/O（直接使用 RDKit）
- 后 HF *ab initio* 量子化学或相对论计算

## 访问和定价模型

Rowan 使用基于信用的使用模型。所有用户，包括免费 tier 用户，都可以创建 API 密钥并使用 Python API。

### 免费 tier 访问

- 访问所有 Rowan 核心工作流
- 每周 20 个信用
- 500 个注册信用

### 定价和信用消耗

信用根据计算类型消耗：

- **CPU**：每分钟 1 个信用
- **GPU**：每分钟 3 个信用
- **H100/H200 GPU**：每分钟 7 个信用

购买的信用按信用定价，自购买之日起有效期最长为一年。

### 典型成本估算

| 工作流 | 典型运行时间 | 估算信用 | 说明 |
|----------|----------------|-------------------|-------|
| 描述符 | <1 分钟 | 0.5–2 | 轻量级，适合筛选 |
| pKa（单跃迁） | 2–5 分钟 | 2–5 | 取决于分子大小 |
| MacropKa（pH 0–14） | 5–15 分钟 | 5–15 | 更广泛的采样，更高成本 |
| 构象搜索 | 3–10 分钟 | 3–10 | 集合质量很重要 |
| 互变异构体搜索 | 2–5 分钟 | 2–5 | 杂环系统 |
| 对接（单配体） | 5–20 分钟 | 5–20 | 取决于口袋大小、优化 |
| 类似物对接系列（10–50 配体） | 30–120 分钟 | 30–100+ | 共享参考框架 |
| MSA 生成 | 5–30 分钟 | 5–30 | 序列长度依赖 |
| 蛋白质-配体共折叠 | 15–60 分钟 | 20–50+ | AI 结构预测，GPU 密集 |

## 快速开始

```bash
uv pip install rowan-python
```

```python
import rowan
rowan.api_key = "your_api_key_here"  # 或设置 ROWAN_API_KEY 环境变量

# 提交描述符工作流 — 不到一分钟完成
wf = rowan.submit_descriptors_workflow("CC(=O)Oc1ccccc1C(=O)O", name="aspirin")
result = wf.result()

print(result.descriptors['MW'])    # 180.16
print(result.descriptors['SLogP']) # 1.19
print(result.descriptors['TPSA'])  # 59.44
```

如果打印无错误，则设置正确。

## 安装

```bash
uv pip install rowan-python
# 或: pip install rowan-python
```

## 用户和 webhook 管理

### 认证

通过环境变量设置 API 密钥（推荐）：

```bash
export ROWAN_API_KEY="your_api_key_here"
```

或在 Python 中直接设置：

```python
import rowan
rowan.api_key = "your_api_key_here"
```

验证认证：

```python
import rowan
user = rowan.whoami()  # 认证成功返回用户信息
print(f"User: {user.email}")
print(f"Credits available: {user.credits_available_string}")
```

### Webhook 密钥管理

对于 webhook 签名验证，通过用户账户管理密钥：

```python
import rowan

# 获取当前 webhook 密钥（如果不存在返回 None）
secret = rowan.get_webhook_secret()
if secret is None:
    secret = rowan.create_webhook_secret()
print(f"Secret key: {secret.secret}")

# 轮换密钥（使旧密钥无效，创建新密钥）
# 定期使用此功能以提高安全性
new_secret = rowan.rotate_webhook_secret()
print(f"New secret created (old secret disabled): {new_secret.secret}")

# 验证传入的 webhook 签名
is_valid = rowan.verify_webhook_secret(
    request_body=b"...",           # 原始请求体（字节）
    signature="X-Rowan-Signature", # 来自请求头
    secret=secret.secret
)
```

## 分子输入格式

Rowan 接受以下格式的分子：

- **SMILES**（首选）：`"CCO"`、`"c1ccccc1O"`
- **SMARTS 模式**（某些工作流）：用于子结构匹配的 SMARTS 子集
- **InChI**（如果您的 API 版本支持）：`"InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"`

API 将验证输入，如果分子无法解析，将引发 `rowan.ValidationError`。始终使用规范的 SMILES 以确保可重现性。

**提示：** 使用 RDKit 在提交前验证 SMILES：

```python
from rdkit import Chem
smiles = "CCO"
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    raise ValueError(f"Invalid SMILES: {smiles}")
```

## 核心使用模式

大多数 Rowan 任务遵循相同的三步模式：

1. **提交** 工作流
2. **等待** 完成（可选流式处理）
3. **检索** 带便利属性的类型化结果

```python
import rowan

# 1. 提交 — 使用特定的工作流函数（不是通用的 submit_workflow）
workflow = rowan.submit_descriptors_workflow(
    "CC(=O)Oc1ccccc1C(=O)O",
    name="aspirin descriptors",
)

# 2. & 3. 等待和检索
result = workflow.result()  # 阻塞直到完成（默认：wait=True, poll_interval=5）
print(result.data)              # 原始字典
print(result.descriptors['MW']) # 180.16 — 使用 result.descriptors 字典，不是 result.molecular_weight
```

对于长时间运行的工作流，使用流式处理：

```python
for partial in workflow.stream_result(poll_interval=5):
    print(f"Progress: {partial.complete}%")
    print(partial.data)
```

### result() vs. stream_result()

| 模式 | 何时使用 | 持续时间 |
|---------|----------|----------|
| `result()` | 您可以等待完整结果 | <5 分钟典型 |
| `stream_result()` | 您希望获得进度反馈或需要早期部分结果 | >5 分钟，或交互式使用 |

**指南：** 对描述符、pKa 使用 `result()`。对构象搜索、对接、共折叠使用 `stream_result()`。

## 处理结果

Rowan 的 API 包括 **类型化工作流结果对象**，带有便利属性。

### 使用类型化属性和 .data

结果有两种访问模式：

1. **便利属性**（推荐首选）：`result.descriptors`、`result.best_pose`、`result.conformer_energies`
2. **原始回退**：`result.data` — 来自 API 的原始字典

示例：

```python
result = rowan.submit_descriptors_workflow(
    "CCO",
    name="ethanol",
).result()

# 便利属性（返回所有描述符的字典）：
print(result.descriptors['MW'])   # 46.042
print(result.descriptors['SLogP'])  # -0.001
print(result.descriptors['TPSA'])   # 57.96

# 原始数据回退（描述符嵌套在 'descriptors' 键下）：
print(result.data['descriptors'])
# {'MW': 46.042, 'SLogP': -0.001, 'TPSA': 57.96, 'nHBDon': 1.0, 'nHBAcc': 1.0, ...}
```

**注意：** `DescriptorsResult` **没有** `molecular_weight` 属性。描述符键使用短名称（`MW`、`SLogP`、`nHBDon`），不是冗长的名称。

### 缓存失效

一些结果属性是惰性加载的（例如，构象几何、蛋白质结构）。要刷新：

```python
result.clear_cache()
new_structures = result.conformer_molecules  # 重新获取
```

## 项目、文件夹和组织

对于非平凡的活动，使用项目和文件夹来保持工作组织。

### 项目

```python
import rowan

# 创建项目
project = rowan.create_project(name="CDK2 lead optimization")
rowan.set_project("CDK2 lead optimization")

# 所有后续工作流都进入此项目
wf = rowan.submit_descriptors_workflow("CCO", name="test compound")

# 稍后检索
project = rowan.retrieve_project("CDK2 lead optimization")
workflows = rowan.list_workflows(project=project, size=50)
```

### 文件夹

```python
# 创建分层文件夹结构
folder = rowan.create_folder(name="docking/batch_1/screening")

wf = rowan.submit_docking_workflow(
    # ... docking params ...
    folder=folder,
    name="compound_001",
)

# 列出文件夹中的工作流
results = rowan.list_workflows(folder=folder)
```

## 工作流决策树

### pKa vs. MacropKa

**使用微观 pKa 当：**

- 您需要单个可离子化基团的 pKa
- 您对酸碱跃迁和质子化热力学感兴趣
- 分子有一个或两个可离子化位点
- 速度至关重要（更快，更少信用）

**使用 macropKa 当：**

- 您需要跨生理相关范围（例如 0–14）的 pH 依赖性行为
- 您希望获得跨 pH 的聚合电荷和质子化状态分布
- 分子有多个可离子化基团，具有耦合的质子化
- 您需要下游属性，如不同 pH 下的水溶性

**示例决策：**

```text
苯酚 (pKa ~10)：使用微观 pKa
胺 (pKa ~9–10)：使用微观 pKa
多离子化药物 (N, O, 酸性基团)：使用 macropKa
跨 GI pH 的 ADME 评估：使用 macropKa
```

### 构象搜索 vs. 互变异构体搜索

**使用构象搜索当：**

- 单一互变异构形式已知
- 您需要用于对接、MD 或 SAR 分析的多样化 3D 集合
- 可旋转键主导化学空间

**使用互变异构体搜索当：**

- 互变异构平衡不确定（例如，杂环、酮-烯醇系统）
- 您需要建模所有相关的质子化异构体
- 下游计算（对接、pKa）依赖于互变异构形式

**组合工作流：**

```python
# 步骤 1：找到最佳互变异构体
taut_wf = rowan.submit_tautomer_search_workflow(
    initial_molecule="O=c1[nH]ccnc1",
    name="imidazole tautomers",
)
best_taut = taut_wf.result().best_tautomer

# 步骤 2：从最佳互变异构体生成构象
conf_wf = rowan.submit_conformer_search_workflow(
    initial_molecule=best_taut,
    name="imidazole conformers",
)
```

### 对接 vs. 类似物对接 vs. 共折叠

| 工作流 | 何时使用 | 输入 | 输出 |
|----------|----------|-------|--------|
| 对接 | 单配体，已知口袋 | 蛋白质 + SMILES + 口袋坐标 | 构象、分数、dG |
| 类似物对接 | 5–100+ 相关化合物 | 蛋白质 + SMILES 列表 + 参考配体 | 所有构象，参考对齐 |
| 蛋白质-配体共折叠 | 序列 + 配体，无晶体结构 | 蛋白质序列 + SMILES | ML 预测的结合复合物 |

## 常见工作流类别

### 1. 描述符

批量筛选、SAR 或探索性脚本的轻量级入口点。

```python
wf = rowan.submit_descriptors_workflow(
    "CC(=O)Oc1ccccc1C(=O)O",  # 位置参数，接受 SMILES 字符串
    name="aspirin descriptors",
)

result = wf.result()
print(result.descriptors['MW'])    # 180.16
print(result.descriptors['SLogP']) # 1.19
print(result.descriptors['TPSA'])  # 59.44
print(result.data['descriptors'])
# {'MW': 180.16, 'SLogP': 1.19, 'TPSA': 59.44, 'nHBDon': 1.0, 'nHBAcc': 4.0, ...}
```

**常见描述符键：**

| 键 | 描述 | 典型药物范围 |
|-----|-------------|-------------------|
| `MW` | 分子量 (Da) | <500 (Lipinski) |
| `SLogP` | 计算的 LogP（亲脂性） | -2 到 +5 |
| `TPSA` | 拓扑极性表面积 (Å²) | <140 用于口服生物利用度 |
| `nHBDon` | H-键供体计数 | ≤5 (Lipinski) |
| `nHBAcc` | H-键受体计数 | ≤10 (Lipinski) |
| `nRot` | 可旋转键计数 | <10 用于口服药物 |
| `nRing` | 环计数 | — |
| `nHeavyAtom` | 重原子计数 | — |
| `FilterItLogS` | 估算的水溶性 (LogS) | >-4 优选 |
| `Lipinski` | Lipinski Ro5 通过 (1.0) 或失败 (0.0) | — |

结果包含数百个额外的分子描述符（BCUT、GETAWAY、WHIM 等）；通过 `result.descriptors['key']` 访问任何描述符。

### 2. 微观 pKa

用于特定结构的质子化状态能量学和酸碱行为。

有两种方法可用：

| 方法 | 输入 | 速度 | 覆盖范围 | 何时使用 |
|--------|-------|-------|--------|----------|
| `chemprop_nevolianis2025` | SMILES 字符串 | 快 | 仅去质子化（阴离子共轭碱） | 仅酸性基团；快速筛选 |
| `starling` | SMILES 字符串 | 快 | 酸 + 碱（完全质子化/去质子化） | 大多数类药物分子；首选 SMILES 方法 |
| `aimnet2_wagen2024` (默认) | 3D 分子对象 | 较慢，更高准确度 | 酸 + 碱 | 您已经有 3D 结构（例如来自构象搜索） |

```python
# 快速路径：SMILES 输入，完全酸碱覆盖（可用时使用 starling 方法）
wf = rowan.submit_pka_workflow(
    initial_molecule="c1ccccc1O",       # 苯酚 SMILES；参数是 initial_molecule，不是 initial_smiles
    method="starling",   # 快速 SMILES 方法，覆盖酸碱；chemprop_nevolianis2025 仅去质子化
    name="phenol pKa",
)

result = wf.result()
print(result.strongest_acid)    # 9.81（最酸性位点的 pKa）
print(result.conjugate_bases)   # 每个可去质子化位点的 {pka, smiles, atom_index, ...} 列表
```

### 3. MacropKa

用于跨范围的 pH 依赖性质子化行为。

```python
wf = rowan.submit_macropka_workflow(
    initial_smiles="CN1CCN(CC1)C2=NC=NC3=CC=CC=C32",  # 咪唑
    min_pH=0,
    max_pH=14,
    min_charge=-2,  # 默认
    max_charge=2,   # 默认
    compute_aqueous_solubility=True,  # 默认
    name="imidazole macropKa",
)

result = wf.result()
print(result.pka_values)               # pKa 值列表
print(result.logd_by_ph)               # {pH: logD} 字典
print(result.aqueous_solubility_by_ph) # {pH: 溶解度} 字典
print(result.isoelectric_point)        # 等电点
print(result.data)
# {'pKa_values': [...], 'logD_by_pH': {...}, 'aqueous_solubility_by_pH': {...}, ...}
```

### 4. 构象搜索

用于 3D 集合生成，当集合质量很重要时。

```python
wf = rowan.submit_conformer_search_workflow(
    initial_molecule="CCOC(=O)N1CCC(CC1)Oc1ncnc2ccccc12",
    num_conformers=50,  # 可选：覆盖默认值
    name="conformer search",
)

result = wf.result()
print(result.conformer_energies)  # [0.0, 1.2, 2.5, ...]
print(result.conformer_molecules)  # 3D 分子列表
print(result.best_conformer)  # 最低能量构象
```

### 5. 互变异构体搜索

用于杂环和互变异构状态影响下游建模的系统。

```python
wf = rowan.submit_tautomer_search_workflow(
    initial_molecule="O=c1[nH]ccnc1",  # 或酮式互变异构体
    name="imidazolone tautomers",
)

result = wf.result()
print(result.best_tautomer)  # 最稳定的 SMILES 字符串
print(result.tautomers)      # 互变异构 SMILES 列表
print(result.molecules)      # 分子对象列表
```

### 6. 对接

用于蛋白质-配体对接，可选构象优化和构象生成。

```python
# 上传蛋白质一次，在多个工作流中重用
protein = rowan.upload_protein(
    name="CDK2",
    file_path="cdk2.pdb",
)

# 定义结合口袋
pocket = {
    "center": [10.5, 24.2, 31.8],
    "size": [18.0, 18.0, 18.0],
}

# 提交对接
wf = rowan.submit_docking_workflow(
    protein=protein,
    pocket=pocket,
    initial_molecule="CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1",
    do_pose_refinement=True,
    do_conformer_search=True,
    name="lead docking",
)

result = wf.result()
print(result.scores)  # 对接分数 (kcal/mol)
print(result.best_pose)  # 带 3D 坐标的 Mol 对象
print(result.data)  # 原始结果字典
```

**蛋白质准备提示：**

- PDB 文件应相当干净（除非有意，否则移除水/杂原子）
- 在对接系列中使用相同的蛋白质对象以保持一致性
- 如果您有 PDB ID，使用 `rowan.create_protein_from_pdb_id()` 代替

### 7. 类似物对接

用于将化合物系列放入共享结合环境。

```python
# 类似物系列（例如 SAR 活动）
analogues = [
    "CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1",    # 参考
    "CCNc1ncc(c(Nc2ccc(Cl)cc2)n1)-c1cccnc1",   # 氯
    "CCNc1ncc(c(Nc2ccc(OC)cc2)n1)-c1cccnc1",   # 甲氧基
    "CCNc1ncc(c(Nc2cc(C)c(F)cc2)n1)-c1cccnc1", # 甲基，氟
]

wf = rowan.submit_analogue_docking_workflow(
    analogues=analogues,
    initial_molecule=analogues[0],  # 参考配体
    protein=protein,
    pocket=pocket,
    name="SAR series docking",
)

result = wf.result()
print(result.analogue_scores)  # 每个类似物的分数列表
print(result.best_poses)  # 构象列表
```

### 8. MSA 生成

用于多序列比对（对下游共折叠有用）。

```python
wf = rowan.submit_msa_workflow(
    initial_protein_sequences=[
        "MENFQKVEKIGEGTYGVVYKARNKLTGEVVALKKIRLDTETEGVP"
    ],
    output_formats=["colabfold", "chai", "boltz"],
    name="target MSA",
)

result = wf.result()
result.download_files()  # 将比对下载到磁盘
```

### 9. 蛋白质-配体共折叠

用于无晶体结构时的基于 AI 的结合复合物预测。

```python
wf = rowan.submit_protein_cofolding_workflow(
    initial_protein_sequences=[
        "MENFQKVEKIGEGTYGVVYKARNKLTGEVVALKKIRLDTETEGVP"
    ],
    initial_smiles_list=[
        "CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1"
    ],
    name="protein-ligand cofolding",
)

result = wf.result()
print(result.predictions)  # 预测结构列表
print(result.messages)  # 模型元数据/警告

predicted_structure = result.get_predicted_structure()
predicted_structure.write("predicted_complex.pdb")
```

## 所有支持的工作流类型

所有工作流都遵循相同的提交 → 等待 → 检索模式，并支持 webhook 和项目/文件夹组织。

### 核心分子建模工作流

| 工作流 | 函数 | 何时使用 |
|----------|----------|-------------|
| 描述符 | `submit_descriptors_workflow` | 首次筛选：MW、LogP、TPSA、HBA/HBD、Lipinski 过滤器 |
| pKa | `submit_pka_workflow` | 单个可离子化基团；需要质子化热力学 |
| MacropKa | `submit_macropka_workflow` | 多离子化药物；pH 依赖性电荷/LogD/溶解度 |
| 构象搜索 | `submit_conformer_search_workflow` | 用于对接、MD 或 SAR 的 3D 集合；已知互变异构体 |
| 互变异构体搜索 | `submit_tautomer_search_workflow` | 杂环、酮-烯醇；不确定互变异构形式 |
| 溶解度 | `submit_solubility_workflow` | 水或溶剂特定溶解度预测 |
| 膜通透性 | `submit_membrane_permeability_workflow` | Caco-2、PAMPA、BBB、血浆通透性 |
| ADMET | `submit_admet_workflow` | 广泛的类药性和 ADMET 属性扫描 |

### 基于结构的设计工作流

| 工作流 | 函数 | 何时使用 |
|----------|----------|-------------|
| 对接 | `submit_docking_workflow` | 单配体，已知结合口袋 |
| 类似物对接 | `submit_analogue_docking_workflow` | SAR 系列（5–100+ 化合物）在共享口袋中 |
| 批量对接 | `submit_batch_docking_workflow` | 快速库筛选；大型化合物集 |
| 蛋白质 MD | `submit_protein_md_workflow` | 长时间尺度动力学；构象采样 |
| 构象分析 MD | `submit_pose_analysis_md_workflow` | 对接构象的 MD 优化 |
| 蛋白质共折叠 | `submit_protein_cofolding_workflow` | 无晶体结构；AI 预测的结合复合物 |
| 蛋白质结合剂设计 | `submit_protein_binder_design_workflow` | 针对蛋白质靶点的从头结合剂生成 |

### 高级计算化学

| 工作流 | 函数 | 何时使用 |
|----------|----------|-------------|
| 基本计算 | `submit_basic_calculation_workflow` | QM/ML 几何优化或单点能量 |
| 电子属性 | `submit_electronic_properties_workflow` | 偶极矩、部分电荷、HOMO-LUMO、ESP |
| BDE | `submit_bde_workflow` | 键解离能；代谢软点预测 |
| 氧化还原电位 | `submit_redox_potential_workflow` | 氧化/还原电位 |
| 自旋状态 | `submit_spin_states_workflow` | 有机金属/自由基的自旋状态能量排序 |
| 应变 | `submit_strain_workflow` | 相对于全局最小值的构象应变 |
| 扫描 | `submit_scan_workflow` | PES 扫描；扭转曲线 |
| 多阶段优化 | `submit_multistage_opt_workflow` | 跨理论水平的渐进优化 |

### 反应化学

| 工作流 | 函数 | 何时使用 |
|----------|----------|-------------|
| 双端 TS 搜索 | `submit_double_ended_ts_search_workflow` | 两个已知结构之间的过渡态 |
| IRC | `submit_irc_workflow` | 确认 TS 连通性；内在反应坐标 |

### 高级属性

| 工作流 | 函数 | 何时使用 |
|----------|----------|-------------|
| NMR | `submit_nmr_workflow` | 预测的 1H/13C 化学位移用于结构验证 |
| 离子迁移率 | `submit_ion_mobility_workflow` | 碰撞截面 (CCS) 用于 MS 方法开发 |
| 氢键强度 | `submit_hydrogen_bond_basicity_workflow` | H-键供体/受体强度用于配方/溶解度 |
| Fukui | `submit_fukui_workflow` | 亲电/亲核攻击的位点反应性指数 |
| 相互作用能分解 | `submit_interaction_energy_decomposition_workflow` | 片段级相互作用分析 |

### 结合自由能

| 工作流 | 函数 | 何时使用 |
|----------|----------|-------------|
| RBFE/FEP | `submit_relative_binding_free_energy_perturbation_workflow` | 同类系列的相对 ΔΔG |
| RBFE 图 | `submit_rbfe_graph_workflow` | 构建和优化 RBFE 扰动网络 |

### 序列和结构生物学

| 工作流 | 函数 | 何时使用 |
|----------|----------|-------------|
| MSA | `submit_msa_workflow` | 多序列比对用于共折叠（ColabFold、Chai、Boltz） |
| 溶剂依赖性构象 | `submit_solvent_dependent_conformers_workflow` | 溶剂感知构象集合 |

## 批量提交和检索

对于库或类似物系列，使用特定的工作流函数在循环中提交。通用 `rowan.batch_submit_workflow()` 和 `rowan.submit_workflow()` 函数目前从 API 返回 422 错误 — 请改用命名函数（`submit_descriptors_workflow`、`submit_pka_workflow` 等）。

### 提交批量

```python
smileses = ["CCO", "CC(=O)O", "c1ccccc1O"]
names = ["ethanol", "acetic acid", "phenol"]

workflows = [
    rowan.submit_descriptors_workflow(smi, name=name)
    for smi, name in zip(smileses, names)
]

print(f"Submitted {len(workflows)} workflows")
```

### 轮询批量状态

```python
statuses = rowan.batch_poll_status([wf.uuid for wf in workflows])
# 返回聚合计数 — 不是按 UUID：
# {'queued': 0, 'running': 1, 'complete': 2, 'failed': 0, 'total': 3, ...}

if statuses["complete"] == statuses["total"]:
    print("All workflows done")
elif statuses["failed"] > 0:
    print(f"{statuses['failed']} workflows failed")
```

### 检索和收集结果

```python
results = []
for wf in workflows:
    try:
        result = wf.result()
        results.append(result.data)
    except rowan.WorkflowError as e:
        print(f"Workflow {wf.uuid} failed: {e}")

# 可选聚合成 DataFrame
import pandas as pd
df = pd.DataFrame(results)
```

### 非阻塞/即发即查模式

对于不需要保持进程打开的长时间运行工作流，提交工作流，保存其 UUID，并在单独的进程中稍后检查。

**会话 1 — 提交并保存 UUID：**

```python
import rowan, json

rowan.api_key = "..."
smileses = ["CCO", "CC(=O)O", "c1ccccc1O"]

workflows = [
    rowan.submit_descriptors_workflow(smi, name=f"compound_{i}")
    for i, smi in enumerate(smileses)
]

# 将 UUID 保存到磁盘（或数据库）
uuids = [wf.uuid for wf in workflows]
with open("workflow_uuids.json", "w") as f:
    json.dump(uuids, f)

print("Submitted. Check back later.")
```

**会话 2 — 准备就绪时检查状态并收集结果：**

```python
import rowan, json

rowan.api_key = "..."

with open("workflow_uuids.json") as f:
    uuids = json.load(f)

results = []
for uuid in uuids:
    wf = rowan.retrieve_workflow(uuid)
    if wf.done():
        result = wf.result(wait=False)
        results.append({"uuid": uuid, "data": result.data})
    else:
        print(f"{uuid}: still running ({wf.status})")

print(f"Collected {len(results)} completed results")
```

## Webhook 和异步工作流

对于长时间运行的活动或当您不想保持进程活动时，使用 webhook 在工作流完成时通知您的后端。

### 设置 webhook

每个工作流提交函数都接受 `webhook_url` 参数：

```python
wf = rowan.submit_docking_workflow(
    protein=protein,
    pocket=pocket,
    initial_molecule="CCO",
    webhook_url="https://myserver.com/rowan_callback",
    name="docking with webhook",
)

print(f"Workflow submitted. Result will be POSTed to webhook when complete.")
```

Webhook URL 可以传递给任何特定的工作流函数（`submit_docking_workflow()`、`submit_pka_workflow()`、`submit_descriptors_workflow()` 等）。

### 使用密钥进行 webhook 认证

Rowan 支持 webhook 签名验证以确保请求是真实的。您需要：

1. **创建或检索 webhook 密钥：**

```python
import rowan

# 创建新的 webhook 密钥
secret = rowan.create_webhook_secret()
print(f"Your webhook secret: {secret.secret}")

# 或检索现有密钥
secret = rowan.get_webhook_secret()

# 轮换密钥（使旧密钥无效，创建新密钥）
new_secret = rowan.rotate_webhook_secret()
```

2. **验证传入的 webhook 请求：**

```python
import rowan
import hmac
import json

def verify_webhook(request_body: bytes, signature: str, secret: str) -> bool:
    """验证 webhook 请求的 HMAC-SHA256 签名。"""
    return rowan.verify_webhook_secret(request_body, signature, secret)
```

### Webhook 负载和签名

工作流完成时，Rowan 会向您的 webhook URL 发送 JSON 负载，带有以下头：

```text
X-Rowan-Signature: <HMAC-SHA256 signature>
```

请求体包含完整的工作流结果：

```json
{
  "workflow_uuid": "wf_12345abc",
  "workflow_type": "docking",
  "workflow_name": "lead docking",
  "status": "COMPLETED_OK",
  "created_at": "2025-04-01T12:00:00Z",
  "completed_at": "2025-04-01T12:15:30Z",
  "data": {
    "scores": [-8.2, -8.0, -7.9],
    "best_pose": {...},
    "metadata": {...}
  }
}
```

### 带签名验证的 webhook 处理器示例（FastAPI）

```python
from fastapi import FastAPI, Request, HTTPException
import rowan
import json

app = FastAPI()
_ws = rowan.get_webhook_secret() or rowan.create_webhook_secret()
webhook_secret = _ws.secret

@app.post("/rowan_callback")
async def handle_rowan_webhook(request: Request):
    # 获取请求体和签名
    body = await request.body()
    signature = request.headers.get("X-Rowan-Signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing X-Rowan-Signature header")

    # 验证签名
    if not rowan.verify_webhook_secret(body, signature, webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    # 解析和处理
    payload = json.loads(body)
    wf_uuid = payload["workflow_uuid"]
    status = payload["status"]

    if status == "COMPLETED_OK":
        print(f"Workflow {wf_uuid} succeeded!")
        result_data = payload["data"]
        # 处理结果，更新数据库，触发下一个工作流等
    elif status == "FAILED":
        print(f"Workflow {wf_uuid} failed!")
        # 处理失败

    # 快速响应以防止重试
    return {"status": "received"}
```

### Webhook 最佳实践

- **始终验证签名** 使用 `rowan.verify_webhook_secret()` 确保请求来自 Rowan
- **快速响应**（< 5 秒）；将繁重处理卸载到异步任务或后台作业
- **实现幂等性**：工作流可能重试；使用 `workflow_uuid` 优雅处理重复负载
- **记录所有事件** 用于调试和审计跟踪
- **用于长活动**：webhook 在 50+ 工作流时表现出色；对于小作业，使用 `result()` 轮询更简单
- **定期轮换密钥** 使用 `rowan.rotate_webhook_secret()` 以提高安全性
- **返回 2xx 状态** 确认接收；Rowan 可能在 5xx 错误时重试

## 蛋白质工具

### 上传蛋白质

```python
# 从本地 PDB 文件
protein = rowan.upload_protein(
    name="egfr_kinase_domain",
    file_path="egfr_kinase.pdb",
)

# 从 PDB 数据库
protein_from_pdb = rowan.create_protein_from_pdb_id(
    name="CDK2 (1M17)",
    code="1M17",
)

# 检索先前上传的蛋白质
protein = rowan.retrieve_protein("protein-uuid")

# 列出所有蛋白质
my_proteins = rowan.list_proteins()
```

### 蛋白质准备指南

- **文件格式**：PDB、mmCIF（Rowan 自动检测）
- **水分子**：Rowan 通常保留相关水；如果需要，在上传前移除大量水
- **杂原子**：辅助因子、离子和结合配体通常被保留；在上传前移除不需要的杂原子
- **多链蛋白质**：完全支持
- **分辨率**：适用于 NMR 结构、同源模型和冷冻电镜；质量对下游预测很重要
- **验证**：Rowan 验证 PDB 语法；严重畸形的文件可能被拒绝

## 端到端示例：先导优化活动

此示例演示了优化命中化合物的真实工作流程：

```python
import rowan
import pandas as pd

# 1. 创建项目和文件夹进行组织
project = rowan.create_project(name="CDK2 Hit Optimization")
rowan.set_project("CDK2 Hit Optimization")
folder = rowan.create_folder(name="round_1_tautomers_and_pka")

# 2. 加载命中化合物和类似物
hit = "CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1"  # 已知命中
analogues = [
    "CCNc1ncc(c(Nc2ccccc2)n1)-c1cccnc1",      # 移除 F
    "CCNc1ncc(c(Nc2ccc(Cl)cc2)n1)-c1cccnc1",  # Cl 代替 F
    "CCC(C)Nc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1",  # 丙基代替乙基
]

# 3. 确定最佳互变异构体（以防万一）
print("Searching tautomeric forms...")
taut_workflows = [
    rowan.submit_tautomer_search_workflow(
        smi, name=f"analog_{i}", folder=folder,
    )
    for i, smi in enumerate(analogues)
]

best_tautomers = []
for wf in taut_workflows:
    result = wf.result()
    best_tautomers.append(result.best_tautomer)

# 4. 预测所有类似物的 pKa 和基本特性
print("Predicting pKa and properties...")
pka_workflows = [
    rowan.submit_pka_workflow(
        smi, method="chemprop_nevolianis2025", name=f"pka_{i}", folder=folder,
    )
    for i, smi in enumerate(best_tautomers)
]

descriptor_workflows = [
    rowan.submit_descriptors_workflow(smi, name=f"desc_{i}", folder=folder)
    for i, smi in enumerate(best_tautomers)
]

# 5. 收集结果
pka_results = []
for wf in pka_workflows:
    try:
        result = wf.result()
        pka_results.append({
            "compound": wf.name,
            "pka": result.strongest_acid,  # 最强酸性位点的 pKa
            "uuid": wf.uuid,
        })
    except rowan.WorkflowError as e:
        print(f"pKa prediction failed for {wf.name}: {e}")

descriptor_results = []
for wf in descriptor_workflows:
    try:
        result = wf.result()
        desc = result.descriptors
        descriptor_results.append({
            "compound": wf.name,
            "mw": desc.get("MW"),
            "logp": desc.get("SLogP"),
            "hba": desc.get("nHBAcc"),
            "hbd": desc.get("nHBDon"),
            "uuid": wf.uuid,
        })
    except rowan.WorkflowError as e:
        print(f"Descriptor calculation failed for {wf.name}: {e}")

# 6. 合并和总结
df_pka = pd.DataFrame(pka_results)
df_desc = pd.DataFrame(descriptor_results)
df = df_pka.merge(df_desc, on="compound", how="outer")

print("\n=== Preliminary SAR ===")
print(df.to_string())

# 7. 选择有前途的化合物进行对接
# 化合物名称为 "pka_0"、"pka_1" 等 — 提取索引以查找 SMILES
top_idx = int(df.loc[df["pka"].idxmin(), "compound"].split("_")[1])
top_smiles = best_tautomers[top_idx]

print(f"\nProceeding with docking: {top_smiles}")

# 8. 对接活动
protein = rowan.create_protein_from_pdb_id(name="CDK2_1CKP", code="1CKP")
pocket = {"center": [10.5, 24.2, 31.8], "size": [18.0, 18.0, 18.0]}

docking_wf = rowan.submit_docking_workflow(
    protein=protein,
    pocket=pocket,
    initial_molecule=top_smiles,
    do_pose_refinement=True,
    name=f"docking_{top_compound}",
)

dock_result = docking_wf.result()
print(f"\nDocking score: {dock_result.scores[0]:.2f} kcal/mol")
print(f"Best pose saved to: best_pose.pdb")
dock_result.best_pose.write("best_pose.pdb")
```

## 错误处理和故障排除

### 常见错误和解决方案

```python
import rowan

# 错误 1: 无效的 SMILES
try:
    wf = rowan.submit_descriptors_workflow("CCCC(CC", name="bad smiles")  # 无效
except rowan.ValidationError as e:
    print(f"Invalid SMILES: {e}")
    # 解决方案: 在提交前使用 RDKit 验证
    from rdkit import Chem
    smi = Chem.MolToSmiles(Chem.MolFromSmiles(smi))

# 错误 2: API 密钥未设置
try:
    wf = rowan.submit_descriptors_workflow("CCO")
except rowan.AuthenticationError:
    print("API key not found. Set ROWAN_API_KEY env var or call rowan.api_key = '...'")

# 错误 3: 信用不足
try:
    wf = rowan.submit_protein_cofolding_workflow(...)
except rowan.InsufficientCreditsError as e:
    print(f"Not enough credits: {e}. Purchase more or reduce job size.")

# 错误 4: 工作流失败（分子错误等）
try:
    wf = rowan.submit_docking_workflow(...)
    result = wf.result()
except rowan.WorkflowError as e:
    print(f"Workflow failed: {e}")
    # 检查 wf.status 获取详情
    print(f"Status: {wf.status}")

# 错误 5: 工作流尚未完成 — 手动轮询
result = wf.result(wait=True, poll_interval=5)  # 等待并每 5s 轮询一次
# 或无阻塞检查状态：
if not wf.done():
    print("Workflow still running. Call wf.result() again later.")
```

### 调试提示

- **检查工作流状态**：`wf.status`，检查 `wf.done()`，或调用 `wf.get_status()`
- **检查原始结果**：`result.data` 而不是便利属性
- **重新运行失败的工作流**：保存 UUID 并使用 `rowan.retrieve_workflow(uuid)` 重试
- **预先验证分子**：在批量提交前使用 RDKit 或 Chemaxon

## 推荐使用模式

- **优先使用 Rowan 原生工作流**，而不是在存在时使用低级组装
- **对任何非平凡活动（>5 个工作流）使用项目和文件夹**
- **使用 `result()` 阻塞直到完成**（默认：`wait=True, poll_interval=5`）
- **首先使用类型化结果属性**，对未映射字段回退到 `.data`
- **对化合物库或类似物系列使用批量提交**
- **链接工作流** 用于多步化学活动：
  - `pKa → macropKa → permeability`（ADME 评估）
  - `互变异构体搜索 → 对接 → 构象分析 MD`（构象优化）
  - `MSA 生成 → 蛋白质-配体共折叠`（AI 结构预测）
- **对长活动（>50 个工作流）或异步管道使用 webhook**
- **对大型构象/对接搜索使用流式处理** 以获得交互式反馈

## 总结

当您的工作流需要用于分子设计任务的云执行时，尤其是当您希望在小分子建模、蛋白质、对接、ADME 预测和 ML 结构生成之间拥有一个统一的 API 和一致的结果处理时，使用 Rowan。

Rowan 是一个分子设计工作流平台，而不仅仅是远程化学引擎。它处理基础设施扩展、结果持久化和多步管道编排，让您可以专注于科学。