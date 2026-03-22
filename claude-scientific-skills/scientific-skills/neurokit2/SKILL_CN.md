---
name: neurokit2
description: 用于分析生理数据的综合生物信号处理工具包,包括ECG、EEG、EDA、RSP、PPG、EMG和EOG信号。在处理心血管信号、大脑活动、电皮层反应、呼吸模式、肌肉活动或眼球运动时使用此技能。适用于心率变异性分析、事件相关电位、复杂性测量、自主神经系统评估、心理生理学研究以及多模态生理信号集成。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# NeuroKit2

## 概述

NeuroKit2是一个用于处理和分析生理信号(生物信号)的综合Python工具包。使用此技能处理心血管、神经、自主神经、呼吸和肌肉信号,用于心理生理学研究、临床应用和人机交互研究。

## 何时使用此技能

在处理以下内容时应用此技能:
- **心脏信号**: ECG、PPG、心率变异性(HRV)、脉搏分析
- **大脑信号**: EEG频带、微状态、复杂性、源定位
- **自主神经信号**: 电皮层活动(EDA/GSR)、皮肤电导反应(SCR)
- **呼吸信号**: 呼吸频率、呼吸变异性(RRV)、单位时间体积
- **肌肉信号**: EMG振幅、肌肉激活检测
- **眼动追踪**: EOG、眨眼检测和分析
- **多模态集成**: 同时处理多个生理信号
- **复杂性分析**: 熵测量、分形维数、非线性动力学

## 核心功能

### 1. 心脏信号处理(ECG/PPG)

处理心电图和光电容积描记信号以进行心血管分析。详见`references/ecg_cardiac.md`获取详细工作流程。

**主要工作流程:**
- ECG处理管道: 清理 → R峰检测 → 描记 → 质量评估
- 跨时域、频域和非线性域的HRV分析
- PPG脉搏分析和质量评估
- ECG衍生呼吸提取

**关键函数:**
```python
import neurokit2 as nk

# 完整ECG处理管道
signals, info = nk.ecg_process(ecg_signal, sampling_rate=1000)

# 分析ECG数据(事件相关或区间相关)
analysis = nk.ecg_analyze(signals, sampling_rate=1000)

# 综合HRV分析
hrv = nk.hrv(peaks, sampling_rate=1000)  # 时域、频域、非线性域
```

### 2. 心率变异性分析

从心脏信号计算综合HRV指标。详见`references/hrv.md`获取所有指标和特定领域分析。

**支持的域:**
- **时域**: SDNN、RMSSD、pNN50、SDSD和衍生指标
- **频域**: ULF、VLF、LF、HF、VHF功率和比率
- **非线性域**: Poincaré图(SD1/SD2)、熵测量、分形维数
- **专用**: 呼吸性窦性心律不齐(RSA)、递归量化分析(RQA)

**关键函数:**
```python
# 一次获取所有HRV指标
hrv_indices = nk.hrv(peaks, sampling_rate=1000)

# 特定域分析
hrv_time = nk.hrv_time(peaks)
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000)
hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=1000)
hrv_rsa = nk.hrv_rsa(peaks, rsp_signal, sampling_rate=1000)
```

### 3. 脑信号分析(EEG)

分析脑电图信号以进行频率功率、复杂性和微状态模式分析。详见`references/eeg.md`获取详细工作流程和MNE集成。

**主要功能:**
- 频带功率分析(Delta、Theta、Alpha、Beta、Gamma)
- 通道质量评估和重参考
- 源定位(sLORETA、MNE)
- 微状态分割和转换动力学
- 全局场功率和相异性测量

**关键函数:**
```python
# 跨频带功率分析
power = nk.eeg_power(eeg_data, sampling_rate=250, channels=['Fz', 'Cz', 'Pz'])

# 微状态分析
microstates = nk.microstates_segment(eeg_data, n_microstates=4, method='kmod')
static = nk.microstates_static(microstates)
dynamic = nk.microstates_dynamic(microstates)
```

### 4. 电皮层活动(EDA)

处理皮肤电导信号以进行自主神经系统评估。详见`references/eda.md`获取详细工作流程。

**主要工作流程:**
- 信号分解为紧张性和时相性成分
- 皮肤电导反应(SCR)检测和分析
- 交感神经系统指数计算
- 自相关和变点检测

**关键函数:**
```python
# 完整EDA处理
signals, info = nk.eda_process(eda_signal, sampling_rate=100)

# 分析EDA数据
analysis = nk.eda_analyze(signals, sampling_rate=100)

# 交感神经系统活动
sympathetic = nk.eda_sympathetic(signals, sampling_rate=100)
```

### 5. 呼吸信号处理(RSP)

分析呼吸模式和呼吸变异性。详见`references/rsp.md`获取详细工作流程。

**主要功能:**
- 呼吸频率计算和变异性分析
- 呼吸幅度和对称性评估
- 单位时间呼吸体积(fMRI应用)
- 呼吸幅度变异性(RAV)

**关键函数:**
```python
# 完整RSP处理
signals, info = nk.rsp_process(rsp_signal, sampling_rate=100)

# 呼吸频率变异性
rrv = nk.rsp_rrv(signals, sampling_rate=100)

# 单位时间呼吸体积
rvt = nk.rsp_rvt(signals, sampling_rate=100)
```

### 6. 肌电图(EMG)

处理肌肉活动信号以进行激活检测和振幅分析。详见`references/emg.md`获取工作流程。

**关键函数:**
```python
# 完整EMG处理
signals, info = nk.emg_process(emg_signal, sampling_rate=1000)

# 肌肉激活检测
activation = nk.emg_activation(signals, sampling_rate=1000, method='threshold')
```

### 7. 眼电图(EOG)

分析眼球运动和眨眼模式。详见`references/eog.md`获取工作流程。

**关键函数:**
```python
# 完整EOG处理
signals, info = nk.eog_process(eog_signal, sampling_rate=500)

# 提取眨眼特征
features = nk.eog_features(signals, sampling_rate=500)
```

### 8. 通用信号处理

对任何信号应用滤波、分解和变换操作。详见`references/signal_processing.md`获取综合实用程序。

**主要操作:**
- 滤波(低通、高通、带通、带阻)
- 分解(EMD、SSA、小波)
- 峰值检测和校正
- 功率谱密度估计
- 信号插值和重采样
- 自相关和同步分析

**关键函数:**
```python
# 滤波
filtered = nk.signal_filter(signal, sampling_rate=1000, lowcut=0.5, highcut=40)

# 峰值检测
peaks = nk.signal_findpeaks(signal)

# 功率谱密度
psd = nk.signal_psd(signal, sampling_rate=1000)
```

### 9. 复杂性和熵分析

计算非线性动力学、分形维数和信息论测量。详见`references/complexity.md`获取所有可用指标。

**可用测量:**
- **熵**: Shannon、近似、样本、排列、谱、模糊、多尺度
- **分形维数**: Katz、Higuchi、Petrosian、Sevcik、相关维数
- **非线性动力学**: Lyapunov指数、Lempel-Ziv复杂性、递归量化
- **DFA**: 去趋势波动分析、多重分形DFA
- **信息论**: Fisher信息、互信息

**关键函数:**
```python
# 一次获取多个复杂性指标
complexity_indices = nk.complexity(signal, sampling_rate=1000)

# 特定测量
apen = nk.entropy_approximate(signal)
dfa = nk.fractal_dfa(signal)
lyap = nk.complexity_lyapunov(signal, sampling_rate=1000)
```

### 10. 事件相关分析

在刺激事件周围创建epoch并分析生理反应。详见`references/epochs_events.md`获取工作流程。

**主要功能:**
- 从事件标记创建epoch
- 事件相关平均和可视化
- 基线校正选项
- 具有置信区间的总平均计算

**关键函数:**
```python
# 在信号中查找事件
events = nk.events_find(trigger_signal, threshold=0.5)

# 在事件周围创建epoch
epochs = nk.epochs_create(signals, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# 跨epoch平均
grand_average = nk.epochs_average(epochs)
```

### 11. 多信号集成

以统一输出同时处理多个生理信号。详见`references/bio_module.md`获取集成工作流程。

**关键函数:**
```python
# 一次处理多个信号
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    emg=emg_signal,
    sampling_rate=1000
)

# 分析所有处理后的信号
bio_analysis = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

## 分析模式

NeuroKit2根据数据持续时间自动在两种分析模式之间选择:

**事件相关分析**(< 10秒):
- 分析刺激锁定的反应
- 基于epoch的分割
- 适用于具有离散试验的实验范式

**区间相关分析**(≥ 10秒):
- 表征长期生理模式
- 静息状态或连续活动
- 适用于基线测量和长期监测

大多数`*_analyze()`函数自动选择适当的模式。

## 安装

```bash
uv pip install neurokit2
```

对于开发版本:
```bash
uv pip install https://github.com/neuropsychology/NeuroKit/zipball/dev
```

## 常见工作流程

### 快速开始: ECG分析
```python
import neurokit2 as nk

# 加载示例数据
ecg = nk.ecg_simulate(duration=60, sampling_rate=1000)

# 处理ECG
signals, info = nk.ecg_process(ecg, sampling_rate=1000)

# 分析HRV
hrv = nk.hrv(info['ECG_R_Peaks'], sampling_rate=1000)

# 可视化
nk.ecg_plot(signals, info)
```

### 多模态分析
```python
# 处理多个信号
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    sampling_rate=1000
)

# 分析所有信号
results = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

### 事件相关电位
```python
# 查找事件
events = nk.events_find(trigger_channel, threshold=0.5)

# 创建epoch
epochs = nk.epochs_create(processed_signals, events,
                          sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# 每种信号类型的事件相关分析
ecg_epochs = nk.ecg_eventrelated(epochs)
eda_epochs = nk.eda_eventrelated(epochs)
```

## 参考

此技能包括按信号类型和分析方法组织的综合参考文档:

- **ecg_cardiac.md**: ECG/PPG处理、R峰检测、描记、质量评估
- **hrv.md**: 所有域的心率变异性指标
- **eeg.md**: EEG分析、频带、微状态、源定位
- **eda.md**: 电皮层活动处理和SCR分析
- **rsp.md**: 呼吸信号处理和变异性
- **ppg.md**: 光电容积描记信号分析
- **emg.md**: 肌电图处理和激活检测
- **eog.md**: 眼电图和眨眼分析
- **signal_processing.md**: 通用信号实用程序和变换
- **complexity.md**: 熵、分形和非线性测量
- **epochs_events.md**: 事件相关分析和epoch创建
- **bio_module.md**: 多信号集成工作流程

根据需要使用Read工具加载特定的参考文件,以访问详细的函数文档和参数。

## 其他资源

- 官方文档: https://neuropsychology.github.io/NeuroKit/
- GitHub仓库: https://github.com/neuropsychology/NeuroKit
- 发表论文: Makowski et al. (2021). NeuroKit2: A Python toolbox for neurophysiological signal processing. Behavior Research Methods. https://doi.org/10.3758/s13428-020-01516-y
