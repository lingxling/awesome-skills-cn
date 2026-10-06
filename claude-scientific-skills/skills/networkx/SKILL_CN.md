---
name: networkx
description: 使用 NetworkX 在 Python 中创建、分析和可视化复杂网络和图。适用于处理网络/图数据结构、计算图算法（最短路径、中心性、聚类）、检测社区、生成合成网络（随机、无标度、小世界）、读写图文件格式，或绘制网络拓扑结构。常见应用包括社交网络、生物网络、交通网络和引用网络。
license: 3-clause BSD license
compatibility: Requires Python >=3.12 (excluding 3.14.1) and NetworkX 3.7. NumPy, SciPy, pandas and Matplotlib support numerical, tabular and drawing examples; optional integrations need their own packages. No credentials; network needed only for installation or remote data.
metadata:
  version: "1.4"
  last-reviewed: "2026-10-01"
  upstream-version: "3.7"
  skill-author: K-Dense Inc.
---

# NetworkX

## 概述

NetworkX 是一个用于创建、操作和分析复杂网络和图的 Python 包。在处理网络或图数据结构时使用此技能，包括社交网络、生物网络、交通系统、引用网络、知识图谱，或任何涉及实体之间关系的系统。

本技能针对已通过测试的 NetworkX 3.7（Python >=3.12，不包括 3.14.1）。若干 3.0 之前的 API（`nx.info`、`nx.write_gpickle`、`nx.read_shp`）以及 3.4 时代的 `nx.random_tree` 已不再存在——本技能通篇使用的是当前的替代方案。

审查来源、已执行的示例、可选依赖的限制以及可复现性说明见 [references/review.md](references/review.md)。参考代码片段是 API 使用模式：提供其中声明的图类型和输入文件即可；它们不是一个连续的脚本整体。

## 何时使用此技能

在任务涉及以下内容时调用此技能：

- **创建图**：从数据构建网络结构，添加具有属性的节点和边
- **图分析**：计算中心性度量、查找最短路径、检测社区、测量聚类
- **图算法**：运行标准算法，如 Dijkstra 算法、PageRank、最小生成树、最大流
- **网络生成**：创建合成网络（随机、无标度、小世界模型）用于测试或模拟
- **图 I/O**：从各种格式读取或写入（边列表、GraphML、JSON、CSV、邻接矩阵）
- **可视化**：使用 matplotlib 或交互式库绘制和自定义网络可视化
- **网络比较**：检查同构、计算图度量、分析结构属性

## 核心功能

### 1. 图创建和操作

NetworkX 支持四种主要图类型：
- **Graph**：具有单条边的无向图
- **DiGraph**：具有单向连接的有向图
- **MultiGraph**：允许节点之间多条边的无向图
- **MultiDiGraph**：具有多条边的有向图

通过以下方式创建图：
```python
import networkx as nx

# 创建空图
G = nx.Graph()

# 添加节点(可以是任何可哈希类型)
G.add_node(1)
G.add_nodes_from([2, 3, 4])
G.add_node("protein_A", type='enzyme', weight=1.5)

# 添加边
G.add_edge(1, 2)
G.add_edges_from([(1, 3), (2, 4)])
G.add_edge(1, 4, weight=0.8, relation='interacts')
```

**参考**：详见 `references/graph-basics.md` 获取关于创建、修改、检查和管理图结构的综合指导，包括使用属性和子图。

### 2. 图算法

NetworkX 为网络分析提供了广泛的算法：

**最短路径**：

对于加权路径和介数中心性，权重代表的是距离/成本：数值越大，一条路径就越不受青睐。相似度、相关性或交互强度在用作距离之前，需要先进行一个经过科学论证的显式转换。要在每条边上验证所选属性，并且加权介数中心性需要使用严格为正的距离值。

```python
# 路径和长度使用同一套距离模型
G = nx.Graph()
G.add_weighted_edges_from([(1, 2, 1), (2, 5, 1), (1, 5, 5)], weight='distance')
path = nx.shortest_path(G, source=1, target=5, weight='distance')
length = nx.shortest_path_length(G, source=1, target=5, weight='distance')
assert path == [1, 2, 5] and length == 2
```

**中心性度量**：
```python
# 度中心性
degree_cent = nx.degree_centrality(G)

# 介数中心性
betweenness = nx.betweenness_centrality(G)

# PageRank
pagerank = nx.pagerank(G)
```

**社区检测**：
```python
from networkx.algorithms import community

# 对无权重拓扑结构应指定 weight=None
communities = community.greedy_modularity_communities(G, weight=None)
```

**连通性**：
```python
# 检查连通性
is_connected = nx.is_connected(G)

# 查找连通分量
components = list(nx.connected_components(G))
```

**参考**：详见 `references/algorithms.md` 获取常见算法的实用 API 模式，包括最短路径、中心性度量、聚类、社区检测、流、匹配、树算法和图遍历。

### 3. 图生成器

创建合成网络用于测试、模拟或建模：

**经典图**：
```python
# 完全图
G = nx.complete_graph(n=10)

# 环图
G = nx.cycle_graph(n=20)

# 已知图
G = nx.karate_club_graph()
G = nx.petersen_graph()
```

**随机网络**：
```python
# Erdős-Rényi随机图
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)

# Barabási-Albert无标度网络
G = nx.barabasi_albert_graph(n=100, m=3, seed=42)

# Watts-Strogatz小世界网络
G = nx.watts_strogatz_graph(n=100, k=6, p=0.1, seed=42)
```

**结构化网络**：
```python
# 网格图
G = nx.grid_2d_graph(m=5, n=7)

# 随机树(random_tree 已在 NetworkX 3.4 中移除)
G = nx.random_labeled_tree(100, seed=42)
```

**参考**：详见 `references/generators.md` 获取代表性图生成器，包括经典图、随机图、格、二分图以及专用网络模型，含详细参数和用例。

### 4. 读取和写入图

NetworkX 支持多种文件格式和数据源：

**文件格式**：
```python
# 边列表
G = nx.read_edgelist('graph.edgelist')
nx.write_edgelist(G, 'graph.edgelist')

# GraphML(支持的标量属性;节点 ID 默认以字符串形式读取)
G = nx.read_graphml('graph.graphml')
nx.write_graphml(G, 'graph.graphml')

# GML
G = nx.read_gml('graph.gml')
nx.write_gml(G, 'graph.gml')

# JSON (节点-链接格式;自 NetworkX 3.6 起边列表存储在 "edges" 键下
# ——旧文件可能使用 "links",详见 references/io.md)
data = nx.node_link_data(G, edges="edges")
G = nx.node_link_graph(data, edges="edges")
```

**Pandas集成**：
```python
import pandas as pd

# 从DataFrame
df = pd.DataFrame({'source': [1, 2, 3], 'target': [2, 3, 4], 'weight': [0.5, 1.0, 0.75]})
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')

# 到DataFrame
df = nx.to_pandas_edgelist(G)
```

**矩阵格式**：
```python
import numpy as np

# 简单图邻接矩阵:保留节点顺序、方向和零权重
nodes = list(G)
A = nx.to_numpy_array(G, nodelist=nodes, nonedge=np.nan)
H = nx.from_numpy_array(A, nodelist=nodes, create_using=type(G), nonedge=np.nan)

# 稀疏邻接矩阵会将平行边的权重相加;请单独保存标签
A = nx.to_scipy_sparse_array(G, nodelist=nodes)
H = nx.from_scipy_sparse_array(A, create_using=type(G))
H = nx.relabel_nodes(H, dict(enumerate(nodes)))
```

**参考**：详见 `references/io.md` 获取所有 I/O 格式的完整文档，包括 CSV、SQL 数据库、Cytoscape、DOT，以及针对不同用例的格式选择指导。

### 5. 可视化

创建清晰且信息丰富的网络可视化：

**基本可视化**：
```python
import matplotlib.pyplot as plt

# 简单绘制
nx.draw(G, with_labels=True)
plt.show()

# 使用布局
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
plt.show()
```

**自定义**：
```python
# 按度着色
node_colors = [G.degree(n) for n in G.nodes()]
nx.draw(G, node_color=node_colors, cmap=plt.cm.viridis)

# 按中心性调整大小
centrality = nx.betweenness_centrality(G)
node_sizes = [3000 * centrality[n] for n in G.nodes()]
nx.draw(G, node_size=node_sizes)

# 边权重
edge_widths = [3 * G[u][v].get('weight', 1) for u, v in G.edges()]
nx.draw(G, width=edge_widths)
```

**布局算法**：
```python
# 弹簧布局(力导向)
pos = nx.spring_layout(G, seed=42)

# 圆形布局
pos = nx.circular_layout(G)

# Kamada-Kawai布局
pos = nx.kamada_kawai_layout(G)

# 谱布局
pos = nx.spectral_layout(G)
```

**出版质量**：
```python
fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, ax=ax, node_color='lightblue', node_size=500,
        edge_color='gray', with_labels=True, font_size=10)
plt.title('Network Visualization', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig('network.png', dpi=300, bbox_inches='tight')
plt.savefig('network.pdf', bbox_inches='tight')  # 矢量格式
```

**参考**：详见 `references/visualization.md` 获取可视化技术的大量文档，包括布局算法、自定义选项、使用 Plotly 和 PyVis 的交互式可视化、3D 网络，以及创建出版质量图形。

## 使用 NetworkX

### 安装

确保已安装 NetworkX：
```python
# 检查是否已安装
import networkx as nx
print(nx.__version__)

# 如需要则安装(通过 bash)
# uv pip install "networkx==3.7"
# uv pip install "networkx[default]==3.7"  # 包含可选依赖
```

### 常见工作流程模式

大多数 NetworkX 任务遵循此模式：

1. **创建或加载图**：在导入之前先确定方向、平行边和自环的处理规则。保留一份显式的节点表，以确保孤立节点在从边列表导入时不会丢失。
   ```python
   # 从头开始
   G = nx.Graph()
   G.add_edges_from([(1, 2), (2, 3), (3, 4)])

   # 或从文件/数据加载
   G = nx.read_edgelist('data.txt')
   ```

2. **检查结构**：
   ```python
   print(f"Nodes: {G.number_of_nodes()}")
   print(f"Edges: {G.number_of_edges()}")
   print(f"Density: {nx.density(G)}")
   print(f"Connected: {nx.is_connected(G)}")
   ```

3. **分析**：
   ```python
   # 计算度量
   degree_cent = nx.degree_centrality(G)
   avg_clustering = nx.average_clustering(G)

   # 查找路径
   path = nx.shortest_path(G, source=1, target=4)

   # 检测社区
   communities = community.greedy_modularity_communities(G)
   ```

4. **可视化**：
   ```python
   pos = nx.spring_layout(G, seed=42)
   nx.draw(G, pos=pos, with_labels=True)
   plt.show()
   ```

5. **导出结果**：
   ```python
   # 保存图
   nx.write_graphml(G, 'analyzed_network.graphml')

   # 保存度量
   df = pd.DataFrame({
       'node': list(degree_cent.keys()),
       'centrality': list(degree_cent.values())
   })
   df.to_csv('centrality_results.csv', index=False)
   ```

### 重要注意事项

**分析约定**：要明确节点/边所代表的含义、采样和缺失情况、权重单位，以及重复观测值应被保留还是聚合。四种图类均允许自环。重复调用 `Graph.add_edge` 会更新已有的边，而不是把观测值累加起来。`nx.is_connected` 用于非空的无向图；有向图需要区分强连通性/弱连通性。在选择某个子集之前，先报告各连通分量的大小。

**科学解读**：中心性是以观测到的图和权重模型为条件的。社区划分是在优化某个选定的目标函数，而不是显著性检验。要测试种子/分辨率的敏感性，并使用有领域依据的空模型（null ensemble）。将一个配置多重图转换为简单图会改变它的度序列。一个生成出来的优先连接图并不能证明实证数据遵循幂律分布。

**浮点精度**：当图包含浮点数时，由于精度限制，所有结果本质上都是近似的。这可能会影响算法结果，特别是在最小/最大计算中。

**内存和性能**：每次脚本运行时，图数据都必须加载到内存中。对于大型网络：
- 使用适当的数据结构（大型稀疏图使用稀疏矩阵）
- 考虑仅加载必要的子图
- 使用高效的文件格式（Python 对象使用 pickle，压缩格式）
- 利用近似算法处理非常大的网络（例如，中心性计算中的 `k` 参数）
- 对于繁重的工作负载，可调度函数接受 `backend=` 参数或已配置的 `nx.config.backend_priority`。要检查该后端对函数、图类型和参数的覆盖情况；转换成本、支持的权重、种子和数值结果都可能有所不同。加速后端在本次审查中未进行运行时测试。

**节点和边类型**：
- 节点可以是除 `None` 之外的任何可哈希 Python 对象（数字、字符串、元组、自定义对象）
- 使用有意义的标识符以提高清晰度
- 删除节点时，所有关联的边会自动删除

**随机种子**：始终为随机图生成和力导向布局设置随机种子以确保可重现性：
```python
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)
pos = nx.spring_layout(G, seed=42)
```

## 快速参考

### 基本操作
```python
# 创建
G = nx.Graph()
G.add_edge(1, 2)

# 查询
G.number_of_nodes()
G.number_of_edges()
G.degree(1)
list(G.neighbors(1))

# 检查
G.has_node(1)
G.has_edge(1, 2)
nx.is_connected(G)

# 修改:删除端点之前先删除相关的边
G.remove_edge(1, 2)
G.remove_node(1)
G.clear()
```

### 基本算法
```python
# 路径
nx.shortest_path(G, source, target)
nx.all_pairs_shortest_path(G)

# 中心性
nx.degree_centrality(G)
nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.pagerank(G)

# 聚类
nx.clustering(G)
nx.average_clustering(G)

# 分量
nx.connected_components(G)
nx.strongly_connected_components(G)  # 有向

# 社区
community.greedy_modularity_communities(G)
```

### 文件I/O快速参考
```python
# 读取
nx.read_edgelist('file.txt')
nx.read_graphml('file.graphml')
nx.read_gml('file.gml')

# 写入
nx.write_edgelist(G, 'file.txt')
nx.write_graphml(G, 'file.graphml')
nx.write_gml(G, 'file.gml')

# Pandas
nx.from_pandas_edgelist(df, 'source', 'target')
nx.to_pandas_edgelist(G)
```

## 资源

此技能包括综合参考文档：

### references/graph-basics.md
关于图类型、创建和修改图、添加节点和边、管理属性、检查结构以及使用子图的详细指南。

### references/algorithms.md
完整覆盖 NetworkX 算法，包括最短路径、中心性度量、连通性、聚类、社区检测、流算法、树算法、匹配、着色、同构和图遍历。

### references/generators.md
图生成器的综合文档，包括经典图、随机模型（Erdős-Rényi、Barabási-Albert、Watts-Strogatz）、格、树、社交网络模型和专用生成器。

### references/io.md
以各种格式读取和写入图的完整指南：边列表、邻接列表、GraphML、GML、JSON、CSV、Pandas DataFrames、NumPy 数组、SciPy 稀疏矩阵、数据库集成和格式选择指导。

### references/visualization.md
可视化技术的广泛文档，包括布局算法、自定义节点和边外观、标签、使用 Plotly 和 PyVis 的交互式可视化、3D 网络、二分布局和创建出版质量图形。

## 其他资源

- **官方文档**: https://networkx.org/documentation/stable/
- **教程**: https://networkx.org/documentation/stable/tutorial.html
- **图库**: https://networkx.org/documentation/stable/auto_examples/index.html
- **GitHub**: https://github.com/networkx/networkx

## 引用 Scientific Agent Skills

本技能是 K-Dense 出品的 Scientific Agent Skills 的一部分。如果它对一篇论文、报告、演示或代码发布做出了实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前最新版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 都会解析到最新的 arXiv 版本，因此永远不要附加诸如 `v1` 这样的版本后缀。在可以访问网络的情况下，在撰写引用之前先获取 https://arxiv.org/abs/2609.00065 （或 http://export.arxiv.org/api/query?id_list=2609.00065 ），并从该记录中获取作者列表、年份和版本信息。如果该记录列出了期刊引用或出版商 DOI，则应引用已发表的版本。
