---
name: ai-studio-image
description: 通过 Google AI Studio(Gemini)生成拟真人像图片。以自然光照和细微瑕疵呈现网红风格或教育风格的写实照片。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- image-generation
- ai-studio
- google
- photography
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# AI Studio Image — 拟真人像图片专家

## 概述

通过 Google AI Studio(Gemini)生成拟真人像图片。以自然光照和细微瑕疵呈现网红风格或教育风格的写实照片。

## 何时使用此技能

- 当用户提到"gera imagem"或相关主题时
- 当用户提到"gerar foto"或相关主题时
- 当用户提到"criar imagem"或相关主题时
- 当用户提到"foto realista"或相关主题时
- 当用户提到"imagem humanizada"或相关主题时
- 当用户提到"foto influencer"或相关主题时

## 何时不使用此技能

- 任务与 AI studio image 无关
- 更简单、更专用的工具就能处理该请求
- 用户需要的是不涉及特定领域专业知识的通用协助

## 工作原理

AI 生成的图像与真实照片之间的差异,体现在难以察觉的细节上:
手机传感器轻微的颗粒感、不够完美的光照、略微偏离中心的取景、
小型镜头特有的景深。本技能会系统性地将这些特质注入每一次生成。

## Ai Studio Image — 拟真人像图片专家

通过 Google AI Studio 生成图像的技能,能将任意提示词转化为具有真实
人类外观的照片。每一张生成的图片看起来都像是由真人用手机拍摄的——
而不是由 AI 生成的。

## 1. 配置 API Key

用户需要一个 Google AI Studio 的 API key:
- 访问 https://aistudio.google.com/apikey
- 创建或复制你的 API key
- 配置为环境变量:

```bash

## Windows

set GEMINI_API_KEY=sua-api-key-aqui

## Linux/Mac

export GEMINI_API_KEY=sua-api-key-aqui
```

或者在 `C:\Users\renat\skills\ai-studio-image\` 下创建一个 `.env` 文件:
```
GEMINI_API_KEY=sua-api-key-aqui
```

## 2. 安装依赖

```bash
pip install -r C:\Users\renat\skills\ai-studio-image\scripts\requirements.txt
```

## 3. 生成你的第一张图片

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py --prompt "mulher jovem tomando cafe em cafeteria" --mode influencer --format square
```

## 主要工作流程

当用户要求生成图片时,请遵循以下流程:

## 第一步:确定模式

询问或根据上下文推断:

| 模式 | 何时使用 | 特征 |
|------|-------------|-----------------|
| **influencer(网红)** | 社交媒体帖子、生活方式、个人品牌打造 | 美观但自然的美学风格,色彩鲜活但不过度饱和,构图具有吸引力 |
| **educacional(教育)** | 课程素材、教程、演示文稿、信息图 | 视觉干净、专业,聚焦内容,元素清晰易读 |

如果用户没有指定,社交媒体内容默认使用 **influencer**,与教学/演示相关的
一切则使用 **educacional**。

## 第二步:确定格式

| 格式 | 宽高比 | 理想用途 |
|---------|-------------|-----------|
| `square` | 1:1 | Instagram 信息流、Facebook、个人主页 |
| `portrait` | 3:4 | Instagram 竖图、Pinterest |
| `landscape` | 16:9 | YouTube 缩略图、横幅广告、桌面端 |
| `stories` | 9:16 | Instagram/Facebook Stories、TikTok、Reels |

如果未指定,根据上下文推断(stories → 9:16,feed → 1:1,等等)。

## 第三步:转换提示词

**这是最重要的一步。** 永远不要把用户的提示词直接发送给 API。
始终先经过拟真化引擎处理:

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\prompt_engine.py --prompt "prompt do usuario" --mode influencer
```

拟真化引擎会添加多层写实元素:

**第 1 层 — 设备与技术:**
- 使用智能手机拍摄(iPhone/Samsung Galaxy)
- 手机镜头,自然景深
- 不使用闪光灯——仅使用环境光
- 轻微的传感器噪点(弱光下的高 ISO)

**第 2 层 — 自然光照:**
- 间接日光 / 黄金时段 / 窗边光
- 柔和、有机的阴影
- 不使用影室布光
- 表面上的自然反光

**第 3 层 — 人类特有的瑕疵:**
- 略微不完美的取景(不是数学意义上的居中)
- 自然的选择性对焦(背景中有轻微失焦的元素)
- 手部的微小抖动(清晰度并非绝对)
- 真实环境中的随机元素

**第 4 层 — 真实感:**
- 真实的面部表情(不是影室摆拍)
- 日常的服装与场景
- 真实的皮肤质感(毛孔、细微痕迹——不是瓷娃娃般的皮肤)
- 符合现实比例的体型

**第 5 层 — 环境背景:**
- 真实场景(不是千篇一律的图库背景)
- 环境中的日常物品
- 与场景相符的光照
- 与活动相符的时间段

## 第四步:生成图片

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "prompt humanizado gerado no passo anterior" \
  --mode influencer \
  --format square \
  --model gemini-2-flash-exp \
  --output C:\Users\renat\skills\ai-studio-image\data\outputs\
```

**可用模型(按推荐顺序排列):**

| 模型 | 速度 | 质量 | 成本 | 理想用途 |
|--------|-----------|-----------|-------|-----------|
| `gemini-2-flash-exp` | 快 | 高 | **免费** | **默认——始终使用** |
| `imagen-4` | 中 | 高 | $0.03/张 | 高质量(需要 --force-paid) |
| `imagen-4-ultra` | 慢 | 最高 | $0.06/张 | 印刷用途,2K(需要 --force-paid) |
| `imagen-4-fast` | 快 | 良好 | $0.02/张 | 大批量(需要 --force-paid) |
| `gemini-flash-image` | 快 | 高 | $0.039/张 | 图像编辑(需要 --force-paid) |
| `gemini-pro-image` | 中 | 最高+4K | $0.134/张 | 参考用图,4K(需要 --force-paid) |

## 第五步:展示并迭代

将结果展示给用户。如果需要调整:
- Reluz(重新布光):调整光照
- Reenquadrar(重新取景):改变构图
- Mais/menos natural(更自然/更少自然):调整瑕疵程度
- Mudar cenario(更换场景):改变环境

## 预配置模板

对于常见场景,使用现成的模板。执行:

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\templates.py --list
```

可用模板:

## Influencer(网红)模式

| 模板 | 描述 |
|----------|-----------|
| `cafe-lifestyle` | 在咖啡馆/餐厅中的人物,配有饮品/食物 |
| `outdoor-adventure` | 户外活动、自然、旅行 |
| `workspace-minimal` | 简约优雅的办公桌、居家办公室 |
| `fitness-natural` | 带自然视觉风格的运动/健康场景 |
| `food-flat-lay` | 俯视角度的食物,休闲的平铺拍摄 |
| `urban-street` | 城市场景、街头风格 |
| `golden-hour-portrait` | 带日落金色光线的肖像 |
| `mirror-selfie` | 镜子自拍,随意而自发 |
| `product-in-use` | 人物自然地使用产品 |
| `behind-scenes` | 幕后花絮、制作过程、真实日常 |

## Educacional(教育)模式

| 模板 | 描述 |
|----------|-----------|
| `tutorial-step` | 人物演示教程步骤 |
| `whiteboard-explain` | 人物在白板/黑板上讲解 |
| `hands-on-demo` | 双手进行实操演示 |
| `before-after` | 前后对比 |
| `tool-showcase` | 正在使用的工具/软件 |
| `classroom-natural` | 课堂/工作坊环境 |
| `infographic-human` | 人物指向数据/图表 |
| `interview-setup` | 自然的采访/播客场景 |
| `screen-recording-human` | 人物用笔记本电脑展示屏幕 |
| `team-collaboration` | 团队自然协作 |

使用模板:
```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --template cafe-lifestyle \
  --custom "mulher ruiva, 30 anos, lendo livro" \
  --format square
```

## 拟真化程度

控制注入多少"瑕疵":

| 级别 | 效果 |
|-------|--------|
| `ultra` | 最大写实度——看起来 100% 像手机照片 |
| `natural`(默认) | 质量与写实度之间的完美平衡 |
| `polished` | 更干净,依然自然但更注重美学 |
| `editorial` | 杂志风格,自然但带有制作感 |

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "..." --humanization natural
```

## 时间段

光照会发生显著变化:

| 选项 | 描述 |
|-------|-----------|
| `morning` | 柔和的晨光,冷暖交织的色调 |
| `golden-hour` | 日落/日出,金色色调 |
| `midday` | 正午的硬光,鲜明的阴影 |
| `overcast` | 多云天,均匀的漫射光 |
| `night` | 人工照明,暖色调 |
| `indoor` | 室内光,混合光源 |

## 批量生成

生成多个变体:

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "..." --variations 4 --format square
```

## Instagram 技能

生成图片并直接发布:
1. 使用 `ai-studio-image` 生成照片
2. 使用 `instagram` 技能配上优化好的文案发布

## Canva 集成

生成的图片可以发送到 Canva,以添加文字/品牌元素。

## 故障排查

| 问题 | 解决方法 |
|----------|----------|
| `GEMINI_API_KEY not found` | 配置环境变量或创建 `.env` 文件 |
| `quota exceeded` | 等待速率限制重置或升级套餐 |
| `image blocked` | 调整提示词——可能包含受限内容 |
| `low quality output` | 将 humanization 提升到 `ultra`,或尝试其他模型 |

## 参考资料

详细指南请参阅:
- `references/setup-guide.md` — 完整的安装与配置指南
- `references/prompt-engineering.md` — 拟真图像的高级提示词技巧
- `references/api-reference.md` — Google AI Studio API 文档

## 最佳实践

- 提供关于你的项目和需求的清晰、具体的上下文
- 在应用到生产代码之前,审查所有建议
- 与其他互补技能结合使用以获得更全面的分析

## 常见陷阱

- 将此技能用于超出其领域专长的任务
- 在不理解你具体上下文的情况下直接应用建议
- 没有提供足够的项目上下文以获得准确的分析

## 相关技能

- `comfyui-gateway` - 增强分析的互补技能
- `image-studio` - 增强分析的互补技能
- `stability-ai` - 增强分析的互补技能

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为针对特定环境验证、测试或专家评审的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,请停下来寻求澄清。
