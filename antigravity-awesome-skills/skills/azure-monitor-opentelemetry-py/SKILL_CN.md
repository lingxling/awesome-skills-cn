---
name: azure-monitor-opentelemetry-py
description: 用于 Python 的 Azure Monitor OpenTelemetry Distro。用于一行式 Application Insights 设置和自动检测。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Monitor OpenTelemetry Distro（Python）

使用 OpenTelemetry 自动检测进行单行 Application Insights 设置。

## 安装

```bash
pip install azure-monitor-opentelemetry
```

## 环境变量

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## 快速开始

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# One-line setup - reads connection string from environment
configure_azure_monitor()

# Your application code...
```

## 显式配置

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string="InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/"
)
```

## 使用 Flask

```python
from flask import Flask
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
```

## 使用 Django

```python
# settings.py
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

# Django settings...
```

## 使用 FastAPI

```python
from fastapi import FastAPI
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## 自定义跟踪

```python
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Do work...
```

## 自定义指标

```python
from opentelemetry import metrics
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

meter = metrics.get_meter(__name__)
counter = meter.create_counter("my_counter")

counter.add(1, {"dimension": "value"})
```

## 自定义日志

```python
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("This will appear in Application Insights")
logger.error("Errors are captured too", exc_info=True)
```

## 采样

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# Sample 10% of requests
configure_azure_monitor(
    sampling_ratio=0.1
)
```

## 云角色名称

为应用程序映射设置云角色名称：

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

configure_azure_monitor(
    resource=Resource.create({SERVICE_NAME: "my-service-name"})
)
```

## 禁用特定的检测

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    instrumentations=["flask", "requests"]  # Only enable these
)
```

## 启用实时指标

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    enable_live_metrics=True
)
```

## Azure AD 身份验证

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.identity import DefaultAzureCredential

configure_azure_monitor(
    credential=DefaultAzureCredential()
)
```

## 包含的自动检测

| 库 | 遥测类型 |
|---------|---------------|
| Flask | 跟踪 |
| Django | 跟踪 |
| FastAPI | 跟踪 |
| Requests | 跟踪 |
| urllib3 | 跟踪 |
| httpx | 跟踪 |
| aiohttp | 跟踪 |
| psycopg2 | 跟踪 |
| pymysql | 跟踪 |
| pymongo | 跟踪 |
| redis | 跟踪 |

## 配置选项

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `connection_string` | Application Insights 连接字符串 | 来自环境变量 |
| `credential` | 用于 AAD 身份验证的 Azure 凭据 | None |
| `sampling_ratio` | 采样率（0.0 到 1.0） | 1.0 |
| `resource` | OpenTelemetry 资源 | 自动检测 |
| `instrumentations` | 要启用的检测列表 | 全部 |
| `enable_live_metrics` | 启用实时指标流 | False |

## 最佳实践

1. **尽早调用 configure_azure_monitor()** — 在导入检测库之前
2. **在生产中使用环境变量**作为连接字符串
3. **为多服务应用程序设置云角色名称**
4. **在高流量应用中启用采样**
5. **使用结构化日志**以获得更好的日志分析查询
6. **向跨度添加自定义属性**以便更好地进行调试
7. **为生产工作负载使用 AAD 身份验证**

## 使用场景

本技能适用于执行上述概述中描述的工作流或操作。

## 限制条件

- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
