---
name: azure-monitor-ingestion-py
description: Azure Monitor Ingestion SDK for Python。用于通过Logs Ingestion API向Log Analytics工作区发送自定义日志。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Monitor Ingestion SDK for Python

使用Logs Ingestion API向Azure Monitor Log Analytics工作区发送自定义日志。

## 安装

```bash
pip install azure-monitor-ingestion
pip install azure-identity
```

## 环境变量

```bash
# Data Collection Endpoint (DCE)
AZURE_DCE_ENDPOINT=https://<dce-name>.<region>.ingest.monitor.azure.com

# Data Collection Rule (DCR) 不可变ID
AZURE_DCR_RULE_ID=dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# DCR中的流名称
AZURE_DCR_STREAM_NAME=Custom-MyTable_CL
```

## 先决条件

在使用此SDK之前，您需要：

1. **Log Analytics工作区** — 日志的目标
2. **Data Collection Endpoint (DCE)** — 摄取端点
3. **Data Collection Rule (DCR)** — 定义架构和目标
4. **自定义表** — 在Log Analytics中（通过DCR创建或手动创建）

## 身份验证

```python
from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential
import os

client = LogsIngestionClient(
    endpoint=os.environ["AZURE_DCE_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 上载自定义日志

```python
from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential
import os

client = LogsIngestionClient(
    endpoint=os.environ["AZURE_DCE_ENDPOINT"],
    credential=DefaultAzureCredential()
)

rule_id = os.environ["AZURE_DCR_RULE_ID"]
stream_name = os.environ["AZURE_DCR_STREAM_NAME"]

logs = [
    {"TimeGenerated": "2024-01-15T10:00:00Z", "Computer": "server1", "Message": "Application started"},
    {"TimeGenerated": "2024-01-15T10:01:00Z", "Computer": "server1", "Message": "Processing request"},
    {"TimeGenerated": "2024-01-15T10:02:00Z", "Computer": "server2", "Message": "Connection established"}
]

client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs)
```

## 从JSON文件上载

```python
import json

with open("logs.json", "r") as f:
    logs = json.load(f)

client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs)
```

## 自定义错误处理

使用回调处理部分失败：

```python
failed_logs = []

def on_error(error):
    print(f"Upload failed: {error.error}")
    failed_logs.extend(error.failed_logs)

client.upload(
    rule_id=rule_id,
    stream_name=stream_name,
    logs=logs,
    on_error=on_error
)

# 重试失败的日志
if failed_logs:
    print(f"Retrying {len(failed_logs)} failed logs...")
    client.upload(rule_id=rule_id, stream_name=stream_name, logs=failed_logs)
```

## 忽略错误

```python
def ignore_errors(error):
    pass  # 静默忽略上载失败

client.upload(
    rule_id=rule_id,
    stream_name=stream_name,
    logs=logs,
    on_error=ignore_errors
)
```

## 异步客户端

```python
import asyncio
from azure.monitor.ingestion.aio import LogsIngestionClient
from azure.identity.aio import DefaultAzureCredential

async def upload_logs():
    async with LogsIngestionClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    ) as client:
        await client.upload(
            rule_id=rule_id,
            stream_name=stream_name,
            logs=logs
        )

asyncio.run(upload_logs())
```

## 主权云

```python
from azure.identity import AzureAuthorityHosts, DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

# Azure Government
credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
client = LogsIngestionClient(
    endpoint="https://example.ingest.monitor.azure.us",
    credential=credential,
    credential_scopes=["https://monitor.azure.us/.default"]
)
```

## 批处理行为

SDK自动进行：
- 将日志分成1MB或更小的块
- 使用gzip压缩每个块
- 并行上载块

大日志集不需要手动批处理。

## 客户端类型

| 客户端 | 用途 |
|--------|---------|
| `LogsIngestionClient` | 用于上载日志的同步客户端 |
| `LogsIngestionClient` (aio) | 用于上载日志的异步客户端 |

## 关键概念

| 概念 | 描述 |
|---------|-------------|
| **DCE** | Data Collection Endpoint — 摄取URL |
| **DCR** | Data Collection Rule — 定义架构、转换、目标 |
| **流** | DCR中的命名数据流 |
| **自定义表** | Log Analytics中的目标表（以`_CL`结尾） |

## DCR流名称格式

流名称遵循以下模式：
- `Custom-<TableName>_CL` — 对于自定义表
- `Microsoft-<TableName>` — 对于内置表

## 最佳实践

1. **使用DefaultAzureCredential** 进行身份验证
2. **优雅地处理错误** — 使用`on_error`回调处理部分失败
3. **包括TimeGenerated** — 所有日志的必需字段
4. **匹配DCR架构** — 日志字段必须与DCR列定义匹配
5. **使用异步客户端** 用于高吞吐量场景
6. **批量上载** — SDK处理批处理，但要发送合理的块
7. **监控摄取** — 在Log Analytics中检查摄取状态
8. **使用上下文管理器** — 确保正确的客户端清理

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述描述的范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
