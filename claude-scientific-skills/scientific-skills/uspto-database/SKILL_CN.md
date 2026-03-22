---
name: uspto-database
description: 访问USPTO API进行专利/商标搜索、审查历史（PEDS）、转让、引用、审查意见、TSDR，用于知识产权分析和现有技术搜索。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# USPTO数据库

## 概述

USPTO提供专门的专利和商标数据API。通过关键词/发明人/受让人搜索专利，通过PEDS检索审查历史，跟踪转让，分析引用和审查意见，访问TSDR获取商标信息，用于知识产权分析和现有技术搜索。

## 何时使用此技能

当以下情况时应使用此技能：

- **专利搜索**：按关键词、发明人、受让人、分类或日期查找专利
- **专利详情**：检索完整专利数据，包括权利要求、摘要、引用
- **商标搜索**：通过序列号或注册号查找商标
- **商标状态**：检查商标状态、所有权和审查历史
- **审查历史**：从PEDS（专利审查数据系统）访问专利审查数据
- **审查意见**：检索审查意见文本、引用和驳回
- **转让**：跟踪专利/商标所有权转移
- **引用**：分析专利引用（前向和后向）
- **诉讼**：访问专利诉讼记录
- **组合分析**：分析公司或发明人的专利/商标组合

## USPTO API生态系统

USPTO为不同数据需求提供多个专门的API：

### 核心API

1. **PatentSearch API** - 基于ElasticSearch的现代专利搜索（2025年5月取代了旧版PatentsView）
   - 按关键词、发明人、受让人、分类、日期搜索专利
   - 访问截至2025年6月30日的专利数据
   - 45次请求/分钟的速率限制
   - **基础URL**：`https://search.patentsview.org/api/v1/`

2. **PEDS（专利审查数据系统）** - 专利审查历史
   - 1981年至今的申请状态和交易历史
   - 审查意见日期和审查事件
   - 使用`uspto-opendata-python` Python库
   - **替代**：PAIR批量数据（PBD）- 已停用

3. **TSDR（商标状态与文档检索）** - 商标数据
   - 商标状态、所有权、审查历史
   - 按序列号或注册号搜索
   - **基础URL**：`https://tsdrapi.uspto.gov/ts/cd/`

### 其他API

4. **专利转让搜索** - 所有权记录和转移
5. **商标转让搜索** - 商标所有权变更
6. **增强引用API** - 专利引用分析
7. **审查意见文本检索** - 审查意见全文
8. **审查意见引用** - 审查意见中的引用
9. **审查意见驳回** - 驳回原因和类型
10. **PTAB API** - 专利审判和上诉委员会程序
11. **专利诉讼案件** - 联邦地区法院诉讼数据
12. **癌症登月数据集** - 癌症相关专利

## 快速开始

### API密钥注册

USPTO API需要API密钥。在以下地址注册：
**https://account.uspto.gov/api-manager/**

**PatentSearch API**的API密钥由PatentsView提供。在以下地址注册：
**https://patentsview.org/api-v01-information-page**

将API密钥设置为环境变量：
```bash
export USPTO_API_KEY="your_api_key_here"
export PATENTSVIEW_API_KEY="you_api_key_here"
```

### 辅助脚本

此技能包含用于常见操作的Python脚本：

- **`scripts/patent_search.py`** - 用于搜索专利的PatentSearch API客户端
- **`scripts/peds_client.py`** - 用于审查历史的PEDS客户端
- **`scripts/trademark_client.py`** - 用于商标数据的TSDR客户端

## 任务1：搜索专利

### 使用PatentSearch API

PatentSearch API使用JSON查询语言，带有各种运算符用于灵活搜索。

#### 基本专利搜索示例

**按摘要中的关键词搜索：**
```python
from scripts.patent_search import PatentSearchClient

client = PatentSearchClient()

# 搜索机器学习专利
results = client.search_patents({
    "_text_all": {"patent_abstract": "machine learning"}
})

for patent in results['patents']:
    print(f"{patent['patent_number']}: {patent['patent_title']}")
```

**按发明人搜索：**
```python
results = client.search_by_inventor("John Smith")
```

**按受让人/公司搜索：**
```python
results = client.search_by_assignee("Google")
```

**按日期范围搜索：**
```python
results = client.search_by_date_range("2024-01-01", "2024-12-31")
```

**按CPC分类搜索：**
```python
results = client.search_by_classification("H04N")  # 视频/图像技术
```

#### 高级专利搜索

使用逻辑运算符组合多个条件：

```python
results = client.advanced_search(
    keywords=["artificial", "intelligence"],
    assignee="Microsoft",
    start_date="2023-01-01",
    end_date="2024-12-31",
    cpc_codes=["G06N", "G06F"]  # AI和计算分类
)
```

#### 直接API使用

对于复杂查询，直接使用API：

```python
import requests

url = "https://search.patentsview.org/api/v1/patent"
headers = {
    "X-Api-Key": "YOUR_API_KEY",
    "Content-Type": "application/json"
}

query = {
    "q": {
        "_and": [
            {"patent_date": {"_gte": "2024-01-01"}},
            {"assignee_organization": {"_text_any": ["Google", "Alphabet"]}},
            {"cpc_subclass_id": ["G06N", "H04N"]}
        ]
    },
    "f": ["patent_number", "patent_title", "patent_date", "inventor_name"],
    "s": [{"patent_date": "desc"}],
    "o": {"per_page": 100, "page": 1}
}

response = requests.post(url, headers=headers, json=query)
results = response.json()
```

### 查询运算符

- **相等**：`{"field": "value"}` 或 `{"field": {"_eq": "value"}}`
- **比较**：`_gt`, `_gte`, `_lt`, `_lte`, `_neq`
- **文本搜索**：`_text_all`, `_text_any`, `_text_phrase`
- **字符串匹配**：`_begins`, `_contains`
- **逻辑**：`_and`, `_or`, `_not`

**最佳实践**：对文本字段使用`_text_*`运算符（比`_contains`或`_begins`更高效）

### 可用的专利端点

- `/patent` - 授权专利
- `/publication` - 预授权公开
- `/inventor` - 发明人信息
- `/assignee` - 受让人信息
- `/cpc_subclass`, `/cpc_at_issue` - CPC分类
- `/uspc` - 美国专利分类
- `/ipc` - 国际专利分类
- `/claims`, `/brief_summary_text`, `/detail_description_text` - 文本数据（测试版）

### 参考文档

见`references/patentsearch_api.md`获取完整的PatentSearch API文档，包括：
- 所有可用端点
- 完整字段参考
- 查询语法和示例
- 响应格式
- 速率限制和最佳实践

## 任务2：检索专利审查数据

### 使用PEDS（专利审查数据系统）

PEDS提供全面的审查历史，包括交易事件、状态变更和审查时间线。

#### 安装

```bash
uv pip install uspto-opendata-python
```

#### 基本PEDS使用

**获取申请数据：**
```python
from scripts.peds_client import PEDSHelper

helper = PEDSHelper()

# 通过申请号
app_data = helper.get_application("16123456")
print(f"标题: {app_data['title']}")
print(f"状态: {app_data['app_status']}")

# 通过专利号
patent_data = helper.get_patent("11234567")
```

**获取交易历史：**
```python
transactions = helper.get_transaction_history("16123456")

for trans in transactions:
    print(f"{trans['date']}: {trans['code']} - {trans['description']}")
```

**获取审查意见：**
```python
office_actions = helper.get_office_actions("16123456")

for oa in office_actions:
    if oa['code'] == 'CTNF':
        print(f"非最终驳回: {oa['date']}")
    elif oa['code'] == 'CTFR':
        print(f"最终驳回: {oa['date']}")
    elif oa['code'] == 'NOA':
        print(f"授权通知: {oa['date']}")
```

**获取状态摘要：**
```python
summary = helper.get_status_summary("16123456")

print(f"当前状态: {summary['current_status']}")
print(f"申请日期: {summary['filing_date']}")
print(f"审查时间: {summary['pendency_days']} 天")

if summary['is_patented']:
    print(f"专利号: {summary['patent_number']}")
    print(f"授权日期: {summary['issue_date']}")
```

#### 审查分析

分析审查模式：

```python
analysis = helper.analyze_prosecution("16123456")

print(f"总审查意见: {analysis['total_office_actions']}")
print(f"非最终驳回: {analysis['non_final_rejections']}")
print(f"最终驳回: {analysis['final_rejections']}")
print(f"授权: {analysis['allowance']}")
print(f"提交的答辩: {analysis['responses']}")
```

### 常见交易代码

- **CTNF** - 非最终驳回邮寄
- **CTFR** - 最终驳回邮寄
- **NOA** - 授权通知邮寄
- **WRIT** - 答辩提交
- **ISS.FEE** - 授权费支付
- **ABND** - 申请放弃
- **AOPF** - 审查意见邮寄

### 参考文档

见`references/peds_api.md`获取完整的PEDS文档，包括：
- 所有可用数据字段
- 交易代码参考
- Python库使用
- 组合分析示例

## 任务3：搜索和监控商标

### 使用TSDR（商标状态与文档检索）

访问商标状态、所有权和审查历史。

#### 基本商标使用

**通过序列号获取商标：**
```python
from scripts.trademark_client import TrademarkClient

client = TrademarkClient()

# 通过序列号
tm_data = client.get_trademark_by_serial("87654321")

# 通过注册号
tm_data = client.get_trademark_by_registration("5678901")
```

**获取商标状态：**
```python
status = client.get_trademark_status("87654321")

print(f"商标: {status['mark_text']}")
print(f"状态: {status['status']}")
print(f"申请日期: {status['filing_date']}")

if status['is_registered']:
    print(f"注册号: {status['registration_number']}")
    print(f"注册日期: {status['registration_date']}")
```

**检查商标健康状况：**
```python
health = client.check_trademark_health("87654321")

print(f"商标: {health['mark']}")
print(f"状态: {health['status']}")

for alert in health['alerts']:
    print(alert)

if health['needs_attention']:
    print("⚠️  此商标需要关注！")
```

#### 商标组合监控

监控多个商标：

```python
def monitor_portfolio(serial_numbers, api_key):
    """监控商标组合健康状况。"""
    client = TrademarkClient(api_key)

    results = {
        'active': [],
        'pending': [],
        'problems': []
    }

    for sn in serial_numbers:
        health = client.check_trademark_health(sn)

        if 'REGISTERED' in health['status']:
            results['active'].append(health)
        elif 'PENDING' in health['status'] or 'PUBLISHED' in health['status']:
            results['pending'].append(health)
        elif health['needs_attention']:
            results['problems'].append(health)

    return results
```

### 常见商标状态

- **REGISTERED** - 活跃注册商标
- **PENDING** - 审查中
- **PUBLISHED FOR OPPOSITION** - 异议期内
- **ABANDONED** - 申请放弃
- **CANCELLED** - 注册取消
- **SUSPENDED** - 审查暂停
- **REGISTERED AND RENEWED** - 注册续展

### 参考文档

见`references/trademark_api.md`获取完整的商标API文档，包括：
- TSDR API参考
- 商标转让搜索API
- 所有状态代码
- 审查历史访问
- 所有权跟踪

## 任务4：跟踪转让和所有权

### 专利和商标转让

专利和商标都有转让搜索API用于跟踪所有权变更。

#### 专利转让API

**基础URL**：`https://assignment-api.uspto.gov/patent/v1.4/`

**按专利号搜索：**
```python
import requests
import xml.etree.ElementTree as ET

def get_patent_assignments(patent_number, api_key):
    url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text  # 返回XML

assignments_xml = get_patent_assignments("11234567", api_key)
root = ET.fromstring(assignments_xml)

for assignment in root.findall('.//assignment'):
    recorded_date = assignment.find('recordedDate').text
    assignor = assignment.find('.//assignor/name').text
    assignee = assignment.find('.//assignee/name').text
    conveyance = assignment.find('conveyanceText').text

    print(f"{recorded_date}: {assignor} → {assignee}")
    print(f"  类型: {conveyance}\n")
```

**按公司名称搜索：**
```python
def find_company_patents(company_name, api_key):
    url = "https://assignment-api.uspto.gov/patent/v1.4/assignment/search"
    headers = {"X-Api-Key": api_key}
    data = {"criteria": {"assigneeName": company_name}}

    response = requests.post(url, headers=headers, json=data)
    return response.text
```

### 常见转让类型

- **ASSIGNMENT OF ASSIGNORS INTEREST** - 所有权转移
- **SECURITY AGREEMENT** - 抵押/担保权益
- **MERGER** - 公司合并
- **CHANGE OF NAME** - 名称变更
- **ASSIGNMENT OF PARTIAL INTEREST** - 部分所有权

## 任务5：访问其他USPTO数据

### 审查意见、引用和诉讼

多个专门的API提供额外的专利数据。

#### 审查意见文本检索

使用申请号检索审查意见全文。与PEDS集成以识别存在哪些审查意见，然后检索全文。

#### 增强引用API

分析专利引用：
- 前向引用（引用此专利的专利）
- 后向引用（引用的现有技术）
- 审查员vs申请人引用
- 引用上下文

#### 专利诉讼案件API

访问联邦地区法院专利诉讼记录：
- 74,623+诉讼记录
- 主张的专利
- 当事人和地点
- 案件结果

#### PTAB API

专利审判和上诉委员会程序：
- 多方审查（IPR）
- 授权后审查（PGR）
- 上诉决定

### 参考文档

见`references/additional_apis.md`获取关于以下内容的综合文档：
- 增强引用API
- 审查意见API（文本、引用、驳回）
- 专利诉讼案件API
- PTAB API
- 癌症登月数据集
- OCE状态/事件代码

## 完整分析示例

### 综合专利分析

组合多个API进行完整的专利情报分析：

```python
def comprehensive_patent_analysis(patent_number, api_key):
    """
    使用多个USPTO API进行完整的专利分析。
    """
    from scripts.patent_search import PatentSearchClient
    from scripts.peds_client import PEDSHelper

    results = {}

    # 1. 获取专利详情
    patent_client = PatentSearchClient(api_key)
    patent_data = patent_client.get_patent(patent_number)
    results['patent'] = patent_data

    # 2. 获取审查历史
    peds = PEDSHelper()
    results['prosecution'] = peds.analyze_prosecution(patent_number)
    results['status'] = peds.get_status_summary(patent_number)

    # 3. 获取转让历史
    import requests
    assign_url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    assign_resp = requests.get(assign_url, headers={"X-Api-Key": api_key})
    results['assignments'] = assign_resp.text if assign_resp.status_code == 200 else None

    # 4. 分析结果
    print(f"\n=== 专利 {patent_number} 分析 ===\n")
    print(f"标题: {patent_data['patent_title']}")
    print(f"受让人: {', '.join(patent_data.get('assignee_organization', []))}")
    print(f"授权日期: {patent_data['patent_date']}")

    print(f"\n审查情况:")
    print(f"  审查意见: {results['prosecution']['total_office_actions']}")
    print(f"  驳回: {results['prosecution']['non_final_rejections']} 非最终, {results['prosecution']['final_rejections']} 最终")
    print(f"  审查时间: {results['prosecution']['pendency_days']} 天")

    # 分析引用
    if 'cited_patent_number' in patent_data:
        print(f"\n引用:")
        print(f"  引用: {len(patent_data['cited_patent_number'])} 项专利")
    if 'citedby_patent_number' in patent_data:
        print(f"  被引用: {len(patent_data['citedby_patent_number'])} 项专利")

    return results
```

## 最佳实践

1. **API密钥管理**
   - 将API密钥存储在环境变量中
   - 永远不要将密钥提交到版本控制
   - 在所有USPTO API中使用相同的密钥

2. **速率限制**
   - PatentSearch: 45次请求/分钟
   - 对速率限制错误实现指数退避
   - 可能时缓存响应

3. **查询优化**
   - 对文本字段使用`_text_*`运算符（更高效）
   - 仅请求需要的字段以减少响应大小
   - 使用日期范围缩小搜索范围

4. **数据处理**
   - 并非所有专利/商标都填充了所有字段
   - 优雅处理缺失数据
   - 一致解析日期

5. **组合API**
   - 使用PatentSearch进行发现
   - 使用PEDS获取审查详情
   - 使用转让API进行所有权跟踪
   - 组合数据进行综合分析

## 重要说明

- **旧API停用**：PatentsView旧API于2025年5月1日停止使用 - 使用PatentSearch API
- **PAIR批量数据已停用**：使用PEDS代替
- **数据覆盖范围**：PatentSearch包含截至2025年6月30日的数据；PEDS从1981年至今
- **文本端点**：权利要求和描述端点处于测试阶段，正在进行回填
- **速率限制**：尊重速率限制以避免服务中断

## 资源

### API文档
- **PatentSearch API**：https://search.patentsview.org/docs/
- **USPTO开发者门户**：https://developer.uspto.gov/
- **USPTO开放数据门户**：https://data.uspto.gov/
- **API密钥注册**：https://account.uspto.gov/api-manager/

### Python库
- **uspto-opendata-python**：https://pypi.org/project/uspto-opendata-python/
- **USPTO文档**：https://docs.ip-tools.org/uspto-opendata-python/

### 参考文件
- `references/patentsearch_api.md` - 完整的PatentSearch API参考
- `references/peds_api.md` - PEDS API和库文档
- `references/trademark_api.md` - 商标API（TSDR和转让）
- `references/additional_apis.md` - 引用、审查意见、诉讼、PTAB

### 脚本
- `scripts/patent_search.py` - PatentSearch API客户端
- `scripts/peds_client.py` - PEDS审查数据客户端
- `scripts/trademark_client.py` - 商标搜索客户端