---
name: opentargets-database
description: 查询 Open Targets 平台获取目标-疾病关联、药物靶点发现、可靶向性/安全性数据、遗传学/组学证据、已知药物，用于治疗靶点识别。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Open Targets 数据库

## 概述

Open Targets 平台是一个综合资源，用于系统识别和优先排序潜在的治疗药物靶点。它整合了公开可用的数据集，包括人类遗传学、组学、文献和化学数据，以构建和评分靶点-疾病关联。

**关键功能：**
- 查询靶点（基因）注释，包括可靶向性、安全性、表达
- 搜索带有证据评分的疾病-靶点关联
- 从多种数据类型（遗传学、通路、文献等）检索证据
- 查找疾病的已知药物及其机制
- 访问药物信息，包括临床试验阶段和不良事件
- 评估靶点的可药性和治疗潜力

**数据访问：** 该平台提供 GraphQL API、Web 界面、数据下载和 Google BigQuery 访问。此技能专注于用于编程访问的 GraphQL API。

## 何时使用此技能

此技能应在以下情况使用：

- **靶点发现：** 为疾病寻找潜在的治疗靶点
- **靶点评估：** 评估基因的可靶向性、安全性和可药性
- **证据收集：** 检索支持靶点-疾病关联的证据
- **药物重新定位：** 识别可用于新适应症的现有药物
- **竞争情报：** 了解临床先例和药物开发格局
- **靶点优先排序：** 基于遗传证据和其他数据类型对靶点进行排名
- **机制研究：** 研究生物通路和基因功能
- **生物标志物发现：** 寻找在疾病中差异表达的基因
- **安全性评估：** 识别药物靶点的潜在毒性问题

## 核心工作流程

### 1. 搜索实体

首先找到目标、疾病或药物的标识符。

**对于靶点（基因）：**
```python
from scripts.query_opentargets import search_entities

# 按基因符号或名称搜索
results = search_entities("BRCA1", entity_types=["target"])
# 返回: [{"id": "ENSG00000012048", "name": "BRCA1", ...}]
```

**对于疾病：**
```python
# 按疾病名称搜索
results = search_entities("alzheimer", entity_types=["disease"])
# 返回: [{"id": "EFO_0000249", "name": "Alzheimer disease", ...}]
```

**对于药物：**
```python
# 按药物名称搜索
results = search_entities("aspirin", entity_types=["drug"])
# 返回: [{"id": "CHEMBL25", "name": "ASPIRIN", ...}]
```

**使用的标识符：**
- 靶点：Ensembl 基因 ID（例如，`ENSG00000157764`）
- 疾病：EFO（实验因素本体论）ID（例如，`EFO_0000249`）
- 药物：ChEMBL ID（例如，`CHEMBL25`）

### 2. 查询靶点信息

检索全面的靶点注释以评估可药性和生物学特性。

```python
from scripts.query_opentargets import get_target_info

target_info = get_target_info("ENSG00000157764", include_diseases=True)

# 访问关键字段：
# - approvedSymbol: HGNC 基因符号
# - approvedName: 完整基因名称
# - tractability: 跨模式的可药性评估
# - safetyLiabilities: 已知安全隐患
# - geneticConstraint: 来自 gnomAD 的约束评分
# - associatedDiseases: 带有评分的顶级疾病关联
```

**要审查的关键注释：**
- **可靶向性：** 小分子、抗体、PROTAC 可药性预测
- **安全性：** 来自多个数据库的已知毒性问题
- **遗传约束：** 表明必要性的 pLI 和 LOEUF 评分
- **疾病关联：** 与靶点链接的疾病及其证据评分

有关所有靶点特征的详细信息，请参阅 `references/target_annotations.md`。

### 3. 查询疾病信息

获取疾病详情和相关靶点/药物。

```python
from scripts.query_opentargets import get_disease_info

disease_info = get_disease_info("EFO_0000249", include_targets=True)

# 访问字段：
# - name: 疾病名称
# - description: 疾病描述
# - therapeuticAreas: 高级疾病类别
# - associatedTargets: 带有关联评分的顶级靶点
```

### 4. 检索靶点-疾病证据

获取支持靶点-疾病关联的详细证据。

```python
from scripts.query_opentargets import get_target_disease_evidence

# 获取所有证据
evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="EFO_0000249"
)

# 按证据类型过滤
genetic_evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="EFO_0000249",
    data_types=["genetic_association"]
)

# 每条证据记录包含：
# - datasourceId: 特定数据源（例如，"gwas_catalog", "chembl"）
# - datatypeId: 证据类别（例如，"genetic_association", "known_drug"）
# - score: 证据强度（0-1）
# - studyId: 原始研究标识符
# - literature: 相关出版物
```

**主要证据类型：**
1. **genetic_association：** GWAS、罕见变异、ClinVar、基因负担
2. **somatic_mutation：** 癌症基因普查、IntOGen、癌症生物标志物
3. **known_drug：** 来自已批准/临床药物的临床先例
4. **affected_pathway：** CRISPR 筛选、通路分析、基因签名
5. **rna_expression：** 来自 Expression Atlas 的差异表达
6. **animal_model：** 来自 IMPC 的小鼠表型
7. **literature：** 来自 Europe PMC 的文本挖掘

有关所有证据类型的详细描述和解释指南，请参阅 `references/evidence_types.md`。

### 5. 查找已知药物

识别用于疾病的药物及其靶点。

```python
from scripts.query_opentargets import get_known_drugs_for_disease

drugs = get_known_drugs_for_disease("EFO_0000249")

# drugs 包含：
# - uniqueDrugs: 独特药物总数
# - uniqueTargets: 独特靶点总数
# - rows: 药物-靶点-适应症记录列表，包含：
#   - drug: {name, drugType, maximumClinicalTrialPhase}
#   - targets: 药物靶向的基因
#   - phase: 此适应症的临床试验阶段
#   - status: 试验状态（活跃、完成等）
#   - mechanismOfAction: 药物如何工作
```

**临床阶段：**
- 第 4 阶段：已批准药物
- 第 3 阶段：晚期临床试验
- 第 2 阶段：中期试验
- 第 1 阶段：早期安全性试验

### 6. 获取药物信息

检索详细的药物信息，包括机制和适应症。

```python
from scripts.query_opentargets import get_drug_info

drug_info = get_drug_info("CHEMBL25")

# 访问：
# - name, synonyms: 药物标识符
# - drugType: 小分子、抗体等
# - maximumClinicalTrialPhase: 开发阶段
# - mechanismsOfAction: 靶点和作用类型
# - indications: 带有试验阶段的疾病
# - withdrawnNotice: 如果撤回，原因和国家
```

### 7. 获取靶点的所有关联

查找与靶点关联的所有疾病，可选择按评分过滤。

```python
from scripts.query_opentargets import get_target_associations

# 获取评分 >= 0.5 的关联
associations = get_target_associations(
    ensembl_id="ENSG00000157764",
    min_score=0.5
)

# 每个关联包含：
# - disease: {id, name}
# - score: 总体关联评分（0-1）
# - datatypeScores: 按证据类型的细分
```

**关联评分：**
- 范围：0-1（越高 = 证据越强）
- 使用调和和聚合所有数据类型的证据
- 不是置信度评分，而是相对排名指标
- 研究不足的疾病可能得分较低，尽管有良好的证据

## GraphQL API 详情

**对于超出提供的辅助函数的自定义查询**，直接使用 GraphQL API 或修改 `scripts/query_opentargets.py`。

关键信息：
- **端点：** `https://api.platform.opentargets.org/api/v4/graphql`
- **交互式浏览器：** `https://api.platform.opentargets.org/api/v4/graphql/browser`
- **无需身份验证**
- **仅请求所需字段**以最小化响应大小
- **对大型结果集使用分页**：`page: {size: N, index: M}`

有关以下内容，请参阅 `references/api_reference.md`：
- 完整的端点文档
- 所有实体类型的示例查询
- 错误处理模式
- API 使用的最佳实践

## 最佳实践

### 靶点优先排序策略

在优先排序药物靶点时：

1. **从遗传证据开始：** 人类遗传学（GWAS、罕见变异）提供最强的疾病相关性
2. **检查可靶向性：** 优先选择有临床或发现先例的靶点
3. **评估安全性：** 审查安全隐患、表达模式和遗传约束
4. **评估临床先例：** 已知药物表明可药性和治疗窗口
5. **考虑多种证据类型：** 来自不同来源的收敛证据增加信心
6. **机械验证：** 通路证据和生物学合理性
7. **手动审查文献：** 对于关键决策，检查原始出版物

### 证据解释

**强证据指标：**
- 多个独立证据来源
- 高遗传关联评分（尤其是 L2G > 0.5 的 GWAS）
- 来自已批准药物的临床先例
- 与疾病匹配的 ClinVar 致病性变异
- 具有相关表型的小鼠模型

**注意事项：**
- 仅单一证据来源
- 文本挖掘作为唯一证据（需要手动验证）
- 跨来源的冲突证据
- 高必要性 + 普遍表达（治疗窗口差）
- 多个安全隐患

**评分解释：**
- 评分排名相对强度，而非绝对置信度
- 研究不足的疾病尽管有潜在有效的靶点，但得分较低
- 专家策划的来源权重高于计算预测
- 检查证据细分，而不仅仅是总体评分

### 常见工作流程

**工作流程 1：疾病的靶点发现**
1. 搜索疾病 → 获取 EFO ID
2. 使用 `include_targets=True` 查询疾病信息
3. 审查按关联评分排序的顶级靶点
4. 对于有前途的靶点，获取详细的靶点信息
5. 检查支持每个关联的证据类型
6. 评估优先靶点的可靶向性和安全性

**工作流程 2：靶点验证**
1. 搜索靶点 → 获取 Ensembl ID
2. 获取全面的靶点信息
3. 检查可靶向性（尤其是临床先例）
4. 审查安全隐患和遗传约束
5. 检查疾病关联以了解生物学
6. 寻找化学探针或工具化合物
7. 检查靶向基因的已知药物以获取机制见解

**工作流程 3：药物重新定位**
1. 搜索疾病 → 获取 EFO ID
2. 获取疾病的已知药物
3. 对于每种药物，获取详细的药物信息
4. 检查作用机制和靶点
5. 寻找相关疾病适应症
6. 评估临床试验阶段和状态
7. 基于机制识别重新定位机会

**工作流程 4：竞争情报**
1. 搜索感兴趣的靶点
2. 获取带有证据的相关疾病
3. 对于每种疾病，获取已知药物
4. 审查临床阶段和开发状态
5. 识别竞争对手及其机制
6. 评估临床先例和市场格局

## 资源

### 脚本

**scripts/query_opentargets.py**
用于常见 API 操作的辅助函数：
- `search_entities()` - 搜索靶点、疾病或药物
- `get_target_info()` - 检索靶点注释
- `get_disease_info()` - 检索疾病信息
- `get_target_disease_evidence()` - 获取支持证据
- `get_known_drugs_for_disease()` - 查找疾病的药物
- `get_drug_info()` - 检索药物详情
- `get_target_associations()` - 获取靶点的所有关联
- `execute_query()` - 执行自定义 GraphQL 查询

### 参考资料

**references/api_reference.md**
完整的 GraphQL API 文档，包括：
- 端点详细信息和身份验证
- 可用的查询类型（靶点、疾病、药物、搜索）
- 所有常见操作的示例查询
- 错误处理和最佳实践
- 数据许可和引用要求

**references/evidence_types.md**
证据类型和数据源的综合指南：
- 所有 7 个主要证据类型的详细描述
- 每个来源的评分方法
- 证据解释指南
- 每种证据类型的优势和局限性
- 质量评估建议

**references/target_annotations.md**
完整的靶点注释参考：
- 12 个主要注释类别解释
- 可靶向性评估详情
- 安全隐患来源
- 表达、必要性和约束数据
- 靶点优先排序的解释指南
- 靶点评估的红旗和绿旗

## 数据更新和版本控制

Open Targets 平台**每季度**更新，发布新的数据版本。当前版本（截至 2025 年 10 月）可在 API 端点获得。

**发布信息：** 查看 https://platform-docs.opentargets.org/release-notes 获取最新更新。

**引用：** 使用 Open Targets 数据时，请引用：
Ochoa, D. et al. (2025) Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery. Nucleic Acids Research, 53(D1):D1467-D1477.

## 限制和考虑因素

1. **API 用于探索性查询：** 对于许多靶点/疾病的系统分析，使用数据下载或 BigQuery
2. **评分是相对的，不是绝对的：** 关联评分对证据强度进行排名，但不预测临床成功
3. **研究不足的疾病得分较低：** 新型或罕见疾病可能有强有力的证据，但总评分较低
4. **证据质量各不相同：** 专家策划的来源权重高于计算预测
5. **需要生物学解释：** 评分和证据必须在生物学和临床背景下解释
6. **无需身份验证：** 所有数据均可自由访问，但请适当引用