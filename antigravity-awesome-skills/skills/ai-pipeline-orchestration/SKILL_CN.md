---
name: ai-pipeline-orchestration
description: 使用 Prefect、Airflow 或 Dagster 编排 AI/ML 流水线，涵盖数据摄取、模型训练、批量推理和
  RAG 索引。
category: devops
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: 需要相关平台的 CLI（kubectl、helm、terraform、git、CI 运行器）以及对目标环境的授权访问。仅文档形式导入；不捆绑辅助脚本和模板。
metadata:
  author: devops-skills
  version: '1.0'
---

# AI Pipeline Orchestration

构建可靠、可观测的 AI 工作流 —— 从文档摄取到批量推理再到模型训练流水线。

## 何时使用此技能

在以下场景使用此技能:
- 调度周期性的 RAG 文档摄取与重新索引
- 编排多步骤的批量 LLM 处理工作流
- 运行夜间模型评估和微调作业
- 构建馈入 AI 模型的 ETL 流水线
- 管理数据准备与模型服务之间的依赖关系

## 工具选择

| 工具 | 最适合 | 复杂度 | GPU 作业 |
|------|----------|------------|----------|
| **Prefect** | 现代 Python 优先;易于上手 | 低 | 良好 |
| **Airflow** | 复杂 DAG;大型团队;已有使用基础 | 高 | 良好 |
| **Dagster** | 以资产为中心;强大的数据血缘 | 中 | 出色 |
| **Temporal** | 长时间运行的工作流;可靠性优先 | 中 | 良好 |

## Prefect —— 快速开始

```bash
pip install prefect prefect-kubernetes

# 启动 Prefect server(或使用 Prefect Cloud)
prefect server start

# 在另一个终端中
prefect worker start --pool default-agent-pool
```

## Prefect:RAG 摄取流水线

```python
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta
import hashlib

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=24))
def fetch_documents(source_url: str) -> list[dict]:
    """从数据源获取文档;结果缓存以避免重复获取。"""
    logger = get_run_logger()
    logger.info(f"Fetching from {source_url}")
    # ... 获取逻辑
    return documents

@task(retries=3, retry_delay_seconds=30)
def chunk_and_embed(documents: list[dict]) -> list[dict]:
    """对文档分块并生成向量嵌入,失败时重试。"""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("BAAI/bge-large-en-v1.5")
    chunks = []
    for doc in documents:
        doc_chunks = chunk_text(doc["content"])
        embeddings = model.encode(doc_chunks, batch_size=64)
        for chunk, emb in zip(doc_chunks, embeddings):
            chunks.append({"text": chunk, "embedding": emb.tolist(),
                           "source": doc["url"], "doc_hash": doc["hash"]})
    return chunks

@task(retries=2)
def upsert_to_vector_store(chunks: list[dict]) -> int:
    """将嵌入向量更新写入 Qdrant,跳过未变更的文档。"""
    from qdrant_client import QdrantClient
    client = QdrantClient("http://qdrant:6333")
    client.upsert(collection_name="knowledge-base", points=[...])
    return len(chunks)

@flow(name="rag-ingestion", log_prints=True)
def rag_ingestion_pipeline(sources: list[str]):
    """完整的 RAG 摄取流程 —— 每天运行一次。"""
    logger = get_run_logger()
    total = 0
    for source in sources:
        docs = fetch_documents(source)
        chunks = chunk_and_embed(docs)
        count = upsert_to_vector_store(chunks)
        total += count
        logger.info(f"Ingested {count} chunks from {source}")
    logger.info(f"Pipeline complete: {total} total chunks indexed")

if __name__ == "__main__":
    rag_ingestion_pipeline.serve(
        name="daily-rag-ingestion",
        cron="0 2 * * *",          # 每天凌晨 2 点
        parameters={"sources": ["https://docs.myapp.com", "https://api.myapp.com/kb"]},
    )
```

## Prefect:批量 LLM 推理流水线

```python
from prefect import flow, task
from prefect.concurrency.sync import concurrency
import asyncio
from openai import AsyncOpenAI

@task(retries=3, retry_delay_seconds=60)
async def process_batch(items: list[dict], model: str = "gpt-4o-mini") -> list[dict]:
    """通过 LLM 处理一批条目,并带有速率限制保护。"""
    client = AsyncOpenAI()
    async with concurrency("openai-api", occupy=len(items)):  # 速率限制
        tasks = [
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": item["prompt"]}],
                max_tokens=256,
            )
            for item in items
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    for item, response in zip(items, responses):
        if isinstance(response, Exception):
            results.append({**item, "error": str(response), "output": None})
        else:
            results.append({**item, "output": response.choices[0].message.content})
    return results

@flow(name="batch-llm-inference")
async def batch_inference_flow(input_file: str, output_file: str, batch_size: int = 50):
    import json
    items = [json.loads(line) for line in open(input_file)]
    batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]

    all_results = []
    for batch in batches:
        results = await process_batch(batch)
        all_results.extend(results)

    with open(output_file, "w") as f:
        for result in all_results:
            f.write(json.dumps(result) + "\n")
    return len(all_results)
```

## Airflow:模型训练 DAG

```python
from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s

@dag(
    dag_id="llm_fine_tuning",
    schedule="@weekly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["ai", "training"],
)
def llm_fine_tuning_dag():

    @task
    def prepare_dataset() -> str:
        """下载并预处理训练数据。"""
        # ... 数据准备逻辑
        return "s3://my-bucket/training-data/2025-03-01/"

    train = KubernetesPodOperator(
        task_id="train_model",
        name="llm-training-job",
        namespace="ml",
        image="nvcr.io/nvidia/pytorch:24.05-py3",
        cmds=["accelerate", "launch", "-m", "axolotl.cli.train", "/config/config.yaml"],
        resources=k8s.V1ResourceRequirements(
            limits={"nvidia.com/gpu": "4", "memory": "320Gi"},
            requests={"nvidia.com/gpu": "4"},
        ),
        node_selector={"nvidia.com/gpu.product": "A100-SXM4-80GB"},
        volumes=[...],
        volume_mounts=[...],
        get_logs=True,
        is_delete_operator_pod=True,
    )

    @task
    def evaluate_model(dataset_path: str) -> dict:
        """运行评估;如果质量下降则使流水线失败。"""
        metrics = run_evals()
        if metrics["accuracy"] < 0.85:
            raise ValueError(f"Model quality too low: {metrics}")
        return metrics

    @task
    def deploy_model(metrics: dict):
        """将合并后的模型推送到 HF Hub 并更新 vLLM 配置。"""
        update_serving_config(new_model="org/fine-tuned-v2")

    dataset = prepare_dataset()
    train.set_upstream(dataset)
    eval_result = evaluate_model(dataset)
    eval_result.set_upstream(train)
    deploy_model(eval_result)

llm_fine_tuning_dag()
```

## Dagster:基于资产的 AI 流水线

```python
from dagster import asset, AssetExecutionContext, define_asset_job, ScheduleDefinition

@asset(description="Raw documents fetched from knowledge sources")
def raw_documents(context: AssetExecutionContext) -> list[dict]:
    context.log.info("Fetching documents...")
    return fetch_all_documents()

@asset(
    deps=[raw_documents],
    description="Chunked and embedded document vectors",
)
def document_embeddings(context: AssetExecutionContext, raw_documents) -> int:
    chunks = process_and_embed(raw_documents)
    context.log.info(f"Generated {len(chunks)} embeddings")
    upsert_to_qdrant(chunks)
    return len(chunks)

@asset(
    deps=[document_embeddings],
    description="RAG system quality metrics",
)
def rag_quality_metrics(context: AssetExecutionContext) -> dict:
    metrics = evaluate_rag_system()
    context.add_output_metadata({"ragas_score": metrics["ragas_score"]})
    return metrics

# 调度:每晚刷新嵌入向量
nightly_refresh = ScheduleDefinition(
    job=define_asset_job("rag_refresh_job", [raw_documents, document_embeddings]),
    cron_schedule="0 1 * * *",
)
```

## 最佳实践

- 对 API 调用使用任务级重试;对瞬时基础设施故障使用流程级重试。
- 缓存高成本的步骤(嵌入生成、数据获取)以加快重跑速度。
- 从流水线中输出自定义指标(分块数、错误率、成本)到你的可观测性系统。
- 在 Prefect 中使用 `concurrency` 限制,或在 Airflow 中使用 `pool` 槽位,以遵守外部速率限制。
- 将摄取、训练和部署流水线分离 —— 不要把它们耦合在一个巨大的 DAG 中。

## 相关技能

- rag-infrastructure (`rag-infrastructure`) - RAG 系统搭建
- llm-fine-tuning (`llm-fine-tuning`) - 训练作业
- agent-observability (`agent-observability`) - 流水线监控
- kubernetes-ops (`kubernetes-ops`) - 在 K8s 上运行流水线 pod

## 限制

- 本指南会针对真实环境执行:在应用任何操作之前,确认目标、影响范围和回滚方案。
- 未经明确批准,绝不部署到生产环境。仅文档形式导入:不捆绑上游脚本和模板。

### 示例

```bash
git status && git diff --stat
kubectl diff -f manifest.yaml
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills)(MIT);为符合上游合规要求,添加了 frontmatter、"何时使用"/"限制" 部分及安全边界。仅文档形式导入:不捆绑辅助脚本和模板。
