---
name: pytdc
description: Therapeutics Data Commons。AI-ready药物发现数据集（ADME、毒性、DTI）、基准测试、支架分割、分子预言机，用于治疗ML和药理学预测。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyTDC (Therapeutics Data Commons)

## 概述

PyTDC是一个开放科学平台，提供用于药物发现和开发的AI-ready数据集和基准测试。访问覆盖整个治疗管线的精选数据集，具有标准化的评估指标和有意义的数据分割，分为三类：单实例预测（分子/蛋白质特性）、多实例预测（药物-靶点相互作用、DDI）和生成（分子生成、逆向合成）。

## 使用场景

当您需要以下操作时使用此技能：
- 处理药物发现或治疗ML数据集
- 在标准化制药任务上基准测试机器学习模型
- 预测分子特性（ADME、毒性、生物活性）
- 预测药物-靶点或药物-药物相互作用
- 生成具有所需特性的新型分子
- 访问具有适当训练/测试分割的精选数据集（支架、冷分割）
- 使用分子预言机进行特性优化

## 安装与设置

使用pip安装PyTDC：

```bash
uv pip install PyTDC
```

升级到最新版本：

```bash
uv pip install PyTDC --upgrade
```

核心依赖（自动安装）：
- numpy, pandas, tqdm, seaborn, scikit_learn, fuzzywuzzy

根据需要，额外的包会自动安装以支持特定功能。

## 快速开始

访问任何TDC数据集的基本模式如下：

```python
from tdc.<problem> import <Task>
data = <Task>(name='<Dataset>')
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])
df = data.get_data(format='df')
```

其中：
- `<problem>`: `single_pred`、`multi_pred`或`generation`之一
- `<Task>`: 特定任务类别（例如，ADME、DTI、MolGen）
- `<Dataset>`: 该任务内的数据集名称

**示例 - 加载ADME数据：**

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold')
# 返回包含'train'、'valid'、'test' DataFrame的字典
```

## 单实例预测任务

单实例预测涉及预测单个生物医学实体（分子、蛋白质等）的特性。

### 可用任务类别

#### 1. ADME（吸收、分布、代谢、排泄）

预测药物分子的药代动力学特性。

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')  # 肠通透性
# 其他数据集：HIA_Hou, Bioavailability_Ma, Lipophilicity_AstraZeneca等
```

**常见ADME数据集：**
- Caco2 - 肠通透性
- HIA - 人体肠吸收
- Bioavailability - 口服生物利用度
- Lipophilicity - 辛醇-水分配系数
- Solubility - 水溶性
- BBB - 血脑屏障穿透
- CYP - 细胞色素P450代谢

#### 2. 毒性（Tox）

预测化合物的毒性和不良反应。

```python
from tdc.single_pred import Tox
data = Tox(name='hERG')  # 心脏毒性
# 其他数据集：AMES, DILI, Carcinogens_Lagunin等
```

**常见毒性数据集：**
- hERG - 心脏毒性
- AMES - 致突变性
- DILI - 药物诱导的肝损伤
- Carcinogens - 致癌性
- ClinTox - 临床试验毒性

#### 3. HTS（高通量筛选）

来自筛选数据的生物活性预测。

```python
from tdc.single_pred import HTS
data = HTS(name='SARSCoV2_Vitro_Touret')
```

#### 4. QM（量子力学）

分子的量子力学特性。

```python
from tdc.single_pred import QM
data = QM(name='QM7')
```

#### 5. 其他单预测任务

- **Yields**：化学反应产率预测
- **Epitope**：生物制品的表位预测
- **Develop**：开发阶段预测
- **CRISPROutcome**：基因编辑结果预测

### 数据格式

单预测数据集通常返回包含以下列的DataFrame：
- `Drug_ID`或`Compound_ID`：唯一标识符
- `Drug`或`X`：SMILES字符串或分子表示
- `Y`：目标标签（连续或二元）

## 多实例预测任务

多实例预测涉及预测多个生物医学实体之间相互作用的特性。

### 可用任务类别

#### 1. DTI（药物-靶点相互作用）

预测药物和蛋白质靶点之间的结合亲和力。

```python
from tdc.multi_pred import DTI
data = DTI(name='BindingDB_Kd')
split = data.get_split()
```

**可用数据集：**
- BindingDB_Kd - 解离常数（52,284对）
- BindingDB_IC50 - 半最大抑制浓度（991,486对）
- BindingDB_Ki - 抑制常数（375,032对）
- DAVIS, KIBA - 激酶结合数据集

**数据格式：** Drug_ID, Target_ID, Drug (SMILES), Target (序列), Y (结合亲和力)

#### 2. DDI（药物-药物相互作用）

预测药物对之间的相互作用。

```python
from tdc.multi_pred import DDI
data = DDI(name='DrugBank')
split = data.get_split()
```

多分类任务，预测相互作用类型。数据集包含191,808个DDI对，涉及1,706种药物。

#### 3. PPI（蛋白质-蛋白质相互作用）

预测蛋白质-蛋白质相互作用。

```python
from tdc.multi_pred import PPI
data = PPI(name='HuRI')
```

#### 4. 其他多预测任务

- **GDA**：基因-疾病关联
- **DrugRes**：药物耐药性预测
- **DrugSyn**：药物协同作用预测
- **PeptideMHC**：肽-MHC结合
- **AntibodyAff**：抗体亲和力预测
- **MTI**：miRNA-靶点相互作用
- **Catalyst**：催化剂预测
- **TrialOutcome**：临床试验结果预测

## 生成任务

生成任务涉及创建具有所需特性的新型生物医学实体。

### 1. 分子生成（MolGen）

生成具有理想化学特性的多样化、新型分子。

```python
from tdc.generation import MolGen
data = MolGen(name='ChEMBL_V29')
split = data.get_split()
```

与预言机一起使用以优化特定特性：

```python
from tdc import Oracle
oracle = Oracle(name='GSK3B')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')  # 评估SMILES
```

有关所有可用预言机函数，请参见`references/oracles.md`。

### 2. 逆向合成（RetroSyn）

预测合成目标分子所需的反应物。

```python
from tdc.generation import RetroSyn
data = RetroSyn(name='USPTO')
split = data.get_split()
```

数据集包含来自USPTO数据库的1,939,253个反应。

### 3. 配对分子生成

生成分子对（例如，前药-药物对）。

```python
from tdc.generation import PairMolGen
data = PairMolGen(name='Prodrug')
```

有关预言机文档和分子生成工作流的详细信息，请参考`references/oracles.md`和`scripts/molecular_generation.py`。

## 基准测试组

基准测试组提供相关数据集的精选集合，用于系统模型评估。

### ADMET基准测试组

```python
from tdc.benchmark_group import admet_group
group = admet_group(path='data/')

# 获取基准测试数据集
benchmark = group.get('Caco2_Wang')
predictions = {}

for seed in [1, 2, 3, 4, 5]:
    train, valid = benchmark['train'], benchmark['valid']
    # 在此训练模型
    predictions[seed] = model.predict(benchmark['test'])

# 用所需的5个种子评估
results = group.evaluate(predictions)
```

**ADMET组包括22个数据集**，涵盖吸收、分布、代谢、排泄和毒性。

### 其他基准测试组

可用的基准测试组包括以下集合：
- ADMET特性
- 药物-靶点相互作用
- 药物组合预测
- 更多专门的治疗任务

有关基准测试评估工作流，请参见`scripts/benchmark_evaluation.py`。

## 数据函数

TDC提供组织为四类的综合数据处理工具。

### 1. 数据集分割

使用各种策略检索训练/验证/测试分区：

```python
# 支架分割（大多数任务的默认值）
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])

# 随机分割
split = data.get_split(method='random', seed=42, frac=[0.8, 0.1, 0.1])

# 冷分割（用于DTI/DDI任务）
split = data.get_split(method='cold_drug', seed=1)  # 测试中未见药物
split = data.get_split(method='cold_target', seed=1)  # 测试中未见靶点
```

**可用分割策略：**
- `random`：随机洗牌
- `scaffold`：基于支架（用于化学多样性）
- `cold_drug`, `cold_target`, `cold_drug_target`：用于DTI任务
- `temporal`：时间数据集的基于时间的分割

### 2. 模型评估

使用标准化指标进行评估：

```python
from tdc import Evaluator

# 对于二元分类
evaluator = Evaluator(name='ROC-AUC')
score = evaluator(y_true, y_pred)

# 对于回归
evaluator = Evaluator(name='RMSE')
score = evaluator(y_true, y_pred)
```

**可用指标：** ROC-AUC, PR-AUC, F1, 准确率, RMSE, MAE, R2, Spearman, Pearson等。

### 3. 数据处理

TDC提供11个关键处理工具：

```python
from tdc.chem_utils import MolConvert

# 分子格式转换
converter = MolConvert(src='SMILES', dst='PyG')
pyg_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

**处理工具包括：**
- 分子格式转换（SMILES、SELFIES、PyG、DGL、ECFP等）
- 分子过滤器（PAINS、类药性质）
- 标签二值化和单位转换
- 数据平衡（过/欠采样）
- 对数据的负采样
- 图转换
- 实体检索（CID到SMILES、UniProt到序列）

有关综合工具文档，请参见`references/utilities.md`。

### 4. 分子生成预言机

TDC提供17+个用于分子优化的预言机函数：

```python
from tdc import Oracle

# 单个预言机
oracle = Oracle(name='DRD2')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# 多个预言机
oracle = Oracle(name='JNK3')
scores = oracle(['SMILES1', 'SMILES2', 'SMILES3'])
```

有关完整的预言机文档，请参见`references/oracles.md`。

## 高级功能

### 检索可用数据集

```python
from tdc.utils import retrieve_dataset_names

# 获取所有ADME数据集
adme_datasets = retrieve_dataset_names('ADME')

# 获取所有DTI数据集
dti_datasets = retrieve_dataset_names('DTI')
```

### 标签转换

```python
# 获取标签映射
label_map = data.get_label_map(name='DrugBank')

# 转换标签
from tdc.chem_utils import label_transform
transformed = label_transform(y, from_unit='nM', to_unit='p')
```

### 数据库查询

```python
from tdc.utils import cid2smiles, uniprot2seq

# 将PubChem CID转换为SMILES
smiles = cid2smiles(2244)

# 将UniProt ID转换为氨基酸序列
sequence = uniprot2seq('P12345')
```

## 常见工作流

### 工作流1：训练单预测模型

有关完整示例，请参见`scripts/load_and_split_data.py`：

```python
from tdc.single_pred import ADME
from tdc import Evaluator

# 加载数据
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold', seed=42)

train, valid, test = split['train'], split['valid'], split['test']

# 训练模型（用户实现）
# model.fit(train['Drug'], train['Y'])

# 评估
evaluator = Evaluator(name='MAE')
# score = evaluator(test['Y'], predictions)
```

### 工作流2：基准测试评估

有关带有多个种子和适当评估协议的完整示例，请参见`scripts/benchmark_evaluation.py`。

### 工作流3：使用预言机的分子生成

有关使用预言机函数进行目标导向生成的示例，请参见`scripts/molecular_generation.py`。

## 资源

此技能包含用于常见TDC工作流的捆绑资源：

### scripts/

- `load_and_split_data.py`：使用各种策略加载和分割TDC数据集的模板
- `benchmark_evaluation.py`：使用适当的5种子协议运行基准测试组评估的模板
- `molecular_generation.py`：使用预言机函数进行分子生成的模板

### references/

- `datasets.md`：按任务类型组织的所有可用数据集的综合目录
- `oracles.md`：所有17+个分子生成预言机的完整文档
- `utilities.md`：数据处理、分割和评估工具的详细指南

## 其他资源

- **官方网站**：https://tdcommons.ai
- **文档**：https://tdc.readthedocs.io
- **GitHub**：https://github.com/mims-harvard/TDC
- **论文**：NeurIPS 2021 - "Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development"