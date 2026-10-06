---
name: lamindb
description: 使用LaminDB管理生物学数据集和模型，包括产物（artifact）注册、血缘追踪、schema验证、Bionty本体注释、查询/搜索、集合（collections）、分支（branches）、存储和工作流集成。用于可复现的生物学数据整理或LaminDB数据湖仓。
license: Apache-2.0 license
compatibility: Requires Python 3.10-3.14 and lamindb; examples tested on Python 3.12 with lamindb 2.10.0, bionty 2.5.0, and IPython. Local SQLite needs no login; public ontologies and remote storage require network access, and private instances require credentials.
metadata:
  version: "2.0"
  last-reviewed: "2026-09-30"
  skill-author: K-Dense Inc.
---

# LaminDB

## 何时使用

用于注册生物学数据集、整理DataFrame/AnnData元数据、查询已注释的
产物，以及追踪科学脚本或工作流程。LaminDB将元数据存储在
SQLite/PostgreSQL中，文件存储在已配置的存储空间中；仅仅注册并
不能确立科学有效性或FAIR合规性。

此技能面向**LaminDB 2.10.0和Bionty 2.5.0**。本地示例已在Python
3.12、pandas 3.0.6和AnnData 0.13.2上执行。LaminDB发行版将AnnData
限定在0.13.2以内；请保留其依赖约束。为注册表的同义词辅助工具
（本版本中 `add_synonym()` 导入了IPython）安装IPython。

## 工作流程

1. 用 `lamin info` 确认预期的实例、存储和写入范围。对于实验，使用
   一个新的本地开发目录。参见[安装和部署](references/setup-deployment.md)。
2. 为生物学数据定义有类型的 `Feature` 记录和一个 `Schema`。对受控
   词汇表使用由注册表支持的分类数据类型；`dtype=str` 只检查字符串。
   参见[注释和验证](references/annotation-validation.md)。
3. 审查本体来源/版本和物种。只标准化经过审查的同义词，并保留
   未解析的注释。参见[Bionty本体](references/ontologies.md)。
4. 在一个脚本或notebook中，启动 `ln.track()`，加载已注册的输入，
   验证，并保存输出。`curator.validate()` 成功时返回 `None`，失败时
   引发 `ln.errors.ValidationError`。修复后再次验证。
5. 通过curator或一个有schema意识的产物构造器进行保存。检查存储的
   schema和往返的内容；用 `ln.finish()` 完成一次成功的运行。
6. 在加载内容之前查询元数据。为可复现性记录产物的UID和schema/来源
   溯源信息；一个key后续可能解析到一个更新的版本。参见
   [查询和流式处理](references/data-management.md)。

## 本地实战示例

在一个专用环境和一个空的项目目录中运行：

```bash
uv venv --python 3.12
uv pip install 'lamindb==2.10.0' 'bionty==2.5.0' 'ipython==9.17.1'
source .venv/bin/activate
lamin init --storage ./storage --name biology-demo --modules bionty
```

将以下内容保存为 `curate_qc.py`，然后运行 `python curate_qc.py`：

```python
import pandas as pd
import lamindb as ln

ln.track(params={"analysis": "QC metadata curation"})
count = ln.Feature(name="gene_count", dtype=int).save()
condition = ln.Feature(name="condition", dtype=str).save()
schema = ln.Schema(
    name="qc_metadata",
    features=[count, condition],
    maximal_set=True,  # 拒绝额外的列
).save()
df = pd.DataFrame({
    "gene_count": [120, 130],
    "condition": ["control", "treated"],
})
curator = ln.curators.DataFrameCurator(df, schema)
curator.validate()  # 数据无效时会引发异常；不要将其用作if条件
artifact = curator.save_artifact(key="experiments/qc.parquet")
assert artifact.schema == schema
pd.testing.assert_frame_equal(artifact.load(), df)
ln.finish()
```

这验证的是表结构/类型，而不是计数值是否满足检测的质量控制要求。
在发表或下游分析之前，添加特定于检测的检查（单位、允许范围、
缺失情况、重复的样本ID、批次平衡）。

## 核心对象和契约

| 对象 | 用途和重要约束 |
| --- | --- |
| `Artifact` | 一个文件/文件夹或序列化的数据集；`cache()` 获取一个本地路径，`load()` 将内容实体化，`open()` 返回一个特定于格式的访问器。 |
| `Feature` | 一个有类型的元数据字段；在 `artifact.features.set_values(...)` 之前先保存其定义。 |
| `Schema` | 验证规则和特征成员身份；`maximal_set=True` 拒绝额外项。单独的 `flexible=False` 不会这样做。 |
| `Record`、`ULabel` | 实验实体和简单标签。一个自定义术语不是一个本体断言。 |
| `Run`、`Transform` | 一次执行及其代码定义。输入是 `run.input_artifacts`；输出是 `run.output_artifacts`。 |
| `Collection` | 一组有版本的产物；用 `collection.artifacts.all()` 遍历。 |
| `Project`、`Branch`、`Space` | 分组、变更组织和访问范围；分支不能替代权限控制。 |

对一个工作流入口点使用 `@ln.flow()`，在其内部使用 `@ln.step()`。
血缘追踪的是被追踪的访问，而不是LaminDB之外的任意读取操作。
关于追踪、标签和修订版本，参见[核心概念](references/core-concepts.md)。

## 需要避免的失败模式

- `Artifact.backed()`、`delete_cache()` 和 `is_cached()` 在2.10.0中
  不存在。使用受支持的 `open()`/`cache()` 契约和缓存设置。
- 一个Parquet的 `open()` 结果是一个PyArrow数据集，不是字节流。
  一个AnnData访问器是一个上下文管理器；用 `.to_memory()` 将一个切片
  实体化。
- 不存在 `Artifact.is_valid` 查询字段。查询实际使用的确切 `schema`，
  并保留验证证据。赋值一个schema ID不能替代整理过程。
- `curator.cat.add_ontology()` 和 `inspect_standardize()` 不存在。
  定义该特征的Bionty数据类型，使用由来源支持的记录，并使用
  `cat.standardize()`。对于AnnData，使用 `curator.slots["obs"].cat`，
  而不是 `curator.cat`。
- Bionty的 `from_values()` 可能省略未解析的值，并返回未保存的记录。
  显式检查所有值，并在链接它们之前保存记录。
- 不要将 `lamindb-wetlab` 作为一个Lamin Labs模块安装。当前的官方
  文档描述的是用于扰动的 `pertdb` 和用于灵活实验室实体的 `Record`。
- 不要编造管理命令。当前的设置使用
  `lamin settings cache-dir ...`、`lamin disconnect` 和
  `lamin migrate deploy`；云端共享和备份需要它们实际文档记录的系统。

## 集成和验证边界

关于Nextflow的 `nf-lamin`、外部ML运行ID、DuckDB、Git以及指向官方
工作流示例的链接，参见[集成](references/integrations.md)。需要
私有Hub访问、云写入、外部工作流服务或公共本体下载的示例是
示范性的/经来源验证的，除非明确标注为已执行。

本地回归测试覆盖范围包括DataFrame和AnnData整理、无效数据拒绝、
往返测试、特征、修订版本、集合访问、本地Bionty同义词/层级结构，
以及被追踪的输入/输出血缘关系。发行版/来源审查记录在
[审查来源](references/sources.md)中。

将API密钥、云凭证和数据库密码排除在输出之外。对经认证的工作，
使用工作负载身份或命名的环境变量。一次本地试运行不得更改一个
现有实例或一个共享缓存。

## 引用 Scientific Agent Skills

此技能是 K-Dense 出品的 Scientific Agent Skills 的一部分。如果它对某篇
手稿、报告、演示或代码发布有实质性贡献，请将该论文添加到参考文献或
软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 都指向
最新的 arXiv 版本，因此切勿附加诸如 `v1` 的版本后缀。在可访问网络的
情况下，请在撰写引用之前先获取 https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中获取
作者列表、年份和版本信息。如果该记录列出了期刊参考文献或出版商 DOI，
请改为引用已发表的版本。
