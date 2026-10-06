---
name: phylogenetics
description: 使用 MAFFT 多序列比对、带 ModelFinder 和分支支持度的 IQ-TREE 最大似然法以及 FastTree 近似推断，构建并分析系统发育树。使用 ETE3 进行树的汇总与可视化。适用于同源核苷酸或蛋白质序列、微生物基因树、蛋白质家族，以及需谨慎解读的定年系统发育树。
license: Unknown
compatibility: Requires MAFFT and IQ-TREE 3 or FastTree executables. Optional tree summaries use Python 3.12 and ete3 3.1.3; rendering also needs PyQt5. Optional trimming needs trimAl. Network access is required for installation, not local inference.
metadata:
  version: "1.5"
  skill-author: Kuan-lin Huang
  last-reviewed: "2026-10-01"
---

# 系统发育学

## 何时使用

对于同源基因座或蛋白质的比对、基因树、分支支持度以及可解读的树图，请使用此工作流程。多基因座分区、一致性因子（concordance factors）、祖先状态和定年内容见 [IQ-TREE 参考](references/iqtree_inference.md)。

基因树本身并不能确立物种树、传播方向或水平转移。仅凭采样日期并不能证明分子钟成立。

## 版本与安装

已于 2026-10-01 对照当前官方文档进行审阅。已执行的冒烟（smoke）工作流程在 Python 3.12 上使用了 MAFFT **7.526**、IQ-TREE **3.1.4**、FastTree **2.2.0** 和 ETE3 **3.1.3**。此辅助脚本有意继续使用 ETE3；ETE4 是另一套 API，并不是可直接替换的版本。ETE3 会导入 `cgi`，而该模块在 Python 3.13 中已被移除。原生可执行文件不是 Python 包。

示意性的安装命令；安装后请核实可执行文件的版本：

```bash
conda create -n phylo -c conda-forge -c bioconda mafft iqtree fasttree trimal
conda activate phylo
uv venv --python 3.12 .venv-phylo
uv pip install --python .venv-phylo/bin/python ete3==3.1.3 numpy six
# 可选的渲染后端；它可能需要可用的 Qt 平台插件。
uv pip install --python .venv-phylo/bin/python PyQt5
```

该辅助脚本默认使用 `iqtree3` 和 `FastTree`；对于现有的 IQ-TREE 2 安装，请使用 `--iqtree-bin iqtree2`；如果已安装的名称是 `fasttree`，请使用 `--fasttree-bin fasttree`。版本 2 的兼容性经过源代码核对，在此次更新中未经运行时测试。所有分析都在本地进行；本技能不调用任何 HTTP API 或远程推理端点。

## 工作流程

### 1. 确立生物学输入

- 选择具有适当分类单元覆盖度的同源序列；在假设单一历史能描述所有位点之前，先调查旁系同源基因（paralog）、污染和重组。
- 使用唯一的、不含空白字符的 FASTA ID，并另外保留一份样本元数据表。该辅助脚本会拒绝空记录/全缺失的记录以及 ID 中的 Newick 标点符号。
- 指定 `--type nt` 或 `--type aa`。该辅助脚本会向 IQ-TREE 发送 `-st DNA` 或 `-st AA`，并显式选择核苷酸/蛋白质的 FastTree 标志。
- 如果使用密码子模型，编码 DNA 需要密码子感知的比对。普通的 MAFFT 核苷酸比对不会自动保留阅读框。
- 保留原始序列、登录号版本、过滤条件、比对结果和确切的命令。检查比对长度、空位、组成和分类单元身份。

### 2. 比对与检查

这些 MAFFT 命令已在小型合成 FASTA 数据上运行过：

```bash
mafft --auto --thread 1 --inputorder sequences.fasta > aligned.fasta
# L-INS-i：可局部比对的同源序列，通常用于小型数据集。
mafft --localpair --maxiterate 1000 --thread 1 --inputorder sequences.fasta > linsi.fasta
# E-INS-i：具有大型内部空位的同源序列。
mafft --genafpair --maxiterate 1000 --thread 1 --inputorder sequences.fasta > einsi.fasta
# FFT-NS-i（两轮优化循环），然后是 FFT-NS-2（渐进式）。
mafft --retree 2 --maxiterate 2 --thread 1 --inputorder sequences.fasta > fftnsi.fasta
mafft --retree 2 --maxiterate 0 --thread 1 --inputorder sequences.fasta > fftns.fasta
```

`auto` 将选择委托给 MAFFT。仅凭序列数量并不是准确性的判据。单线程运行简化了可重复性；使用多线程的 MAFFT 迭代优化在不同运行之间可能产生不同的结果。

修剪（trimming）是可选的，必须以比对质量为依据，不能假设它会改善每一棵树。以下 trimAl 命令经过文档核对，仅作示意；本次审阅中没有安装 trimAl：

```bash
trimal -in aligned.fasta -out trimmed.fasta -automated1 -fasta
```

记录保留的列/分类单元，并比较对修剪的敏感性。失败的修剪必须终止修剪步骤；不要默默地将未修剪的输入以“trimmed”文件名复制出来。随附的辅助脚本不会自动修剪。

### 3. 推断树

请使用维护中的辅助脚本，而不是重新创建子进程封装。从技能目录运行，并确保可执行文件名称在 `PATH` 中：

```bash
python scripts/phylogenetic_analysis.py sequences.fasta --type nt --threads 1 \
  --bootstrap 1000 --seed 42 --output-dir results --no-visualization
# 使用经过审阅的比对（包括任何显式修剪），而不重新比对。
python scripts/phylogenetic_analysis.py aligned.fasta --aligned --type nt \
  --threads 1 --output-dir reviewed --no-visualization
# 蛋白质 FastTree 的替代方案；--threads 适用于 MAFFT/IQ-TREE，而不适用于 FastTree。
python scripts/phylogenetic_analysis.py proteins.fasta --type aa --fasttree \
  --threads 1 --output-dir fast_protein --no-visualization
```

标准的 IQ-TREE 命令使用 `-m MFP`（ModelFinder，包含 FreeRate 模型）、`-B 1000`（UFBoot）和 `--alrt 1000`。`-m TEST` 仍然受支持，但搜索的模型集合更窄。对于有科学依据的固定模型，请使用 `--model`。IQ-TREE 的检查点会被保留；`--redo` 会显式地重新开始并替换结果。当数据或模型假设改变时，请使用新的输出前缀。

FastTree 对 DNA 使用 `-nt -gtr -gamma`，对蛋白质使用 `-lg -gamma`。其搜索在 Gamma20 重新缩放之前使用 CAT 近似；它不是完整的 Gamma 模型 ML 搜索。JTT 是 FastTree 的蛋白质默认模型（没有 `-jtt` 标志）；核苷酸的 JC 模型通过不带 `-gtr` 的 `-nt` 来选择。FastTree 默认使用 **0–1** 范围内的 **SH-like 局部支持度**，而不是 UFBoot 百分比。请基于工作负载进行基准测试，而不是使用通用的分类单元数阈值，来决定使用哪种推断工具。

### 4. 解读支持度、定根和输出

请阅读 `.iqtree` 和 `.log`，而不仅仅是图像。在默认的组合检验中，IQ-TREE 会写出以斜杠分隔的 SH-aLRT/UFBoot 标签；请在报告中核实它们的顺序。UFBoot >=95 和 SH-aLRT >=80 是常用的筛选阈值，不是正确性的证明，也不是后验概率。不要将标准自展（bootstrap）的 70% 规则应用于 UFBoot。模型设定错误、比对错误和采样都可能产生支持度很高的错误分支；在评估模型违背和 UFBoot 高估时，可考虑使用 `-bnni`。

可逆的替代模型无法推断进化的根。除非显式做出 `--outgroup` 或 `--midpoint` 的显示选择，否则该辅助脚本会保留所提供的树的方向。请从生物学角度选择外群；中点定根假设路径长度具有足够的类时钟性，并且只是一种启发式方法。`--outgroup` 向 IQ-TREE 传递一个分类单元并验证其存在。显示用的重新定根会将支持度标签保留在其对应的分裂上。这两种显示选项都不会创建定年的系统发育树，也不会覆盖原始推断出的树。

主要输出是 `<prefix>.treefile`（IQ-TREE）或 `<prefix>.tree`（FastTree）、比对结果，以及 IQ-TREE 的 `.iqtree`、`.log`、`.ckp.gz`，外加可选的支持度文件。`.model.gz` 缓存模型选择的工作结果；它不是估计的模型参数报告。请将这些产物放在一起保存。

### 5. 汇总与可视化

ETE 必须使用 `format=1` 将组合的 IQ-TREE 标签读取为内部节点**名称**；其默认的数值支持度解析器无法解析 `95.2/99`。该辅助脚本渲染原始的文本标签，而不是 ETE 默认的支持度值。分支统计使用所有原始的非根边（包括零长度边），且不重新定根。

```python
# 在 ETE3 环境中从技能目录运行。
import sys
sys.path.insert(0, "scripts")
from phylogenetic_analysis import load_tree, tree_summary

tree = load_tree("results/sequences.treefile")
print(tree.get_leaf_names())
print(tree_summary("results/sequences.treefile"))
```

若要请求渲染，请省略 `--no-visualization`。ETE3 需要 PyQt5；在无头主机上必须有合适的 Qt 平台插件可用。缺少渲染支持时，推断出的树保持完整，并且会明确报告这一点。本次审阅中没有运行 Qt 渲染。FigTree 或 iTOL 也可以显示 Newick；请核实查看器保留了支持度标签和分支长度标尺。

## 官方参考

- [MAFFT 手册](https://mafft.cbrc.jp/alignment/software/manual/manual.html)和[多线程](https://mafft.cbrc.jp/alignment/software/multithreading.html)
- [IQ-TREE 快速入门](https://iqtree.github.io/doc/Quickstart)、[当前发布版本](https://github.com/iqtree/iqtree3/releases)、[模型假设](https://iqtree.github.io/doc/Assessing-Phylogenetic-Assumptions)
- [FastTree 手册](https://morgannprice.github.io/fasttree/)
- [ETE3 树的解析](https://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html)和[绘图](https://etetoolkit.org/docs/latest/tutorial/tutorial_drawing.html)
- [trimAl 手册](https://vicfero.github.io/trimal/)
