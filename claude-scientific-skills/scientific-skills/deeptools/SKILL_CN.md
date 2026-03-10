---
name: deeptools
description: NGS 分析工具包。BAM 到 bigWig 转换、QC（相关性、PCA、指纹）、热图/轮廓（TSS、峰），用于 ChIP-seq、RNA-seq、ATAC-seq 可视化。
license: BSD license
metadata:
    skill-author: K-Dense Inc.
---

# deepTools：NGS 数据分析工具包

## 概述

deepTools 是一套全面的 Python 命令行工具，用于处理和分析高通量测序数据。使用 deepTools 执行质量控制、归一化数据、比较样本，并为 ChIP-seq、RNA-seq、ATAC-seq、MNase-seq 和其他 NGS 实验生成出版质量的可视化。

**核心能力：**
- 将 BAM 比对转换为归一化的覆盖轨道（bigWig/bedGraph）
- 质量控制评估（指纹、相关性、覆盖度）
- 样本比较和相关性分析
- 在基因组特征周围生成热图和轮廓图
- 富集分析和峰区域可视化

## 何时使用此技能

此技能应在以下情况下使用：

- **文件转换**："将 BAM 转换为 bigWig"、"生成覆盖轨道"、"归一化 ChIP-seq 数据"
- **质量控制**："检查 ChIP 质量"、"比较重复"、"评估测序深度"、"QC 分析"
- **可视化**："在 TSS 周围创建热图"、"绘制 ChIP 信号"、"可视化富集"、"生成轮廓图"
- **样本比较**："比较处理与对照"、"关联样本"、"PCA 分析"
- **分析工作流**："分析 ChIP-seq 数据"、"RNA-seq 覆盖度"、"ATAC-seq 分析"、"完整工作流"
- **处理特定文件类型**：基因组学背景下的 BAM 文件、bigWig 文件、BED 区域文件

## 快速入门

对于 deepTools 的新用户，从文件验证和常见工作流开始：

### 1. 验证输入文件

在运行任何分析之前，使用验证脚本验证 BAM、bigWig 和 BED 文件：

```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam --bed regions.bed
```

这将检查文件存在性、BAM 索引和格式正确性。

### 2. 生成工作流模板

对于标准分析，使用工作流生成器创建自定义脚本：

```bash
# 列出可用工作流
python scripts/workflow_generator.py --list

# 生成 ChIP-seq QC 工作流
python scripts/workflow_generator.py chipseq_qc -o qc_workflow.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398

# 使其可执行并运行
chmod +x qc_workflow.sh
./qc_workflow.sh
```

### 3. 最常见操作

有关常用命令和参数，请参阅 `assets/quick_reference.md`。

## 安装

```bash
uv pip install deeptools
```

## 核心工作流

deepTools 工作流通常遵循此模式：**QC → 归一化 → 比较/可视化**

### ChIP-seq 质量控制工作流

当用户请求 ChIP-seq QC 或质量评估时：

1. **生成工作流脚本**，使用 `scripts/workflow_generator.py chipseq_qc`
2. **关键 QC 步骤**：
   - 样本相关性（multiBamSummary + plotCorrelation）
   - PCA 分析（plotPCA）
   - 覆盖度评估（plotCoverage）
   - 片段大小验证（bamPEFragmentSize）
   - ChIP 富集强度（plotFingerprint）

**结果解读：**
- **相关性**：重复应聚集在一起，具有高相关性（>0.9）
- **指纹**：强 ChIP 显示急剧上升；平坦的对角线表示富集不良
- **覆盖度**：评估测序深度是否足以进行分析

完整工作流详情在 `references/workflows.md` → "ChIP-seq Quality Control Workflow"

### ChIP-seq 完整分析工作流

用于从 BAM 到可视化的完整 ChIP-seq 分析：

1. **生成覆盖轨道**，使用归一化（bamCoverage）
2. **创建比较轨道**（bamCompare 用于 log2 比率）
3. **在特征周围计算信号矩阵**（computeMatrix）
4. **生成可视化**（plotHeatmap、plotProfile）
5. **峰处富集分析**（plotEnrichment）

使用 `scripts/workflow_generator.py chipseq_analysis` 生成模板。

`references/workflows.md` → "ChIP-seq Analysis Workflow" 中的完整命令序列

### RNA-seq 覆盖度工作流

用于链特异性 RNA-seq 覆盖度轨道：

使用带有 `--filterRNAstrand` 的 bamCoverage 分离前向和反向链。

**重要**：对于 RNA-seq 永远不要使用 `--extendReads`（会跨越剪接位点）。

使用归一化：CPM 用于固定箱，RPKM 用于基因级分析。

可用模板：`scripts/workflow_generator.py rnaseq_coverage`

`references/workflows.md` → "RNA-seq Coverage Workflow" 中的详细信息

### ATAC-seq 分析工作流

ATAC-seq 需要 Tn5 偏移校正：

1. **使用 alignmentSieve 和 `--ATACshift` 移位读取**
2. **使用 bamCoverage 生成覆盖度**
3. **分析片段大小**（预期核小体梯形模式）
4. **在峰处可视化**（如果可用）

模板：`scripts/workflow_generator.py atacseq`

`references/workflows.md` → "ATAC-seq Workflow" 中的完整工作流

## 工具类别和常见任务

### BAM/bigWig 处理

**将 BAM 转换为归一化覆盖度：**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC --effectiveGenomeSize 2913022398 \
    --binSize 10 --numberOfProcessors 8
```

**比较两个样本（log2 比率）：**
```bash
bamCompare -b1 treatment.bam -b2 control.bam -o ratio.bw \
    --operation log2 --scaleFactorsMethod readCount
```

**关键工具**：bamCoverage、bamCompare、multiBamSummary、multiBigwigSummary、correctGCBias、alignmentSieve

完整参考：`references/tools_reference.md` → "BAM and bigWig File Processing Tools"

### 质量控制

**检查 ChIP 富集：**
```bash
plotFingerprint -b input.bam chip.bam -o fingerprint.png \
    --extendReads 200 --ignoreDuplicates
```

**样本相关性：**
```bash
multiBamSummary bins --bamfiles *.bam -o counts.npz
plotCorrelation -in counts.npz --corMethod pearson \
    --whatToShow heatmap -o correlation.png
```

**关键工具**：plotFingerprint、plotCoverage、plotCorrelation、plotPCA、bamPEFragmentSize

完整参考：`references/tools_reference.md` → "Quality Control Tools"

### 可视化

**在 TSS 周围创建热图：**
```bash
# 计算矩阵
computeMatrix reference-point -S signal.bw -R genes.bed \
    -b 3000 -a 3000 --referencePoint TSS -o matrix.gz

# 生成热图
plotHeatmap -m matrix.gz -o heatmap.png \
    --colorMap RdBu --kmeans 3
```

**创建轮廓图：**
```bash
plotProfile -m matrix.gz -o profile.png \
    --plotType lines --colors blue red
```

**关键工具**：computeMatrix、plotHeatmap、plotProfile、plotEnrichment

完整参考：`references/tools_reference.md` → "Visualization Tools"

## 归一化方法

选择正确的归一化对于有效比较至关重要。请参阅 `references/normalization_methods.md` 获取全面指导。

**快速选择指南：**

- **ChIP-seq 覆盖度**：使用 RPGC 或 CPM
- **ChIP-seq 比较**：使用带有 log2 和 readCount 的 bamCompare
- **RNA-seq 箱**：使用 CPM
- **RNA-seq 基因**：使用 RPKM（考虑基因长度）
- **ATAC-seq**：使用 RPGC 或 CPM

**归一化方法：**
- **RPGC**：1× 基因组覆盖度（需要 --effectiveGenomeSize）
- **CPM**：每百万映射读取的计数
- **RPKM**：每千碱基每百万读取（考虑区域长度）
- **BPM**：每百万箱
- **None**：原始计数（不推荐用于比较）

完整说明：`references/normalization_methods.md`

## 有效基因组大小

RPGC 归一化需要有效基因组大小。常见值：

| 生物 | 组装 | 大小 | 用法 |
|----------|----------|------|-------|
| 人类 | GRCh38/hg38 | 2,913,022,398 | `--effectiveGenomeSize 2913022398` |
| 小鼠 | GRCm38/mm10 | 2,652,783,500 | `--effectiveGenomeSize 2652783500` |
| 斑马鱼 | GRCz11 | 1,368,780,147 | `--effectiveGenomeSize 1368780147` |
| *果蝇* | dm6 | 142,573,017 | `--effectiveGenomeSize 142573017` |
| *线虫* | ce10/ce11 | 100,286,401 | `--effectiveGenomeSize 100286401` |

包含读取长度特定值的完整表格：`references/effective_genome_sizes.md`

## 工具间的常见参数

许多 deepTools 命令共享这些选项：

**性能：**
- `--numberOfProcessors, -p`：启用并行处理（始终使用可用核心）
- `--region`：处理特定区域以进行测试（例如，`chr1:1-1000000`）

**读取过滤：**
- `--ignoreDuplicates`：移除 PCR 重复（推荐用于大多数分析）
- `--minMappingQuality`：按比对质量过滤（例如，`--minMappingQuality 10`）
- `--minFragmentLength` / `--maxFragmentLength`：片段长度边界
- `--samFlagInclude` / `--samFlagExclude`：SAM 标志过滤

**读取处理：**
- `--extendReads`：延伸到片段长度（ChIP-seq：是，RNA-seq：否）
- `--centerReads`：在片段中点居中以获得更清晰的信号

## 最佳实践

### 文件验证
**始终首先验证文件**，使用 `scripts/validate_files.py` 检查：
- 文件存在性和可读性
- BAM 索引存在（.bai 文件）
- BED 格式正确性
- 文件大小合理

### 分析策略

1. **从 QC 开始**：在进行详细分析之前，运行相关性、覆盖度和指纹分析
2. **在小区域上测试**：使用 `--region chr1:1-10000000` 进行参数测试
3. **记录命令**：保存完整命令行以确保可重复性
4. **使用一致的归一化**：在比较中对所有样本应用相同的方法
5. **验证基因组组装**：确保 BAM 和 BED 文件使用匹配的基因组构建

### ChIP-seq 特定

- **始终延伸读取**用于 ChIP-seq：`--extendReads 200`
- **移除重复**：在大多数情况下使用 `--ignoreDuplicates`
- **首先检查富集**：在进行详细分析之前运行 plotFingerprint
- **GC 校正**：仅在检测到显著偏倚时应用；在 GC 校正后永远不要使用 `--ignoreDuplicates`

### RNA-seq 特定

- **永远不要延伸读取**用于 RNA-seq（会跨越剪接位点）
- **链特异性**：对于链特异性库使用 `--filterRNAstrand forward/reverse`
- **归一化**：箱使用 CPM，基因使用 RPKM

### ATAC-seq 特定

- **应用 Tn5 校正**：使用带有 `--ATACshift` 的 alignmentSieve
- **片段过滤**：设置适当的最小/最大片段长度
- **检查核小体模式**：片段大小图应显示梯形模式

### 性能优化

1. **使用多个处理器**：`--numberOfProcessors 8`（或可用核心）
2. **增加箱大小**以加快处理速度并减小文件大小
3. **单独处理染色体**以用于内存受限的系统
4. **使用 alignmentSieve 预过滤 BAM 文件**以创建可重用的过滤文件
5. **使用 bigWig 而不是 bedGraph**：压缩且处理更快

## 故障排除

### 常见问题

**缺少 BAM 索引：**
```bash
samtools index input.bam
```

**内存不足：**
使用 `--region` 单独处理染色体：
```bash
bamCoverage --bam input.bam -o chr1.bw --region chr1
```

**处理缓慢：**
增加 `--numberOfProcessors` 和/或增加 `--binSize`

**bigWig 文件太大：**
增加箱大小：`--binSize 50` 或更大

### 验证错误

运行验证脚本以识别问题：
```bash
python scripts/validate_files.py --bam *.bam --bed regions.bed
```

脚本输出中解释了常见错误和解决方案。

## 参考文档

此技能包含全面的参考文档：

### references/tools_reference.md
所有 deepTools 命令的完整文档，按类别组织：
- BAM 和 bigWig 处理工具（9 个工具）
- 质量控制工具（6 个工具）
- 可视化工具（3 个工具）
- 其他工具（2 个工具）

每个工具包括：
- 用途和概述
- 带有解释的关键参数
- 使用示例
- 重要说明和最佳实践

**使用此参考**：当用户询问特定工具、参数或详细用法时。

### references/workflows.md
常见分析的完整工作流示例：
- ChIP-seq 质量控制工作流
- ChIP-seq 完整分析工作流
- RNA-seq 覆盖度工作流
- ATAC-seq 分析工作流
- 多样本比较工作流
- 峰区域分析工作流
- 故障排除和性能技巧

**使用此参考**：当用户需要完整的分析管道或工作流示例时。

### references/normalization_methods.md
归一化方法的综合指南：
- 每种方法的详细说明（RPGC、CPM、RPKM、BPM 等）
- 何时使用每种方法
- 公式和解读
- 按实验类型的选择指南
- 常见陷阱和解决方案
- 快速参考表

**使用此参考**：当用户询问归一化、比较样本或使用哪种方法时。

### references/effective_genome_sizes.md
有效基因组大小值和用法：
- 常见生物值（人类、小鼠、果蝇、线虫、斑马鱼）
- 读取长度特定值
- 计算方法
- 何时以及在命令中如何使用
- 自定义基因组计算说明

**使用此参考**：当用户需要 RPGC 归一化或 GC 偏倚校正的基因组大小时。

## 辅助脚本

### scripts/validate_files.py

验证 deepTools 分析的 BAM、bigWig 和 BED 文件。检查文件存在性、索引和格式。

**用法：**
```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam \
    --bed peaks.bed --bigwig signal.bw
```

**何时使用**：开始任何分析之前，或在故障排除错误时。

### scripts/workflow_generator.py

为常见 deepTools 工作流生成可自定义的 bash 脚本模板。

**可用工作流：**
- `chipseq_qc`：ChIP-seq 质量控制
- `chipseq_analysis`：完整 ChIP-seq 分析
- `rnaseq_coverage`：链特异性 RNA-seq 覆盖度
- `atacseq`：带有 Tn5 校正的 ATAC-seq

**用法：**
```bash
# 列出工作流
python scripts/workflow_generator.py --list

# 生成工作流
python scripts/workflow_generator.py chipseq_qc -o qc.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398 --threads 8

# 运行生成的工作流
chmod +x qc.sh
./qc.sh
```

**何时使用**：当用户请求标准工作流或需要模板脚本进行自定义时。

## 资产

### assets/quick_reference.md

包含最常用命令、有效基因组大小和典型工作流模式的快速参考卡。

**何时使用**：当用户需要快速命令示例而无需详细文档时。

## 处理用户请求

### 对于新用户

1. 从安装验证开始
2. 使用 `scripts/validate_files.py` 验证输入文件
3. 根据实验类型推荐适当的工作流
4. 使用 `scripts/workflow_generator.py` 生成工作流模板
5. 指导自定义和执行

### 对于有经验的用户

1. 为请求的操作提供特定的工具命令
2. 参考 `references/tools_reference.md` 中的适当部分
3. 建议优化和最佳实践
4. 为问题提供故障排除

### 对于特定任务

**"将 BAM 转换为 bigWig"：**
- 使用带有适当归一化的 bamCoverage
- 根据用例推荐 RPGC 或 CPM
- 为生物提供有效基因组大小
- 建议相关参数（extendReads、ignoreDuplicates、binSize）

**"检查 ChIP 质量"：**
- 运行完整的 QC 工作流或专门使用 plotFingerprint
- 解释结果解读
- 根据结果建议后续操作

**"创建热图"：**
- 指导两步过程：computeMatrix → plotHeatmap
- 帮助选择适当的矩阵模式（reference-point 与 scale-regions）
- 建议可视化参数和聚类选项

**"比较样本"：**
- 推荐用于两个样本比较的 bamCompare
- 建议用于多样本的 multiBamSummary + plotCorrelation
- 指导归一化方法选择

### 参考文档

当用户需要详细信息时：
- **工具详细信息**：指向 `references/tools_reference.md` 中的特定部分
- **工作流**：使用 `references/workflows.md` 进行完整分析管道
- **归一化**：查阅 `references/normalization_methods.md` 进行方法选择
- **基因组大小**：参考 `references/effective_genome_sizes.md`

使用 grep 模式搜索参考：
```bash
# 查找工具文档
grep -A 20 "^### toolname" references/tools_reference.md

# 查找工作流
grep -A 50 "^## Workflow Name" references/workflows.md

# 查找归一化方法
grep -A 15 "^### Method Name" references/normalization_methods.md
```

## 示例交互

**用户："我需要分析我的 ChIP-seq 数据"**

响应方法：
1. 询问可用文件（BAM 文件、峰、基因）
2. 使用验证脚本验证文件
3. 生成 chipseq_analysis 工作流模板
4. 为其特定文件和生物进行自定义
5. 在脚本运行时解释每个步骤

**用户："我应该使用哪种归一化？"**

响应方法：
1. 询问实验类型（ChIP-seq、RNA-seq 等）
2. 询问比较目标（样本内还是样本间）
3. 查阅 `references/normalization_methods.md` 选择指南
4. 推荐适当的方法并给出理由
5. 提供带有参数的命令示例

**用户："在 TSS 周围创建热图"**

响应方法：
1. 验证 bigWig 和基因 BED 文件可用
2. 使用 reference-point 模式在 TSS 处使用 computeMatrix
3. 使用适当的可视化参数生成 plotHeatmap
4. 如果数据集较大，建议聚类
5. 提供轮廓图作为补充

## 关键提醒

- **首先验证文件**：分析前始终验证输入文件
- **归一化很重要**：为比较类型选择适当的方法
- **仔细延伸读取**：ChIP-seq 为是，RNA-seq 为否
- **使用所有核心**：将 `--numberOfProcessors` 设置为可用核心
- **在区域上测试**：使用 `--region` 进行参数测试
- **首先检查 QC**：在进行详细分析之前运行质量控制
- **记录所有内容**：保存命令以确保可重复性
- **参考文档**：使用全面参考以获取详细指导
