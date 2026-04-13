---
name: imaging-data-commons
description: 使用idc-index查询和下载来自NCI成像数据公共资源的公共癌症成像数据。用于访问大规模放射学（CT、MR、PET）和病理学数据集以进行AI训练或研究。无需身份验证。按元数据查询、在浏览器中可视化、检查许可证。
license: 此技能在MIT许可证下提供。IDC数据本身具有单独的许可（主要是CC-BY，一些CC-NC），在使用数据时必须遵守。
metadata:
    version: 1.4.0
    skill-author: Andrey Fedorov, @fedorov
    idc-index: "0.11.14"
    idc-data-version: "v23"
    repository: https://github.com/ImagingDataCommons/idc-claude-skill
---

# 成像数据公共资源

## 概述

使用`idc-index` Python软件包查询和下载来自国家癌症研究所成像数据公共资源（IDC）的公共癌症成像数据。数据访问无需身份验证。

**当前IDC数据版本：v23**（始终使用`IDCClient().get_idc_version()`验证）

**主要工具：** `idc-index`（[GitHub](https://github.com/imagingdatacommons/idc-index)）

**关键 - 检查软件包版本并在需要时升级（首先运行此操作）：**

```python
import idc_index

REQUIRED_VERSION = "0.11.14"  # 必须与此文件中的metadata.idc-index匹配
installed = idc_index.__version__

if installed < REQUIRED_VERSION:
    print(f"正在将idc-index从{installed}升级到{REQUIRED_VERSION}...")
    import subprocess
    subprocess.run(["pip3", "install", "--upgrade", "--break-system-packages", "idc-index"], check=True)
    print("升级完成。重启Python以使用新版本。")
else:
    print(f"idc-index {installed}满足要求（{REQUIRED_VERSION}）")
```

**验证IDC数据版本并检查当前数据规模：**

```python
from idc_index import IDCClient
client = IDCClient()

# 验证IDC数据版本（应该是"v23"）
print(f"IDC数据版本：{client.get_idc_version()}")

# 获取集合计数和总序列
stats = client.sql_query("""
    SELECT
        COUNT(DISTINCT collection_id) as collections,
        COUNT(DISTINCT analysis_result_id) as analysis_results,
        COUNT(DISTINCT PatientID) as patients,
        COUNT(DISTINCT StudyInstanceUID) as studies,
        COUNT(DISTINCT SeriesInstanceUID) as series,
        SUM(instanceCount) as instances,
        SUM(series_size_MB)/1000000 as size_TB
    FROM index
""")
print(stats)
```

**核心工作流程：**
1. 查询元数据 → `client.sql_query()`
2. 下载DICOM文件 → `client.download_from_selection()`
3. 在浏览器中可视化 → `client.get_viewer_URL(seriesInstanceUID=...)`

## 何时使用此技能

- 查找公开可用的放射学（CT、MR、PET）或病理学（切片显微镜）图像
- 按癌症类型、模态、解剖部位或其他元数据选择图像子集
- 从IDC下载DICOM数据
- 在研究或商业应用中使用前检查数据许可证
- 在不使用本地DICOM查看器软件的情况下在浏览器中可视化医学图像

## 快速导航

**核心部分（内联）：**
- IDC数据模型 - 集合和分析结果层次结构
- 索引表 - 可用表和连接模式
- 安装 - 软件包设置和版本验证
- 核心功能 - 基本API模式（查询、下载、可视化、许可证、引用、批量）
- 最佳实践 - 使用指南
- 故障排除 - 常见问题和解决方案

**参考指南（按需加载）：**

| 指南 | 何时加载 |
|-------|--------------|
| `index_tables_guide.md` | 复杂JOIN、模式发现、DataFrame访问 |
| `use_cases.md` | 端到端工作流示例（训练数据集、批量下载） |
| `sql_patterns.md` | 快速SQL模式用于过滤器发现、注释、大小估计 |
| `clinical_data_guide.md` | 临床/表格数据、成像+临床连接、值映射 |
| `cloud_storage_guide.md` | 直接S3/GCS访问、版本控制、UUID映射 |
| `dicomweb_guide.md` | DICOMweb端点、PACS集成 |
| `digital_pathology_guide.md` | 切片显微镜（SM）、注释（ANN）、病理学工作流 |
| `bigquery_guide.md` | 完整DICOM元数据、私有元素（需要GCP） |
| `cli_guide.md` | 命令行工具（`idc download`、清单文件） |
| `parquet_access_guide.md` | 通过GCS直接Parquet查询（无需安装idc-index） |

## IDC数据模型

IDC在标准DICOM层次结构（患者 → 研究 → 序列 → 实例）之上添加了两个分组级别：

- **collection_id**：按疾病、模态或研究重点对患者进行分组（例如，`tcga_luad`、`nlst`）。一个患者恰好属于一个集合。
- **analysis_result_id**：识别跨一个或多个原始集合的派生对象（分割、注释、放射组学特征）。

使用`collection_id`查找原始成像数据，可能包括随图像一起存放的注释；使用`analysis_result_id`查找AI生成或专家注释。

**查询的关键标识符：**
| 标识符 | 范围 | 用于 |
|------------|-------|---------|
| `collection_id` | 数据集分组 | 按项目/研究过滤 |
| `PatientID` | 患者 | 按患者分组图像 |
| `StudyInstanceUID` | DICOM研究 | 相关序列的分组、可视化 |
| `SeriesInstanceUID` | DICOM序列 | 相关序列的分组、可视化 |

## 索引表

`idc-index`软件包提供多个元数据索引表，可通过SQL或pandas DataFrame访问。

**完整索引表文档：** 使用https://idc-index.readthedocs.io/en/latest/indices_reference.html快速检查可用表和列，而无需执行任何代码。

**重要：** 使用`client.indices_overview`获取当前表描述和列模式。这是可用列及其类型的权威来源 - 在编写SQL或探索数据结构时始终查询它。

### 可用表

| 表 | 行粒度 | 加载 | 描述 |
|-------|-----------------|--------|-------------|
| `index` | 1行 = 1个DICOM序列 | 自动 | 所有当前IDC数据的主要元数据 |
| `prior_versions_index` | 1行 = 1个DICOM序列 | 自动 | 来自先前IDC版本的序列；用于下载已弃用的数据 |
| `collections_index` | 1行 = 1个集合 | fetch_index() | 集合级元数据和描述 |
| `analysis_results_index` | 1行 = 1个分析结果集合 | fetch_index() | 关于派生数据集（注释、分割）的元数据 |
| `clinical_index` | 1行 = 1个临床数据列 | fetch_index() | 将临床表列映射到集合的字典 |
| `sm_index` | 1行 = 1个切片显微镜序列 | fetch_index() | 切片显微镜（病理学）序列元数据 |
| `sm_instance_index` | 1行 = 1个切片显微镜实例 | fetch_index() | 切片显微镜的实例级（SOPInstanceUID）元数据 |
| `seg_index` | 1行 = 1个DICOM分割序列 | fetch_index() | 分割元数据：算法、段计数、对源图像序列的引用 |
| `ann_index` | 1行 = 1个DICOM ANN序列 | fetch_index() | 显微镜批量简单注释序列元数据；引用注释的图像序列 |
| `ann_group_index` | 1行 = 1个注释组 | fetch_index() | 详细注释组元数据：图形类型、注释计数、属性代码、算法 |
| `contrast_index` | 1行 = 1个带有对比度信息的序列 | fetch_index() | 对比度剂元数据：剂名称、成分、给药途径（CT、MR、PT、XA、RF） |
| `volume_geometry_index` | 1行 = 1个CT/MR/PT序列 | fetch_index() | 单帧CT、MR和PT序列的3D体积几何验证；方向、间距、维度和切片位置的布尔检查；复合 `regularly_spaced_3d_volume` 标志 |
| `rtstruct_index` | 1行 = 1个RTSTRUCT序列 | fetch_index() | RT结构集元数据：总ROI计数、ROI名称、生成算法、解释类型以及引用的图像序列UID |

**自动** = 实例化`IDCClient()`时自动加载
**fetch_index()** = 需要`client.fetch_index("table_name")`来加载

### 连接表

**关键列没有明确标记，以下是可用于连接的子集。**

| 连接列 | 表 | 用例 |
|-------------|--------|----------|
| `collection_id` | index、prior_versions_index、collections_index、clinical_index | 将序列连接到集合元数据或临床数据 |
| `SeriesInstanceUID` | index、prior_versions_index、sm_index、sm_instance_index | 跨表连接序列；连接到切片显微镜详情 |
| `StudyInstanceUID` | index、prior_versions_index | 跨当前和历史数据连接研究 |
| `PatientID` | index、prior_versions_index | 跨当前和历史数据连接患者 |
| `analysis_result_id` | index、analysis_results_index | 将序列连接到分析结果元数据（注释、分割） |
| `source_DOI` | index、analysis_results_index | 按出版DOI连接 |
| `crdc_series_uuid` | index、prior_versions_index | 按CRDC唯一标识符连接 |
| `Modality` | index、prior_versions_index | 按成像模态过滤 |
| `SeriesInstanceUID` | index、seg_index、ann_index、ann_group_index、contrast_index | 将分割/注释/对比度序列连接到其索引元数据 |
| `segmented_SeriesInstanceUID` | seg_index → index | 将分割连接到其源图像序列（连接seg_index.segmented_SeriesInstanceUID = index.SeriesInstanceUID） |
| `referenced_SeriesInstanceUID` | ann_index → index | 将注释连接到其源图像序列（连接ann_index.referenced_SeriesInstanceUID = index.SeriesInstanceUID） |
| `SeriesInstanceUID` | index, volume_geometry_index | 将序列连接到其3D几何验证结果（连接index.SeriesInstanceUID = volume_geometry_index.SeriesInstanceUID） |
| `SeriesInstanceUID` / `referenced_SeriesInstanceUID` | index, rtstruct_index | 将RTSTRUCT序列连接到其元数据（index.SeriesInstanceUID = rtstruct_index.SeriesInstanceUID）；使用rtstruct_index.referenced_SeriesInstanceUID查找源图像序列 |

**注意：** `Subjects`、`Updated`和`Description`出现在多个表中，但具有不同的含义（计数vs标识符、不同的更新上下文）。

有关详细连接示例、模式发现模式、关键列参考和DataFrame访问，请参阅`references/index_tables_guide.md`。

### 临床数据访问

```python
# 获取临床索引（也下载临床数据表）
client.fetch_index("clinical_index")

# 查询临床索引以查找可用表和列
tables = client.sql_query("SELECT DISTINCT table_name, column_label FROM clinical_index")

# 将特定临床表加载为DataFrame
clinical_df = client.get_clinical_table("table_name")
```

有关详细工作流，包括值映射模式和将临床数据与成像连接，请参阅`references/clinical_data_guide.md`。

## 数据访问选项

| 方法 | 需要身份验证 | 最适合 |
|--------|---------------|----------|
| `idc-index` | 否 | 关键查询和下载（推荐） |
| Direct Parquet（GCS） | 否 | 无需安装idc-index的快速查询；始终使用最新数据 |
| IDC门户 | 否 | 交互式探索、手动选择、基于浏览器的下载 |
| BigQuery | 是（GCP账户） | 复杂查询、完整DICOM元数据 |
| DICOMweb代理 | 否 | 通过DICOMweb API进行工具集成 |
| 云存储（S3/GCS） | 否 | 直接文件访问、批量下载、自定义流程 |

**云存储组织**

IDC在AWS S3和Google云存储之间镜像的公共云存储桶中维护所有DICOM文件。文件按CRDC UUID（而非DICOM UID）组织，以支持版本控制。

| 桶（AWS / GCS） | 许可证 | 内容 |
|--------------------|---------|---------|
| `idc-open-data` / `idc-open-data` | 无商业限制 | >90%的IDC数据 |
| `idc-open-data-two` / `idc-open-idc1` | 无商业限制 | 可能包含头部扫描的集合 |
| `idc-open-data-cr` / `idc-open-cr` | 商业使用受限（CC BY-NC） | ~4%的数据 |

文件存储为`<crdc_series_uuid>/<crdc_instance_uuid>.dcm`。通过AWS CLI、gsutil或s5cmd使用匿名访问免费访问（无出口费）。使用索引中的`series_aws_url`列获取S3 URL；GCS使用相同的路径结构。

有关桶详情、访问命令、UUID映射和版本控制，请参阅`references/cloud_storage_guide.md`。

**DICOMweb访问**

IDC数据可通过DICOMweb接口（Google云医疗API实现）获得，用于与PACS系统和DICOMweb兼容工具集成。

| 端点 | 身份验证 | 用例 |
|----------|------|----------|
| 公共代理 | 否 | 测试、适度查询、每日配额 |
| Google医疗 | 是（GCP） | 生产使用、更高配额 |

有关端点URL、代码示例、支持的操作和实施细节，请参阅`references/dicomweb_guide.md`。

**Direct Parquet访问**

所有idc-index元数据表都以Parquet文件形式发布到公共GCS桶（`idc-index-data-artifacts`），具有不受限制的CORS。这使得无需安装idc-index即可使用DuckDB或pandas查询，包括跨表连接和针对`volume_geometry_index`和`rtstruct_index`的查询。

有关URL模式、可用文件和DuckDB查询示例，请参阅`references/parquet_access_guide.md`。

## 安装和设置

**必需（用于基本访问）：**
```bash
pip install --upgrade idc-index
```

**重要：** 新的IDC数据发布将始终触发`idc-index`的新版本。安装时始终使用`--upgrade`标志，除非为了可重复性需要较旧版本。

**重要：** IDC数据版本v23是当前版本。始终验证您的版本：
```python
print(client.get_idc_version())  # 应该返回"v23"
```
如果您看到较旧版本，请使用以下命令升级：`pip install --upgrade idc-index`

**测试于：** idc-index 0.11.14（IDC数据版本v23）

**可选（用于数据分析）：**
```bash
pip install pandas numpy pydicom
```

## 核心功能

### 1. 数据发现和探索

发现IDC中可用的成像集合和数据：

```python
from idc_index import IDCClient

client = IDCClient()

# 从主索引获取摘要统计
query = """
SELECT
  collection_id,
  COUNT(DISTINCT PatientID) as patients,
  COUNT(DISTINCT SeriesInstanceUID) as series,
  SUM(series_size_MB) as size_mb
FROM index
GROUP BY collection_id
ORDER BY patients DESC
"""
collections_summary = client.sql_query(query)

# 对于更丰富的集合元数据，使用collections_index
client.fetch_index("collections_index")
collections_info = client.sql_query("""
    SELECT collection_id, CancerTypes, TumorLocations, Species, Subjects, SupportingData
    FROM collections_index
""")

# 对于分析结果（注释、分割），使用analysis_results_index
client.fetch_index("analysis_results_index")
analysis_info = client.sql_query("""
    SELECT analysis_result_id, analysis_result_title, Subjects, Collections, Modalities
    FROM analysis_results_index
""")
```

**`collections_index`**为每个集合提供策划的元数据：癌症类型、肿瘤位置、物种、受试者计数和支持数据类型 - 无需从主索引聚合。

**`analysis_results_index`**列出派生数据集（AI分割、专家注释、放射组学特征）及其源集合和模态。

### 2. 使用SQL查询元数据

使用SQL查询IDC迷你索引以查找特定数据集。

**首先，探索过滤器列的可用值：**
```python
from idc_index import IDCClient

client = IDCClient()

# 检查存在什么模态值
modalities = client.sql_query("""
    SELECT DISTINCT Modality, COUNT(*) as series_count
    FROM index
    GROUP BY Modality
    ORDER BY series_count DESC
""")
print(modalities)

# 检查MR模态存在什么BodyPartExamined值
body_parts = client.sql_query("""
    SELECT DISTINCT BodyPartExamined, COUNT(*) as series_count
    FROM index
    WHERE Modality = 'MR' AND BodyPartExamined IS NOT NULL
    GROUP BY BodyPartExamined
    ORDER BY series_count DESC
    LIMIT 20
""")
print(body_parts)
```

**然后使用验证的过滤器值查询：**
```python
# 查找乳腺MRI扫描（使用上述探索中的实际值）
results = client.sql_query("""
    SELECT
      collection_id,
      PatientID,
      SeriesInstanceUID,
      Modality,
      SeriesDescription,
      license_short_name
    FROM index
    WHERE Modality = 'MR'
      AND BodyPartExamined = 'BREAST'
    LIMIT 20
""")

# 作为pandas DataFrame访问结果
for idx, row in results.iterrows():
    print(f"患者：{row['PatientID']}，序列：{row['SeriesInstanceUID']}")
```

**要按癌症类型过滤，与`collections_index`连接：**
```python
client.fetch_index("collections_index")
results = client.sql_query("""
    SELECT i.collection_id, i.PatientID, i.SeriesInstanceUID, i.Modality
    FROM index i
    JOIN collections_index c ON i.collection_id = c.collection_id
    WHERE c.CancerTypes LIKE '%Breast%'
      AND i.Modality = 'MR'
    LIMIT 20
""")
```

**可用元数据字段**（使用`client.indices_overview`获取完整列表）：
- 标识符：collection_id、PatientID、StudyInstanceUID、SeriesInstanceUID
- 成像：Modality、BodyPartExamined、Manufacturer、ManufacturerModelName
- 临床：PatientAge、PatientSex、StudyDate
- 描述：StudyDescription、SeriesDescription
- 许可证：license_short_name

**注意：** 癌症类型在`collections_index.CancerTypes`中，而不在主`index`表中。

### 3. 下载DICOM文件

从IDC的云存储高效下载成像数据：

**下载整个集合：**
```python
from idc_index import IDCClient

client = IDCClient()

# 下载小集合（RIDER Pilot ~1GB）
client.download_from_selection(
    collection_id="rider_pilot",
    downloadDir="./data/rider"
)
```

**下载特定序列：**
```python
# 首先，查询序列UID
series_df = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
      AND collection_id = 'nlst'
    LIMIT 5
""")

# 仅下载那些序列
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/lung_ct"
)
```

**自定义目录结构：**

默认`dirTemplate`：`%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`

```python
# 简化层次结构（省略StudyInstanceUID级别）
client.download_from_selection(
    collection_id="tcga_luad",
    downloadDir="./data",
    dirTemplate="%collection_id/%PatientID/%Modality"
)
# 结果在：./data/tcga_luad/TCGA-05-4244/CT/

# 扁平结构（所有文件在一个目录中）
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/flat",
    dirTemplate=""
)
# 结果在：./data/flat/*.dcm
```

**下载的文件名：**

单个DICOM文件使用其CRDC实例UUID命名：`<crdc_instance_uuid>.dcm`（例如，`0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm`）。这种基于UUID的命名：
- 启用版本跟踪（UUID在文件内容更改时更改）
- 匹配云存储组织（`s3://idc-open-data/<crdc_series_uuid>/<crdc_instance_uuid>.dcm`）
- 与保存在文件元数据中的DICOM UID（SOPInstanceUID）不同

要识别文件，请在查询中使用`crdc_instance_uuid`列或从文件中读取DICOM元数据（SOPInstanceUID）。

### 命令行下载

安装`idc-index`后，`idc download`命令提供命令行访问下载功能。

**自动检测输入类型：** 清单文件路径，或标识符（collection_id、PatientID、StudyInstanceUID、SeriesInstanceUID、crdc_series_uuid）。

```bash
# 下载整个集合
idc download rider_pilot --download-dir ./data

# 按UID下载特定序列
idc download "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# 下载多个项目（逗号分隔）
idc download "tcga_luad,tcga_lusc" --download-dir ./data

# 从清单文件下载（自动检测）
idc download manifest.txt --download-dir ./data
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--download-dir` | 输出目录（默认：当前目录） |
| `--dir-template` | 目录层次结构模板（默认：`%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`） |
| `--log-level` | 详细程度：debug、info、warning、error、critical |

**清单文件：**

清单文件包含S3 URL（每行一个），可以是：
- 在队列选择后从IDC门户导出
- 由协作者共享以实现可重复的数据访问
- 从查询结果以编程方式生成

格式（每行一个S3 URL）：
```
s3://idc-open-data/cb09464a-c5cc-4428-9339-d7fa87cfe837/*
s3://idc-open-data/88f3990d-bdef-49cd-9b2b-4787767240f2/*
```

**示例：从Python查询生成清单：**

```python
from idc_index import IDCClient

client = IDCClient()

# 查询序列URL
results = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
""")

# 保存为清单文件
with open('ct_manifest.txt', 'w') as f:
    for url in results['series_aws_url']:
        f.write(url + '\n')
```

然后下载：
```bash
idc download ct_manifest.txt --download-dir ./ct_data
```

### 4. 可视化IDC图像

在浏览器中查看DICOM数据而无需下载：

```python
from idc_index import IDCClient
import webbrowser

client = IDCClient()

# 首先查询以获取有效UID
results = client.sql_query("""
    SELECT SeriesInstanceUID, StudyInstanceUID
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 1
""")

# 查看单个序列
viewer_url = client.get_viewer_URL(seriesInstanceUID=results.iloc[0]['SeriesInstanceUID'])
webbrowser.open(viewer_url)

# 查看研究中的所有序列（对于多序列检查（如MRI协议）有用）
viewer_url = client.get_viewer_URL(studyInstanceUID=results.iloc[0]['StudyInstanceUID'])
webbrowser.open(viewer_url)
```

该方法自动为放射学选择OHIF v3，或为切片显微镜选择SLIM。按研究查看在DICOM研究包含多个序列（例如，来自单个MRI会话的T1、T2、DWI序列）时很有用。

### 5. 理解和检查许可证

在使用前检查数据许可证（对于商业应用至关重要）：

```python
from idc_index import IDCClient

client = IDCClient()

# 检查所有集合的许可证
query = """
SELECT DISTINCT
  collection_id,
  license_short_name,
  COUNT(DISTINCT SeriesInstanceUID) as series_count
FROM index
GROUP BY collection_id, license_short_name
ORDER BY collection_id
"""

licenses = client.sql_query(query)
print(licenses)
```

**IDC中的许可证类型：**
- **CC BY 4.0** / **CC BY 3.0**（~97%的数据）- 允许商业使用，需署名
- **CC BY-NC 4.0** / **CC BY-NC 3.0**（~3%的数据）- 仅非商业使用
- **自定义许可证**（罕见）- 某些集合有特定条款（例如，NLM条款和条件）

**重要：** 在出版物或商业应用中使用IDC数据之前，始终检查许可证。每个DICOM文件在元数据中标记有其特定许可证。

### 为署名生成引用

`source_DOI`列包含DOI，链接到描述数据生成方式的出版物。要满足署名要求，使用`citations_from_selection()`生成正确格式的引用：

```python
from idc_index import IDCClient

client = IDCClient()

# 获取集合的引用（默认APA格式）
citations = client.citations_from_selection(collection_id="rider_pilot")
for citation in citations:
    print(citation)

# 获取特定序列的引用
results = client.sql_query("""
    SELECT SeriesInstanceUID FROM index
    WHERE collection_id = 'tcga_luad' LIMIT 5
""")
citations = client.citations_from_selection(
    seriesInstanceUID=list(results['SeriesInstanceUID'].values)
)

# 替代格式：BibTeX（用于LaTeX文档）
bibtex_citations = client.citations_from_selection(
    collection_id="tcga_luad",
    citation_format=IDCClient.CITATION_FORMAT_BIBTEX
)
```

**参数：**
- `collection_id`：按集合过滤
- `patientId`：按患者ID过滤
- `studyInstanceUID`：按研究UID过滤
- `seriesInstanceUID`：按序列UID过滤
- `citation_format`：使用`IDCClient.CITATION_FORMAT_*`常量：
  - `CITATION_FORMAT_APA`（默认）- APA样式
  - `CITATION_FORMAT_BIBTEX` - BibTeX用于LaTeX
  - `CITATION_FORMAT_JSON` - CSL JSON
  - `CITATION_FORMAT_TURTLE` - RDF Turtle

**最佳实践：** 使用IDC数据发布结果时，包含生成的引用以正确归属数据源并满足许可证要求。

### 6. 批量处理和过滤

使用过滤高效处理大型数据集：

```python
from idc_index import IDCClient
import pandas as pd

client = IDCClient()

# 查找来自GE扫描仪的胸部CT扫描
query = """
SELECT
  SeriesInstanceUID,
  PatientID,
  collection_id,
  ManufacturerModelName
FROM index
WHERE Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
  AND Manufacturer = 'GE MEDICAL SYSTEMS'
  AND license_short_name = 'CC BY 4.0'
LIMIT 100
"""

results = client.sql_query(query)

# 稍后保存清单
results.to_csv('lung_ct_manifest.csv', index=False)

# 分批下载以避免超时
batch_size = 10
for i in range(0, len(results), batch_size):
    batch = results.iloc[i:i+batch_size]
    client.download_from_selection(
        seriesInstanceUID=list(batch['SeriesInstanceUID'].values),
        downloadDir=f"./data/batch_{i//batch_size}"
    )
```

### 7. 使用BigQuery进行高级查询

对于需要完整DICOM元数据、复杂JOIN、临床数据表或私有DICOM元素的查询，使用Google BigQuery。需要启用计费的GCP账户。

**快速参考：**
- 数据集：`bigquery-public-data.idc_current.*`
- 主表：`dicom_all`（组合元数据）
- 完整元数据：`dicom_metadata`（所有DICOM标签）
- 私有元素：`OtherElements`列（供应商特定标签，如扩散b值）

有关设置、表模式、查询模式、私有元素访问和成本优化的详细信息，请参阅`references/bigquery_guide.md`。

**在使用BigQuery之前**，始终检查专门的索引表是否已有您需要的元数据：
1. 使用`client.indices_overview`或[idc-index索引参考](https://idc-index.readthedocs.io/en/latest/indices_reference.html)发现所有可用表及其列
2. 获取相关索引：`client.fetch_index("table_name")`
3. 使用`client.sql_query()`本地查询（免费，无需GCP账户）

常用专用索引：`seg_index`（分割）、`ann_index` / `ann_group_index`（显微镜注释）、`sm_index`（切片显微镜）、`collections_index`（集合元数据）。仅当您需要私有DICOM元素或任何索引中不存在的属性时才使用BigQuery。

**需要BigQuery的用例（无idc-index等效项）：**
- **每段解剖搜索** — `seg_index`提供序列级SEG元数据，但BigQuery `segmentations`表单独公开每个段及其DICOM编码结构名称（例如，查找包含"肝脏"或"肿瘤"段的所有SEG序列）
- **来自SR的定量测量** — BigQuery `quantitative_measurements`表包含从DICOM SR TID1500对象中预先提取的放射组学特征（体积、直径、形状描述符、纹理、强度统计）；无idc-index等效项
- **来自SR的定性测量** — BigQuery `qualitative_measurements`表包含来自DICOM SR TID1500的编码评估（恶性度评级、钙化、纹理、边缘）；无idc-index等效项

有关这些表的模式、列描述和查询示例，请参阅`references/bigquery_guide.md`。

### 8. 工具选择指南

| 任务 | 工具 | 参考 |
|------|------|-----------|
| 编程查询和下载 | `idc-index` | 此文档 |
| 交互式探索 | IDC门户 | https://portal.imaging.datacommons.cancer.gov/explore/ |
| 复杂元数据查询 | BigQuery | `references/bigquery_guide.md` |
| 3D可视化和分析 | SlicerIDCBrowser | https://github.com/ImagingDataCommons/SlicerIDCBrowser |

**默认选择：** 对于大多数任务使用`idc-index`（无需身份验证、简单API、批量下载）。

### 9. 与分析流程集成

将IDC数据集成到成像分析工作流中：

**读取下载的DICOM文件：**
```python
import pydicom
import os

# 从下载的序列读取DICOM文件
series_dir = "./data/rider/rider_pilot/RIDER-1007893286/CT_1.3.6.1..."

dicom_files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)
               if f.endswith('.dcm')]

# 加载第一张图像
ds = pydicom.dcmread(dicom_files[0])
print(f"患者ID：{ds.PatientID}")
print(f"模态：{ds.Modality}")
print(f"图像形状：{ds.pixel_array.shape}")
```

**从CT序列构建3D体积：**
```python
import pydicom
import numpy as np
from pathlib import Path

def load_ct_series(series_path):
    """将CT序列加载为3D numpy数组"""
    files = sorted(Path(series_path).glob('*.dcm'))
    slices = [pydicom.dcmread(str(f)) for f in files]

    # 按切片位置排序
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    # 堆叠为3D数组
    volume = np.stack([s.pixel_array for s in slices])

    return volume, slices[0]  # 返回体积和第一张切片的元数据

volume, metadata = load_ct_series("./data/lung_ct/series_dir")
print(f"体积形状：{volume.shape}")  # (z, y, x)
```

**与SimpleITK集成：**
```python
import SimpleITK as sitk
from pathlib import Path

# 读取DICOM序列
series_path = "./data/ct_series"
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(series_path)
reader.SetFileNames(dicom_names)
image = reader.Execute()

# 应用处理
smoothed = sitk.CurvatureFlow(image1=image, timeStep=0.125, numberOfIterations=5)

# 保存为NIfTI
sitk.WriteImage(smoothed, "processed_volume.nii.gz")
```

## 常见用例

有关完整的端到端工作流示例，请参阅`references/use_cases.md`，包括：
- 从肺部CT扫描构建深度学习训练数据集
- 比较扫描仪制造商之间的图像质量
- 下载前在浏览器中预览数据
- 商业使用的许可证感知批量下载

## 最佳实践

- **在生成响应之前验证IDC版本** - 始终在会话开始时调用`client.get_idc_version()`以确认您正在使用预期的数据版本（当前v23）。如果使用较旧版本，建议`pip install --upgrade idc-index`
- **使用前检查许可证** - 始终查询`license_short_name`字段并尊重许可条款（CC BY vs CC BY-NC）
- **为署名生成引用** - 使用`citations_from_selection()`从`source_DOI`值获取正确格式的引用；在出版物中包含这些引用
- **从小查询开始** - 探索时使用`LIMIT`子句以避免长时间下载并了解数据结构
- **使用迷你索引进行简单查询** - 仅在需要全面元数据或复杂JOIN时使用BigQuery
- **使用dirTemplate组织下载** - 使用有意义的目录结构，如`%collection_id/%PatientID/%Modality`
- **缓存查询结果** - 将DataFrame保存到CSV文件以避免重新查询并确保可重复性
- **首先估计大小** - 下载前检查集合大小 - 某些集合大小为太字节！
- **保存清单** - 始终保存带有序列UID的查询结果以实现可重复性和数据来源
- **阅读文档** - IDC数据结构和元数据字段记录在https://learn.canceridc.dev/
- **使用IDC论坛** - 在https://discourse.canceridc.dev/搜索问题/答案并向IDC维护者和用户提问

## 故障排除

**问题：** `ModuleNotFoundError: No module named 'idc_index'`
- **原因：** 未安装idc-index软件包
- **解决方案：** 使用`pip install --upgrade idc-index`安装

**问题：** 下载失败，连接超时
- **原因：** 网络不稳定或下载大小过大
- **解决方案：**
  - 分批下载（例如，每次10-20个序列）
  - 检查网络连接
  - 使用`dirTemplate`按批次组织下载
  - 实施带延迟的重试逻辑

**问题：** `BigQuery quota exceeded`或计费错误
- **原因：** BigQuery需要启用计费的GCP项目
- **解决方案：** 对简单查询使用idc-index迷你索引（无需计费），或参阅`references/bigquery_guide.md`以获取成本优化提示

**问题：** 未找到序列UID或未返回数据
- **原因：** UID拼写错误、数据不在当前IDC版本中，或字段名称错误
- **解决方案：**
  - 检查数据是否在当前IDC版本中（某些旧数据可能已弃用）
  - 使用`LIMIT 5`首先测试查询
  - 对照元数据模式文档检查字段名称

**问题：** 下载的DICOM文件无法打开
- **原因：** 下载损坏或查看器不兼容
- **解决方案：**
  - 检查DICOM对象类型（Modality和SOPClassUID属性）- 某些对象类型需要专用工具
  - 验证文件完整性（检查文件大小）
  - 使用pydicom验证：`pydicom.dcmread(file, force=True)`
  - 尝试不同的DICOM查看器（3D Slicer、Horos、RadiAnt、QuPath）
  - 重新下载序列

## 常见SQL查询模式

有关快速参考SQL模式，请参阅`references/sql_patterns.md`，包括：
- 过滤器值发现（模态、身体部位、制造商）
- 注释和分割查询（包括seg_index、ann_index连接）
- 切片显微镜查询（sm_index模式）
- 下载大小估计
- 临床数据连接

有关分割和注释的详细信息，也请参阅`references/digital_pathology_guide.md`。

## 相关技能

以下技能补充IDC工作流以进行下游分析和可视化：

### DICOM处理
- **pydicom** - 读取、写入和操作下载的DICOM文件。用于提取像素数据、读取元数据、匿名化和格式转换。对于处理IDC放射学数据（CT、MR、PET）至关重要。

### 病理学和切片显微镜
有关DICOM兼容工具（highdicom、wsidicom、TIA-Toolbox、Slim查看器），请参阅`references/digital_pathology_guide.md`。

### 元数据可视化
- **matplotlib** - 低级绘图以实现完全自定义。用于创建汇总IDC查询结果的静态图表（模态的条形图、序列计数的直方图等）。
- **seaborn** - 带有pandas集成的统计可视化。用于快速探索IDC元数据分布、变量之间的关系以及具有吸引人默认值的分类比较。
- **plotly** - 交互式可视化。当您需要悬停信息、缩放和平移以探索IDC元数据，或创建集合统计信息的可嵌入仪表板时使用。

### 数据探索
- **exploratory-data-analysis** - 对科学数据文件进行全面EDA。在下载IDC数据后使用以了解分析前的文件结构、质量和特征。

## 资源

### 模式参考（主要来源）

**始终使用`client.indices_overview`获取当前列模式。** 这确保与安装的idc-index版本的准确性：

```python
# 获取任何表的所有列名和类型
schema = client.indices_overview["index"]["schema"]
columns = [(c['name'], c['type'], c.get('description', '')) for c in schema['columns']]
```

### 参考文档

有关完整参考指南列表，请参阅顶部的快速导航部分，并附带决策触发器。

- **[indices_reference](https://idc-index.readthedocs.io/en/latest/indices_reference.html)** - 索引表的外部文档（可能领先于安装版本）

### 外部链接

- **IDC门户**：https://portal.imaging.datacommons.cancer.gov/explore/
- **文档**：https://learn.canceridc.dev/
- **教程**：https://github.com/ImagingDataCommons/IDC-Tutorials
- **用户论坛**：https://discourse.canceridc.dev/
- **idc-index GitHub**：https://github.com/ImagingDataCommons/idc-index
- **引用**：Fedorov, A., et al. "National Cancer Institute Imaging Data Commons: Toward Transparency, Reproducibility, and Scalability in Imaging Artificial Intelligence." RadioGraphics 43.12 (2023). https://doi.org/10.1148/rg.230180

### 技能更新

此技能版本在技能元数据中可用。要检查更新：
- 访问[releases页面](https://github.com/ImagingDataCommons/idc-claude-skill/releases)
- 在GitHub上观察仓库（Watch → Custom → Releases）
