---
name: fda-database
description: 查询openFDA API获取药物、器械、不良事件、召回、监管提交（510k、PMA）、物质识别（UNII），用于FDA监管数据分析和安全研究。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# FDA 数据库访问

## 概述

通过openFDA访问全面的FDA监管数据，这是FDA为公共数据集提供开放API的倡议。使用Python和标准化接口查询有关药物、医疗器械、食品、动物/兽医产品以及物质的信息。

**核心功能：**
- 查询药物、器械、食品和兽医产品的不良事件
- 访问产品标签、批准和监管提交
- 监控召回和执法行动
- 查找国家药品代码（NDC）和物质标识符（UNII）
- 分析器械分类和批准（510k、PMA）
- 跟踪药物短缺和供应问题
- 研究化学结构和物质关系

## 何时使用此技能

此技能应在以下情况下使用：

- **药物研究：** 安全概况、不良事件、标签、批准、短缺
- **医疗器械监测：** 不良事件、召回、510(k)批准、PMA批准
- **食品安全：** 召回、过敏原追踪、不良事件、膳食补充剂
- **兽医学：** 按物种和品种的动物药物不良事件
- **化学/物质数据：** UNII查找、CAS编号映射、分子结构
- **监管分析：** 批准途径、执法行动、合规性追踪
- **药物警戒：** 上市后监测、安全信号检测
- **科学研究：** 药物相互作用、比较安全性、流行病学研究

## 快速开始

### 1. 基本设置

```python
from scripts.fda_query import FDAQuery

# 初始化（API密钥可选但推荐）
fda = FDAQuery(api_key="YOUR_API_KEY")

# 查询药物不良事件
events = fda.query_drug_events("aspirin", limit=100)

# 获取药物标签
label = fda.query_drug_label("Lipitor", brand=True)

# 搜索器械召回
recalls = fda.query("device", "enforcement",
                   search="classification:Class+I",
                   limit=50)
```

### 2. API 密钥设置

虽然API在没有密钥的情况下工作，但注册提供更高的速率限制：
- **无密钥：** 240请求/分钟，1,000/天
- **有密钥：** 240请求/分钟，120,000/天

在以下位置注册：https://open.fda.gov/apis/authentication/

设置为环境变量：
```bash
export FDA_API_KEY="your_key_here"
```

### 3. 运行示例

```bash
# 运行综合示例
python scripts/fda_examples.py

# 这演示了：
# - 药物安全概况
# - 器械监测
# - 食品召回监测
# - 物质查找
# - 比较药物分析
# - 兽医药物分析
```

## FDA 数据库类别

### 药物

访问6个药物相关端点，涵盖从批准到上市后监测的完整药物生命周期。

**端点：**
1. **不良事件** - 副作用、错误和治疗失败的报告
2. **产品标签** - 处方信息、警告、适应症
3. **NDC目录** - 国家药品代码产品信息
4. **执法报告** - 药物召回和安全行动
5. **Drugs@FDA** - 自1939年以来的历史批准数据
6. **药物短缺** - 当前和已解决的供应问题

**常见用例：**
```python
# 安全信号检测
fda.count_by_field("drug", "event",
                  search="patient.drug.medicinalproduct:metformin",
                  field="patient.reaction.reactionmeddrapt")

# 获取处方信息
label = fda.query_drug_label("Keytruda", brand=True)

# 检查召回
recalls = fda.query_drug_recalls(drug_name="metformin")

# 监控短缺
shortages = fda.query("drug", "drugshortages",
                     search="status:Currently+in+Shortage")
```

**参考：** 参见 `references/drugs.md` 获取详细文档

### 器械

访问9个器械相关端点，涵盖医疗器械安全、批准和注册。

**端点：**
1. **不良事件** - 器械故障、伤害、死亡
2. **510(k)批准** - 上市前通知
3. **分类** - 器械类别和风险类别
4. **执法报告** - 器械召回
5. **召回** - 详细召回信息
6. **PMA** - III类器械的上市前批准数据
7. **注册和上市** - 制造设施数据
8. **UDI** - 唯一器械识别数据库
9. **COVID-19血清学** - 抗体检测性能数据

**常见用例：**
```python
# 监测器械安全
events = fda.query_device_events("pacemaker", limit=100)

# 查找器械分类
classification = fda.query_device_classification("DQY")

# 查找510(k)批准
clearances = fda.query_device_510k(applicant="Medtronic")

# 按UDI搜索
device_info = fda.query("device", "udi",
                       search="identifiers.id:00884838003019")
```

**参考：** 参见 `references/devices.md` 获取详细文档

### 食品

访问2个食品相关端点，用于安全监测和召回。

**端点：**
1. **不良事件** - 食品、膳食补充剂和化妆品事件
2. **执法报告** - 食品产品召回

**常见用例：**
```python
# 监控过敏原召回
recalls = fda.query_food_recalls(reason="undeclared peanut")

# 追踪膳食补充剂事件
events = fda.query_food_events(
    industry="Dietary Supplements")

# 查找污染召回
listeria = fda.query_food_recalls(
    reason="listeria",
    classification="I")
```

**参考：** 参见 `references/foods.md` 获取详细文档

### 动物和兽医

访问具有物种特定信息的兽医药物不良事件数据。

**端点：**
1. **不良事件** - 按物种、品种和产品的动物药物副作用

**常见用例：**
```python
# 物种特定事件
dog_events = fda.query_animal_events(
    species="Dog",
    drug_name="flea collar")

# 品种易感性分析
breed_query = fda.query("animalandveterinary", "event",
    search="reaction.veddra_term_name:*seizure*+AND+"
           "animal.breed.breed_component:*Labrador*")
```

**参考：** 参见 `references/animal_veterinary.md` 获取详细文档

### 物质和其他

访问分子级物质数据，包括UNII代码、化学结构和关系。

**端点：**
1. **物质数据** - UNII、CAS、化学结构、关系
2. **NSDE** - 历史物质数据（遗留）

**常见用例：**
```python
# UNII到CAS映射
substance = fda.query_substance_by_unii("R16CO5Y76E")

# 按名称搜索
results = fda.query_substance_by_name("acetaminophen")

# 获取化学结构
structure = fda.query("other", "substance",
    search="names.name:ibuprofen+AND+substanceClass:chemical")
```

**参考：** 参见 `references/other.md` 获取详细文档

## 常见查询模式

### 模式1：安全概况分析

创建结合多个数据源的综合安全概况：

```python
def drug_safety_profile(fda, drug_name):
    """生成完整的安全概况。"""

    # 1. 不良事件总数
    events = fda.query_drug_events(drug_name, limit=1)
    total = events["meta"]["results"]["total"]

    # 2. 最常见反应
    reactions = fda.count_by_field(
        "drug", "event",
        search=f"patient.drug.medicinalproduct:*{drug_name}*",
        field="patient.reaction.reactionmeddrapt",
        exact=True
    )

    # 3. 严重事件
    serious = fda.query("drug", "event",
        search=f"patient.drug.medicinalproduct:*{drug_name}*+AND+serious:1",
        limit=1)

    # 4. 最近召回
    recalls = fda.query_drug_recalls(drug_name=drug_name)

    return {
        "total_events": total,
        "top_reactions": reactions["results"][:10],
        "serious_events": serious["meta"]["results"]["total"],
        "recalls": recalls["results"]
    }
```

### 模式2：时间趋势分析

使用日期范围分析趋势：

```python
from datetime import datetime, timedelta

def get_monthly_trends(fda, drug_name, months=12):
    """获取月度不良事件趋势。"""
    trends = []

    for i in range(months):
        end = datetime.now() - timedelta(days=30*i)
        start = end - timedelta(days=30)

        date_range = f"[{start.strftime('%Y%m%d')}+TO+{end.strftime('%Y%m%d')}]"
        search = f"patient.drug.medicinalproduct:*{drug_name}*+AND+receivedate:{date_range}"

        result = fda.query("drug", "event", search=search, limit=1)
        count = result["meta"]["results"]["total"] if "meta" in result else 0

        trends.append({
            "month": start.strftime("%Y-%m"),
            "events": count
        })

    return trends
```

### 模式3：比较分析

并排比较多个产品：

```python
def compare_drugs(fda, drug_list):
    """比较多个药物的安全概况。"""
    comparison = {}

    for drug in drug_list:
        # 总事件数
        events = fda.query_drug_events(drug, limit=1)
        total = events["meta"]["results"]["total"] if "meta" in events else 0

        # 严重事件
        serious = fda.query("drug", "event",
            search=f"patient.drug.medicinalproduct:*{drug}*+AND+serious:1",
            limit=1)
        serious_count = serious["meta"]["results"]["total"] if "meta" in serious else 0

        comparison[drug] = {
            "total_events": total,
            "serious_events": serious_count,
            "serious_rate": (serious_count/total*100) if total > 0 else 0
        }

    return comparison
```

### 模式4：跨数据库查找

链接多个端点的数据：

```python
def comprehensive_device_lookup(fda, device_name):
    """跨所有相关数据库查找器械。"""

    return {
        "adverse_events": fda.query_device_events(device_name, limit=10),
        "510k_clearances": fda.query_device_510k(device_name=device_name),
        "recalls": fda.query("device", "enforcement",
                           search=f"product_description:*{device_name}*"),
        "udi_info": fda.query("device", "udi",
                            search=f"brand_name:*{device_name}*")
    }
```

## 处理结果

### 响应结构

所有API响应遵循此结构：

```python
{
    "meta": {
        "disclaimer": "...",
        "results": {
            "skip": 0,
            "limit": 100,
            "total": 15234
        }
    },
    "results": [
        # 结果对象数组
    ]
}
```

### 错误处理

始终处理潜在错误：

```python
result = fda.query_drug_events("aspirin", limit=10)

if "error" in result:
    print(f"错误: {result['error']}")
elif "results" not in result or len(result["results"]) == 0:
    print("未找到结果")
else:
    # 处理结果
    for event in result["results"]:
        # 处理事件数据
        pass
```

### 分页

对于大型结果集，使用分页：

```python
# 自动分页
all_results = fda.query_all(
    "drug", "event",
    search="patient.drug.medicinalproduct:aspirin",
    max_results=5000
)

# 手动分页
for skip in range(0, 1000, 100):
    batch = fda.query("drug", "event",
                     search="...",
                     limit=100,
                     skip=skip)
    # 处理批次
```

## 最佳实践

### 1. 使用特定搜索

**做：**
```python
# 特定字段搜索
search="patient.drug.medicinalproduct:aspirin"
```

**不做：**
```python
# 过于宽泛的通配符
search="*aspirin*"
```

### 2. 实施速率限制

`FDAQuery`类自动处理速率限制，但请注意限制：
- 每分钟240个请求
- 每天120,000个请求（带API密钥）

### 3. 缓存频繁访问的数据

`FDAQuery`类包含内置缓存（默认启用）：

```python
# 缓存是自动的
fda = FDAQuery(api_key=api_key, use_cache=True, cache_ttl=3600)
```

### 4. 使用精确匹配进行计数

计数/聚合时，使用`.exact`后缀：

```python
# 计数精确短语
fda.count_by_field("drug", "event",
                  search="...",
                  field="patient.reaction.reactionmeddrapt",
                  exact=True)  # 自动添加.exact
```

### 5. 验证输入数据

清理和验证搜索词：

```python
def clean_drug_name(name):
    """清理药物名称以进行查询。"""
    return name.strip().replace('"', '\\"')

drug_name = clean_drug_name(user_input)
```

## API 参考

有关详细信息，请参阅：
- **身份验证和速率限制** → 参见 `references/api_basics.md`
- **药物数据库** → 参见 `references/drugs.md`
- **器械数据库** → 参见 `references/devices.md`
- **食品数据库** → 参见 `references/foods.md`
- **动物/兽医数据库** → 参见 `references/animal_veterinary.md`
- **物质数据库** → 参见 `references/other.md`

## 脚本

### `scripts/fda_query.py`

主要查询模块，提供`FDAQuery`类：
- 统一接口访问所有FDA端点
- 自动速率限制和缓存
- 错误处理和重试逻辑
- 常见查询模式

### `scripts/fda_examples.py`

综合示例演示：
- 药物安全概况分析
- 器械监测
- 食品召回追踪
- 物质查找
- 比较药物分析
- 兽医药物分析

运行示例：
```bash
python scripts/fda_examples.py
```

## 其他资源

- **openFDA主页**: https://open.fda.gov/
- **API文档**: https://open.fda.gov/apis/
- **交互式API资源管理器**: https://open.fda.gov/apis/try-the-api/
- **GitHub仓库**: https://github.com/FDA/openfda
- **服务条款**: https://open.fda.gov/terms/

## 支持和故障排除

### 常见问题

**问题**: 超过速率限制
- **解决方案**: 使用API密钥，实施延迟或减少请求频率

**问题**: 未找到结果
- **解决方案**: 尝试更宽泛的搜索词，检查拼写，使用通配符

**问题**: 无效的查询语法
- **解决方案**: 查阅`references/api_basics.md`中的查询语法

**问题**: 结果中缺少字段
- **解决方案**: 并非所有记录都包含所有字段；始终检查字段是否存在

### 获取帮助

- **GitHub问题**: https://github.com/FDA/openfda/issues
- **电子邮件**: open-fda@fda.hhs.gov
