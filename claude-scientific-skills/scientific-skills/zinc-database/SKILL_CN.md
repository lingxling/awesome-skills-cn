---
name: zinc-database
description: 访问ZINC（2.3亿+可购买化合物）。通过ZINC ID/SMILES搜索，相似性搜索，用于对接的3D就绪结构，类似物发现，用于虚拟筛选和药物发现。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# ZINC数据库

## 概述

ZINC是由UCSF维护的可自由访问的2.3亿+可购买化合物库。通过ZINC ID或SMILES搜索，执行相似性搜索，下载用于对接的3D就绪结构，发现用于虚拟筛选和药物发现的类似物。

## 何时使用此技能

此技能应在以下情况使用：

- **虚拟筛选**：为分子对接研究寻找化合物
- **先导发现**：识别可商购的药物开发化合物
- **结构搜索**：通过SMILES执行相似性或类似物搜索
- **化合物检索**：通过ZINC ID或供应商代码查找分子
- **化学空间探索**：探索可购买的化学多样性
- **对接研究**：访问3D就绪的分子结构
- **类似物搜索**：基于结构相似性寻找相似化合物
- **供应商查询**：识别来自特定化学供应商的化合物
- **随机采样**：获取用于筛选的随机化合物集

## 数据库版本

ZINC经历了多个版本：

- **ZINC22**（当前）：最大版本，包含2.3亿+可购买化合物和数十亿规模的按需合成化合物
- **ZINC20**：仍在维护，专注于类先导和类药物化合物
- **ZINC15**：前身版本，传统但仍有文档

此技能主要关注ZINC22，最当前和全面的版本。

## 访问方法

### Web界面

主要访问点：https://zinc.docking.org/
交互式搜索：https://cartblanche22.docking.org/

### API访问

所有ZINC22搜索都可以通过CartBlanche22 API以编程方式执行：

**基础URL**：`https://cartblanche22.docking.org/`

所有API端点以文本或JSON格式返回数据，具有可自定义字段。

## 核心功能

### 1. 通过ZINC ID搜索

使用ZINC标识符检索特定化合物。

**Web界面**：https://cartblanche22.docking.org/search/zincid

**API端点**：
```bash
curl "https://cartblanche22.docking.org/[email protected]_fields=smiles,zinc_id"
```

**多个ID**：
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=smiles,zinc_id,tranche"
```

**响应字段**：`zinc_id`、`smiles`、`sub_id`、`supplier_code`、`catalogs`、`tranche`（包括H计数、LogP、MW、phase）

### 2. 通过SMILES搜索

使用SMILES表示法按化学结构查找化合物，具有用于类似物搜索的可选距离参数。

**Web界面**：https://cartblanche22.docking.org/search/smiles

**API端点**：
```bash
curl "https://cartblanche22.docking.org/[email protected]=4-Fadist=4"
```

**参数**：
- `smiles`：查询SMILES字符串（必要时URL编码）
- `dist`：Tanimoto距离阈值（默认：0表示精确匹配）
- `adist`：用于更广泛搜索的替代距离参数（默认：0）
- `output_fields`：所需输出字段的逗号分隔列表

**示例 - 精确匹配**：
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1"
```

**示例 - 相似性搜索**：
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1&dist=3&output_fields=zinc_id,smiles,tranche"
```

### 3. 通过供应商代码搜索

查询来自特定化学供应商的化合物或检索特定目录中的所有分子。

**Web界面**：https://cartblanche22.docking.org/search/catitems

**API端点**：
```bash
curl "https://cartblanche22.docking.org/catitems.txt:catitem_id=SUPPLIER-CODE-123"
```

**用例**：
- 验证来自特定供应商的化合物可用性
- 检索目录中的所有化合物
- 将供应商代码与ZINC ID交叉引用

### 4. 随机化合物采样

生成用于筛选或基准测试的随机化合物集。

**Web界面**：https://cartblanche22.docking.org/search/random

**API端点**：
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=100"
```

**参数**：
- `count`：要检索的随机化合物数量（默认：100）
- `subset`：按子集筛选（例如，'lead-like'、'drug-like'、'fragment'）
- `output_fields`：自定义返回数据字段

**示例 - 随机类先导分子**：
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=1000&subset=lead-like&output_fields=zinc_id,smiles,tranche"
```

## 常见工作流程

### 工作流程1：准备对接库

1. **基于目标属性或所需化学空间定义搜索条件**

2. **使用适当的搜索方法查询ZINC22**：
   ```bash
   # 示例：获取具有特定LogP和MW的类药物化合物
   curl "https://cartblanche22.docking.org/substance/random.txt:count=10000&subset=drug-like&output_fields=zinc_id,smiles,tranche" > docking_library.txt
   ```

3. **解析结果以提取ZINC ID和SMILES**：
   ```python
   import pandas as pd

   # 加载结果
   df = pd.read_csv('docking_library.txt', sep='\t')

   # 按tranche数据中的属性筛选
   # Tranche格式：H##P###M###-phase
   # H = H键供体，P = LogP*10，M = MW
   ```

4. **使用ZINC ID下载3D结构**或从文件存储库下载用于对接

### 工作流程2：寻找命中化合物的类似物

1. **获取命中化合物的SMILES**：
   ```python
   hit_smiles = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"  # 示例：布洛芬
   ```

2. **执行带距离阈值的相似性搜索**：
   ```bash
   curl "https://cartblanche22.docking.org/smiles.txt:smiles=CC(C)Cc1ccc(cc1)C(C)C(=O)O&dist=5&output_fields=zinc_id,smiles,catalogs" > analogs.txt
   ```

3. **分析结果以识别可购买的类似物**：
   ```python
   import pandas as pd

   analogs = pd.read_csv('analogs.txt', sep='\t')
   print(f"找到 {len(analogs)} 个类似物")
   print(analogs[['zinc_id', 'smiles', 'catalogs']].head(10))
   ```

4. **为最有前景的类似物检索3D结构**

### 工作流程3：批量化合物检索

1. **从文献、数据库或先前的筛选中编译ZINC ID列表**：
   ```python
   zinc_ids = [
       "ZINC000000000001",
       "ZINC000000000002",
       "ZINC000000000003"
   ]
   zinc_ids_str = ",".join(zinc_ids)
   ```

2. **查询ZINC22 API**：
   ```bash
   curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=zinc_id,smiles,supplier_code,catalogs"
   ```

3. **处理结果用于下游分析或采购**

### 工作流程4：化学空间采样

1. **根据筛选目标选择子集参数**：
   - 片段：MW < 250，适合基于片段的药物发现
   - 类先导：MW 250-350，LogP ≤ 3.5
   - 类药物：MW 350-500，遵循Lipinski五规则

2. **生成随机样本**：
   ```bash
   curl "https://cartblanche22.docking.org/substance/random.txt:count=5000&subset=lead-like&output_fields=zinc_id,smiles,tranche" > chemical_space_sample.txt
   ```

3. **分析化学多样性**并为虚拟筛选做准备

## 输出字段

使用`output_fields`参数自定义API响应：

**可用字段**：
- `zinc_id`：ZINC标识符
- `smiles`：SMILES字符串表示
- `sub_id`：内部物质ID
- `supplier_code`：供应商目录号
- `catalogs`：提供化合物的供应商列表
- `tranche`：编码的分子属性（H计数、LogP、MW、反应性阶段）

**示例**：
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001&output_fields=zinc_id,smiles,catalogs,tranche"
```

## Tranche系统

ZINC根据分子属性将化合物组织为"tranche"：

**格式**：`H##P###M###-phase`

- **H##**：氢键供体数量（00-99）
- **P###**：LogP × 10（例如，P035 = LogP 3.5）
- **M###**：分子量（道尔顿）（例如，M400 = 400 Da）
- **phase**：反应性分类

**示例tranche**：`H05P035M400-0`
- 5个H键供体
- LogP = 3.5
- MW = 400 Da
- 反应性阶段0

使用tranche数据按药物相似性标准筛选化合物。

## 下载3D结构

对于分子对接，3D结构可通过文件存储库获取：

**文件存储库**：https://files.docking.org/zinc22/

结构按tranche组织，有多种格式可用：
- MOL2：带3D坐标的多分子格式
- SDF：结构数据文件格式
- DB2.GZ：DOCK的压缩数据库格式

有关下载协议和批量访问方法，请参阅ZINC文档：https://wiki.docking.org

## Python集成

### 使用curl与Python

```python
import subprocess
import json

def query_zinc_by_id(zinc_id, output_fields="zinc_id,smiles,catalogs"):
    """通过ZINC ID查询ZINC22。"""
    url = f"https://cartblanche22.docking.org/[email protected]_id={zinc_id}&output_fields={output_fields}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout

def search_by_smiles(smiles, dist=0, adist=0, output_fields="zinc_id,smiles"):
    """通过SMILES搜索ZINC22，带有可选距离参数。"""
    url = f"https://cartblanche22.docking.org/smiles.txt:smiles={smiles}&dist={dist}&adist={adist}&output_fields={output_fields}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout

def get_random_compounds(count=100, subset=None, output_fields="zinc_id,smiles,tranche"):
    """从ZINC22获取随机化合物。"""
    url = f"https://cartblanche22.docking.org/substance/random.txt:count={count}&output_fields={output_fields}"
    if subset:
        url += f"&subset={subset}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout
```

### 解析结果

```python
import pandas as pd
from io import StringIO

# 查询ZINC并解析为DataFrame
result = query_zinc_by_id("ZINC000000000001")
df = pd.read_csv(StringIO(result), sep='\t')

# 提取tranche属性
def parse_tranche(tranche_str):
    """解析ZINC tranche代码以提取属性。"""
    # 格式：H##P###M###-phase
    import re
    match = re.match(r'H(\d+)P(\d+)M(\d+)-(\d+)', tranche_str)
    if match:
        return {
            'h_donors': int(match.group(1)),
            'logP': int(match.group(2)) / 10.0,
            'mw': int(match.group(3)),
            'phase': int(match.group(4))
        }
    return None

df['tranche_props'] = df['tranche'].apply(parse_tranche)
```

## 最佳实践

### 查询优化

- **开始具体**：在扩展到相似性搜索之前，先进行精确搜索
- **使用适当的距离参数**：小的dist值（1-3）用于接近类似物，大的（5-10）用于多样化类似物
- **限制输出字段**：仅请求必要的字段以减少数据传输
- **批量查询**：尽可能在单个API调用中组合多个ZINC ID

### 性能考虑

- **速率限制**：尊重服务器资源；避免快速连续请求
- **缓存**：在本地存储频繁访问的化合物
- **并行下载**：下载3D结构时，对文件存储库使用并行wget或aria2c
- **子集筛选**：使用类先导、类药物或片段子集来减少搜索空间

### 数据质量

- **验证可用性**：供应商目录会变化；在大量订单前确认化合物可用性
- **检查立体化学**：SMILES可能未完全指定立体化学；验证3D结构
- **验证结构**：使用化学信息学工具（RDKit、OpenBabel）验证结构有效性
- **交叉引用**：可能时，与其他数据库（PubChem、ChEMBL）交叉检查

## 资源

### references/api_reference.md

综合文档包括：

- 完整的API端点参考
- URL语法和参数规范
- 高级查询模式和示例
- 文件存储库组织和访问
- 批量下载方法
- 错误处理和故障排除
- 与分子对接软件的集成

请参考此文档获取详细的技术信息和高级使用模式。

## 重要免责声明

### 数据可靠性

ZINC明确声明：**"我们不保证任何分子用于任何目的的质量，对使用本数据库引起的错误不承担任何责任。"**

- 化合物可用性可能会随时更改，恕不通知
- 结构表示可能包含错误
- 供应商信息应独立验证
- 在实验工作前使用适当的验证

### 适当使用

- ZINC旨在用于药物发现的学术和研究目的
- 验证商业使用的许可条款
- 处理专利化合物时尊重知识产权
- 遵循您机构的化合物采购指南

## 其他资源

- **ZINC网站**：https://zinc.docking.org/
- **CartBlanche22界面**：https://cartblanche22.docking.org/
- **ZINC Wiki**：https://wiki.docking.org/
- **文件存储库**：https://files.docking.org/zinc22/
- **GitHub**：https://github.com/docking-org/
- **主要出版物**：Irwin et al., J. Chem. Inf. Model 2020 (ZINC15)
- **ZINC22出版物**：Irwin et al., J. Chem. Inf. Model 2023

## 引用

在出版物中使用ZINC时，请引用适当的版本：

**ZINC22**：
Irwin, J. J., et al. "ZINC22—A Free Multi-Billion-Scale Database of Tangible Compounds for Ligand Discovery." *Journal of Chemical Information and Modeling* 2023.

**ZINC15**：
Irwin, J. J., et al. "ZINC15 – Ligand Discovery for Everyone." *Journal of Chemical Information and Modeling* 2020, 60, 6065–6073.