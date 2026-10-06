---
name: imaging-data-commons
description: 从 NCI Imaging Data Commons 查询和下载公开的癌症影像数据。支持 IDC 数据集合发现、DICOM 访问、放射学（CT、MR、PET）和病理学 AI 数据集、元数据 SQL、可视化、许可和引用。使用公开的元数据和下载途径，无需身份验证；可选的 BigQuery 和 Google Healthcare 途径需要 Google 凭据。
compatibility: Requires network access for hosted APIs, index fetching, citations, and downloads. Local Python workflows target idc-index 0.12.5; BigQuery and Google Healthcare require Google credentials.
license: This skill is provided under the MIT License. IDC data itself has individual licensing (mostly CC-BY, some CC-NC) that must be respected when using the data.
metadata:
  version: "1.8"
  last-reviewed: "2026-09-30"
  source-skill-version: "1.8.1"
  skill-author: Andrey Fedorov, @fedorov
  idc-index: "0.12.5"
  idc-data-version: "v24"
  repository: https://github.com/ImagingDataCommons/imaging-data-commons-skill
---

# Imaging Data Commons

## 概述

从美国国家癌症研究所影像数据共享库（National Cancer Institute Imaging Data Commons，IDC）查询和下载公开的癌症影像数据。访问数据无需身份验证。

**预期的网络访问：** IDC 元数据有三种获取途径——捆绑的本地 DuckDB 索引（安装后可离线使用；额外的索引从 GitHub 获取，临床表从 S3 获取），或通过 MCP 或 REST 访问托管的 IDC 服务（`api.imaging.datacommons.cancer.gov`，无需身份验证）。文件下载使用公开的 GCS（`storage.googleapis.com`）和 AWS S3（`s3.amazonaws.com`）——无需身份验证。DICOMweb 访问可使用公开的 IDC 代理（`proxy.imaging.datacommons.cancer.gov`，无需验证），或 Google Cloud Healthcare API（`healthcare.googleapis.com`，需要 GCP 身份验证）。可选的 BigQuery 查询（`bigquery.googleapis.com`）同样需要 GCP 身份验证。引用解析会访问 DOI 服务。公开的 IDC 途径不需要任何凭据；可选的 Google 客户端使用应用默认凭据（Application Default Credentials）。

**2026-09-30 审阅：** idc-index 0.12.5、idc-index-data 24.2.2、IDC v24；托管 API 3.0.0b3。使用时请重新核对。

**首先选择访问路径。** 不存在单一的默认路径：成本最低且正确的路径取决于会话和任务。

1. **会话中已有 IDC MCP 服务器？** 将发现和元数据查询交给它——参见 *IDC MCP 服务器*。
2. **否则，`idc-index` 是否已安装且为最新？** 运行 `python scripts/check_version.py`。如果通过，则所有工作都使用 `idc-index`。
3. **未安装，且任务是只读元数据查询**——计数、属性值、数据集合查找、10 000 行以内的 SQL、许可、引用、查看器 URL？**通过 `curl` 使用 REST API；不要安装任何东西。** 安装需要约 77 MB 的打包索引数据外加 pandas、pyarrow 和 duckdb，而元数据问题并不需要这些。参见 *数据访问选项*。
4. **未安装，且任务需要的不仅是元数据**——下载文件、pandas 或绘图、pydicom/SimpleITK、病理切片分块（tiling）、超过 10 000 行的结果，或用户需要重复运行的版本固定脚本？安装 `idc-index`：`check_version.py` 会以非零状态退出，并打印适用于当前运行解释器的确切安装命令。优先使用虚拟环境，然后重启 Python。

`idc-index`（[GitHub](https://github.com/imagingdatacommons/idc-index)）仍然是功能最强的 Python 途径，在一个客户端中同时提供查询和下载辅助功能。`check_version.py` 本身从不安装任何东西——当存在更新的 `idc-index` 或技能版本时，它也会给出提示。

**`idc-index` 路径的设置：** 使用目标解释器运行 `scripts/check_version.py`，并在继续之前确认其输出 `meets pinned minimum` 消息。启动失败不算通过。

```python
from idc_index import IDCClient
client = IDCClient()

# 验证 IDC 数据版本（应为 "v24"）
print(f"IDC data version: {client.get_idc_version()}")
```

除非另有说明，下载和图像处理示例仅作说明用途；验证范围参见参考文档中的审阅说明。

**核心工作流：** 使用 `client.sql_query()` 查询元数据 → 使用 `client.download_from_selection()` 下载 → 使用 `client.get_viewer_URL()` 可视化。下面的 Python 示例均假定已有此 `client`；*数据访问选项* 中给出了对应的 REST 等价方式。要了解当前的数据规模，请运行 `references/sql_patterns.md` 中的汇总查询或 `GET /v3/stats`。

## IDC MCP 服务器

IDC 在 `https://api.imaging.datacommons.cancer.gov/mcp` 运营一个托管的 MCP 服务器（可流式 HTTP，无需身份验证）。在可用的情况下，它是下文 `idc-index` 工作流的补充——而不是替代。

**识别方法：** 通过 MCP 资源 `idc://guide`，或通过以下工具名称中的三个或更多：`build_cohort`、`get_cohort_urls`、`list_analysis_results` 和 `get_idc_version`。像 `run_sql` 这样的通用名称本身不能作为证据。如果识别结果不明确，请使用 `idc-index`。

**如果本会话中有该服务器**，则将其视为发现和元数据方面的权威来源——IDC 版本、计数、属性值、队列构建、元数据 SQL——并遵循服务器自身的说明，而不是根据本文件重新推导。其数据版本以服务器报告的为准：调用 `get_idc_version`，而不要依赖本文件中固定的版本。

对于服务器不做的事情，请回到这里：下载文件、本地 pandas/notebook 分析、DICOMweb、BigQuery、数字病理切片分块以及可复现脚本。交接方式是将服务器给出的 SeriesInstanceUID 传给 `client.download_from_selection(...)`，并在此时运行 `scripts/check_version.py`。

**如果它不可用**，同一服务无需任何配置即可通过 REST API 在 `https://api.imaging.datacommons.cancer.gov/v3` 访问——按照 *概述* 中的路由规则，对于只读元数据请使用它，而不是安装 `idc-index`。最多建议一次连接 MCP 服务器，且仅在需要反复进行交互式发现时才建议，并且绝不要自行修改用户的配置。

工具清单、交接模式和各宿主环境的说明参见 `references/mcp_guide.md`。

## 何时使用此技能

- 查找公开可用的放射学（CT、MR、PET）或病理学（玻片显微成像）图像
- 按癌症类型、模态、解剖部位或其他元数据选择图像子集
- 从 IDC 下载 DICOM 数据
- 在用于研究或商业应用之前检查数据许可
- 在浏览器中可视化医学图像，无需本地 DICOM 查看器软件

## 快速导航

下文直接包含：MCP/REST 路由规则、IDC 数据模型、索引表及其连接方式、核心 API 模式（查询、下载、可视化、许可、引用）、最佳实践和故障排除。

**参考指南（按需加载）：**

| 指南 | 何时加载 |
|-------|--------------|
| `index_tables_guide.md` | 复杂 JOIN、模式（schema）发现、DataFrame 访问 |
| `use_cases.md` | 端到端工作流：训练数据集、批量下载、使用 pydicom/SimpleITK 读取 DICOM、流水线集成 |
| `sql_patterns.md` | 用于筛选值发现、注释、大小估算的快速 SQL 模式 |
| `clinical_data_guide.md` | 临床/表格数据、影像与临床数据连接、值映射 |
| `licensing_and_citation.md` | 商业使用问题、混合许可队列、引用格式 |
| `cloud_storage_guide.md` | 直接 S3/GCS 访问、版本控制、UUID 映射 |
| `dicomweb_guide.md` | DICOMweb 端点、PACS 集成 |
| `digital_pathology_guide.md` | 玻片显微成像（SM）、注释（ANN）、病理学工作流 |
| `bigquery_guide.md` | 完整 DICOM 元数据、私有元素（需要 GCP） |
| `cli_guide.md` | 命令行工具（`idc download`、清单文件） |
| `parquet_access_guide.md` | 通过 GCS 直接查询 Parquet（无需安装 idc-index） |
| `mcp_guide.md` | 托管的 IDC MCP 服务器：工具清单、识别、交接到 `idc-index` |
| `rest_api_guide.md` | 托管的 IDC REST API：端点、筛选语法、基于 HTTP 的 SQL、清单 |

## IDC 数据模型

IDC 在标准 DICOM 层级（Patient → Study → Series → Instance）之上增加了两个分组层级：

- **collection_id**：按疾病、模态或研究重点对患者分组（例如 `tcga_luad`、`nlst`）。将 `(collection_id, PatientID)` 视为患者键；不要假定 PatientID 是全局唯一的。
- **analysis_result_id**：标识跨一个或多个原始数据集合的衍生对象（分割、注释、影像组学特征）。用它查找 AI 生成的或专家注释，而 `collection_id` 用于查找原始影像数据（其中本身可能包含随数据提交的注释）。

**查询的关键标识符：**
| 标识符 | 范围 | 用途 |
|------------|-------|---------|
| `collection_id` | 数据集分组 | 按项目/研究筛选 |
| `PatientID` | 患者 | 按患者对图像分组 |
| `StudyInstanceUID` | DICOM 检查（study） | 相关序列的分组、可视化 |
| `SeriesInstanceUID` | DICOM 序列（series） | 相关序列的分组、可视化 |

## 索引表

`idc-index` 包提供多个元数据索引表，可通过 SQL 或作为 pandas DataFrame 访问。REST API 通过 `GET /tables` 和 `POST /sql` 提供相同的表。

**重要：** `client.indices_overview` 是当前表描述、可用列及其类型的权威来源——编写 SQL 或探索数据结构时请查询它。它还能回答“哪个表包含列 X”；该搜索模式及完整的模式发现参见 `references/index_tables_guide.md`。

### 可用表

在查询任何索引表之前，务必调用 `client.fetch_index("table_name")`——它对所有表（包括启动时自动加载的表）都是安全且幂等的。

| 类别 | 表 | 粒度 |
|--------|--------|-------------|
| 核心 | `index`（所有当前数据的主元数据）、`collections_index`、`analysis_results_index` | 序列 / 数据集合 / 分析结果 |
| 模态采集参数 | `ct_index`、`mr_index`、`pt_index`、`contrast_index` | 1 行 = 该模态的 1 个序列 |
| 衍生对象 | `seg_index`、`rtstruct_index`、`ann_index`、`ann_group_index` | 1 行 = 1 个序列（或注释组） |
| 显微成像 | `sm_index`、`sm_instance_index` | 1 行 = 1 个 SM 序列 / 实例 |
| 几何、临床、历史 | `volume_geometry_index`、`clinical_index`、`version_metadata_index`、`prior_versions_index` | 参见指南 |

`references/index_tables_guide.md` 包含完整清单，列出每个表的列和内容——当你需要了解某个专用表实际包含什么时加载它。

**`prior_versions_index` 包含历史序列版本**，包括其 DICOM SeriesInstanceUID 仍出现在 `index` 中的修订版本。对于历史内容，请固定 `crdc_series_uuid`。要查询当前发布中的“新增内容”，请使用主 `index` 表中的 `series_init_idc_version` / `series_revised_idc_version`，它们与该表中的 `min_idc_version` / `max_idc_version` 并不等价。

### 连接表

**`SeriesInstanceUID` 是所有序列级专用表的通用连接键**：`sm_index`、`sm_instance_index`、`seg_index`、`ann_index`、`ann_group_index`、`contrast_index`、`volume_geometry_index`、`rtstruct_index`、`ct_index`、`mr_index`、`pt_index`。始终通过 `SeriesInstanceUID` 将这些表与 `index` 连接。下面的例外情况使用不同的列名。

| 连接列 | 表 | 用例 |
|-------------|--------|----------|
| `collection_id` | index、prior_versions_index、collections_index、clinical_index | 将序列链接到数据集合元数据或临床数据 |
| `analysis_result_id` | index、analysis_results_index | 将序列链接到分析结果元数据（注释、分割） |
| `source_DOI` | index、analysis_results_index | 按出版物 DOI 链接 |
| `segmented_SeriesInstanceUID` | seg_index → index | 将分割链接到其源图像序列（`seg_index.segmented_SeriesInstanceUID = index.SeriesInstanceUID`） |
| `referenced_SeriesInstanceUID` | ann_index → index、rtstruct_index → index | 将注释或 RTSTRUCT 链接到其源图像序列 |

**注意：** `subjects`、`updated` 和 `description` 出现在多个表中，但含义不同（计数与标识符、不同的更新上下文）。仅按 UID 连接 `prior_versions_index` 可能匹配到多个历史修订版本；请使用 CRDC UUID 加以区分。

详细的连接示例、模式发现模式、关键列参考和 DataFrame 访问，参见 `references/index_tables_guide.md`。

### 临床数据访问

临床（非影像）属性——分期、人口统计学、治疗——存放在按数据集合划分的表中。`client.fetch_index("clinical_index")` 加载将列映射到数据集合的字典；`client.get_clinical_table(name)` 以 DataFrame 形式返回单个表。

发现工作流、编码值映射以及临床数据与影像的连接，参见 `references/clinical_data_guide.md`。

## 数据访问选项

| 方法 | 认证 | 最适合 | 参考 |
|--------|------|----------|-----------|
| `idc-index` | 否 | 下载、pandas 分析、无限制查询——功能最强的途径 | 本文档 |
| IDC MCP 服务器 | 否 | 会话中已有该服务器时的发现、队列构建、元数据 | `mcp_guide.md` |
| IDC REST API | 否 | 无需安装、可从任何语言或 shell 获取元数据——`idc-index` 不存在时的默认途径 | `rest_api_guide.md` |
| 直接 Parquet（GCS） | 否 | 版本固定的查询，或超出 REST 行数上限的结果 | `parquet_access_guide.md` |
| 云存储（S3/GCS） | 否 | 直接文件访问、批量传输、自定义流水线 | `cloud_storage_guide.md` |
| 通过 IDC 代理的 DICOMweb | 否 | 工具和 PACS 集成；有每日配额，适合测试和中等规模使用 | `dicomweb_guide.md` |
| 通过 Google Healthcare 的 DICOMweb | 是（GCP） | 生产规模下的相同 DICOMweb API，没有代理配额限制 | `dicomweb_guide.md` |
| SlicerIDCBrowser | 否 | 在 3D Slicer 中进行 3D 可视化和分析 | https://github.com/ImagingDataCommons/SlicerIDCBrowser |
| BigQuery | 是（GCP） | 完整 DICOM 元数据、私有元素、SR 测量值——最后手段 | `bigquery_guide.md` |

**IDC 门户（https://portal.imaging.datacommons.cancer.gov/）仅供交互使用**——基于浏览器的探索、手动队列选择和下载。与上述所有选项不同，它没有编程接口，因此可以引导用户去那里自行浏览或点选数据；绝不要将其用作脚本或工作流中的一个步骤。

**REST API——无需安装的元数据途径**

`https://api.imaging.datacommons.cancer.gov/v3`，无需身份验证：发现、队列计数和清单、只读 SQL、临床表、查看器 URL、许可、引用。它与 MCP 服务器是同一服务，只是通过普通 HTTP 提供，因此无需任何配置。它从不传输图像字节——要下载、获取 DataFrame 或处理超过 10 000 行的结果，请切换到 `idc-index`。

```bash
B=https://api.imaging.datacommons.cancer.gov/v3
curl -s $B/version   # idc_version、idc_index_data_version、api_version
curl -s $B/stats     # 数据集合、患者、检查、序列、实例、size_TB
curl -s "$B/attributes/Modality/values?limit=5"   # 真实的筛选值及计数
curl -s $B/sql -H 'content-type: application/json' \
  -d '{"sql":"SELECT collection_id, COUNT(*) n FROM index GROUP BY 1 ORDER BY n DESC LIMIT 3"}'
curl -s $B/cohort/counts -H 'content-type: application/json' \
  -d '{"filters":{"terms":{"collection_id":["rider_pilot"]}}}'
```

**筛选对象始终放在 `filters` 下**——在 `cohort/counts`、`cohort/manifest`、`cohort/manifest.txt`、`licenses` 和 `citations` 上都是如此。裸筛选对象或无法识别的键会返回 422，并指明修正方法；未加筛选的序列枚举请求会返回 400，而不是整个存档。带筛选的 JSON 响应会回显 `filters_applied` 和 `warnings`（对于清单，位于 `counts` 内）——请阅读它们，因为它们会指出服务器丢弃了哪些谓词。因此，计数为零且 `warnings` 为空意味着筛选条件没有匹配到任何内容，而不是某个值的大小写错误；大小写错误会产生一条说明此情况的警告。

`POST /sql` 接受一条只读的 `SELECT`/`WITH` 语句，作用于 `idc-index` 提供的表以及 `clinical.<table>`；`max_rows` 默认为 5 000，上限为 10 000，`truncated` 标记结果是否被截断。`GET /attributes` 列出 19 个可筛选属性——临床值、分割的解剖结构和采集参数不在其中，需要使用 SQL。请求限制仍然适用。**仅使用 v3：** V1 和 V2 已被取代并计划关闭，因此对于用户带来的任何 `/v1/` 或 `Modality_btw` 风格的示例，请将其移植过来，而不是在其基础上扩展。

两端都构建在 `idc-index-data` 之上，因此在混合使用之前，请比较 API 的 `idc_index_data_version` 与本地的 `idc_index_data.__version__`：**主版本号即 IDC 数据发布版本**（`24.x.y` 提供 `v24`）；次版本/补丁版本的索引构建可能会修正元数据。如果 API 领先整整一个发布版本，`idc-index` **无法下载额外的序列**——混合选择可能会遗漏无法识别的 UID，而完全无法匹配的选择会抛出异常——因此要么升级它（运行 `scripts/check_version.py` 获取正确的命令），要么使用 `s5cmd --no-sign-request` 直接从存储桶传输。

端点参考、筛选值依据、限制以及基于清单的下载流程，参见 `references/rest_api_guide.md`。

**云存储组织方式**

所有 DICOM 文件都存放在 AWS S3 和 GCS 之间互为镜像的公开存储桶中，按 CRDC UUID（而非 DICOM UID）组织以支持版本控制，格式为 `<crdc_series_uuid>/<crdc_instance_uuid>.dcm`。通过 AWS CLI、gsutil 或 s5cmd 匿名访问是免费的（无出口流量费用）；S3 URL 请使用 `series_aws_url` 列。存储桶名称并不决定许可；请为每个所选序列查询 `license_short_name`。完整的存储桶列表和 UUID 映射参见 `references/cloud_storage_guide.md`。

**DICOMweb 访问**

IDC 数据可通过 DICOMweb（Google Cloud Healthcare API）访问，用于 PACS 集成和兼容 DICOMweb 的工具：公开代理（无需验证，有每日配额）用于测试和中等规模查询，或 Google Healthcare（需 GCP 验证）用于生产规模。参见 `references/dicomweb_guide.md`。

**直接 Parquet 访问**

idc-index 元数据表也以 Parquet 格式发布在公开的 GCS 存储桶（`idc-index-data-artifacts`）上，可使用 DuckDB 或 pandas 查询。这需要安装 DuckDB
对于临时的元数据查询，优先使用 REST `/sql`；对于固定版本或大型结果，选择 Parquet。另有一个独立的公开 S3 导出，还包含临床表和完整的 BigQuery 元数据。参见 `references/parquet_access_guide.md`。

## 核心功能

以下模式是凭记忆而非经过核对时最容易出错的那些。每个领域的完整示例位于文中所提及的参考指南中。

### 1. 发现——先枚举取值，再据此筛选

按猜测的 `Modality` 或 `BodyPartExamined` 字符串进行筛选，是结果集为空的最常见原因。请先枚举：

```python
modalities = client.sql_query("""
    SELECT DISTINCT Modality, COUNT(*) as series_count
    FROM index
    GROUP BY Modality
    ORDER BY series_count DESC
""")
print(modalities)
```

同样的模式适用于任何筛选列，并可选择用另一列进一步缩小范围——如某个 `Modality` 内的 `BodyPartExamined`、`Manufacturer`、`collection_id`。在 REST 途径上，这种取值核实只需一次调用——`GET /attributes/{attr}/values` 返回取值及其计数——而队列端点会在 `warnings` 中报告大小写错误的值，而不是返回空结果。

有两个索引包含主 `index` 所没有的、经过整理的数据集合级元数据，两者都需要先调用 `client.fetch_index(...)`：`collections_index`（癌症类型、肿瘤部位、物种、受试者数量）和 `analysis_results_index`（衍生数据集——AI 分割、专家注释、影像组学——及其源数据集合和模态）。

**癌症类型位于 `collections_index.cancer_types` 中，而不在 `index` 中**——按癌症类型筛选需要进行连接：

```python
client.fetch_index("collections_index")
results = client.sql_query("""
    SELECT i.collection_id, i.PatientID, i.SeriesInstanceUID, i.Modality
    FROM index i
    JOIN collections_index c ON i.collection_id = c.collection_id
    WHERE c.cancer_types LIKE '%Breast%'
      AND i.Modality = 'MR'
    LIMIT 20
""")
```

`client.sql_query()` 返回一个 pandas DataFrame。在编写查询之前，请使用 `client.get_index_schema('index')` 或 `client.indices_overview` 确认列名，而不要凭假设。

筛选值发现、注释和分割查询、大小估算、临床链接和版本跟踪（“vX 中有什么新内容”——使用 `index` 中的 `series_init_idc_version` / `series_revised_idc_version`；历史对象使用 `prior_versions_index`），参见 `references/sql_patterns.md`。

### 2. 下载 DICOM 文件

**两种下载方法的前两个参数顺序相反。** 这是 IDC 代码出错的最常见来源——请核对，而不要凭记忆：

| 方法 | 第一个参数 | 第二个参数 | 使用场景 |
|--------|-----------|------------|----------|
| `download_from_selection` | `downloadDir`（必需） | 筛选关键字参数（可选） | 按数据集合、患者、检查或序列筛选 |
| `download_dicom_series` | `seriesInstanceUID`（必需） | `downloadDir`（必需） | 仅按 UID 下载特定序列 |

**`download_from_selection` 接受筛选关键字参数，而不是 DataFrame。** 名称中的 “from_selection” 指的是按条件筛选 IDC 索引——而不是接受 pandas DataFrame。要下载查询结果，请先将 UID 提取为列表：

```python
# 第 1 步：查询序列 UID
series_df = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
      AND collection_id = 'nlst'
    LIMIT 5
""")

# 第 2 步：从 DataFrame 中将 UID 提取为列表
uids = list(series_df['SeriesInstanceUID'].values)

# 第 3 步：将列表传给 download_from_selection（不是 DataFrame 本身）
client.download_from_selection(
    downloadDir="./data/lung_ct",
    seriesInstanceUID=uids       # 字符串列表，而不是 DataFrame
)

# 替代方式：download_dicom_series 的第一个参数是 seriesInstanceUID（顺序不同！）
client.download_dicom_series(
    seriesInstanceUID=uids,      # 这里是第一个参数
    downloadDir="./data/lung_ct"
)

# 整个数据集合：downloadDir 仍然是第一个位置参数
client.download_from_selection(downloadDir="./data/rider", collection_id="rider_pilot")
```

两者默认都使用 AWS；如需使用 Google，请指定 `source_bucket_location="gcs"`。在 0.12.5 中，最具体的选择器优先生效，因此对于需要取交集的条件，请先使用 SQL，并验证每个请求的 UID 都存在。

**下载的文件命名为 `<crdc_instance_uuid>.dcm`，而不是按 SOPInstanceUID 命名。** DICOM UID 保存在文件元数据中，而不是文件名中。请读取 DICOM 头部获取序列 UID；`crdc_instance_uuid` 不是序列级 `index` 的列。

`idc download <collection|series-uid|manifest> --download-dir ./data` 可在 shell 中完成同样的操作。`dirTemplate` 层级选项（Python 默认值：`%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`；`dirTemplate=""` 表示扁平化）、支持断点续传的清单下载以及试运行（dry-run）大小估算，参见 `references/cli_guide.md`。

### 3. 可视化 IDC 图像

```python
viewer_url = client.get_viewer_URL(seriesInstanceUID=uid)        # 单个序列
viewer_url = client.get_viewer_URL(studyInstanceUID=study_uid)   # 一个检查中的所有序列
```

返回一个浏览器 URL——不会下载任何内容。该方法会自动为放射学选择 OHIF v3，为玻片显微成像选择 SLIM。当单个 DICOM 检查包含多个序列（来自一次 MRI 扫描的 T1、T2 和 DWI）时，按检查查看非常有用。

### 4. 许可和引用——是义务，而非可选步骤

IDC 数据附带许可条款和署名要求，这些要求会延续到任何下游出版物或产品中，而且两者都无法从像素数据中推断出来。**使用前检查许可，并为下载的所有内容生成引用。**

```python
# 某个选择的许可分布
licenses = client.sql_query("""
    SELECT DISTINCT collection_id, license_short_name,
           COUNT(DISTINCT SeriesInstanceUID) as series_count
    FROM index GROUP BY collection_id, license_short_name
""")

# 为你下载的同一选择生成引用（默认 APA 格式）
for citation in client.citations_from_selection(collection_id="rider_pilot"):
    print(citation)
```

在经审阅的 v24 快照中，按大小计算约 97% 的 IDC 数据为 CC BY（允许商业使用，需署名），约 3% 为 CC BY-NC（仅限非商业使用）。**许可附加在序列上，而不是数据集合上**——176 个数据集合中有 39 个包含不止一种许可——因此请检查你实际打算使用的选择，并注意每个组成部分都保留其许可义务。

这两项任务在所有三种访问途径中都可用，因此请继续使用会话当前正在使用的途径：如上所示的 `idc-index`、REST 上的 `POST /v3/licenses` 和 `POST /v3/citations`，或 MCP 工具 `get_licenses` 和 `get_citations`。完整的许可清单、所有三种途径、引用格式（APA、BibTeX、CSL JSON、RDF Turtle）以及发表时应包含的内容，参见 `references/licensing_and_citation.md`。

### 5. 超出索引范围

使用 *概述* 中的路由规则选择访问途径；上文的 *数据访问选项* 是完整的路由表。

在使用 BigQuery（需要 Google Cloud 项目和访问权限）之前，请检查某个专用索引表是否已有你需要的列：搜索 `client.indices_overview`，然后执行 `client.fetch_index(...)` 并在本地免费查询。完整的实例元数据、逐分割段的行以及 SR 测量表需要 BigQuery 或其公开的 Parquet 导出；它们不在紧凑的 idc-index 表中。

## 最佳实践

- **编写查询前检查模式** —— 使用 `client.get_index_schema('index')`（读取缓存的元数据，不执行 SQL）或 `client.indices_overview` 查看所有可用列及其描述。主 `index` 表中的版本跟踪列 `series_init_idc_version` 和 `series_revised_idc_version` 可直接回答“有什么新内容 / 何时添加”的问题，无需涉及 `prior_versions_index`。
- **对于 IDC 数据内容问题，使用索引** - 直接查询 IDC 索引，可在本地通过 `client.sql_query()` 或通过 HTTP 使用 `POST /v3/sql`。网络来源（发布说明、博客文章、文档页面）经常过时，会导致错误的答案。索引是权威来源；即使可以进行网络搜索，也要使用索引。
- **在会话开始时验证 IDC 数据版本** - 根据所用途径，使用 `client.get_idc_version()`、`GET /v3/version` 或 MCP 工具 `get_idc_version`（当前为 v24）。对于过时的本地索引，运行 `scripts/check_version.py` 并使用其打印的升级命令
- **检查许可并生成引用** - 查询 `license_short_name` 并遵守 CC BY 与 CC BY-NC 的条款；使用 `citations_from_selection()` 根据 `source_DOI` 为出版物生成引用
- **先小规模探索，再正式执行** - 探索时使用 `LIMIT`（或较小的 `max_rows`），并在下载前检查数据集合大小——有些数据集合达到 TB 级。参见 `references/cli_guide.md`
- **保持下载可复现** - 使用 `dirTemplate`（例如 `%collection_id/%PatientID/%Modality`）组织文件，并保存你构建的任何数据集背后的序列 UID 或清单

## 故障排除

**问题：`ModuleNotFoundError: No module named 'idc_index'`**
- **原因：** 未安装 idc-index 包
- **解决方案：** 如果任务是只读元数据查询，不要安装它——改用 REST API（*数据访问选项*）。否则运行 `scripts/check_version.py` 并使用其打印的安装命令，该命令针对当前运行的解释器并固定经过验证的版本。进行数据分析时还需添加 pandas、numpy 和 pydicom（已在 pandas>=1.5、numpy>=1.23、pydicom>=2.3 下测试）

**问题：下载因连接超时失败**
- **原因：** 网络不稳定或下载量过大
- **解决方案：** 分小批次下载（10-20 个序列）；`--use-s5cmd-sync` 断点续传和重试指导参见 `references/cli_guide.md`

**问题：`BigQuery quota exceeded` 或计费错误**
- **原因：** 项目配额、沙盒限制或计费配置导致查询无法执行
- **解决方案：** 对简单查询使用 idc-index 迷你索引（无需计费），或参见 `references/bigquery_guide.md` 中的成本优化技巧

**问题：找不到序列 UID 或未返回数据**
- **原因：** UID 拼写错误、数据不在当前 IDC 版本中，或字段名错误
- **解决方案：** 先用 `LIMIT 5` 测试，对照 `client.indices_overview` 检查字段名，并确认该序列在当前版本中（一些旧数据已被弃用）

**问题：在 `index` 表中找不到列（例如 `SliceThickness`、`PixelSpacing`、`KVP`、`EchoTime`、`InjectedDose`）**
- **原因：** `index` 表仅包含序列级元数据；特定模态的采集和重建参数位于专用表中（`ct_index`、`mr_index`、`pt_index`）
- **解决方案：** 在 `client.indices_overview` 中搜索该列以找到其所在的表——相应循环见 `references/index_tables_guide.md` 中的 *Finding which table contains a column* 部分——然后获取该表并通过 `SeriesInstanceUID` 连接：
  ```python
  client.fetch_index("ct_index")
  result = client.sql_query("""
      SELECT i.SeriesInstanceUID, i.Modality, c.SliceThickness, c.KVP, c.PixelSpacing_row_mm
      FROM index i
      JOIN ct_index c USING (SeriesInstanceUID)
      WHERE i.collection_id = 'your_collection'
  """)
  ```

**问题：下载的 DICOM 文件无法打开**
- **原因：** 下载损坏，或查看器不支持的对象类型——SEG、RTSTRUCT、SR 和玻片显微成像都需要专用工具
- **解决方案：** 使用常规的 `pydicom.dcmread` 检查 `Modality`、`SOPClassUID` 和传输语法；[强制解析并不等于验证](https://pydicom.github.io/pydicom/stable/reference/generated/pydicom.filereader.dcmread.html)。在重新下载之前，检查下载完整性以及解码器/查看器的支持情况；仅对已诊断为非 Part-10 的输入使用 `force=True`。

## 资源

参考指南及其使用触发条件已在上文 *快速导航* 中列出。

- **IDC 门户**：https://portal.imaging.datacommons.cancer.gov/explore/
- **文档**：https://learn.canceridc.dev/ — **教程**：https://github.com/ImagingDataCommons/IDC-Tutorials
- **用户论坛**：https://discourse.canceridc.dev/ — **idc-index**：https://github.com/ImagingDataCommons/idc-index
- **[indices_reference](https://idc-index.readthedocs.io/en/latest/indices_reference.html)** —— 外部索引表文档（可能领先于已安装的版本）
- **引用**：Fedorov, A., et al. "National Cancer Institute Imaging Data Commons: Toward Transparency, Reproducibility, and Scalability in Imaging Artificial Intelligence." RadioGraphics 43.12 (2023). https://doi.org/10.1148/rg.230180
- **技能更新**：[发布页面](https://github.com/ImagingDataCommons/imaging-data-commons-skill/releases)；关注该仓库（Watch → Custom → Releases）
