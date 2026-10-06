---
name: cellprofiler
description: 运行可复现的 CellProfiler 显微镜流程，用于细胞核分割、细胞计数以及逐对象荧光测量。支持图像/通道清单、无界面（headless）批量执行、分割叠加图，以及 2D 荧光实验的测量质控。
license: MIT
compatibility: Python 3.12+，需 numpy 和 tifffile（当前仅辅助脚本依赖）；分割需要单独的 CellProfiler 4.2.8 应用程序/容器。完整的 CellProfiler 依赖较旧的原生依赖。仅安装时需要网络访问。无需凭据。
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  upstream-version: "4.2.8"
  last-reviewed: "2026-09-30"
---

# CellProfiler 定量显微镜分析

当用户需要可重复的 CellProfiler `.cppipe`、细胞核计数、细胞核荧光或批量显微镜测量时，使用此技能。内置的实验流程接受**每个视野一个 2D 灰度 TIFF 细胞核通道**，像素为 black-is-zero（MINISBLACK），即明亮的细胞核位于暗背景上。调色板（Palette）和 white-is-zero 的 TIFF 需要进行显式转换。对于体积分割、多通道细胞绘画（cell painting）或针对特定组织的模型，应设计单独的流程并验证这些假设，而不是默默地对图像进行投影或拆分。

官方应用程序和手册仍为 **4.2.8**。PyPI 发布的是 **4.2.8.1**；此处使用的七个模块以及内嵌的 Threshold 模块与 4.2.8 源码一致，但本次审阅并未执行该原生发行版。请将辅助脚本环境与 CellProfiler 较旧的依赖栈分开；验证边界请参阅运行时参考。

## 工作流程

1. 确定采集单元：板、孔、位点、时间点（如有）、像素尺寸、细胞核通道标识、相机位深、曝光以及生物学重复。保留原始图像强度。在使用此辅助脚本之前，先用 Bio-Formats 对专有格式进行显式转换。
2. 创建下面的 CSV 清单。`image_path` 是绝对路径或相对于清单的路径；样本 ID 使用字母、数字、点、短横线或下划线；样本 ID 以及板/孔/位点的组合必须唯一。使用非纯数字的样本 ID，例如 `sample_001`：LoadData 会推断列类型，否则可能把 `001` 变成 `1`。标识符两侧避免出现空白字符。TIFF 必须是 uint8 或 uint16、单平面/单序列/单分辨率，并且不是常数图像。辅助脚本会拒绝 RGB、z-stack 和浮点图像，而不是去猜测通道。
3. 使用 [assets/nuclei.cppipe](assets/nuclei.cppipe) 作为起始流程：LoadData → IdentifyPrimaryObjects → 强度/大小测量 → 轮廓叠加图 → CSV 导出。初始直径范围为 8–80 **像素**，使用全局 Otsu 阈值，不做阈值平滑，并排除边界对象。在比较不同条件之前，请根据代表性图像和采集像素尺寸校准此范围。
4. 运行一个小型试点，涵盖对照、低/高密度、暗图像和板边缘。检查保存的叠加图，看是否有漏检的细胞核、分裂、合并以及边缘排除。在 CellProfiler 中调整阈值和去团簇（declumping），导出调优后的 `.cppipe`，并通过 `--pipeline` 传入以保留它。不要为每种处理单独选择设置，以使它们的计数一致。
5. 冻结调优后的流程并分析整批数据。检查输入饱和警告、零计数、计数/面积分布以及对照行为。用于推断的聚合应在生物学重复层面进行；来自同一个孔的数千个细胞并不是独立的孔。

## 运行有界的实验

在此技能目录下，创建 `images.csv`：

```csv
sample_id,image_path,plate,well,site
control_A01_1,images/control_A01_1_DAPI.tif,Plate1,A01,1
```

```bash
python scripts/nuclei_assay.py prepare images.csv load_data.csv
python scripts/nuclei_assay.py run images.csv results --executable cellprofiler
python scripts/nuclei_assay.py summarize results
```

`run` 需要一个全新/空的输出目录，并使用 `-c -r`、已保存的流程副本、`--data-file`、输出文件夹和 `--done-file` 来执行 CellProfiler。成功需要满足：退出码为零、存在 `Complete` 标记，且测量表有效。它会在执行前将命令、流程校验和、输入图像校验和以及样本质控记录到 `assay_qc.json` 中，如果执行或输出验证失败，则保留 `failed` 状态和错误信息。CellProfiler 的输出会写入 `cellprofiler.log`。请在新的输出文件夹中重新运行。`summarize` 会独立检查 CSV 内容；它并不能证明引擎运行已经完成。

自定义流程必须保留 `DNA`、`Nuclei`、`Metadata_Sample`、整数类型缩放，以及无前缀的单对象 `Image.csv`/`Nuclei.csv` 导出约定。保留所需的强度/面积测量。重命名的对象集或不同的强度尺度需要对辅助脚本做相应调整，而不是不加检查地替换 `--pipeline`。

可执行文件也可以是 CellProfiler 应用程序启动器或本地容器启动器；容器目标、文件系统映射和验证证据请参阅 [references/runtime-and-qc.md](references/runtime-and-qc.md)。`prepare` 和 `summarize` 无需 CellProfiler 即可运行。

## 解读输出

- `Image.csv`：每个图像/视野一行，包含 `Count_Nuclei` 和采集元数据。
- `Nuclei.csv`：每个被接受的对象一行，包含 DNA 的平均/积分强度、面积和形状。
- `*_nuclei.png`：输入图像上叠加的绿色细胞核边界，用于视觉质控。
- `pipeline.cppipe` 和 `cellprofiler.done`：确切的流程副本和引擎完成标记。
- `assay_qc.json`：运行状态、唯一的图像/对象键、精确计数、有限的平均/积分强度和正面积检查、以像素为单位的视野平均面积，以及存储饱和标志。

在此资源中，LoadData 在缩放时忽略相机元数据，并除以整数存储最大值：uint8 → 255，uint16 → 65535。因此，以 uint16 存储的 12 位相机，其最大值接近 0.0625。在没有显式校准的情况下，不要在不同位深、曝光、增益或染色批次之间比较强度。一幅饱和的图像可能通过分割，但其强度测量已无法使用。照明校正和背景扣除是针对具体实验的附加步骤；此起始流程两者都不做。

饱和比例仅统计处于**存储最大值**的像素。12 位探测器可能在 4095 处饱和，而 uint16 存储最大值为 65535；请单独检查已知的采集上限。积分强度是像素值之和，可能超过 1；只有逐像素的平均强度被限制在 0–1 之间。视野的平均细胞核强度对每个细胞核等权重，而不是对每个像素等权重。

计数检查无法证明分割正确。请检查叠加图和独立标注的视野；在报告生物学结果的同时，也要报告边界排除和分割错误。可选的合成引擎测试针对一个已知的三细胞核示例，而不是在未见过的细胞类型上的实验性能。在本次审阅中该测试被跳过，因为没有配置引擎。

## 来源

- [官方示例流程](https://cellprofiler.org/examples)：选择针对具体实验的起点。
- [CellProfiler 4.2.8 手册](https://cellprofiler-manual.s3.amazonaws.com/CellProfiler-4.2.8/index.html)：模块设置与解读。
- [无界面批量处理](https://cellprofiler-manual.s3.amazonaws.com/CellProfiler-4.2.8/help/other_batch.html)：命令行执行。
- [当前应用程序下载](https://cellprofiler.org/releases) 和 [PyPI 发行版](https://pypi.org/project/cellprofiler/)：不同的发布目标。
