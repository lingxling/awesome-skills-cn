---
name: azure-monitor-opentelemetry-exporter-py
description: 用于 Python 的 Azure Monitor OpenTelemetry 导出器。用于低级别 OpenTelemetry 导出到 Application Insights。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Monitor OpenTelemetry 导出器（Python）

用于向 Application Insights 发送 OpenTelemetry 跟踪、指标和日志的低级别导出器。

## 安装

```bash
pip install azure-monitor-opentelemetry-exporter
```

## 环境变量

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## 使用时机

| 场景 | 使用 |
|----------|-----|
| 快速设置、自动检测 | `azure-monitor-opentelemetry` (distro) |
| 自定义 OpenTelemetry 管道 | `azure-monitor-opentelemetry-exporter` (此包) |
| 对遥测进行细粒度控制 | `azure-monitor-opentelemetry-exporter` (此包) |

## 跟踪导出器

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Create exporter
exporter = AzureMonitorTraceExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure tracer provider
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(exporter)
)

# Use tracer
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-span"):
    print("Hello, World!")
```

## 指标导出器

```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

# Create exporter
exporter = AzureMonitorMetricExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure meter provider
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))

# Use meter
meter = metrics.get_meter(__name__)
counter = meter.create_counter("requests_total")
counter.add(1, {"route": "/api/users"})
```

## 日志导出器

```python
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

# Create exporter
exporter = AzureMonitorLogExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure logger provider
logger_provider = LoggerProvider()
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
set_logger_provider(logger_provider)

# Add handler to Python logging
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

# Use logging
logger = logging.getLogger(__name__)
logger.info("This will be sent to Application Insights")
```

## 从环境变量读取

导出器会自动读取 `APPLICATIONINSIGHTS_CONNECTION_STRING`：

```python
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Connection string from environment
exporter = AzureMonitorTraceExporter()
```

## Azure AD 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter(
    credential=DefaultAzureCredential()
)
```

## 采样

使用 `ApplicationInsightsSampler` 实现一致的采样：

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
from azure.monitor.opentelemetry.exporter import ApplicationInsightsSampler

# Sample 10% of traces
sampler = ApplicationInsightsSampler(sampling_ratio=0.1)

trace.set_tracer_provider(TracerProvider(sampler=sampler))
```

## 离线存储

配置离线存储以进行重试：

```python
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter(
    connection_string="...",
    storage_directory="/path/to/storage",  # Custom storage path
    disable_offline_storage=False  # Enable retry (default)
)
```

## 禁用离线存储

```python
exporter = AzureMonitorTraceExporter(
    connection_string="...",
    disable_offline_storage=True  # No retry on failure
)
```

## 主权云

```python
from azure.identity import AzureAuthorityHosts, DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Azure Government
credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
exporter = AzureMonitorTraceExporter(
    connection_string="InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.us/",
    credential=credential
)
```

## 导出器类型

| 导出器 | 遥测类型 | Application Insights 表 |
|----------|---------------|---------------------------|
| `AzureMonitorTraceExporter` | 跟踪/跨度 | requests, dependencies, exceptions |
| `AzureMonitorMetricExporter` | 指标 | customMetrics, performanceCounters |
| `AzureMonitorLogExporter` | 日志 | traces, customEvents |

## 配置选项

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `connection_string` | Application Insights 连接字符串 | 来自环境变量 |
| `credential` | 用于 AAD 身份验证的 Azure 凭据 | None |
| `disable_offline_storage` | 禁用重试存储 | False |
| `storage_directory` | 自定义存储路径 | 临时目录 |

## 最佳实践

1. **使用 BatchSpanProcessor** 用于生产环境（不是 SimpleSpanProcessor）
2. **使用 ApplicationInsightsSampler** 实现跨服务的一致采样
3. **启用离线存储**以提高生产中的可靠性
4. **使用 AAD 身份验证**而不是检测密钥
5. **设置导出间隔**适合你的工作负载
6. **使用 distro**（`azure-monitor-opentelemetry`）除非你需要自定义管道

## 限制条件

- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
