---
name: datamol
description: RDKit 的 Pythonic 包装器，具有简化的界面和合理的默认值。首选用于标准药物发现，包括 SMILES 解析、标准化、描述符、指纹、聚类、3D 构象、并行处理。返回原生 rdkit.Chem.Mol 对象。对于高级控制或自定义参数，直接使用 rdkit。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Datamol 化学信息学技能

## 概述

Datamol 是一个 Python 库，为 RDKit 分子信息学提供了轻量级、Pythonic 的抽象层。通过合理的默认值、高效的并行化和现代 I/O 功能简化复杂的分子操作。所有分子对象都是原生的 `rdkit.Chem.Mol` 实例，确保与 RDKit 生态系统完全兼容。

**关键能力**：
- 分子格式转换（SMILES、SELFIES、InChI）
- 结构标准化和清理
- 分子描述符和指纹
- 3D 构象生成和分析
- 聚类和多样性选择
- 骨架和片段分析
- 化学反应应用
- 可视化和对齐
- 带并行化的批处理
- 通过 fsspec 支持云存储

## 安装和设置

指导用户安装 datamol：

```bash
uv pip install datamol
```

**导入约定**：
```python
import datamol as dm
```

## 核心工作流

### 1. 基本分子处理

**从 SMILES 创建分子**：
```python
import datamol as dm

# 单个分子
mol = dm.to_mol("CCO")  # 乙醇

# 从 SMILES 列表
smiles_list = ["CCO", "c1ccccc1", "CC(=O)O"]
mols = [dm.to_mol(smi) for smi in smiles_list]

# 错误处理
mol = dm.to_mol("invalid_smiles")  # 返回 None
if mol is None:
    print("解析 SMILES 失败")
```

**将分子转换为 SMILES**：
```python
# 规范 SMILES
smiles = dm.to_smiles(mol)

# 异构 SMILES（包括立体化学）
smiles = dm.to_smiles(mol, isomeric=True)

# 其他格式
inchi = dm.to_inchi(mol)
inchikey = dm.to_inchikey(mol)
selfies = dm.to_selfies(mol)
```

**标准化和清理**（对于用户提供的分子始终推荐）：
```python
# 清理分子
mol = dm.sanitize_mol(mol)

# 完整标准化（推荐用于数据集）
mol = dm.standardize_mol(
    mol,
    disconnect_metals=True,
    normalize=True,
    reionize=True
)

# 对于 SMILES 字符串直接
clean_smiles = dm.standardize_smiles(smiles)
```

### 2. 读取和写入分子文件

有关综合 I/O 文档，请参阅 `references/io_module.md`。

**读取文件**：
```python
# SDF 文件（化学中最常见）
df = dm.read_sdf("compounds.sdf", mol_column='mol')

# SMILES 文件
df = dm.read_smi("molecules.smi", smiles_column='smiles', mol_column='mol')

# 带 SMILES 列的 CSV
df = dm.read_csv("data.csv", smiles_column="SMILES", mol_column="mol")

# Excel 文件
df = dm.read_excel("compounds.xlsx", sheet_name=0, mol_column="mol")

# 通用读取器（自动检测格式）
df = dm.open_df("file.sdf")  # 适用于 .sdf、.csv、.xlsx、.parquet、.json
```

**写入文件**：
```python
# 保存为 SDF
dm.to_sdf(mols, "output.sdf")
# 或从 DataFrame
dm.to_sdf(df, "output.sdf", mol_column="mol")

# 保存为 SMILES 文件
dm.to_smi(mols, "output.smi")

# 带渲染分子图像的 Excel
dm.to_xlsx(df, "output.xlsx", mol_columns=["mol"])
```

**远程文件支持**（S3、GCS、HTTP）：
```python
# 从云存储读取
df = dm.read_sdf("s3://bucket/compounds.sdf")
df = dm.read_csv("https://example.com/data.csv")

# 写入云存储
dm.to_sdf(mols, "s3://bucket/output.sdf")
```

### 3. 分子描述符和属性

有关详细描述符文档，请参阅 `references/descriptors_viz.md`。

**计算单个分子的描述符**：
```python
# 获取标准描述符集
descriptors = dm.descriptors.compute_many_descriptors(mol)
# 返回：{'mw': 46.07, 'logp': -0.03, 'hbd': 1, 'hba': 1,
#           'tpsa': 20.23, 'n_aromatic_atoms': 0, ...}
```

**批处理描述符计算**（推荐用于数据集）：
```python
# 并行计算所有分子
desc_df = dm.descriptors.batch_compute_many_descriptors(
    mols,
    n_jobs=-1,      # 使用所有 CPU 核心
    progress=True   # 显示进度条
)
```

**特定描述符**：
```python
# 芳香性
n_aromatic = dm.descriptors.n_aromatic_atoms(mol)
aromatic_ratio = dm.descriptors.n_aromatic_atoms_proportion(mol)

# 立体化学
n_stereo = dm.descriptors.n_stereo_centers(mol)
n_unspec = dm.descriptors.n_stereo_centers_unspecified(mol)

# 柔性
n_rigid = dm.descriptors.n_rigid_bonds(mol)
```

**药物相似性过滤（Lipinski 五法则）**：
```python
# 过滤化合物
def is_druglike(mol):
    desc = dm.descriptors.compute_many_descriptors(mol)
    return (
        desc['mw'] <= 500 and
        desc['logp'] <= 5 and
        desc['hbd'] <= 5 and
        desc['hba'] <= 10
    )

druglike_mols = [mol for mol in mols if is_druglike(mol)]
```

### 4. 分子指纹和相似性

**生成指纹**：
```python
# ECFP（扩展连接指纹，默认）
fp = dm.to_fp(mol, fp_type='ecfp', radius=2, n_bits=2048)

# 其他指纹类型
fp_maccs = dm.to_fp(mol, fp_type='maccs')
fp_topological = dm.to_fp(mol, fp_type='topological')
fp_atompair = dm.to_fp(mol, fp_type='atompair')
```

**相似性计算**：
```python
# 集合内的成对距离
distance_matrix = dm.pdist(mols, n_jobs=-1)

# 两个集之间的距离
distances = dm.cdist(query_mols, library_mols, n_jobs=-1)

# 查找最相似的分子
from scipy.spatial.distance import squareform
dist_matrix = squareform(dm.pdist(mols))
# 较低距离 = 较高相似性（Tanimoto 距离 = 1 - Tanimoto 相似性）
```

### 5. 聚类和多样性选择

有关聚类详细信息，请参阅 `references/core_api.md`。

**Butina 聚类**：
```python
# 按结构相似性聚类分子
clusters = dm.cluster_mols(
    mols,
    cutoff=0.2,    # Tanimoto 距离阈值（0=相同，1=完全不同）
    n_jobs=-1      # 并行处理
)

# 每个聚类是分子索引的列表
for i, cluster in enumerate(clusters):
    print(f"聚类 {i}: {len(cluster)} 个分子")
    cluster_mols = [mols[idx] for idx in cluster]
```

**重要**：Butina 聚类构建完整的距离矩阵 - 适用于约 1000 个分子，不适用于 10000+ 个。

**多样性选择**：
```python
# 选择多样性子集
diverse_mols = dm.pick_diverse(
    mols,
    npick=100  # 选择 100 个多样性分子
)

# 选择聚类中心
centroids = dm.pick_centroids(
    mols,
    npick=50   # 选择 50 个代表性分子
)
```

### 6. 骨架分析

有关完整骨架文档，请参阅 `references/fragments_scaffolds.md`。

**提取 Murcko 骨架**：
```python
# 获取 Bemis-Murcko 骨架（核心结构）
scaffold = dm.to_scaffold_murcko(mol)
scaffold_smiles = dm.to_smiles(scaffold)
```

**基于骨架的分析**：
```python
# 按骨架分组化合物
from collections import Counter

scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# 统计骨架频率
scaffold_counts = Counter(scaffold_smiles)
most_common = scaffold_counts.most_common(10)

# 创建骨架到分子的映射
scaffold_groups = {}
for mol, scaf_smi in zip(mols, scaffold_smiles):
    if scaf_smi not in scaffold_groups:
        scaffold_groups[scaf_smi] = []
    scaffold_groups[scaf_smi].append(mol)
```

**基于骨架的训练/测试拆分**（用于机器学习）：
```python
# 确保训练集和测试集具有不同的骨架
scaffold_to_mols = {}
for mol, scaf in zip(mols, scaffold_smiles):
    if scaf not in scaffold_to_mols:
        scaffold_to_mols[scaf] = []
    scaffold_to_mols[scaf].append(mol)

# 将骨架拆分为训练/测试
import random
scaffolds = list(scaffold_to_mols.keys())
random.shuffle(scaffolds)
split_idx = int(0.8 * len(scaffolds))
train_scaffolds = scaffolds[:split_idx]
test_scaffolds = scaffolds[split_idx:]

# 获取每个拆分的分子
train_mols = [mol for scaf in train_scaffolds for mol in scaffold_to_mols[scaf]]
test_mols = [mol for scaf in test_scaffolds for mol in scaffold_to_mols[scaf]]
```

### 7. 分子片段化

有关片段化详细信息，请参阅 `references/fragments_scaffolds.md`。

**BRICS 片段化**（16 种键类型）：
```python
# 片段化分子
fragments = dm.fragment.brics(mol)
# 返回：带有连接点的片段 SMILES 集，如 '[1*]CCN'
```

**RECAP 片段化**（11 种键类型）：
```python
fragments = dm.fragment.recap(mol)
```

**片段分析**：
```python
# 查找化合物库中的常见片段
from collections import Counter

all_fragments = []
for mol in mols:
    frags = dm.fragment.brics(mol)
    all_fragments.extend(frags)

fragment_counts = Counter(all_fragments)
common_frags = fragment_counts.most_common(20)

# 基于片段的评分
def fragment_score(mol, reference_fragments):
    mol_frags = dm.fragment.brics(mol)
    overlap = mol_frags.intersection(reference_fragments)
    return len(overlap) / len(mol_frags) if mol_frags else 0
```

### 8. 3D 构象生成

有关详细构象文档，请参阅 `references/conformers_module.md`。

**生成构象**：
```python
# 生成 3D 构象
mol_3d = dm.conformers.generate(
    mol,
    n_confs=50,           # 生成数量（如果为 None 则自动）
    rms_cutoff=0.5,       # 过滤相似构象（埃）
    minimize_energy=True,  # 使用 UFF 力场最小化
    method='ETKDGv3'      # 嵌入方法（推荐）
)

# 访问构象
n_conformers = mol_3d.GetNumConformers()
conf = mol_3d.GetConformer(0)  # 获取第一个构象
positions = conf.GetPositions()  # 原子坐标的 Nx3 数组
```

**构象聚类**：
```python
# 按 RMSD 聚类构象
clusters = dm.conformers.cluster(
    mol_3d,
    rms_cutoff=1.0,
    centroids=False
)

# 获取代表性构象
centroids = dm.conformers.return_centroids(mol_3d, clusters)
```

**SASA 计算**：
```python
# 计算溶剂可及表面积
sasa_values = dm.conformers.sasa(mol_3d, n_jobs=-1)

# 从构象属性访问 SASA
conf = mol_3d.GetConformer(0)
sasa = conf.GetDoubleProp('rdkit_free_sasa')
```

### 9. 可视化

有关可视化文档，请参阅 `references/descriptors_viz.md`。

**基本分子网格**：
```python
# 可视化分子
dm.viz.to_image(
    mols[:20],
    legends=[dm.to_smiles(m) for m in mols[:20]],
    n_cols=5,
    mol_size=(300, 300)
)

# 保存到文件
dm.viz.to_image(mols, outfile="molecules.png")

# 用于出版的 SVG
dm.viz.to_image(mols, outfile="molecules.svg", use_svg=True)
```

**对齐可视化**（用于 SAR 分析）：
```python
# 按公共子结构对齐分子
dm.viz.to_image(
    similar_mols,
    align=True,  # 启用 MCS 对齐
    legends=activity_labels,
    n_cols=4
)
```

**高亮子结构**：
```python
# 高亮特定原子和键
dm.viz.to_image(
    mol,
    highlight_atom=[0, 1, 2, 3],  # 原子索引
    highlight_bond=[0, 1, 2]      # 键索引
)
```

**构象可视化**：
```python
# 显示多个构象
dm.viz.conformers(
    mol_3d,
    n_confs=10,
    align_conf=True,
    n_cols=3
)
```

### 10. 化学反应

有关反应文档，请参阅 `references/reactions_data.md`。

**应用反应**：
```python
from rdkit.Chem import rdChemReactions

# 从 SMARTS 定义反应
rxn_smarts = '[C:1](=[O:2])[OH:3]>>[C:1](=[O:2])[Cl:3]'
rxn = rdChemReactions.ReactionFromSmarts(rxn_smarts)

# 应用于分子
reactant = dm.to_mol("CC(=O)O")  # 乙酸
product = dm.reactions.apply_reaction(
    rxn,
    (reactant,),
    sanitize=True
)

# 转换为 SMILES
product_smiles = dm.to_smiles(product)
```

**批处理反应应用**：
```python
# 将反应应用于库
products = []
for mol in reactant_mols:
    try:
        prod = dm.reactions.apply_reaction(rxn, (mol,))
        if prod is not None:
            products.append(prod)
    except Exception as e:
        print(f"反应失败：{e}")
```

## 并行化

Datamol 为许多操作包含内置并行化。使用 `n_jobs` 参数：
- `n_jobs=1`：顺序（无并行化）
- `n_jobs=-1`：使用所有可用的 CPU 核心
- `n_jobs=4`：使用 4 个核心

**支持并行化的函数**：
- `dm.read_sdf(..., n_jobs=-1)`
- `dm.descriptors.batch_compute_many_descriptors(..., n_jobs=-1)`
- `dm.cluster_mols(..., n_jobs=-1)`
- `dm.pdist(..., n_jobs=-1)`
- `dm.conformers.sasa(..., n_jobs=-1)`

**进度条**：许多批处理操作支持 `progress=True` 参数。

## 常见工作流和模式

### 完整管道路径：数据加载 → 过滤 → 分析

```python
import datamol as dm
import pandas as pd

# 1. 加载分子
df = dm.read_sdf("compounds.sdf")

# 2. 标准化
df['mol'] = df['mol'].apply(lambda m: dm.standardize_mol(m) if m else None)
df = df[df['mol'].notna()]  # 移除失败的分子

# 3. 计算描述符
desc_df = dm.descriptors.batch_compute_many_descriptors(
    df['mol'].tolist(),
    n_jobs=-1,
    progress=True
)

# 4. 按药物相似性过滤
druglike = (
    (desc_df['mw'] <= 500) &
    (desc_df['logp'] <= 5) &
    (desc_df['hbd'] <= 5) &
    (desc_df['hba'] <= 10)
)
filtered_df = df[druglike]

# 5. 聚类并选择多样性子集
diverse_mols = dm.pick_diverse(
    filtered_df['mol'].tolist(),
    npick=100
)

# 6. 可视化结果
dm.viz.to_image(
    diverse_mols,
    legends=[dm.to_smiles(m) for m in diverse_mols],
    outfile="diverse_compounds.png",
    n_cols=10
)
```

### 结构-活性关系（SAR）分析

```python
# 按骨架分组
scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# 创建带有活性的 DataFrame
sar_df = pd.DataFrame({
    'mol': mols,
    'scaffold': scaffold_smiles,
    'activity': activities  # 用户提供的活性数据
})

# 分析每个骨架系列
for scaffold, group in sar_df.groupby('scaffold'):
    if len(group) >= 3:  # 需要多个示例
        print(f"\n骨架：{scaffold}")
        print(f"数量：{len(group)}")
        print(f"活性范围：{group['activity'].min():.2f} - {group['activity'].max():.2f}")

        # 用活性作为图例进行可视化
        dm.viz.to_image(
            group['mol'].tolist(),
            legends=[f"活性：{act:.2f}" for act in group['activity']],
            align=True  # 按公共子结构对齐
        )
```

### 虚拟筛选管道路径

```python
# 1. 为查询和库生成指纹
query_fps = [dm.to_fp(mol) for mol in query_actives]
library_fps = [dm.to_fp(mol) for mol in library_mols]

# 2. 计算相似性
from scipy.spatial.distance import cdist
import numpy as np

distances = dm.cdist(query_actives, library_mols, n_jobs=-1)

# 3. 查找最接近的匹配（到任何查询的最小距离）
min_distances = distances.min(axis=0)
similarities = 1 - min_distances  # 将距离转换为相似性

# 4. 排名并选择前 N 个命中
top_indices = np.argsort(similarities)[::-1][:100]  # 前 100 个
top_hits = [library_mols[i] for i in top_indices]
top_scores = [similarities[i] for i in top_indices]

# 5. 可视化命中
dm.viz.to_image(
    top_hits[:20],
    legends=[f"相似性：{score:.3f}" for score in top_scores[:20]],
    outfile="screening_hits.png"
)
```

## 参考文档

有关详细的 API 文档，请查阅这些参考文件：

- **`references/core_api.md`**：核心命名空间函数（转换、标准化、指纹、聚类）
- **`references/io_module.md`**：文件 I/O 操作（读/写 SDF、CSV、Excel、远程文件）
- **`references/conformers_module.md`**：3D 构象生成、聚类、SASA 计算
- **`references/descriptors_viz.md`**：分子描述符和可视化函数
- **`references/fragments_scaffolds.md`**：骨架提取、BRICS/RECAP 片段化
- **`references/reactions_data.md`**：化学反应和玩具数据集

## 最佳实践

1. **始终标准化来自外部来源的分子**：
   ```python
   mol = dm.standardize_mol(mol, disconnect_metals=True, normalize=True, reionize=True)
   ```

2. **在分子解析后检查 None 值**：
   ```python
   mol = dm.to_mol(smiles)
   if mol is None:
       # 处理无效 SMILES
   ```

3. **对大型数据集使用并行处理**：
   ```python
   result = dm.operation(..., n_jobs=-1, progress=True)
   ```

4. **利用 fsspec 进行云存储**：
   ```python
   df = dm.read_sdf("s3://bucket/compounds.sdf")
   ```

5. **使用适当的指纹进行相似性**：
   - ECFP (Morgan)：通用目的，结构相似性
   - MACCS：快速，较小的特征空间
   - 原子对：考虑原子对和距离

6. **考虑规模限制**：
   - Butina 聚类：约 1,000 个分子（完整距离矩阵）
   - 对于更大的数据集：使用多样性选择或分层方法

7. **机器学习的骨架拆分**：通过骨架确保适当的训练/测试分离

8. **可视化 SAR 系列时对齐分子**

## 错误处理

```python
# 安全的分子创建
def safe_to_mol(smiles):
    try:
        mol = dm.to_mol(smiles)
        if mol is not None:
            mol = dm.standardize_mol(mol)
        return mol
    except Exception as e:
        print(f"处理 {smiles} 失败：{e}")
        return None

# 安全的批处理
valid_mols = []
for smiles in smiles_list:
    mol = safe_to_mol(smiles)
    if mol is not None:
        valid_mols.append(mol)
```

## 与机器学习集成

```python
# 特征生成
X = np.array([dm.to_fp(mol) for mol in mols])

# 或描述符
desc_df = dm.descriptors.batch_compute_many_descriptors(mols, n_jobs=-1)
X = desc_df.values

# 训练模型
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X, y_target)

# 预测
predictions = model.predict(X_test)
```

## 故障排除

**问题**：分子解析失败
- **解决方案**：首先使用 `dm.standardize_smiles()` 或尝试 `dm.fix_mol()`

**问题**：聚类时出现内存错误
- **解决方案**：对于大型集使用 `dm.pick_diverse()` 而不是完整聚类

**问题**：构象生成缓慢
- **解决方案**：减少 `n_confs` 或增加 `rms_cutoff` 以生成更少的构象

**问题**：远程文件访问失败
- **解决方案**：确保安装了 fsspec 和适当的云提供商库（s3fs、gcsfs 等）

## 其他资源

- **Datamol 文档**：https://docs.datamol.io/
- **RDKit 文档**：https://www.rdkit.org/docs/
- **GitHub 仓库**：https://github.com/datamol-io/datamol
