---
name: medchem
description: 药物化学和药物发现工具。包括分子性质预测、ADMET预测、药物相似性分析、先导化合物优化、虚拟筛选、QSAR建模、分子对接、药效团建模和药物设计。使用RDKit、OpenEye、Schrodinger、MOE等工具。适用于药物发现、先导化合物优化和药物设计。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# 药物化学

## 概述

药物化学和药物发现工具集，包括分子性质预测、ADMET预测、药物相似性分析、先导化合物优化、虚拟筛选、QSAR建模、分子对接、药效团建模和药物设计。该技能使用RDKit、OpenEye、Schrodinger、MOE等工具，适用于药物发现、先导化合物优化和药物设计。

## 核心能力

### 1. 分子性质预测

- **物理化学性质**：分子量、LogP、TPSA、氢键供体/受体
- **溶解度**：LogS、水溶性
- **渗透性**：Caco-2渗透性、血脑屏障渗透性
- **反应性**：反应性基团、代谢稳定性
- **毒性**：毒性预测、hERG抑制

### 2. ADMET预测

- **吸收**：肠道吸收、生物利用度
- **分布**：血浆蛋白结合、组织分布
- **代谢**：代谢稳定性、CYP抑制
- **排泄**：清除率、半衰期
- **毒性**：肝毒性、心脏毒性、遗传毒性

### 3. 药物相似性分析

- **Lipinski规则**：五规则
- **Veber规则**：口服生物利用度规则
- **Ghose规则**：药物相似性规则
- **Egan规则**：药物相似性规则
- **Muegge规则**：药物相似性规则

### 4. 先导化合物优化

- **生物电子等排替换**：替换功能基团
- **骨架跃迁**：改变分子骨架
- **官能团修饰**：修饰官能团
- **构象限制**：限制分子构象
- **前药设计**：设计前药

### 5. 虚拟筛选

- **基于配体的筛选**：基于配体的虚拟筛选
- **基于结构的筛选**：基于结构的虚拟筛选
- **药效团筛选**：基于药效团的筛选
- **机器学习筛选**：基于机器学习的筛选

### 6. QSAR建模

- **描述符计算**：计算分子描述符
- **特征选择**：选择相关特征
- **模型构建**：构建QSAR模型
- **模型验证**：验证模型性能
- **模型应用**：应用模型预测

### 7. 分子对接

- **对接准备**：准备配体和受体
- **对接计算**：执行分子对接
- **结果分析**：分析对接结果
- **打分函数**：使用打分函数评估

### 8. 药效团建模

- **药效团识别**：识别药效团特征
- **药效团生成**：生成药效团模型
- **药效团筛选**：基于药效团筛选
- **药效团优化**：优化药效团模型

## 何时使用此技能

在以下情况下使用此技能：
- 预测分子性质和ADMET
- 进行药物相似性分析
- 优化先导化合物
- 执行虚拟筛选
- 构建QSAR模型
- 进行分子对接
- 建立药效团模型
- 进行药物设计

## 常用工具

### RDKit
- **特点**：开源、功能丰富
- **适用**：分子描述符、指纹、化学信息学
- **优势**：免费、易于使用

### OpenEye
- **特点**：商业软件、高性能
- **适用**：分子对接、药效团建模
- **优势**：精确、高效

### Schrodinger
- **特点**：商业软件、全面
- **适用**：药物发现、分子对接
- **优势**：功能全面、文档完善

### MOE
- **特点**：商业软件、集成
- **适用**：药物设计、分子建模
- **优势**：集成环境、可视化

## 使用示例

### 分子性质预测（RDKit）

```python
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

# 创建分子
mol = Chem.MolFromSmiles("CCO")

# 计算分子性质
mw = Descriptors.MolWt(mol)
logp = Descriptors.MolLogP(mol)
tpsa = Descriptors.TPSA(mol)
hbd = Lipinski.NumHDonors(mol)
hba = Lipinski.NumHAcceptors(mol)

print(f"分子量: {mw}")
print(f"LogP: {logp}")
print(f"TPSA: {tpsa}")
print(f"氢键供体: {hbd}")
print(f"氢键受体: {hba}")
```

### Lipinski规则检查

```python
from rdkit import Chem
from rdkit.Chem import Lipinski

def lipinski_rule(mol):
    mw = Lipinski.MolWt(mol)
    logp = Lipinski.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    
    if mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10:
        return True
    return False

mol = Chem.MolFromSmiles("CCO")
print(f"符合Lipinski规则: {lipinski_rule(mol)}")
```

### 虚拟筛选

```python
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import FingerprintSimilarity

# 参考分子
ref_mol = Chem.MolFromSmiles("CCO")
ref_fp = AllChem.GetMorganFingerprintAsBitVect(ref_mol, 2)

# 候选分子
candidates = ["CC(C)O", "c1ccccc1", "CCN"]

# 计算相似性
for smi in candidates:
    mol = Chem.MolFromSmiles(smi)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
    similarity = FingerprintSimilarity(ref_fp, fp)
    print(f"{smi}: {similarity}")
```

### QSAR建模

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd

# 准备数据
data = pd.read_csv("molecules.csv")
smiles = data["smiles"]
activity = data["activity"]

# 计算描述符
X = []
for smi in smiles:
    mol = Chem.MolFromSmiles(smi)
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    tpsa = Descriptors.TPSA(mol)
    X.append([mw, logp, tpsa])

# 分割数据
X_train, X_test, y_train, y_test = train_test_split(X, activity, test_size=0.2)

# 构建模型
model = RandomForestRegressor()
model.fit(X_train, y_train)

# 评估模型
score = model.score(X_test, y_test)
print(f"模型得分: {score}")
```

## 最佳实践

1. **数据质量**：确保数据质量高、可靠
2. **描述符选择**：选择与活性相关的描述符
3. **模型验证**：使用交叉验证和外部验证
4. **多样性**：确保分子多样性
5. **可解释性**：确保模型可解释
6. **实验验证**：实验验证预测结果

## 常见问题

**Q: 什么是Lipinski规则？**
A: Lipinski规则是预测口服药物吸收的五规则：分子量≤500、LogP≤5、氢键供体≤5、氢键受体≤10。

**Q: 如何进行虚拟筛选？**
A: 使用分子相似性、药效团或分子对接进行虚拟筛选。

**Q: QSAR模型的局限性是什么？**
A: QSAR模型依赖于训练数据，外推能力有限。

**Q: 如何优化先导化合物？**
A: 通过生物电子等排替换、骨架跃迁、官能团修饰等方法优化先导化合物。

## 资源

- **RDKit文档**：https://www.rdkit.org/docs
- **OpenEye文档**：https://docs.eyesopen.com
- **Schrodinger文档**：https://www.schrodinger.com/documentation
- **MOE文档**：https://www.chemcomp.com/MOE-documentation
