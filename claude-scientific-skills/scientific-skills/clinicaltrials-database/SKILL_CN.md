---
name: clinicaltrials-database
description: 通过 API v2 查询 ClinicalTrials.gov。按疾病、药物、位置、状态或阶段搜索试验。通过 NCT ID 检索试验详细信息,导出数据,用于临床研究和患者匹配。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# ClinicalTrials.gov 数据库

## 概述

ClinicalTrials.gov 是由美国国家医学图书馆维护的全球性临床研究综合注册表。访问 API v2 以搜索试验、检索详细研究信息、按各种标准筛选以及导出数据进行分析。API 是公开的(无需身份验证),速率限制约为每分钟 50 个请求,支持 JSON 和 CSV 格式。

## 何时使用此技能

在以下情况下使用此技能:

- **患者匹配** - 为特定疾病或患者人群查找招募试验
- **研究分析** - 分析临床试验趋势、结果或研究设计
- **药物/干预研究** - 识别测试特定药物或干预措施的试验
- **地理搜索** - 查找特定地点或区域的试验
- **主办机构/组织跟踪** - 查找由特定机构进行的试验
- **数据导出** - 提取临床试验数据以进行进一步分析或报告
- **试验监测** - 跟踪特定试验的状态更新或结果
- **资格筛选** - 审查试验的纳入/排除标准

## 快速开始

### 基本搜索查询

使用辅助脚本搜索临床试验:

```bash
cd scientific-databases/clinicaltrials-database/scripts
python3 query_clinicaltrials.py
```

或直接使用 Python 和 `requests` 库:

```python
import requests

url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.cond": "breast cancer",
    "filter.overallStatus": "RECRUITING",
    "pageSize": 10
}

response = requests.get(url, params=params)
data = response.json()

print(f"Found {data['totalCount']} trials")
```

### 检索特定试验

使用其 NCT ID 获取有关试验的详细信息:

```python
import requests

nct_id = "NCT04852770"
url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}"

response = requests.get(url)
study = response.json()

# 访问特定模块
title = study['protocolSection']['identificationModule']['briefTitle']
status = study['protocolSection']['statusModule']['overallStatus']
```

## 核心功能

### 1. 按疾病/状况搜索

使用 `query.cond` 参数搜索研究特定疾病或状况的试验。

**示例: 查找招募中的糖尿病试验**
```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="type 2 diabetes",
    status="RECRUITING",
    page_size=20,
    sort="LastUpdatePostDate:desc"
)

print(f"Found {results['totalCount']} recruiting diabetes trials")
for study in results['studies']:
    protocol = study['protocolSection']
    nct_id = protocol['identificationModule']['nctId']
    title = protocol['identificationModule']['briefTitle']
    print(f"{nct_id}: {title}")
```

**常见用例:**
- 查找罕见疾病的试验
- 识别合并症试验
- 跟踪特定诊断的试验可用性

### 2. 按干预/药物搜索

使用 `query.intr` 参数搜索测试特定干预措施、药物、设备或程序的试验。

**示例: 查找测试帕博利珠单抗的 3 期试验**
```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    intervention="Pembrolizumab",
    status=["RECRUITING", "ACTIVE_NOT_RECRUITING"],
    page_size=50
)

# 在结果中筛选 3 期
phase3_trials = [
    study for study in results['studies']
    if 'PHASE3' in study['protocolSection'].get('designModule', {}).get('phases', [])
]
```

**常见用例:**
- 药物开发跟踪
- 制药公司的竞争情报
- 临床医生的治疗选择研究

### 3. 地理搜索

使用 `query.locn` 参数查找特定位置的试验。

**示例: 查找纽约的癌症试验**
```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="cancer",
    location="New York",
    status="RECRUITING",
    page_size=100
)

# 提取位置详情
for study in results['studies']:
    locations_module = study['protocolSection'].get('contactsLocationsModule', {})
    locations = locations_module.get('locations', [])
    for loc in locations:
        if 'New York' in loc.get('city', ''):
            print(f"{loc['facility']}: {loc['city']}, {loc.get('state', '')}")
```

**常见用例:**
- 患者转诊至本地试验
- 地理试验分布分析
- 新试验的站点选择

### 4. 按主办机构/组织搜索

使用 `query.spons` 参数查找由特定组织进行的试验。

**示例: 查找由 NCI 赞助的试验**
```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    sponsor="National Cancer Institute",
    page_size=100
)

# 提取主办机构信息
for study in results['studies']:
    sponsor_module = study['protocolSection']['sponsorCollaboratorsModule']
    lead_sponsor = sponsor_module['leadSponsor']['name']
    collaborators = sponsor_module.get('collaborators', [])
    print(f"Lead: {lead_sponsor}")
    if collaborators:
        print(f"  Collaborators: {', '.join([c['name'] for c in collaborators])}")
```

**常见用例:**
- 跟踪机构研究组合
- 分析资助组织优先事项
- 识别合作机会

### 5. 按研究状态筛选

使用 `filter.overallStatus` 参数按招募或完成状态筛选试验。

**有效状态值:**
- `RECRUITING` - 当前正在招募参与者
- `NOT_YET_RECRUITING` - 尚未开放招募
- `ENROLLING_BY_INVITATION` - 仅通过邀请招募
- `ACTIVE_NOT_RECRUITING` - 活跃但不再招募
- `SUSPENDED` - 暂时停止
- `TERMINATED` - 过早停止
- `COMPLETED` - 研究已结束
- `WITHDRAWN` - 入组前撤回

**示例: 查找最近完成且有结果的试验**
```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="alzheimer disease",
    status="COMPLETED",
    sort="LastUpdatePostDate:desc",
    page_size=50
)

# 筛选有结果的试验
trials_with_results = [
    study for study in results['studies']
    if study.get('hasResults', False)
]

print(f"Found {len(trials_with_results)} completed trials with results")
```

### 6. 检索详细研究信息

获取特定试验的全面信息,包括资格标准、结果、联系方式和位置。

**示例: 提取资格标准**
```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
eligibility = study['protocolSection']['eligibilityModule']

print(f"Eligible Ages: {eligibility.get('minimumAge')} - {eligibility.get('maximumAge')}")
print(f"Eligible Sex: {eligibility.get('sex')}")
print(f"\nInclusion Criteria:")
print(eligibility.get('eligibilityCriteria'))
```

**示例: 提取联系信息**
```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
contacts_module = study['protocolSection']['contactsLocationsModule']

# 总体联系方式
if 'centralContacts' in contacts_module:
    for contact in contacts_module['centralContacts']:
        print(f"Contact: {contact.get('name')}")
        print(f"Phone: {contact.get('phone')}")
        print(f"Email: {contact.get('email')}")

# 研究地点
if 'locations' in contacts_module:
    for location in contacts_module['locations']:
        print(f"\nFacility: {location.get('facility')}")
        print(f"City: {location.get('city')}, {location.get('state')}")
        if location.get('status'):
            print(f"Status: {location['status']}")
```

### 7. 分页和批量数据检索

高效处理大型结果集使用分页。

**示例: 检索所有匹配的试验**
```python
from scripts.query_clinicaltrials import search_with_all_results

# 获取所有试验(自动处理分页)
all_trials = search_with_all_results(
    condition="rare disease",
    status="RECRUITING"
)

print(f"Retrieved {len(all_trials)} total trials")
```

**示例: 手动分页控制**
```python
from scripts.query_clinicaltrials import search_studies

all_studies = []
page_token = None
max_pages = 10  # 限制以避免过多请求

for page in range(max_pages):
    results = search_studies(
        condition="cancer",
        page_size=1000,  # 最大页面大小
        page_token=page_token
    )

    all_studies.extend(results['studies'])

    # 检查下一页
    page_token = results.get('pageToken')
    if not page_token:
        break

print(f"Retrieved {len(all_studies)} studies across {page + 1} pages")
```

### 8. 数据导出为 CSV

将试验数据导出为 CSV 格式,以便在电子表格软件或数据分析工具中分析。

**示例: 导出为 CSV 文件**
```python
from scripts.query_clinicaltrials import search_studies

# 请求 CSV 格式
results = search_studies(
    condition="heart disease",
    status="RECRUITING",
    format="csv",
    page_size=1000
)

# 保存到文件
with open("heart_disease_trials.csv", "w") as f:
    f.write(results)

print("Data exported to heart_disease_trials.csv")
```

**注意:** CSV 格式返回字符串而不是 JSON 字典。

### 9. 提取和总结研究信息

提取关键信息以进行快速概述或报告。

**示例: 创建试验摘要**
```python
from scripts.query_clinicaltrials import get_study_details, extract_study_summary

# 获取详细信息并提取摘要
study = get_study_details("NCT04852770")
summary = extract_study_summary(study)

print(f"NCT ID: {summary['nct_id']}")
print(f"Title: {summary['title']}")
print(f"Status: {summary['status']}")
print(f"Phase: {', '.join(summary['phase'])}")
print(f"Enrollment: {summary['enrollment']}")
print(f"Last Update: {summary['last_update']}")
print(f"\nBrief Summary:\n{summary['brief_summary']}")
```

### 10. 组合查询策略

组合多个筛选器进行针对性搜索。

**示例: 多标准搜索**
```python
from scripts.query_clinicaltrials import search_studies

# 查找加利福尼亚州的 2/3 期免疫治疗肺癌试验
results = search_studies(
    condition="lung cancer",
    intervention="immunotherapy",
    location="California",
    status=["RECRUITING", "NOT_YET_RECRUITING"],
    page_size=100
)

# 进一步按阶段筛选
phase2_3_trials = [
    study for study in results['studies']
    if any(phase in ['PHASE2', 'PHASE3']
           for phase in study['protocolSection'].get('designModule', {}).get('phases', []))
]

print(f"Found {len(phase2_3_trials)} Phase 2/3 immunotherapy trials")
```

## 资源

### scripts/query_clinicaltrials.py

为常见查询模式提供辅助函数的全面 Python 脚本:

- `search_studies()` - 使用各种筛选器搜索试验
- `get_study_details()` - 检索特定试验的完整信息
- `search_with_all_results()` - 自动分页遍历所有结果
- `extract_study_summary()` - 提取关键信息以进行快速概述

直接运行脚本以获取示例用法:
```bash
python3 scripts/query_clinicaltrials.py
```

### references/api_reference.md

详细的 API 文档,包括:
- 完整的端点规范
- 所有查询参数和有效值
- 响应数据结构和模块
- 常见用例及代码示例
- 错误处理和最佳实践
- 数据标准(ISO 8601 日期、CommonMark markdown)

在使用不熟悉的 API 功能或排查问题时加载此参考。

## 最佳实践

### 速率限制管理

API 的速率限制约为每分钟 50 个请求。对于批量数据检索:

1. 使用最大页面大小(1000)以最小化请求
2. 在速率限制错误(429 状态)上实施指数退避
3. 对于大规模数据收集,在请求之间添加延迟

```python
import time
import requests

def search_with_rate_limit(params):
    try:
        response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("Rate limited. Waiting 60 seconds...")
            time.sleep(60)
            return search_with_rate_limit(params)  # 重试
        raise
```

### 数据结构导航

API 响应具有嵌套结构。常见信息的路径:

- **NCT ID**: `study['protocolSection']['identificationModule']['nctId']`
- **标题**: `study['protocolSection']['identificationModule']['briefTitle']`
- **状态**: `study['protocolSection']['statusModule']['overallStatus']`
- **阶段**: `study['protocolSection']['designModule']['phases']`
- **资格**: `study['protocolSection']['eligibilityModule']`
- **位置**: `study['protocolSection']['contactsLocationsModule']['locations']`
- **干预**: `study['protocolSection']['armsInterventionsModule']['interventions']`

### 错误处理

始终为网络请求实施适当的错误处理:

```python
import requests

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError as e:
    print(f"JSON decode error: {e}")
```

### 处理缺失数据

并非所有试验都有完整信息。始终检查字段是否存在:

```python
# 使用 .get() 进行安全导航
phases = study['protocolSection'].get('designModule', {}).get('phases', [])
enrollment = study['protocolSection'].get('designModule', {}).get('enrollmentInfo', {}).get('count', 'N/A')

# 访问前检查
if 'resultsSection' in study:
    # 处理结果
    pass
```

## 技术规范

- **基础 URL**: `https://clinicaltrials.gov/api/v2`
- **身份验证**: 不需要(公开 API)
- **速率限制**: 每个约 50 个请求/分钟
- **响应格式**: JSON(默认)、CSV
- **最大页面大小**: 每个请求 1000 个研究
- **日期格式**: ISO 8601
- **文本格式**: 富文本字段的 CommonMark markdown
- **API 版本**: 2.0(2024 年 3 月发布)
- **API 规范**: OpenAPI 3.0

有关完整的技术细节,请参阅 `references/api_reference.md`。
