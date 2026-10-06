---
name: nmrglue
description: 使用 nmrglue 将已校准的一维复数 NMR 自由感应衰减（FID）处理为相位校正后的谱图、候选峰和带符号的积分区域。适用于原始一维 NMR 处理、ppm 轴验证、切趾（apodization）、傅里叶变换、手动相位校正、基线校正或可复现的谱图积分。
license: MIT
compatibility: Requires Python 3.12+, nmrglue, NumPy 2+, and SciPy. Installation needs network access; processing is local and needs no credentials.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  tested-package-version: "0.12"
  last-reviewed: "2026-10-01"
---

# nmrglue：已校准的一维 FID 处理

## 何时使用

适用于均匀采样的复数一维 FID，且其采集参数和复数频率约定均已知。该辅助脚本会生成
按 ppm 降序排列的谱图、正峰候选、带符号的区域积分以及可复现的处理报告。
它不会鉴定化合物，也不会对共振峰进行归属。

该可执行脚本接受一个仅包含一个复数 `fid` 数组的 NumPy `.npz` 文件，或一个
标准的一维复数时域 NMRPipe 文件。NMRPipe 读取功能已通过合成数据的写入/读取往返测试、
已知谱图恢复测试以及一个小型上游 NMRPipe 生成的二进制测试夹具（fixture）进行验证。实验性的 Bruker、Varian 和 JEOL
导入**未经本测试套件验证**。对于这些格式，请先检查相应的
nmrglue 读取器和采集元数据。能够打开转换后的文件并不代表原始采集的解码是正确的。
阅读 [references/acquisition-and-validation.md](references/acquisition-and-validation.md)
了解转换边界、坐标轴校准和定量限制。

## 工作流程

1. 保留原始 FID。根据采集参数或已知参考确定以 Hz 为单位的谱宽、以 MHz 为单位的正观测频率、
   以 ppm 为单位的载波频率、观测核以及符号约定。确定是否已经进行了数字滤波器/群延迟去除。
   不要根据数组长度或典型仪器默认值推断这些参数。
2. 复制 [assets/processing.json](assets/processing.json)，并将其中的合成示例值
   替换为实测参数和明确的处理选项。其符号 `-i`
   表示位于偏移 `f = (ppm - carrier_ppm) * observation_mhz` 处的共振具有时间
   依赖性 `exp(-2*pi*i*f*t)`。仅在相反约定时选择 `+i`；辅助脚本会在处理前对其
   取共轭。请使用已知参考峰进行验证。
3. 选择非负的指数线宽展宽（Hz）、不小于所采集 FID 长度的偶数补零大小、
   首点缩放系数以及相位角。
   补零改善的是插值，而不是采集得到的谱分辨率。
   首点缩放系数 `0.5` 适用于所提供的因果合成示例；
   实际采集和先前的预处理可能需要其他值。
4. 运行辅助脚本，检查实部和虚部谱图，必要时修正手动相位。
   `phase0_deg + phase1_deg * index / zero_fill_points` 在傅里叶变换后应用；
   索引零对应高 ppm 端。不存在隐式枢轴点，也没有自动相位估计。
5. 仅当明确提供的 ppm 区域无信号时才拟合线性基线。
   将 `baseline` 设为 `linear`，并添加至少包含两个区域的 `baseline_regions_ppm`。
   检查残差和宽峰；穿过信号进行拟合会使积分产生偏差。
6. 将峰位置与参考进行比较，检查候选峰是否为伪影，并对
   指定区域进行积分。将重叠峰报告为重叠峰。保留负面积
   作为相位/基线问题的诊断证据，而不要取绝对值。

## 执行

已在 Python 3.12、nmrglue 0.12、NumPy 2.5.3 和 SciPy 1.18.1 下测试：

```bash
uv run --no-project --python 3.12 --with nmrglue==0.12 --with numpy==2.5.3 --with scipy==1.18.1 \
  python skills/nmrglue/scripts/process_1d.py fid.npz processing.json nmr-result
```

路径假定以本集合根目录为起点。安装在其他位置时请相应调整。输出
目录必须是新目录，以便重复处理时保留之前的结果以供审阅。

对于已有的一维 NMRPipe FID，添加 `--input-format nmrpipe` 并用其路径替代
`fid.npz`。辅助脚本要求标准的 FDF2 直接维度、复数正交检测、
时域标志，并要求文件头与 JSON 中的谱宽、观测频率和载波一致。
JSON 设置保持显式；不一致时会直接失败，而不会静默地
重新校准。`FDF2TDSIZE` 必须等于存储的复数点数，且 `FDF2CENTER` /
`FDF2ORIG` 必须描述一个标准的居中坐标轴。先前已补零、截断
或重新居中的文件需要单独的、考虑采集信息的工作流程。观测核/复数符号
以及先前的数字滤波器校正仍需要采集方面的证据。仅凭时域
标志并不能确定该 FID 未经处理。

以下可执行的合成示例与所提供的设置相匹配，在 3 ppm 和 7 ppm 处生成
振幅比为 1:2 的共振峰，并不代表实验样品：

```python
import numpy as np

t = np.arange(8192) / 4000.0
fid = sum(a * np.exp(-np.pi * 2.0 * t)
          * np.exp(-2j * np.pi * (ppm - 5.0) * 400.0 * t)
          for ppm, a in [(3.0, 1.0), (7.0, 2.0)])
np.savez("fid.npz", fid=fid)
```

使用 `assets/processing.json` 作为设置参数运行它。仓库测试套件
会执行该信号和 CLI，检查两个峰位置误差均在 0.001 ppm 以内，检查
积分比和解析面积，并检查相位和基线的恢复情况。NMRPipe
往返测试使用 `ng.pipe.create_dic`/`ng.pipe.write` 写入该 FID，通过
CLI 读取，并验证恢复的峰和积分比。已处理的频域
文件以及相互冲突的校准元数据会被拒绝。

这个 2,176 字节的上游测试夹具使用由 NMRPipe 的 `simTimeND` / `SET` 工具生成的文件，
检查复数采样顺序和文件头校准。本次审查中未运行这些原生工具；
这只是测试夹具兼容性，而不是与 NMRPipe 实时处理结果的比较。

## 交付物与解读

- `spectrum.csv`：降序的 ppm、基线校正后的实部信号、相位校正后的虚部
  信号以及拟合得到的实部基线。绘制 NMR 谱图时将高 ppm 端放在左侧。
- `report.json`：输入/设置的 SHA-256、软件包版本、全部设置、采集时长、
  补零后的数字间隔、正峰候选以及带符号的区域面积。

积分采用端点插值，并沿 ppm 递增方向进行梯形积分；
面积单位为任意信号单位乘以 ppm，与显示方向无关。超出
采样 ppm 轴范围的区域会直接失败，而不会被静默截断。峰显著度（prominence）
是相对于最大正实部强度的比例；它不是基于噪声推导的检测
限。强溶剂信号可能在默认阈值下掩盖较弱的候选峰。

对于定量 NMR，还需另外确定弛豫延迟、脉冲角、饱和、
接收机行为、内标/外标用量以及积分不确定度。
辅助脚本不计算浓度，也不校正不等的弛豫。请将
这些限制与结果一同保留，而不要将任意面积换算为分子数。

## 上游约定

- [处理函数](https://nmrglue.readthedocs.io/en/latest/reference/proc_base.html)：
  指数切趾、补零、FFT 和相位操作。
- [文件与坐标轴工具](https://nmrglue.readthedocs.io/en/latest/reference/fileiobase.html)：
  单位换算使用以 Hz 为单位的谱宽、以 MHz 为单位的观测频率、以 Hz 为单位的载波。
- [NMRPipe 读取器/写入器](https://nmrglue.readthedocs.io/en/latest/reference/pipe.html)：
  经过验证的导入路径是合成的标准一维时域往返。
- [nmrglue 项目](https://github.com/jjhelmus/nmrglue)：上游源代码和格式读取器。

检查时，托管的 `latest` 文档自称版本为 0.9-dev；实际测试的是
0.12 软件包的 API 和数值行为。其 `proc_base.fft` 使用
负指数的 NumPy FFT，随后执行 `fftshift`；NMRPipe 的傅里叶变换约定对应
`fft_positive`，因此在未重新核查 FID 符号和相位之前不要替换为它。
参见 [v0.12 处理源代码](https://github.com/jjhelmus/nmrglue/blob/v0.12/nmrglue/process/proc_base.py)。
多维处理、非均匀采样、自动归属以及实验性的厂商格式导入仍不在
该辅助脚本的已验证范围之内。
