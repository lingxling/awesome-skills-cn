---
name: deepspot-m
description: 使用 DeepSpot-M 从 H&E 组织学图像生成全转录组级别的虚拟空间转录组学数据。用于从约 20 倍放大下的 224x224 切片预测 log1p-CPM 表达量、按基因符号查询已发布的蛋白编码基因面板，以及在使用 histolab 进行分辨率感知切片后对整张切片进行预测。
license: PolyForm-Noncommercial-1.0.0
compatibility: Requires deepspotm 1.0.0, Python >=3.10 and PyTorch; network and approved Hugging Face access for initial gated weight download. CPU supported; CUDA optional. Optional histolab 0.7.0 tiling requires a separate Python 3.10/3.11 environment and OpenSlide. AnnData is needed for H5AD export.
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.2"
  skill-author: Ratschlab, ETH Zurich
  last-reviewed: "2026-09-30"
---

# DeepSpot-M

## 概述

DeepSpot-M 是一个多模态基础模型，它将一张 224x224 的 H&E 组织学切片映射为
以 log1p-CPM 表示的空间基因表达。其输出是虚拟空间转录组学数据：每个
被查询基因、每个切片对应一个数值，按照这些切片原本所在的网格排布。

一个经过 LoRA 适配的病理学基础模型骨干网络（Midnight）将切片进行分词化。一个
交叉注意力基因解码器让每个基因查询能够关注这些图块（patch）token，而一个
基因路由超网络会根据冻结的生物学嵌入（Evo 2、Orthrus、ProtT5、scGPT、Apertus）
构建出基因特定的投影。基因以可查询的嵌入形式进入模型，而不是作为固定的输出
槽位，因此发布的模型覆盖了约 1.9 万个蛋白编码基因的面板，其中包括训练中
未见过的基因。该面板随权重一起发布，以 `tokens.csv` 的形式提供，并通过
`model.gene_names` 暴露出来；不在该面板中的基因在本版本中无法被查询。

将该模型应用于 TCGA 数据后，产生了一份覆盖 32 种癌症类型、28,664 张切片的
虚拟空间转录组学图谱。

## 许可

代码采用 PolyForm Noncommercial 1.0.0 许可，权重采用 CC-BY-NC-SA-4.0 许可。
当前的模型访问申请表还额外限制了申请资格，要求申请人为无并行商业关联的
学术/公共非营利研究人员，并排除商业资助/合作用途。在申请访问权限之前，请
阅读当前实际的声明；仅有非商业意图并不足以证明资格。仅限研究用途，
不得用于临床或诊断用途。请保留适用的署名和许可声明。

## 安装

```bash
uv pip install deepspotm==1.0.0
```

PyPI 上的 1.0.0 版本声明要求 Python >=3.10，且没有上限；这并不能证明它与
未来每一个依赖项发布版本兼容。请使用一个隔离的环境。
如果使用 GPU，请安装与你的 CUDA 运行时相匹配的 PyTorch 构建版本。
可选的 histolab 0.7.0 切片工具要求 Python <3.12 以及一套较旧的科学计算
软件栈：请单独运行切片步骤，并以 PNG 切片加坐标清单的形式交换数据。

## 模型访问

权重是受限访问的：

1. 打开 <https://huggingface.co/ratschlab/DeepSpotM> 并申请访问权限。
2. 获得访问权限后，对将用于下载的机器进行身份验证：

```bash
hf auth login
```

Hugging Face 下载器使用缓存的凭证或 `HF_TOKEN`；审批和
身份验证是两个独立的步骤。如果要选择缓存位置，请在导入 Hub 相关库之前
设置 `HF_HOME`。不要把 token 写入代码中。一个已获批准的本地模型目录
可以离线加载。

## 快速开始

以下是受限访问模型推理的示意性示例；加载/查询 API 和本地预处理在
未下载权重的情况下已经过检查：

```python
import torch
from PIL import Image
from deepspotm import DeepSpotM

device = "cuda" if torch.cuda.is_available() else "cpu"
revision = "48be27af436a50e5c74175680ac2b7b2596a506b"
model, image_processor = DeepSpotM.from_pretrained(
    "ratschlab/DeepSpotM", source="scgpt", device=device, revision=revision
)

with Image.open("tile.png") as image:
    if image.size != (224, 224):
        raise ValueError("Expected a pre-tiled 224x224 image at verified ~0.5 um/px")
    batch = image_processor(image.convert("RGB")).unsqueeze(0).to(device)
genes = ["EPCAM", "CD3D"]
vals = model.predict_genes(batch, genes).cpu()  # shape (1, 2)
```

`image_processor` 将一张 PIL 图像转换为张量；`unsqueeze(0)` 添加 batch
维度，而 `predict_genes` 接受该 batch 以及一个
HGNC 基因符号列表作为参数。返回的数值以 log1p-CPM 表示，与你传入的基因列表
一一对应，因此要将该列表与输出一起保存，以保留列的标签信息。基因符号必须
在已发布的约 1.9 万基因面板（`model.gene_names`）中；未知符号会引发
`KeyError`，并指明是哪些基因出了问题。

## 切片要求

切片必须是大约 20 倍放大（约每像素 0.5 微米）下的 224x224 RGB 图像。请在
流水线的边界处检查尺寸，而不是将未经检查的裁剪直接传入：

```python
TILE_PX = 224

def require_tile(tile):
    """Return an RGB 224x224 tile, or raise if the crop is the wrong size."""
    if tile.size != (TILE_PX, TILE_PX):
        raise ValueError(
            f"DeepSpot-M expects a {TILE_PX}x{TILE_PX} tile at about 20x "
            f"(~0.5 microns per pixel); got {tile.size[0]}x{tile.size[1]}. "
            "Re-tile at the matching level or resample the crop."
        )
    return tile.convert("RGB")
```

仅凭像素尺寸无法验证放大倍数。请读取两个方向的 MPP（微米/像素）值以及
实际的层级降采样系数；只有在某个原生层级的物理分辨率足够接近所选目标
分辨率时才使用它。否则，应显式地从足够精细的原始像素重新采样，并记录该
变换过程。永远不要从层级编号推断出 20 倍放大。返回的处理器会对图像进行
缩放/裁剪，但无法确定其物理 MPP 值。

## 保持该依赖项为可选项

`deepspotm` 及其权重是一个很重、受限访问的依赖项。应在需要它的函数内部
导入它，使周边项目在没有它的情况下也能安装、导入和测试，并将
`ImportError` 转换为一条列明每一步的提示信息：

```python
DEEPSPOTM_HELP = (
    "DeepSpot-M is unavailable. Install it with `uv pip install deepspotm==1.0.0`, request "
    "access to the gated weights at https://huggingface.co/ratschlab/DeepSpotM, then "
    "authenticate with `hf auth login`."
)

def load_deepspotm(source="scgpt"):
    try:
        from deepspotm import DeepSpotM
    except ImportError as exc:
        raise RuntimeError(DEEPSPOTM_HELP) from exc
    return DeepSpotM.from_pretrained("ratschlab/DeepSpotM", source=source)
```

## 嵌入来源

`source` 用于选择路由网络从哪种冻结基因嵌入构建投影。它是以下五个值
之一：

| `source`  | 基因嵌入类型                        |
| --------- | --------------------------------- |
| `evo2`    | 基因组序列                          |
| `orthrus` | RNA                               |
| `prott5`  | 蛋白质序列                          |
| `scgpt`   | 单细胞表达                          |
| `apertus` | 语言模型                            |

每一种都给出了基因身份的不同视角。每次运行选择一种，当这一选择对你的
分析有影响时，对同一批切片用多个来源分别运行一遍。已发布的多来源模型可以
使用 `model.set_source(name)` 进行切换；无需重新加载模型。
推理调用接口、批处理和设备放置、基因符号处理以及输出单位，参见
`references/api.md`。

## 整张切片工作流程

预测是按切片进行的，因此整张切片规模的运行是一个切片步骤，后面跟着
批量推理：

1. 验证切片的 MPP，使用 `histolab` 技能在组织网格上提取 224x224 切片，
   并保留每个切片在第 0 层的边界框以及测得的输出 MPP。
2. 使用 `torch.stack` 处理并堆叠切片为批次。
3. 对每个批次调用一次 `predict_genes`，使用同一个基因列表。
4. 按记录的切片 ID 顺序拼接各批次结果；按这些 ID 将坐标连接起来，
   检查唯一性和缺失的切片，而不要假设文件/报告的行顺序。

要将输出标注为模型预测结果，而不是实测的转录本计数。应在带有配对检测
手段的留出切片/患者上进行验证，针对预期的组织和处理条件；来自同一张
切片的多个切片不是独立的生物学重复样本。已发布的基础模型也与
针对特定癌症微调过的 TCGA 图谱模型有所不同。

该矩阵就是该切片的虚拟空间转录组学图谱，可以直接导入 `AnnData` 用于
下游分析。[整张切片工作流程](references/whole_slide.md) 中有一个完整的
示例循环、批次大小设定以及 `AnnData` 组装步骤。

## 验证范围

本次审查于 2026-09-30 针对当前的 PyPI 1.0.0 wheel 包及对应的上游模型
源代码进行。CPU 检查使用了 Python 3.12.10、Torch 2.7.1、Torchvision 0.22.1、
Transformers 5.18.0、PEFT 0.21.1、Lightning 2.6.6 以及 Hugging Face Hub 1.33.0。
合成检查覆盖了加载/查询接口约定、归一化、分辨率拒绝、坐标连接以及
H5AD 往返读写。受限权重、CUDA、真实切片分切以及生物学预测准确性均
未经测试；完整的推理示例只是示意性的。

## 常见用例

- 肿瘤切片中标记基因的空间表达图谱。
- 在没有匹配检测实验运行的切片队列上进行全转录组预测。
- 按符号查询约 1.9 万基因面板中的任意基因，包括训练中未见过的基因——
  远超一个典型空间检测面板中的几百个基因。
- 为只有形态学信息的组织学流水线添加表达通道。
- 构建切片级队列图谱，正如对 TCGA 所做的那样。

## 详细参考文档

- `references/api.md`：完整介绍 `from_pretrained` 和 `predict_genes`、五种
  嵌入来源及如何选择、批处理、设备放置、基因符号处理，以及如何转换
  log1p-CPM 输出。
- `references/whole_slide.md`：使用 histolab 进行切片分切、整张切片规模的
  预测循环、组装并存储切片×基因矩阵，以及队列规模的运行。

## 主要来源

- 论文：<https://doi.org/10.64898/2026.06.19.26356060>（medRxiv，2026）
- 代码：<https://github.com/ratschlab/DeepSpotM>
- 权重：<https://huggingface.co/ratschlab/DeepSpotM>
- PyPI：<https://pypi.org/project/deepspotm/>
