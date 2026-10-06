---
name: hf-cloud-sagemaker-production-defaults
description: '创建 SageMaker 端点（实时、可缩容到零的实时端点或异步端点），默认启用自动扩缩、CloudWatch 告警和标签。每当即将创建 SageMaker 端点、编写调用 `create_endpoint` 的部署代码，或在镜像 URI 和 IAM 角色已确定后完成部署时，都应使用此技能。提供 deploy.py 用于实时端点，deploy_ic.py 用于通过推理组件（inference components）缩容到零实例的实时端点，deploy_async.py 用于异步端点（同样可缩容到零）。这是 SageMaker 部署工作流的最后一步。切勿在没有这些默认设置的情况下生成裸 `create_endpoint` 调用——没有自动扩缩或告警的端点只是演示，而不是部署。'
---

# SageMaker 生产默认配置

演示端点与可以长期运行的端点之间的区别在于：它能随流量扩缩，出故障时会通知你，并且之后可以调试。此技能将这三点设为默认，而不是可选的附加项。

在此技能运行时，规划器已经选定了实时端点，IAM 已有可用角色，镜像选择也已解析出容器 URI 和 AMI 版本。此技能将这些转化为实际的部署。

## 会创建哪些资源

对于每个端点，此技能会作为一个整体创建以下资源：

1. **SageMaker Model** — 镜像 + 环境变量 + 执行角色 + S3 制品
2. **Endpoint config** — 实例类型、初始数量、可选的数据捕获
3. **Endpoint** — 提供推理服务的实时端点
4. **自动扩缩目标 + 策略** — 基于每实例调用次数的目标跟踪
5. **CloudWatch 告警** — 延迟、错误、平台开销

推理组件部署（`deploy_ic.py`）创建的是同一组资源，但有两处不同：endpoint config 携带执行角色和 `ManagedInstanceScaling`，而由一个**推理组件**承载模型。其自动扩缩目标是该组件，而不是变体（variant）。

数据捕获（将请求/响应记录到 S3）**默认关闭**——它对调试有用，但会产生用户未必要求的持续 S3 费用。使用 `--enable-data-capture` 启用。

所有资源都会获得一致的标签集，其中包括 `CreatedBy=agentic-deploy-skills`，便于之后清理。

默认值及其理由见 `references/deployment-template.md`。

## 运行部署

对于文本生成 LLM（vLLM），首先将固定版本的模型快照打包为 SageMaker `model.tar.gz` 制品，并上传到账户控制的 S3 存储桶。SageMaker 会将其解压到 `/opt/ml/model` 下，因此部署在运行时不会获取或执行仓库代码：

```bash
python scripts/deploy.py \
    --model-name qwen3-medical \
    --image-uri "$IMAGE_URI" \
    --inference-ami-version "$AMI" \
    --role-arn "$ROLE_ARN" \
    --model-s3-uri "s3://<your-model-bucket>/qwen3-medical/model.tar.gz" \
    --instance-type ml.g5.xlarge \
    --region "$REGION" \
    --env SM_VLLM_MODEL=/opt/ml/model \
    --env SM_VLLM_HOST=0.0.0.0 \
    --env SM_VLLM_TRUST_REMOTE_CODE=false \
    --env SM_VLLM_MAX_MODEL_LEN=4096
```

对于嵌入模型（TEI，通常运行在 CPU 上）：

```bash
python scripts/deploy.py \
    --model-name bge-large-embeddings \
    --image-uri "$IMAGE_URI" \
    --role-arn "$ROLE_ARN" \
    --instance-type ml.c6i.2xlarge \
    --region "$REGION" \
    --env HF_MODEL_ID=BAAI/bge-large-en-v1.5
```

注意：TEI 部署**不需要** `--inference-ami-version`。该标志是 vLLM 专用的。TEI 的环境变量也更简单（用 `HF_MODEL_ID` 而不是 `SM_VLLM_*`，无需配置 host 或 trust-remote-code）。

各个值的来源：

| 参数 | 来源 |
|---|---|
| `--image-uri` | `hf-cloud-serving-image-selection` — 智能体从 AWS DLC 目录页面读取 |
| `--inference-ami-version` | `hf-cloud-serving-image-selection` — 对包含 cu130+ 的 vLLM 标签是必需的 |
| `--role-arn` | `hf-cloud-sagemaker-iam-preflight`（`check_role.py`） |
| `--region` | `hf-cloud-aws-context-discovery` |
| `--instance-type` | 用户输入或规划器推荐 |
| `--env` | 因模型而异；所需的 `SM_VLLM_*` 变量见 `hf-cloud-serving-image-selection` |
| `--model-s3-uri` | 生产环境首选 — 固定版本模型制品的 S3 URI，会被解压到 `/opt/ml/model`；仅在"运行时从 Hub 加载"的例外情况下省略 |

脚本会按顺序创建资源并处理错误，等待 `InService`（最多 30 分钟），呈现失败原因，注册自动扩缩和告警，并打印包含清理命令的摘要。它会在 stdout 上输出一个 JSON 对象，包含端点/配置/模型名称，供下游脚本使用。

这些脚本随此技能一起提供。如果安装的副本缺少 `scripts/` 目录（某些运行框架在安装时只复制 SKILL.md），请从源仓库获取它们，而不是根据本说明重新实现。

**模型加载默认方式**：将固定版本的权重预先放到 S3 中并传入 `--model-s3-uri`；容器会从 `/opt/ml/model` 加载它们，在运行时不依赖 Hub。从 Hub 加载是明确的例外：预计端点启动后需要 5–15 分钟以上的下载时间，对受限（gated）模型需要提供 token，并保持 `SM_VLLM_TRUST_REMOTE_CODE=false`，除非特定架构需要经过审查的自定义代码。`deploy.py` 会等待 30 分钟。

## InService 并不等于成功——宣布成功前先做冒烟测试

`InService` 只意味着容器响应了 `/ping`。在基于 MMS 的容器（HF Inference Toolkit）中，即使 Python worker 处于崩溃循环，Java 前端仍会响应 ping——端点可能处于 InService 却什么都不提供。始终执行两项检查：

1. **一次真实调用。**
   - 实时：使用 `invoke_endpoint.py`（见下文）发送最小负载；要求返回 HTTP 200 且响应体合理。
   - 异步：向 S3 上传一个输入，调用 `invoke-endpoint-async`，在几分钟内轮询输出 URI（参见"调用异步端点"）。出现结果对象 = 成功；在失败 URI 中出现对象，或什么都没出现 = 已损坏。
2. **扫描端点日志中的 worker 崩溃标记** — 即使冒烟请求只是超时，也能捕获崩溃循环的情况：

   ```bash
   aws logs filter-log-events \
       --log-group-name /aws/sagemaker/Endpoints/<endpoint-name> \
       --filter-pattern '?"Worker died" ?"Load model failed" ?"ImportError"' \
       --region <region> --max-items 5
   ```

   推理组件部署则将日志写入 `/aws/sagemaker/InferenceComponents/<component-name>`。`deploy_ic.py` 在等待期间会自动扫描该日志组。

**诊断调用被拒绝时的通用规则**：当工作流用于诊断的只读调用被拒绝时（受限角色没有 `logs:FilterLogEvents`、`servicequotas:ListServiceQuotas` 等权限），用一行说明这一点，然后继续执行可以正常工作的检查。切勿因为仅用于诊断的权限而阻塞部署，也切勿把被拒绝的调用当作一切正常的证据。

只有在两项检查都通过后才报告部署完成。如果日志扫描命中，请呈现 CloudWatch 中的实际回溯信息——而不是 InService 状态。

## 测试实时端点

端点进入 `InService` 后，使用随附的辅助脚本进行测试。它跨平台且**对 BOM 安全**——请使用它，而不要手写负载文件并直接调用 `invoke-endpoint`：

```bash
# macOS / Linux
python3 scripts/invoke_endpoint.py \
    --endpoint-name <endpoint-name> \
    --payload '{"inputs": "Hello"}' \
    --region "$REGION"
```

```powershell
# Windows (PowerShell)
python scripts\invoke_endpoint.py `
    --endpoint-name <endpoint-name> `
    --payload-file payload.json `
    --region $REGION
```

它接受 `--payload '<json>'`（内联）或 `--payload-file <path>`，会验证 JSON，以纯 UTF-8 写入请求体，调用端点，并将响应体打印到 stdout。

### UTF-8 BOM 陷阱（Windows）

如果你在 Windows 上自己编写请求负载，**不要**使用 `Set-Content -Encoding UTF8`——根据 PowerShell 版本的不同，它会在开头添加 UTF-8 字节顺序标记（BOM）。SageMaker 的 JSON 解析器会以 400 `ModelError` 拒绝 BOM：

```
Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
```

这**不是**模型、端点健康状况或镜像的问题——只是请求体的文件编码问题。`invoke_endpoint.py` 完全避免了这个问题（它甚至会去除已带有 BOM 的 `--payload-file` 中的 BOM）。如果必须直接调用 CLI，请将请求体写为无 BOM 的 UTF-8：

```powershell
# 无 BOM 的 UTF-8 — 使用这个
[System.IO.File]::WriteAllText((Resolve-Path "payload.json"), $json, [System.Text.UTF8Encoding]::new($false))

aws sagemaker-runtime invoke-endpoint `
    --endpoint-name <endpoint-name> `
    --content-type application/json `
    --body fileb://payload.json `
    --region $REGION `
    response.json
```

**回退方案：**如果任何调用因 `Unexpected UTF-8 BOM` 失败，请将负载重写为无 BOM 的 UTF-8（或改用 `invoke_endpoint.py` 重新运行）并重试一次，然后再判定端点或模型已损坏。

### 调用生成式重排序器（vLLM）

生成式重排序器（Qwen3-Reranker 等——由 `hf-cloud-serving-image-selection` 路由到 HuggingFace vLLM DLC）是按第一个生成 token 打分的因果语言模型，而不是聊天模型。请使用**带原始 `prompt` 的 completions API**，而不是 messages/chat API：聊天模板化并不能可靠地遵循 `chat_template_kwargs`（如 `{"enable_thinking": false}`），而错误的模板会悄无声息地为每个查询–文档对返回几乎相同的分数，而不是报错。

负载格式（Qwen3-Reranker 期望的格式——替换 `{query}` / `{document}`）：

```json
{
  "prompt": "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be \"yes\" or \"no\".<|im_end|>\n<|im_start|>user\n<Instruct>: Given a web search query, retrieve relevant passages that answer the query\n<Query>: {query}\n<Document>: {document}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n",
  "max_tokens": 1,
  "temperature": 0,
  "logprobs": 20
}
```

末尾的 `<|im_start|>assistant\n<think>\n\n</think>\n\n` 后缀至关重要：它预先填充了一个空的思考块，使第一个生成的 token 就是 yes/no 判断。根据返回的 logprobs 计算分数：`P("yes") / (P("yes") + P("no"))`。用一个相关对（预期 >0.9）和一个不相关对（预期 <0.05）对端点进行合理性检查——各对之间分数几乎相同意味着提示模板有误，而不是模型损坏。

同样的规则可以推广：对于任何需要逐字节精确提示的思考模式模型，优先使用原始 completions API 而不是 chat。

### 选择镜像 URI

智能体从 AWS 的 [Deep Learning Containers 目录](https://aws.github.io/deep-learning-containers/reference/available_images/) 读取镜像 URI——选择与模型系列匹配的行（LLM 用 HuggingFace vLLM，嵌入用 TEI，等等），将 `<region>` 替换为部署区域，然后传给 `deploy.py --image-uri`。

特别是对于 vLLM 镜像（包括 `huggingface-vllm` 和 AWS `vllm` 备选），还要检查标签中的 CUDA 版本：

```bash
# 示例：目录中的 HuggingFace vLLM 0.21.0
IMAGE_URI="763104351884.dkr.ecr.eu-west-1.amazonaws.com/huggingface-vllm:0.21.0-transformers5.8.1-gpu-py312-cu130-ubuntu22.04"

# cu130 标签 → 必须传入 --inference-ami-version
python deploy.py --image-uri "$IMAGE_URI" \
    --inference-ami-version al2-ami-sagemaker-inference-gpu-3-1 \
    ...
```

对于 `cu129` 或更低版本的标签，省略 `--inference-ami-version`。完整的 vLLM AMI 查找表以及每个镜像系列的环境变量要求，请参见 `hf-cloud-serving-image-selection`。

## 实时端点缩容到零

实时端点只有在托管**推理组件**时才能缩减到零实例。`deploy.py` 注册的变体级目标无法低于一个实例。`deploy_ic.py` 则构建基于组件的形态。

当流量稀疏或按计划到达，并且客户端能容忍首个请求耗时数分钟时使用它。不要将其用于有 SLA 的交互式流量：唤醒需要数分钟，唤醒期间的每个请求都会失败。

```bash
python scripts/deploy_ic.py \
    --model-name qwen3-scale-to-zero \
    --image-uri "$IMAGE_URI" \
    --inference-ami-version "$AMI" \
    --role-arn "$ROLE_ARN" \
    --model-s3-uri "s3://<your-model-bucket>/qwen3-scale-to-zero/model.tar.gz" \
    --instance-type ml.g5.xlarge \
    --region "$REGION" \
    --env SM_VLLM_MODEL=/opt/ml/model \
    --env SM_VLLM_HOST=0.0.0.0 \
    --env SM_VLLM_TRUST_REMOTE_CODE=false \
    --env SM_VLLM_MAX_MODEL_LEN=4096
```

### 与 deploy.py 的区别

| 组成部分 | 基于模型（`deploy.py`） | 基于组件（`deploy_ic.py`） |
|---|---|---|
| 执行角色 | 在 Model 上 | 在 **endpoint config** 上（`ExecutionRoleArn`） |
| 模型引用 | `ProductionVariants[].ModelName` | `InferenceComponent.Specification.ModelName`；变体没有 `ModelName` |
| 实例下限 | `InitialInstanceCount`，最小为 1 | `ManagedInstanceScaling {Status: ENABLED, MinInstanceCount: 0}` |
| 扩缩目标 | `endpoint/<ep>/variant/AllTraffic`，`sagemaker:variant:DesiredInstanceCount` | `inference-component/<ic>`，`sagemaker:inference-component:DesiredCopyCount` |
| 扩缩指标 | `SageMakerVariantInvocationsPerInstance`（20/分钟） | `SageMakerInferenceComponentConcurrentRequestsPerCopyHighResolution`（每副本 5 个并发） |
| 从零唤醒 | 不适用 | 步进策略 + `NoCapacityInvocationFailures` 告警 |
| 调用 | 端点名称 | 端点名称**加上** `InferenceComponentName` |

`InferenceAmiVersion` 仍然属于变体，并且它可以与 `ManagedInstanceScaling` 共存（已在 `cu130` + `ml.g5.xlarge` 上验证）。

要让"缩容到零"生效需要四个组成部分，缺一不可。目标跟踪无法离开零，因为它不能除以零个副本。去掉步进策略或其告警，端点会缩容到零一次，然后再也不会响应。`deploy_ic.py` 会把这四部分全部连接好。

### 实测行为

`Qwen/Qwen3-0.6B`，从 Hub 加载，`ml.g5.xlarge`，`us-east-1`，2026 年 7 月：

| 步骤 | 时间 |
|---|---|
| 端点 `InService`（启动时为空，不加载模型） | 4 分钟 |
| 组件 `InService`（Hub 下载 + vLLM 启动 + CUDA graphs） | +6 分钟 |
| 空闲到 0 个副本 | 最后一个请求后 11 分钟 |
| 0 个副本到 0 个实例 | +12 分钟 |
| 零状态下的首个请求 → HTTP 400 `has no capacity` | 立即 |
| `NoCapacityInvocationFailures` 告警 → ALARM | +67 秒 |
| 步进策略将期望副本数和实例数提升到 1 | +1 分 42 秒 |
| HTTP 200 | **+9 分 24 秒** |

缩容无法通过此技能调整：Application Auto Scaling 会自行创建 AlarmLow，周期为 10 秒、评估周期为 90 个，因此需要 15 分钟的空闲数据点才会触发。

预先放置生产权重并传入 `--model-s3-uri`。除了避免运行时访问 Hub 之外，这还能缩短每次唤醒：模型制品在**每次**唤醒时都会重新加载，因此其获取过程位于每个空闲期之后首个请求的关键路径上。

### 确定组件规格

`ComputeResourceRequirements` 是调度预留，而不是上限。请求 1024 MB 的组件运行 vLLM 时使用数 GB 的主机内存也没有问题。

可调度池远小于实例内存。在 `ml.g5.xlarge`（16 GiB）上，调度器**接受 1024 MB，拒绝 4096 MB**。请求过多会导致立即且令人困惑的失败：

```
There is not enough hardware resources on the instances for this endpoint to
create a copy of the inference component.
```

即使端点有一个健康的实例，也会出现这条消息。应将其理解为"请求过大"，而不是"需要增加实例"。从默认的 1024 MB 开始，仅当多个组件共享一个实例时才提高它。

对于多 GPU 模型，`--accelerator-devices` 必须与 `SM_VLLM_TENSOR_PARALLEL_SIZE` 匹配。

### 调用与测试

传入组件名称，并为唤醒留出时间：

```bash
python3 scripts/invoke_endpoint.py \
    --endpoint-name <endpoint-name> \
    --inference-component-name <component-name> \
    --payload '{"prompt": "hello", "max_tokens": 16}' \
    --wait-for-capacity 900 --region "$REGION"
```

400 `has no capacity` 错误是唤醒信号，而不是故障：它会发布触发步进策略的指标。使用 `--wait-for-capacity` 时，辅助脚本每 30 秒重试一次，直到某个副本处理了该请求。如果不使用它，冷端点看起来总是像坏了一样。

### 清理顺序

`teardown.py` 能处理两种形态，但顺序至关重要：

1. 告警（`<endpoint>-*` 和 `<component>-*`）
2. 扩缩策略和可扩缩目标，基于组件资源 ID
3. **推理组件**
4. 端点、endpoint config、模型

有两种行为使这一顺序成为必要：

- **`delete-endpoint` 不会删除组件。**它们会保留下来，继续报告 `InService`，并阻止创建同名的新组件。始终先删除组件。
- **在瞬态状态下组件删除会被拒绝** — 容器启动期间的 `CREATE_IN_PROGRESS`，以及扩缩操作改变副本数期间的 `UPDATE_RC_IN_PROGRESS`。脚本每 15 秒重试一次，持续 15 分钟；在扩缩事件之后立即进行清理，合理地需要数分钟。

`TargetTracking-inference-component/<ic>-AlarmHigh|Low` 告警属于 Application Auto Scaling。删除策略时会将它们一并删除，因此脚本不会触碰它们（已验证：清理后没有残留告警）。

## 异步推理部署

对于长时间运行的推理（>60 秒）、大负载，或足够突发/稀疏、能从缩容到零中获益的工作负载，请使用 `deploy_async.py` 而不是 `deploy.py`。异步端点在变体本身上就支持 `MinCapacity=0`。实时端点也能缩减到零，但只能通过推理组件——参见下文"实时端点缩容到零"。当单次推理超过 60 秒的 `InvokeEndpoint` 响应限制时，异步仍然是正确的选择。

```bash
python scripts/deploy_async.py \
    --model-name flux-text-to-image \
    --image-uri "$IMAGE_URI" \
    --role-arn "$ROLE_ARN" \
    --instance-type ml.g5.2xlarge \
    --region "$REGION" \
    --output-s3-uri s3://amzn-s3-demo-async-output/async-output/ \
    --env HF_MODEL_ID=black-forest-labs/FLUX.1-dev
```

相对于 `deploy.py` 额外必需的参数：
- `--output-s3-uri` — 异步结果的存放位置（结果不会同步返回）

可选的异步专用标志：
- `--failure-s3-uri` — 失败调用的单独路径
- `--success-sns-topic`、`--error-sns-topic` — 异步结果就绪或失败时接收通知
- `--min-capacity 0`（默认值）— 在批次之间缩容到零
- `--backlog-per-instance-target N` — 每实例的目标队列深度（默认 5）
- `--max-concurrent-invocations-per-instance N` — 默认 4

### 缩容到零的工作原理

异步脚本会在变体上注册**两个**自动扩缩策略：

1. 基于 `ApproximateBacklogSizePerInstance` 的**目标跟踪** — 处理最小值与最大值之间的持续扩缩
2. 由 `HasBacklogWithoutCapacity` CloudWatch 告警触发的**步进扩缩** — 处理 `0→1` 的从零唤醒

两者缺一不可。仅靠目标跟踪无法从零开始转换（它不能除以零个实例），因此如果没有步进策略，端点启动后会在第一批之后缩容到零，然后再也不会唤醒。脚本会自动将其连接好。

### 异步告警

脚本会创建三个 CloudWatch 告警：
- `ApproximateBacklogSize > 50` — 队列积累速度超过容量的消化速度
- `InvocationsFailed > 5` — 反复出现处理失败
- `HasBacklogWithoutCapacity` — 驱动从零唤醒策略（不是通知类告警；其动作是步进扩缩策略，而不是 SNS 主题）

如果传入 `--sns-alarm-topic <arn>`，前两个告警会向该主题发送通知。唤醒告警始终指向步进策略。

### 调用异步端点

异步端点不是同步调用的。你将输入上传到 S3，用 S3 输入位置调用 `invoke-endpoint-async`，SageMaker 完成后会将结果写入你的 `--output-s3-uri`：

```bash
# 先上传输入
aws s3 cp input.json s3://amzn-s3-demo-input/job1/input.json

# 调用
aws sagemaker-runtime invoke-endpoint-async \
    --endpoint-name <endpoint-name> \
    --input-location s3://amzn-s3-demo-input/job1/input.json \
    --content-type application/json \
    --region <region>

# 在输出 URI 处轮询结果
aws s3 cp s3://amzn-s3-demo-async-output/async-output/<inference-id>.out result.json
```

同样的 UTF-8 BOM 注意事项也适用于你上传的 `input.json`（参见上文"UTF-8 BOM 陷阱"）——如果在 Windows 上构建它，请将其写为无 BOM 的 UTF-8，否则容器的 JSON 解析器会拒绝它。

清理方式与实时端点相同：`python3 scripts/teardown.py <endpoint-name>`（清理脚本通过名称前缀发现策略和告警，因此能处理两种部署模式）。

## 默认值一览

| 设置 | 默认值 | 覆盖方式 |
|---|---|---|
| 初始实例数 | 1 | `--initial-instance-count` |
| 自动扩缩最小值 / 最大值 | 1 / 4 | `--min-capacity`、`--max-capacity` |
| 自动扩缩目标 | 每实例每分钟 20 次调用 | `--target-invocations-per-instance` |
| 数据捕获 | 禁用（需主动开启） | `--enable-data-capture` |
| CloudWatch 告警 | 3 个告警 | `--no-alarms` |
| SNS 通知 | 无（会创建告警但不会通知） | `--sns-alarm-topic <arn>` |
| 环境标签 | `dev` | `--environment` |
| InferenceAmiVersion | 无（SageMaker 默认） | `--inference-ami-version`（vLLM CUDA 13+ 必需） |

未设默认值（需要用户特定输入）：VPC 配置、KMS 密钥、多变体、异步推理。

### 自动扩缩目标——按模型类型调整

默认的 `--target-invocations-per-instance 20` 较为保守，是针对每个请求耗时 1–5 秒的 LLM 工作负载调整的。对于嵌入部署（TEI），每个请求要快得多（CPU 上通常 <100ms，GPU 上 <20ms），因此单个实例可以处理高得多的吞吐量。**对于嵌入部署，请根据实例和模型大小将目标提高到 100–500。**默认值 20 会让嵌入部署的自动扩缩过于激进，浪费资金。

经验法则：目标值 ≈ 60 /（典型请求延迟，单位为秒）。延迟 3 秒的 LLM → 目标 20。100ms 的嵌入 → 目标 600。生成式重排序器介于两者之间——它们每个请求只生成一个 token，因此 ~40–100 是合理的目标。

## 数据捕获 + IAM 陷阱

如果用户启用了数据捕获，执行角色需要对捕获前缀具有 S3 写入权限。默认 URI（`s3://sagemaker-<region>-<account>/<endpoint>/data-capture/`）通常与模型制品存储桶不是同一个桶。如果 `hf-cloud-sagemaker-iam-preflight` 将内联策略的范围严格限定为仅模型存储桶，捕获写入会静默失败——端点继续提供服务，但不会出现任何数据。

如果用户报告"数据捕获没有显示"，请检查角色的 S3 访问权限。要么放宽内联策略，要么传入 `--data-capture-s3-uri`，指向角色可写入的存储桶。

## 清理

```bash
python3 scripts/teardown.py <endpoint-name> <region>   # macOS / Linux
python  scripts\teardown.py <endpoint-name> <region>   # Windows
```

按安全顺序删除：告警 → 自动扩缩 → 端点（停止计费）→ endpoint config → 模型。幂等。

**不会**删除：IAM 执行角色（可能被共享）、数据捕获的 S3 对象（用户可能想保留）、SNS 主题、原始模型制品。

在部署摘要之后始终告诉用户清理命令。用户会忘记；端点会持续产生费用。

## 部署失败时

**`CannotStartContainerError` + 从未创建任何 CloudWatch 日志** — 这是 InferenceAmiVersion 问题。如果镜像标签包含 `cu130` 或更高版本，而你没有传入 `--inference-ami-version al2-ami-sagemaker-inference-gpu-3-1`，这就是原因。参见 `hf-cloud-serving-image-selection`。不要去折腾镜像、IAM 角色、环境变量或实例类型——许多其他问题的失败特征与此完全相同，但这里的原因是 AMI。

**"Failed to pass ping health check"** — 容器*确实*启动了并产生了日志，但 `/ping` 没有响应。检查 CloudWatch 中的 `/aws/sagemaker/Endpoints/<endpoint-name>`。通常是：镜像与模型架构不匹配、缺少 HF token，或 OOM。

**"Container failed to start"（存在日志）** — 入口点运行后退出了。检查 CloudWatch。常见原因：缺少必需的环境变量（`SM_VLLM_MODEL`、`SM_VLLM_HOST`、`SM_VLLM_TRUST_REMOTE_CODE`）、`ModelDataUrl` 格式错误、模型制品不可读。

**`ResourceLimitExceeded`** — 该区域中没有此实例类型的配额。申请提高配额或选择其他类型（规划器本应预先检查配额——参见 `hf-cloud-sagemaker-deployment-planner`）。

**CloudWatch 日志中出现 `ImportError: libtorch_cuda.so: undefined symbol: ncclCommResume`** — 这是 `huggingface-pytorch-inference` GPU 镜像中已知的打包缺陷（参见 `hf-cloud-serving-image-selection` 中的"已知损坏的镜像"）。问题位于容器内部，因此任何环境变量、AMI、实例类型或同系列标签都无法修复。请切换到 DJL Inference。

**InService，但调用超时 / 异步输出从未出现** — 存活的 MMS 前端背后是已死亡的 Python worker。执行上文"InService 并不等于成功"中的日志扫描；CloudWatch 中的回溯信息才是真正的错误。

**启动期间从 HF Hub 下载权重时出现 `403 Forbidden`** — 容器内置的 `huggingface_hub` 早于 HF 的 XET CDN 认证。添加 `--env HF_HUB_ENABLE_HF_TRANSFER=0`，或将权重预先放到 S3。注意：这可能会*掩盖*更深层的故障（下载成功后 worker 仍可能崩溃）——修复后请重新检查日志。

**诊断规则**：当多种配置（不同镜像、角色、实例类型）下的失败看起来完全相同，并且**从未产生任何日志**时，原因几乎总是在容器之下——主机 AMI、网络、账户层面——而不是部署配置。停止在配置上反复尝试；检查 AMI 版本和账户状态。

**组件卡在 `Creating`，没有 `FailureReason`** — 容器处于崩溃循环，supervisord 不断重启它，因此状态永远不会改变。组件会一直保持 `Creating`，直到 `ContainerStartupHealthCheckTimeoutInSeconds` 到期，最长可达一小时。读取 `/aws/sagemaker/InferenceComponents/<component-name>`，查找 `exited: app`、`not expected` 或 `api_server.py: error:`。`deploy_ic.py` 在每次轮询时都会执行此扫描，并在大约一分钟内中止。

**`There is not enough hardware resources on the instances for this endpoint`** — 组件的 `ComputeResourceRequirements` 超过了可调度池，而该池比实例内存小得多。降低 `--min-memory-mb`（1024 在 `ml.g5.xlarge` 上可行；4096 会被拒绝）。不要增加实例：即使存在健康的实例也会出现这条消息。

**`Cannot delete inference component ... while it is in state CREATE_IN_PROGRESS` / `UPDATE_RC_IN_PROGRESS`** — 正常现象，不是错误。重试即可；`teardown.py` 会重试 15 分钟。`UPDATE_RC_IN_PROGRESS` 表示扩缩操作正在更改副本数。

**组件比其端点存活更久** — `delete-endpoint` 会留下组件，它们仍然报告 `InService`。它们会阻止名称的重用。先删除组件，这正是 `teardown.py` 的做法。

不要盲目重试。脚本会打印 `describe-endpoint` 中具体的 `FailureReason`——先修复根本原因，再重试。
