---
name: pydicom
description: Python库，用于处理DICOM（医学数字成像和通信）文件。当读取、写入或修改DICOM格式的医学成像数据，从医学图像（CT、MRI、X光、超声）中提取像素数据，匿名化DICOM文件，处理DICOM元数据和标签，将DICOM图像转换为其他格式，处理压缩的DICOM数据，或处理医学成像数据集时使用此技能。适用于涉及医学图像分析、PACS系统、放射学工作流程和医疗成像应用的任务。
license: https://github.com/pydicom/pydicom/blob/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
---

# Pydicom

## 概述

Pydicom是一个纯Python包，用于处理DICOM文件，这是医学成像数据的标准格式。此技能提供有关读取、写入和操作DICOM文件的指导，包括处理像素数据、元数据和各种压缩格式。

## 使用场景

当处理以下内容时使用此技能：
- 医学成像文件（CT、MRI、X光、超声、PET等）
- 需要提取或修改元数据的DICOM数据集
- 从医学扫描中提取像素数据和图像处理
- 用于研究或数据共享的DICOM匿名化
- 将DICOM文件转换为标准图像格式
- 需要解压缩的压缩DICOM数据
- DICOM序列和结构化报告
- 多切片体积重建
- PACS（图片存档和通信系统）集成

## 安装

安装pydicom和常见依赖：

```bash
uv pip install pydicom
uv pip install pillow  # 用于图像格式转换
uv pip install numpy   # 用于像素数组操作
uv pip install matplotlib  # 用于可视化
```

对于处理压缩的DICOM文件，可能需要额外的包：

```bash
uv pip install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg  # JPEG压缩
uv pip install python-gdcm  # 替代压缩处理程序
```

## 核心工作流程

### 读取DICOM文件

使用`pydicom.dcmread()`读取DICOM文件：

```python
import pydicom

# 读取DICOM文件
ds = pydicom.dcmread('path/to/file.dcm')

# 访问元数据
print(f"Patient Name: {ds.PatientName}")
print(f"Study Date: {ds.StudyDate}")
print(f"Modality: {ds.Modality}")

# 显示所有元素
print(ds)
```

**关键点：**
- `dcmread()`返回一个`Dataset`对象
- 使用属性表示法（例如，`ds.PatientName`）或标签表示法（例如，`ds[0x0010, 0x0010]`）访问数据元素
- 使用`ds.file_meta`访问文件元数据，如传输语法UID
- 使用`getattr(ds, 'AttributeName', default_value)`或`hasattr(ds, 'AttributeName')`处理缺失属性

### 处理像素数据

从DICOM文件中提取和操作图像数据：

```python
import pydicom
import numpy as np
import matplotlib.pyplot as plt

# 读取DICOM文件
ds = pydicom.dcmread('image.dcm')

# 获取像素数组（需要numpy）
pixel_array = ds.pixel_array

# 图像信息
print(f"Shape: {pixel_array.shape}")
print(f"Data type: {pixel_array.dtype}")
print(f"Rows: {ds.Rows}, Columns: {ds.Columns}")

# 应用窗宽窗位进行显示（CT/MRI）
if hasattr(ds, 'WindowCenter') and hasattr(ds, 'WindowWidth'):
    from pydicom.pixel_data_handlers.util import apply_voi_lut
    windowed_image = apply_voi_lut(pixel_array, ds)
else:
    windowed_image = pixel_array

# 显示图像
plt.imshow(windowed_image, cmap='gray')
plt.title(f"{ds.Modality} - {ds.StudyDescription}")
plt.axis('off')
plt.show()
```

**处理彩色图像：**

```python
# RGB图像的形状为 (rows, columns, 3)
if ds.PhotometricInterpretation == 'RGB':
    rgb_image = ds.pixel_array
    plt.imshow(rgb_image)
elif ds.PhotometricInterpretation == 'YBR_FULL':
    from pydicom.pixel_data_handlers.util import convert_color_space
    rgb_image = convert_color_space(ds.pixel_array, 'YBR_FULL', 'RGB')
    plt.imshow(rgb_image)
```

**多帧图像（视频/序列）：**

```python
# 对于多帧DICOM文件
if hasattr(ds, 'NumberOfFrames') and ds.NumberOfFrames > 1:
    frames = ds.pixel_array  # 形状: (num_frames, rows, columns)
    print(f"Number of frames: {frames.shape[0]}")

    # 显示特定帧
    plt.imshow(frames[0], cmap='gray')
```

### 将DICOM转换为图像格式

使用提供的`dicom_to_image.py`脚本或手动转换：

```python
from PIL import Image
import pydicom
import numpy as np

ds = pydicom.dcmread('input.dcm')
pixel_array = ds.pixel_array

# 归一化到0-255范围
if pixel_array.dtype != np.uint8:
    pixel_array = ((pixel_array - pixel_array.min()) /
                   (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)

# 保存为PNG
image = Image.fromarray(pixel_array)
image.save('output.png')
```

使用脚本：`python scripts/dicom_to_image.py input.dcm output.png`

### 修改元数据

修改DICOM数据元素：

```python
import pydicom
from datetime import datetime

ds = pydicom.dcmread('input.dcm')

# 修改现有元素
ds.PatientName = "Doe^John"
ds.StudyDate = datetime.now().strftime('%Y%m%d')
ds.StudyDescription = "Modified Study"

# 添加新元素
ds.SeriesNumber = 1
ds.SeriesDescription = "New Series"

# 移除元素
if hasattr(ds, 'PatientComments'):
    delattr(ds, 'PatientComments')
# 或使用del
if 'PatientComments' in ds:
    del ds.PatientComments

# 保存修改后的文件
ds.save_as('modified.dcm')
```

### 匿名化DICOM文件

移除或替换患者识别信息：

```python
import pydicom
from datetime import datetime

ds = pydicom.dcmread('input.dcm')

# 通常包含PHI（受保护健康信息）的标签
tags_to_anonymize = [
    'PatientName', 'PatientID', 'PatientBirthDate',
    'PatientSex', 'PatientAge', 'PatientAddress',
    'InstitutionName', 'InstitutionAddress',
    'ReferringPhysicianName', 'PerformingPhysicianName',
    'OperatorsName', 'StudyDescription', 'SeriesDescription',
]

# 移除或替换敏感数据
for tag in tags_to_anonymize:
    if hasattr(ds, tag):
        if tag in ['PatientName', 'PatientID']:
            setattr(ds, tag, 'ANONYMOUS')
        elif tag == 'PatientBirthDate':
            setattr(ds, tag, '19000101')
        else:
            delattr(ds, tag)

# 更新日期以保持时间关系
if hasattr(ds, 'StudyDate'):
    # 按随机偏移量移动日期
    ds.StudyDate = '20000101'

# 保持像素数据不变
ds.save_as('anonymized.dcm')
```

使用提供的脚本：`python scripts/anonymize_dicom.py input.dcm output.dcm`

### 写入DICOM文件

从头创建DICOM文件：

```python
import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
import numpy as np

# 创建文件元信息
file_meta = Dataset()
file_meta.MediaStorageSOPClassUID = pydicom.uid.generate_uid()
file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

# 创建FileDataset实例
ds = FileDataset('new_dicom.dcm', {}, file_meta=file_meta, preamble=b"\0" * 128)

# 添加必需的DICOM元素
ds.PatientName = "Test^Patient"
ds.PatientID = "123456"
ds.Modality = "CT"
ds.StudyDate = datetime.now().strftime('%Y%m%d')
ds.StudyTime = datetime.now().strftime('%H%M%S')
ds.ContentDate = ds.StudyDate
ds.ContentTime = ds.StudyTime

# 添加图像特定元素
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"
ds.Rows = 512
ds.Columns = 512
ds.BitsAllocated = 16
ds.BitsStored = 16
ds.HighBit = 15
ds.PixelRepresentation = 0

# 创建像素数据
pixel_array = np.random.randint(0, 4096, (512, 512), dtype=np.uint16)
ds.PixelData = pixel_array.tobytes()

# 添加必需的UID
ds.SOPClassUID = pydicom.uid.CTImageStorage
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.SeriesInstanceUID = pydicom.uid.generate_uid()
ds.StudyInstanceUID = pydicom.uid.generate_uid()

# 保存文件
ds.save_as('new_dicom.dcm')
```

### 压缩和解压缩

处理压缩的DICOM文件：

```python
import pydicom

# 读取压缩的DICOM文件
ds = pydicom.dcmread('compressed.dcm')

# 检查传输语法
print(f"Transfer Syntax: {ds.file_meta.TransferSyntaxUID}")
print(f"Transfer Syntax Name: {ds.file_meta.TransferSyntaxUID.name}")

# 解压缩并保存为未压缩
ds.decompress()
ds.save_as('uncompressed.dcm', write_like_original=False)

# 或在保存时压缩（需要适当的编码器）
ds_uncompressed = pydicom.dcmread('uncompressed.dcm')
ds_uncompressed.compress(pydicom.uid.JPEGBaseline8Bit)
ds_uncompressed.save_as('compressed_jpeg.dcm')
```

**常见传输语法：**
- `ExplicitVRLittleEndian` - 未压缩，最常见
- `JPEGBaseline8Bit` - JPEG有损压缩
- `JPEGLossless` - JPEG无损压缩
- `JPEG2000Lossless` - JPEG 2000无损
- `RLELossless` - 游程编码无损

完整列表见`references/transfer_syntaxes.md`。

### 处理DICOM序列

处理嵌套数据结构：

```python
import pydicom

ds = pydicom.dcmread('file.dcm')

# 访问序列
if 'ReferencedStudySequence' in ds:
    for item in ds.ReferencedStudySequence:
        print(f"Referenced SOP Instance UID: {item.ReferencedSOPInstanceUID}")

# 创建序列
from pydicom.sequence import Sequence

sequence_item = Dataset()
sequence_item.ReferencedSOPClassUID = pydicom.uid.CTImageStorage
sequence_item.ReferencedSOPInstanceUID = pydicom.uid.generate_uid()
ds.ReferencedImageSequence = Sequence([sequence_item])
```

### 处理DICOM序列

处理多个相关的DICOM文件：

```python
import pydicom
import numpy as np
from pathlib import Path

# 读取目录中的所有DICOM文件
dicom_dir = Path('dicom_series/')
slices = []

for file_path in dicom_dir.glob('*.dcm'):
    ds = pydicom.dcmread(file_path)
    slices.append(ds)

# 按切片位置或实例编号排序
slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
# 或: slices.sort(key=lambda x: int(x.InstanceNumber))

# 创建3D体积
volume = np.stack([s.pixel_array for s in slices])
print(f"Volume shape: {volume.shape}")  # (num_slices, rows, columns)

# 获取用于适当缩放的间距信息
pixel_spacing = slices[0].PixelSpacing  # [row_spacing, col_spacing]
slice_thickness = slices[0].SliceThickness
print(f"Voxel size: {pixel_spacing[0]}x{pixel_spacing[1]}x{slice_thickness} mm")
```

## 辅助脚本

此技能在`scripts/`目录中包含实用脚本：

### anonymize_dicom.py
通过移除或替换受保护健康信息（PHI）来匿名化DICOM文件。

```bash
python scripts/anonymize_dicom.py input.dcm output.dcm
```

### dicom_to_image.py
将DICOM文件转换为常见图像格式（PNG、JPEG、TIFF）。

```bash
python scripts/dicom_to_image.py input.dcm output.png
python scripts/dicom_to_image.py input.dcm output.jpg --format JPEG
```

### extract_metadata.py
以可读格式提取和显示DICOM元数据。

```bash
python scripts/extract_metadata.py file.dcm
python scripts/extract_metadata.py file.dcm --output metadata.txt
```

## 参考资料

详细参考信息可在`references/`目录中找到：

- **common_tags.md**：按类别（患者、研究、序列、图像等）组织的常用DICOM标签的综合列表
- **transfer_syntaxes.md**：DICOM传输语法和压缩格式的完整参考

## 常见问题和解决方案

**问题："Unable to decode pixel data"**
- 解决方案：安装额外的压缩处理程序：`uv pip install pylibjpeg pylibjpeg-libjpeg python-gdcm`

**问题：访问标签时出现"AttributeError"**
- 解决方案：使用`hasattr(ds, 'AttributeName')`或`ds.get('AttributeName', default)`检查属性是否存在

**问题：图像显示不正确（太暗/太亮）**
- 解决方案：应用VOI LUT窗宽窗位：`apply_voi_lut(pixel_array, ds)`或使用`WindowCenter`和`WindowWidth`手动调整

**问题：大型序列的内存问题**
- 解决方案：迭代处理文件，使用内存映射数组，或对图像进行下采样

## 最佳实践

1. **在访问属性之前始终检查**，使用`hasattr()`或`get()`
2. **保存文件时保留文件元数据**，使用`save_as()`并设置`write_like_original=True`
3. **使用传输语法UID**在处理像素数据之前了解压缩格式
4. **处理来自不可信来源的文件时处理异常**
5. **对医学图像可视化应用适当的窗宽窗位**（VOI LUT）
6. **处理3D体积时保持空间信息**（像素间距，切片厚度）
7. **在共享医学数据之前彻底验证匿名化**
8. **正确使用UID** - 创建新实例时生成新UID，修改时保留它们

## 文档

官方pydicom文档：https://pydicom.github.io/pydicom/dev/
- 用户指南：https://pydicom.github.io/pydicom/dev/guides/user/index.html
- 教程：https://pydicom.github.io/pydicom/dev/tutorials/index.html
- API参考：https://pydicom.github.io/pydicom/dev/reference/index.html
- 示例：https://pydicom.github.io/pydicom/dev/auto_examples/index.html