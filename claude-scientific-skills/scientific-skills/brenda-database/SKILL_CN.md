---
name: brenda-database
description: 通过 SOAP API 访问 BRENDA 酶数据库。检索动力学参数（Km、kcat）、反应方程、生物体数据和底物特异性酶信息，用于生化研究和代谢途径分析。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# BRENDA 数据库

## 概述

BRENDA（BRaunschweig ENzyme DAtabase）是世界上最全面的酶信息系统，包含来自科学文献的详细酶数据。使用官方 SOAP API 查询动力学参数（Km、kcat）、反应方程、底物特异性、生物体信息和酶的最佳条件。访问超过 45,000 种酶和数百万个动力学数据点，用于生化研究、代谢工程和酶发现。

## 何时使用此技能

在以下情况应使用此技能：
- 搜索酶动力学参数（Km、kcat、Vmax）
- 检索反应方程和化学计量
- 查找特定底物或反应的酶
- 比较不同生物体的酶特性
- 研究最佳 pH、温度和条件
- 访问酶抑制和激活数据
- 支持代谢途径重建和逆合成
- 进行酶工程和优化研究
- 分析底物特性和辅因子要求

## 核心能力

### 1. 动力学参数检索

访问酶的综合动力学数据：

**按 EC 编号获取 Km 值**：
```python
from brenda_client import get_km_values

# 获取所有生物体的 Km 值
km_data = get_km_values("1.1.1.1")  # 醇脱氢酶

# 获取特定生物体的 Km 值
km_data = get_km_values("1.1.1.1", organism="Saccharomyces cerevisiae")

# 获取特定底物的 Km 值
km_data = get_km_values("1.1.1.1", substrate="ethanol")
```

**解析 Km 结果**：
```python
for entry in km_data:
    print(f"Km: {entry}")
    # 示例输出："organism*Homo sapiens#substrate*ethanol#kmValue*1.2#commentary*"
```

**提取特定信息**：
```python
from scripts.brenda_queries import parse_km_entry, extract_organism_data

for entry in km_data:
    parsed = parse_km_entry(entry)
    organism = extract_organism_data(entry)
    print(f"Organism: {parsed['organism']}")
    print(f"Substrate: {parsed['substrate']}")
    print(f"Km value: {parsed['km_value']}")
    print(f"pH: {parsed.get('ph', 'N/A')}")
    print(f"Temperature: {parsed.get('temperature', 'N/A')}")
```

### 2. 反应信息

检索反应方程和详细信息：

**按 EC 编号获取反应**：
```python
from brenda_client import get_reactions

# 获取 EC 编号的所有反应
reactions = get_reactions("1.1.1.1")

# 按生物体过滤
reactions = get_reactions("1.1.1.1", organism="Escherichia coli")

# 搜索特定反应
reactions = get_reactions("1.1.1.1", reaction="ethanol + NAD+")
```

**处理反应数据**：
```python
from scripts.brenda_queries import parse_reaction_entry, extract_substrate_products

for reaction in reactions:
    parsed = parse_reaction_entry(reaction)
    substrates, products = extract_substrate_products(reaction)

    print(f"Reaction: {parsed['reaction']}")
    print(f"Organism: {parsed['organism']}")
    print(f"Substrates: {substrates}")
    print(f"Products: {products}")
```

### 3. 酶发现

查找特定生化转化的酶：

**按底物查找酶**：
```python
from scripts.brenda_queries import search_enzymes_by_substrate

# 查找作用于葡萄糖的酶
enzymes = search_enzymes_by_substrate("glucose", limit=20)

for enzyme in enzymes:
    print(f"EC: {enzyme['ec_number']}")
    print(f"Name: {enzyme['enzyme_name']}")
    print(f"Reaction: {enzyme['reaction']}")
```

**按产物查找酶**：
```python
from scripts.brenda_queries import search_enzymes_by_product

# 查找产生乳酸的酶
enzymes = search_enzymes_by_product("lactate", limit=10)
```

**按反应模式搜索**：
```python
from scripts.brenda_queries import search_by_pattern

# 查找氧化反应
enzymes = search_by_pattern("oxidation", limit=15)
```

### 4. 生物体特异性酶数据

比较不同生物体的酶特性：

**获取多个生物体的酶数据**：
```python
from scripts.brenda_queries import compare_across_organisms

organisms = ["Escherichia coli", "Saccharomyces cerevisiae", "Homo sapiens"]
comparison = compare_across_organisms("1.1.1.1", organisms)

for org_data in comparison:
    print(f"Organism: {org_data['organism']}")
    print(f"Avg Km: {org_data['average_km']}")
    print(f"Optimal pH: {org_data['optimal_ph']}")
    print(f"Temperature range: {org_data['temperature_range']}")
```

**查找具有特定酶的生物体**：
```python
from scripts.brenda_queries import get_organisms_for_enzyme

organisms = get_organisms_for_enzyme("6.3.5.5")  # 谷氨酰胺合成酶
print(f"Found {len(organisms)} organisms with this enzyme")
```

### 5. 环境参数

访问最佳条件和环境参数：

**获取 pH 和温度数据**：
```python
from scripts.brenda_queries import get_environmental_parameters

params = get_environmental_parameters("1.1.1.1")

print(f"Optimal pH range: {params['ph_range']}")
print(f"Optimal temperature: {params['optimal_temperature']}")
print(f"Stability pH: {params['stability_ph']}")
print(f"Temperature stability: {params['temperature_stability']}")
```

**辅因子要求**：
```python
from scripts.brenda_queries import get_cofactor_requirements

cofactors = get_cofactor_requirements("1.1.1.1")
for cofactor in cofactors:
    print(f"Cofactor: {cofactor['name']}")
    print(f"Type: {cofactor['type']}")
    print(f"Concentration: {cofactor['concentration']}")
```

### 6. 底物特异性

分析酶底物偏好：

**获取底物特异性数据**：
```python
from scripts.brenda_queries import get_substrate_specificity

specificity = get_substrate_specificity("1.1.1.1")

for substrate in specificity:
    print(f"Substrate: {substrate['name']}")
    print(f"Km: {substrate['km']}")
    print(f"Vmax: {substrate['vmax']}")
    print(f"kcat: {substrate['kcat']}")
    print(f"Specificity constant: {substrate['kcat_km_ratio']}")
```

**比较底物偏好**：
```python
from scripts.brenda_queries import compare_substrate_affinity

comparison = compare_substrate_affinity("1.1.1.1")
sorted_by_km = sorted(comparison, key=lambda x: x['km'])

for substrate in sorted_by_km[:5]:  # 前 5 个最低 Km
    print(f"{substrate['name']}: Km = {substrate['km']}")
```

### 7. 抑制和激活

访问酶调节数据：

**获取抑制剂信息**：
```python
from scripts.brenda_queries import get_inhibitors

inhibitors = get_inhibitors("1.1.1.1")

for inhibitor in inhibitors:
    print(f"Inhibitor: {inhibitor['name']}")
    print(f"Type: {inhibitor['type']}")
    print(f"Ki: {inhibitor['ki']}")
    print(f"IC50: {inhibitor['ic50']}")
```

**获取激活剂信息**：
```python
from scripts.brenda_queries import get_activators

activators = get_activators("1.1.1.1")

for activator in activators:
    print(f"Activator: {activator['name']}")
    print(f"Effect: {activator['effect']}")
    print(f"Mechanism: {activator['mechanism']}")
```

### 8. 酶工程支持

查找工程靶点和替代方案：

**查找嗜热同源物**：
```python
from scripts.brenda_queries import find_thermophilic_homologs

thermophilic = find_thermophilic_homologs("1.1.1.1", min_temp=50)

for enzyme in thermophilic:
    print(f"Organism: {enzyme['organism']}")
    print(f"Optimal temp: {enzyme['optimal_temperature']}")
    print(f"Km: {enzyme['km']}")
```

**查找碱性/酸性稳定变体**：
```python
from scripts.brenda_queries import find_ph_stable_variants

alkaline = find_ph_stable_variants("1.1.1.1", min_ph=8.0)
acidic = find_ph_stable_variants("1.1.1.1", max_ph=6.0)
```

### 9. 动力学建模

为动力学建模准备数据：

**获取建模的动力学参数**：
```python
from scripts.brenda_queries import get_modeling_parameters

model_data = get_modeling_parameters("1.1.1.1", substrate="ethanol")

print(f"Km: {model_data['km']}")
print(f"Vmax: {model_data['vmax']}")
print(f"kcat: {model_data['kcat']}")
print(f"Enzyme concentration: {model_data['enzyme_conc']}")
print(f"Temperature: {model_data['temperature']}")
print(f"pH: {model_data['ph']}")
```

**生成 Michaelis-Menten 图**：
```python
from scripts.brenda_visualization import plot_michaelis_menten

# 生成动力学图
plot_michaelis_menten("1.1.1.1", substrate="ethanol")
```

## 安装要求

```bash
uv pip install zeep requests pandas matplotlib seaborn
```

## 身份验证设置

BRENDA 需要身份验证凭据：

1. **创建 .env 文件**：
```
BRENDA_EMAIL=your.email@example.com
BRENDA_PASSWORD=your_brenda_password
```

2. **或设置环境变量**：
```bash
export BRENDA_EMAIL="your.email@example.com"
export BRENDA_PASSWORD="your_brenda_password"
```

3. **注册 BRENDA 访问**：
   - 访问 https://www.brenda-enzymes.org/
   - 创建账户
   - 检查电子邮件以获取凭据
   - 注意：还有 `BRENDA_EMAIL`（注意拼写错误）用于传统支持

## 辅助脚本

此技能包括用于 BRENDA 数据库查询的综合 Python 脚本：

### scripts/brenda_queries.py

为酶数据分析提供高级函数：

**关键函数**：
- `parse_km_entry(entry)`：解析 BRENDA Km 数据条目
- `parse_reaction_entry(entry)`：解析反应数据条目
- `extract_organism_data(entry)`：提取生物体特异性信息
- `search_enzymes_by_substrate(substrate, limit)`：查找底物的酶
- `search_enzymes_by_product(product, limit)`：查找产生产物的酶
- `compare_across_organisms(ec_number, organisms)`：比较酶特性
- `get_environmental_parameters(ec_number)`：获取 pH 和温度数据
- `get_cofactor_requirements(ec_number)`：获取辅因子信息
- `get_substrate_specificity(ec_number)`：分析底物偏好
- `get_inhibitors(ec_number)`：获取酶抑制数据
- `get_activators(ec_number)`：获取酶激活数据
- `find_thermophilic_homologs(ec_number, min_temp)`：查找热稳定变体
- `get_modeling_parameters(ec_number, substrate)`：获取动力学建模参数
- `export_kinetic_data(ec_number, format, filename)`：将数据导出到文件

**用法**：
```python
from scripts.brenda_queries import search_enzymes_by_substrate, compare_across_organisms

# 搜索酶
enzymes = search_enzymes_by_substrate("glucose", limit=20)

# 跨生物体比较
comparison = compare_across_organisms("1.1.1.1", ["E. coli", "S. cerevisiae"])
```

### scripts/brenda_visualization.py

为酶数据提供可视化函数：

**关键函数**：
- `plot_kinetic_parameters(ec_number)`：绘制 Km 和 kcat 分布
- `plot_organism_comparison(ec_number, organisms)`：比较生物体
- `plot_pH_profiles(ec_number)`：绘制 pH 活性曲线
- `plot_temperature_profiles(ec_number)`：绘制温度活性曲线
- `plot_substrate_specificity(ec_number)`：可视化底物偏好
- `plot_michaelis_menten(ec_number, substrate)`：生成动力学曲线
- `create_heatmap_data(enzymes, parameters)`：创建热图数据
- `generate_summary_plots(ec_number)`：创建综合酶概述

**用法**：
```python
from scripts.brenda_visualization import plot_kinetic_parameters, plot_michaelis_menten

# 绘制动力学参数
plot_kinetic_parameters("1.1.1.1")

# 生成 Michaelis-Menten 曲线
plot_michaelis_menten("1.1.1.1", substrate="ethanol")
```

### scripts/enzyme_pathway_builder.py

构建酶途径和逆合成路线：

**关键函数**：
- `find_pathway_for_product(product, max_steps)`：查找酶途径
- `build_retrosynthetic_tree(target, depth)`：构建逆合成树
- `suggest_enzyme_substitutions(ec_number, criteria)`：建议酶替代方案
- `calculate_pathway_feasibility(pathway)`：评估途径可行性
- `optimize_pathway_conditions(pathway)`：建议最佳条件
- `generate_pathway_report(pathway, filename)`：创建详细途径报告

**用法**：
```python
from scripts.enzyme_pathway_builder import find_pathway_for_product, build_retrosynthetic_tree

# 查找产物途径
pathway = find_pathway_for_product("lactate", max_steps=3)

# 构建逆合成树
tree = build_retrosynthetic_tree("lactate", depth=2)
```

## API 速率限制和最佳实践

**速率限制**：
- BRENDA API 具有适度的速率限制
- 建议：持续使用时每秒 1 次请求
- 最大值：每 10 秒 5 次请求

**最佳实践**：
1. **缓存结果**：在本地存储频繁访问的酶数据
2. **批量查询**：尽可能组合相关请求
3. **使用特定搜索**：尽可能按生物体、底物缩小范围
4. **处理缺失数据**：并非所有酶都有完整数据
5. **验证 EC 编号**：确保 EC 编号格式正确
6. **实现延迟**：在连续请求之间添加延迟
7. **明智地使用通配符**：在适当的时候使用 '*' 进行更广泛的搜索
8. **监控配额**：跟踪您的 API 使用情况

**错误处理**：
```python
from brenda_client import get_km_values, get_reactions
from zeep.exceptions import Fault, TransportError

try:
    km_data = get_km_values("1.1.1.1")
except RuntimeError as e:
    print(f"Authentication error: {e}")
except Fault as e:
    print(f"BRENDA API error: {e}")
except TransportError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 常见工作流程

### 工作流程 1：新底物的酶发现

查找适合特定底物的酶：

```python
from brenda_client import get_km_values
from scripts.brenda_queries import search_enzymes_by_substrate, compare_substrate_affinity

# 搜索作用于底物的酶
substrate = "2-phenylethanol"
enzymes = search_enzymes_by_substrate(substrate, limit=15)

print(f"Found {len(enzymes)} enzymes for {substrate}")
for enzyme in enzymes:
    print(f"EC {enzyme['ec_number']}: {enzyme['enzyme_name']}")

# 获取最佳候选物的动力学数据
if enzymes:
    best_ec = enzymes[0]['ec_number']
    km_data = get_km_values(best_ec, substrate=substrate)

    if km_data:
        print(f"Kinetic data for {best_ec}:")
        for entry in km_data[:3]:  # 前 3 个条目
            print(f"  {entry}")
```

### 工作流程 2：跨生物体酶比较

比较不同生物体的酶特性：

```python
from scripts.brenda_queries import compare_across_organisms, get_environmental_parameters

# 定义用于比较的生物体
organisms = [
    "Escherichia coli",
    "Saccharomyces cerevisiae",
    "Bacillus subtilis",
    "Thermus thermophilus"
]

# 比较醇脱氢酶
comparison = compare_across_organisms("1.1.1.1", organisms)

print("Cross-organism comparison:")
for org_data in comparison:
    print(f"\n{org_data['organism']}:")
    print(f"  Average Km: {org_data['average_km']}")
    print(f"  Optimal pH: {org_data['optimal_ph']}")
    print(f"  Temperature: {org_data['optimal_temperature']}°C")

# 获取详细的环境参数
env_params = get_environmental_parameters("1.1.1.1")
print(f"\nOverall optimal pH range: {env_params['ph_range']}")
```

### 工作流程 3：酶工程靶点识别

查找酶改进的工程机会：

```python
from scripts.brenda_queries import (
    find_thermophilic_homologs,
    find_ph_stable_variants,
    compare_substrate_affinity
)

# 查找嗜热变体以提高热稳定性
thermophilic = find_thermophilic_homologs("1.1.1.1", min_temp=50)
print(f"Found {len(thermophilic)} thermophilic variants")

# 查找碱性稳定变体
alkaline = find_ph_stable_variants("1.1.1.1", min_ph=8.0)
print(f"Found {len(alkaline)} alkaline-stable variants")

# 比较底物特异性以确定工程靶点
specificity = compare_substrate_affinity("1.1.1.1")
print("Substrate affinity ranking:")
for i, sub in enumerate(specificity[:5]):
    print(f"  {i+1}. {sub['name']}: Km = {sub['km']}")
```

### 工作流程 4：酶途径构建

构建酶合成途径：

```python
from scripts.enzyme_pathway_builder import (
    find_pathway_for_product,
    build_retrosynthetic_tree,
    calculate_pathway_feasibility
)

# 查找产物途径
target = "lactate"
pathway = find_pathway_for_product(target, max_steps=3)

if pathway:
    print(f"Found pathway to {target}:")
    for i, step in enumerate(pathway['steps']):
        print(f"  Step {i+1}: {step['reaction']}")
        print(f"    Enzyme: EC {step['ec_number']}")
        print(f"    Organism: {step['organism']}")

# 评估途径可行性
feasibility = calculate_pathway_feasibility(pathway)
print(f"\nPathway feasibility score: {feasibility['score']}/10")
print(f"Potential issues: {feasibility['warnings']}")
```

### 工作流程 5：动力学参数分析

用于酶选择的综合动力学分析：

```python
from brenda_client import get_km_values
from scripts.brenda_queries import parse_km_entry, get_modeling_parameters
from scripts.brenda_visualization import plot_kinetic_parameters

# 获取综合动力学数据
ec_number = "1.1.1.1"
km_data = get_km_values(ec_number)

# 分析动力学参数
all_entries = []
for entry in km_data:
    parsed = parse_km_entry(entry)
    if parsed['km_value']:
        all_entries.append(parsed)

print(f"Analyzed {len(all_entries)} kinetic entries")

# 查找最佳动力学表现者
best_km = min(all_entries, key=lambda x: x['km_value'])
print(f"\nBest kinetic performer:")
print(f"  Organism: {best_km['organism']}")
print(f"  Substrate: {best_km['substrate']}")
print(f"  Km: {best_km['km_value']}")

# 获取建模参数
model_data = get_modeling_parameters(ec_number, substrate=best_km['substrate'])
print(f"\nModeling parameters:")
print(f"  Km: {model_data['km']}")
print(f"  kcat: {model_data['kcat']}")
print(f"  Vmax: {model_data['vmax']}")

# 生成可视化
plot_kinetic_parameters(ec_number)
```

### 工作流程 6：工业酶选择

为工业应用选择酶：

```python
from scripts.brenda_queries import (
    find_thermophilic_homologs,
    get_environmental_parameters,
    get_inhibitors
)

# 工业标准：高温耐受性、有机溶剂抗性
target_enzyme = "1.1.1.1"

# 查找嗜热变体
thermophilic = find_thermophilic_homologs(target_enzyme, min_temp=60)
print(f"Thermophilic candidates: {len(thermophilic)}")

# 检查溶剂耐受性（抑制剂数据）
inhibitors = get_inhibitors(target_enzyme)
solvent_tolerant = [
    inv for inv in inhibitors
    if 'ethanol' not in inv['name'].lower() and
       'methanol' not in inv['name'].lower()
]

print(f"Solvent tolerant candidates: {len(solvent_tolerant)}")

# 评估顶级候选物
for candidate in thermophilic[:3]:
    print(f"\nCandidate: {candidate['organism']}")
    print(f"  Optimal temp: {candidate['optimal_temperature']}°C")
    print(f"  Km: {candidate['km']}")
    print(f"  pH range: {candidate.get('ph_range', 'N/A')}")
```

## 数据格式和解析

### BRENDA 响应格式

BRENDA 以需要解析的特定格式返回数据：

**Km 值格式**：
```
organism*Escherichia coli#substrate*ethanol#kmValue*1.2#kmValueMaximum*#commentary*pH 7.4, 25°C#ligandStructureId*#literature*
```

**反应格式**：
```
ecNumber*1.1.1.1#organism*Saccharomyces cerevisiae#reaction*ethanol + NAD+ <=> acetaldehyde + NADH + H+#commentary*#literature*
```

### 数据提取模式

```python
import re

def parse_brenda_field(data, field_name):
    """从 BRENDA 数据条目中提取特定字段"""
    pattern = f"{field_name}\\*([^#]*)"
    match = re.search(pattern, data)
    return match.group(1) if match else None

def extract_multiple_values(data, field_name):
    """提取字段的多个值"""
    pattern = f"{field_name}\\*([^#]*)"
    matches = re.findall(pattern, data)
    return [match for match in matches if match.strip()]
```

## 参考文档

有关详细的 BRENDA 文档，请参阅 `references/api_reference.md`。这包括：
- 完整的 SOAP API 方法文档
- 完整的参数列表和格式
- EC 编号结构和验证
- 响应格式规范
- 错误代码和处理
- 数据字段定义
- 文献引用格式

## 故障排除

**身份验证错误**：
- 验证 .env 文件中的 BRENDA_EMAIL 和 BRENDA_PASSWORD
- 检查拼写是否正确（注意 BRENDA_EMAIL 传统支持）
- 确保 BRENDA 账户处于活动状态并具有 API 访问权限

**未返回结果**：
- 尝试使用通配符（*）进行更广泛的搜索
- 检查 EC 编号格式（例如，"1.1.1.1" 而不是 "1.1.1"）
- 验证底物拼写和命名
- 某些酶在 BRENDA 中的数据可能有限

**速率限制**：
- 在请求之间添加延迟（0.5-1 秒）
- 在本地缓存结果
- 使用更具体的查询以减少数据量
- 考虑对多个查询使用批量操作

**网络错误**：
- 检查互联网连接
- BRENDA 服务器可能暂时不可用
- 几分钟后重试
- 如果受地理限制，考虑使用 VPN

**数据格式问题**：
- 使用脚本中提供的解析函数
- BRENDA 数据在格式上可能不一致
- 优雅地处理缺失字段
- 使用前验证解析的数据

**性能问题**：
- 大型查询可能很慢；限制搜索范围
- 使用特定的生物体或底物过滤器
- 考虑对批量操作使用异步处理
- 监控大型数据集的内存使用情况

## 其他资源

- BRENDA 主页：https://www.brenda-enzymes.org/
- BRENDA SOAP API 文档：https://www.brenda-enzymes.org/soap.php
- 酶委员会（EC）编号：https://www.qmul.ac.uk/sbcs/iubmb/enzyme/
- Zeep SOAP 客户端：https://python-zeep.readthedocs.io/
- 酶命名法：https://www.iubmb.org/enzyme/
