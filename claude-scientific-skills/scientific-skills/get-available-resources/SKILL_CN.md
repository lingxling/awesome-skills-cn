---
name: get-available-resources
description: 此技能应在任何计算密集型科学任务开始时使用，以检测和报告可用系统资源（CPU核心、GPU、内存、磁盘空间）。它创建包含资源信息和策略建议的JSON文件，为计算方法决策提供信息，例如是否使用并行处理（joblib、multiprocessing）、核外计算（Dask、Zarr）、GPU加速（PyTorch、JAX）或内存高效策略。在运行分析、训练模型、处理大型数据集或资源约束重要的任何任务之前使用此技能。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 获取可用资源

## 概述

检测可用计算资源并为科学计算任务生成策略建议。此技能自动识别CPU能力、GPU可用性（NVIDIA CUDA、AMD ROCm、Apple Silicon Metal）、内存约束和磁盘空间，以帮助做出关于计算方法的明智决策。

## 何时使用此技能

在以下情况下主动使用此技能：

- **数据分析之前**：确定数据集是否可以加载到内存中或需要核外处理
- **模型训练之前**：检查GPU加速是否可用以及使用哪个后端
- **并行处理之前**：为joblib、multiprocessing或Dask识别最佳工作线程数
- **大型文件操作之前**：验证足够的磁盘空间和适当的存储策略
- **项目初始化时**：了解基线功能以做出架构决策

**示例场景：**
- "帮我分析这个50GB的基因组数据集" → 首先使用此技能确定是否需要Dask/Zarr
- "在这个数据上训练神经网络" → 使用此技能检测可用GPU和后端
- "并行处理10,000个文件" → 使用此技能确定最佳工作线程数
- "运行计算密集型模拟" → 使用此技能了解资源约束

## 此技能如何工作

### 资源检测

此技能运行`scripts/detect_resources.py`以自动检测：

1. **CPU信息**
   - 物理和逻辑核心数
   - 处理器架构和型号
   - CPU频率信息

2. **GPU信息**
   - NVIDIA GPU：通过nvidia-smi检测，报告VRAM、驱动版本、计算能力
   - AMD GPU：通过rocm-smi检测
   - Apple Silicon：检测具有Metal支持和统一内存的M1/M2/M3/M4芯片

3. **内存信息**
   - 总内存和可用内存
   - 当前内存使用百分比
   - 交换空间可用性

4. **磁盘空间信息**
   - 工作目录的总磁盘空间和可用磁盘空间
   - 当前使用百分比

5. **操作系统信息**
   - 操作系统类型（macOS、Linux、Windows）
   - 操作系统版本和发布
   - Python版本

### 输出格式

此技能在当前工作目录中生成`.claude_resources.json`文件，包含：

```json
{
  "timestamp": "2025-10-23T10:30:00",
  "os": {
    "system": "Darwin",
    "release": "25.0.0",
    "machine": "arm64"
  },
  "cpu": {
    "physical_cores": 8,
    "logical_cores": 8,
    "architecture": "arm64"
  },
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.5,
    "percent_used": 46.9
  },
  "disk": {
    "total_gb": 500.0,
    "available_gb": 200.0,
    "percent_used": 60.0
  },
  "gpu": {
    "nvidia_gpus": [],
    "amd_gpus": [],
    "apple_silicon": {
      "name": "Apple M2",
      "type": "Apple Silicon",
      "backend": "Metal",
      "unified_memory": true
    },
    "total_gpus": 1,
    "available_backends": ["Metal"]
  },
  "recommendations": {
    "parallel_processing": {
      "strategy": "high_parallelism",
      "suggested_workers": 6,
      "libraries": ["joblib", "multiprocessing", "dask"]
    },
    "memory_strategy": {
      "strategy": "moderate_memory",
      "libraries": ["dask", "zarr"],
      "note": "Consider chunking for datasets > 2GB"
    },
    "gpu_acceleration": {
      "available": true,
      "backends": ["Metal"],
      "suggested_libraries": ["pytorch-mps", "tensorflow-metal", "jax-metal"]
    },
    "large_data_handling": {
      "strategy": "disk_abundant",
      "note": "Sufficient space for large intermediate files"
    }
  }
}
```

### 策略建议

此技能生成上下文感知的建议：

**并行处理建议：**
- **高并行度（8+核心）**：使用Dask、joblib或multiprocessing，工作线程数 = 核心数 - 2
- **中等并行度（4-7核心）**：使用joblib或multiprocessing，工作线程数 = 核心数 - 1
- **顺序（< 4核心）**：首选顺序处理以避免开销

**内存策略建议：**
- **内存受限（< 4GB可用）**：使用Zarr、Dask或H5py进行核外处理
- **中等内存（4-16GB可用）**：对大于2GB的数据集使用Dask/Zarr
- **内存充足（> 16GB可用）**：可以直接将大多数数据集加载到内存中

**GPU加速建议：**
- **检测到NVIDIA GPU**：使用PyTorch、TensorFlow、JAX、CuPy或RAPIDS
- **检测到AMD GPU**：使用PyTorch-ROCm或TensorFlow-ROCm
- **检测到Apple Silicon**：使用带有MPS后端的PyTorch、TensorFlow-Metal或JAX-Metal
- **未检测到GPU**：使用CPU优化库

**大数据处理建议：**
- **磁盘受限（< 10GB）**：使用流式或压缩策略
- **中等磁盘（10-100GB）**：使用Zarr、H5py或Parquet格式
- **磁盘充足（> 100GB）**：可以自由创建大型中间文件

## 使用说明

### 步骤1：运行资源检测

在任何计算密集型任务开始时执行检测脚本：

```bash
python scripts/detect_resources.py
```

可选参数：
- `-o, --output <path>`：指定自定义输出路径（默认：`.claude_resources.json`）
- `-v, --verbose`：将完整资源信息打印到stdout

### 步骤2：读取并应用建议

运行检测后，读取生成的`.claude_resources.json`文件以通知计算决策：

```python
# 示例：在代码中使用建议
import json

with open('.claude_resources.json', 'r') as f:
    resources = json.load(f)

# 检查并行处理策略
if resources['recommendations']['parallel_processing']['strategy'] == 'high_parallelism':
    n_jobs = resources['recommendations']['parallel_processing']['suggested_workers']
    # 使用joblib、Dask或multiprocessing，工作线程数为n_jobs

# 检查内存策略
if resources['recommendations']['memory_strategy']['strategy'] == 'memory_constrained':
    # 使用Dask、Zarr或H5py进行核外处理
    import dask.array as da
    # 分块加载数据

# 检查GPU可用性
if resources['recommendations']['gpu_acceleration']['available']:
    backends = resources['recommendations']['gpu_acceleration']['backends']
    # 根据可用后端使用适当的GPU库
```

### 步骤3：做出明智决策

使用资源信息和建议做出战略选择：

**对于数据加载：**
```python
memory_available_gb = resources['memory']['available_gb']
dataset_size_gb = 10

if dataset_size_gb > memory_available_gb * 0.5:
    # 数据集相对于内存较大，使用Dask
    import dask.dataframe as dd
    df = dd.read_csv('large_file.csv')
else:
    # 数据集适合内存，使用pandas
    import pandas as pd
    df = pd.read_csv('large_file.csv')
```

**对于并行处理：**
```python
from joblib import Parallel, delayed

n_jobs = resources['recommendations']['parallel_processing'].get('suggested_workers', 1)

results = Parallel(n_jobs=n_jobs)(
    delayed(process_function)(item) for item in data
)
```

**对于GPU加速：**
```python
import torch

if 'CUDA' in resources['gpu']['available_backends']:
    device = torch.device('cuda')
elif 'Metal' in resources['gpu']['available_backends']:
    device = torch.device('mps')
else:
    device = torch.device('cpu')

model = model.to(device)
```

## 依赖项

检测脚本需要以下Python包：

```bash
uv pip install psutil
```

所有其他功能使用Python标准库模块（json、os、platform、subprocess、sys、pathlib）。

## 平台支持

- **macOS**：完全支持，包括Apple Silicon（M1/M2/M3/M4）GPU检测
- **Linux**：完全支持，包括NVIDIA（nvidia-smi）和AMD（rocm-smi）GPU检测
- **Windows**：完全支持，包括NVIDIA GPU检测

## 最佳实践

1. **尽早运行**：在项目开始时或主要计算任务之前执行资源检测
2. **定期重新运行**：系统资源随时间变化（内存使用、磁盘空间）
3. **扩展前检查**：在扩展并行工作线程或数据大小之前验证资源
4. **记录决策**：在项目目录中保留`.claude_resources.json`文件以记录资源感知决策
5. **配合版本控制使用**：不同机器具有不同功能；资源文件有助于保持可移植性

## 故障排除

**未检测到GPU：**
- 确保安装了GPU驱动程序（nvidia-smi、rocm-smi或Apple Silicon的system_profiler）
- 检查GPU实用程序是否在系统PATH中
- 验证GPU未被其他进程使用

**脚本执行失败：**
- 确保安装了psutil：`uv pip install psutil`
- 检查Python版本兼容性（Python 3.6+）
- 验证脚本具有执行权限：`chmod +x scripts/detect_resources.py`

**内存读数不准确：**
- 内存读数是快照；实际可用内存不断变化
- 在检测前关闭其他应用程序以获得准确的"可用"内存
- 考虑多次运行检测并平均结果
