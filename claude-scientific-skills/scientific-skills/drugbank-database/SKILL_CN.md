---
name: drugbank-database
description: 访问和分析来自 DrugBank 数据库的综合药物信息，包括药物属性、相互作用、靶点、通路、化学结构和药理学数据。当处理药物数据、药物发现研究、药理学研究、药物-药物相互作用分析、靶点识别、化学相似性搜索、ADMET 预测或任何需要来自 DrugBank 的详细药物和药物靶点信息的任务时，应使用此技能。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# DrugBank 数据库

## 概述

DrugBank 是一个全面的生物信息学和化学信息学数据库，包含关于药物和药物靶点的详细信息。此技能使能够对 DrugBank 数据进行编程访问，包括约 9,591 个药物条目（2,037 个 FDA 批准的小分子、241 个生物技术药物、96 个营养保健品和 6,000+ 个实验化合物），每个条目有 200 多个数据字段。

## 核心能力

### 1. 数据访问和身份验证

使用 Python 通过适当的身份验证下载和访问 DrugBank 数据。此技能提供关于以下方面的指导：
- 安装和配置 `drugbank-downloader` 包
- 通过环境变量或配置文件安全地管理凭据
- 下载特定或最新版本的数据库
- 高效地打开和解析 XML 数据
- 使用缓存数据以优化性能

**何时使用**：设置 DrugBank 访问、下载数据库更新、初始项目配置。

**参考**：有关详细身份验证、下载过程、API 访问、缓存策略和故障排除，请参阅 `references/data-access.md`。

### 2. 药物信息查询

从数据库中提取综合药物信息，包括标识符、化学属性、药理学、临床数据和外部数据库的交叉引用。

**查询能力**：
- 通过 DrugBank ID、名称、CAS 号或关键词搜索
- 提取基本药物信息（名称、类型、描述、适应症）
- 检索化学属性（SMILES、InChI、分子式）
- 获取药理学数据（作用机制、药效学、ADME）
- 访问外部标识符（PubChem、ChEMBL、UniProt、KEGG）
- 构建可搜索的药物数据库并导出到 DataFrame
- 按类型过滤药物（小分子、生物技术、营养保健品）

**何时使用**：检索特定药物信息、构建药物数据库、药理学研究、文献综述、药物分析。

**参考**：有关 XML 导航、查询函数、数据提取方法和性能优化，请参阅 `references/drug-queries.md`。

### 3. 药物-药物相互作用分析

分析药物-药物相互作用（DDI），包括机制、临床意义和相互作用网络，用于药物警戒和临床决策支持。

**分析能力**：
- 提取特定药物的所有相互作用
- 构建双向相互作用网络
- 按严重性和机制分类相互作用
- 检查药物对之间的相互作用
- 识别具有最多相互作用的药物
- 分析多药治疗方案的安全性
- 创建相互作用矩阵和网络图
- 在相互作用网络中执行社区检测
- 计算相互作用风险评分

**何时使用**：多药安全性分析、临床决策支持、药物相互作用预测、药物警戒研究、识别禁忌症。

**参考**：有关相互作用提取、分类方法、网络分析和临床应用，请参阅 `references/interactions.md`。

### 4. 药物靶点和通路

访问关于药物-蛋白质相互作用的详细信息，包括靶点、酶、转运蛋白、载体和生物通路。

**靶点分析能力**：
- 提取带有作用（抑制剂、激动剂、拮抗剂）的药物靶点
- 识别代谢酶（CYP450、II 相酶）
- 分析转运蛋白（摄取、外排）用于 ADME 研究
- 将药物映射到生物通路（SMPDB）
- 查找靶向特定蛋白质的药物
- 识别具有共享靶点的药物以用于重新定位
- 分析多药理学和脱靶效应
- 提取靶点的基因本体（GO）术语
- 与 UniProt 交叉引用以获取蛋白质数据

**何时使用**：作用机制研究、药物重新定位研究、靶点识别、通路分析、预测脱靶效应、理解药物代谢。

**参考**：有关靶点提取、通路分析、重新定位策略、CYP450 分析和转运蛋白分析，请参阅 `references/targets-pathways.md`。

### 5. 化学属性和相似性

执行基于结构的分析，包括分子相似性搜索、属性计算、子结构搜索和 ADMET 预测。

**化学分析能力**：
- 提取化学结构（SMILES、InChI、分子式）
- 计算物理化学属性（MW、logP、PSA、氢键）
- 应用 Lipinski 五法则和 Veber 规则
- 计算分子之间的 Tanimoto 相似性
- 生成分子指纹（Morgan、MACCS、拓扑）
- 使用 SMARTS 模式执行子结构搜索
- 查找结构相似的药物以进行重新定位
- 为药物聚类创建相似性矩阵
- 预测口服吸收和血脑屏障渗透性
- 使用 PCA 和聚类分析化学空间
- 导出化学属性数据库

**何时使用**：结构-活性关系（SAR）研究、药物相似性搜索、QSAR 建模、药物相似性评估、ADMET 预测、化学空间探索。

**参考**：有关结构提取、相似性计算、指纹生成、ADMET 预测和化学空间分析，请参阅 `references/chemical-analysis.md`。

## 典型工作流

### 药物发现工作流
1. 使用 `data-access.md` 下载和访问最新的 DrugBank 数据
2. 使用 `drug-queries.md` 构建可搜索的药物数据库
3. 使用 `chemical-analysis.md` 查找相似化合物
4. 使用 `targets-pathways.md` 识别共享靶点
5. 使用 `interactions.md` 检查候选组合的安全性

### 多药安全性分析工作流
1. 使用 `drug-queries.md` 查找患者药物
2. 使用 `interactions.md` 检查所有成对相互作用
3. 使用 `interactions.md` 对相互作用严重性进行分类
4. 使用 `interactions.md` 计算总体风险评分
5. 使用 `targets-pathways.md` 理解相互作用机制

### 药物重新定位研究工作流
1. 使用 `targets-pathways.md` 查找具有共享靶点的药物
2. 使用 `chemical-analysis.md` 查找结构相似的药物
3. 使用 `drug-queries.md` 提取适应症和药理学数据
4. 使用 `interactions.md` 评估潜在的联合治疗

### 药理学研究工作流
1. 使用 `drug-queries.md` 提取感兴趣的药物
2. 使用 `targets-pathways.md` 识别所有蛋白质相互作用
3. 使用 `targets-pathways.md` 映射到生物通路
4. 使用 `chemical-analysis.md` 预测 ADMET 属性
5. 使用 `interactions.md` 识别潜在的禁忌症

## 安装要求

### Python 包
```bash
uv pip install drugbank-downloader  # 核心访问
uv pip install bioversions          # 最新版本检测
uv pip install lxml                 # XML 解析优化
uv pip install pandas               # 数据操作
uv pip install rdkit                # 化学信息学（用于相似性）
uv pip install networkx             # 网络分析（用于相互作用）
uv pip install scikit-learn         # ML/聚类（用于化学空间）
```

### 账户设置
1. 在 go.drugbank.com 创建免费账户
2. 接受许可协议（学术使用免费）
3. 获取用户名和密码凭据
4. 按照 `references/data-access.md` 中的说明配置凭据

## 数据版本和可重复性

始终指定 DrugBank 版本以确保可重复的研究：

```python
from drugbank_downloader import download_drugbank
path = download_drugbank(version='5.1.10')  # 指定确切版本
```

在出版物和分析脚本中记录使用的版本。

## 最佳实践

1. **凭据**：使用环境变量或配置文件，永远不要硬编码
2. **版本控制**：指定确切的数据库版本以确保可重复性
3. **缓存**：缓存解析的数据以避免重新下载和重新解析
4. **命名空间**：解析时正确处理 XML 命名空间
5. **验证**：使用前使用 RDKit 验证化学结构
6. **交叉引用**：使用外部标识符（UniProt、PubChem）进行集成
7. **临床背景**：解释相互作用数据时始终考虑临床背景
8. **许可合规**：确保您的使用案例的适当许可

## 参考文档

所有详细的实现指导都组织在模块化参考文件中：

- **references/data-access.md**：身份验证、下载、解析、API 访问、缓存
- **references/drug-queries.md**：XML 导航、查询方法、数据提取、索引
- **references/interactions.md**：DDI 提取、分类、网络分析、安全性评分
- **references/targets-pathways.md**：靶点/酶/转运蛋白提取、通路映射、重新定位
- **references/chemical-analysis.md**：结构提取、相似性、指纹、ADMET 预测

根据您的具体分析需求加载这些参考。
