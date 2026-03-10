---
name: ena-database
description: 通过 API/FTP 访问欧洲核苷酸档案。检索 DNA/RNA 序列、原始读取（FASTQ）、按访问号的基因组组装，用于基因组学和生物信息学管道。支持多种格式。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# ENA 数据库

## 概述

欧洲核苷酸档案（ENA）是一个用于核苷酸序列数据和关联元数据的全面公共存储库。通过 REST API 和 FTP 访问和查询 DNA/RNA 序列、原始测序读取、基因组组装和功能注释，用于基因组学和生物信息学管道。

## 何时使用此技能

此技能应在以下情况下使用：

- 按访问号检索核苷酸序列或原始测序读取
- 按元数据标准搜索样本、研究或组装
- 下载 FASTQ 文件或基因组组装以进行分析
- 查询生物的分类信息
- 访问序列注释和功能数据
- 将 ENA 数据集成到生物信息学管道中
- 执行与相关数据库的交叉引用搜索
- 通过 FTP 或 Aspera 批量下载数据集

## 核心能力

### 1. 数据类型和结构

ENA 将数据组织为分层对象类型：

**研究/项目** - 对相关数据进行分组并控制发布日期。研究是引用存档数据的主要单位。

**样本** - 代表制备测序文库的生物材料单位。在提交大多数数据类型之前，必须注册样本。

**原始读取** - 包括：
- **实验**：关于测序方法、文库制备和仪器细节的元数据
- **运行**：对来自单次测序运行的数据文件的引用

**组装** - 各种完成水平的基因组、转录组、宏基因组或宏转录组组装。

**序列** - 存储在 EMBL 核苷酸序列数据库中的组装和注释序列，包括编码/非编码区域和功能注释。

**分析** - 序列数据的计算分析结果。

**分类记录** - 包括谱系和等级的分类信息。

### 2. 编程访问

ENA 为数据访问提供多个 REST API。有关详细的端点文档，请参阅 `references/api_reference.md`。

**关键 API：**

**ENA 门户 API** - 跨所有 ENA 数据类型的高级搜索功能
- 文档：https://www.ebi.ac.uk/ena/portal/api/doc
- 用于复杂查询和元数据搜索

**ENA 浏览器 API** - 记录和元数据的直接检索
- 文档：https://www.ebi.ac.uk/ena/browser/api/doc
- 用于按访问号下载特定记录
- 以 XML 格式返回数据

**ENA 分类 REST API** - 查询分类信息
- 访问谱系、等级和相关分类数据

**ENA 交叉引用服务** - 访问来自外部数据库的相关记录
- 端点：https://www.ebi.ac.uk/ena/xref/rest/

**CRAM 引用注册表** - 检索参考序列
- 端点：https://www.ebi.ac.uk/ena/cram/
- 按 MD5 或 SHA1 校验和查询

**速率限制**：所有 API 的速率限制为每秒 50 个请求。超过此限制将返回 HTTP 429（请求过多）。

### 3. 搜索和检索数据

**基于浏览器的搜索：**
- 跨所有字段的自由文本搜索
- 序列相似性搜索（BLAST 集成）
- 交叉引用搜索以查找相关记录
- 使用 Rulespace 查询构建器的高级搜索
- 按数据类型、日期范围、分类或元数据字段过滤
- 将结果下载为表格化元数据摘要或 XML 记录

**编程查询：**
- 使用门户 API 进行大规模高级搜索
- 按数据类型、日期范围、分类或元数据字段过滤
- 将结果下载为表格化元数据摘要或 XML 记录

**示例 API 查询模式：**
```python
import requests

# 搜索特定研究中的样本
base_url = "https://www.ebi.ac.uk/ena/portal/api/search"
params = {
    "result": "sample",
    "query": "study_accession=PRJEB1234",
    "format": "json",
    "limit": 100
}

response = requests.get(base_url, params=params)
samples = response.json()
```

### 4. 数据检索格式

**元数据格式：**
- XML（原生 ENA 格式）
- JSON（通过门户 API）
- TSV/CSV（表格化摘要）

**序列数据：**
- FASTQ（原始读取）
- BAM/CRAM（比对读取）
- FASTA（组装序列）
- EMBL 扁平文件格式（注释序列）

**下载方法：**
- 直接 API 下载（小文件）
- FTP 用于批量数据传输
- Aspera 用于大型数据集的高速传输
- enaBrowserTools 命令行实用程序用于批量下载

### 5. 常见用例

**按访问号检索原始测序读取：**
```python
# 使用浏览器 API 下载运行文件
accession = "ERR123456"
url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{accession}"
```

**搜索研究中的所有样本：**
```python
# 使用门户 API 列出样本
study_id = "PRJNA123456"
url = f"https://www.ebi.ac.uk/ena/portal/api/search?result=sample&query=study_accession={study_id}&format=tsv"
```

**查找特定生物的组装：**
```python
# 按分类搜索组装
organism = "Escherichia coli"
url = f"https://www.ebi.ac.uk/ena/portal/api/search?result=assembly&query=tax_tree({organism})&format=json"
```

**获取分类谱系：**
```python
# 查询分类 API
taxon_id = "562"  # E. coli
url = f"https://www.ebi.ac.uk/ena/taxonomy/rest/tax-id/{taxon_id}"
```

### 6. 与分析管道集成

**批量下载模式：**
1. 使用门户 API 搜索匹配标准的访问号
2. 从搜索结果中提取文件 URL
3. 通过 FTP 或使用 enaBrowserTools 下载文件
4. 在管道中处理下载的数据

**BLAST 集成：**
与 EBI 的 NCBI BLAST 服务（REST/SOAP API）集成，以对 ENA 序列进行序列相似性搜索。

### 7. 最佳实践

**速率限制：**
- 收到 HTTP 429 响应时实施指数退避
- 尽可能批处理请求以保持在 50 次/秒的限制内
- 对于大型数据集，使用批量下载工具而不是迭代 API 调用

**数据引用：**
- 发表时始终使用研究/项目访问号进行引用
- 包含使用的特定样本、运行或组装的访问号

**API 响应处理：**
- 在处理响应之前检查 HTTP 状态代码
- 使用适当的 XML 库（而不是正则表达式）解析 XML 响应
- 处理大型结果集的分页

**性能：**
- 使用 FTP/Aspera 下载大文件（>100MB）
- 如果只需要元数据，则优先使用 TSV/JSON 格式而不是 XML
- 处理许多记录时本地缓存分类查找

## 资源

此技能包含用于使用 ENA 的详细参考文档：

### references/

**api_reference.md** - 全面的 API 端点文档，包括：
- 门户 API 和浏览器 API 的详细参数
- 响应格式规范
- 高级查询语法和运算符
- 用于过滤和搜索的字段名称
- 常见 API 模式和示例

当构建复杂的 API 查询、调试 API 响应或需要特定参数详细信息时，请加载此参考。
