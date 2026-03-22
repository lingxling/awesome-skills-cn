---
name: phylogenetics
description: 使用MAFFT（多序列比对）、IQ-TREE 2（最大似然法）和FastTree（快速NJ/ML）构建和分析系统发育树。使用ETE3或FigTree进行可视化。适用于进化分析、微生物基因组学、病毒系统动力学、蛋白质家族分析和分子钟研究。
license: Unknown
metadata:
    skill-author: Kuan-lin Huang
---

# 系统发育学

## 概述

系统发育分析通过推断生物序列（基因、蛋白质、基因组）的进化分支模式来重建其进化历史。此技能涵盖标准流程：

1. **MAFFT** — 多序列比对
2. **IQ-TREE 2** — 带模型选择的最大似然树推断
3. **FastTree** — 快速近似最大似然法（适用于大型数据集）
4. **ETE3** — 用于树操作和可视化的Python库

**安装：**
```bash
# Conda（推荐用于命令行工具）
conda install -c bioconda mafft iqtree fasttree
pip install ete3
```

## 何时使用此技能

当以下情况时使用系统发育学：

- **进化关系**：哪种生物/基因与我的序列最相关？
- **病毒系统动力学**：追踪疫情传播并估计传播日期
- **蛋白质家族分析**：推断基因家族内的进化关系
- **水平基因转移检测**：识别具有不一致物种/基因树的基因
- **祖先序列重建**：推断祖先蛋白质序列
- **分子钟分析**：使用时间采样估计分化日期
- **GWAS辅助**：将变异置于进化背景中（例如SARS-CoV-2变异）
- **微生物学**：从16S rRNA或核心基因组系统发育构建物种系统发育

## 标准工作流程

### 1. 使用MAFFT进行多序列比对

```python
import subprocess
import os

def run_mafft(input_fasta: str, output_fasta: str, method: str = "auto",
               n_threads: int = 4) -> str:
    """
    使用MAFFT比对序列。

    参数：
        input_fasta: 未比对的FASTA文件路径
        output_fasta: 比对输出路径
        method: 'auto'（自动选择）, 'einsi'（准确）, 'linsi'（准确，慢）,
                'fftnsi'（中等）, 'fftns'（快速）, 'retree2'（快速）
        n_threads: CPU线程数

    返回：
        比对后的FASTA文件路径
    """
    methods = {
        "auto": ["mafft", "--auto"],
        "einsi": ["mafft", "--genafpair", "--maxiterate", "1000"],
        "linsi": ["mafft", "--localpair", "--maxiterate", "1000"],
        "fftnsi": ["mafft", "--fftnsi"],
        "fftns": ["mafft", "--fftns"],
        "retree2": ["mafft", "--retree", "2"],
    }

    cmd = methods.get(method, methods["auto"])
    cmd += ["--thread", str(n_threads), "--inputorder", input_fasta]

    with open(output_fasta, 'w') as out:
        result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"MAFFT失败:\n{result.stderr}")

    # 计算比对的序列数
    with open(output_fasta) as f:
        n_seqs = sum(1 for line in f if line.startswith('>'))
    print(f"MAFFT: 比对了 {n_seqs} 个序列 → {output_fasta}")

    return output_fasta

# MAFFT方法选择指南：
# 少数序列（<200），准确：linsi 或 einsi
# 许多序列（<1000），中等：fftnsi
# 大型数据集（>1000）：fftns 或 auto
# 超快（>10000）：mafft --retree 1
```

### 2. 修剪比对（可选但推荐）

```python
def trim_alignment_trimal(aligned_fasta: str, output_fasta: str,
                            method: str = "automated1") -> str:
    """
    使用TrimAl修剪比对质量差的列。

    方法：
    - 'automated1': 自动启发式（推荐）
    - 'gappyout': 移除有缺口的列
    - 'strict': 严格的缺口阈值
    """
    cmd = ["trimal", f"-{method}", "-in", aligned_fasta, "-out", output_fasta, "-fasta"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"TrimAl警告: {result.stderr}")
        # 回退到使用未修剪的比对
        import shutil
        shutil.copy(aligned_fasta, output_fasta)
    return output_fasta
```

### 3. IQ-TREE 2 — 最大似然树

```python
def run_iqtree(aligned_fasta: str, output_prefix: str,
                model: str = "TEST", bootstrap: int = 1000,
                n_threads: int = 4, extra_args: list = None) -> dict:
    """
    使用IQ-TREE 2构建最大似然树。

    参数：
        aligned_fasta: 比对后的FASTA文件
        output_prefix: 输出文件前缀
        model: 'TEST'用于自动模型选择，或指定（例如，DNA用'GTR+G'，
               蛋白质用'LG+G4'，蛋白质用'JTT+G'）
        bootstrap: 超快引导复制次数（推荐1000）
        n_threads: 线程数（'AUTO'自动检测）
        extra_args: 额外的IQ-TREE参数

    返回：
        包含输出文件路径的字典
    """
    cmd = [
        "iqtree2",
        "-s", aligned_fasta,
        "--prefix", output_prefix,
        "-m", model,
        "-B", str(bootstrap),   # 超快引导
        "-T", str(n_threads),
        "--redo"                # 覆盖现有结果
    ]

    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"IQ-TREE失败:\n{result.stderr}")

    # 打印模型选择结果
    log_file = f"{output_prefix}.log"
    if os.path.exists(log_file):
        with open(log_file) as f:
            for line in f:
                if "Best-fit model" in line:
                    print(f"IQ-TREE: {line.strip()}")

    output_files = {
        "tree": f"{output_prefix}.treefile",
        "log": f"{output_prefix}.log",
        "iqtree": f"{output_prefix}.iqtree",  # 完整报告
        "model": f"{output_prefix}.model.gz",
    }

    print(f"IQ-TREE: 树保存到 {output_files['tree']}")
    return output_files

# IQ-TREE模型选择指南：
# DNA:     TEST → GTR+G, HKY+G, TrN+G
# Protein: TEST → LG+G4, WAG+G, JTT+G, Q.pfam+G
# Codon:   TEST → MG+F3X4

# 对于时间（分子钟）分析，添加：
# extra_args = ["--date", "dates.txt", "--clock-test", "--date-CI", "95"]
```

### 4. FastTree — 快速近似ML

对于大型数据集（>1000个序列），IQ-TREE太慢时使用：

```python
def run_fasttree(aligned_fasta: str, output_tree: str,
                  sequence_type: str = "nt", model: str = "gtr",
                  n_threads: int = 4) -> str:
    """
    使用FastTree构建快速近似ML树。

    参数：
        sequence_type: 'nt'表示核苷酸或'aa'表示氨基酸
        model: 对于nt: 'gtr'（推荐）或'jc'；对于aa: 'lg', 'wag', 'jtt'
    """
    if sequence_type == "nt":
        cmd = ["FastTree", "-nt", "-gtr"]
    else:
        cmd = ["FastTree", f"-{model}"]

    cmd += [aligned_fasta]

    with open(output_tree, 'w') as out:
        result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FastTree失败:\n{result.stderr}")

    print(f"FastTree: 树保存到 {output_tree}")
    return output_tree
```

### 5. 使用ETE3进行树分析和可视化

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace, PhyloTree
import matplotlib.pyplot as plt

def load_tree(tree_file: str) -> Tree:
    """加载Newick树文件。"""
    t = Tree(tree_file)
    print(f"树: {len(t)} 个叶节点, {len(list(t.traverse()))} 个节点")
    return t

def basic_tree_stats(t: Tree) -> dict:
    """计算基本树统计信息。"""
    leaves = t.get_leaves()
    distances = [t.get_distance(l1, l2) for l1 in leaves[:min(50, len(leaves))]
                 for l2 in leaves[:min(50, len(leaves))] if l1 != l2]

    stats = {
        "n_leaves": len(leaves),
        "n_internal_nodes": len(t) - len(leaves),
        "total_branch_length": sum(n.dist for n in t.traverse()),
        "max_leaf_distance": max(distances) if distances else 0,
        "mean_leaf_distance": sum(distances)/len(distances) if distances else 0,
    }
    return stats

def find_mrca(t: Tree, leaf_names: list) -> Tree:
    """找到一组叶节点的最近共同祖先。"""
    return t.get_common_ancestor(*leaf_names)

def visualize_tree(t: Tree, output_file: str = "tree.png",
                    show_branch_support: bool = True,
                    color_groups: dict = None,
                    width: int = 800) -> None:
    """
    将系统发育树渲染为图像。

    参数：
        t: ETE3 Tree对象
        color_groups: 将叶节点名称映射到颜色的字典（用于给分类群着色）
        show_branch_support: 显示引导值
    """
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.show_branch_support = show_branch_support
    ts.mode = "r"  # 'r' = 矩形, 'c' = 圆形

    if color_groups:
        for node in t.traverse():
            if node.is_leaf() and node.name in color_groups:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = color_groups[node.name]
                nstyle["size"] = 8
                node.set_style(nstyle)

    t.render(output_file, tree_style=ts, w=width, units="px")
    print(f"树保存到: {output_file}")

def midpoint_root(t: Tree) -> Tree:
    """在中点处根化树（当外群未知时使用）。"""
    t.set_outgroup(t.get_midpoint_outgroup())
    return t

def prune_tree(t: Tree, keep_leaves: list) -> Tree:
    """修剪树以仅保留指定的叶节点。"""
    t.prune(keep_leaves, preserve_branch_length=True)
    return t
```

### 6. 完整分析脚本

```python
import subprocess, os
from ete3 import Tree

def full_phylogenetic_analysis(
    input_fasta: str,
    output_dir: str = "phylo_results",
    sequence_type: str = "nt",
    n_threads: int = 4,
    bootstrap: int = 1000,
    use_fasttree: bool = False
) -> dict:
    """
    完整的系统发育流程：比对 → 修剪 → 树 → 可视化。

    参数：
        input_fasta: 未比对的FASTA
        sequence_type: 'nt'（核苷酸）或'aa'（氨基酸/蛋白质）
        use_fasttree: 使用FastTree而不是IQ-TREE（对大型数据集更快）
    """
    os.makedirs(output_dir, exist_ok=True)
    prefix = os.path.join(output_dir, "phylo")

    print("=" * 50)
    print("步骤 1: 多序列比对 (MAFFT)")
    aligned = run_mafft(input_fasta, f"{prefix}_aligned.fasta",
                         method="auto", n_threads=n_threads)

    print("\n步骤 2: 树推断")
    if use_fasttree:
        tree_file = run_fasttree(
            aligned, f"{prefix}.tree",
            sequence_type=sequence_type,
            model="gtr" if sequence_type == "nt" else "lg"
        )
    else:
        model = "TEST" if sequence_type == "nt" else "TEST"
        iqtree_files = run_iqtree(
            aligned, prefix,
            model=model,
            bootstrap=bootstrap,
            n_threads=n_threads
        )
        tree_file = iqtree_files["tree"]

    print("\n步骤 3: 树分析")
    t = Tree(tree_file)
    t = midpoint_root(t)

    stats = basic_tree_stats(t)
    print(f"树统计信息: {stats}")

    print("\n步骤 4: 可视化")
    visualize_tree(t, f"{prefix}_tree.png", show_branch_support=True)

    # 保存根化树
    rooted_tree_file = f"{prefix}_rooted.nwk"
    t.write(format=1, outfile=rooted_tree_file)

    results = {
        "aligned_fasta": aligned,
        "tree_file": tree_file,
        "rooted_tree": rooted_tree_file,
        "visualization": f"{prefix}_tree.png",
        "stats": stats
    }

    print("\n" + "=" * 50)
    print("系统发育分析完成！")
    print(f"结果在: {output_dir}/")
    return results
```

## IQ-TREE模型指南

### DNA模型

| 模型 | 描述 | 用例 |
|-------|-------------|---------|
| `GTR+G4` | 一般时间可逆 + Gamma | 最灵活的DNA模型 |
| `HKY+G4` | Hasegawa-Kishino-Yano + Gamma | 双速率模型（常见） |
| `TrN+G4` | Tamura-Nei | 不等转换 |
| `JC` | Jukes-Cantor | 最简单；所有速率相等 |

### 蛋白质模型

| 模型 | 描述 | 用例 |
|-------|-------------|---------|
| `LG+G4` | Le-Gascuel + Gamma | 最佳平均蛋白质模型 |
| `WAG+G4` | Whelan-Goldman | 广泛使用 |
| `JTT+G4` | Jones-Taylor-Thornton | 经典模型 |
| `Q.pfam+G4` | pfam训练 | 用于Pfam样蛋白质家族 |
| `Q.bird+G4` | 鸟类特定 | 脊椎动物蛋白质 |

**提示：** 使用`-m TEST`让IQ-TREE自动选择最佳模型。

## 最佳实践

- **比对质量优先**：差的比对 → 不可靠的树；手动检查比对
- **小序列（<200）使用`linsi`，大比对使用`fftns`或`auto`**
- **模型选择**：除非有特定原因，否则始终对IQ-TREE使用`-m TEST`
- **引导**：使用≥1000次超快引导（`-B 1000`）获得分支支持
- **根化树**：无根树可能产生误导；使用外群或中点根化
- **>5000序列使用FastTree**：IQ-TREE变得缓慢；FastTree快10–100倍
- **修剪长比对**：TrimAl移除不可靠的列；提高树的准确性
- **在构建树之前检查病毒/细菌序列的重组**（`RDP4`、`GARD`）

## 其他资源

- **MAFFT**：https://mafft.cbrc.jp/alignment/software/
- **IQ-TREE 2**：http://www.iqtree.org/ | 教程：https://www.iqtree.org/workshop/molevol2022
- **FastTree**：http://www.microbesonline.org/fasttree/
- **ETE3**：http://etetoolkit.org/
- **FigTree**（GUI可视化）：https://tree.bio.ed.ac.uk/software/figtree/
- **iTOL**（网络可视化）：https://itol.embl.de/
- **MUSCLE**（替代比对工具）：https://www.drive5.com/muscle/
- **TrimAl**（比对修剪）：https://vicfero.github.io/trimal/