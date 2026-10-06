---
name: openpiv
description: 使用 OpenPIV 进行粒子图像测速（PIV）分析。适用于从 PIV 图像对中提取速度场、分析流体动力学或流动可视化实验、对判读窗口进行互相关、验证并替换伪 PIV 矢量，或根据测得的速度场计算涡量、应变率和湍流统计量。
license: BSD-3-Clause
compatibility: Requires Python 3.10+ with openpiv installed (uv pip install openpiv). numpy, scipy, scikit-image, and matplotlib arrive as dependencies. No network access needed after install.
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.3"
  skill-author: OpenPIV Team
  tested-against: "openpiv 0.26.1"
  last-reviewed: "2026-10-01"
---

# OpenPIV

## 概述

OpenPIV（Open Particle Image Velocimetry，开源粒子图像测速）用于从 PIV 图像对中分析流体流动。它涵盖
预处理、互相关、矢量验证、异常值替换、平滑以及换算到物理单位。

目标版本为 **openpiv 0.26.1**。合成数据检查在 Python 3.13、NumPy 2.5.3、SciPy 1.18.1、
scikit-image 0.26.0 和 Matplotlib 3.11.2 上运行。未安装 Rust；经过测试的路径请使用 `backend="scipy"`。
参见[审查证据](references/advanced_algorithms.md#review-sources-and-verification)。

## 何时使用

在处理实验 PIV 或流动可视化图像对时使用此技能：测量二维
速度场、调整判读窗口参数、验证矢量，或推导涡量、
应变率和湍流统计量。如果是要*模拟*流动而非测量流动，请改用 CFD
技能。

## 快速开始

安装 OpenPIV：

```bash
uv pip install openpiv

# 当分析需要可复现时固定版本——下面每个代码片段
# 都是针对该版本检查的。
uv pip install "openpiv==0.26.1"
```

对一个图像对运行 PIV 分析：

```python
import numpy as np
from openpiv import tools, pyprocess, validation, filters, scaling

frame_a = tools.imread("image_a.bmp")
frame_b = tools.imread("image_b.bmp")

# 始终返回 (u, v, s2n)；若 sig2noise_method=None，则 s2n 全为 NaN。
u, v, s2n = pyprocess.extended_search_area_piv(
    frame_a.astype(np.float32),
    frame_b.astype(np.float32),
    window_size=32,
    overlap=12,
    dt=0.02,
    search_area_size=38,
    correlation_method="linear",   # circular 也支持扩展搜索
    normalized_correlation=True,
    backend="scipy",
    sig2noise_method="peak2peak",
)

x, y = pyprocess.get_coordinates(
    image_size=frame_a.shape,
    search_area_size=38,
    overlap=12,
    center_on_field=False,         # 与滑动窗口位置一致
)

# flags 是布尔数组：True 表示伪矢量。
flags = validation.sig2noise_val(s2n, threshold=1.05) | ~np.isfinite(s2n)
flags |= ~np.isfinite(u) | ~np.isfinite(v)
u, v = filters.replace_outliers(u, v, flags, method="localmean", max_iter=3, kernel_size=2)

# 先缩放，再转换为右手系的图像边界坐标。
x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor=96.52)
y, v = frame_a.shape[0] / 96.52 - y, -v

tools.save("vectors.txt", x, y, u, v, flags)
```

或者使用附带的 CLI，它还会检查输入并保留掩膜和处理参数：

```bash
python skills/openpiv/scripts/runner.py \
    --image frame_a.bmp --image frame_b.bmp --output_dir results --verbose
```

## 核心概念

### PIV 基础

粒子图像测速是一种光学方法，通过在两幅图像之间追踪被照亮的
示踪粒子来测量流体速度。

**处理流程：**

1. 采集一对图像（`frame_a`、`frame_b`），二者间隔已知时间 `dt`。
2. 将图像划分为判读窗口。
3. 对匹配窗口进行互相关以找到峰值位移。
4. 验证矢量（信噪比、全局范围、局部中值）。
5. 用插值替换伪矢量。
6. 将像素位移换算为物理单位。

### 判读窗口参数

**`window_size`**——以像素为单位的相关窗口（通常为 16–128）。窗口越大，
相关性越好，但空间分辨率越粗。

**`overlap`**——相邻窗口之间共享的像素数（通常为 `window_size` 的 50–75%）。
重叠越高，矢量密度和计算开销越大，但相邻矢量会变得相关而非
相互独立。

**`search_area_size`**——在第二帧中搜索的窗口。必须 ≥ `window_size`；大几个
像素即可容纳更大的位移。`"circular"` 和 `"linear"` 都支持扩展
搜索。CLI 为此选择零填充的 `"linear"` 并设置 `normalized_correlation=True`；这
并不能恢复任意位移，也不能消除伪峰。网格步长为
`search_area_size - overlap`，因此 overlap 必须小于搜索区域。

经验法则：最大位移应保持在 `window_size` 的约四分之一以下，并力求
每个窗口包含 5–10 个粒子。

### 信噪比

`s2n` 衡量相关峰的显著程度。`sig2noise_method` 控制其计算方式——
`"peak2mean"`（函数默认值）或 `"peak2peak"`。**两者的量纲尺度不同**，因此
为其中一种调好的阈值对另一种毫无意义。典型的 `peak2peak` 阈值为 1.05–1.3。

```python
flags = validation.sig2noise_val(s2n, threshold=1.05)
# flags 为布尔型：True == 伪矢量。`~flags` 选出有效矢量。
```

## 常用操作

### 动态掩膜

掩膜功能位于 `openpiv.preprocess` 中，返回 `(image, mask)`。请使用浮点副本，
以避免无符号减法产生的伪影。分析前请检查两帧上的掩膜。

```python
from openpiv import preprocess

# 强度掩膜使用 Otsu 方法；threshold 参数用于边缘方法。
frame_a_masked, mask_a = preprocess.dynamic_masking(
    frame_a.astype(np.float64), method="intensity", filter_size=7, threshold=0.005
)
frame_b_masked, mask_b = preprocess.dynamic_masking(
    frame_b.astype(np.float64), method="intensity", filter_size=7, threshold=0.005
)
```

将并集 `mask_a | mask_b` 作为被排除的物理区域保留下来。CLI 会在
判读中心处对其采样、保存，并在替换后保持这些速度为 NaN。跨越
物体的窗口仍可能存在偏差：请针对实验检查/膨胀掩膜。在 0.26.1 中，
`method="edges"` 使用 uint8 而非 bool 进行索引，可能会损坏图像或直接失败。
CLI 会拒绝它；在自定义工作流中请使用强度掩膜或经过验证的布尔掩膜。

### 多遍处理

多遍处理（窗口变形）位于 `openpiv.windef` 中，由 `PIVSettings` 数据类驱动。
`pyprocess` 没有多遍处理入口。

```python
import numpy as np
from openpiv import scaling, windef

settings = windef.PIVSettings(
    windowsizes=(64, 32, 16), overlap=(32, 16, 8), num_iterations=3,
    backend="scipy", sig2noise_method="peak2peak", sig2noise_threshold=1.05,
)

x, y, u, v, flags = windef.simple_multipass(
    frame_a.astype(np.float32), frame_b.astype(np.float32), settings
)

# 输出单位为“像素/帧”——需自行转换。scaling.uniform 只会除以
# scaling_factor，因此需单独处理 dt。
dt = 0.02
x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor=96.52)
u, v = u / dt, v / dt
```

`simple_multipass` 会进行验证、替换异常值、用零填充剩余的 NaN，并变换
坐标。请保留它的 flags：修复/零填充后的输出并不是独立的测量值。
务必传入 settings：在 0.26.1 中，其不传 settings 的路径有两个窗口尺寸却有三次迭代。

**单位陷阱：** `simple_multipass` 及其别名 `multigrid_windef` 会忽略 `settings.dt` 和
`settings.scaling_factor`；请按上文方式转换其数组。批处理 `windef.piv(settings)` 会在保存前
同时应用这两者——不要再次缩放其输出文件。简单封装函数并不遵循所有批处理
预处理/输出开关。

若要控制每一遍处理，`windef.first_pass` 和 `windef.multipass_img_deform` 是
更底层的构建模块。

## 验证与后处理

### 验证方法

每个验证器都返回一个布尔数组，其中 **True 表示伪矢量**。同时也要剔除
非有限值的 `u`、`v` 和 `s2n`：仅靠 `sig2noise_val` 不会标记 NaN。

```python
# 信噪比
flags = validation.sig2noise_val(s2n, threshold=1.05)

# 全局范围——接收 (min, max) 元组，可按位置传入，或作为 u_thresholds/v_thresholds 传入。
flags = validation.global_val(u, v, (-300, 300), (-300, 300))

# 局部中值——u_threshold 和 v_threshold 为必需参数；size 是邻域半宽。
flags = validation.local_median_val(u, v, u_threshold=30.0, v_threshold=30.0, size=1)

# 用布尔 OR 组合（不要用 np.maximum——这些是布尔数组）。
flags = (
    validation.sig2noise_val(s2n, threshold=1.05)
    | validation.global_val(u, v, (-300, 300), (-300, 300))
    | validation.local_median_val(u, v, u_threshold=30.0, v_threshold=30.0)
)
```

**请以 `u` 和 `v` 的单位设置这些阈值，而不是以像素/帧为单位。**
`extended_search_area_piv` 会除以 `dt`，因此当 `dt=0.02` 时，3 px/帧的位移会变成
150 px/s。上面的阈值适用于这种情况；PIV 文献和
`PIVSettings.min_max_u_disp` 使用的 `(-30, 30)` 是 px/帧的限值，把它应用于 px/s 输出会剔除
整个场。可以用 `dt=1` 进行相关，在转换前验证位移；或者将
阈值调整为实际的速度单位（同时考虑时间和标定系数）。

### 异常值替换

```python
u, v = filters.replace_outliers(
    u, v, flags, method="localmean", max_iter=3, tol=1e-3, kernel_size=2
)
```

`method` 接受 `"localmean"`、`"disk"` 或 `"distance"`；在填充缺失单元时，无效名称会引发 `ValueError`。
对 `"distance"` 请使用 `kernel_size>=2`：在 0.26.1 中，size 为 1 会把所有邻居
权重截断为零并留下空洞。替换会用插值*填充*被标记的
位置——如果你随后又用 NaN 覆盖它们，替换就白做了。二者择一：

```python
# 将被标记的矢量完全排除在分析之外，而不是对其插值。
u = np.where(flags, np.nan, u)
v = np.where(flags, np.nan, v)
```

### 平滑

平滑函数是 `openpiv.smoothn.smoothn`；不存在 `openpiv.smooth` 模块。它返回一个元组，
第一个元素是平滑后的场。NaN/Inf 被视为缺失观测；请传入副本，因为
它可能会修改输入。先把空洞填零会错误地将其视为测得的零值。

```python
from openpiv.smoothn import smoothn

u_smooth, *_ = smoothn(np.asarray(u, dtype=float).copy(), s=0.5)  # 越大越平滑
v_smooth, *_ = smoothn(np.asarray(v, dtype=float).copy(), s=0.5)
u_smooth = np.asarray(u_smooth)
```

## 可视化

### 矢量场绘图

`display_vector_field` 读取已保存的矢量文件，并在内部调用 `plt.show()`，因此批量运行时请选择
非交互式后端。

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpiv import tools

fig, ax = plt.subplots(figsize=(8, 8))
tools.display_vector_field(
    "vectors.txt",
    ax=ax,
    scaling_factor=96.52,   # 与 scaling.uniform 中使用的系数相同，用于映射回图像
    scale=50,
    width=0.0035,
    on_img=False,
)
image = tools.imread("frame_a.bmp")
height, width = image.shape
ax.imshow(image, cmap="gray", origin="upper", zorder=-1,
          extent=(0, width / 96.52, 0, height / 96.52))
fig.savefig("vector_field.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

请显式设置图像范围：该辅助函数的 `on_img=True` 会根据最后一个矢量推断范围，
当窗口留下未使用的边距时可能导致叠加图被拉伸。CLI 使用实际的图像边界绘图。

### 自定义可视化

```python
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

mag = np.sqrt(u**2 + v**2)
for ax, field, title, cmap in [
    (axes[0], mag, "Velocity Magnitude", "viridis"),
    (axes[1], u, "U Velocity", "RdBu_r"),
    (axes[2], v, "V Velocity", "RdBu_r"),
]:
    im = ax.imshow(field, cmap=cmap)
    ax.set_title(title)
    plt.colorbar(im, ax=ax)

fig.tight_layout()
fig.savefig("velocity_components.png")
plt.close(fig)
```

## 分析函数

`scripts/analyze.py` 针对由 `runner.py` 写出的 `params.npz` 打包提供了这些功能。它会根据
保存的坐标推断物理网格间距，因此导数是按单位长度计算的：

```python
import sys
sys.path.insert(0, "skills/openpiv/scripts")
from analyze import PIVAnalyzer

piv = PIVAnalyzer("results/params.npz")
vorticity = piv.compute_vorticity()          # dv/dx - du/dy
exx, eyy, exy = piv.compute_strain()
stats = piv.compute_statistics()             # 排除被标记和被掩膜的矢量
piv.plot_vector_field(save_path="quiver.png")
```

如果你更愿意内联计算，可以使用以下独立形式：

### 涡量

```python
def compute_vorticity(u, v, dx=1.0, dy=None):
    """Out-of-plane vorticity dv/dx - du/dy. Pass the physical grid spacing, not 1.0."""
    dy = dx if dy is None else dy
    return np.gradient(v, dx, axis=1) - np.gradient(u, dy, axis=0)
```

对于单遍扩展搜索网格，物理单位下的间距为
`(search_area_size - overlap) / scaling_factor`；只有当两个窗口尺寸相同时，它才简化为
`(window_size - overlap) / scaling_factor`。
优先使用已保存的 `x` 和 `y` 坐标的差值，尤其是在多遍
处理之后。保留 `dx=1.0` 得到的是每个网格单元的涡量，而不是每单位长度的涡量。
参见 [OpenPIV 坐标生成](https://openpiv.readthedocs.io/en/stable/src/tutorial1.html)。

**符号约定：** CLI 写入 `y = image_height / scaling_factor - y` 并对 `v` 取反，
同时保持行按图像顺序排列。保存的 `y` 沿数组向下递减。独立形式需要
带符号的 `dy`（此处为负），或者使用会读取方向的 `PIVAnalyzer`。正的 `dy` 会改变
y 方向导数的贡献，甚至可能抵消真实的旋转。

### 应变率

```python
def compute_strain(u, v, dx=1.0, dy=None):
    """Return (exx, eyy, exy) of the 2D strain-rate tensor."""
    dy = dx if dy is None else dy
    du_dx = np.gradient(u, dx, axis=1)
    du_dy = np.gradient(u, dy, axis=0)
    dv_dx = np.gradient(v, dx, axis=1)
    dv_dy = np.gradient(v, dy, axis=0)
    return du_dx, dv_dy, 0.5 * (du_dy + dv_dx)
```

### 湍流统计量

```python
def compute_statistics(u, v):
    """Single-frame spatial statistics. NOT Reynolds decomposition."""
    u_prime = u - np.nanmean(u)
    v_prime = v - np.nanmean(v)
    rms_u, rms_v = np.nanstd(u_prime), np.nanstd(v_prime)
    return {
        "u_mean": np.nanmean(u),
        "v_mean": np.nanmean(v),
        "rms_u": rms_u,
        "rms_v": rms_v,
        "tke": 0.5 * (rms_u**2 + rms_v**2),
    }
```

**注意：** 减去单帧的*空间*均值测得的是空间方差，只有在均匀性/遍历性假设
成立的前提下，它才等于湍流强度。雷诺分解
需要一个系综：从每个实现中减去系综平均场。遗留的 `tke` 键只是
两分量的空间方差能量，而不是完整的湍动能。分析器默认排除
被标记的矢量；`compute_statistics(include_interpolated=True)` 会包含修复后的矢量。

## CLI 用法

```bash
# 基本运行
python skills/openpiv/scripts/runner.py \
    --image img1.bmp --image img2.bmp --output_dir results --verbose

# 调整参数并使用动态掩膜
python skills/openpiv/scripts/runner.py \
    --image frame_a.bmp \
    --image frame_b.bmp \
    --output_dir results \
    --window_size 32 \
    --overlap 12 \
    --search_area 38 \
    --dt 0.02 \
    --scaling 96.52 \
    --threshold 1.05 \
    --mask dynamic \
    --mask_method intensity \
    --verbose
```

### CLI 选项

| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `--image` | 必需 | 图像文件；必须恰好指定两次以构成图像对 |
| `--output_dir` | `results` | 输出目录（不存在时创建） |
| `--window_size` | 32 | 判读窗口尺寸（px） |
| `--overlap` | 12 | 搜索网格重叠（px），非负且小于搜索区域 |
| `--search_area` | 38 | 搜索区域尺寸（px），必须 ≥ `--window_size` |
| `--dt` | 0.02 | 帧间时间（s） |
| `--scaling` | 96.52 | 缩放系数，每物理单位的像素数（例如 px/mm） |
| `--threshold` | 1.05 | `peak2peak` 信噪比阈值 |
| `--mask` | `none` | `none` 或 `dynamic`（`openpiv.preprocess.dynamic_masking`） |
| `--mask_method` | `intensity` | 在 0.26.1 中仅 intensity 可用；edges 会被拒绝 |
| `--backend` | `scipy` | `scipy`、`auto` 或 `rust`；Rust 需要其扩展 |
| `--drop_invalid` | 关 | 将被标记的矢量置为 NaN，而不是保留插值结果 |
| `--verbose` | 关 | 打印进度信息 |

使用 OpenPIV 自带的图像对端到端验证安装：

```bash
python skills/openpiv/scripts/run_example.py --output_dir /tmp/openpiv-demo
```

## 输出文件

- **vectors.txt**——制表符分隔，`%.4e` 格式，带有 `# x y u v flags mask` 注释表头
- **params.npz**——`x`、`y`、`u`、`v`、`flags`、`mask`、`s2n`、时间/标定/窗口参数、
  请求的后端以及 OpenPIV 版本。坐标使用物理单位；速度使用 单位/s。
- **vector_field.png**——绘制在第一帧上的矢量场

```text
# x	y	u	v	flags	mask
2.1757e-01	3.5226e+00	-6.2220e-02	-2.7081e+00	0.0000e+00	0.0000e+00
4.8695e-01	3.5226e+00	-3.1587e-01	-2.9800e+00	0.0000e+00	0.0000e+00
```

`flags` 为浮点数，`0` 表示有效，`1` 表示被标记。`mask=1` 表示被排除的物体区域，
与 flags 相互独立。请将两者与测得的场一起保留。

## 最佳实践

### 参数选择

1. **窗口尺寸**——32×32 适合大多数情况。64/128 以较粗的分辨率换取更好的相关性；
   16/24 以噪声为代价换取更细的分辨率。
2. **重叠**——窗口尺寸的 50–75%。
3. **阈值**——提高阈值可剔除更多矢量；切换
   `sig2noise_method` 后务必重新调整。
4. **缩放系数**——对照已知参照物（如标定网格）进行标定，并保持
   单位清晰（OpenPIV `test1` 教程数据中的 `96.52` 单位为 px/mm）。

### 图像质量

- 粒子清晰可见且分布均匀，每个判读窗口 5–10 个
- 没有饱和或过曝区域
- 背景噪声尽量小；可考虑对整个序列做背景扣除

### 处理技巧

1. 从默认值开始，然后根据得到的矢量场进行调整。
2. 检查 `s2n` 分布——中位数偏低意味着相关性差，而不是阈值不当。
3. 尽早可视化；明显的问题（均匀矢量、边缘伪影）会立即显现。
4. 对于速度梯度或位移较大的流动，使用多遍处理（`windef`）。
5. 对反光和固体边界进行掩膜，而不是让它们生成矢量。

## 资源

### references/

- `advanced_algorithms.md`——相关和亚像素方法、多遍窗口变形、
  `PIVSettings` 字段、三维和相分离模块

需要详细的算法或设置信息时，请加载该参考文件。
