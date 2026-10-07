---
name: azure-data-tables-py
description: Azure 表 SDK for Python（存储和 Cosmos DB）。用于 NoSQL 键值存储、实体 CRUD 和批量操作。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Tables SDK for Python

用于结构化数据的 NoSQL 键值存储（Azure 存储表或 Cosmos DB 表 API）。

## 安装

```bash
pip install azure-data-tables azure-identity
```

## 环境变量

```bash
# Azure 存储表
AZURE_STORAGE_ACCOUNT_URL=https://<account>.table.core.windows.net

# Cosmos DB 表 API
COSMOS_TABLE_ENDPOINT=https://<account>.table.cosmos.azure.com
```

## 认证

```python
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient, TableClient

credential = DefaultAzureCredential()
endpoint = "https://<account>.table.core.windows.net"

# 服务客户端（管理表）
service_client = TableServiceClient(endpoint=endpoint, credential=credential)

# 表客户端（处理实体）
table_client = TableClient(endpoint=endpoint, table_name="mytable", credential=credential)
```

## 客户端类型

| 客户端 | 目的 |
|--------|---------|
| `TableServiceClient` | 创建/删除表、列出表 |
| `TableClient` | 实体 CRUD、查询 |

## 表操作

```python
# 创建表
service_client.create_table("mytable")

# 创建（如果不存在）
service_client.create_table_if_not_exists("mytable")

# 删除表
service_client.delete_table("mytable")

# 列出表
for table in service_client.list_tables():
    print(table.name)

# 获取表客户端
table_client = service_client.get_table_client("mytable")
```

## 实体操作

**重要**：每个实体都需要 `PartitionKey` 和 `RowKey`（共同形成唯一 ID）。

### 创建实体

```python
entity = {
    "PartitionKey": "sales",
    "RowKey": "order-001",
    "product": "Widget",
    "quantity": 5,
    "price": 9.99,
    "shipped": False
}

# 创建（如果存在则失败）
table_client.create_entity(entity=entity)

# 更新插入（创建或替换）
table_client.upsert_entity(entity=entity)
```

### 获取实体

```python
# 按键获取（最快）
entity = table_client.get_entity(
    partition_key="sales",
    row_key="order-001"
)
print(f"Product: {entity['product']}")
```

### 更新实体

```python
# 替换整个实体
entity["quantity"] = 10
table_client.update_entity(entity=entity, mode="replace")

# 合并（仅更新特定字段）
update = {
    "PartitionKey": "sales",
    "RowKey": "order-001",
    "shipped": True
}
table_client.update_entity(entity=update, mode="merge")
```

### 删除实体

```python
table_client.delete_entity(
    partition_key="sales",
    row_key="order-001"
)
```

## 查询实体

### 在分区内查询

```python
# 按分区查询（高效）
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales'"
)
for entity in entities:
    print(entity)
```

### 带筛选器的查询

```python
# 按属性筛选
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales' and quantity gt 3"
)

# 使用参数（更安全）
entities = table_client.query_entities(
    query_filter="PartitionKey eq @pk and price lt @max_price",
    parameters={"pk": "sales", "max_price": 50.0}
)
```

### 选择特定属性

```python
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales'",
    select=["RowKey", "product", "price"]
)
```

### 列出所有实体

```python
# 列出所有（跨分区 - 谨慎使用）
for entity in table_client.list_entities():
    print(entity)
```

## 批量操作

```python
from azure.data.tables import TableTransactionError

# 批量操作（仅限同一分区！）
operations = [
    ("create", {"PartitionKey": "batch", "RowKey": "1", "data": "first"}),
    ("create", {"PartitionKey": "batch", "RowKey": "2", "data": "second"}),
    ("upsert", {"PartitionKey": "batch", "RowKey": "3", "data": "third"}),
]

try:
    table_client.submit_transaction(operations)
except TableTransactionError as e:
    print(f"Transaction failed: {e}")
```

## 异步客户端

```python
from azure.data.tables.aio import TableServiceClient, TableClient
from azure.identity.aio import DefaultAzureCredential

async def table_operations():
    credential = DefaultAzureCredential()
    
    async with TableClient(
        endpoint="https://<account>.table.core.windows.net",
        table_name="mytable",
        credential=credential
    ) as client:
        # 创建
        await client.create_entity(entity={
            "PartitionKey": "async",
            "RowKey": "1",
            "data": "test"
        })
        
        # 查询
        async for entity in client.query_entities("PartitionKey eq 'async'"):
            print(entity)

import asyncio
asyncio.run(table_operations())
```

## 数据类型

| Python 类型 | 表存储类型 |
|-------------|-------------------|
| `str` | String |
| `int` | Int64 |
| `float` | Double |
| `bool` | Boolean |
| `datetime` | DateTime |
| `bytes` | Binary |
| `UUID` | Guid |

## 最佳实践

1. **设计分区键**以适应查询模式和均匀分布
2. **尽可能在分区内查询**（跨分区成本很高）
3. **对同一分区中的多个实体使用批量操作**
4. **对幂等写入使用 `upsert_entity`**
5. **使用参数化查询**以防止注入
6. **保持实体小型** — 每个实体最多 1MB
7. **对高吞吐量场景使用异步客户端**

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
