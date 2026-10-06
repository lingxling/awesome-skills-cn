---
name: nwb-conversion
description: 使用 NeuroConv 和 PyNWB 将神经科学采集数据转换为 Neurodata Without Borders 文件，保留元数据和时间基准，检查基于证据的时钟对齐，并生成 schema 验证、NWB Inspector 检查结果和往返一致性检查。适用于平面单通道双光子 TIFF 成像以及带时间戳的行为位置 CSV 的 NWB 转换和同步；本技能不进行放电分选（spike sorting），也不声称对任意采集格式都经过测试支持。
license: MIT
compatibility: Requires Python 3.12 with neuroconv[tiff] 0.10.2, PyNWB 4.2.0, NWB Inspector 0.7.2, roiextractors 0.10.0, tifffile 2026.9.20, zarr 2.18.7 and hdmf-zarr 0.11.3. Local HDF5 file access is required. Network is needed only for installation; no credentials.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-10-01"
  upstream-neuroconv: "0.10.2"
  upstream-pynwb: "4.2.0"
  upstream-nwbinspector: "0.7.2"
---

# 经验证的 NWB 转换

## 支持的数据流

本可执行工作流在一次会话中涵盖两种明确的输入数据流：

| 输入 | NWB 表示方式 | 经测试的约束条件 |
| --- | --- | --- |
| 双光子灰度多页 TIFF + 帧时间戳 CSV | 通过 NeuroConv 得到的名为 `Imaging` 的采集 `TwoPhotonSeries` | 单通道、单平面、每页一张 2D 图像、固定的形状和数据类型 |
| 经校准的位置 CSV（`time_s,x,y`） | 通过 PyNWB 得到的行为 `Position` / `SpatialSeries` | 坐标单位为 m、cm 或 mm；会转换为米，不进行时间重采样 |

其他采集读取器需要各自特定格式的测试。特别是，这个辅助脚本
不解码 SpikeGLX、Open Ephys、多通道 TIFF、体积 TIFF、压缩视频，或像素-到-世界坐标
校准。不要把任意的数值表重新命名为一种受支持的数据流。

## 安装经测试的环境

```bash
uv venv --python 3.12 nwb-env
uv pip install --python nwb-env/bin/python 'neuroconv[tiff]==0.10.2' pynwb==4.2.0 \
  nwbinspector==0.7.2 roiextractors==0.10.0 tifffile==2026.9.20 \
  zarr==2.18.7 hdmf-zarr==0.11.3
```

即使只做 HDF5 转换，也要保留这两个 Zarr 版本锚定：NeuroConv 0.10.2
在启动时会导入其后端配置模块，经测试的未加约束的 Zarr 3.4.0 安装在
`zarr.codec_registry` 上失败了。这个锚定版本的环境在 macOS ARM64 上成功运行了实际的转换、PyNWB 验证和
Inspector 检查。依赖解析器会提供 NumPy 和 HDF5 支持。
这些只是兼容性版本锚定，并不是说 Zarr 2 和 hdmf-zarr 0.11.3 是最新发布版本。
当前的接口检查和经测试的依赖例外情况记录在
[references/upstream-review.md](references/upstream-review.md) 中。

## 工作流程

1. 盘点实际的输入和采集元数据。确定每个数据流的图像平面/通道、
   光学设置、受试者/会话标识符、时区、行为坐标系统、单位,以及
   时间戳时钟。保留原始数据。不要用示例配置中看似合理的默认值来替代缺失的元数据。
2. 将 [assets/session-template.json](assets/session-template.json) 复制到原始数据旁边，并
   替换其中明确标注为合成值的内容。路径会相对于该 JSON 文件解析。关于确切的 CSV 和元数据
   契约以及脉冲对（pulse-pair）变体，见
   [references/input-contract.md](references/input-contract.md)。TIFF 像素会按采集时的原样保留；一个原始的任意单位
   强度值不会仅仅因为改变了单位标签就变成光子计数。
3. 从采集证据中确立共同的时间基准。帧时间戳必须已经是
   相对于带时区的会话开始时间的参考时钟秒数。对于位置数据，应提供一个
   有文档记载的共享时钟，或匹配的同步脉冲。该辅助脚本会拟合一个仿射时钟
   变换，对照指定的容差检查其残差，并拒绝超出脉冲范围的外推。
   它绝不会从看起来同时发生的神经/行为信号中估计同步关系。时钟重置或非线性漂移需要一个明确经过验证的分段映射。
4. 执行转换器。输入必须具有有限且严格递增的时间戳，并且图像/时间戳
   数量匹配。应明确声明单通道和单平面；已知的 TIFF 通道/平面
   元数据必须与之一致。仅凭灰度页面本身无法排除未记录的交错排列。
   采集样本数据保持不变；只有坐标单位,以及在有证据支持的情况下，
   行为时间戳会被转换。
5. 阅读与 NWB 文件一起生成的 `.validation.json`。schema 合规性、Inspector
   检查结果和数据相等性回答的是不同的问题。该脚本在 schema 检查失败时会以错误退出，并在报告中标记需要审查的关键 Inspector
   检查结果。应在具体背景下审查所有检查结果；验证成功并不能证明用户提供的解剖学标签、脉冲配对，或校准
   是正确的。
6. 交付 NWB 文件、验证 JSON、原始转换配置,以及对剩余元数据
   缺口或 Inspector 检查结果的说明。本工作流不包含任何上传或存档提交环节。

## 执行

从技能所在目录运行以下命令，并使用指向实际分析文件的路径：

```bash
nwb-env/bin/python scripts/convert_session.py /path/to/session.json --output /path/to/session.nwb
```

`nwb-env` 必须指向上面创建的环境；示例中绝对的输入路径仅作说明性用途。该命令要求一个 `.nwb` 输出路径，并拒绝覆盖已存在的 NWB 或
验证报告。输出内容包括源文件和转换器的校验和、
软件包版本、完整提供的元数据、单位和时钟拟合的溯源信息，这些内容会同时记录在一份临时记录和验证报告中。在为大型数据调整此命令时，应注意
TIFF 写入是逐帧迭代的，相等性检查也是一次加载一帧；位置 CSV 目前会整体加载到内存中。
往返一致性检查还会验证数据类型、单位缩放、光学通道链接、受试者元数据、
位置参考坐标系、共同时间原点,以及嵌入的溯源信息。需要审查的 Inspector
检查结果会出现在 CLI 摘要中；仅凭退出码为零并不能说明文件在科学上是正确的。
在写入或往返检查过程中发生的异常可能会留下一个没有报告的不完整 NWB 文件；
应保留错误信息，并在纠正原因之后使用一个全新的输出路径。

该真实库测试转换了八张非正方形的 uint16 图像，帧时间不规则,并带有
四个位置样本，断言精确的像素和时间戳往返结果，并检查厘米到米的
转换。第二个集成测试从三个匹配的脉冲中恢复出一个已知的 1000-ppm 时钟漂移和 50-ms
偏移量。重复的时间戳、不匹配的帧数、缺失的时钟证据、
不一致的非线性脉冲以及缺失的时区都是会被拒绝的情况。映射关系是
TIFF 的 `(time,y,x)` 对应 NWB 的 `(time,x,y)`，这会针对每一个转置后的源页面明确检查。NWB Inspector 会因为宽度超过帧数，用一个关键的方向性启发式检测标记出这个简短的
fixture；报告会保留这一检查结果，并附加精确的帧/时间戳相等性证据。不会仅仅为了满足某个"最长轴"启发式规则就执行转置操作。

## 主要参考资料

- [NeuroConv TIFF 转换](https://neuroconv.readthedocs.io/en/stable/conversion_examples_gallery/imaging/tiff.html)
- [NeuroConv 时间对齐](https://neuroconv.readthedocs.io/en/stable/user_guide/temporal_alignment.html)
- [PyNWB](https://github.com/NeurodataWithoutBorders/pynwb)
- [NWB Inspector 及其与 schema 验证的关系](https://github.com/NeurodataWithoutBorders/nwbinspector)
