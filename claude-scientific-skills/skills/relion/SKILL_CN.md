---
name: relion
description: 验证并执行RELION单颗粒冷冻电镜精修和半图后处理。支持STAR光学/采集检查、粒子堆栈一致性、金标准半数据集、软掩膜验证、诊断性傅里叶壳相关（FSC），以及重启指导。
license: MIT
compatibility: Python 3.12+ with numpy, mrcfile and starfile for bundled validation; RELION 5.0.1 CPU/MPI executables for refinement and postprocessing. Native workflows require MPI, OpenMP and an FFT library (FFTW or MKL). GPU builds require their supported accelerator stack. Network is needed for installation only.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  upstream-version: "5.0.1"
  last-reviewed: "2026-10-01"
---

# RELION单颗粒精修

用于RELION单颗粒项目，特别是提取的粒子 → 同质化选定的
粒子子集 → 金标准精修 → 半图验证和后处理。内置的
运行器从**已标注CTF的提取粒子和一个初始3D参考**开始。它不能
替代运动校正、挑选、2D/3D筛选，或对图谱质量的生物学解读。
对于断层扫描、螺旋重建、Blush，或异质状态建模，请使用相应的
上游工作流程，而不要强行将这些数据纳入此受限的SPA运行器。

## 保留采集和坐标约定

从电影或恢复作业时，请阅读 [references/acquisition-and-restarts.md](references/acquisition-and-restarts.md)。确认像素大小的单位为**Å/像素**，电压单位为**kV**，球差单位为**mm**，离焦单位为**Å**，振幅对比为一个分数，以及样本所依据的对称性。不要通过猜测单位来"修正"一个可疑的值。

`data_optics` 描述采集/图像分组；`data_particles` 通过
`_rlnOpticsGroup` 引用它们。粒子文件名使用**从1开始**的
`index@stack.mrcs`；类似 `00000001@stack.mrcs` 这样的前导零是有效的。相对路径的解析
基准是RELION项目目录，而不是STAR文件所在的目录。在合并
或对STAR文件取子集时，请保留光学分组。`_rlnOriginXAngst`/`_rlnOriginYAngst` 是以Å为单位的平移量，不是像素。

从此技能目录运行，并使用指向实际项目的路径：

```bash
python scripts/spa_workflow.py validate-star project/particles.star --project project
```

这会打开引用的堆栈，并检查光学分组归属、有限的采集/CTF值、索引、
盒子大小、重复的粒子引用以及现有的半数据集分配。只有在堆栈
确实不可用时才使用 `--metadata-only`；此时JSON会记录
`stack_checks_performed: false`。它不会扫描每个粒子像素以检测损坏，
也不会确立正确的图像归一化。物理范围警告是审查提示，不是
证明异常显微镜设置是错误的。

## 对选定的粒子群体进行精修

在运行之前，请检视代表性粒子和类平均图、离焦分布、CTF
拟合、粒子方向分布以及初始参考。确保图谱与粒子的
盒子/像素大小在任何降采样之后保持一致。该运行器有意只支持
光学分组间的一个有效盒子/像素大小；对于异质采样，请使用
一个明确的上游重采样工作流程来处理。请使用常规提取、已归一化的
粒子，且这些粒子尚未经过相位翻转或维纳滤波；此运行器不配置
这些特殊的输入情形。

```bash
python scripts/spa_workflow.py refine \
  --star project/particles.star --reference project/initial.mrc \
  --project project --diameter 180 --symmetry C1 \
  --initial-lowpass 40 --mpi-ranks 3 --threads 2 --output project/RefinePilot
```

上面的直径和低通滤波值是示例性的**Å**单位值。请使用适合
样本的实际值。精修执行的是带有 `--auto_refine`、
`--split_random_halves`、`--ctf` 以及一个低通起始参考的
`mpirun -np 3 relion_refine_mpi`。金标准分割需要MPI；
普通的顺序执行文件 `relion_refine` 无法执行此分割。
请使用奇数且≥3的rank数（主进程加上均衡的半数据集工作进程），
并配合匹配的MPI安装。该CPU命令适用于有边界的试运行；对于完整数据，
请选择一个有文档记录的GPU/MPI启动方式。

该运行器将命令、原生版本和日志保存在一个新的输出目录中，记录一个
明确的随机种子（默认为1），显示运行时警告，在进程失败时停止，并且
要求在报告成功之前获得收敛的未滤波半图。它不会自动重试
昂贵的作业，也不会悄无声息地丢弃失败作业的文件。请保留
`_optimiser.star`、模型/采样STAR文件以及引用的粒子路径以便重启。
请使用原始作业的optimiser，而不要从一个部分处理的表格重新
开始一次新的随机分割。

## 检视独立的半图

请使用两个独立精修得到的**未滤波**半图，而不要使用合并后、
经过锐化的图谱的两份副本。匹配的文件头并不能确立统计
独立性；独立的粒子分配和精修历史才能提供这一证据。除了
全局FSC曲线外，还要检视方向性各向异性、优先方向以及局部
分辨率。

```bash
python scripts/spa_workflow.py fsc \
  project/RefinePilot/run_half1_class001_unfil.mrc \
  project/RefinePilot/run_half2_class001_unfil.mrc --output diagnostic-fsc.tsv
```

这会检查图谱维度、有限值、像素大小、原点、坐标轴顺序以及重复的
图谱，然后写出一个**未加掩膜的诊断性FSC**。所报告的0.143穿越点
使用的是线性插值；`null` 表示未检测到向下的穿越，而不是无限
分辨率。Nyquist分辨率为2 × 像素大小。此诊断功能仅限于
≤256³的偶数立方图谱；对于更大的图谱，请使用RELION原生的
`relion_image_handler --fsc`。它不能替代经掩膜校正的FSC。
该辅助工具要求实空间图谱具有标准坐标轴、零MRC起始索引以及
正交的晶胞角。请明确地转换其他网格并保留溯源信息；仅仅
编辑文件头可能导致密度错位。匹配的文件头和FSC无法确定
绝对的手性（handedness）。

## 使用软掩膜进行后处理

从一个适当低通滤波的密度构建溶剂掩膜，边界要扩展，边缘要
平滑。检视所有切片；过紧的掩膜会夸大相关性。避免使用
从两个半图共享的高频噪声中导出的掩膜。

```bash
python scripts/spa_workflow.py postprocess \
  --half1 project/RefinePilot/run_half1_class001_unfil.mrc \
  --half2 project/RefinePilot/run_half2_class001_unfil.mrc \
  --mask project/soft_mask.mrc --output project/PostProcessPilot
```

该辅助工具检查掩膜是否为[0,1]区间内的非常数值、软边界体素以及
匹配的图谱网格，然后运行带有明确半图、掩膜和像素大小的
`relion_postprocess`。RELION会执行自己的掩膜/随机化
校正，并写出 `postprocess.star`。这个受限的命令将
B因子留在零（不进行自动B因子估计）；只有在选择了可论证的拟合
范围并检视了图谱质量之后，才添加自动/手动锐化。一个有效的范围和
一些分数掩膜体素并不能证明该掩膜在科学上是合适的。请检视
报告分辨率附近的相位随机化加掩膜FSC：残余相关性需要一个更平滑/更宽的
掩膜以及另一次后处理运行。

关于经过测试的原生工具，以及流程执行与重建验证之间的区别，
参见 [references/runtime-and-validation.md](references/runtime-and-validation.md)。

## 主要参考文献

- [RELION 5.0安装](https://relion.readthedocs.io/en/release-5.0/Installation.html)。
- [STAR和图谱约定](https://relion.readthedocs.io/en/release-5.0/Reference/Conventions.html)。
- [单颗粒教程](https://relion.readthedocs.io/en/release-5.0/SPA_tutorial/index.html)。
- [金标准精修](https://relion.readthedocs.io/en/release-5.0/SPA_tutorial/Refine3D.html)。
- [掩膜创建和后处理](https://relion.readthedocs.io/en/release-5.0/SPA_tutorial/Mask.html)。
