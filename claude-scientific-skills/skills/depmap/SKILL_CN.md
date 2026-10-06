---
name: depmap
description: 检索并分析Cancer Dependency Map（DepMap）发行版数据，包括CRISPR Chronos基因效应、癌症模型注释、多组学生物标志物以及PRISM药物敏感性数据。支持癌症选择性依赖性、共必需性（co-essentiality）以及候选合成致死性分析，并带有版本感知的标识符和统计检查。
license: CC-BY-4.0
compatibility: Requires Python 3.10+ with numpy, pandas, and scipy>=1.11 for the bundled helpers. Network access is needed for release discovery; downloading current data may require browser verification through the DepMap portal.
metadata:
  version: "1.2"
  skill-author: Kuan-lin Huang
  last-reviewed: "2026-09-30"
---

# DepMap —— Cancer Dependency Map

## 何时使用

使用此技能对癌症模型中的依赖性进行排序，比较预先指定的生物标志物
队列，检视共必需性，或将遗传依赖性与PRISM化合物反应联系起来。这些
分析会生成靶点和合成致死性假设；它们不能确立临床疗效、治疗窗口或
因果关系。

DepMap整合了Broad和Sanger的CRISPR筛选，并托管独立的RNAi和药物筛选
数据集。请将每个问题与其对应的检测方法和固定的发行版相匹配。RNAi
DEMETER2是一种不同的扰动模式，而不是一种更老的CRISPR评分方法。

## 1. 发现一个发行版，然后获取其文件

使用[DepMap下载页面](https://depmap.org/portal/data_page/)以及所选
发行版的README和发行说明。审查时，实时目录中最新的
`DepMap Public` 发行版是**26Q1**，日期为2026-04-01。在新工作之前请重新
核实；一个发行版名称或预期的季度并不是该发行版可用的证据。

### 经验证的公共端点

`GET https://depmap.org/portal/api/no-captcha/download/files` 返回一个
完整的CSV目录，不需要请求体、API密钥或分页参数。必需的
元数据列是 `release`、`release_date`、`filename` 和 `md5_hash`。
实时响应还有 `url`：**较旧的文件可能有链接，而最近的
发行版行链接为空**。审查时26Q1的全部85个条目的 `url` 值均为空。请逐行
而不是逐端点判断可用性。

[团队公告](https://forum.depmap.org/t/provide-an-open-endpoint-for-latest-version-retrieval/4652)
于2026年7月引入了这个元数据路由。较旧的
`https://depmap.org/portal/api/download/files` 目录可以提供下载链接，但
在审查期间返回了一个HTML验证页面，即使HTTP状态码为200时也是如此。
请在解析之前验证内容。当需要验证时，请通过门户网站获取当前文件。
在使用前立即刷新即将过期的已签名链接；不要编造存储URL，也不要
假设每个新发行版都在Figshare上。

对于之前的 `/api/gene?gene_id=...` 或 `/api/data/gene_dependency` 示例，
没有被验证出受支持的契约。请使用本地的发行版矩阵来获取基因切片。
不要假设一个名为 `depmap` 的Python包就是官方的门户客户端。

从技能的根目录，使用内置的[辅助工具](scripts/depmap_data.py)：

```python
from scripts.depmap_data import fetch_catalogue, select_file, verify_md5

catalogue = fetch_catalogue()
public = catalogue[catalogue["release"].str.startswith("DepMap Public ")]
print(public[["release", "release_date"]].drop_duplicates()
      .sort_values("release_date", ascending=False).head(12))

# 一个明确的示例固定版本；在选择你的发行版之前先检视发现结果的输出。
release = "DepMap Public 26Q1"
record = select_file(catalogue, release, "CRISPRGeneEffect.csv")
print(record[["release", "filename", "md5_hash"]])
# 从门户网站获取此文件之后：
# verify_md5("CRISPRGeneEffect.csv", record["md5_hash"])
```

将选定的元数据、获取日期、发行版引用、本地校验值和README与
分析输出一起保存。将源数据集的使用条款与此技能的许可证分开记录；
较新的发行版条款与较旧的Figshare发行版条款不同。
对于缺失的已发布校验值，保留一个本地的SHA-256值，并明确说明
它未与发布者的校验值进行比较。

## 2. 在连接（join）之前检查文件契约

以下名称已在26Q1目录中得到验证。在将一个文件当作数值矩阵
处理之前，请检查该发行版的README以了解单位和标识符层级。

| 文件 | 用途和重要契约 |
|---|---|
| `CRISPRGeneEffect.csv` | 整合后的、模型层级的Chronos效应；行是ModelID，列保留 `Symbol (EntrezID)` 格式 |
| `CRISPRGeneEffectUncorrected.csv` | 未校正的效应；不能与校正后的效应互换使用 |
| `CRISPRGeneDependency.csv` | 特定于发行版的依赖性统计量；请在README中确认概率/FDR的定义和方向 |
| `Model.csv` | 以 `ModelID` 为键的模型元数据 |
| `ModelCondition.csv` | 以 `ModelConditionID` 为键的生长/处理条件，映射到 `ModelID` |
| `ScreenGeneEffect.csv`、`ScreenSequenceMap.csv`、`CRISPRScreenMap.csv` | 筛选层级的效应和映射；多个筛选可能属于同一个模型 |
| `OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv` | 带有测序/模型元数据和默认条目标志的表达输出；表达计算时要排除元数据列 |
| `OmicsSomaticMutationsMatrixDamaging.csv`、`OmicsSomaticMutationsMatrixHotspot.csv` | 不同的突变注释；损害性突变和热点突变回答的是不同的生物学问题 |
| `OmicsCNGeneWGS.csv`、`OmicsCNGeneMC_WES.csv` | 独立的WGS/WES拷贝数产品；不要将其拼接成一个统一处理的队列 |
| `PortalOmicsCNGeneLog2.csv` | 经转换的门户拷贝数产品；在求逆之前先确定确切的转换方式 |
| `OmicsProfiles.csv`、`Gene.csv` | 多组学溯源/映射和基因注释 |
| `AchillesScreenQCReport.csv`、`AchillesSequenceQCReport.csv` | 筛选/测序质控；应用文档规定的资格规则，而不是自行编造通用的截断值 |

当前的模型注释包括 `CellLineName`、`OncotreeLineage`、
`OncotreePrimaryDisease` 和 `OncotreeSubtype`。旧版 `sample_info.csv`
字段（`DepMap_ID`、`lineage`、`primary_disease`）需要明确的转换。
`Model.csv` 包含没有CRISPR测量数据的模型：在效应矩阵中缺失不等于
一个非依赖性得分。

多组学数据可能以 `SequencingID`、`ModelConditionID` 或 `ModelID` 为索引。
对于基础模型分析，使用该发行版的 `IsDefaultEntryForModel == Yes` 标志，
然后要求每个 `ModelID` 只有一行。条件层级的标志
`IsDefaultEntryForMC` 回答的是一个不同的问题。在从映射表中选择默认值
之前，先对检测方法/数据类型取子集。永远不要对重复的条件取平均值，
也不要在没有明确科学设计的情况下将它们当作独立的模型来计数。

参见[映射指南源码](https://github.com/broadinstitute/depmap-portal/blob/master/frontend/packages/portal-frontend/src/dataPage/components/MapSection.tsx)
和[元数据定义](https://forum.depmap.org/t/depmap-metadata/3694)。

## 3. 解读Chronos并检视一个靶点

Chronos基因效应是连续且无界的。更负的值表示更强的适应性丧失。
在归一化的发行版矩阵中，大约0是非必需对照锚点，-1是常见必需对照
锚点；-1不是一个依赖性边界。诸如≤ -0.5这样的筛选是探索性的，
不是一个p值、FDR或概率截断值。正效应可能反映生长优势或技术噪声，
需要验证。

对于二元判定，请检视所选文件的统计量和方向。高依赖性概率和低FDR
是不同的规则。不要在它们之间悄无声息地转换。使用与发行版匹配的
正/负对照列表和质控输出。参见[评分和质控注意事项](references/dependency_analysis.md)。

以下本地数据示例是示范性的，需要针对你所选的文件实际运行后才有效。
辅助工具的行为已使用合成测试夹具测试过；此次审查期间没有下载当前的
批量矩阵。

```python
from scripts.depmap_data import load_gene_effect, load_models, gene_profile

effects = load_gene_effect("CRISPRGeneEffect.csv")
models = load_models("Model.csv")
profile = gene_profile(effects, models, "KRAS (3845)")
print(profile[["CellLineName", "OncotreeLineage", "gene_effect"]].head(20))

# 检视实际的注释值，然后选择一个确切的队列。
print(profile["OncotreeLineage"].value_counts())
known = profile.dropna(subset=["OncotreeLineage"])
lung = known.loc[known["OncotreeLineage"].eq("Lung"), "gene_effect"]
other = known.loc[~known["OncotreeLineage"].eq("Lung"), "gene_effect"]
if lung.empty or other.empty:
    raise ValueError("两个队列都需要观察到的效应值和已知的谱系")
print({"n_lung": len(lung), "n_other": len(other),
       "other_minus_lung_mean": other.mean() - lung.mean(),
       "lung_fraction_below_exploratory_cutoff": (lung <= -0.5).mean()})
```

这是与其他癌症模型的描述性比较，而不是与正常组织的比较。请保留
分母和缺失值计数。保留完整的基因标签；一个符号可能存在歧义，
该辅助工具会拒绝进行有歧义的符号解析。

## 4. 检验生物标志物关联

1. 在检视靶点得分之前定义好改变类型。一个损害性突变矩阵不能确立
   双等位基因缺失；激活型KRAS热点突变需要一个与通用损害性突变不同
   的定义。
2. 将概况（profile）映射到正确的模型/条件。只有在已检测为阴性时才使用
   `0`，预先指定的生物标志物用 `1`，未知状态则缺失。
3. 限制在科学上可比较的模型范围内（谱系、培养条件、筛选来源以及
   相关患者结构）。在检验之前检视混杂因素。
4. 对计划的基因家族中每一个符合条件的基因都进行检验，然后在选择
   命中结果之前调整其所有的p值。报告组大小、效应量、p值和q值。
5. 用匹配的/同基因（isogenic）扰动以及挽救实验或正交证据来验证候选的
   合成致死性；仅凭关联性是不够的。

```python
import pandas as pd
from scripts.depmap_data import biomarker_scan

# 用户准备好的、与发行版匹配的注释，经过上面的映射和整理之后。
status = pd.read_csv("curated_biomarker_status.csv", index_col="ModelID")["status"]
results = biomarker_scan(effects, status, min_n=5)
# 正的effect_size意味着在生物标志物阳性的模型中依赖性更强。
candidates = results.loc[(results["qval"] < 0.1) & (results["effect_size"] > 0)]
```

这个单侧的Mann–Whitney检验筛选是探索性的，不对协变量进行调整。
`min_n=5` 是一个明确的示例下限，不是一个功效保证。对于跨谱系的
推断，请拟合一个适当的调整模型，并检视谱系内部的效应稳定性；
不要将该辅助工具的q值报告为已经过混杂因素调整。

## 5. 共必需性和药物敏感性

```python
from scripts.depmap_data import coessentiality

correlates = coessentiality(effects, "KRAS (3845)", min_n=500)
print(correlates[["gene", "n", "r", "pval", "qval"]].head(20))
```

`min_n` 是可配置的，应该为该分析预先指定。稀疏的基因可能会以
虚假的相关性主导排名；请始终保留成对的样本计数。该辅助工具使用
成对完整观测值，并跳过常数基因。Pearson/BH输出仍需要谱系、文库
和筛选质量检查；共必需性不是物理相互作用或共享通路的证据。
[DepMap团队的讨论](https://forum.depmap.org/t/crispr-co-depency-top-hits-obscured-by-newly-added-screens/4503)
记录了这种特定的稀疏覆盖失效模式。

对于PRISM，首先选择确切的筛选/发行版和终点。处理信息CSV文件是
注释，不是敏感性数值。最初的主筛选的
`primary-screen-replicate-collapsed-logfold-change.csv` 的反应行以
细胞系 `row_name` 为键，列以处理 `column_name` 为键。连接对应的
细胞系和处理信息文件；保留化合物、剂量和筛选身份信息。较低的
log2倍数变化表示更大的活力丧失。次要筛选的AUC来自剂量-反应曲线
参数，与单剂量的log倍数变化不是同一个量。在加载这些文件之前，
请参见[PRISM工作流程](references/dependency_analysis.md)。

## 验证和来源

报告之前：验证发行版/文件身份、唯一的连接、标识符层级、
完整的基因标签、队列成员身份、缺失情况、筛选资格、评分的
单位/方向、多重检验的族，以及证据是否属于观察性的。表达、
拷贝数和CRISPR可能共享技术混杂因素；低表达并不保证所测得的
分数为零。广泛的必需性为正常细胞/选择性研究提供了动机；但它
本身并不能证明一个靶点是不可成药的。

- [26Q1发行说明](https://forum.depmap.org/t/announcing-the-26q1-release/4606)：文库校正和更新的注释。
- [25Q2发行说明](https://forum.depmap.org/t/announcing-the-25q2-release/4257)：多组学/默认映射以及WGS/WES变化。
- [Chronos上游源码](https://github.com/broadinstitute/chronos)：归一化、拷贝数校正和命中判定定义。
- [Dempster et al., Genome Biology 22:343 (2021)](https://doi.org/10.1186/s13059-021-02540-7)：Chronos方法，PMID 34930405。
- [最初的PRISM Repurposing资源](https://depmap.org/repurposing/)：特定发行版的数据和README。

实时的no-captcha目录和原始的PRISM README都已成功获取。该辅助工具
使用Python urllib，审查时成功；同一个公共端点在使用默认的requests
客户端时返回HTTP 403。请暴露访问失败，而不要将一个错误页面当作数据
处理。
受保护的门户端点返回了验证页面；经认证的下载和针对当前矩阵的
端到端分析仍未得到验证。此次审查并不声称存在一个可用的bearer令牌
API或未文档化的基因查询端点。
