---
name: pacsomatic
description: nf-core/pacsomatic匹配的肿瘤-正常工作流的操作员工具包。当用户需要验证运行输入、生成符合pacsomatic的样本表、准备可重现的Nextflow启动工件、在本地运行或提交到调度程序（LSF/Slurm/PBS/SGE）以及分类执行故障时使用此技能。在运行pacsomatic、准备启动命令/脚本、执行试运行检查或排除管道启动和调度程序提交错误的请求时触发。
license: MIT
metadata: {"version": "1.0", "skill-author": "Beifang Niu", "contributors": "Haidong, Wenchao", "upstream-pipeline": "https://github.com/nf-core/pacsomatic"}
---






# pacsomatic

## 概述

此技能为 nf-core/pacsomatic 提供可重现的执行工作流程，围绕一个处理验证、工件生成和可选执行的单一辅助入口点。

主要入口点：
- `scripts/run_pacsomatic.py`

辅助脚本：
- 验证必需的标识符、文件、参考模式和运行时先决条件
- 写入 pacsomatic 兼容的样本表（`patient,sample,status,bam,pbi`）
- 生成 params YAML 和启动脚本以供可重现的重新运行
- 支持干运行验证和运行/提交执行路径

将此技能用作 pacsomatic 操作的默认路径。除非用户明确要求手动命令构建，否则不要绕过它使用手动组装的 `nextflow run nf-core/pacsomatic` 命令。

## 何时使用此技能

在用户要求以下操作时调用此技能：
- 从 BAM 文件运行配对肿瘤-正常分析
- 生成或修复 pacsomatic 样本表和启动工件
- 在本地执行或提交到调度器（LSF/Slurm/PBS/SGE）
- 执行前进行干运行验证
- 排除启动失败或总结运行输出

不要将此技能用于：
- 运行级别合理性检查之外的深度生物学解释
- 除非明确要求，否则不编辑管道内部

典型触发短语：
- "为这个肿瘤-正常配对运行 nf-core/pacsomatic"
- "准备 pacsomatic 样本表和启动脚本"
- "先做干运行并告诉我缺少什么"
- "提交 pacsomatic 到 slurm/lsf 并返回作业 ID"
- "为什么 pacsomatic 提交失败"

## 路由和执行规则

1. 始终首先收集必需的运行输入。
2. 始终通过 `scripts/run_pacsomatic.py` 进行验证和工件生成。
3. 当用户仅要求检查/验证时，默认为 `--dry-run`。
4. 仅当用户要求执行/提交时使用 `--run`。
5. 对于调度器模式，包含执行器特定的资源参数并在可用时返回检测到的作业 ID。
6. 如果执行失败，报告第一个失败点和下一个分类目标（`.nextflow.log`、`pipeline_info`、失败任务日志）。

## 必需输入

必需：
- 肿瘤 BAM 路径
- 正常 BAM 路径
- 患者 ID
- 肿瘤样本 ID
- 正常样本 ID
- 输出目录
- 恰好一种参考模式：`--fasta` 或 `--genome`

可选：
- profile、资源、调度器账户/队列
- 管道版本（`-r`）
- params 文件、resume/report/dag 标志
- `--dry-run` 和/或 `--run`

## 工作流程

1. 验证身份和输入约束。
2. 验证必需的本地路径（BAM、可选 PBI、可选 FASTA）。
3. 解决运行时和依赖检查。
4. 构建样本表和生成的 params YAML。
5. 为选定的执行器生成启动脚本。
6. 如果是 `--dry-run` 且不是 `--run`，在生成工件后停止。
7. 如果是 `--run`，在本地执行或提交到调度器。
8. 返回命令/脚本路径、验证状态和作业 ID（如果检测到）。

## 代理响应契约

每次调用后的响应应包括：
- 使用的确切命令或生成的脚本路径
- 确认验证检查已运行
- 运行类型（`dry-run` vs `run`）
- 调度器作业 ID（如果可用）
- 验证/分类的一个具体下一步

## 快速开始

干运行：

```bash
python scripts/run_pacsomatic.py \
  --tumor-bam /path/to/tumor.bam \
  --normal-bam /path/to/normal.bam \
  --patient-id P001 \
  --tumor-sample-id P001_T \
  --normal-sample-id P001_N \
  --outdir /path/to/output \
  --genome GRCh38 \
  --profile singularity,sanger \
  --dry-run
```

调度器执行示例（Slurm）：

```bash
python scripts/run_pacsomatic.py \
  --tumor-bam /path/to/tumor.bam \
  --normal-bam /path/to/normal.bam \
  --patient-id P001 \
  --tumor-sample-id P001_T \
  --normal-sample-id P001_N \
  --outdir /path/to/output \
  --genome GRCh38 \
  --profile singularity,sanger \
  --executor slurm \
  --queue compute \
  --project my_account \
  --cpus 16 \
  --memory-gb 64 \
  --walltime 48:00 \
  --run
```

## 配置

可以自定义 Pacsomatic 的行为：

1. **环境变量**：
   - `PACSOMATIC_DEBUG`：启用调试模式
   - `PACSOMATIC_CONFIG_PATH`：指定配置文件路径

2. **配置文件**：
   - 默认配置：`~/.pacsomatic/config.yaml`
   - 项目配置：`.pacsomatic.yaml`

## 测试

测试您的 PACSomatic 配置：

```bash
# 验证配置
pacsomatic validate

# 模拟运行
pacsomatic dry-run

# 本地测试
pacsomatic test --local
```

## 参考资料

- [Pacsomatic 文档](https://pacsomatic.readthedocs.io/)
- [GitHub 仓库](https://github.com/snakemake-projects/pacsomatic)
- [Snakemake 文档](https://snakemake.readthedocs.io/)
