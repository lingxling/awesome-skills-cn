---
name: adaptyv
description: 云实验室平台，用于自动化蛋白质测试和验证。在设计蛋白质并需要实验验证时使用，包括结合测定、表达测试、热稳定性测量、酶活性测定或蛋白质序列优化。也可用于通过 API 提交实验、跟踪实验状态、下载结果、使用计算工具（NetSolP、SoluProt、SolubleMPNN、ESM）优化蛋白质序列以获得更好的表达，或管理具有湿实验验证的蛋白质设计工作流程。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Adaptyv

Adaptyv 是一个云实验室平台，提供自动化蛋白质测试和验证服务。通过 API 或 Web 界面提交蛋白质序列，在大约 21 天内接收实验结果。

## 快速开始

### 认证设置

Adaptyv 需要 API 认证。设置您的凭据：

1. 联系 support@adaptyvbio.com 请求 API 访问权限（平台处于 alpha/beta 阶段）
2. 接收您的 API 访问令牌
3. 设置环境变量：

```bash
export ADAPTYV_API_KEY="your_api_key_here"
```

或创建 `.env` 文件：

```
ADAPTYV_API_KEY=your_api_key_here
```

### 安装

使用 uv 安装所需的包：

```bash
uv pip install requests python-dotenv
```

### 基本用法

提交蛋白质序列进行测试：

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ADAPTYV_API_KEY")
base_url = "https://kq5jp7qj7wdqklhsxmovkzn4l40obksv.lambda-url.eu-central-1.on.aws"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 提交实验
response = requests.post(
    f"{base_url}/experiments",
    headers=headers,
    json={
        "sequences": ">protein1\nMKVLWALLGLLGAA...",
        "experiment_type": "binding",
        "webhook_url": "https://your-webhook.com/callback"
    }
)

experiment_id = response.json()["experiment_id"]
```

## 可用的实验类型

Adaptyv 支持多种测定类型：
- **结合测定** - 使用生物层干涉技术测试蛋白质-靶标相互作用
- **表达测试** - 测量蛋白质表达水平
- **热稳定性** - 表征蛋白质热稳定性
- **酶活性** - 评估酶功能

有关每种实验类型和工作流程的详细信息，请参阅 `reference/experiments.md`。

## 蛋白质序列优化

在提交序列之前，优化它们以获得更好的表达和稳定性：

**需要解决的常见问题：**
- 形成不需要的二硫键的未配对半胱氨酸
- 导致聚集的过度疏水区域
- 溶解度预测不佳

**推荐工具：**
- NetSolP / SoluProt - 初始溶解度筛选
- SolubleMPNN - 改善溶解度的序列重新设计
- ESM - 序列可能性评分
- ipTM - 界面稳定性评估
- pSAE - 疏水性暴露量化

有关详细的优化工作流程和工具使用，请参阅 `reference/protein_optimization.md`。

## API 参考

有关完整的 API 文档，包括所有端点、请求/响应格式和身份验证详细信息，请参阅 `reference/api_reference.md`。

## 示例

有关涵盖常见用例（实验提交、状态跟踪、结果检索、批处理）的具体代码示例，请参阅 `reference/examples.md`。

## 重要说明
- 平台目前处于 alpha/beta 阶段，功能可能会发生变化
- 并非所有平台功能都可通过 API 使用
- 结果通常在约 21 天内交付
- 如需访问请求或问题，请联系 support@adaptyvbio.com
- 适用于高通量 AI 驱动的蛋白质设计工作流程
