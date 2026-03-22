---
name: string-database
description: 查询STRING API获取蛋白质-蛋白质相互作用（59M蛋白质，20B相互作用）。网络分析、GO/KEGG富集、相互作用发现、5000+物种，适用于系统生物学。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# STRING数据库

## 概述

STRING是一个全面的已知和预测蛋白质-蛋白质相互作用数据库，涵盖59M蛋白质和20B+相互作用，跨越5000+生物。查询相互作用网络，执行功能富集，通过REST API发现合作伙伴，用于系统生物学和通路分析。

## 何时使用此技能

当以下情况时应使用此技能：
- 检索单个或多个蛋白质的蛋白质-蛋白质相互作用网络
- 对蛋白质列表进行功能富集分析（GO、KEGG、Pfam）
- 发现相互作用伙伴并扩展蛋白质网络
- 测试蛋白质是否形成显著富集的功能模块
- 生成带有基于证据的着色的网络可视化
- 分析同源性和蛋白质家族关系
- 进行跨物种蛋白质相互作用比较
- 识别中心蛋白质和网络连接模式

## 快速入门

该技能提供：
1. Python辅助函数（`scripts/string_api.py`）用于所有STRING REST API操作
2. 综合参考文档（`references/string_reference.md`），包含详细的API规范

当用户请求STRING数据时，确定需要哪个操作并使用`scripts/string_api.py`中的适当函数。

## 核心操作

### 1. 标识符映射（`string_map_ids`）

将基因名称、蛋白质名称和外部ID转换为STRING标识符。

**何时使用**：开始任何STRING分析，验证蛋白质名称，查找规范标识符。

**用法**：
```python
from scripts.string_api import string_map_ids

# 映射单个蛋白质
result = string_map_ids('TP53', species=9606)

# 映射多个蛋白质
result = string_map_ids(['TP53', 'BRCA1', 'EGFR', 'MDM2'], species=9606)

# 每个查询映射多个匹配
result = string_map_ids('p53', species=9606, limit=5)
```

**参数**：
- `species`：NCBI分类ID（9606 = 人类，10090 = 小鼠，7227 = 果蝇）
- `limit`：每个标识符的匹配数（默认：1）
- `echo_query`：在输出中包含查询词（默认：1）

**最佳实践**：始终首先映射标识符，以便后续查询更快。

### 2. 网络检索（`string_network`）

以表格格式获取蛋白质-蛋白质相互作用网络数据。

**何时使用**：构建相互作用网络，分析连接性，检索相互作用证据。

**用法**：
```python
from scripts.string_api import string_network

# 获取单个蛋白质的网络
network = string_network('9606.ENSP00000269305', species=9606)

# 获取多个蛋白质的网络
proteins = ['9606.ENSP00000269305', '9606.ENSP00000275493']
network = string_network(proteins, required_score=700)

# 使用额外的相互作用蛋白扩展网络
network = string_network('TP53', species=9606, add_nodes=10, required_score=400)

# 仅物理相互作用
network = string_network('TP53', species=9606, network_type='physical')
```

**参数**：
- `required_score`：置信度阈值（0-1000）
  - 150：低置信度（探索性）
  - 400：中等置信度（默认，标准分析）
  - 700：高置信度（保守）
  - 900：最高置信度（非常严格）
- `network_type`：`'functional'`（所有证据，默认）或`'physical'`（仅直接结合）
- `add_nodes`：添加N个最连接的蛋白质（0-10）

**输出列**：相互作用对、置信度分数和各个证据分数（邻域、融合、共表达、实验、数据库、文本挖掘）。

### 3. 网络可视化（`string_network_image`）

生成作为PNG图像的网络可视化。

**何时使用**：创建图形、视觉探索、演示。

**用法**：
```python
from scripts.string_api import string_network_image

# 获取网络图像
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1']
img_data = string_network_image(proteins, species=9606, required_score=700)

# 保存图像
with open('network.png', 'wb') as f:
    f.write(img_data)

# 基于证据着色的网络
img = string_network_image(proteins, species=9606, network_flavor='evidence')

# 基于置信度的可视化
img = string_network_image(proteins, species=9606, network_flavor='confidence')

# 动作网络（激活/抑制）
img = string_network_image(proteins, species=9606, network_flavor='actions')
```

**网络风格**：
- `'evidence'`：彩色线条显示证据类型（默认）
- `'confidence'`：线条粗细表示置信度
- `'actions'`：显示激活/抑制关系

### 4. 相互作用伙伴（`string_interaction_partners`）

查找与给定蛋白质相互作用的所有蛋白质。

**何时使用**：发现新的相互作用，寻找中心蛋白质，扩展网络。

**用法**：
```python
from scripts.string_api import string_interaction_partners

# 获取TP53的前10个相互作用伙伴
partners = string_interaction_partners('TP53', species=9606, limit=10)

# 获取高置信度相互作用伙伴
partners = string_interaction_partners('TP53', species=9606,
                                      limit=20, required_score=700)

# 查找多个蛋白质的相互作用伙伴
partners = string_interaction_partners(['TP53', 'MDM2'],
                                      species=9606, limit=15)
```

**参数**：
- `limit`：返回的伙伴最大数量（默认：10）
- `required_score`：置信度阈值（0-1000）

**用例**：
- 中心蛋白质识别
- 从种子蛋白质扩展网络
- 发现间接连接

### 5. 功能富集（`string_enrichment`）

在基因本体论、KEGG通路、Pfam域等方面进行富集分析。

**何时使用**：解释蛋白质列表，通路分析，功能表征，理解生物学过程。

**用法**：
```python
from scripts.string_enrichment import string_enrichment

# 蛋白质列表的富集
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1', 'ATR', 'TP73']
enrichment = string_enrichment(proteins, species=9606)

# 解析结果以找到显著术语
import pandas as pd
df = pd.read_csv(io.StringIO(enrichment), sep='\t')
significant = df[df['fdr'] < 0.05]
```

**富集类别**：
- **基因本体论**：生物学过程、分子功能、细胞组件
- **KEGG通路**：代谢和信号通路
- **Pfam**：蛋白质域
- **InterPro**：蛋白质家族和域
- **SMART**：域结构
- **UniProt关键词**：策划的功能关键词

**输出列**：
- `category`：注释数据库（例如，"KEGG Pathways"、"GO Biological Process"）
- `term`：术语标识符
- `description`：人类可读的术语描述
- `number_of_genes`：具有此注释的输入蛋白质
- `p_value`：未校正的富集p值
- `fdr`：错误发现率（校正p值）

**统计方法**：Fisher精确检验，使用Benjamini-Hochberg FDR校正。

**解释**：FDR < 0.05表示统计显著富集。

### 6. PPI富集（`string_ppi_enrichment`）

测试蛋白质网络是否比随机预期有显著更多的相互作用。

**何时使用**：验证蛋白质是否形成功能模块，测试网络连接性。

**用法**：
```python
from scripts.string_api import string_ppi_enrichment
import json

# 测试网络连接性
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1']
result = string_ppi_enrichment(proteins, species=9606, required_score=400)

# 解析JSON结果
data = json.loads(result)
print(f"Observed edges: {data['number_of_edges']}")
print(f"Expected edges: {data['expected_number_of_edges']}")
print(f"P-value: {data['p_value']}")
```

**输出字段**：
- `number_of_nodes`：网络中的蛋白质
- `number_of_edges`：观察到的相互作用
- `expected_number_of_edges`：随机网络中的预期值
- `p_value`：统计显著性

**解释**：
- p值 < 0.05：网络显著富集（蛋白质可能形成功能模块）
- p值 ≥ 0.05：无显著富集（蛋白质可能无关）

### 7. 同源性分数（`string_homology`）

检索蛋白质相似性和同源性信息。

**何时使用**：识别蛋白质家族，旁系同源分析，跨物种比较。

**用法**：
```python
from scripts.string_api import string_homology

# 获取蛋白质之间的同源性
proteins = ['TP53', 'TP63', 'TP73']  # p53家族
homology = string_homology(proteins, species=9606)
```

**用例**：
- 蛋白质家族识别
- 旁系同源发现
- 进化分析

### 8. 版本信息（`string_version`）

获取当前STRING数据库版本。

**何时使用**：确保可重复性，记录方法。

**用法**：
```python
from scripts.string_api import string_version

version = string_version()
print(f"STRING version: {version}")
```

## 常见分析工作流

### 工作流1：蛋白质列表分析（标准工作流）

**用例**：分析来自实验的蛋白质列表（例如，差异表达、蛋白质组学）。

```python
from scripts.string_api import (string_map_ids, string_network,
                                string_enrichment, string_ppi_enrichment,
                                string_network_image)

# 步骤1：将基因名称映射到STRING ID
gene_list = ['TP53', 'BRCA1', 'ATM', 'CHEK2', 'MDM2', 'ATR', 'BRCA2']
mapping = string_map_ids(gene_list, species=9606)

# 步骤2：获取相互作用网络
network = string_network(gene_list, species=9606, required_score=400)

# 步骤3：测试网络是否富集
ppi_result = string_ppi_enrichment(gene_list, species=9606)

# 步骤4：执行功能富集
enrichment = string_enrichment(gene_list, species=9606)

# 步骤5：生成网络可视化
img = string_network_image(gene_list, species=9606,
                          network_flavor='evidence', required_score=400)
with open('protein_network.png', 'wb') as f:
    f.write(img)

# 步骤6：解析和解释结果
```

### 工作流2：单个蛋白质调查

**用例**：深入研究一种蛋白质的相互作用和伙伴。

```python
from scripts.string_api import (string_map_ids, string_interaction_partners,
                                string_network_image)

# 步骤1：映射蛋白质名称
protein = 'TP53'
mapping = string_map_ids(protein, species=9606)

# 步骤2：获取所有相互作用伙伴
partners = string_interaction_partners(protein, species=9606,
                                      limit=20, required_score=700)

# 步骤3：可视化扩展网络
img = string_network_image(protein, species=9606, add_nodes=15,
                          network_flavor='confidence', required_score=700)
with open('tp53_network.png', 'wb') as f:
    f.write(img)
```

### 工作流3：通路中心分析

**用例**：识别和可视化特定生物学通路中的蛋白质。

```python
from scripts.string_api import string_enrichment, string_network

# 步骤1：从已知通路蛋白质开始
dna_repair_proteins = ['TP53', 'ATM', 'ATR', 'CHEK1', 'CHEK2',
                       'BRCA1', 'BRCA2', 'RAD51', 'XRCC1']

# 步骤2：获取网络
network = string_network(dna_repair_proteins, species=9606,
                        required_score=700, add_nodes=5)

# 步骤3：富集以确认通路注释
enrichment = string_enrichment(dna_repair_proteins, species=9606)

# 步骤4：解析DNA修复通路的富集
import pandas as pd
import io
df = pd.read_csv(io.StringIO(enrichment), sep='\t')
dna_repair = df[df['description'].str.contains('DNA repair', case=False)]
```

### 工作流4：跨物种分析

**用例**：比较不同生物之间的蛋白质相互作用。

```python
from scripts.string_api import string_network

# 人类网络
human_network = string_network('TP53', species=9606, required_score=700)

# 小鼠网络
mouse_network = string_network('Trp53', species=10090, required_score=700)

# 酵母网络（如果存在同源物）
yeast_network = string_network('gene_name', species=4932, required_score=700)
```

### 工作流5：网络扩展和发现

**用例**：从种子蛋白质开始，发现连接的功能模块。

```python
from scripts.string_api import (string_interaction_partners, string_network,
                                string_enrichment)

# 步骤1：从种子蛋白质开始
seed_proteins = ['TP53']

# 步骤2：获取一级相互作用蛋白
partners = string_interaction_partners(seed_proteins, species=9606,
                                      limit=30, required_score=700)

# 步骤3：解析伙伴以获取蛋白质列表
import pandas as pd
import io
df = pd.read_csv(io.StringIO(partners), sep='\t')
all_proteins = list(set(df['preferredName_A'].tolist() +
                       df['preferredName_B'].tolist()))

# 步骤4：对扩展网络执行富集
enrichment = string_enrichment(all_proteins[:50], species=9606)

# 步骤5：筛选有趣的功能模块
enrichment_df = pd.read_csv(io.StringIO(enrichment), sep='\t')
modules = enrichment_df[enrichment_df['fdr'] < 0.001]
```

## 常见物种

指定物种时，使用NCBI分类ID：

| 生物 | 通用名称 | 分类ID |
|------|----------|--------|
| Homo sapiens | 人类 | 9606 |
| Mus musculus | 小鼠 | 10090 |
| Rattus norvegicus | 大鼠 | 10116 |
| Drosophila melanogaster | 果蝇 | 7227 |
| Caenorhabditis elegans | 秀丽隐杆线虫 | 6239 |
| Saccharomyces cerevisiae | 酵母 | 4932 |
| Arabidopsis thaliana | 拟南芥 | 3702 |
| Escherichia coli | 大肠杆菌 | 511145 |
| Danio rerio | 斑马鱼 | 7955 |

完整列表可在：https://string-db.org/cgi/input?input_page_active_form=organisms 查看

## 理解置信度分数

STRING提供综合置信度分数（0-1000），整合多种证据类型：

### 证据渠道

1. **邻域（nscore）**：跨物种保守的基因组邻域
2. **融合（fscore）**：基因融合事件
3. **系统发育谱（pscore）**：跨物种的共现模式
4. **共表达（ascore）**：相关RNA表达
5. **实验（escore）**：生化和遗传实验
6. **数据库（dscore）**：策划的通路和复合物数据库
7. **文本挖掘（tscore）**：文献共现和NLP提取

### 推荐阈值

根据分析目标选择阈值：

- **150（低置信度）**：探索性分析，假设生成
- **400（中等置信度）**：标准分析，平衡敏感性/特异性
- **700（高置信度）**：保守分析，高置信度相互作用
- **900（最高置信度）**：非常严格，首选实验证据

**权衡**：
- 较低阈值：更多相互作用（较高召回率，更多假阳性）
- 较高阈值：较少相互作用（较高精度，更多假阴性）

## 网络类型

### 功能网络（默认）

包括所有证据类型（实验、计算、文本挖掘）。表示功能相关的蛋白质，即使没有直接物理结合。

**何时使用**：
- 通路分析
- 功能富集研究
- 系统生物学
- 大多数一般分析

### 物理网络

仅包括直接物理结合的证据（实验数据和物理相互作用的数据库注释）。

**何时使用**：
- 结构生物学研究
- 蛋白质复合物分析
- 直接结合验证
- 需要物理接触时

## API最佳实践

1. **始终首先映射标识符**：在其他操作之前使用`string_map_ids()`以加快查询速度
2. **尽可能使用STRING ID**：使用格式`9606.ENSP00000269305`而不是基因名称
3. **为>10个蛋白质的网络指定物种**：准确结果所需
4. **尊重速率限制**：API调用之间等待1秒
5. **使用版本化URL以确保可重复性**：在参考文档中可用
6. **优雅处理错误**：检查返回字符串中的"Error:"前缀
7. **选择适当的置信度阈值**：将阈值与分析目标匹配

## 详细参考

有关综合API文档、完整参数列表、输出格式和高级用法，请参考`references/string_reference.md`。这包括：

- 完整的API端点规范
- 所有支持的输出格式（TSV、JSON、XML、PSI-MI）
- 高级功能（批量上传、值/排名富集）
- 错误处理和故障排除
- 与其他工具的集成（Cytoscape、R、Python库）
- 数据许可和引用信息

## 故障排除

**未找到蛋白质**：
- 验证物种参数与标识符匹配
- 尝试首先使用`string_map_ids()`映射标识符
- 检查蛋白质名称中的拼写错误

**空网络结果**：
- 降低置信度阈值（`required_score`）
- 检查蛋白质是否实际相互作用
- 验证物种正确

**超时或缓慢查询**：
- 减少输入蛋白质数量
- 使用STRING ID而不是基因名称
- 将大型查询分成批次

**"需要物种"错误**：
- 为>10个蛋白质的网络添加`species`参数
- 始终包含物种以保持一致性

**结果看起来意外**：
- 使用`string_version()`检查STRING版本
- 验证network_type适当（功能vs物理）
- 审查置信度阈值选择

## 其他资源

对于蛋白质组规模分析或完整物种网络上传：
- 访问 https://string-db.org
- 使用"Upload proteome"功能
- STRING将生成完整的相互作用网络并预测功能

对于完整数据集的批量下载：
- 下载页面：https://string-db.org/cgi/download
- 包括完整的相互作用文件、蛋白质注释和通路映射

## 数据许可

STRING数据在**Creative Commons BY 4.0**许可下免费提供：
- 学术和商业使用免费
- 发布时需要归因
- 引用最新的STRING出版物

## 引用

在出版物中使用STRING时，请引用最新的出版物，可从：https://string-db.org/cgi/about 获取