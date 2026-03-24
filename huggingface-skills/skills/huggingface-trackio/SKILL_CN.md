---
name: huggingface-trackio
description: 使用 Trackio 跟踪和可视化 ML 训练实验。在训练期间记录指标（Python API）、为训练诊断触发警报或检索/分析记录的指标（CLI）时使用。支持实时仪表板可视化、带有 webhook 的警报、HF Space 同步以及用于自动化的 JSON 输出。
---

# Trackio - ML 训练的实验跟踪

Trackio 是一个实验跟踪库，用于记录和可视化 ML 训练指标。它同步到 Hugging Face Spaces 以实现实时监控仪表板。

## 三个接口

| 任务 | 接口 | 参考 |
|------|-----------|-----------|
| **在训练期间记录指标** | Python API | [references/logging_metrics.md](references/logging_metrics.md) |
| **为训练诊断触发警报** | Python API | [references/alerts.md](references/alerts.md) |
| **在训练后/期间检索指标和警报** | CLI | [references/retrieving_metrics.md](references/retrieving_metrics.md) |

## 何时使用每个接口

### Python API → 记录

在训练脚本中使用 `import trackio` 来记录指标：

- 使用 `trackio.init()` 初始化跟踪
- 使用 `trackio.log()` 记录指标或使用 TRL 的 `report_to="trackio"`
- 使用 `trackio.finish()` 完成

**关键概念**：对于远程/云训练，传递 `space_id` — 指标同步到 Space 仪表板，以便在实例终止后保持持久性。

→ 有关设置、TRL 集成和配置选项，请参见 [references/logging_metrics.md](references/logging_metrics.md)。

### Python API → 警报

在训练代码中插入 `trackio.alert()` 调用来标记重要事件 — 就像插入打印语句进行调试一样，但具有结构化和可查询性：

- `trackio.alert(title="...", level=trackio.AlertLevel.WARN)` — 触发警报
- 三个严重性级别：`INFO`、`WARN`、`ERROR`
- 警报会打印到终端，存储在数据库中，显示在仪表板中，并可选地发送到 webhook（Slack/Discord）

**LLM 代理的关键概念**：警报是自主实验迭代的主要机制。代理应该在训练代码中为诊断条件（损失尖峰、NaN 梯度、低准确率、训练停滞）插入警报。由于警报会打印到终端，监视训练脚本输出的代理会自动看到它们。对于后台或分离运行，代理可以通过 CLI 轮询。

→ 有关完整的警报 API、webhook 设置和自主代理工作流程，请参见 [references/alerts.md](references/alerts.md)。

### CLI → 检索

使用 `trackio` 命令查询记录的指标和警报：

- `trackio list projects/runs/metrics` — 发现可用内容
- `trackio get project/run/metric` — 检索摘要和值
- `trackio list alerts --project <name> --json` — 检索警报
- `trackio show` — 启动仪表板
- `trackio sync` — 同步到 HF Space

**关键概念**：添加 `--json` 以获取适合自动化和 LLM 代理的程序化输出。

→ 有关所有命令、工作流程和 JSON 输出格式，请参见 [references/retrieving_metrics.md](references/retrieving_metrics.md)。

## 最小记录设置

```python
import trackio

trackio.init(project="my-project", space_id="username/trackio")
trackio.log({"loss": 0.1, "accuracy": 0.9})
trackio.log({"loss": 0.09, "accuracy": 0.91})
trackio.finish()
```

### 最小检索

```bash
trackio list projects --json
trackio get metric --project my-project --run my-run --metric loss --json
```

## 自主 ML 实验工作流程

当作为 LLM 代理自主运行实验时，推荐的工作流程是：

1. **设置带警报的训练** — 为诊断条件插入 `trackio.alert()` 调用
2. **启动训练** — 在后台运行脚本
3. **轮询警报** — 使用 `trackio list alerts --project <name> --json --since <timestamp>` 检查新警报
4. **读取指标** — 使用 `trackio get metric ...` 检查特定值
5. **迭代** — 根据警报和指标，停止运行，调整超参数，并启动新运行

```python
import trackio

trackio.init(project="my-project", config={"lr": 1e-4})

for step in range(num_steps):
    loss = train_step()
    trackio.log({"loss": loss, "step": step})

    if step > 100 and loss > 5.0:
        trackio.alert(
            title="Loss divergence",
            text=f"Loss {loss:.4f} still high after {step} steps",
            level=trackio.AlertLevel.ERROR,
        )
    if step > 0 and abs(loss) < 1e-8:
        trackio.alert(
            title="Vanishing loss",
            text="Loss near zero — possible gradient collapse",
            level=trackio.AlertLevel.WARN,
        )

trackio.finish()
```

然后从单独的终端/进程轮询：

```bash
trackio list alerts --project my-project --json --since "2025-01-01T00:00:00"
```