---
name: modal
description: 用于部署Python函数和应用程序的云平台。使用装饰器将函数部署为无服务器端点、容器化应用、定时任务、Web服务、机器学习模型等。支持GPU、自定义Docker镜像、持久化存储、队列、定时器和Webhooks。适用于数据管道、机器学习推理、批处理作业、API端点和后台任务。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Modal

## 概述

Modal是一个用于部署Python函数和应用程序的云平台。它使用装饰器将函数部署为无服务器端点、容器化应用、定时任务、Web服务、机器学习模型等。Modal支持GPU、自定义Docker镜像、持久化存储、队列、定时器和Webhooks，适用于数据管道、机器学习推理、批处理作业、API端点和后台任务。

## 核心能力

### 1. 函数部署

使用装饰器将Python函数部署为无服务器函数：

- **@app.function**：基本函数部署
- **@app.method**：方法部署
- **@app.web_endpoint**：Web端点部署
- **@app.scheduled**：定时任务部署
- **@app.batch**：批处理作业部署

### 2. 容器化

- **自定义Docker镜像**：使用自定义Docker镜像
- **Python环境**：指定Python版本和依赖项
- **GPU支持**：自动分配GPU资源
- **持久化卷**：挂载持久化存储

### 3. 存储

- **网络挂载**：挂载网络文件系统
- **持久化卷**：创建持久化卷
- **对象存储**：集成S3兼容的对象存储
- **临时存储**：使用临时存储

### 4. 队列和任务

- **任务队列**：创建任务队列
- **批处理**：批量处理任务
- **并行执行**：并行执行任务
- **任务监控**：监控任务执行

### 5. 定时器和Webhooks

- **定时任务**：使用cron表达式定时执行任务
- **Webhooks**：创建Webhook端点
- **事件触发**：响应事件触发任务

### 6. Web服务

- **API端点**：创建REST API端点
- **WebSocket**：支持WebSocket连接
- **静态文件**：提供静态文件服务
- **反向代理**：配置反向代理

## 何时使用此技能

在以下情况下使用此技能：
- 部署Python函数到云端
- 创建无服务器API端点
- 部署机器学习模型
- 运行批处理作业
- 创建定时任务
- 构建数据管道
- 部署Web服务
- 运行GPU加速任务

## 安装和设置

```bash
# 安装Modal客户端
pip install modal

# 登录Modal
modal token new
```

## 使用示例

### 基本函数部署

```python
import modal

app = modal.App("example-app")

@app.function()
def hello(name: str) -> str:
    return f"Hello, {name}!"

# 远程调用
with modal.run():
    print(hello.remote("World"))
```

### Web端点

```python
@app.web_endpoint(method="GET")
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### 定时任务

```python
@app.scheduled(cron="0 9 * * *")  # 每天上午9点运行
def daily_report():
    print("Running daily report...")
```

### GPU加速

```python
@app.function(gpu="A100")
def gpu_task():
    import torch
    print(f"GPU available: {torch.cuda.is_available()}")
```

### 批处理

```python
@app.batch()
def process_batch(items: list[str]) -> list[str]:
    return [item.upper() for item in items]

with modal.run():
    results = process_batch.map(["a", "b", "c"])
```

### 持久化存储

```python
@app.function(volumes={"/data": modal.Volume.from_name("my-volume")})
def save_data(data: str):
    with open("/data/output.txt", "w") as f:
        f.write(data)
```

### Web服务

```python
@app.web_endpoint(method="POST")
def predict(image: bytes) -> dict:
    import torch
    from PIL import Image
    import io

    # 加载图像
    img = Image.open(io.BytesIO(image))

    # 预处理和推理
    # ...

    return {"prediction": "cat"}
```

## 高级功能

### 自定义Docker镜像

```python
image = modal.Image.debian_slim().pip_install(
    "torch",
    "transformers",
    "pillow"
)

@app.function(image=image)
def ml_task():
    import torch
    print(f"PyTorch version: {torch.__version__}")
```

### 任务队列

```python
@app.function()
def process_item(item: str) -> str:
    return item.upper()

# 创建队列
queue = process_item.starmap([("a",), ("b",), ("c",)])

# 等待结果
results = list(queue)
```

### Webhooks

```python
@app.web_endpoint(method="POST")
def webhook_handler(data: dict) -> dict:
    print(f"Received webhook: {data}")
    return {"status": "success"}
```

### 并行执行

```python
@app.function()
def parallel_task(x: int) -> int:
    return x * 2

with modal.run():
    results = parallel_task.map([1, 2, 3, 4, 5])
    print(results)
```

## 最佳实践

1. **函数设计**：保持函数简单和独立
2. **错误处理**：实现适当的错误处理
3. **资源管理**：合理配置CPU、内存和GPU
4. **日志记录**：添加详细的日志记录
5. **测试**：在本地测试函数后再部署
6. **监控**：监控函数执行和性能
7. **成本优化**：优化资源使用以降低成本

## 常见问题

**Q: Modal支持哪些GPU？**
A: Modal支持A100、V100、T4等多种GPU。

**Q: 如何持久化数据？**
A: 使用持久化卷或对象存储。

**Q: 如何调试函数？**
A: 使用日志记录和Modal的调试工具。

**Q: Modal的定价如何？**
A: Modal按使用量计费，详见定价页面。

## 资源

- **Modal文档**：https://modal.com/docs
- **Modal GitHub**：https://github.com/modal-labs/modal
- **Modal定价**：https://modal.com/pricing
