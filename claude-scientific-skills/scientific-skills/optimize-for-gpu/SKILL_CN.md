---
name: optimize-for-gpu
description: "使用 CuPy、Numba CUDA、Warp、cuDF、cuML、cuGraph、KvikIO、cuCIM、cuxfilter、cuVS、cuSpatial 和 RAFT 对 Python 代码进行 GPU 加速。当用户提到 GPU/CUDA/NVIDIA 加速，或希望加速 NumPy、pandas、scikit-learn、scikit-image、NetworkX、GeoPandas 或 Faiss 工作负载时使用。涵盖物理模拟、可微分渲染、网格光线投射、粒子系统（DEM/SPH/流体）、向量/相似性搜索、GPUDirect Storage 文件 IO、交互式仪表板、地理空间分析、医学成像和稀疏特征值求解器。当您看到可从 GPU 加速中受益的 CPU 密集型 Python 代码（循环、大型数组、ML 管道、图分析、图像处理）时，即使没有明确请求，也使用此技能。"
metadata:
  author: K-Dense, Inc.
---

# 使用 NVIDIA 进行 Python GPU 优化

您是一位专业的 GPU 优化工程师。您的工作是帮助用户编写新的 GPU 加速代码或将他们现有的 CPU 密集型 Python 代码转换为在 NVIDIA GPU 上运行，以获得显著的速度提升 — 对于合适的工作负载，通常是 10 倍到 1000 倍的速度提升。

## 此技能适用的场景

- 用户希望加速数值/科学 Python 代码
- 用户正在处理大型数组、矩阵或数据框
- 用户提到 CUDA、GPU、NVIDIA 或并行计算
- 用户拥有处理大型数据集的 NumPy、pandas、SciPy、scikit-learn、NetworkX 或 scipy.sparse.linalg 代码
- 用户需要低级 GPU 原语（稀疏特征值求解器、设备内存管理、多 GPU 通信）
- 用户正在进行机器学习（训练、推理、超参数调整、预处理）
- 用户正在进行图分析（中心性、社区检测、最短路径、PageRank 等）
- 用户正在进行向量搜索、最近邻搜索、相似性搜索或构建 RAG 管道
- 用户拥有可 GPU 加速的 Faiss、Annoy、ScaNN 或 sklearn NearestNeighbors 代码
- 用户需要 GPU 加速的交互式仪表板、交叉过滤或大型数据集的探索性数据分析
- 用户正在进行地理空间分析（点-in-多边形、空间连接、轨迹分析、距离计算），使用 GeoPandas 或 shapely
- 用户正在进行图像处理、计算机视觉或医学成像（过滤、分割、形态学、特征检测），使用 scikit-image 或 OpenCV
- 用户正在处理全切片图像（WSI）、数字病理学、显微镜或遥感图像
- 用户正在将大型二进制数据文件加载到 GPU 内存中（numpy.fromfile → cupy，或 Python open() → GPU 数组）
- 用户需要从 S3、HTTP 或 WebHDFS 直接读取文件到 GPU 内存
- 用户提到 GPUDirect Storage (GDS) 或希望绕过 CPU 内存进行文件 IO
- 用户正在进行物理模拟（粒子、布料、流体、刚体）或可微分模拟
- 用户需要 GPU 上的网格操作（光线投射、最近点查询、有符号距离场）或几何处理
- 用户正在进行机器人学（运动学、动力学、控制），使用变换和四元数
- 用户有可被 JIT 编译为 GPU 内核的 Python 模拟循环
- 用户提到 NVIDIA Warp 或希望将可微分 GPU 模拟与 PyTorch/JAX 集成
- 用户正在进行模拟、信号处理、金融建模、生物信息学、物理学或任何计算密集型工作
- 用户希望优化现有代码，而 GPU 加速是正确的答案

## 决策框架：使用哪个库

根据用户代码的实际功能选择合适的工具。在编写任何 GPU 代码之前，请阅读相应的参考文件。

### CuPy — 用于数组/矩阵操作（NumPy 替代品）
**阅读：** `references/cupy.md`

当用户的代码主要是：
- NumPy 数组操作（元素级数学、线性代数、FFT、排序、归约）
- SciPy 操作（稀疏矩阵、信号处理、图像过滤、特殊函数）
- 任何链接 NumPy 调用的代码 — CuPy 是直接替代品

CuPy 包装了 NVIDIA 的优化库（cuBLAS、cuFFT、cuSOLVER、cuSPARSE、cuRAND），因此标准操作已经过调优。大多数 NumPy 代码只需将 `import numpy as np` 改为 `import cupy as cp` 即可工作。

**最适合：** 线性代数、FFT、数组数学、图像处理、信号处理、带数组操作的蒙特卡洛、任何 NumPy 密集型工作流。

### Numba CUDA — 用于自定义 GPU 内核
**阅读：** `references/numba.md`

当用户需要：
- 不映射到标准数组操作的自定义算法
- 对 GPU 线程、块和共享内存的精细控制
- 具有复杂逻辑的元素级操作（使用 `@vectorize(target='cuda')`）
- 具有自定义逻辑的归约操作
- 模板计算或依赖邻居的计算
- 任何需要直接使用 CUDA 编程模型的情况

Numba 将 Python 直接编译为 CUDA 内核。它提供对 GPU 线程层次结构、共享内存和同步的完全控制 — 对于无法表示为数组操作的算法至关重要。

**最适合：** 自定义内核、粒子模拟、模板代码、自定义归约、需要共享内存的算法、具有复杂元素级逻辑的任何代码。

### Warp — 用于模拟、空间计算和可微分编程
**阅读：** `references/warp.md`

当用户的代码主要是：
- 物理模拟（粒子、布料、流体、刚体、DEM、SPH）
- 几何处理（网格操作、光线投射、有符号距离场、Marching Cubes）
- 机器人学（运动学、动力学、控制，使用变换和四元数）
- 用于 ML 训练的可微分模拟（与 PyTorch/JAX 自动微分集成）
- 任何需要被 JIT 编译到 GPU 的 Python 模拟循环
- 使用网格、体积（NanoVDB）、哈希网格或 BVH 查询的空间计算

Warp 将 `@wp.kernel` Python 函数 JIT 编译为 CUDA，具有用于空间计算的内置类型（vec3、mat33、quat、transform）和用于几何查询的原语（Mesh、Volume、HashGrid、BVH）。所有内核都自动可微分。

**最适合：** 物理模拟、网格光线投射、粒子系统、可微分渲染、机器人运动学、SDF 操作、任何结合空间数据结构和 GPU 计算的工作负载。

**Warp vs Numba：** 两者都将 Python 编译为 CUDA，但 Warp 提供更高级的空间类型（vec3、quat、Mesh、Volume）和自动微分，而 Numba 提供原始 CUDA 控制（共享内存、块/线程管理、原子操作）。对于模拟/几何，使用 Warp；对于通用自定义内核，使用 Numba。

### cuDF — 用于数据框操作（pandas 替代品）
**阅读：** `references/cudf.md`

当用户的代码主要是：
- pandas DataFrame 操作（过滤、分组、连接、聚合）
- CSV/Parquet/JSON 读取和处理
- 大型数据集的 ETL 管道或数据处理
- 任何适合 GPU 内存的 pandas 密集型工作流

cuDF 的 `cudf.pandas` 加速模式可以零代码更改加速现有 pandas 代码。为获得最大性能，请使用原生 cuDF API。

**最适合：** 数据处理、ETL、分组/聚合、连接、字符串处理（数据框）、时间序列（表格数据）。

### cuML — 用于机器学习（scikit-learn 替代品）
**阅读：** `references/cuml.md`

当用户的代码主要是：
- scikit-learn 估计器（分类、回归、聚类、降维）
- ML 预处理（缩放、编码、插补、特征提取）
- 超参数调整或交叉验证
- 树模型推理（XGBoost、LightGBM、通过 FIL 的 sklearn Random Forest）
- 大型数据集上的 UMAP、t-SNE、HDBSCAN 或 KNN

cuML 的 `cuml.accel` 加速模式可以零代码更改加速现有 sklearn 代码。为获得最大性能，请使用原生 cuML API。速度提升从简单线性模型的 2-10 倍到复杂算法如 HDBSCAN 和 KNN 的 60-600 倍不等。

**最适合：** 分类、回归、聚类、降维、预处理管道、模型推理、任何 scikit-learn 密集型工作流。

### cuGraph — 用于图分析（NetworkX 替代品）
**阅读：** `references/cugraph.md`

当用户的代码主要是：
- NetworkX 图算法（中心性、社区检测、最短路径、PageRank）
- 大型网络的图构建和分析
- 社交网络分析、知识图谱或推荐系统
- 任何具有 10K+ 边的网络上的图算法

cuGraph 的 `nx-cugraph` 后端可以通过环境变量零代码更改加速现有 NetworkX 代码。为获得最大性能，请使用带有 cuDF DataFrame 的原生 cuGraph API。速度提升从小型图的 10 倍到大型图（数百万边）的 500 倍以上。

**最适合：** PageRank、介数中心性、社区检测（Louvain、Leiden）、BFS/SSSP、连通分量、链接预测、图神经网络采样、任何 NetworkX 密集型工作流。

### KvikIO — 用于高性能 GPU 文件 IO
**阅读：** `references/kvikio.md`

当用户的代码主要是：
- 将大型二进制数据文件直接加载到 GPU 内存
- 将 GPU 数组写入磁盘而无需先复制到主机
- 从远程存储（S3、HTTP、WebHDFS）读取数据到 GPU 内存
- 在 GPU 上处理 Zarr 数组（GDSStore 后端）
- 任何文件 IO 是存储和 GPU 之间瓶颈的管道

KvikIO 提供 NVIDIA cuFile 的 Python 绑定，启用 GPUDirect Storage (GDS) — 数据直接在 NVMe 存储和 GPU 内存之间流动，完全绕过 CPU 内存。当 GDS 不可用时，它会透明地回退到 POSIX IO。它无缝处理主机和设备数据。

**最适合：** 加载二进制数据到 GPU、将 GPU 数组保存到磁盘、直接从 S3/HTTP 读取到 GPU、GPU 上的 Zarr 数组、替换 `numpy.fromfile()` → `cupy` 模式、任何 IO 密集型 GPU 管道，其中数据通过 CPU 内存的分阶段是瓶颈。

**注意：** 对于表格格式（CSV、Parquet、JSON），请使用 cuDF 的内置读取器 — 它们针对这些格式进行了优化。KvikIO 适用于原始二进制数据和远程文件访问。

### cuxfilter — 用于 GPU 加速的交互式仪表板
**阅读：** `references/cuxfilter.md`

当用户需要：
- 大型数据集（数百万行）上的交互式交叉过滤仪表板
- 带有相互过滤的链接图表的探索性数据分析
- GPU 加速的可视化，包括散点图、条形图、热力图、 choropleths 或图可视化
- 从 Jupyter 笔记本快速原型仪表板，代码最少
- 可视化 cuDF、cuML 或 cuGraph 管道的结果

cuxfilter 利用 cuDF 在 GPU 上进行所有数据操作 — 过滤、分组和聚合完全在 GPU 上进行，只有渲染结果发送到浏览器。它集成了 Bokeh、Datashader（用于数百万点）、Deck.gl（用于地图）和 Panel 小部件。

**最适合：** 交互式数据探索仪表板、多图表交叉过滤、地理空间可视化、图可视化、可视化 RAPIDS 管道结果、任何用户需要交互式探索和过滤大型 GPU 驻留数据集的场景。

### cuCIM — 用于图像处理（scikit-image 替代品）
**阅读：** `references/cucim.md`

当用户的代码主要是：
- scikit-image 操作（过滤、形态学、分割、特征检测、颜色转换）
- 深度学习的图像预处理管道（调整大小、标准化、增强）
- 数字病理学（全切片图像读取、H&E 染色标准化、细胞计数）
- 显微镜、遥感或医学成像工作流
- 任何处理 512x512 或更大图像的 scikit-image 密集型管道

cuCIM 的 `cucim.skimage` 模块镜像 scikit-image 的 API，提供 200+ GPU 加速函数。它还提供高性能 WSI 读取器 (`CuImage`)，比 OpenSlide 快 5-6 倍。所有函数都在 CuPy 数组上工作 — 零复制，全在 GPU 上。

**最适合：** 过滤（高斯、Sobel、Frangi）、形态学、阈值化、连通分量标记、区域属性、颜色空间转换、图像配准、去噪、全切片图像处理、DL 预处理管道。

### cuVS — 用于向量搜索（Faiss/Annoy 替代品）
**阅读：** `references/cuvs.md`

当用户的代码主要是：
- 高维向量的近似最近邻 (ANN) 搜索
- 用于 RAG、推荐系统或语义检索的相似性搜索
- 用于聚类或可视化的 k-NN 图构建
- 任何 Faiss、Annoy、ScaNN 或 sklearn NearestNeighbors 在大型嵌入数据集上的工作负载

cuVS 提供 GPU 加速的 ANN 索引类型（CAGRA、IVF-Flat、IVF-PQ、暴力）以及用于从 GPU 构建的索引进行 CPU 服务的 HNSW。它为 Faiss、Milvus 和 Lucene 的 GPU 后端提供支持。对于大多数用例，从 CAGRA 开始 — 它是最快的 GPU 原生算法。

**最适合：** 嵌入搜索、RAG 检索、推荐系统、图像/文本/音频相似性搜索、k-NN 图构建、任何 10K+ 向量的最近邻工作负载。

### cuSpatial — 用于地理空间分析（GeoPandas 替代品）
**阅读：** `references/cuspatial.md`

当用户的代码主要是：
- GeoPandas 空间操作（点-in-多边形、空间连接、距离计算）
- 轨迹分析（分组 GPS 轨迹、计算速度/距离）
- 用于大规模空间连接的空间索引（四叉树）
- 经纬度坐标上的 Haversine 距离计算
- 任何 GeoPandas/shapely 密集型大型地理空间数据集工作流

cuSpatial 提供与 GeoPandas 兼容的 GPU 加速 `GeoSeries` 和 `GeoDataFrame` 类型，以及空间连接、距离和轨迹函数。使用 `cuspatial.from_geopandas()` 从 GeoPandas 转换。

**最适合：** 点-in-多边形测试、数百万点/多边形上的空间连接、Haversine 和欧几里得距离计算、轨迹重建和分析、任何 GeoPandas 密集型地理空间工作流。

### RAFT (pylibraft) — 用于低级 GPU 原语和多 GPU
**阅读：** `references/raft.md`

当用户需要：
- GPU 加速的稀疏特征值问题（`scipy.sparse.linalg.eigsh` 替代品）
- 低级 GPU 设备内存管理 (`device_ndarray`)
- 随机图生成（用于基准测试的 R-MAT 模型）
- 多节点多 GPU 通信基础设施（通过 `raft-dask`）
- 构建高级 RAPIDS 库的基础块

RAFT 提供 cuML 和 cuGraph 构建的基础原语。大多数用户应该首先使用那些高级库 — 当您需要它公开的特定原语（稀疏特征值求解器、设备内存、图生成）或通过 Dask 进行多 GPU 通信时，直接使用 RAFT。

**最适合：** 稀疏特征值分解（谱方法、图分区）、R-MAT 图生成、低级设备内存管理、多 GPU 编排。

**注意：** 向量搜索算法（k-NN、IVFPQ、CAGRA）已迁移到 cuVS — 不要使用 RAFT 进行向量搜索。

### 组合库

许多实际工作负载受益于一起使用多个库。它们通过 CUDA 数组接口互操作 — CuPy、Numba、Warp、cuDF、cuML、cuGraph、cuVS、cuCIM、cuSpatial、KvikIO、PyTorch、JAX 和其他 GPU 库之间的零复制数据共享。

常见组合：
- **cuDF + cuML**：使用 cuDF 加载和预处理数据，使用 cuML 训练/预测 — 完整的 RAPIDS 管道
- **cuDF + cuGraph**：从 cuDF 边列表构建图，使用 cuGraph 运行图分析
- **cuGraph + cuML**：使用 cuGraph 提取图特征，将其输入 cuML 进行 ML
- **cuML + cuVS**：使用 cuML 训练嵌入模型，使用 cuVS 索引和搜索嵌入
- **cuDF + CuPy**：使用 cuDF 加载和过滤数据，然后使用 CuPy 进行数值分析
- **CuPy + cuVS**：使用 CuPy 操作生成嵌入，构建 cuVS 搜索索引 — 零复制
- **Warp + PyTorch**：在 Warp 中进行可微分模拟，将梯度反向传播到 PyTorch 训练循环
- **Warp + CuPy**：使用 CuPy 进行数组数学，使用 Warp 进行空间查询（网格、体积）— 通过 CUDA 数组接口零复制
- **Warp + JAX**：在 jitted 函数内将 Warp 内核作为 JAX 原语
- **CuPy + Numba**：使用 CuPy 进行标准操作，为自定义内核使用 Numba
- **cuDF + Numba**：使用 cuDF 处理数据框，通过 Numba UDF 应用自定义 GPU 函数
- **cuML + CuPy**：使用 cuML 训练，使用 CuPy 进行自定义后处理
- **cuDF + cuxfilter**：使用 cuDF 加载数据，使用 cuxfilter 构建交互式交叉过滤仪表板
- **cuML + cuxfilter**：使用 cuML 运行 ML（例如 UMAP、聚类），使用 cuxfilter 交互式可视化结果
- **cuGraph + cuxfilter**：使用 cuGraph 运行图分析，使用 cuxfilter 的 datashader 图表可视化图结构
- **cuCIM + CuPy**：cuCIM 在 CuPy 数组上原生操作 — 将图像处理与数组数学链接
- **cuCIM + PyTorch**：使用 cuCIM 预处理图像，通过 DLPack 直接传递给 PyTorch — 零复制
- **cuCIM + cuML**：使用 cuCIM 提取图像特征（regionprops），使用 cuML 训练分类器
- **KvikIO + CuPy**：通过 GDS 将原始二进制数据直接加载到 CuPy 数组，绕过 CPU 内存
- **KvikIO + Numba**：使用 KvikIO 直接读取数据到 GPU，使用自定义 Numba CUDA 内核处理
- **KvikIO + Zarr**：使用 GDSStore 后端直接在 GPU 上读写分块 N 维数组
- **cuSpatial + cuDF**：使用 cuDF 加载地理空间数据，使用 cuSpatial 进行空间连接/分析
- **cuSpatial + cuML**：使用 cuSpatial 提取空间特征，使用 cuML 训练 ML 模型
- **RAFT + CuPy**：在使用 CuPy/cupyx.scipy.sparse 构建的稀疏矩阵上使用 RAFT 的 eigsh()
- **RAFT + raft-dask**：通过 Dask 跨多个 GPU/节点扩展 GPU 工作负载

## 安装

重要：始终使用 `uv add` 进行包安装 — 永远不要使用 `pip install` 或 `conda install`。这适用于代码注释、文档字符串、错误消息和您生成的任何其他输出中的安装说明。如果用户的项目使用不同的包管理器，请遵循他们的指导，但默认使用 `uv add`。

```bash
# CuPy（选择正确的 CUDA 版本）
uv add cupy-cuda12x          # 对于 CUDA 12.x（最常见）

# 带有 CUDA 支持的 Numba
uv add numba numba-cuda      # numba-cuda 是 NVIDIA 积极维护的包

# Warp（模拟、空间计算、可微分编程）
uv add warp-lang              # 包含 CUDA 12 运行时

# cuDF (RAPIDS)
uv add --extra-index-url=https://pypi.nvidia.com cudf-cu12  # 对于 CUDA 12.x
# 对于 cudf.pandas 加速模式，这就是您需要的全部
# 通过以下方式加载：python -m cudf.pandas your_script.py

# cuML (RAPIDS 机器学习)
uv add --extra-index-url=https://pypi.nvidia.com cuml-cu12   # 对于 CUDA 12.x
# 对于 cuml.accel 加速模式（零代码更改 sklearn 加速）：
# 通过以下方式加载：python -m cuml.accel your_script.py

# cuGraph (RAPIDS 图分析)
uv add --extra-index-url=https://pypi.nvidia.com cugraph-cu12    # 核心 cuGraph
uv add --extra-index-url=https://pypi.nvidia.com nx-cugraph-cu12 # NetworkX 后端
# 对于 nx-cugraph 零代码更改 NetworkX 加速：
# NX_CUGRAPH_AUTOCONFIG=True python your_script.py

# KvikIO（高性能 GPU 文件 IO）
uv add kvikio-cu12               # 对于 CUDA 12.x
# 可选：uv add zarr          # 对于 Zarr GPU 后端支持

# cuxfilter（GPU 加速的交互式仪表板）
uv add --extra-index-url=https://pypi.nvidia.com cuxfilter-cu12   # 对于 CUDA 12.x
# 依赖于 cuDF — 自动安装它

# cuCIM（RAPIDS 图像处理 — GPU 上的 scikit-image）
uv add --extra-index-url=https://pypi.nvidia.com cucim-cu12    # 对于 CUDA 12.x

# cuVS (RAPIDS 向量搜索)
uv add --extra-index-url=https://pypi.nvidia.com cuvs-cu12   # 对于 CUDA 12.x

# cuSpatial (RAPIDS 地理空间)
uv add --extra-index-url=https://pypi.nvidia.com cuspatial-cu12   # 对于 CUDA 12.x

# RAFT（低级 GPU 原语）
uv add --extra-index-url=https://pypi.nvidia.com pylibraft-cu12   # 核心原语
uv add --extra-index-url=https://pypi.nvidia.com raft-dask-cu12   # 多 GPU 支持（可选）
```

安装后检查 CUDA 可用性：

```python
# CuPy
import cupy as cp
print(cp.cuda.runtime.getDeviceCount())  # 应 >= 1

# Numba
from numba import cuda
print(cuda.is_available())               # 应 True
print(cuda.detect())                     # 显示 GPU 详细信息

# cuDF
import cudf
print(cudf.Series([1, 2, 3]))           # 应打印 GPU 系列

# cuML
import cuml
print(cuml.__version__)                  # 应打印版本

# cuGraph
import cugraph
print(cugraph.__version__)               # 应打印版本

# Warp
import warp as wp
wp.init()                                # 应打印设备信息

# KvikIO
import kvikio
import kvikio.cufile_driver
print(kvikio.cufile_driver.get("is_gds_available"))  # 如果 GDS 设置正确则为 True

# cuxfilter
import cuxfilter
print(cuxfilter.__version__)             # 应打印版本

# cuVS
from cuvs.neighbors import cagra
import cupy as cp
dataset = cp.random.rand(1000, 128, dtype=cp.float32)
index = cagra.build(cagra.IndexParams(), dataset)
print("cuVS working")                    # 应打印确认

# cuSpatial
import cuspatial
from shapely.geometry import Point
gs = cuspatial.GeoSeries([Point(0, 0)])
print("cuSpatial working")              # 应打印确认

# RAFT (pylibraft)
from pylibraft.common import DeviceResources
handle = DeviceResources()
handle.sync()
print("pylibraft is working")
```

## 优化工作流程

帮助用户优化代码时，遵循以下过程：

### 1. 首先分析
在优化之前，了解时间实际花在哪里：
```python
import time
# 或使用 cProfile、line_profiler 或 py-spy 进行详细分析
```
不要猜测 — 测量。瓶颈可能不在用户认为的地方。

### 2. 评估 GPU 适用性
并非所有代码都受益于 GPU 加速。GPU 在以下情况下表现出色：
- **数据并行度高**：相同操作应用于数千/数百万个元素
- **计算强度高**：每个访问的内存字节有许多 FLOP
- **数据足够大**：GPU 开销意味着小数组（< ~10K 元素）在 GPU 上可能更慢
- **内存适合**：数据必须适合 GPU 内存（通常为 8-80 GB）

GPU 不适合的情况：
- 数据很小（< 10K 元素）
- 算法本质上是顺序的，步骤之间存在数据依赖
- 代码受 I/O 限制（磁盘、网络），而非计算限制 — 尽管当 IO 为 GPU 计算提供数据时，带有 GPUDirect Storage 的 KvikIO 可以提供帮助
- 许多小的、异构操作（内核启动开销占主导）

### 3. 从简单开始，然后优化
1. **首先尝试直接替代品**。NumPy 的 CuPy，pandas 的 cudf.pandas，sklearn 的 cuml.accel，NetworkX 的 nx-cugraph。这 alone 通常会带来 5-50 倍的速度提升。
2. **最小化主机-设备传输**。将数据保持在 GPU 上。每次通过 PCI-e 的传输都很昂贵（~12 GB/s），而 GPU 内存带宽（~900 GB/s+）则快得多。
3. **批处理操作**。较少的大型 GPU 操作优于许多小型操作。
4. **仅在需要时编写自定义内核**。CuPy 和 cuDF 使用 NVIDIA 的手工调优库。自定义 Numba 内核应保留给没有库等效项的操作。
5. **分析 GPU 版本**。使用 `nvprof`、`nsys` 或 CuPy 的内置基准测试。

### 4. 内存管理原则
这些适用于所有库：
- **预分配输出数组**，而不是在循环中创建新数组
- **重用 GPU 内存** — 使用内存池（CuPy 内置）
- **使用固定（页面锁定）主机内存**以加快 CPU-GPU 传输
- **避免不必要的复制** — 尽可能使用原地操作
- **流式操作**以重叠计算和数据传输

### 5. 需要注意的常见陷阱
- **隐式 CPU 回退**：某些操作会静默回退到 CPU。注意警告。
- **同步开销**：GPU 操作是异步的。调用 `.get()` 或 `cp.asnumpy()` 会强制同步。
- **dtype 不匹配**：当精度允许时，使用 `float32` 而不是 `float64` — GPU float32 吞吐量是 2x-32x 更高。
- **小型内核启动**：每个内核启动有 ~5-20us 开销。尽可能融合操作。

## 代码转换模式

转换现有 CPU 代码时，应用这些模式：

### NumPy 到 CuPy
```python
# 之前（CPU）
import numpy as np
a = np.random.rand(10_000_000)
b = np.fft.fft(a)
c = np.sort(b.real)

# 之后（GPU）— 通常只需更改导入
import cupy as cp
a = cp.random.rand(10_000_000)
b = cp.fft.fft(a)
c = cp.sort(b.real)
```

### pandas 到 cuDF
```python
# 之前（CPU）
import pandas as pd
df = pd.read_parquet("large_data.parquet")
result = df.groupby("category")["value"].mean()

# 之后（GPU）— 更改导入
import cudf
df = cudf.read_parquet("large_data.parquet")
result = df.groupby("category")["value"].mean()

# 或零代码更改：python -m cudf.pandas your_script.py
```

### 自定义循环到 Numba CUDA 内核
```python
# 之前（CPU）— 慢 Python 循环
def process(data, out):
    for i in range(len(data)):
        out[i] = math.sin(data[i]) * math.exp(-data[i])

# 之后（GPU）— Numba 内核
from numba import cuda
import math

@cuda.jit
def process(data, out):
    i = cuda.grid(1)
    if i < data.size:
        out[i] = math.sin(data[i]) * math.exp(-data[i])

threads = 256
blocks = (len(data) + threads - 1) // threads
process[blocks, threads](d_data, d_out)
```

### NetworkX 到 cuGraph
```python
# 之前（CPU）
import networkx as nx
G = nx.read_edgelist("edges.csv", delimiter=",", nodetype=int)
pr = nx.pagerank(G)
bc = nx.betweenness_centrality(G)

# 之后（GPU）— 直接 cuGraph API
import cugraph
import cudf
edges = cudf.read_csv("edges.csv", names=["src", "dst"], dtype=["int32", "int32"])
G = cugraph.Graph()
G.from_cudf_edgelist(edges, source="src", destination="dst")
pr = cugraph.pagerank(G)
bc = cugraph.betweenness_centrality(G)

# 或零代码更改：NX_CUGRAPH_AUTOCONFIG=True python your_script.py
```

### scikit-learn 到 cuML
```python
# 之前（CPU）
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 之后（GPU）— 更改导入
from cuml.ensemble import RandomForestClassifier
from cuml.preprocessing import StandardScaler
from cuml.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 或零代码更改：python -m cuml.accel your_script.py
```

### 模拟循环到 Warp 内核
```python
# 之前（CPU）— 慢 Python 粒子循环
import numpy as np

def integrate(positions, velocities, forces, dt):
    for i in range(len(positions)):
        velocities[i] += forces[i] * dt
        positions[i] += velocities[i] * dt

# 之后（GPU）— Warp 内核，JIT 编译为 CUDA
import warp as wp

@wp.kernel
def integrate(positions: wp.array(dtype=wp.vec3),
              velocities: wp.array(dtype=wp.vec3),
              forces: wp.array(dtype=wp.vec3),
              dt: float):
    tid = wp.tid()
    velocities[tid] = velocities[tid] + forces[tid] * dt
    positions[tid] = positions[tid] + velocities[tid] * dt

wp.launch(integrate, dim=num_particles,
          inputs=[positions, velocities, forces, 0.01], device="cuda")
```

### 文件 IO 到 GPU（使用 KvikIO）
```python
# 之前 — CPU 分阶段（磁盘 → CPU → GPU）
import numpy as np
import cupy as cp

data = np.fromfile("data.bin", dtype=np.float32)
gpu_data = cp.asarray(data)  # 通过 CPU 内存的额外复制

# 之后 — 直接到 GPU（磁盘 → GPU 通过 GDS）
import cupy as cp
import kvikio

gpu_data = cp.empty(1_000_000, dtype=cp.float32)
with kvikio.CuFile("data.bin", "r") as f:
    f.read(gpu_data)  # 通过 GPUDirect Storage 绕过 CPU 内存

# 直接从 S3 读取到 GPU
with kvikio.RemoteFile.open_s3_url("s3://bucket/data.bin") as f:
    buf = cp.empty(f.nbytes() // 4, dtype=cp.float32)
    f.read(buf)
```

### 使用 cuxfilter 的 GPU 加速仪表板
```python
# 之前 — 静态 matplotlib/seaborn 图表，无交互性
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("large_dataset.parquet")
fig, axes = plt.subplots(1, 2)
df.plot.scatter(x="feature1", y="feature2", ax=axes[0])
df["category"].value_counts().plot.bar(ax=axes[1])
plt.show()

# 之后（GPU）— 交互式交叉过滤仪表板
import cudf
import cuxfilter

df = cudf.read_parquet("large_dataset.parquet")
cux_df = cuxfilter.DataFrame.from_dataframe(df)

scatter = cuxfilter.charts.scatter(x="feature1", y="feature2", pixel_shade_type="linear")
bar = cuxfilter.charts.bar("category")
slider = cuxfilter.charts.range_slider("value_col")

d = cux_df.dashboard(
    [scatter, bar],
    sidebar=[slider],
    layout=cuxfilter.layouts.feature_and_base,
    theme=cuxfilter.themes.rapids_dark,
    title="交互式探索器",
)
d.app()  # 或 d.show() 用于独立 web 应用
```

### scikit-image 到 cuCIM
```python
# 之前（CPU）
from skimage.filters import gaussian, sobel, threshold_otsu
from skimage.morphology import binary_opening, disk
from skimage.measure import label, regionprops_table
import numpy as np

blurred = gaussian(image, sigma=3)
binary = blurred > threshold_otsu(blurred)
cleaned = binary_opening(binary, footprint=disk(3))
labels = label(cleaned)
props = regionprops_table(labels, image, properties=['area', 'centroid'])

# 之后（GPU）— 更改导入，用 cp.asarray 包装输入
from cucim.skimage.filters import gaussian, sobel, threshold_otsu
from cucim.skimage.morphology import binary_opening, disk
from cucim.skimage.measure import label, regionprops_table
import cupy as cp

image_gpu = cp.asarray(image)  # 只传输一次
blurred = gaussian(image_gpu, sigma=3)
binary = blurred > threshold_otsu(blurred)
cleaned = binary_opening(binary, footprint=disk(3))
labels = label(cleaned)
props = regionprops_table(labels, image_gpu, properties=['area', 'centroid'])
```

### GeoPandas 到 cuSpatial
```python
# 之前（CPU）
import geopandas as gpd
from shapely.geometry import Point

points = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y in coords], crs="EPSG:4326")
polygons = gpd.read_file("regions.geojson")
joined = gpd.sjoin(points, polygons, predicate="within")

# 之后（GPU）— 转换并使用 cuSpatial
import cuspatial
import cudf

points_cu = cuspatial.from_geopandas(points)
polygons_cu = cuspatial.from_geopandas(polygons)
joined = cuspatial.point_in_polygon(
    points_cu.geometry.x, points_cu.geometry.y,
    polygons_cu.geometry
)
```

### Faiss/Annoy 到 cuVS
```python
# 之前（CPU）— Faiss
import faiss
import numpy as np

embeddings = np.random.rand(1_000_000, 128).astype(np.float32)
index = faiss.IndexFlatL2(128)
index.add(embeddings)
distances, neighbors = index.search(queries, k=10)

# 之后（GPU）— cuVS CAGRA（快几个数量级）
import cupy as cp
from cuvs.neighbors import cagra

embeddings = cp.random.rand(1_000_000, 128, dtype=cp.float32)
index = cagra.build(cagra.IndexParams(), embeddings)
distances, neighbors = cagra.search(cagra.SearchParams(), index, queries, k=10)
```

### scipy.sparse.linalg 到 RAFT
```python
# 之前（CPU）
import numpy as np
from scipy.sparse import random as sparse_random
from scipy.sparse.linalg import eigsh

A = sparse_random(10000, 10000, density=0.01, format="csr", dtype=np.float32)
A = A + A.T  # 使对称
eigenvalues, eigenvectors = eigsh(A, k=10, which="LM")

# 之后（GPU）— RAFT 稀疏特征值求解器
import cupy as cp
import cupyx.scipy.sparse as sp_gpu
from pylibraft.sparse.linalg import eigsh as gpu_eigsh

A_gpu = sp_gpu.csr_matrix(A)  # 传输到 GPU
eigenvalues, eigenvectors = gpu_eigsh(A_gpu, k=10, which="LM")
```

## 重要注意事项

- 始终处理无 GPU 可用的情况 — 提供 CPU 回退或明确的错误消息
- 测试与 CPU 结果的数值正确性（由于操作顺序，GPU 浮点可能略有不同）
- GPU 内存有限 — 对于大于 GPU 内存的数据集，考虑分块或使用 RAPIDS Dask 进行多 GPU
- CUDA 数组接口允许 CuPy、Numba、Warp、cuDF、cuML、cuGraph、cuVS、cuSpatial、KvikIO、PyTorch 和 JAX 数组在 GPU 上零复制共享

## 参考文件

在编写任何 GPU 优化代码之前，请阅读相关参考文件：

| 文件 | 何时阅读 |
|------|-------------|
| `references/cupy.md` | 用户有 NumPy/SciPy 代码，或需要在 GPU 上进行数组操作 |
| `references/numba.md` | 用户需要自定义 CUDA 内核、精细的 GPU 控制或 GPU ufuncs |
| `references/cudf.md` | 用户有 pandas 代码，或需要在 GPU 上进行数据框操作 |
| `references/cuml.md` | 用户有 scikit-learn 代码，或需要在 GPU 上进行 ML 训练/推理/预处理 |
| `references/cugraph.md` | 用户有 NetworkX 代码，或需要在 GPU 上进行图分析 |
| `references/warp.md` | 用户需要 GPU 模拟、空间计算、网格/体积查询、可微分编程或机器人学 |
| `references/kvikio.md` | 用户需要高性能文件 IO 到/从 GPU、GPUDirect Storage、读取 S3/HTTP 到 GPU，或 GPU 上的 Zarr |
| `references/cuxfilter.md` | 用户想要 GPU 加速的交互式仪表板、交叉过滤或 EDA 可视化 |
| `references/cucim.md` | 用户有 scikit-image 代码，或需要在 GPU 上进行图像处理、数字病理学或 WSI 读取 |
| `references/cuvs.md` | 用户需要向量搜索、最近邻、相似性搜索或 RAG 检索在 GPU 上 |
| `references/cuspatial.md` | 用户有 GeoPandas/shapely 代码，或需要在 GPU 上进行空间连接、距离计算或轨迹分析 |
| `references/raft.md` | 用户需要稀疏特征值求解器、设备内存管理或多 GPU 原语 |

在编写代码之前阅读特定参考 — 它们包含针对每个库的详细 API 模式、优化技术和陷阱。