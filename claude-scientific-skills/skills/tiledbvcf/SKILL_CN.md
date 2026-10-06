---
name: tiledbvcf
description: 使用 TileDB-VCF 存储和检索基因组变异检出结果。适用于带索引的单样本 VCF/BCF 导入、增量式队列构建、区域与样本查询、流式结果处理、等位基因统计、质控（QC）,以及本地或通过 TileDB Cloud 进行的 VCF/BCF 导出。
license: MIT license
compatibility: Requires a native TileDB-VCF installation and Python 3.9-3.12 for the reviewed Conda builds. bcftools compresses/indexes input fixtures. Installation and remote storage need network access; TileDB Cloud needs its Python client, account token, and storage permissions.
metadata:
  version: "1.3"
  skill-author: Jeremy Leipzig
  last-reviewed: "2026-10-01"
  upstream-version: "TileDB-VCF 0.40.3; tiledb-cloud 0.14.4"
---

# TileDB-VCF

## 何时使用

适用于队列（cohort）变异存储、增量式样本导入、区间查询，以及为下游基因组学分析导出子集。TileDB-VCF 只存储记录；它**不**执行联合变异检出（joint variant calling）、关联检验、归一化,或群体结构调整。数据集大小本身并不能决定云端执行是否合适：应针对预期的样本、区域和属性工作负载做基准测试。

本技能针对已发布的 **TileDB-VCF 0.40.3**。原生 Python/CLI 检查在 macOS ARM64 上使用了两个合成的单样本 VCF。云客户端 **0.14.4** 的契约已对照其发布的 wheel 包和模拟调度进行了检查；未实际执行托管查询和作业。见[安装与验证说明](references/verification.md)。

## 安装并验证原生技术栈

截至本次审查，`tiledbvcf` 的 Python 发行版尚未发布在 PyPI 上。官方的 **`tiledb` Conda 频道**为 macOS ARM64、
macOS x86-64 和 Linux x86-64 提供了 `tiledbvcf-py` 0.40.3，并带有 Python 3.9-3.12 的构建版本。PyPI 上的 `tiledb` 是 TileDB-Py，并不会安装 TileDB-VCF。原生 Apple Silicon 不再需要强制设置 `CONDA_SUBDIR=osx-64`。

对于经测试的 macOS ARM64 环境，下面的版本锚定可以避免在原本可以成功解析的当前 Conda 解析结果中出现版本化库导入失败的问题：

```bash
conda create -n tiledb-vcf -c tiledb -c conda-forge \
  python=3.12 tiledbvcf-py=0.40.3 \
  azure-core-cpp=1.16.2 azure-storage-blobs-cpp=12.16.0 \
  azure-storage-files-datalake-cpp=12.14.0 capnproto=1.4.0 c-blosc2=2.23.1
conda activate tiledb-vcf
python -c 'import tiledbvcf; print(tiledbvcf.version)'
tiledbvcf version
```

等效的 Micromamba 解析/安装流程也已实际执行过。这些额外的 ABI 版本锚定是针对 macOS ARM64 的、经验证的变通方案，并不是对所有平台都适用的断言。生产环境应保留已解析出的环境。其他平台的安装方式和官方 Docker 镜像是上游文档中记载的替代方案，本技能未对它们进行测试。

## 准备并创建队列（cohort）

1. 记录参考基因组组装版本、contig 命名/长度、使用的调用软件（caller）、归一化规则、样本身份,以及文件校验和。不要混用不同的基因组组装版本，也不要假定 `1` 和
   `chr1` 是等价的。确认各输入文件之间 header 是兼容的。
2. 每个输入文件必须只包含**一个样本**，按坐标排序，并带有索引。使用经 BGZF 压缩的 VCF 或 BCF，并配有匹配的
   `.csi`/`.tbi`。用 `bcftools query -l sample1.vcf.gz` 检查；文件名并不是样本标识符。
3. 显式创建数据集，然后再导入。仅以 `mode="w"` 打开并不会创建其 schema。在创建时就实体化（materialize）那些会被频繁读取的字段。
4. 在扩大规模之前，先在一个已知的小区间上验证一次往返导出（round-trip export）。

对于现有的已排序纯文本 VCF（每个输入文件只需运行一次；输出文件名必须是新的）：

```bash
bcftools view -Oz -o sample1.vcf.gz sample1.vcf
bcftools index -c sample1.vcf.gz
bcftools view -Oz -o sample2.vcf.gz sample2.vcf
bcftools index -c sample2.vcf.gz
```

以下本地示例使用样本 ID `S1` 和 `S2`、contig
`chr1`，坐标 1-100 进行了实际测试；在真实数据中请替换为经验证的 ID 和区间。

```python
import tiledbvcf

uri = "cohort"
config = {"sm.compute_concurrency_level": "2", "sm.io_concurrency_level": "2"}
with tiledbvcf.Dataset(uri, mode="w", tiledb_config=config) as ds:
    ds.create_dataset(extra_attrs=["fmt_GT", "fmt_DP"])
    ds.ingest_samples(
        ["sample1.vcf.gz"], threads=2, total_memory_budget_mb=512
    )

# 增量导入使用已存在的数据集；不要再次调用 create_dataset。
with tiledbvcf.Dataset(uri, mode="w", tiledb_config=config) as ds:
    ds.ingest_samples(
        ["sample2.vcf.gz"], threads=2, total_memory_budget_mb=512
    )
```

schema-v4 的数据数组有 `contig`、起始坐标和样本这几个**维度**；
header 和可选的统计信息是数据集组内的独立数组。未被显式实体化的字段仍保留在 INFO/FORMAT 负载中。像
`pos_start` 这样的查询名称并不需要与原始存储列名一致。

上游支持并行的线程/进程导入。应为不同任务分配不同的样本，并协调好生命周期/维护操作；不要盲目地重复导入样本。
`resume=True` 支持恢复被中断的导入，而不是任意的重复纠正。

## 完整查询并正确解释坐标

| 接口 | 坐标约定 |
| --- | --- |
| Python `regions=["chr1:10-14"]` | 1 起始，闭区间 |
| 返回的 `pos_start`、`pos_end` | 1 起始，记录端点均包含在内 |
| BED 输入以及 `query_bed_start`、`query_bed_end` | 0 起始，半开区间 |
| 0.40.3 中 `read_variant_stats()` / `read_allele_count()` 返回的 `pos` 列 | **0 起始**；在与 VCF 的 POS 字段关联之前要加 1 |

查询返回的是**与区间重叠的记录**，而不仅仅是起点落在区间内的记录。
一个跨越位置 10-14 的缺失会出现在 `chr1:14-14` 查询结果中，其
`pos_start=10`。对于 BED 的 `[13,14)`，对应的字符串是 `chr1:14-14`。
Python 的区域解析器要求显式写出 `contig:start-end`；在本版本中，裸的 `"chr1"`
会被拒绝。对整个 contig 查询时应使用一个已知的 contig 长度。

```python
cfg = tiledbvcf.ReadConfig(memory_budget_mb=128, tiledb_config=config)
attrs = ["sample_name", "contig", "pos_start", "pos_end", "alleles", "fmt_GT"]
with tiledbvcf.Dataset(uri, cfg=cfg) as ds:
    assert {"S1", "S2"}.issubset(ds.samples())
    assert set(attrs).issubset(ds.attributes())
    for batch in ds.read_iter(
        attrs=attrs, regions=["chr1:1-100"], samples=["S1", "S2"]
    ):
        print(batch)  # 替换为一个有限制的消费者或分区输出。
```

- `read()` 返回一个 pandas DataFrame；`read_arrow()` 返回一个 PyArrow Table。
  两者都可能只返回第一个受内存限制的批次。应持续调用
  `continue_read()` / `continue_read_arrow()` 直到 `read_completed()`，或者对普通的 DataFrame 查询使用
  `read_iter()`。当结果无法完全放入内存时，避免拼接所有批次。
- `ReadConfig(memory_budget_mb=...)` 控制的是读取操作；写入时请使用
  `ingest_samples(total_memory_budget_mb=...)`。读取预算并不是进程 RSS 的上限。`limit` 截断的是总输出量；它不是分页大小。
- `sample_partition=(0, 2)` 选择两个分区中的第零个分区。类似地，
  `region_partition=(index, number_of_partitions)` 对查询区域进行分区；
  这些元组不是坐标边界、tile 范围或样本容量。
- **0.40.3 会保留 BED 选择状态**，即当后续调用省略 `bed_file` 时也是如此。
  在更改 BED/区域输入时，应打开一个全新的 `Dataset` 以进行独立查询。
- `fmt_GT` 包含等位基因索引：0 表示 REF，正值索引 ALT，
  -1 表示缺失。应保留多等位基因身份和倍性信息；不要把每一个正整数都当作双等位基因剂量，也不要把缺失的调用当作参考基因型。
  这个整数列表本身并不编码原始的带相位（phased）GT 字符串。

## 导出与验证

```python
from pathlib import Path

Path("exported").mkdir(exist_ok=True)
with tiledbvcf.Dataset(uri, cfg=cfg) as ds:
    ds.export(
        samples=["S1"], regions=["chr1:1-100"],
        output_format="v", output_dir="exported",
    )
```

Python 导出格式：`v` VCF、`z` 压缩 VCF、`u` 未压缩 BCF、`b`
压缩 BCF。`merge=False` 为每个样本写出单独的文件；`merge=True` 需要一个
合并后的 `output_path`。合并导出并不是联合变异检出。导出的文件在用于带索引的下游访问之前应重新建立索引。应比较样本 ID、contig、记录
数量、等位基因、INFO/FORMAT 值,以及缺失/带相位的基因型；语义上的往返保留并不意味着字节级相同的压缩方式或 header。

CLI 接受位置参数形式的样本路径,或 `--samples-file`（每行一个 URI），
而不是逗号分隔的 `--samples` 参数：

```bash
tiledbvcf create --uri cli_cohort
tiledbvcf store --uri cli_cohort --threads 2 --total-memory-budget-mb 512 \
  -- sample1.vcf.gz sample2.vcf.gz
tiledbvcf list --uri cli_cohort
tiledbvcf stat --uri cli_cohort
tiledbvcf export --uri cli_cohort --regions chr1:1-100 \
  --sample-names S1,S2 -Ot --tsv-fields 'SAMPLE,CHR,POS,REF,ALT,F:GT' \
  --output-path variants.tsv
```

`--` 用于保护位置路径参数不被类似 `--tiledb-config` 这样的可变长度选项误解析。应同时检查预期的产物、样本数量,以及退出码：在经审查的 CLI 中，一个无效的 store 命令会在打印错误信息的同时返回退出码零。TSV 字段中 FORMAT/GT 使用 `F:GT`，INFO/DP 使用 `I:DP`。

## 队列统计与质控

```python
with tiledbvcf.Dataset(uri, cfg=cfg) as ds:
    stats = ds.read_variant_stats(regions=["chr1:1-100"], drop_ref=True)
    stats["vcf_pos"] = stats["pos"] + 1
    print(stats[["contig", "vcf_pos", "alleles", "ac", "an", "af"]])

qc = tiledbvcf.sample_qc(uri, samples=["S1"], config=config)
print(qc)
```

统计数组在创建时默认启用；较旧的/被禁用的数组可能不支持这些操作。
`read_variant_stats` 没有 `samples` 参数。
较旧的 `read_allele_frequency(dataset_uri, region)` 包装函数接受单个
区域，并委托给已废弃的单数参数；应优先使用上面的 Dataset 方法。`sample_qc` 的第一个参数是 `dataset_uri`，而不是 `uri`。

`ac`、`an` 和 `af` 的值总结的是已导入的整个队列，而不是某个选定的
族群或查询出的样本子集。在经测试的发布版本中，`read(samples=[...], set_af_filter=">0.6")`
过滤仍然使用的是全队列的 AF。应从正确选出的调用结果中计算子群体频率,并明确规定缺失值、倍性、可调用区域（callable-region）
和 gVCF 参考区块（reference-block）的处理策略。应使用恰当的已调用等位基因分母，而不是统一使用
`2 * number_of_samples`；一条缺失的 VCF 记录并不能证明该位点是纯合参考基因型。QC 指标和稀疏存储本身并不能确立 GWAS
的可用性或科学有效性。

## 对象存储与 TileDB Cloud

直接存储使用 `s3://bucket/path`、`azure://container/path` 或
`gcs://bucket/path`，由已安装的 TileDB 后端和其对应的提供方凭证支持。这并不会自动分布式执行计算。应使用提供方的凭证链或范围受限的配置，并验证对数据集和源索引两者的访问权限。TileDB Cloud 的 token
与存储桶凭证是不同的概念。下面的远程存储示例仅作说明性用途、已经过源码核实,但并非经过身份验证的端到端测试。

在兼容的环境中安装 `tiledb-cloud==0.14.4`。它的 `life-sciences`
附加组件添加的是 TileDB-SOMA，**不是** TileDB-VCF。在导入客户端之前，通过执行环境提供
`TILEDB_REST_TOKEN`；如有需要，`TILEDB_REST_HOST` 可以选择一个
自定义部署。不要把 token 嵌入代码中，也不要打印配置信息。

```python
# 示例性：需要一个可访问的已注册队列和一个计费命名空间。
import tiledb.cloud
import tiledb.cloud.vcf

cloud_cfg = tiledb.cloud.Config()
with tiledbvcf.Dataset("tiledb://my-namespace/cohort", tiledb_config=cloud_cfg) as ds:
    sample_names = ds.samples()

result = tiledb.cloud.vcf.read(
    dataset_uri="tiledb://my-namespace/cohort",
    config=cloud_cfg, attrs=["sample_name", "pos_start", "fmt_GT"],
    regions=["chr1:1-100"], samples=sample_names[:2],
    num_region_partitions=1, namespace="my-namespace", max_workers=2,
)
frame = result.to_pandas()  # read 返回的是 Arrow table，而不是 DataFrame。
```

分布式读取会在内部组装出一个 Arrow 结果，可能会使用大量的 worker/客户端
内存。应限定所请求的区域/样本以及 worker 数量；分区并不能使最终拼接出的结果变得不占内存。这是 SDK 任务执行，而不是分页式的 VCF REST 列表 API。

```python
# 示例性的、会产生副作用的云任务：仅在经授权的导入任务中使用。
submission = tiledb.cloud.vcf.ingest(
    dataset_uri="s3://my-bucket/cohort",
    sample_list_uri="s3://my-bucket/inputs/sample-uris.txt",
    namespace="my-namespace", acn="registered-storage-role",
    register_name="cohort", max_samples=2,
    ingest_resources={"cpu": "2", "memory": "4Gi"},
)
print(submission["graph_id"])
```

`search_uri`、`sample_list_uri` 或 `metadata_uri` 三者中只能恰好使用一个；文件搜索模式适用于 `search_uri`。注册需要访问凭证名称
（`acn`）。`vcf.ingest` 异步提交任务，返回
`{"status": "started", "graph_id": ...}`；应追踪该任务图直到终态成功，并在声称完成之前验证已导入的样本。目前没有已发布的
`ingest_vcf_dataset(source=..., output=...)` API。定价、可用性、安全
控制措施以及部署义务需要参照当前的账户/服务条款。

## 官方参考资料

- [TileDB-VCF 0.40.3 发布说明](https://github.com/TileDB-Inc/TileDB-VCF/releases/tag/0.40.3)
- [Dataset API](https://tiledb-inc.github.io/TileDB-VCF/documentation/reference/Dataset.html)
- [导入（Ingestion）](https://tiledb-inc.github.io/TileDB-VCF/documentation/how-to/ingest-samples.html)
- [大型查询](https://tiledb-inc.github.io/TileDB-VCF/documentation/how-to/handle-large-queries.html)
- [云存储](https://tiledb-inc.github.io/TileDB-VCF/documentation/how-to/work-with-cloud-object-stores.html)
- [TileDB Cloud 客户端发布版本](https://pypi.org/project/tiledb-cloud/0.14.4/)
- [验证细节与已知的发布版本问题](references/verification.md)
