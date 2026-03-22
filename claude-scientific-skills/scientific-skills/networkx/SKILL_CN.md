---
name: networkx
description: 用于在Python中创建、分析和可视化复杂网络和图的综合工具包。在处理网络/图数据结构、分析实体之间的关系、计算图算法(最短路径、中心性、聚类)、检测社区、生成合成网络或可视化网络拓扑时使用。适用于社交网络、生物网络、交通系统、引用网络以及任何涉及成对关系的领域。
license: 3-clause BSD license
metadata:
    skill-author: K-Dense Inc.
---

# NetworkX

## 概述

NetworkX是一个用于创建、操作和分析复杂网络和图的Python包。在处理网络或图数据结构时使用此技能,包括社交网络、生物网络、交通系统、引用网络、知识图谱或任何涉及实体之间关系的系统。

## 何时使用此技能

在任务涉及以下内容时调用此技能:

- **创建图**: 从数据构建网络结构,添加具有属性的节点和边
- **图分析**: 计算中心性度量、查找最短路径、检测社区、测量聚类
- **图算法**: 运行标准算法,如Dijkstra算法、PageRank、最小生成树、最大流
- **网络生成**: 创建合成网络(随机、无标度、小世界模型)用于测试或模拟
- **图I/O**: 从各种格式读取或写入(边列表、GraphML、JSON、CSV、邻接矩阵)
- **可视化**: 使用matplotlib或交互式库绘制和自定义网络可视化
- **网络比较**: 检查同构、计算图度量、分析结构属性

## 核心功能

### 1. 图创建和操作

NetworkX支持四种主要图类型:
- **Graph**: 具有单条边的无向图
- **DiGraph**: 具有单向连接的有向图
- **MultiGraph**: 允许节点之间多条边的无向图
- **MultiDiGraph**: 具有多条边的有向图

通过以下方式创建图:
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

**参考**: 详见`references/graph-basics.md`获取关于创建、修改、检查和管理图结构的综合指导,包括使用属性和子图。

### 2. 图算法

NetworkX为网络分析提供了广泛的算法:

**最短路径**:
```python
# 查找最短路径
path = nx.shortest_path(G, source=1, target=5)
length = nx.shortest_path_length(G, source=1, target=5, weight='weight')
```

**中心性度量**:
```python
# 度中心性
degree_cent = nx.degree_centrality(G)

# 介数中心性
betweenness = nx.betweenness_centrality(G)

# PageRank
pagerank = nx.pagerank(G)
```

**社区检测**:
```python
from networkx.algorithms import community

# 检测社区
communities = community.greedy_modularity_communities(G)
```

**连通性**:
```python
# 检查连通性
is_connected = nx.is_connected(G)

# 查找连通分量
components = list(nx.connected_components(G))
```

**参考**: 详见`references/algorithms.md`获取所有可用算法的详细文档,包括最短路径、中心性度量、聚类、社区检测、流、匹配、树算法和图遍历。

### 3. 图生成器

创建合成网络用于测试、模拟或建模:

**经典图**:
```python
# 完全图
G = nx.complete_graph(n=10)

# 环图
G = nx.cycle_graph(n=20)

# 已知图
G = nx.karate_club_graph()
G = nx.petersen_graph()
```

**随机网络**:
```python
# Erdős-Rényi随机图
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)

# Barabási-Albert无标度网络
G = nx.barabasi_albert_graph(n=100, m=3, seed=42)

# Watts-Strogatz小世界网络
G = nx.watts_strogatz_graph(n=100, k=6, p=0.1, seed=42)
```

**结构化网络**:
```python
# 网格图
G = nx.grid_2d_graph(m=5, n=7)

# 随机树
G = nx.random_tree(n=100, seed=42)
```

**参考**: 详见`references/generators.md`获取所有图生成器的综合覆盖,包括经典图、随机模型(Erdős-Rényi、Barabási-Albert、Watts-Strogatz)、格、树、社交网络模型和专用生成器,包含详细参数和用例。

### 4. 读取和写入图

NetworkX支持多种文件格式和数据源:

**文件格式**:
```python
# 边列表
G = nx.read_edgelist('graph.edgelist')
nx.write_edgelist(G, 'graph.edgelist')

# GraphML(保留属性)
G = nx.read_graphml('graph.graphml')
nx.write_graphml(G, 'graph.graphml')

# GML
G = nx.read_gml('graph.gml')
nx.write_gml(G, 'graph.gml')

# JSON
data = nx.node_link_data(G)
G = nx.node_link_graph(data)
```

**Pandas集成**:
```python
import pandas as pd

# 从DataFrame
df = pd.DataFrame({'source': [1, 2, 3], 'target': [2, 3, 4], 'weight': [0.5, 1.0, 0.75]})
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')

# 到DataFrame
df = nx.to_pandas_edgelist(G)
```

**矩阵格式**:
```python
import numpy as np

# 邻接矩阵
A = nx.to_numpy_array(G)
G = nx.from_numpy_array(A)

# 稀疏矩阵
A = nx.to_scipy_sparse_array(G)
G = nx.from_scipy_sparse_array(A)
```

**参考**: 详见`references/io.md`获取所有I/O格式的完整文档,包括CSV、SQL数据库、Cytoscape、DOT以及针对不同用例的格式选择指导。

### 5. 可视化

创建清晰且信息丰富的网络可视化:

**基本可视化**:
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

**自定义**:
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

**布局算法**:
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

**出版质量**:
```python
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, node_color='lightblue', node_size=500,
        edge_color='gray', with_labels=True, font_size=10)
plt.title('Network Visualization', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig('network.png', dpi=300, bbox_inches='tight')
plt.savefig('network.pdf', bbox_inches='tight')  # 矢量格式
```

**参考**: 详见`references/visualization.md`获取可视化技术的广泛文档,包括布局算法、自定义选项、使用Plotly和PyVis的交互式可视化、3D网络和出版质量图形创建。

## 使用NetworkX

### 安装

确保已安装NetworkX:
```python
# 检查是否已安装
import networkx as nx
print(nx.__version__)

# 如需要则安装(通过bash)
# uv pip install networkx
# uv pip install networkx[default]  # 包含可选依赖
```

### 常见工作流程模式

大多数NetworkX任务遵循此模式:

1. **创建或加载图**:
   ```python
   # 从头开始
   G = nx.Graph()
   G.add_edges_from([(1, 2), (2, 3), (3, 4)])

   # 或从文件/数据加载
   G = nx.read_edgelist('data.txt')
   ```

2. **检查结构**:
   ```python
   print(f"Nodes: {G.number_of_nodes()}")
   print(f"Edges: {G.number_of_edges()}")
   print(f"Density: {nx.density(G)}")
   print(f"Connected: {nx.is_connected(G)}")
   ```

3. **分析**:
   ```python
   # 计算度量
   degree_cent = nx.degree_centrality(G)
   avg_clustering = nx.average_clustering(G)

   # 查找路径
   path = nx.shortest_path(G, source=1, target=4)

   # 检测社区
   communities = community.greedy_modularity_communities(G)
   ```

4. **可视化**:
   ```python
   pos = nx.spring_layout(G, seed=42)
   nx.draw(G, pos=pos, with_labels=True)
   plt.show()
   ```

5. **导出结果**:
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

**浮点精度**: 当图包含浮点数时,由于精度限制,所有结果本质上都是近似的。这可能会影响算法结果,特别是在最小/最大计算中。

**内存和性能**: 每次脚本运行时,图数据都必须加载到内存中。对于大型网络:
- 使用适当的数据结构(大型稀疏图使用稀疏矩阵)
- 考虑仅加载必要的子图
- 使用高效的文件格式(Python对象使用pickle,压缩格式)
- 利用近似算法处理非常大的网络(例如,中心性计算中的`k`参数)

**节点和边类型**:
- 节点可以是任何可哈希的Python对象(数字、字符串、元组、自定义对象)
- 使用有意义的标识符以提高清晰度
- 删除节点时,所有关联的边会自动删除

**随机种子**: 始终为随机图生成和力导向布局设置随机种子以确保可重现性:
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

# 修改
G.remove_node(1)
G.remove_edge(1, 2)
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

此技能包括综合参考文档:

### references/graph-basics.md
关于图类型、创建和修改图、添加节点和边、管理属性、检查结构以及使用子图的详细指南。

### references/algorithms.md
完整覆盖NetworkX算法,包括最短路径、中心性度量、连通性、聚类、社区检测、流算法、树算法、匹配、着色、同构和图遍历。

### references/generators.md
图生成器的综合文档,包括经典图、随机模型(Erdős-Rényi、Barabási-Albert、Watts-Strogatz)、格、树、社交网络模型和专用生成器。

### references/io.md
以各种格式读取和写入图的完整指南:边列表、邻接列表、GraphML、GML、JSON、CSV、Pandas DataFrames、NumPy数组、SciPy稀疏矩阵、数据库集成和格式选择指导。

### references/visualization.md
可视化技术的广泛文档,包括布局算法、自定义节点和边外观、标签、使用Plotly和PyVis的交互式可视化、3D网络、二分布局和创建出版质量图形。

## 其他资源

- **官方文档**: https://networkx.org/documentation/latest/
- **教程**: https://networkx.org/documentation/latest/tutorial.html
- **图库**: https://networkx.org/documentation/latest/auto_examples/index.html
- **GitHub**: https://github.com/networkx/networkx
