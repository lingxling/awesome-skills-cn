---
name: torch-geometric
description: 图神经网络 (PyG)。节点/图分类、链接预测、GCN、GAT、GraphSAGE、异构图、分子属性预测，用于几何深度学习。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyTorch Geometric (PyG)

## 概述

PyTorch Geometric 是一个基于 PyTorch 构建的库，用于开发和训练图神经网络 (GNN)。此技能适用于图和不规则结构的深度学习，包括小批量处理、多 GPU 训练和几何深度学习应用。

## 何时使用此技能

当您处理以下任务时，应使用此技能：
- **基于图的机器学习**：节点分类、图分类、链接预测
- **分子属性预测**：药物发现、化学属性预测
- **社交网络分析**：社区检测、影响力预测
- **引用网络**：论文分类、推荐系统
- **3D 几何数据**：点云、网格、分子结构
- **异构图**：多类型节点和边（例如知识图谱）
- **大规模图学习**：邻居采样、分布式训练

## 快速开始

### 安装

```bash
uv pip install torch_geometric
```

对于额外的依赖项（稀疏操作、聚类）：
```bash
uv pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html
```

### 基本图创建

```python
import torch
from torch_geometric.data import Data

# 创建一个包含 3 个节点的简单图
edge_index = torch.tensor([[0, 1, 1, 2],  # 源节点
                           [1, 0, 2, 1]], dtype=torch.long)  # 目标节点
x = torch.tensor([[-1], [0], [1]], dtype=torch.float)  # 节点特征

data = Data(x=x, edge_index=edge_index)
print(f"节点: {data.num_nodes}, 边: {data.num_edges}")
```

### 加载基准数据集

```python
from torch_geometric.datasets import Planetoid

# 加载 Cora 引用网络
dataset = Planetoid(root='/tmp/Cora', name='Cora')
data = dataset[0]  # 获取第一个（也是唯一的）图

print(f"数据集: {dataset}")
print(f"节点: {data.num_nodes}, 边: {data.num_edges}")
print(f"特征: {data.num_node_features}, 类别: {dataset.num_classes}")
```

## 核心概念

### 数据结构

PyG 使用 `torch_geometric.data.Data` 类表示图，具有以下关键属性：

- **`data.x`**：节点特征矩阵 `[num_nodes, num_node_features]`
- **`data.edge_index`**：COO 格式的图连接 `[2, num_edges]`
- **`data.edge_attr`**：边特征矩阵 `[num_edges, num_edge_features]`（可选）
- **`data.y`**：节点或图的目标标签
- **`data.pos`**：节点空间位置 `[num_nodes, num_dimensions]`（可选）
- **自定义属性**：可以添加任何属性（例如 `data.train_mask`, `data.batch`）

**重要**：这些属性不是强制性的——根据需要扩展 Data 对象的自定义属性。

### 边索引格式

边以 COO（坐标）格式存储为 `[2, num_edges]` 张量：
- 第一行：源节点索引
- 第二行：目标节点索引

```python
# 边列表：(0→1), (1→0), (1→2), (2→1)
edge_index = torch.tensor([[0, 1, 1, 2],
                           [1, 0, 2, 1]], dtype=torch.long)
```

### 小批量处理

PyG 通过创建块对角邻接矩阵来处理批处理，将多个图连接成一个大的不连通图：

- 邻接矩阵对角堆叠
- 节点特征沿节点维度连接
- `batch` 向量将每个节点映射到其源图
- 无需填充——计算效率高

```python
from torch_geometric.loader import DataLoader

loader = DataLoader(dataset, batch_size=32, shuffle=True)
for batch in loader:
    print(f"批量大小: {batch.num_graphs}")
    print(f"总节点数: {batch.num_nodes}")
    # batch.batch 将节点映射到图
```

## 构建图神经网络

### 消息传递范式

PyG 中的 GNN 遵循邻域聚合方案：
1. 转换节点特征
2. 沿边传播消息
3. 聚合来自邻居的消息
4. 更新节点表示

### 使用预构建层

PyG 提供 40+ 个卷积层。常见的包括：

**GCNConv**（图卷积网络）：
```python
from torch_geometric.nn import GCNConv
import torch.nn.functional as F

class GCN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

**GATConv**（图注意力网络）：
```python
from torch_geometric.nn import GATConv

class GAT(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GATConv(num_features, 8, heads=8, dropout=0.6)
        self.conv2 = GATConv(8 * 8, num_classes, heads=1, concat=False, dropout=0.6)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.dropout(x, p=0.6, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

**GraphSAGE**：
```python
from torch_geometric.nn import SAGEConv

class GraphSAGE(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = SAGEConv(num_features, 64)
        self.conv2 = SAGEConv(64, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

### 自定义消息传递层

对于自定义层，继承 `MessagePassing`：

```python
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class CustomConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='add')  # "add", "mean", 或 "max"
        self.lin = torch.nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index):
        # 向邻接矩阵添加自环
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        # 转换节点特征
        x = self.lin(x)

        # 计算归一化
        row, col = edge_index
        deg = degree(col, x.size(0), dtype=x.dtype)
        deg_inv_sqrt = deg.pow(-0.5)
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]

        # 传播消息
        return self.propagate(edge_index, x=x, norm=norm)

    def message(self, x_j, norm):
        # x_j: 源节点的特征
        return norm.view(-1, 1) * x_j
```

关键方法：
- **`forward()`**：主入口点
- **`message()`**：从源节点到目标节点构造消息
- **`aggregate()`**：聚合消息（通常不重写——设置 `aggr` 参数）
- **`update()`**：聚合后更新节点嵌入

**变量命名约定**：在张量名称后追加 `_i` 或 `_j` 会自动将它们映射到目标或源节点。

## 处理数据集

### 加载内置数据集

PyG 提供广泛的基准数据集：

```python
# 引用网络（节点分类）
from torch_geometric.datasets import Planetoid
dataset = Planetoid(root='/tmp/Cora', name='Cora')  # 或 'CiteSeer', 'PubMed'

# 图分类
from torch_geometric.datasets import TUDataset
dataset = TUDataset(root='/tmp/ENZYMES', name='ENZYMES')

# 分子数据集
from torch_geometric.datasets import QM9
dataset = QM9(root='/tmp/QM9')

# 大规模数据集
from torch_geometric.datasets import Reddit
dataset = Reddit(root='/tmp/Reddit')
```

请查看 `references/datasets_reference.md` 获取完整列表。

### 创建自定义数据集

对于适合内存的数据集，继承 `InMemoryDataset`：

```python
from torch_geometric.data import InMemoryDataset, Data
import torch

class MyOwnDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super().__init__(root, transform, pre_transform)
        self.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return ['my_data.csv']  # raw_dir 中需要的文件

    @property
    def processed_file_names(self):
        return ['data.pt']  # processed_dir 中的文件

    def download(self):
        # 下载原始数据到 self.raw_dir
        pass

    def process(self):
        # 读取数据，创建 Data 对象
        data_list = []

        # 示例：创建一个简单的图
        edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)
        x = torch.randn(2, 16)
        y = torch.tensor([0], dtype=torch.long)

        data = Data(x=x, edge_index=edge_index, y=y)
        data_list.append(data)

        # 应用 pre_filter 和 pre_transform
        if self.pre_filter is not None:
            data_list = [d for d in data_list if self.pre_filter(d)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(d) for d in data_list]

        # 保存处理后的数据
        self.save(data_list, self.processed_paths[0])
```

对于不适合内存的大型数据集，继承 `Dataset` 并实现 `len()` 和 `get(idx)`。

### 从 CSV 加载图

```python
import pandas as pd
import torch
from torch_geometric.data import HeteroData

# 加载节点
nodes_df = pd.read_csv('nodes.csv')
x = torch.tensor(nodes_df[['feat1', 'feat2']].values, dtype=torch.float)

# 加载边
edges_df = pd.read_csv('edges.csv')
edge_index = torch.tensor([edges_df['source'].values,
                           edges_df['target'].values], dtype=torch.long)

data = Data(x=x, edge_index=edge_index)
```

## 训练工作流程

### 节点分类（单个图）

```python
import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid

# 加载数据集
dataset = Planetoid(root='/tmp/Cora', name='Cora')
data = dataset[0]

# 创建模型
model = GCN(dataset.num_features, dataset.num_classes)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# 训练
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'轮次 {epoch}, 损失: {loss.item():.4f}')

# 评估
model.eval()
pred = model(data).argmax(dim=1)
correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
acc = int(correct) / int(data.test_mask.sum())
print(f'测试准确率: {acc:.4f}')
```

### 图分类（多个图）

```python
from torch_geometric.datasets import TUDataset
from torch_geometric.loader import DataLoader
from torch_geometric.nn import global_mean_pool

class GraphClassifier(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.conv2 = GCNConv(64, 64)
        self.lin = torch.nn.Linear(64, num_classes)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)

        # 全局池化（将节点特征聚合到图级别）
        x = global_mean_pool(x, batch)

        x = self.lin(x)
        return F.log_softmax(x, dim=1)

# 加载数据集
dataset = TUDataset(root='/tmp/ENZYMES', name='ENZYMES')
loader = DataLoader(dataset, batch_size=32, shuffle=True)

model = GraphClassifier(dataset.num_features, dataset.num_classes)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 训练
model.train()
for epoch in range(100):
    total_loss = 0
    for batch in loader:
        optimizer.zero_grad()
        out = model(batch)
        loss = F.nll_loss(out, batch.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    if epoch % 10 == 0:
        print(f'轮次 {epoch}, 损失: {total_loss / len(loader):.4f}')
```

### 带邻居采样的大规模图

对于大型图，使用 `NeighborLoader` 采样子图：

```python
from torch_geometric.loader import NeighborLoader

# 创建邻居采样器
train_loader = NeighborLoader(
    data,
    num_neighbors=[25, 10],  # 为第 1 跳采样 25 个邻居，第 2 跳 10 个
    batch_size=128,
    input_nodes=data.train_mask,
)

# 训练
model.train()
for batch in train_loader:
    optimizer.zero_grad()
    out = model(batch)
    # 仅对种子节点（前 batch_size 个节点）计算损失
    loss = F.nll_loss(out[:batch.batch_size], batch.y[:batch.batch_size])
    loss.backward()
    optimizer.step()
```

**重要**：
- 输出子图是有向的
- 节点索引被重新标记（0 到 batch.num_nodes - 1）
- 仅使用种子节点预测计算损失
- 采样超过 2-3 跳通常不可行

## 高级功能

### 异构图

对于具有多种节点和边类型的图，使用 `HeteroData`：

```python
from torch_geometric.data import HeteroData

data = HeteroData()

# 添加不同类型的节点特征
data['paper'].x = torch.randn(100, 128)  # 100 篇论文，128 个特征
data['author'].x = torch.randn(200, 64)  # 200 位作者，64 个特征

# 添加不同类型的边（source_type, edge_type, target_type）
data['author', 'writes', 'paper'].edge_index = torch.randint(0, 200, (2, 500))
data['paper', 'cites', 'paper'].edge_index = torch.randint(0, 100, (2, 300))

print(data)
```

将同质模型转换为异质：

```python
from torch_geometric.nn import to_hetero

# 定义同质模型
model = GNN(...)

# 转换为异质
model = to_hetero(model, data.metadata(), aggr='sum')

# 正常使用
out = model(data.x_dict, data.edge_index_dict)
```

或使用 `HeteroConv` 进行自定义边类型特定操作：

```python
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv

class HeteroGNN(torch.nn.Module):
    def __init__(self, metadata):
        super().__init__()
        self.conv1 = HeteroConv({
            ('paper', 'cites', 'paper'): GCNConv(-1, 64),
            ('author', 'writes', 'paper'): SAGEConv((-1, -1), 64),
        }, aggr='sum')

        self.conv2 = HeteroConv({
            ('paper', 'cites', 'paper'): GCNConv(64, 32),
            ('author', 'writes', 'paper'): SAGEConv((64, 64), 32),
        }, aggr='sum')

    def forward(self, x_dict, edge_index_dict):
        x_dict = self.conv1(x_dict, edge_index_dict)
        x_dict = {key: F.relu(x) for key, x in x_dict.items()}
        x_dict = self.conv2(x_dict, edge_index_dict)
        return x_dict
```

### 变换

应用变换修改图结构或特征：

```python
from torch_geometric.transforms import NormalizeFeatures, AddSelfLoops, Compose

# 单个变换
transform = NormalizeFeatures()
dataset = Planetoid(root='/tmp/Cora', name='Cora', transform=transform)

# 组合多个变换
transform = Compose([
    AddSelfLoops(),
    NormalizeFeatures(),
])
dataset = Planetoid(root='/tmp/Cora', name='Cora', transform=transform)
```

常见变换：
- **结构**：`ToUndirected`, `AddSelfLoops`, `RemoveSelfLoops`, `KNNGraph`, `RadiusGraph`
- **特征**：`NormalizeFeatures`, `NormalizeScale`, `Center`
- **采样**：`RandomNodeSplit`, `RandomLinkSplit`
- **位置编码**：`AddLaplacianEigenvectorPE`, `AddRandomWalkPE`

请查看 `references/transforms_reference.md` 获取完整列表。

### 模型可解释性

PyG 提供可解释性工具来理解模型预测：

```python
from torch_geometric.explain import Explainer, GNNExplainer

# 创建解释器
explainer = Explainer(
    model=model,
    algorithm=GNNExplainer(epochs=200),
    explanation_type='model',  # 或 'phenomenon'
    node_mask_type='attributes',
    edge_mask_type='object',
    model_config=dict(
        mode='multiclass_classification',
        task_level='node',
        return_type='log_probs',
    ),
)

# 为特定节点生成解释
node_idx = 10
explanation = explainer(data.x, data.edge_index, index=node_idx)

# 可视化
print(f'节点 {node_idx} 解释:')
print(f'重要边: {explanation.edge_mask.topk(5).indices}')
print(f'重要特征: {explanation.node_mask[node_idx].topk(5).indices}')
```

### 池化操作

对于层次图表示：

```python
from torch_geometric.nn import TopKPooling, global_mean_pool

class HierarchicalGNN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.pool1 = TopKPooling(64, ratio=0.8)
        self.conv2 = GCNConv(64, 64)
        self.pool2 = TopKPooling(64, ratio=0.8)
        self.lin = torch.nn.Linear(64, num_classes)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = F.relu(self.conv1(x, edge_index))
        x, edge_index, _, batch, _, _ = self.pool1(x, edge_index, None, batch)

        x = F.relu(self.conv2(x, edge_index))
        x, edge_index, _, batch, _, _ = self.pool2(x, edge_index, None, batch)

        x = global_mean_pool(x, batch)
        x = self.lin(x)
        return F.log_softmax(x, dim=1)
```

## 常见模式和最佳实践

### 检查图属性

```python
# 无向检查
from torch_geometric.utils import is_undirected
print(f"是否无向: {is_undirected(data.edge_index)}")

# 连通组件
from torch_geometric.utils import connected_components
print(f"连通组件: {connected_components(data.edge_index)}")

# 包含自环
from torch_geometric.utils import contains_self_loops
print(f"有自环: {contains_self_loops(data.edge_index)}")
```

### GPU 训练

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
data = data.to(device)

# 对于 DataLoader
for batch in loader:
    batch = batch.to(device)
    # 训练...
```

### 保存和加载模型

```python
# 保存
torch.save(model.state_dict(), 'model.pth')

# 加载
model = GCN(num_features, num_classes)
model.load_state_dict(torch.load('model.pth'))
model.eval()
```

### 层能力

选择层时，考虑这些能力：
- **SparseTensor**：支持高效的稀疏矩阵操作
- **edge_weight**：处理一维边权重
- **edge_attr**：处理多维边特征
- **Bipartite**：适用于二分图（不同的源/目标维度）
- **Lazy**：无需指定输入维度即可初始化

请查看 GNN 速查表 `references/layer_capabilities.md`。

## 资源

### 捆绑参考

此技能包含详细的参考文档：

- **`references/layers_reference.md`**：所有 40+ GNN 层的完整列表，带有描述和能力
- **`references/datasets_reference.md`**：按类别组织的综合数据集目录
- **`references/transforms_reference.md`**：所有可用的变换及其用例
- **`references/api_patterns.md`**：常见的 API 模式和编码示例

### 脚本

`scripts/` 中提供了实用脚本：

- **`scripts/visualize_graph.py`**：使用 networkx 和 matplotlib 可视化图结构
- **`scripts/create_gnn_template.py`**：为常见 GNN 架构生成样板代码
- **`scripts/benchmark_model.py`**：在标准数据集上基准测试模型性能

直接执行脚本或阅读它们以了解实现模式。

### 官方资源

- **文档**：https://pytorch-geometric.readthedocs.io/
- **GitHub**：https://github.com/pyg-team/pytorch_geometric
- **教程**：https://pytorch-geometric.readthedocs.io/en/latest/get_started/introduction.html
- **示例**：https://github.com/pyg-team/pytorch_geometric/tree/master/examples