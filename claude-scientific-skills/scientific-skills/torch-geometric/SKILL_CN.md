---
name: torch-geometric
name_zh: 图神经网络 (PyTorch Geometric)
description: "使用 PyTorch Geometric (PyG) 构建图神经网络的指南。当用户询问图神经网络、GNN、节点分类、链接预测、图分类、消息传递网络、异构图、邻居采样，或任何涉及 torch_geometric / PyG 的任务时，使用此技能。当看到 torch_geometric 的导入语句，或用户提到图卷积（GCN、GAT、GraphSAGE、GIN）、图数据结构，或处理关系/网络数据时，也触发此技能。即使用户只说'图学习'或'几何深度学习'，也要使用此技能。"
description_zh: "使用 PyTorch Geometric (PyG) 构建图神经网络的指南。当用户询问图神经网络、GNN、节点分类、链接预测、图分类、消息传递网络、异构图、邻居采样，或任何涉及 torch_geometric / PyG 的任务时，使用此技能。当看到 torch_geometric 的导入语句，或用户提到图卷积（GCN、GAT、GraphSAGE、GIN）、图数据结构，或处理关系/网络数据时，也触发此技能。即使用户只说'图学习'或'几何深度学习'，也要使用此技能。"
---

# PyTorch Geometric (PyG)

PyG 是基于 PyTorch 构建的图神经网络标准库。它提供了图的数据结构、60+ 种 GNN 层实现、可扩展的小批量训练，以及对异构图的支持。

安装：`uv add torch_geometric`（或 `uv pip install torch_geometric`；需要 PyTorch）。可选：`pyg-lib`、`torch-scatter`、`torch-sparse`、`torch-cluster` 用于加速操作。

## 核心概念

### 图数据：`Data` 和 `HeteroData`

图存储在 `Data` 对象中。关键属性：

```python
from torch_geometric.data import Data

data = Data(
    x=node_features,          # [num_nodes, num_node_features]
    edge_index=edge_index,     # [2, num_edges] — COO 格式，dtype=torch.long
    edge_attr=edge_features,   # [num_edges, num_edge_features]
    y=labels,                  # 节点级 [num_nodes, *] 或图级 [1, *]
    pos=positions,             # [num_nodes, num_dimensions]（用于点云/空间数据）
)
```

**`edge_index` 格式至关重要**：它是一个 `[2, num_edges]` 张量，其中 `edge_index[0]` = 源节点，`edge_index[1]` = 目标节点。它不是元组列表。如果您的边对是行格式，请转置并调用 `.contiguous()`：

```python
# 如果边是 [[src1, dst1], [src2, dst2], ...] — 先转置：
edge_index = edge_pairs.t().contiguous()
```

对于无向图，包括两个方向：边 (0,1) 需要在 edge_index 中同时包含 `[0,1]` 和 `[1,0]`。

对于异构图，使用 `HeteroData` — 见下面的异构图部分。

### 数据集

PyG 捆绑了许多标准数据集，可自动下载和预处理：

```python
from torch_geometric.datasets import Planetoid, TUDataset

# 单图节点分类（Cora、Citeseer、Pubmed）
dataset = Planetoid(root='./data', name='Cora')
data = dataset[0]  # 带有训练/验证/测试掩码的单图

# 多图分类（ENZYMES、MUTAG、IMDB-BINARY 等）
dataset = TUDataset(root='./data', name='ENZYMES')
# dataset[0], dataset[1], ... 是单个图
```

按任务划分的常见数据集：
- **节点分类**：Planetoid（Cora/Citeseer/Pubmed）、OGB（ogbn-arxiv、ogbn-products、ogbn-mag）
- **图分类**：TUDataset（MUTAG、ENZYMES、PROTEINS、IMDB-BINARY）、OGB（ogbg-molhiv）
- **链接预测**：OGB（ogbl-collab、ogbl-citation2）
- **分子**：QM7、QM9、MoleculeNet
- **点云/网格**：ShapeNet、ModelNet10/40、FAUST

### 变换

变换用于预处理或增强图数据，类似于 torchvision 变换：

```python
import torch_geometric.transforms as T

# 常见变换
T.NormalizeFeatures()    # 行归一化节点特征，使其和为 1
T.ToUndirected()         # 添加反向边使图无向
T.AddSelfLoops()         # 添加自环边
T.KNNGraph(k=6)          # 从点云位置构建 k-NN 图
T.RandomJitter(0.01)     # 对位置进行随机噪声增强
T.Compose([...])         # 链接多个变换

# 应用为 pre_transform（一次，保存到磁盘）或 transform（每次访问）
dataset = ShapeNet(root='./data', pre_transform=T.KNNGraph(k=6),
                   transform=T.RandomJitter(0.01))
```

## 构建 GNN 模型

### 快速开始：使用内置层

构建 GNN 的最快方法 — 从 `torch_geometric.nn` 堆叠卷积层：

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return x
```

**重要**：PyG 卷积层不包含激活函数 — 请在每个层后自行应用。这是为了灵活性而设计的。

### 选择卷积层

根据任务和图结构选择：

| 层 | 最适合 | 核心思想 |
|-------|----------|----------|
| `GCNConv` | 同构图，半监督节点分类 | 谱启发，度归一化聚合 |
| `GATConv` / `GATv2Conv` | 当邻居重要性变化时 | 注意力加权消息 |
| `SAGEConv` | 大型图，归纳设置 | 采样友好，可学习聚合 |
| `GINConv` | 图分类，最大化表达能力 | 与 WL 测试一样强大 |
| `TransformerConv` | 丰富的边特征，复杂交互 | 带有边特征的多头注意力 |
| `EdgeConv` | 点云，动态图 | 边特征的 MLP (x_i, x_j - x_i) |
| `RGCNConv` | 具有多种关系类型的异构图 | 关系特定的权重矩阵 |
| `HGTConv` | 异构图 | 类型特定的注意力 |

所有卷积层至少接受 `(x, edge_index)`。许多还接受 `edge_attr` 作为边特征。

### 延迟初始化

使用 `-1` 作为输入通道，让 PyG 自动推断维度 — 对异构模型特别有用：

```python
conv = SAGEConv((-1, -1), 64)  # 输入维度在第一次前向传播时推断
# 初始化延迟模块：
with torch.no_grad():
    out = model(data.x, data.edge_index)
```

### 高级模型 API

对于常见架构，PyG 提供现成的模型类：

```python
from torch_geometric.nn import GraphSAGE, GCN, GAT, GIN

model = GraphSAGE(
    in_channels=dataset.num_features,
    hidden_channels=64,
    out_channels=dataset.num_classes,
    num_layers=2,
)
```

### 通过 MessagePassing 自定义层

要实现新颖的 GNN 层，请继承 `MessagePassing`。框架如下：

1. `propagate()` 协调消息传递
2. `message()` 定义沿每条边流动的信息（phi 函数）
3. `aggregate()` 组合每个节点的消息（sum/mean/max）
4. `update()` 转换聚合结果（gamma 函数）

```python
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class MyConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='add')  # "add", "mean", or "max"
        self.lin = torch.nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index):
        # 消息传递前的预处理
        x = self.lin(x)
        # 开始消息传递
        return self.propagate(edge_index, x=x)

    def message(self, x_j):
        # x_j: 每条边的源节点特征 [num_edges, features]
        # _j 后缀自动索引源节点，_i 索引目标节点
        return x_j
```

**`_i` / `_j` 约定**：传递给 `propagate()` 的任何张量都可以通过在 `message()` 签名中附加 `_i`（目标/中心节点）或 `_j`（源/邻居节点）来自动索引。因此，如果您向 propagate 传递 `x=...`，您可以在 message() 中访问 `x_i` 和 `x_j`。

阅读 `references/message_passing.md` 获取完整的 GCN 和 EdgeConv 实现示例。

## 任务特定模式

### 节点分类

```python
# 在单个图上的全批量训练（例如，Cora）
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

# 评估
model.eval()
pred = model(data.x, data.edge_index).argmax(dim=1)
acc = (pred[data.test_mask] == data.y[data.test_mask]).float().mean()
```

### 图分类

多个图 — 使用 `DataLoader` 进行小批量处理，并使用全局池化获取图级表示：

```python
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool

loader = DataLoader(dataset, batch_size=32, shuffle=True)

class GraphClassifier(torch.nn.Module):
    def __init__(self, in_ch, hidden_ch, out_ch):
        super().__init__()
        self.conv1 = GCNConv(in_ch, hidden_ch)
        self.conv2 = GCNConv(hidden_ch, hidden_ch)
        self.lin = torch.nn.Linear(hidden_ch, out_ch)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index).relu()
        x = global_mean_pool(x, batch)  # [num_graphs_in_batch, hidden_ch]
        return self.lin(x)

# 训练循环
for data in loader:
    out = model(data.x, data.edge_index, data.batch)
    loss = F.cross_entropy(out, data.y)
```

PyG 的 `DataLoader` 通过创建块对角邻接矩阵来批量处理多个图。`batch` 张量将每个节点映射到其图索引。池化操作（`global_mean_pool`、`global_max_pool`、`global_add_pool`）使用此来聚合每个图。

### 链接预测

将边分为训练/验证/测试，使用负采样：

```python
from torch_geometric.transforms import RandomLinkSplit

transform = RandomLinkSplit(
    num_val=0.1,
    num_test=0.1,
    is_undirected=True,
    add_negative_train_samples=False,
)
train_data, val_data, test_data = transform(data)

# 编码节点，然后评分边
z = model.encode(train_data.x, train_data.edge_index)
# 正边
pos_score = (z[train_data.edge_label_index[0]] * z[train_data.edge_label_index[1]]).sum(dim=1)
```

阅读 `references/link_prediction.md` 获取完整的链接预测指南：GAE/VGAE 自动编码器、完整训练循环、大型图的 LinkNeighborLoader、异构链接预测和评估指标。

## 扩展到大型图

对于不适合 GPU 内存的图，使用 `NeighborLoader` 进行邻居采样：

```python
from torch_geometric.loader import NeighborLoader

train_loader = NeighborLoader(
    data,
    num_neighbors=[15, 10],     # 在第 1 跳采样 15 个邻居，第 2 跳采样 10 个
    batch_size=128,              # 每批种子节点数
    input_nodes=data.train_mask, # 从哪些节点采样
    shuffle=True,
)

for batch in train_loader:
    batch = batch.to(device)
    out = model(batch.x, batch.edge_index)
    # 仅使用前 batch_size 个节点计算损失（这些是种子节点）
    loss = F.cross_entropy(out[:batch.batch_size], batch.y[:batch.batch_size])
```

**关于 NeighborLoader 的关键点**：
- `num_neighbors` 列表长度应与 GNN 深度（消息传递层数）匹配
- 种子节点始终是输出中前 `batch.batch_size` 个节点
- `batch.n_id` 将重新标记的索引映射回原始节点 ID
- 适用于 `Data` 和 `HeteroData`
- 对于链接预测，改用 `LinkNeighborLoader`
- 采样超过 2-3 跳通常不可行（指数爆炸）

其他可扩展性选项：`ClusterLoader` (ClusterGCN)、`GraphSAINTSampler`、`ShaDowKHopSampler`。对于多 GPU 训练、DDP、PyTorch Lightning 集成和 `torch.compile` 支持，请阅读 `references/scaling.md`。

## 异构图

对于具有多种节点和边类型的图（社交网络、知识图谱、推荐）：

```python
from torch_geometric.data import HeteroData

data = HeteroData()

# 节点特征 — 按节点类型字符串索引
data['user'].x = torch.randn(1000, 64)
data['movie'].x = torch.randn(500, 128)

# 边索引 — 按 (src_type, edge_type, dst_type) 三元组索引
data['user', 'rates', 'movie'].edge_index = torch.randint(0, 500, (2, 3000))
data['user', 'follows', 'user'].edge_index = torch.randint(0, 1000, (2, 5000))

# 访问便利字典
data.x_dict        # {'user': tensor, 'movie': tensor}
data.edge_index_dict  # {('user','rates','movie'): tensor, ...}
data.metadata()    # ([node_types], [edge_types])
```

### 构建异质 GNN 的三种方法

**1. 使用 `to_hetero()` 自动转换** — 编写同构模型，自动转换：

```python
from torch_geometric.nn import SAGEConv, to_hetero

class GNN(torch.nn.Module):
    def __init__(self, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

model = GNN(64, dataset.num_classes)
model = to_hetero(model, data.metadata(), aggr='sum')

# 现在接受字典：
out = model(data.x_dict, data.edge_index_dict)
```

对二分输入通道使用 `(-1, -1)`（源和目标可能不同）。延迟初始化处理其余部分。

**2. `HeteroConv` 包装器** — 每种边类型使用不同的卷积：

```python
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv, GATConv

conv = HeteroConv({
    ('paper', 'cites', 'paper'): GCNConv(-1, 64),
    ('author', 'writes', 'paper'): SAGEConv((-1, -1), 64),
    ('paper', 'rev_writes', 'author'): GATConv((-1, -1), 64, add_self_loops=False),
}, aggr='sum')
```

**3. 原生异构运算符** 如 `HGTConv`：

```python
from torch_geometric.nn import HGTConv
conv = HGTConv(hidden_channels, hidden_channels, data.metadata(), num_heads=4)
```

**异构图的重要提示**：
- 使用 `T.ToUndirected()` 添加反向边类型以实现双向消息流
- 在二分卷积层中禁用 `add_self_loops`（源和目标类型不同）— 改用跳跃连接：`conv(x, edge_index) + lin(x)`
- 对于 HeteroData 上的 NeighborLoader，将 `input_nodes` 指定为 `('node_type', mask)` 元组
- `num_neighbors` 可以是按边类型键控的字典，用于精细控制

阅读 `references/heterogeneous.md` 获取完整示例，包括训练循环和异构图的 NeighborLoader 使用。

## 自定义数据集

将自己的数据加载到 PyG 中：

- **快速（不需要类）**：直接创建 `Data` 对象并将列表传递给 `DataLoader`
- **可重用（适合 RAM）**：继承 `InMemoryDataset` — 覆盖 `raw_file_names`、`processed_file_names`、`download()`、`process()`
- **大型（磁盘备份）**：继承 `Dataset` — 还需覆盖 `len()` 和 `get()`
- **从 CSV**：使用 pandas 加载节点/边表，构建连续索引映射，组装成 `Data` 或 `HeteroData`
- **从 NetworkX**：`from_networkx(G)` 直接转换 NetworkX 图
- **从 scipy 稀疏**：`from_scipy_sparse_matrix(adj)` 提取 edge_index

阅读 `references/custom_datasets.md` 获取所有模式的完整示例、带编码器的 CSV 加载，以及 MovieLens 演练。

## 可解释性

PyG 提供 `torch_geometric.explain` 用于解释 GNN 预测：

```python
from torch_geometric.explain import Explainer, GNNExplainer

explainer = Explainer(
    model=model,
    algorithm=GNNExplainer(epochs=200),
    explanation_type='model',
    node_mask_type='attributes',
    edge_mask_type='object',
    model_config=dict(
        mode='multiclass_classification',
        task_level='node',
        return_type='log_probs',
    ),
)

explanation = explainer(data.x, data.edge_index, index=10)
explanation.visualize_graph()           # 重要子图
explanation.visualize_feature_importance(top_k=10)  # 特征重要性
```

可用算法：`GNNExplainer`（基于优化）、`PGExplainer`（参数化，训练）、`CaptumExplainer`（基于梯度，通过 Captum）、`AttentionExplainer`（注意力权重）。适用于同构图和异构图。

阅读 `references/explainability.md` 获取所有算法、异构解释、评估指标和 PGExplainer 训练。

## 常见陷阱

1. **edge_index 形状**：必须是 `[2, num_edges]`，不是 `[num_edges, 2]`。必要时转置。
2. **忘记激活函数**：卷积层不包含 ReLU 等 — 手动添加。
3. **异质二分图中的自环**：当源和目标节点类型不同时，不要使用 `add_self_loops=True`。改用跳跃连接。
4. **NeighborLoader 切片**：只有前 `batch.batch_size` 个节点是种子节点。相应地切片预测和标签。
5. **无向图**：如果图是无向的，在 `edge_index` 中包含两个方向的边，或使用 `T.ToUndirected()`。
6. **延迟初始化**：具有 `-1` 输入通道的模型在训练前需要一次 `torch.no_grad()` 的前向传播来初始化参数。
7. **图任务的全局池化**：使用 `global_mean_pool(x, batch)`（不是手动重塑）将节点特征聚合到图级。
8. **num_neighbors 对齐**：保持 `len(num_neighbors)` 等于 GNN 层数。跳数多于层数会浪费计算；少于层数会浪费模型容量。