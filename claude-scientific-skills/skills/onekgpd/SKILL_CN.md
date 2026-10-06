---
name: onekgpd
description: >
  在个体参与者层面查询千人基因组计划（1000 Genomes Project）数据集（3,202 名
  全基因组测序个体，GRCh38）。
  当问题涉及千人基因组计划队列中的个体或变异时使用：哪些个体在某个基因或区域中
  携带符合特定条件的变异、哪些个体在某个位置为纯合参考型、数据集中或指定个体在
  某个基因或区域中存在哪些变异，以及两个指定个体之间的亲缘关系。
  返回的变异附带千人基因组等位基因频率（AF）、gnomAD v4.1 外显子组和基因组 AF、
  AlphaMissense 评分以及 HGVSp 注释。
license: MIT
compatibility: Requires Python >=3.11. Variant and sample queries require outbound network access to the public 1000 Genomes query endpoint over TLS; the sample/population metadata commands run fully offline over a data file bundled in the skill. No credentials, API keys, or environment variables are used.
allowed-tools: Write Bash
metadata:
  version: "1.4"
  last-reviewed: "2026-09-30"
  upstream-version: "dnaerys 0.2.1; proto R1.20.0"
  skill-author: Dnaerys
---

# OneKGPd：基于千人基因组计划的个体层面查询

## 范围

本技能查询千人基因组计划数据集——即由 3,202 名全基因组测序个体组成的扩展高覆盖度队列，
基于 GRCh38 组装版本。所有结果均来自该队列，本技能返回的样本名称（例如
`HG00096` 或 `NA21130`）标识其参与者。

查询基于该队列的逐个体基因型数据进行解析。这支持两类互补的问题：选择某区域内携带的
**变异**（在整个队列中或在指定的个体集合中），以及选择携带符合给定条件变异的
**个体**。变异选择可以按等位基因频率、预测后果、临床意义、AlphaMissense 分类以及下文
列出的其他注释维度进行过滤。还可以查询两个指定个体之间的亲缘关系。

变异的携带基因型状态——杂合或纯合——是查询可以指定的条件；结果以变异或样本名称的形式
返回，而不是原始基因型。

公共服务为 **TLS gRPC，地址 `db.dnaerys.org:443`**，通过
`dnaerys 0.2.1`（Python 3.11+）访问；它不是 REST 基础 URL。所维护的服务快照声明使用
VEP 115 / GENCODE 49、ClinVar 202502 和 gnomAD 4.1。这些是该服务所用的注释版本，而不是
各上游资源的最新版本。解释结果时请记录这些版本。

## 何时使用

**在以下情况下使用本技能：**

-   在整个队列中查找某个区域或区域集合内携带的、符合特定条件的**变异**
    （`select-variants`）。
-   在特定个体集合中查找某个区域或区域集合内携带的、符合特定条件的**变异**
    （`select-variants-in-samples`）。
-   查找**哪些千人基因组个体**在某个区域或区域集合内携带符合特定条件的变异
    （`select-samples`）。
-   统计携带特定变异的个体数量（`count-samples`）。
-   将任何变异查询限制为**仅杂合或仅纯合**携带，或同时查询两者（默认）。
-   识别在单个位置上为**纯合参考型**的个体
    （`select-samples-hom-ref`）。
-   确定两个指定千人基因组个体之间的**亲缘关系**——包括亲缘度（双胞胎 / 一级 / 二级 /
    三级 / 无亲缘关系）和 KING 亲缘系数（`kinship`）。
-   获取**数据集总量**——样本数、性别构成、变异数、组装版本
    （`dataset-info`）。
-   变异选择可以按 KGP 等位基因频率、gnomAD 4.1 外显子组和
    gnomAD 4.1 基因组等位基因频率、AlphaMissense 评分和 AlphaMissense 类别、
    ClinVar 临床意义（202502）以及 VEP 注释（影响、生物类型、特征类型、
    变异类别、后果）进行指定。

**请勿将本技能用于：**

-   将基因符号、rsID 或转录本解析为坐标，或获取参考序列。请先解析坐标（参见下文的
    坐标来源），再用解析得到的 GRCh38 区域查询本技能。
-   千人基因组计划以外的任何队列——本技能仅服务于该数据集。

## 前提条件

1.  **`uv`**：本技能的脚本通过 `uv run` 运行，它会读取脚本内联的依赖元数据并创建一个
    临时环境。请确保已安装 `uv` 且其位于 PATH 中（https://docs.astral.sh/uv/）。
2.  **数据使用条款**：千人基因组计划数据是开放的；用户应了解千人基因组计划 / IGSR 的
    数据使用条款（https://www.internationalgenome.org/data）。
3.  **访问约束**：无需配置 API 密钥、`.env` 文件或速率限制令牌。
4.  **超时**：网络命令默认对每次 RPC 使用 `--timeout 30` 秒。
    允许使用正的有限值进行覆盖。分页会发起多次 RPC，且可重试的失败会将整个获取过程
    重试最多三次，因此这并不是整个命令的截止时间。

## 核心规则

-   **使用封装脚本**：始终执行所提供的辅助脚本，而不是自行构造客户端调用或网络请求。
    变异/样本/亲缘关系查询请使用 `scripts/onekgpd_api.py`（它负责处理连接、流式传输、
    分页和 JSON 序列化），样本/群体元数据请使用
    `scripts/onekgpd_meta.py`（离线，参见
    [样本与群体元数据](#sample--population-metadata-offline)）。
-   **坐标必须首先根据权威来源进行解析**——参见
    [坐标来源](#coordinate-provenance-mandatory-first-step)。这是强制性的，而非建议。
-   **先计数再选择**：每个变异和样本选择命令都有一个配对的计数命令。请**先**调用计数
    命令以评估结果集大小，仅当数量可控时再进行选择。
-   **合子型默认包含两者**：选择和计数命令默认同时包含杂合和纯合携带。当问题仅针对
    其中一种状态时，用 `--het-only` 或 `--hom-only` 缩小范围。（要获取两者无需传递任何
    参数。）
-   **输出**：脚本将完整 JSON 写入文件（`--output`，默认位于 `/tmp/` 下），并向 stdout
    打印简明摘要。不要将大型 JSON 文件读入上下文——请使用 `jq` 或一个小型一次性
    `uv run python` 代码片段提取字段。`--page-size` 会获取所有分页，但会把全部变异累积在
    内存中；它不是内存受限的导出方式。请先评估查询规模。
-   **检查完整性**：`result_incomplete=true` 表示结果无法支持确定的“零/不存在”结论。
    请在服务恢复后重新运行。对于有上限的变异选择，`truncated=true` 表示已达到上限，可能
    还有更多记录，即使集群结果本身是完整的。

## 坐标来源（强制性第一步）

在任何基于区域的查询之前，请根据权威来源（例如 Ensembl 或 NCBI）将基因或特征解析为
**GRCh38** 坐标，并使用这些解析后的坐标进行查询。输入为 **1-based、闭区间**：BED 区间
`[start0, end0)` 对应 `start=start0+1, end=end0`。请记录来源登录号、注释版本和获取日期；
即使在同一组装版本上，基因边界也可能因注释版本而异。必须明确组装版本，且基因范围在使用
前必须解析为精确位置。这是结构性要求，而非建议：数据源端没有任何防护机制能捕获错误放置
的区域，因此未经验证的坐标会在不报错的情况下产生非预期位置的结果。

```bash
# 首先使用权威来源将基因符号解析为 GRCh38 区域，
# 然后将经过验证的坐标传给下面的 OneKGPd 查询。
```

> [!CAUTION]
> 本数据集为 GRCh38。GRCh37 坐标，或任何未在 GRCh38 上正确对应目标特征的区域，都会在
> 不报错的情况下返回非预期位置的结果。查询前请核实组装版本和解析后的坐标。

## 命令选择指南

将问题与命令相匹配。计数命令开销很小，应在对应的选择命令之前执行。

-   哪些个体在某区域内携带匹配的变异 → `count-samples`
    然后 `select-samples`
-   某区域内在整个队列中携带哪些变异 → `count-variants`
    然后 `select-variants`
-   某区域内在指定个体集合中携带哪些变异 →
    `count-variants-in-samples` 然后 `select-variants-in-samples`
-   谁在单个位置上为纯合参考型 → `count-samples-hom-ref`
    然后 `select-samples-hom-ref`
-   两个指定个体之间的亲缘关系（亲缘度 + 系数）→
    `kinship`
-   数据集总量（样本数、性别构成、变异总数、组装版本）→
    `dataset-info`

## 队列解读

3,202 个样本的队列包含亲属：额外的 698 个高覆盖度样本扩展了原有的 2,504 样本面板。
因此，携带者计数并不是独立观测的计数，队列 AF 也不是群体患病率估计值。对于关联或频率
比较，请记录所选群体和亲缘关系处理策略；在选择或审核分析集时，请使用随附的家系元数据和
`kinship`。参见
[IGSR 队列公告](https://www.internationalgenome.org/announcements/3202-samples-at-high-coverage-from-NYGC/)。

## 注释过滤器（变异与样本选择/计数共用）

所有变异和样本选择命令（`count-variants`、
`select-variants`、它们的 `-in-samples` 形式、`count-samples`、`select-samples`）
都接受相同的注释过滤器。不同过滤字段之间以 **AND** 组合；同一字段内的多个值以 **OR**
组合。枚举值不区分大小写（例如 `missense_variant` 或 `MISSENSE_VARIANT`）。

这些是在服务器端应用的选择条件。所选变异返回的字段列于
[返回变异的命令](#variant-returning-commands)；用于过滤的条件不一定会在返回的变异中
回显。

-   `--af-lt` / `--af-gt`：千人基因组数据集等位基因频率上下界
-   `--gnomad-exomes-af-lt` / `--gnomad-exomes-af-gt`：gnomAD v4.1 外显子组 AF 上下界
-   `--gnomad-genomes-af-lt` / `--gnomad-genomes-af-gt`：gnomAD v4.1 基因组 AF 上下界
-   `--clin-significance`：ClinVar 临床意义术语，CSV（例如 `PATHOGENIC,LIKELY_PATHOGENIC`）
-   `--consequence`：序列本体（Sequence Ontology）后果术语，CSV（例如 `MISSENSE_VARIANT,STOP_GAINED`）
-   `--impact`：VEP 影响，CSV（`HIGH,MODERATE,LOW,MODIFIER`）
-   `--variant-type`、`--feature-type`、`--bio-type`：SO 变异类别 / VEP 特征 / VEP 生物类型，CSV
-   `--alpha-missense-class`：`AM_LIKELY_BENIGN,AM_LIKELY_PATHOGENIC,AM_AMBIGUOUS`（CSV）
-   `--alpha-missense-score-lt` / `--alpha-missense-score-gt`：AlphaMissense 评分上下界
-   `--biallelic-only` / `--multiallelic-only`
-   `--exclude-males` / `--exclude-females`
-   `--min-len-bp` / `--max-len-bp`：替代等位基因长度上下界（bp）

> [!NOTE]
> `--alpha-missense-class` 与 `--alpha-missense-score-*` 互斥
> （设置评分上下界时引擎会忽略类别）。`--biallelic-only`
> 与 `--multiallelic-only` 互斥。`--exclude-males` 与
> `--exclude-females` 互斥。将 `*-gt` 界设置为大于或等于与之对应的 `*-lt` 界会定义一个
> 空范围，不会返回任何结果。

> [!NOTE]
> `gnomad_exomes_af`、`gnomad_genomes_af` 和 `am_score` 使用 `0.0` 表示
> **在此服务快照中未注释**。这并不能证明在当前 gnomAD 版本中不存在、在生物学上罕见，
> 或预测为良性。数据集自身的 `af` 字段是另一种统计量，而不是此哨兵值。

> [!CAUTION]
> **数值过滤器为零时在服务器端视为未设置**，因此 `--gnomad-exomes-af-gt 0`
> 不会排除缺失的注释。封装脚本会拒绝零、非有限值、超出范围以及 float32 下溢的界值。
> 请选择一个明确的正阈值（例如 `--gnomad-exomes-af-gt 0.000001` 表示 AF > 1e-6，
> 而不仅仅是存在注释）。如需精确的 `> 0`，请获取完整的变异集合并在本地对返回的 AF
> 进行后过滤。单独使用 `< X` 过滤器会包含未注释的零值。对 AlphaMissense 的缺失评分也应
> 采取同样的谨慎。

分类注释会跨转录本保留。组合使用后果和影响过滤器并不能确定它们描述的是同一个转录本。
`amino_acids` 可能包含多个 HGVSp 条目；通用 gRPC 服务会将典型（canonical）注释放在
最前面，而独立的 MCP 层会裁剪其输出。请保留转录本标识符，不要将模型的“可能致病”类别
视为临床诊断或参与者表型。

## 快速入门

```bash
# 第 1 步。NCBI Gene 672，GRCh38.p14 / NC_000017.11，RS_2025_08：
# BRCA1 跨越 chr17:43044295-43170327（1-based 闭区间）。
# 来源：https://www.ncbi.nlm.nih.gov/gene/672 ；请为你的分析重新解析。
# 第 2 步。评估结果集大小：有多少个体在该区域携带预测为可能致病的
#    错义变异？
uv run scripts/onekgpd_api.py count-samples \
  --chrom chr17 --start 43044295 --end 43170327 \
  --consequence MISSENSE_VARIANT \
  --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/count.json
# 第 3 步。如果数量可控，列出这些个体。
uv run scripts/onekgpd_api.py select-samples \
  --chrom chr17 --start 43044295 --end 43170327 \
  --consequence MISSENSE_VARIANT \
  --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/samples.json
# 第 4 步。针对实际返回的样本 ID，先计数再选择变异。
# 下面的 HG03169,NA20506 是示例 ID；请替换为第 3 步的结果。
uv run scripts/onekgpd_api.py count-variants-in-samples \
  --chrom chr17 --start 43044295 --end 43170327 \
  --samples HG03169,NA20506 \
  --consequence MISSENSE_VARIANT --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/variant_count.json
uv run scripts/onekgpd_api.py select-variants-in-samples \
  --chrom chr17 --start 43044295 --end 43170327 \
  --samples HG03169,NA20506 \
  --consequence MISSENSE_VARIANT --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/variants.json
```

## 命令

每个命令都会将完整 JSON 写入文件（`--output PATH`，默认为临时文件），并在 stdout 打印
简明摘要。所有区域/样本命令共享：区域输入（`--chrom`/`--start`/`--end`，可选
`--ref`/`--alt`，或一个或多个重复的 `--region CHR:START-END`）、合子型标志
（`--het-only`/`--hom-only`，默认两者）以及上述注释过滤器。
完整的逐标志表格见
[references/onekgpd_commands.md](references/onekgpd_commands.md)。

### 返回变异的命令

`select-*` 返回匹配的变异；`count-*` 返回整数计数。

-   `count-variants` —— 在整个队列中统计某区域内的变异。
-   `select-variants` —— 在整个队列中选择某区域内的变异。使用 `--limit N`
    （硬上限，默认 200）**或** `--page-size N`（分页获取完整集合）；两者互斥。达到上限时
    摘要会标记 `truncated`。
-   `count-variants-in-samples` —— 同 `count-variants`，但限制在
    `--samples NAME1,NAME2,...`（必需）范围内。
-   `select-variants-in-samples` —— 同 `select-variants`，但限制在
    `--samples NAME1,NAME2,...`（必需）范围内。

每个返回的变异包含以下 22 个键：`chr`、`start`、`end`、`ref`、
`alt`、`af`、`ac`、`an`、`hom_samples`、`het_samples`、`mis_samples`、
`hom_samples_fx`、`het_samples_fx`、`mis_samples_fx`、`hom_samples_mxy`、
`het_samples_mxy`、`mis_samples_mxy`、`gnomad_exomes_af`、`gnomad_genomes_af`、
`am_score`、`amino_acids`、`biallelic`。
ClinVar 临床意义和 VEP 后果仅作为过滤条件，不会被返回。完整模式（schema）：
[references/onekgpd_commands.md](references/onekgpd_commands.md)。

### 返回样本的命令

-   `count-samples` —— 统计在某区域内携带匹配变异的个体数。
-   `select-samples` —— 列出携带匹配变异的个体名称。
    支持 `--skip N` 和 `--limit N`。仅返回名称；要查看是哪些变异使某个体符合条件，请将
    名称传入 `select-variants-in-samples`。

### 纯合参考型命令

通过 `--chrom` + `--position` 指定单个位置（而非区域）。

-   `count-samples-hom-ref` —— 统计在该位置为 0/0 判型的个体数。
    计数使用哨兵值：`-1` = 该位置根本不存在变异；
    `0` = 存在变异，但没有个体为纯合参考型；`>0` = 纯合参考型个体的数量。这些解读要求
    `result_incomplete=false`；否则 `variant_present` 为 `null`。没有变异记录并不能证明
    所有 3,202 个个体都具有可判型的 0/0 基因型。
-   `select-samples-hom-ref` —— 列出在该位置为 0/0 判型的个体。

### 亲缘关系命令

-   `kinship --sample1 NAME --sample2 NAME` —— 两个指定个体之间的亲缘关系：亲缘度
    （`TWINS_MONOZYGOTIC` / `FIRST_DEGREE` /
    `SECOND_DEGREE` / `THIRD_DEGREE` / `UNRELATED`）以及 KING 亲缘系数
    （`phi_bwf`）。

### 数据集元数据命令

-   `dataset-info` —— 数据集总量：`samples_total`（3,202）、女性/男性构成、
    `variants_total`、`assembly`（GRCh38）以及队列细分。无需指定区域；也可用作连通性检查。

## 样本与群体元数据（离线）

群体、性别、家系和超级群体相关问题由第二个脚本 `scripts/onekgpd_meta.py` 根据技能中
随附的数据文件来回答——**无需网络、无需凭据、无需坐标**。样本 ID 与变异命令使用的名称
相同，因此两层可以组合使用（例如按群体挑选一个队列，然后查询其变异）。运行
`uv run scripts/onekgpd_meta.py <command>`。

该队列包含 5 个超级群体（`AFR`、`AMR`、`EAS`、`EUR`、`SAS`）和 26 个群体。
群体/超级群体的值按简码或全名**不区分大小写**匹配；**样本 ID 区分大小写**。

-   `sample-metadata --samples NA19240,HG00096` —— 给定样本的家庭、性别、父母、
    子女、群体、超级群体和 phase3 状态。
-   `list-populations` —— 全部 26 个群体及其超级群体和样本数
    （用于发现有效取值）。
-   `list-superpopulations` —— 5 个超级群体及其样本数和组成群体。
-   `population-stats --populations YRI [--populations CHS …]` —— 每个群体的性别构成、
    phase3 数量和三联体（trio）成员情况。多个值需重复 `--populations`
    （全名中含有逗号，因此不使用逗号分隔）。
-   `superpopulation-summary --superpopulations EAS [--superpopulations EUR …]` ——
    每个超级群体的总量及按群体的细分。
-   `select-samples-by-population --population YRI` 和/或 `--superpopulation AFR`，
    可选 `--skip`/`--limit`（默认 0 / 50，最大 3202）—— 某群体和/或超级群体中的样本 ID；
    两者同时给出时取交集。将名称传入 `select-variants-in-samples` 即可查看其变异。

完整参数表和 JSON 输出模式请参见 [references/onekgpd_commands.md](references/onekgpd_commands.md)。

## 典型工作流程

### 先找个体，再看其携带的变异

以下为示例模板；请替换所有尖括号占位符。

```bash
# 第 1 步：将基因解析为经过验证的 GRCh38 区域（权威来源）。
# 第 2 步：统计在该区域内携带符合条件变异的个体数。
uv run scripts/onekgpd_api.py count-samples \
  --chrom <chr> --start <start> --end <end> \
  --consequence MISSENSE_VARIANT --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/n.json
# 第 3 步：列出这些个体。
uv run scripts/onekgpd_api.py select-samples \
  --chrom <chr> --start <start> --end <end> \
  --consequence MISSENSE_VARIANT --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/who.json
# 第 4 步：在选择之前，先统计这些个体的变异数。
uv run scripts/onekgpd_api.py count-variants-in-samples \
  --chrom <chr> --start <start> --end <end> \
  --samples <name1,name2,...> \
  --consequence MISSENSE_VARIANT --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/variant_count.json
uv run scripts/onekgpd_api.py select-variants-in-samples \
  --chrom <chr> --start <start> --end <end> \
  --samples <name1,name2,...> \
  --consequence MISSENSE_VARIANT --alpha-missense-class AM_LIKELY_PATHOGENIC \
  --output /tmp/variants.json
```

### 目标位置上的纯合参考型携带者

示例模板；请用经过验证的坐标替换占位符。

```bash
# 确定目标位置（经过验证的坐标）之后：
uv run scripts/onekgpd_api.py count-samples-hom-ref \
  --chrom <chr> --position <pos> --output /tmp/homref_n.json
uv run scripts/onekgpd_api.py select-samples-hom-ref \
  --chrom <chr> --position <pos> --output /tmp/homref.json
```

## 常见错误

-   **错误：**使用未经验证的坐标进行查询。
    **修正：**始终先根据权威来源将基因/特征解析为 GRCh38。
    错误放置的区域会在不报错的情况下返回非预期位置的结果。
-   **错误：**在计数命令之前调用选择命令。
    **修正：**先计数；选择的结果集可能很大。
-   **错误：**以为 GRCh37 坐标也能使用。
    **修正：**本数据集仅支持 GRCh38。

## 参考资料

-   [references/onekgpd_commands.md](references/onekgpd_commands.md) —— 完整的
    逐命令参数表以及返回变异的输出模式。
-   [references/annotation_vocabularies.md](references/annotation_vocabularies.md)
    —— CSV 过滤标志所接受的受控词汇术语
    （后果、影响、生物类型、特征类型、ClinVar 临床意义、
    AlphaMissense 类别、变异类别）。
-   当前 API 契约和实时检查范围：参见
    [命令参考](references/onekgpd_commands.md#verified-api-contract)。
-   千人基因组计划 / IGSR：https://www.internationalgenome.org/
-   千人基因组计划数据集在线版：https://dnaerys.org/online/
