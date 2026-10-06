---
name: pacsomatic
description: 从未比对的 BAM 输入准备并启动 nf-core/pacsomatic 配对肿瘤-正常 PacBio HiFi 基因组工作流。支持生成样本表、固定版本的 Nextflow 启动工件、本地检查、LSF/Slurm/PBS Pro/SGE 启动器提交，以及启动故障排查。用于 pacsomatic 的运行准备和执行，而不是通用的短读长体细胞变异分析或医学影像 PACS。
license: MIT
compatibility: Requires Python 3.10+ for the standard-library helper. Execution requires Bash, Nextflow >=24.04.2, a compatible Java runtime (current Nextflow supports Java 17-26), the selected container runtime and optionally a scheduler. Network access is needed for uncached pipeline code, plugins, references and containers.
metadata:
  version: "1.4"
  skill-author: Beifang Niu
  contributors: Haidong, Wenchao
  upstream-pipeline: https://github.com/nf-core/pacsomatic
  upstream-revision: "24c84cb371b0339c1d65a4de9451671945e19772"
  last-reviewed: "2026-10-01"
---

# pacsomatic

## 何时使用

使用 [scripts/run_pacsomatic.py](scripts/run_pacsomatic.py) 来准备一对匹配的
PacBio HiFi 肿瘤/正常样本，生成样本表和可复现的启动工件，并在本地启动或将
**Nextflow 驱动程序**提交到调度器。该流程会重新比对输入 BAM；此辅助工具针对
未比对的 HiFi BAM 以及可选的 PacBio `.pbi` 索引。不要用短读长数据替代，也不要
将 BAM 文件名当作平台、配对身份或甲基化信息的证据。

经审查的上游 `dev` 提交为 `24c84cb371b0339c1d65a4de9451671945e19772`。截至
2026-10-01，GitHub 上没有发布版本或标签，尽管内部清单中写的是 `1.0.0`。该辅助
工具默认将此提交固定为 `nf-core/pacsomatic` 的版本；它不会凭空编造一个发布标签。
这是一个经过源码审查的开发工作流，不是经过临床验证的检测方法。有关来源和科学
性检查，请参见 [references/pacsomatic_guide.md](references/pacsomatic_guide.md)。

## 工作流程

1. 获取不同的肿瘤和正常 BAM 路径、患者 ID、不同的样本 ID、输出目录，以及
   恰好一种参考模式：`--fasta` 或 `--genome`。ID 和 BAM/PBI/FASTA 路径不能
   包含空白字符。本地输入必须是非空的常规文件。远程 BAM/PBI/FASTA URI 会
   被直接传递，不进行下载或认证；请使用受管理的文件系统/云凭据，切勿将密钥
   或签名 URL 嵌入生成的文件中。
2. 根据采集元数据确认 PacBio HiFi 读组和样本身份；确认甲基化所需的 MM/ML
   修饰标签已被保留。为每个注释资源验证参考序列/contig 兼容性。
3. 使用 `--dry-run` 生成工件。这会执行辅助检查并写入文件，但**不会**调用
   流程、验证 BAM 内容、检查远程可用性、解析每个流程参数或验证生物学合理性。
   此处缺失的运行时工具只会产生警告。`--dry-run` 不能与 `--run`/`--submit`、
   克隆操作或环境创建组合使用。
4. 审查样本表、生成的参数 YAML、脚本、流程版本、profile，以及分支特定的
   资源/跳过选项。已存在的工件需要显式使用 `--overwrite`；输入文件永远不能
   作为工件目标。`config.yaml` 是一份操作者参考文档，不是自动加载的配置文件。
5. 对于执行阶段，使用 `--use-current-path` 或已有的 `--conda-env` 选择实际的
   运行时。在调用该辅助工具**之前**加载集群模块；`--module-load` 只会在生成
   的脚本中重复这些命令。没有捆绑任何 Conda YAML 文件；创建环境需要显式使用
   `--conda-env-file`。
6. 仅在需要实际执行时使用 `--run`。对于 HPC，要区分外部启动器调度器
   （`--executor`）和 Nextflow 的每任务 `process.executor`（由站点 profile 或
   `--nextflow-config` 配置）。驱动程序的 CPU/内存请求并不约束任务资源。
   请阅读 [references/config-and-output.md](references/config-and-output.md)。
7. 报告工件路径、版本、检查/警告信息、运行类型、提交 ID（如有），以及具体
   的下一步 QC 或故障排查步骤。调度器接受任务并不等于流程已完成。保持输出
   目录和 work/cache 状态稳定以便 `--resume`；脚本以输出目录作为其当前工作
   目录运行。

## 示例

从仓库根目录运行以下命令。路径和站点设置仅作**示例说明**；本地测试只使用
合成的占位数据，而不是人类基因组数据。

```bash
python skills/pacsomatic/scripts/run_pacsomatic.py \
  --tumor-bam /data/P001_T.bam --normal-bam /data/P001_N.bam \
  --patient-id P001 --tumor-sample-id P001_T --normal-sample-id P001_N \
  --outdir /results/P001 --fasta /refs/GRCh38.fa \
  --profile apptainer --use-current-path --dry-run
```

审查工件后，Slurm 启动可以使用相同的输入加上以下选项（将 `--dry-run` 替换为
`--run`）：

```text
--executor slurm --queue compute --project my_account
--cpus 2 --memory-gb 8 --walltime 48:00
--nextflow-config /configs/slurm.config --overwrite --run
```

这些资源是为驱动程序设置的，假设经审查的基础设施配置设置了
`process.executor = 'slurm'` 以及合适的任务队列/资源。该辅助工具会将 `48:00`
规范化为 Slurm 的 `48:00:00`（48 小时）。除非确实使用该机构的 LSF 基础设施，
否则不要添加 `sanger` profile。

自定义流程参数放在 `--params-file` 中；基础设施配置放在 `--nextflow-config`
（`-c`）中。该辅助工具明确的输入/输出目录/参考选项优先于 params-file 中的值。
`--extra-args` 会被分词并进行 shell 引用处理，但不能覆盖这些受管理的输入/配置
选项。请将外部参数/配置文件中的路径保持为绝对路径，因为启动器的工作目录就是
输出目录。

## 验证与参考资料

```bash
uv run skills-ref validate skills/pacsomatic
python tests/run_all.py --isolated pacsomatic
```

该标准库测试套件检查本地工件行为、路径保护、CLI 模式、运行时故障，以及模拟
的调度器提交。原生 Nextflow 检查使用一个微小的本地工作流；它们并不能证明
pacsomatic 完整的容器化科学流程在给定数据集或集群上能够成功运行。

- [操作者手册](references/agent-playbook.md)
- [配置、调度器和输出契约](references/config-and-output.md)
- [上游来源和科学性检查](references/pacsomatic_guide.md)
