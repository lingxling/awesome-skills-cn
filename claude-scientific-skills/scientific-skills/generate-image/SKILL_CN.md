---
name: generate-image
description: 使用DALL-E 3或Stable Diffusion生成图像。用于创建科学可视化、生成图表、创建插图或任何需要图像生成的任务。支持文本到图像、图像到图像、图像编辑和图像修复。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# 图像生成

## 概述

图像生成技能使用DALL-E 3（OpenAI）或Stable Diffusion（Stability AI）根据文本描述生成高质量图像。它支持多种生成模式，包括文本到图像、图像到图像、图像编辑和图像修复。

## 何时使用此技能

使用图像生成当：

- **创建科学可视化**：生成分子结构、细胞过程、生物系统的插图
- **生成图表**：创建流程图、示意图、概念图
- **创建插图**：为论文、演示文稿、海报生成插图
- **图像编辑**：修改现有图像、添加元素、更改风格
- **图像修复**：修复损坏的图像、移除不需要的元素
- **概念设计**：可视化实验设计、产品概念、用户界面

## 核心功能

### 1. DALL-E 3（OpenAI）

#### 文本到图像

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.images.generate(
    model="dall-e-3",
    prompt="一个详细的蛋白质结构图，显示α螺旋和β折叠，使用科学准确的配色方案",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
```

#### 图像编辑

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="在图像中添加一个DNA双螺旋结构",
    n=1,
    size="1024x1024"
)

image_url = response.data[0].url
```

#### 图像变体

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.images.create_variation(
    model="dall-e-2",
    image=open("original.png", "rb"),
    n=1,
    size="1024x1024"
)

image_url = response.data[0].url
```

### 2. Stable Diffusion

#### 文本到图像

```python
from diffusers import StableDiffusionPipeline
import torch

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 生成图像
prompt = "一个详细的蛋白质结构图，显示α螺旋和β折叠，使用科学准确的配色方案"
negative_prompt = "模糊、低质量、变形"

image = pipe(
    prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=50,
    guidance_scale=7.5
).images[0]

# 保存图像
image.save("protein_structure.png")
```

#### 图像到图像

```python
from diffusers import StableDiffusionImg2ImgPipeline
import torch
from PIL import Image

# 加载模型
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 加载输入图像
init_image = Image.open("input.png").convert("RGB")

# 生成图像
prompt = "将此图像转换为科学插图风格"
negative_prompt = "模糊、低质量、变形"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=init_image,
    strength=0.75,
    guidance_scale=7.5,
    num_inference_steps=50
).images[0]

# 保存图像
image.save("output.png")
```

#### 图像修复

```python
from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image

# 加载模型
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 加载图像和掩码
init_image = Image.open("original.png").convert("RGB")
mask_image = Image.open("mask.png").convert("RGB")

# 修复图像
prompt = "在掩码区域添加一个DNA双螺旋结构"
negative_prompt = "模糊、低质量、变形"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=init_image,
    mask_image=mask_image,
    guidance_scale=7.5,
    num_inference_steps=50
).images[0]

# 保存图像
image.save("inpainting.png")
```

### 3. 高级功能

#### 批量生成

```python
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

prompts = [
    "蛋白质结构图1",
    "蛋白质结构图2",
    "蛋白质结构图3"
]

for i, prompt in enumerate(prompts):
    image = pipe(prompt, num_inference_steps=50).images[0]
    image.save(f"protein_structure_{i}.png")
```

#### 风格迁移

```python
from diffusers import StableDiffusionControlNetPipeline
import torch
from PIL import Image

# 加载模型
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet="lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 加载边缘图
control_image = Image.open("edges.png")

# 生成图像
prompt = "科学插图风格"
image = pipe(
    prompt=prompt,
    control_image=control_image,
    num_inference_steps=50,
    controlnet_conditioning_scale=1.0
).images[0]

image.save("style_transfer.png")
```

#### 超分辨率

```python
from diffusers import StableDiffusionUpscalePipeline
import torch
from PIL import Image

# 加载模型
pipe = StableDiffusionUpscalePipeline.from_pretrained(
    "stabilityai/sd-x2-latent-upscaler",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 加载低分辨率图像
low_res_img = Image.open("low_res.png")

# 超分辨率
prompt = "高质量科学插图"
upscaled_image = pipe(
    prompt=prompt,
    image=low_res_img,
    num_inference_steps=50,
    guidance_scale=7.5
).images[0]

# 保存图像
upscaled_image.save("high_res.png")
```

## 常见工作流

### 工作流1：生成科学插图

```python
from diffusers import StableDiffusionPipeline
import torch

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 生成多个变体
prompts = [
    "一个详细的蛋白质结构图，显示α螺旋和β折叠，使用科学准确的配色方案，专业科学插图风格",
    "细胞膜结构图，显示磷脂双分子层、膜蛋白和胆固醇分子，3D渲染风格",
    "DNA复制过程图，显示解旋酶、DNA聚合酶和引物酶，教育插图风格"
]

for i, prompt in enumerate(prompts):
    image = pipe(
        prompt,
        num_inference_steps=50,
        guidance_scale=7.5
    ).images[0]
    image.save(f"scientific_illustration_{i}.png")
```

### 工作流2：图像编辑和优化

```python
from diffusers import StableDiffusionImg2ImgPipeline
import torch
from PIL import Image

# 加载模型
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 加载原始图像
original_image = Image.open("original.png").convert("RGB")

# 编辑图像
prompts = [
    "将图像转换为科学插图风格",
    "提高图像质量，使其更清晰和专业",
    "添加科学标注和标签"
]

for i, prompt in enumerate(prompts):
    edited_image = pipe(
        prompt=prompt,
        image=original_image,
        strength=0.75,
        num_inference_steps=50,
        guidance_scale=7.5
    ).images[0]
    edited_image.save(f"edited_image_{i}.png")
```

### 工作流3：创建流程图

```python
from diffusers import StableDiffusionPipeline
import torch

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 生成流程图
prompts = [
    "PCR反应流程图，显示变性、退火和延伸步骤，专业科学插图风格",
    "蛋白质合成流程图，显示转录和翻译过程，教育插图风格",
    "细胞信号转导通路图，显示受体激活和下游信号，专业科学插图风格"
]

for i, prompt in enumerate(prompts):
    image = pipe(
        prompt,
        num_inference_steps=50,
        guidance_scale=7.5
    ).images[0]
    image.save(f"flowchart_{i}.png")
```

## 最佳实践

1. **提示工程**：使用详细、具体的描述以获得更好的结果
2. **负面提示**：使用负面提示避免不需要的元素
3. **迭代优化**：生成多个变体并选择最好的
4. **后处理**：使用图像编辑工具进一步优化生成的图像
5. **风格一致性**：在系列图像中使用一致的提示以保持风格
6. **分辨率**：使用高分辨率模型或超分辨率以获得更好的质量
7. **GPU加速**：使用GPU加速以提高生成速度

## 与其他工具集成

### 与matplotlib集成

```python
import matplotlib.pyplot as plt
from diffusers import StableDiffusionPipeline
import torch

# 生成图像
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

image = pipe("科学插图", num_inference_steps=50).images[0]

# 使用matplotlib显示
plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis('off')
plt.show()
```

### 与Pillow集成

```python
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch

# 生成图像
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

image = pipe("科学插图", num_inference_steps=50).images[0]

# 添加标注
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 24)
draw.text((50, 50), "蛋白质结构", fill="white", font=font)

# 保存图像
image.save("annotated_image.png")
```

### 与OpenCV集成

```python
import cv2
import numpy as np
from diffusers import StableDiffusionPipeline
import torch

# 生成图像
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

image = pipe("科学插图", num_inference_steps=50).images[0]

# 转换为OpenCV格式
cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# 应用图像处理
processed_image = cv2.GaussianBlur(cv_image, (5, 5), 0)

# 保存图像
cv2.imwrite("processed_image.png", processed_image)
```

## 故障排除

**问题：生成图像质量差**
- 解决方案：增加num_inference_steps，调整guidance_scale，或使用更好的提示

**问题：生成速度慢**
- 解决方案：使用GPU加速，减少num_inference_steps，或使用更小的模型

**问题：不符合预期**
- 解决方案：改进提示，添加负面提示，或生成多个变体

**问题：内存不足**
- 解决方案：使用更小的模型，减少batch size，或使用CPU

**问题：风格不一致**
- 解决方案：在提示中指定风格，使用ControlNet，或使用风格迁移

## 其他资源

- **DALL-E文档**: https://platform.openai.com/docs/guides/images
- **Stable Diffusion文档**: https://huggingface.co/docs/diffusers
- **Diffusers库**: https://github.com/huggingface/diffusers
- **提示工程指南**: https://prompthero.com/stable-diffusion-prompts
