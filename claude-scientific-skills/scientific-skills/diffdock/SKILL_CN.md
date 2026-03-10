---
name: diffdock
description: 基于扩散的分子对接。从 PDB/SMILES 预测蛋白质-配体结合位姿、置信度评分、虚拟筛选，用于基于结构的药物设计。不适用于亲和力预测。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# DiffDock：使用扩散模型的分子对接

## 概述

DiffDock 是一个基于扩散的深度学习工具，用于分子对接，可预测小分子配体与蛋白质靶点的 3D 结合位姿。它代表了计算对接的最先进技术，对于基于结构的药物发现和化学生物学至关重要。

**核心能力：**
- 使用深度学习以高精度预测配体结合位姿
- 支持蛋白质结构（PDB 文件）或序列（通过 ESMFold）
- 处理单个复合物或批处理虚拟筛选活动
- 生成置信度评分以评估预测可靠性
- 处理多样化的配体输入（SMILES、SDF、MOL2）

**关键区别：**DiffDock 预测**结合位姿**（3D 结构）和**置信度**（预测确定性），而不是结合亲和力（ΔG、Kd）。始终结合评分函数（GNINA、MM/GBSA）进行亲和力评估。

## 何时使用此技能

此技能应在以下情况下使用：

- "对接这个配体到蛋白质"或"预测结合位姿"
- "运行分子对接"或"执行蛋白质-配体对接"
- "虚拟筛选"或"筛选化合物库"
- "这个分子在哪里结合？"或"预测结合位点"
- 基于结构的药物设计或先导优化任务
- 涉及 PDB 文件 + SMILES 字符串或配体结构的任务
- 批处理多个蛋白质-配体对

## 安装和环境设置

### 检查环境状态

在继续 DiffDock 任务之前，验证环境设置：

```bash
# 使用提供的设置检查器
python scripts/setup_check.py
```

此脚本验证 Python 版本、带有 CUDA 的 PyTorch、PyTorch Geometric、RDKit、ESM 和其他依赖项。

### 安装选项

**选项 1：Conda（推荐）**
```bash
git clone https://github.com/gcorso/DiffDock.git
cd DiffDock
conda env create --file environment.yml
conda activate diffdock
```

**选项 2：Docker**
```bash
docker pull rbgcsail/diffdock
docker run -it --gpus all --entrypoint /bin/bash rbgcsail/diffdock
micromamba activate diffdock
```

**重要说明：**
- 强烈推荐 GPU（与 CPU 相比，速度提升 10-100 倍）
- 首次运行预计算 SO(2)/SO(3) 查找表（约 2-5 分钟）
- 模型检查点（约 500MB）如果不存在会自动下载

## 核心工作流

### 工作流 1：单个蛋白质-配体对接

**用例**：将一个配体对接到一个蛋白质靶点

**输入要求：**
- 蛋白质：PDB 文件或氨基酸序列
- 配体：SMILES 字符串或结构文件（SDF/MOL2）

**命令：**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)Oc1ccccc1C(=O)O" \
  --out_dir results/single_docking/
```

**替代方案（蛋白质序列）：**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_sequence "MSKGEELFTGVVPILVELDGDVNGHKF..." \
  --ligand ligand.sdf \
  --out_dir results/sequence_docking/
```

**输出结构：**
```
results/single_docking/
├── rank_1.sdf          # 排名第一的位姿
├── rank_2.sdf          # 排名第二的位姿
├── ...
├── rank_10.sdf         # 第 10 个位姿（默认：10 个样本）
└── confidence_scores.txt
```

### 工作流 2：批处理多个复合物

**用例**：将多个配体对接到蛋白质、虚拟筛选活动

**步骤 1：准备批处理 CSV**

使用提供的脚本创建或验证批处理输入：

```bash
# 创建模板
python scripts/prepare_batch_csv.py --create --output batch_input.csv

# 验证现有 CSV
python scripts/prepare_batch_csv.py my_input.csv --validate
```

**CSV 格式：**
```csv
complex_name,protein_path,ligand_description,protein_sequence
complex1,protein1.pdb,CC(=O)Oc1ccccc1C(=O)O,
complex2,,COc1ccc(C#N)cc1,MSKGEELFT...
complex3,protein3.pdb,ligand3.sdf,
```

**必需列：**
- `complex_name`：唯一标识符
- `protein_path`：PDB 文件路径（如果使用序列则留空）
- `ligand_description`：SMILES 字符串或配体文件路径
- `protein_sequence`：氨基酸序列（如果使用 PDB 则留空）

**步骤 2：运行批处理对接**

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv batch_input.csv \
  --out_dir results/batch/ \
  --batch_size 10
```

**对于大型虚拟筛选（>100 个化合物）：**

预计算蛋白质嵌入以加快处理速度：

```bash
# 预计算嵌入
python datasets/esm_embedding_preparation.py \
  --protein_ligand_csv screening_input.csv \
  --out_file protein_embeddings.pt

# 使用预计算的嵌入运行
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv screening_input.csv \
  --esm_embeddings_path protein_embeddings.pt \
  --out_dir results/screening/
```

### 工作流 3：分析结果

对接完成后，分析置信度评分并对预测进行排名：

```bash
# 分析所有结果
python scripts/analyze_results.py results/batch/

# 显示每个复合物的前 5 个
python scripts/analyze_results.py results/batch/ --top 5

# 按置信度阈值过滤
python scripts/analyze_results.py results/batch/ --threshold 0.0

# 导出到 CSV
python scripts/analyze_results.py results/batch/ --export summary.csv

# 显示所有复合物的前 20 个预测
python scripts/analyze_results.py results/batch/ --best 20
```

分析脚本：
- 解析所有预测的置信度评分
- 分类为高（>0）、中（-1.5 到 0）、低（<-1.5）
- 在复合物内和跨复合物对预测进行排名
- 生成统计摘要
- 导出到 CSV 以进行下游分析

## 置信度评分解读

**理解评分：**

| 评分范围 | 置信度水平 | 解读 |
|------------|--------------|------|
| **> 0** | 高 | 强预测，可能准确 |
| **-1.5 到 0** | 中 | 合理预测，仔细验证 |
| **< -1.5** | 低 | 不确定预测，需要验证 |

**关键说明：**
1. **置信度 ≠ 亲和力**：高置信度意味着模型对结构的确定性，而不是强结合
2. **上下文很重要**：根据以下调整预期：
   - 大配体（>500 Da）：预期置信度较低
   - 多蛋白质链：可能会降低置信度
   - 新颖蛋白质家族：可能表现不佳
3. **多个样本**：查看前 3-5 个预测，寻找一致性

**有关详细指导**：使用 Read 工具阅读 `references/confidence_and_limitations.md`

## 参数自定义

### 使用自定义配置

为特定用例创建自定义配置：

```bash
# 复制模板
cp assets/custom_inference_config.yaml my_config.yaml

# 编辑参数（参见模板中的预设）
# 然后使用自定义配置运行
python -m inference \
  --config my_config.yaml \
  --protein_ligand_csv input.csv \
  --out_dir results/
```

### 要调整的关键参数

**采样密度：**
- `samples_per_complex: 10` → 增加到 20-40 用于困难情况
- 更多样本 = 更好的覆盖范围但运行时间更长

**推理步骤：**
- `inference_steps: 20` → 增加到 25-30 以获得更高精度
- 更多步骤 = 可能更好的质量但更慢

**温度参数（控制多样性）：**
- `temp_sampling_tor: 7.04` → 为柔性配体增加（8-10）
- `temp_sampling_tor: 7.04` → 为刚性配体减少（5-6）
- 更高温度 = 更多样的位姿

**模板中可用的预设：**
1. 高精度：更多样本 + 步骤，较低温度
2. 快速筛选：更少样本，更快
3. 柔性配体：增加扭转温度
4. 刚性配体：减少扭转温度

**有关完整的参数参考**：使用 Read 工具阅读 `references/parameters_reference.md`

## 高级技术

### 集成对接（蛋白质柔性）

对于已知柔性的蛋白质，对接到多个构象：

```python
# 创建集成 CSV
import pandas as pd

conformations = ["conf1.pdb", "conf2.pdb", "conf3.pdb"]
ligand = "CC(=O)Oc1ccccc1C(=O)O"

data = {
    "complex_name": [f"ensemble_{i}" for i in range(len(conformations))],
    "protein_path": conformations,
    "ligand_description": [ligand] * len(conformations),
    "protein_sequence": [""] * len(conformations)
}

pd.DataFrame(data).to_csv("ensemble_input.csv", index=False)
```

使用增加的采样运行对接：

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv ensemble_input.csv \
  --samples_per_complex 20 \
  --out_dir results/ensemble/
```

### 与评分函数集成

DiffDock 生成位姿；结合其他工具进行亲和力：

**GNINA（快速神经网络评分）：**
```bash
for pose in results/*.sdf; do
    gnina -r protein.pdb -l "$pose" --score_only
done
```

**MM/GBSA（更准确，更慢）：**
在能量最小化后使用 AmberTools MMPBSA.py 或 gmx_MMPBSA

**自由能计算（最准确）：**
使用 OpenMM + OpenFE 或 GROMACS 进行 FEP/TI 计算

**推荐工作流：**
1. DiffDock → 生成带置信度评分的位姿
2. 视觉检查 → 检查结构合理性
3. GNINA 或 MM/GBSA → 重新评分并按亲和力排名
4. 实验验证 → 生化测定

## 限制和范围

**DiffDock 适用于：**
- 小分子配体（通常 100-1000 Da）
- 类药物有机化合物
- 小肽（<20 个残基）
- 单链或多链蛋白质

**DiffDock 不适用于：**
- 大生物分子（蛋白质-蛋白质对接）→ 使用 DiffDock-PP 或 AlphaFold-Multimer
- 大肽（>20 个残基）→ 使用替代方法
- 共价对接 → 使用专门的共价对接工具
- 结合亲和力预测 → 结合评分函数
- 膜蛋白 → 未专门训练，谨慎使用

**有关完整的限制**：使用 Read 工具阅读 `references/confidence_and_limitations.md`

## 故障排除

### 常见问题

**问题：所有预测的置信度评分都很低**
- 原因：大/异常配体、结合位点不明确、蛋白质柔性
- 解决方案：增加 `samples_per_complex`（20-40），尝试集成对接，验证蛋白质结构

**问题：内存不足**
- 原因：GPU 内存不足以处理批次大小
- 解决方案：减少 `--batch_size 2` 或一次处理更少的复合物

**问题：性能缓慢**
- 原因：在 CPU 而不是 GPU 上运行
- 解决方案：使用 `python -c "import torch; print(torch.cuda.is_available())"` 验证 CUDA，使用 GPU

**问题：不现实的结合位姿**
- 原因：蛋白质准备不当、配体太大、结合位点错误
- 解决方案：检查蛋白质是否有缺失残基，移除远端水，考虑指定结合位点

**问题："Module not found"错误**
- 原因：缺少依赖项或环境错误
- 解决方案：运行 `python scripts/setup_check.py` 进行诊断

### 性能优化

**获得最佳结果：**
1. 使用 GPU（实际使用必不可少）
2. 为重复的蛋白质使用预计算 ESM 嵌入
3. 一起批处理多个复合物
4. 从默认参数开始，然后根据需要调整
5. 验证蛋白质结构（解决缺失残基）
6. 对配体使用规范 SMILES

## 图形用户界面

对于交互式使用，启动 Web 界面：

```bash
python app/main.py
# 导航到 http://localhost:7860
```

或使用在线演示而无需安装：
- https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web

## 资源

### 辅助脚本（`scripts/`）

**`prepare_batch_csv.py`**：创建和验证批处理输入 CSV 文件
- 使用示例条目创建模板
- 验证文件路径和 SMILES 字符串
- 检查必需列和格式问题

**`analyze_results.py`**：分析置信度评分并对预测进行排名
- 解析来自单个或批处理运行的结果
- 生成统计摘要
- 导出到 CSV 以进行下游分析
- 识别跨复合物的顶级预测

**`setup_check.py`**：验证 DiffDock 环境设置
- 检查 Python 版本和依赖项
- 验证 PyTorch 和 CUDA 可用性
- 测试 RDKit 和 PyTorch Geometric 安装
- 如果需要，提供安装说明

### 参考文档（`references/`）

**`parameters_reference.md`**：完整的参数文档
- 所有命令行选项和配置参数
- 默认值和可接受范围
- 用于控制多样性的温度参数
- 模型检查点位置和版本标志

当用户需要时阅读此文件：
- 详细的参数说明
- 特定系统的微调指导
- 替代采样策略

**`confidence_and_limitations.md`**：置信度评分解读和工具限制
- 详细的置信度评分解读
- 何时信任预测
- DiffDock 的范围和限制
- 与互补工具的集成
- 预测质量的故障排除

当用户需要时阅读此文件：
- 帮助解读置信度评分
- 了解何时不使用 DiffDock
- 结合其他工具的指导
- 验证策略

**`workflows_examples.md`**：全面的工作流示例
- 详细的安装说明
- 所有工作流的分步示例
- 高级集成模式
- 常见问题的故障排除
- 最佳实践和优化技巧

当用户需要时阅读此文件：
- 带有代码的完整工作流示例
- 与 GNINA、OpenMM 或其他工具的集成
- 虚拟筛选工作流
- 集成对接程序

### 资产（`assets/`）

**`batch_template.csv`**：批处理的模板
- 预格式化的 CSV，带有必需列
- 显示不同输入类型的示例条目
- 准备好使用实际数据自定义

**`custom_inference_config.yaml`**：配置模板
- 带有所有参数的注释 YAML
- 常见用例的四个预设配置
- 解释每个参数的详细注释
- 准备好自定义和使用

## 最佳实践

1. **始终验证环境**，在开始大型作业之前使用 `setup_check.py`
2. **验证批处理 CSV**，使用 `prepare_batch_csv.py` 尽早捕获错误
3. **从默认开始**，然后根据系统特定需求调整参数
4. **生成多个样本**（10-40）以获得鲁棒的预测
5. **视觉检查**下游分析前的顶级位姿
6. **结合评分**函数进行亲和力评估
7. **使用置信度评分**进行初始排名，而不是最终决策
8. **预计算嵌入**用于虚拟筛选活动
9. **记录参数**以确保可重复性
10. **尽可能验证结果**实验

## 引用

使用 DiffDock 时，引用适当的论文：

**DiffDock-L（当前默认模型）：**
```
Stärk et al. (2024) "DiffDock-L: Improving Molecular Docking with Diffusion Models"
arXiv:2402.18396
```

**原始 DiffDock：**
```
Corso et al. (2023) "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking"
ICLR 2023, arXiv:2210.01776
```

## 其他资源

- **GitHub 仓库**：https://github.com/gcorso/DiffDock
- **在线演示**：https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web
- **DiffDock-L 论文**：https://arxiv.org/abs/2402.18396
- **原始论文**：https://arxiv.org/abs/2210.01776
