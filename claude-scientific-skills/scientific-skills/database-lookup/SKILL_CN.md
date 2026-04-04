---
name: database-lookup
description: 通过 REST API 搜索 78 个公共科学、生物医学、材料科学和经济数据库并返回结构化 JSON 结果。涵盖物理/天文学（NASA、NIST、SDSS、SIMBAD、系外行星档案）、地球/环境（USGS、NOAA、EPA、OpenWeatherMap）、化学/药物（PubChem、ChEMBL、DrugBank、FDA、KEGG、DailyMed、ZINC、BindingDB）、材料科学（Materials Project、COD）、生物学/基因组学（Reactome、BRENDA、UniProt、STRING、Ensembl、NCBI Gene、GEO、GTEx、PDB、AlphaFold、InterPro、ChEBI、BioGRID、Gene Ontology、QuickGO、NCBI Protein/Taxonomy、dbSNP、SRA、ENA、gnomAD、UCSC Genome、ENCODE、JASPAR、MouseMine、PRIDE、LINCS L1000、Human Protein Atlas、Human Cell Atlas、RummaGEO、Metabolomics Workbench、EMDB、Addgene）、疾病/临床（COSMIC、Open Targets、ClinPGx、ClinicalTrials.gov、OMIM、ClinVar、GDC/TCGA、cBioPortal、DisGeNET、GWAS Catalog、Monarch、HPO）、监管（FDA、USPTO、SEC EDGAR）、经济/金融（FRED、BEA、BLS、Federal Reserve、World Bank、ECB、US Treasury、Alpha Vantage、Data Commons）和人口统计学（US Census、Eurostat、WHO）。当用户想要查找化合物、药物、蛋白质、基因、通路、酶、基因表达、变体、临床试验、专利、SEC  filings、经济指标、晶体结构、天文物体、地震、天气，或任何来自公共数据库 API 的数据时使用此技能。当用户提到任何数据库名称或询问分子特性、药物-靶点相互作用、结合亲和力、蛋白质相互作用、通路成员资格、药物基因组学、经济时间序列、材料特性、商业可用化合物、虚拟筛选、化合物可购买性、化学库、构建模块、癌症基因组学、体细胞突变、肿瘤突变谱、核苷酸序列、基因组组装、测序读数、ENA 登录号、INSDC 数据，或希望跨来源交叉引用实体时也会触发。
metadata:
  skill-author: K-Dense Inc.
---

# 数据库查找

您可以通过 REST API 访问 78 个公共数据库。您的任务是确定哪些数据库与用户的问题相关，查询它们，并返回原始 JSON 结果以及您使用的数据库。

## 核心工作流程

1. **理解查询** — 用户在寻找什么？化合物？基因？通路？专利？表达数据？经济指标？这决定了要访问哪些数据库。

2. **选择数据库** — 使用下面的数据库选择指南。如果不确定，搜索多个数据库 — 宁可广泛撒网也不要错过相关数据。

3. **阅读参考文件** — 每个数据库在 `references/` 目录中都有一个参考文件，包含端点详细信息、查询格式和示例调用。在进行 API 调用之前阅读相关文件。

4. **进行 API 调用** — 请参阅下面的**进行 API 调用**部分，了解在您的平台上使用哪个 HTTP 抓取工具。

5. **返回结果** — 始终返回：
   - 每个数据库的**原始 JSON** 响应
   - **查询的数据库列表**以及使用的特定端点
   - 如果查询返回无结果，明确说明而不是省略

## 数据库选择指南

将用户的意图与正确的数据库匹配。许多查询受益于访问多个数据库。

### 物理与天文学
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 近地天体、小行星 | NASA (NeoWs) | — |
| 火星车图像 | NASA (Mars Rover Photos) | — |
| 系外行星、轨道参数 | NASA Exoplanet Archive | — |
| 按名称/坐标查询天文物体 | SIMBAD | SDSS |
| 星系/恒星光谱、光度测量 | SDSS | SIMBAD |
| 物理常数 | NIST | — |
| 原子光谱、谱线 | NIST (ASD) | — |

### 地球与环境科学
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 地震、地震事件 | USGS Earthquakes | — |
| 水数据、流量、地下水 | USGS Water Services | — |
| 天气（当前、预报、历史） | OpenWeatherMap | NOAA |
| 气候数据、历史气象站 | NOAA (CDO) | — |
| 空气质量、有毒物质排放 | EPA (Envirofacts) | — |

### 化学与药物
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 化合物、分子 | PubChem | ChEMBL |
| 分子特性（重量、分子式、SMILES） | PubChem | — |
| 药物同义词、CAS 编号 | PubChem (synonyms) | DrugBank |
| 生物活性数据、IC50、结合测定 | ChEMBL | BindingDB、PubChem |
| 药物结合亲和力（Ki、IC50、Kd） | ChEMBL、BindingDB | PubChem |
| 药物-靶点相互作用 | ChEMBL、DrugBank | BindingDB、Open Targets |
| 蛋白质靶点的配体（按 UniProt） | BindingDB | ChEMBL |
| 从化合物结构识别靶点 | BindingDB (SMILES 相似性) | ChEMBL |
| 药物标签、不良事件、召回 | FDA (OpenFDA) | DailyMed |
| 药物标签（结构化产品标签） | DailyMed | FDA (OpenFDA) |
| 药物药理学、适应症 | DrugBank | FDA |
| 化学交叉引用 | PubChem (xrefs) | ChEMBL |
| 可用于筛选的商业可用化合物 | ZINC | PubChem |
| 相似性/子结构搜索（可购买） | ZINC | PubChem、ChEMBL |
| 类药物化合物库、构建模块 | ZINC | — |
| FDA 批准的药物结构 | ZINC (fda subset) | PubChem、FDA |
| 化合物可购买性、供应商目录 | ZINC | — |

### 材料科学与晶体学
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 按化学式或元素查询材料 | Materials Project | COD |
| 带隙、电子结构 | Materials Project | — |
| 晶体结构、CIF 文件 | COD | Materials Project |
| 弹性/机械特性 | Materials Project | — |
| 形成能、热力学 | Materials Project | — |
| 晶胞参数、空间群 | COD | Materials Project |

### 生物学与基因组学
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 生物通路 | Reactome、KEGG | — |
| 基因/蛋白质所在的通路 | Reactome (mapping)、KEGG | — |
| 酶动力学、催化活性 | BRENDA | KEGG |
| 代谢组学研究、代谢物谱 | Metabolomics Workbench | PubChem |
| m/z 或精确质量查询 | Metabolomics Workbench (moverz/exactmass) | PubChem |
| 蛋白质序列、功能、注释 | UniProt | Ensembl |
| 蛋白质-蛋白质相互作用 | STRING | BioGRID |
| 基因信息、基因组位置 | NCBI Gene | Ensembl |
| 基因组序列、变体、转录本 | Ensembl | NCBI Gene |
| 基因表达数据集 | GEO (NCBI E-utilities) | — |
| 跨组织的基因表达 | GTEx | Human Protein Atlas |
| 基因表达特征 (CMap/L1000) | LINCS L1000 | GEO |
| 与 GEO 的基因集富集 | RummaGEO | GEO |
| 蛋白质序列 (NCBI) | NCBI Protein | UniProt |
| 分类学分类 | NCBI Taxonomy | — |
| SNP/变体数据 (dbSNP) | dbSNP | ClinVar、gnomAD |
| 群体变体频率 | gnomAD | dbSNP |
| 测序运行元数据 | SRA | ENA、GEO |
| 核苷酸序列（欧洲档案） | ENA | SRA、NCBI Gene |
| 基因组组装、原始读数（欧洲） | ENA | SRA、Ensembl |
| 从序列登录号交叉引用 | ENA (xref) | NCBI Gene、UniProt |
| 基因组注释、轨道 | UCSC Genome Browser | Ensembl |
| 3D 蛋白质结构（实验） | PDB (RCSB) | EMDB |
| 3D 蛋白质结构（预测） | AlphaFold DB | PDB |
| EM 图、冷冻电镜结构 | EMDB | PDB |
| 蛋白质家族、结构域 | InterPro | UniProt |
| 化学实体（生物） | ChEBI | PubChem |
| 蛋白质/遗传相互作用 | BioGRID | STRING |
| 基因功能注释（GO 术语） | QuickGO | Gene Ontology |
| 调控元件、ChIP-seq、ATAC-seq | ENCODE | — |
| TF 结合谱/基序 | JASPAR | ENCODE |
| 跨组织的蛋白质表达 | Human Protein Atlas | UniProt |
| 单细胞图谱项目 | Human Cell Atlas | — |
| 蛋白质组学数据集 | PRIDE | — |
| 小鼠基因数据 | MouseMine | NCBI Gene |
| 质粒库 | Addgene | — |

**生物体/物种很重要**。大多数生物学数据库涵盖多种生物体。如果用户的查询是关于特定生物体的，明确传递它 — 不要假设人类。常见模式：Ensembl 在 URL 路径中使用 `{species}`（例如 `homo_sapiens`），STRING/BioGRID/QuickGO 使用 NCBI 分类 ID（人类 `species=9606`，小鼠 `10090`），UniProt 在搜索查询中使用 `organism_id:9606`，KEGG 使用生物体代码（`hsa`、`mmu`）。GTEx 和 Human Protein Atlas 仅适用于人类。检查每个数据库的参考文件以获取特定参数。

### 疾病与临床
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 癌症中的体细胞突变 | COSMIC | Open Targets、cBioPortal |
| 癌症基因组学 (TCGA) | GDC (TCGA) | COSMIC、cBioPortal |
| 癌症研究突变、CNA、表达 | cBioPortal | GDC (TCGA)、COSMIC |
| 肿瘤临床数据（生存、分期） | cBioPortal | GDC (TCGA) |
| 药物-靶点-疾病关联 | Open Targets | ChEMBL |
| 基因-疾病关联 | DisGeNET | Open Targets、Monarch |
| 孟德尔疾病-基因关系 | OMIM | NCBI Gene |
| 变体临床意义 | ClinVar (NCBI) | OMIM |
| GWAS SNP-性状关联 | GWAS Catalog | — |
| 疾病-表型-基因链接 | Monarch Initiative | HPO |
| 表型本体、HPO 术语 | HPO | Monarch |
| 药物基因组学、药物-基因相互作用 | ClinPGx (PharmGKB) | DrugBank |
| 药物/疾病的临床试验 | ClinicalTrials.gov | FDA |
| 疾病相关表达数据 | GEO | Open Targets |

### 专利与监管
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 按关键词或技术查询专利 | USPTO (PatentsView) | — |
| 按发明人或受让人查询专利 | USPTO (PatentsView) | — |
| 专利审查状态 | USPTO (PEDS) | — |
| 商标查询 | USPTO (TSDR) | — |
| SEC 公司文件、10-K、10-Q | SEC EDGAR | — |

### 经济与金融
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 美国经济时间序列（GDP、CPI、利率） | FRED | BEA |
| 就业、工资、劳工统计 | BLS | FRED |
| GDP、国民账户 | BEA | FRED、World Bank |
| 国际发展指标 | World Bank | FRED |
| 利率、货币供应量 | Federal Reserve | FRED |
| 欧元汇率、ECB 货币统计 | ECB | — |
| 美国债务、收益率曲线、财政数据 | US Treasury | FRED |
| 股票价格、外汇、加密货币 | Alpha Vantage | — |
| 多个主题的统计数据 | Data Commons | — |

### 社会科学与人口统计学
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 美国人口、住房、收入数据 | US Census | Data Commons |
| 欧盟统计数据（经济、贸易、健康） | Eurostat | World Bank |
| 全球健康指标（死亡率、疾病） | WHO GHO | World Bank |

### 跨领域查询
| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 关于化合物的一切 | PubChem + ChEMBL + DrugBank | BindingDB、ZINC、Reactome、FDA |
| 关于基因的一切 | NCBI Gene + UniProt + Ensembl | Reactome、STRING、COSMIC、cBioPortal、ENA |
| 关于变体的一切 | dbSNP + ClinVar + gnomAD | GWAS Catalog、COSMIC、cBioPortal |
| 药物靶点通路 | ChEMBL + Reactome | Open Targets、GEO |
| 化学发明的现有技术 | USPTO + PubChem | ChEMBL |
| 关于材料的一切 | Materials Project + COD | — |
| 美国经济概览 | FRED + BLS + BEA | Federal Reserve |

当用户的查询跨越多个领域时（例如，"我们对阿司匹林了解多少"或"查找关于 BRCA1 的一切"），并行查询所有相关数据库。

## 常见标识符格式

不同的数据库使用不同的标识符系统。如果查询失败，标识符格式可能错误。以下是快速参考：

| 标识符 | 格式 | 示例 | 使用数据库 |
|---|---|---|---|
| UniProt 登录号 | `P#####` 或 `Q#####` | `P04637` (TP53) | UniProt、STRING、AlphaFold、Reactome mapping |
| Ensembl 基因 ID | `ENSG###########` | `ENSG00000141510` | Ensembl、Open Targets、GTEx |
| NCBI Gene ID | 整数 | `7157` (TP53) | NCBI Gene、GEO、DisGeNET、HPO |
| HGNC ID | `HGNC:#####` | `HGNC:11998` | Monarch |
| PubChem CID | 整数 | `2244` (阿司匹林) | PubChem |
| ZINC ID | `ZINC` + 15 位数字 | `ZINC000000000053` (阿司匹林) | ZINC |
| ENA 项目 | `PRJEB` + 数字 | `PRJEB40665` | ENA |
| ENA 运行 | `ERR` + 数字 | `ERR1234567` | ENA |
| ENA 实验 | `ERX` + 数字 | `ERX1234567` | ENA |
| ENA 样本 | `ERS` + 数字 | `ERS1234567` | ENA |
| ChEMBL ID | `CHEMBL####` | `CHEMBL25` (阿司匹林) | ChEMBL |
| Reactome 稳定 ID | `R-HSA-######` | `R-HSA-109581` | Reactome |
| HP 术语 | `HP:#######` | `HP:0001250` (癫痫) | HPO (URL 编码冒号为 %3A) |
| MONDO 疾病 | `MONDO:#######` | `MONDO:0007947` | Monarch |
| GO 术语 | `GO:#######` | `GO:0008150` | QuickGO、Gene Ontology |
| dbSNP rsID | `rs########` | `rs334` | dbSNP、GWAS Catalog、gnomAD |
| GENCODE ID | `ENSG###.##` (版本化) | `ENSG00000139618.17` | GTEx (需要版本后缀) |

### 标识符解析

当数据库不识别标识符时，使用以下工作流程进行转换：

**基因**：符号（例如 "TP53"）→ 在 **NCBI Gene** 中查找（通过符号 esearch）→ 获取 NCBI Gene ID → 通过 **Ensembl** `/xrefs/symbol/homo_sapiens/{symbol}` 转换为 Ensembl ID，或通过 **UniProt** 搜索（`gene_exact:{symbol} AND organism_id:9606`）转换为 UniProt 登录号。

**化合物**：名称 → **PubChem** `/compound/name/{name}/cids/JSON` → 获取 CID → 通过 **UniChem** 或 **ChEMBL** 分子搜索转换为 ChEMBL ID。如果名称查找失败，尝试 SMILES、InChIKey 或 CAS 编号。

**变体**：rsID（例如 "rs334"）直接适用于 **dbSNP**、**ClinVar**、**GWAS Catalog**、**gnomAD**。对于基因组坐标，使用 **Ensembl** VEP 获取结果注释和链接的 rsID。

**疾病**：名称 → **Open Targets** 或 **Monarch** 搜索 → 获取 EFO 或 MONDO ID → 用于下游查询。

## 仅 POST API

这些数据库需要 HTTP POST 并且**不能与 WebFetch 一起使用**（仅 GET）。请改用平台的 shell 工具通过 `curl`：

| 数据库 | 需要 POST 的原因 | 示例 |
|---|---|---|
| Open Targets | GraphQL 端点 | `curl -X POST -H "Content-Type: application/json" -d '{"query":"..."}' https://api.platform.opentargets.org/api/v4/graphql` |
| gnomAD | GraphQL 端点 | `curl -X POST -H "Content-Type: application/json" -d '{"query":"..."}' https://gnomad.broadinstitute.org/api` |
| RummaGEO | 仅 POST 富集 | `curl -X POST -H "Content-Type: application/json" -d '{"genes":["..."]}' https://rummageo.com/api/enrich` |
| GDC/TCGA | 复杂过滤查询 | `curl -X POST -H "Content-Type: application/json" -d '{"filters":...}' https://api.gdc.cancer.gov/ssms` |
| SEC EDGAR | 需要 User-Agent 头 | `curl -H "User-Agent: YourApp you@email.com" https://efts.sec.gov/LATEST/search-index?q=...` |

## API 密钥和访问限制

一些数据库需要 API 密钥或有访问限制。当需要 API 密钥时：

1. **首先检查当前环境** — 密钥可能已经作为 shell 环境变量导出（例如 `$FRED_API_KEY`）。直接从环境中读取它。
2. **回退到 `.env`** — 如果变量不在环境中，检查当前工作目录中的 `.env` 文件。
3. **如果两者都没有** — 在没有密钥的情况下继续（大多数 API 仍以较低的速率限制工作），并告诉用户缺少哪个密钥以及如何获取。

### 需要 API 密钥的数据库（免费注册）

| 数据库 | 环境变量 | 注册 URL |
|---|---|---|
| FRED | `FRED_API_KEY` | https://fred.stlouisfed.org/docs/api/api_key.html |
| BEA | `BEA_API_KEY` | https://apps.bea.gov/API/signup/ |
| BLS | `BLS_API_KEY` | https://data.bls.gov/registrationEngine/ |
| NCBI (GEO, Gene) | `NCBI_API_KEY` | https://www.ncbi.nlm.nih.gov/account/settings/ |
| OpenFDA | `OPENFDA_API_KEY` | https://open.fda.gov/apis/authentication/ |
| USPTO (PatentsView) | `PATENTSVIEW_API_KEY` | https://patentsview.org/apis/keyrequest |
| Data Commons | `DATACOMMONS_API_KEY` | Google Cloud Console |
| Materials Project | `MP_API_KEY` | https://materialsproject.org (免费账户) |
| NASA | `NASA_API_KEY` | https://api.nasa.gov (免费，提供 DEMO_KEY) |
| NOAA (CDO) | `NOAA_API_KEY` | https://www.ncdc.noaa.gov/cdo-web/token |
| OpenWeatherMap | `OPENWEATHERMAP_API_KEY` | https://openweathermap.org/appid |
| OMIM | `OMIM_API_KEY` | https://omim.org/api (免费学术) |
| BioGRID | `BIOGRID_API_KEY` | https://webservice.thebiogrid.org (免费) |
| Alpha Vantage | `ALPHAVANTAGE_API_KEY` | https://www.alphavantage.co/support/#api-key |
| US Census | `CENSUS_API_KEY` | https://api.census.gov/data/key_signup.html |
| DisGeNET | `DISGENET_API_KEY` | https://www.disgenet.org (免费学术) |
| Addgene | `ADDGENE_API_KEY` | https://www.addgene.org (免费账户) |
| LINCS L1000 (CLUE) | `CLUE_API_KEY` | https://clue.io (免费学术) |

这些都是免费获取的。API 在没有密钥的情况下也能工作，但速率限制较低。始终首先尝试使用密钥 — 如果环境变量未设置，在没有密钥的情况下继续，并在响应中注意速率限制可能较低。

### 付费或受限访问的数据库

| 数据库 | 限制 | 免费替代方案 |
|---|---|---|
| DrugBank | 需要付费 API 许可证 | 改用 **ChEMBL** + **PubChem** + **OpenFDA** |
| COSMIC | 需要免费学术注册（JWT 认证） | 使用 **Open Targets** 获取癌症突变数据 |
| BRENDA | 需要免费注册（SOAP，非 REST） | 使用 **KEGG** 获取酶/通路数据 |

当数据库需要用户尚未设置的付费访问或注册时：
1. **回退到可以回答相同问题的免费替代方案**
2. **告诉用户**您无法访问哪个数据库，原因是什么，以及您使用了什么替代方案
3. 如果用户特别请求受限数据库，解释访问要求以便他们可以设置

### 加载 API 密钥

**步骤 1 — 检查当前环境**。密钥可能已经作为 shell 变量导出。例如，在 Claude Code 中，您可以使用 Bash 检查：`echo $FRED_API_KEY`。如果变量已设置且非空，使用它。

**步骤 2 — 检查 `.env` 文件**。如果环境变量未设置，从当前工作目录读取 `.env`。格式：
```
FRED_API_KEY=your_key_here
BEA_API_KEY=your_key_here
```

**步骤 3 — 继续无密钥**。如果两个源都没有密钥，在没有密钥的情况下继续（大多数 API 仍以较低的速率限制工作），并向用户提及这一点。

## 进行 API 调用

使用环境的 HTTP 抓取工具调用 REST 端点。工具名称因平台而异：

| 平台 | HTTP 抓取工具 | 回退 |
|---|---|---|
| Claude Code | `WebFetch` | `curl` via Bash |
| Gemini CLI | `web_fetch` | `curl` via shell |
| Windsurf | `read_url_content` | `curl` via terminal |
| Cursor | 无专用抓取工具 | `curl` via `run_terminal_cmd` |
| Codex CLI | 无专用抓取工具 | `curl` via `shell` |
| Cline | 无专用抓取工具 | `curl` via `execute_command` |

如果您不认识您的平台或抓取工具失败，回退到通过任何可用的 shell/终端工具使用 `curl`。示例：
```bash
curl -s -H "Accept: application/json" "https://api.example.com/endpoint"
```

### 请求指南

- 在支持的地方设置 `Accept: application/json` 头
- URL 编码查询参数中的特殊字符 — SMILES 字符串（`/`、`#`、`=`、`@`）、带括号的化合物名称和带冒号的本体术语（`HP:0001250` → `HP%3A0001250`）是常见的失败原因。使用 `curl` 时，为安全起见使用 `--data-urlencode`。
- **并行 OK**：查询*不同*数据库时（例如，PubChem + ChEMBL + Reactome），并行运行它们 — 大多数 API 具有慷慨的速率限制。
- **序列化对速率限制 API 的请求**：NCBI API（Gene、GEO、Protein、Taxonomy、dbSNP、SRA）无密钥时 3 req/sec，有密钥时 10 req/sec。还需注意：Ensembl（15 req/sec）、BLS v1（无密钥 25 req/天）、SEC EDGAR（10 req/sec）、NOAA（带令牌 5 req/sec）。
- 如果收到速率限制错误（HTTP 429 或 503），短暂等待并重试一次

### 错误恢复

如果 API 返回错误或空结果：
1. **检查标识符格式** — 使用上面的常见标识符格式表。基因符号可能需要首先转换为 NCBI Gene ID 或 Ensembl ID。
2. **尝试替代标识符** — 如果化合物名称在 PubChem 中失败，尝试 SMILES、InChIKey 或 CID。如果基因符号失败，尝试 NCBI Gene ID。
3. **尝试不同的数据库** — 如果一个数据库宕机或返回无结果，检查选择指南中的"也可考虑"列获取替代方案。
4. **报告失败** — 告诉用户哪个数据库失败，错误是什么，以及您尝试了什么替代方案。

### 分页

许多 API 返回分页结果 — 如果您只读取第一页，可能会错过数据。常见模式：

- **Offset/Limit**：`offset=0&limit=100` → 为下一页按 limit 增加 offset（ChEMBL、FRED、NOAA、USGS、NCBI E-utilities、ENA、GDC、FDA）
- **基于游标**：响应包含 `nextPageToken` 或 `cursor` 值 — 在下次请求中传递它（ClinicalTrials.gov、UniProt）
- **页码**：`page=1&per_page=50` → 增加页码（World Bank、cBioPortal、ZINC）

检查每个数据库的参考文件以获取特定的分页参数。如果响应包含 `total`、`totalCount` 或 `next`，且返回的结果数量小于总数，则还有更多页面。

对于目标查找（单个基因、单个化合物），第一页通常足够。当用户需要全面结果时（例如，"X 的所有临床试验"或"基因 Y 中的所有已知变体"），进行分页。

## 输出格式

按以下结构组织您的响应：

```
## 已查询数据库
- **PubChem** — /compound/name/aspirin/property/...
- **Reactome** — /search/query?query=aspirin

## 结果

### PubChem
[原始 JSON 响应]

### Reactome
[原始 JSON 响应]
```

如果结果非常大，展示最相关的部分并注意还有更多数据可用。但默认显示完整的原始 JSON — 用户要求了它。

## 添加新数据库

此技能设计为可扩展。每个数据库都是 `references/` 中的自包含参考文件。要添加新数据库：

1. 创建 `references/<database-name>.md`，遵循与现有文件相同的格式
2. 在上面的数据库选择指南中添加条目
3. 参考文件应包括：基础 URL、关键端点、查询参数格式、示例调用、速率限制和响应结构

## 可用数据库

在进行任何 API 调用之前，请阅读相关参考文件。

### 物理与天文学
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| NASA | `references/nasa.md` | NEO 小行星、火星车、APOD |
| NASA Exoplanet Archive | `references/nasa-exoplanet-archive.md` | 系外行星、轨道参数 |
| NIST | `references/nist.md` | 物理常数、原子光谱 |
| SDSS | `references/sdss.md` | 星系/恒星光谱、光度测量 |
| SIMBAD | `references/simbad.md` | 天文物体目录 |

### 地球与环境科学
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| USGS | `references/usgs.md` | 地震、水数据 |
| NOAA | `references/noaa.md` | 气候、气象站数据 |
| EPA | `references/epa.md` | 空气质量、有毒物质排放 |
| OpenWeatherMap | `references/openweathermap.md` | 天气当前/预报 |

### 化学与药物
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| PubChem | `references/pubchem.md` | 化合物、特性、同义词 |
| ChEMBL | `references/chembl.md` | 生物活性、药物发现 |
| DrugBank | `references/drugbank.md` | 药物数据、相互作用（付费） |
| FDA (OpenFDA) | `references/fda.md` | 药物标签、不良事件、召回 |
| DailyMed | `references/dailymed.md` | 药物标签 (NIH/NLM) |
| KEGG | `references/kegg.md` | 通路、基因、化合物 |
| ChEBI | `references/chebi.md` | 生物相关化学实体 |
| ZINC | `references/zinc.md` | 商业可用化合物、虚拟筛选 |
| BindingDB | `references/bindingdb.md` | 实验测量的结合亲和力 |

### 材料科学
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| Materials Project | `references/materials-project.md` | 带隙、弹性特性、晶体结构 |
| COD | `references/cod.md` | 晶体结构、CIF 文件 |

### 生物学与基因组学
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| Reactome | `references/reactome.md` | 生物通路、反应 |
| BRENDA | `references/brenda.md` | 酶动力学、催化（SOAP） |
| UniProt | `references/uniprot.md` | 蛋白质序列、功能 |
| STRING | `references/string.md` | 蛋白质-蛋白质相互作用 |
| Ensembl | `references/ensembl.md` | 基因组、变体、序列 |
| NCBI Gene | `references/ncbi-gene.md` | 基因信息、链接 |
| NCBI Protein | `references/ncbi-protein.md` | 蛋白质序列、记录 |
| NCBI Taxonomy | `references/ncbi-taxonomy.md` | 分类学分类 |
| GEO (NCBI) | `references/geo.md` | 基因表达数据集 |
| GTEx | `references/gtex.md` | 跨组织的基因表达 |
| PDB | `references/pdb.md` | 蛋白质 3D 结构 |
| AlphaFold DB | `references/alphafold.md` | 预测的蛋白质结构 |
| EMDB | `references/emdb.md` | 电子显微镜图 |
| InterPro | `references/interpro.md` | 蛋白质家族、结构域 |
| BioGRID | `references/biogrid.md` | 蛋白质/遗传相互作用 |
| Gene Ontology | `references/gene-ontology.md` | GO 术语、基因注释 |
| QuickGO | `references/quickgo.md` | GO 注释（EBI，推荐） |
| dbSNP | `references/dbsnp.md` | SNP/变体数据 |
| SRA | `references/sra.md` | 测序运行元数据 |
| gnomAD | `references/gnomad.md` | 群体变体频率（POST） |
| UCSC Genome Browser | `references/ucsc-genome.md` | 基因组注释、轨道 |
| ENCODE | `references/encode.md` | DNA 元素、ChIP-seq、ATAC-seq |
| JASPAR | `references/jaspar.md` | TF 结合谱/基序 |
| Human Protein Atlas | `references/human-protein-atlas.md` | 跨组织的蛋白质表达 |
| Human Cell Atlas | `references/hca.md` | 单细胞图谱数据 |
| LINCS L1000 | `references/lincs-l1000.md` | 基因表达特征 (CMap) |
| RummaGEO | `references/rummageo.md` | GEO 基因集富集（POST） |
| PRIDE | `references/pride.md` | 蛋白质组学数据存储库 |
| Metabolomics Workbench | `references/metabolomics-workbench.md` | 代谢组学研究、代谢物 |
| MouseMine | `references/mousemine.md` | 小鼠基因组信息学 |
| ENA | `references/ena.md` | 核苷酸序列、读数、组装、分类学 (EMBL-EBI) |
| Addgene | `references/addgene.md` | 质粒库 |

### 疾病与临床
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| Open Targets | `references/opentargets.md` | 靶点-疾病关联（POST） |
| COSMIC | `references/cosmic.md` | 癌症中的体细胞突变 |
| ClinPGx (PharmGKB) | `references/clinpgx.md` | 药物基因组学 |
| ClinicalTrials.gov | `references/clinicaltrials.md` | 临床试验注册 |
| OMIM | `references/omim.md` | 孟德尔疾病-基因数据 |
| ClinVar | `references/clinvar.md` | 变体临床意义 |
| GDC (TCGA) | `references/tcga-gdc.md` | 癌症基因组学、突变（POST） |
| cBioPortal | `references/cbioportal.md` | 癌症研究突变、CNA、表达、临床数据 |
| DisGeNET | `references/disgenet.md` | 基因-疾病关联 |
| GWAS Catalog | `references/gwas-catalog.md` | GWAS SNP-性状关联 |
| Monarch Initiative | `references/monarch.md` | 疾病-表型-基因链接 |
| HPO | `references/hpo.md` | 人类表型本体 |

### 专利与监管
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| USPTO | `references/uspto.md` | 专利、商标 |
| SEC EDGAR | `references/sec-edgar.md` | 公司文件（需要 User-Agent 头） |

### 经济与金融
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| FRED | `references/fred.md` | 美国经济时间序列 |
| Federal Reserve | `references/federal-reserve.md` | 货币/金融数据 |
| BEA | `references/bea.md` | GDP、国民账户 |
| BLS | `references/bls.md` | 就业、工资、CPI |
| World Bank | `references/worldbank.md` | 发展指标 |
| ECB | `references/ecb.md` | 欧元汇率、货币统计 |
| US Treasury | `references/treasury.md` | 债务、收益率曲线、财政数据 |
| Alpha Vantage | `references/alphavantage.md` | 股票、外汇、加密货币 |
| Data Commons | `references/datacommons.md` | 统计知识图谱 |

### 社会科学与人口统计学
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| US Census | `references/census.md` | 人口、住房、经济调查 |
| Eurostat | `references/eurostat.md` | 欧盟统计数据 |
| WHO GHO | `references/who.md` | 全球健康指标 |