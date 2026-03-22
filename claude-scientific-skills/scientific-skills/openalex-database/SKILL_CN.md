---
name: openalex-database
description: 使用 OpenAlex 数据库查询和分析学术文献。当搜索学术论文、分析研究趋势、查找作者或机构的作品、跟踪引用、发现开放获取出版物或对 2.4 亿+ 学术作品进行文献计量分析时，应使用此技能。用于文献搜索、研究输出分析、引用分析和学术数据库查询。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# OpenAlex 数据库

## 概述

OpenAlex 是一个包含 2.4 亿+ 学术作品、作者、机构、主题、来源、出版商和资助者的综合开放目录。此技能提供了查询 OpenAlex API 的工具和工作流程，用于搜索文献、分析研究输出、跟踪引用和进行文献计量研究。

## 快速开始

### 基本设置

始终使用电子邮件地址初始化客户端以访问礼貌池（10 倍速率限制提升）：

```python
from scripts.openalex_client import OpenAlexClient

client = OpenAlexClient(email="your-email@example.edu")
```

### 安装要求

使用 uv 安装所需包：

```bash
uv pip install requests
```

无需 API 密钥 - OpenAlex 完全开放。

## 核心功能

### 1. 搜索论文

**用途**：通过标题、摘要或主题查找论文

```python
# 简单搜索
results = client.search_works(
    search="machine learning",
    per_page=100
)

# 带过滤器的搜索
results = client.search_works(
    search="CRISPR gene editing",
    filter_params={
        "publication_year": ">2020",
        "is_oa": "true"
    },
    sort="cited_by_count:desc"
)
```

### 2. 查找作者的作品

**用途**：获取特定研究人员的所有出版物

使用两步模式（实体名称 → ID → 作品）：

```python
from scripts.query_helpers import find_author_works

works = find_author_works(
    author_name="Jennifer Doudna",
    client=client,
    limit=100
)
```

**手动两步方法**：
```python
# 步骤 1：获取作者 ID
author_response = client._make_request(
    '/authors',
    params={'search': 'Jennifer Doudna', 'per-page': 1}
)
author_id = author_response['results'][0]['id'].split('/')[-1]

# 步骤 2：获取作品
works = client.search_works(
    filter_params={"authorships.author.id": author_id}
)
```

### 3. 查找机构的作品

**用途**：分析大学或组织的研究输出

```python
from scripts.query_helpers import find_institution_works

works = find_institution_works(
    institution_name="Stanford University",
    client=client,
    limit=200
)
```

### 4. 高被引论文

**用途**：查找领域内有影响力的论文

```python
from scripts.query_helpers import find_highly_cited_recent_papers

papers = find_highly_cited_recent_papers(
    topic="quantum computing",
    years=">2020",
    client=client,
    limit=100
)
```

### 5. 开放获取论文

**用途**：查找免费可用的研究

```python
from scripts.query_helpers import get_open_access_papers

papers = get_open_access_papers(
    search_term="climate change",
    client=client,
    oa_status="any",  # 或 "gold", "green", "hybrid", "bronze"
    limit=200
)
```

### 6. 出版物趋势分析

**用途**：跟踪随时间的研究输出

```python
from scripts.query_helpers import get_publication_trends

trends = get_publication_trends(
    search_term="artificial intelligence",
    filter_params={"is_oa": "true"},
    client=client
)

# 排序和显示
for trend in sorted(trends, key=lambda x: x['key'])[-10:]:
    print(f"{trend['key']}: {trend['count']} publications")
```

### 7. 研究输出分析

**用途**：对作者或机构研究进行综合分析

```python
from scripts.query_helpers import analyze_research_output

analysis = analyze_research_output(
    entity_type='institution',  # 或 'author'
    entity_name='MIT',
    client=client,
    years='>2020'
)

print(f"Total works: {analysis['total_works']}")
print(f"Open access: {analysis['open_access_percentage']}%")
print(f"Top topics: {analysis['top_topics'][:5]}")
```

### 8. 批量查找

**用途**：高效获取多个 DOI、ORCID 或 ID 的信息

```python
dois = [
    "https://doi.org/10.1038/s41586-021-03819-2",
    "https://doi.org/10.1126/science.abc1234",
    # ... 最多 50 个 DOI
]

works = client.batch_lookup(
    entity_type='works',
    ids=dois,
    id_field='doi'
)
```

### 9. 随机抽样

**用途**：获取用于分析的代表性样本

```python
# 小样本
works = client.sample_works(
    sample_size=100,
    seed=42,  # 用于可重现性
    filter_params={"publication_year": "2023"}
)

# 大样本 (>10k) - 自动处理多个请求
works = client.sample_works(
    sample_size=25000,
    seed=42,
    filter_params={"is_oa": "true"}
)
```

### 10. 引用分析

**用途**：查找引用特定作品的论文

```python
# 获取作品
work = client.get_entity('works', 'https://doi.org/10.1038/s41586-021-03819-2')

# 使用 cited_by_api_url 获取引用论文
import requests
citing_response = requests.get(
    work['cited_by_api_url'],
    params={'mailto': client.email, 'per-page': 200}
)
citing_works = citing_response.json()['results']
```

### 11. 主题和学科分析

**用途**：了解研究重点领域

```python
# 获取机构的顶级主题
topics = client.group_by(
    entity_type='works',
    group_field='topics.id',
    filter_params={
        "authorships.institutions.id": "I136199984",  # MIT
        "publication_year": ">2020"
    }
)

for topic in topics[:10]:
    print(f"{topic['key_display_name']}: {topic['count']} works")
```

### 12. 大规模数据提取

**用途**：下载大型数据集用于分析

```python
# 分页获取所有结果
all_papers = client.paginate_all(
    endpoint='/works',
    params={
        'search': 'synthetic biology',
        'filter': 'publication_year:2020-2024'
    },
    max_results=10000
)

# 导出到 CSV
import csv
with open('papers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Year', 'Citations', 'DOI', 'OA Status'])

    for paper in all_papers:
        writer.writerow([
            paper.get('title', 'N/A'),
            paper.get('publication_year', 'N/A'),
            paper.get('cited_by_count', 0),
            paper.get('doi', 'N/A'),
            paper.get('open_access', {}).get('oa_status', 'closed')
        ])
```

## 关键最佳实践

### 始终使用电子邮件获取礼貌池
添加电子邮件以获得 10 倍速率限制（1 请求/秒 → 10 请求/秒）：
```python
client = OpenAlexClient(email="your-email@example.edu")
```

### 对实体查找使用两步模式
永远不要直接按实体名称过滤 - 始终先获取 ID：
```python
# ✅ 正确
# 1. 搜索实体 → 获取 ID
# 2. 按 ID 过滤

# ❌ 错误
# filter=author_name:Einstein  # 这不起作用！
```

### 使用最大页面大小
始终使用 `per-page=200` 进行高效数据检索：
```python
results = client.search_works(search="topic", per_page=200)
```

### 批量处理多个 ID
对多个 ID 使用 batch_lookup() 而不是单个请求：
```python
# ✅ 正确 - 50 个 DOI 一次请求
works = client.batch_lookup('works', doi_list, 'doi')

# ❌ 错误 - 50 个单独请求
for doi in doi_list:
    work = client.get_entity('works', doi)
```

### 对随机数据使用 Sample 参数
使用 `sample_works()` 带种子进行可重现的随机抽样：
```python
# ✅ 正确
works = client.sample_works(sample_size=100, seed=42)

# ❌ 错误 - 随机页码会使结果产生偏差
# 使用随机页码不会给出真正的随机样本
```

### 只选择需要的字段
通过选择特定字段减少响应大小：
```python
results = client.search_works(
    search="topic",
    select=['id', 'title', 'publication_year', 'cited_by_count']
)
```

## 常见过滤模式

### 日期范围
```python
# 单年
filter_params={"publication_year": "2023"}

# 年份之后
filter_params={"publication_year": ">2020"}

# 范围
filter_params={"publication_year": "2020-2024"}
```

### 多个过滤器 (AND)
```python
# 所有条件必须匹配
filter_params={
    "publication_year": ">2020",
    "is_oa": "true",
    "cited_by_count": ">100"
}
```

### 多个值 (OR)
```python
# 任何机构匹配
filter_params={
    "authorships.institutions.id": "I136199984|I27837315"  # MIT 或 Harvard
}
```

### 合作（属性内的 AND）
```python
# 具有来自两个机构的作者的论文
filter_params={
    "authorships.institutions.id": "I136199984+I27837315"  # MIT 和 Harvard
}
```

### 否定
```python
# 排除类型
filter_params={
    "type": "!paratext"
}
```

## 实体类型

OpenAlex 提供这些实体类型：
- **works** - 学术文档（文章、书籍、数据集）
- **authors** - 具有明确身份的研究人员
- **institutions** - 大学和研究组织
- **sources** - 期刊、存储库、会议
- **topics** - 主题分类
- **publishers** - 出版组织
- **funders** - 资助机构

使用一致的模式访问任何实体类型：
```python
client.search_works(...)
client.get_entity('authors', author_id)
client.group_by('works', 'topics.id', filter_params={...})
```

## 外部 ID

直接使用外部标识符：
```python
# 作品的 DOI
work = client.get_entity('works', 'https://doi.org/10.7717/peerj.4375')

# 作者的 ORCID
author = client.get_entity('authors', 'https://orcid.org/0000-0003-1613-5981')

# 机构的 ROR
institution = client.get_entity('institutions', 'https://ror.org/02y3ad647')

# 来源的 ISSN
source = client.get_entity('sources', 'issn:0028-0836')
```

## 参考文档

### 详细 API 参考
请参阅 `references/api_guide.md` 了解：
- 完整的过滤语法
- 所有可用的端点
- 响应结构
- 错误处理
- 性能优化
- 速率限制详细信息

### 常见查询示例
请参阅 `references/common_queries.md` 了解：
- 完整的工作示例
- 实际用例
- 复杂查询模式
- 数据导出工作流程
- 多步骤分析程序

## 脚本

### openalex_client.py
主要 API 客户端，具有：
- 自动速率限制
- 指数退避重试逻辑
- 分页支持
- 批量操作
- 错误处理

用于完全控制的直接 API 访问。

### query_helpers.py
用于常见操作的高级辅助函数：
- `find_author_works()` - 按作者获取论文
- `find_institution_works()` - 从机构获取论文
- `find_highly_cited_recent_papers()` - 获取有影响力的论文
- `get_open_access_papers()` - 查找 OA 出版物
- `get_publication_trends()` - 分析随时间的趋势
- `analyze_research_output()` - 综合分析

用于具有简化界面的常见研究查询。

## 故障排除

### 速率限制
如果遇到 403 错误：
1. 确保请求中添加了电子邮件
2. 验证不超过 10 请求/秒
3. 客户端自动实现指数退避

### 空结果
如果搜索返回无结果：
1. 检查过滤语法（参见 `references/api_guide.md`）
2. 对实体查找使用两步模式（不要按名称过滤）
3. 验证实体 ID 格式正确

### 超时错误
对于大型查询：
1. 使用 `per-page=200` 进行分页
2. 使用 `select=` 限制返回的字段
3. 必要时拆分为更小的查询

## 速率限制

- **默认**：1 请求/秒，10 万请求/天
- **礼貌池（带电子邮件）**：10 请求/秒，10 万请求/天

始终通过向客户端提供电子邮件来为生产工作流程使用礼貌池。

## 注意事项

- 无需身份验证
- 所有数据都是开放和免费的
- 速率限制适用于全局，而不是每 IP
- 如果需要基于 LLM 的分析，请使用 LitLLM 与 OpenRouter（不要直接使用 Perplexity API）
- 客户端自动处理分页、重试和速率限制