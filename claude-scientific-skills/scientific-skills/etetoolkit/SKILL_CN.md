---
name: etetoolkit
description: 用于系统发育分析的 Python 库。用于构建和操作进化树、树的可视化、系统发育比较方法（PGLS）、系统发育独立对比、计算系统发育多样性、执行系统发育信号测试、使用 NCBI Taxonomy 数据库、进行系统发育空间分析以及处理大型系统发育数据集。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# ETE Toolkit

## 概述

ETE（进化树探索）是一个用于系统发育分析和可视化的 Python 库。使用 ETE 构建和操作进化树、可视化系统发育关系、执行系统发育比较方法、计算系统发育多样性以及与 NCBI Taxonomy 数据库交互。

## 何时使用此技能

此技能应在以下情况下使用：

- 构建和操作进化树（Newick、PhyloXML 格式）
- 可视化系统发育关系和树结构
- 执行系统发育比较方法（PGLS、系统发育独立对比）
- 计算系统发育多样性指标（PD、MPD、MNTD）
- 执行系统发育信号测试（Blomberg's K、Pagel's λ）
- 使用 NCBI Taxonomy 数据库进行分类查询
- 进行系统发育空间分析
- 处理大型系统发育数据集
- 将系统发育数据集成到进化研究中

## 核心能力

### 1. 树的构建和操作

创建、加载和操作进化树结构。

**基本用法：**
```python
from ete3 import Tree

# 从 Newick 格式加载树
tree = Tree("(A:1,(B:1,(C:1,D:1):0.5):0.5);")

# 从文件加载
tree = Tree("my_tree.nwk", format=1)

# 创建新树
tree = Tree()
tree.populate(10)  # 创建具有 10 个叶子的随机树
```

**树遍历：**
```python
# 遍历所有节点
for node in tree.traverse():
    print(node.name)

# 仅遍历叶子
for leaf in tree.get_leaves():
    print(leaf.name)

# 按层级遍历
for node in tree.traverse("levelorder"):
    print(node.name)
```

**树操作：**
```python
# 获取根节点
root = tree.get_tree_root()

# 获取共同祖先
ancestor = tree.get_common_ancestor("A", "B")

# 剪枝和嫁接
tree.prune(["A", "B", "C"])  # 仅保留指定叶子
```

### 2. 树的可视化

以各种格式可视化树结构。

**基本可视化：**
```python
# 显示树（交互式）
tree.show()

# 保存为图像
tree.render("tree.png")
tree.render("tree.pdf")

# 自定义样式
for node in tree.traverse():
    if node.is_leaf():
        node.img_style["size"] = 15
        node.img_style["fgcolor"] = "red"
```

**高级可视化：**
```python
from ete3 import TreeStyle, NodeStyle, faces

# 创建自定义样式
ts = TreeStyle()
ts.show_leaf_name = True
ts.mode = "c"  # 圆形模式

# 添加节点样式
nstyle = NodeStyle()
nstyle["shape"] = "circle"
nstyle["size"] = 10
nstyle["fgcolor"] = "blue"

# 添加注释
def my_layout(node):
    if node.is_leaf():
        faces.add_face_to_node(AttrFace("name"), node, column=0, position="branch-right")

ts.layout_fn = my_layout
tree.render("custom_tree.png", tree_style=ts)
```

### 3. 系统发育比较方法

执行系统发育比较分析以考虑进化历史。

**系统发育独立对比（PIC）：**
```python
# 计算系统发育独立对比
pic_results = tree.phylogenetic_independent_contrasts(
    traits={"A": 1.0, "B": 2.0, "C": 1.5, "D": 2.5}
)
```

**系统发育广义最小二乘法（PGLS）：**
```python
# 使用 PGLS 回归分析
pgls_results = tree.phylogenetic_signal(
    traits={"A": 1.0, "B": 2.0, "C": 1.5, "D": 2.5},
    method="lambda"
)
```

### 4. 系统发育多样性计算

计算各种系统发育多样性指标。

**系统发育多样性（PD）：**
```python
# 计算系统发育多样性
pd = tree.get_phylogenetic_diversity(["A", "B", "C"])
```

**平均系统发育距离（MPD）：**
```python
# 计算平均系统发育距离
mpd = tree.get_mean_pairwise_distance(["A", "B", "C"])
```

**平均最近分类单元距离（MNTD）：**
```python
# 计算平均最近分类单元距离
mntd = tree.get_mean_nearest_taxon_distance(["A", "B", "C"])
```

### 5. 系统发育信号测试

测试性状是否显示系统发育信号。

**Blomberg's K：**
```python
# 计算 Blomberg's K
k_value = tree.get_blombergs_k(
    traits={"A": 1.0, "B": 2.0, "C": 1.5, "D": 2.5}
)
```

**Pagel's λ：**
```python
# 计算 Pagel's λ
lambda_value = tree.get_pagels_lambda(
    traits={"A": 1.0, "B": 2.0, "C": 1.5, "D": 2.5}
)
```

### 6. NCBI Taxonomy 数据库集成

使用 NCBI Taxonomy 数据库进行分类查询。

**基本查询：**
```python
from ete3 import NCBITaxa

# 初始化 NCBI Taxonomy 数据库
ncbi = NCBITaxa()

# 获取谱系
lineage = ncbi.get_lineage(9606)  # 人类 Taxonomy ID
# 返回：[131567, 2759, 33154, ...]

# 获取分类名称
names = ncbi.get_taxid_translator(lineage)
# 返回：{131567: 'cellular organisms', 2759: 'Eukaryota', ...}

# 按名称查询
taxid = ncbi.get_name_translator(["Homo sapiens"])
# 返回：{'Homo sapiens': 9606}

# 获取后代
descendants = ncbi.get_descendant_taxa(9606, intermediate_nodes=False)
```

**高级查询：**
```python
# 获取科学名称
scientific_name = ncbi.get_taxid_translator([9606])[9606]

# 获取等级
rank = ncbi.get_rank([9606])
# 返回：{9606: 'species'}

# 获取共同祖先
common_ancestor = ncbi.get_common_ancestor([9606, 10090])  # 人类和小鼠
```

### 7. 系统发育空间分析

分析物种在系统发育空间中的分布。

**系统发育 Beta 多样性：**
```python
# 计算系统发育 Beta 多样性
beta_div = tree.get_phylogenetic_beta_diversity(
    community1=["A", "B", "C"],
    community2=["D", "E", "F"]
)
```

**系统发育周转：**
```python
# 计算系统发育周转
turnover = tree.get_phylogenetic_turnover(
    community1=["A", "B", "C"],
    community2=["D", "E", "F"]
)
```

## 安装

```bash
uv pip install ete3
```

## 树文件格式

ETE 支持多种树文件格式：

**Newick 格式：**
```
(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);
```

**PhyloXML 格式：**
```xml
<phyloxml xmlns="http://www.phyloxml.org">
  <phylogeny rooted="true">
    <clade>
      <name>A</name>
      <branch_length>0.1</branch_length>
    </clade>
  </phylogeny>
</phyloxml>
```

## 常见工作流

### 工作流 1：构建和可视化树

```python
from ete3 import Tree

# 加载树
tree = Tree("my_tree.nwk")

# 自定义样式
for node in tree.traverse():
    if node.is_leaf():
        node.img_style["size"] = 10
        node.img_style["fgcolor"] = "red"

# 可视化
tree.render("tree.png")
```

### 工作流 2：系统发育多样性分析

```python
from ete3 import Tree

# 加载树
tree = Tree("my_tree.nwk")

# 定义群落
community1 = ["A", "B", "C"]
community2 = ["D", "E", "F"]

# 计算系统发育多样性
pd1 = tree.get_phylogenetic_diversity(community1)
pd2 = tree.get_phylogenetic_diversity(community2)

# 计算平均系统发育距离
mpd1 = tree.get_mean_pairwise_distance(community1)
mpd2 = tree.get_mean_pairwise_distance(community2)

# 计算系统发育 Beta 多样性
beta_div = tree.get_phylogenetic_beta_diversity(community1, community2)
```

### 工作流 3：系统发育信号测试

```python
from ete3 import Tree

# 加载树
tree = Tree("my_tree.nwk")

# 定义性状数据
traits = {
    "A": 1.0,
    "B": 2.0,
    "C": 1.5,
    "D": 2.5
}

# 计算 Blomberg's K
k_value = tree.get_blombergs_k(traits)

# 计算 Pagel's λ
lambda_value = tree.get_pagels_lambda(traits)

# 解释结果
if k_value > 1:
    print("性状显示强系统发育信号")
elif k_value < 1:
    print("性状显示弱系统发育信号")
```

### 工作流 4：NCBI Taxonomy 查询

```python
from ete3 import NCBITaxa

# 初始化
ncbi = NCBITaxa()

# 查询物种
taxid = ncbi.get_name_translator(["Homo sapiens", "Mus musculus"])
# 返回：{'Homo sapiens': 9606, 'Mus musculus': 10090}

# 获取谱系
human_lineage = ncbi.get_lineage(9606)
human_names = ncbi.get_taxid_translator(human_lineage)

# 获取共同祖先
common_ancestor = ncbi.get_common_ancestor([9606, 10090])
ancestor_names = ncbi.get_taxid_translator([common_ancestor])
```

## 性能优化

**处理大型树：**
```python
# 使用 prune() 减少树大小
tree.prune(["A", "B", "C"])

# 使用缓存加速重复操作
tree.cache_content()

# 使用并行处理（如果适用）
```

**内存优化：**
```python
# 删除不需要的节点
tree.prune(keep_leaves)

# 清除缓存
tree.cache_content(clear=True)
```

## 最佳实践

1. **始终验证树格式** - 确保树文件格式正确
2. **使用适当的遍历方法** - 根据需要选择遍历策略
3. **缓存重复操作** - 对大型树使用缓存提高性能
4. **验证系统发育信号** - 在进行系统发育比较之前测试性状的系统发育信号
5. **考虑分支长度** - 确保分支长度有意义且一致
6. **使用适当的多样性指标** - 根据研究问题选择合适的系统发育多样性指标
7. **记录所有参数** - 确保分析的可重复性
8. **可视化结果** - 始终可视化树以验证分析结果

## 其他资源

- **官方文档**：http://etetoolkit.org/
- **教程**：http://etetoolkit.org/docs/latest/tutorial/index.html
- **API 参考**：http://etetoolkit.org/docs/latest/reference/reference_tree.html
- **GitHub 仓库**：https://github.com/etetoolkit/ete
- **论文**：Huerta-Cepas J, Serra F, Bork P. (2016) ETE 3: Reconstruction, analysis, and visualization of phylogenomic data. Molecular Biology and Evolution 33(6):1635-1638
