---
name: transformers-js
description: 使用Transformers.js直接在JavaScript/TypeScript中运行最先进的机器学习模型。支持NLP（文本分类、翻译、摘要）、计算机视觉（图像分类、目标检测）、音频（语音识别、音频分类）和多模态任务。在Node.js和浏览器（使用WebGPU/WASM）中工作，使用来自Hugging Face Hub的预训练模型。
license: Apache-2.0
metadata:
  author: huggingface
  version: "3.8.1"
  category: machine-learning
  repository: https://github.com/huggingface/transformers.js
compatibility: 需要Node.js 18+或支持ES模块的现代浏览器。WebGPU支持需要兼容的浏览器/环境。从Hugging Face Hub下载模型需要互联网访问（如果使用本地模型则可选）。
---

# Transformers.js - JavaScript的机器学习

Transformers.js使您能够直接在JavaScript中运行最先进的机器学习模型，无论是在浏览器还是Node.js环境中，无需服务器。

## 何时使用此技能

当您需要：
- 在JavaScript中运行用于文本分析、生成或翻译的ML模型
- 执行图像分类、目标检测或分割
- 实现语音识别或音频处理
- 构建多模态AI应用程序（文本到图像、图像到文本等）
- 在浏览器中在客户端运行模型，无需后端

## 安装

### NPM安装
```bash
npm install @huggingface/transformers
```

### 浏览器使用（CDN）
```javascript
<script type="module">
  import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers';
</script>
```

## 核心概念

### 1. Pipeline API
Pipeline API是使用模型的最简单方法。它将预处理、模型推理和后处理组合在一起：

```javascript
import { pipeline } from '@huggingface/transformers';

// 创建特定任务的pipeline
const pipe = await pipeline('sentiment-analysis');

// 使用pipeline
const result = await pipe('I love transformers!');
// 输出: [{ label: 'POSITIVE', score: 0.999817686 }]

// 重要：使用完毕后必须释放内存
await classifier.dispose();
```

**⚠️ 内存管理：** 所有pipeline必须在完成后使用`pipe.dispose()`释放，以防止内存泄漏。请参阅[代码示例](./references/EXAMPLES.md)中不同环境的清理模式。

### 2. 模型选择
您可以将自定义模型指定为第二个参数：

```javascript
const pipe = await pipeline(
  'sentiment-analysis',
  'Xenova/bert-base-multilingual-uncased-sentiment'
);
```

**查找模型：**

浏览Hugging Face Hub上可用的Transformers.js模型：
- **所有模型**：https://huggingface.co/models?library=transformers.js&sort=trending
- **按任务**：添加`pipeline_tag`参数
  - 文本生成：https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending
  - 图像分类：https://huggingface.co/models?pipeline_tag=image-classification&library=transformers.js&sort=trending
  - 语音识别：https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&library=transformers.js&sort=trending

**提示：** 按任务类型过滤，按趋势/下载量排序，并查看模型卡片以获取性能指标和使用示例。

### 3. 设备选择
选择在哪里运行模型：

```javascript
// 在CPU上运行（WASM的默认设置）
const pipe = await pipeline('sentiment-analysis', 'model-id');

// 在GPU上运行（WebGPU - 实验性）
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  device: 'webgpu',
});
```

### 4. 量化选项
控制模型精度与性能：

```javascript
// 使用量化模型（更快，更小）
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q4',  // 选项: 'fp32', 'fp16', 'q8', 'q4'
});
```

## 支持的任务

**注意：** 以下所有示例显示基本用法。

### 自然语言处理

#### 文本分类
```javascript
const classifier = await pipeline('text-classification');
const result = await classifier('This movie was amazing!');
```

#### 命名实体识别（NER）
```javascript
const ner = await pipeline('token-classification');
const entities = await ner('My name is John and I live in New York.');
```

#### 问答
```javascript
const qa = await pipeline('question-answering');
const answer = await qa({
  question: 'What is the capital of France?',
  context: 'Paris is the capital and largest city of France.'
});
```

#### 文本生成
```javascript
const generator = await pipeline('text-generation', 'onnx-community/gemma-3-270m-it-ONNX');
const text = await generator('Once upon a time', {
  max_new_tokens: 100,
  temperature: 0.7
});
```

**关于流式传输和聊天：** 请参阅**[文本生成指南](./references/TEXT_GENERATION.md)**了解：
- 使用`TextStreamer`进行逐令牌输出流式传输
- 带有系统/用户/助手角色的聊天/对话格式
- 生成参数（temperature、top_k、top_p）
- 浏览器和Node.js示例
- React组件和API端点

#### 翻译
```javascript
const translator = await pipeline('translation', 'Xenova/nllb-200-distilled-600M');
const output = await translator('Hello, how are you?', {
  src_lang: 'eng_Latn',
  tgt_lang: 'fra_Latn'
});
```

#### 摘要
```javascript
const summarizer = await pipeline('summarization');
const summary = await summarizer(longText, {
  max_length: 100,
  min_length: 30
});
```

#### 零样本分类
```javascript
const classifier = await pipeline('zero-shot-classification');
const result = await classifier('This is a story about sports.', ['politics', 'sports', 'technology']);
```

### 计算机视觉

#### 图像分类
```javascript
const classifier = await pipeline('image-classification');
const result = await classifier('https://example.com/image.jpg');
// 或使用本地文件
const result = await classifier(imageUrl);
```

#### 目标检测
```javascript
const detector = await pipeline('object-detection');
const objects = await detector('https://example.com/image.jpg');
// 返回: [{ label: 'person', score: 0.95, box: { xmin, ymin, xmax, ymax } }, ...]
```

#### 图像分割
```javascript
const segmenter = await pipeline('image-segmentation');
const segments = await segmenter('https://example.com/image.jpg');
```

#### 深度估计
```javascript
const depthEstimator = await pipeline('depth-estimation');
const depth = await depthEstimator('https://example.com/image.jpg');
```

#### 零样本图像分类
```javascript
const classifier = await pipeline('zero-shot-image-classification');
const result = await classifier('image.jpg', ['cat', 'dog', 'bird']);
```

### 音频处理

#### 自动语音识别
```javascript
const transcriber = await pipeline('automatic-speech-recognition');
const result = await transcriber('audio.wav');
// 返回: { text: 'transcribed text here' }
```

#### 音频分类
```javascript
const classifier = await pipeline('audio-classification');
const result = await classifier('audio.wav');
```

#### 文本到语音
```javascript
const synthesizer = await pipeline('text-to-speech', 'Xenova/speecht5_tts');
const audio = await synthesizer('Hello, this is a test.', {
  speaker_embeddings: speakerEmbeddings
});
```

### 多模态

#### 图像到文本（图像描述）
```javascript
const captioner = await pipeline('image-to-text');
const caption = await captioner('image.jpg');
```

#### 文档问答
```javascript
const docQA = await pipeline('document-question-answering');
const answer = await docQA('document-image.jpg', 'What is the total amount?');
```

#### 零样本目标检测
```javascript
const detector = await pipeline('zero-shot-object-detection');
const objects = await detector('image.jpg', ['person', 'car', 'tree']);
```

### 特征提取（嵌入）

```javascript
const extractor = await pipeline('feature-extraction');
const embeddings = await extractor('This is a sentence to embed.');
// 返回: 形状为 [1, sequence_length, hidden_size] 的张量

// 对于句子嵌入（均值池化）
const extractor = await pipeline('feature-extraction', 'onnx-community/all-MiniLM-L6-v2-ONNX');
const embeddings = await extractor('Text to embed', { pooling: 'mean', normalize: true });
```

## 查找和选择模型

### 浏览Hugging Face Hub

在Hugging Face Hub上发现兼容的Transformers.js模型：

**基本URL（所有模型）：**
```
https://huggingface.co/models?library=transformers.js&sort=trending
```

**按任务过滤**使用`pipeline_tag`参数：

| 任务 | URL |
|------|-----|
| **文本生成** | https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending |
| **文本分类** | https://huggingface.co/models?pipeline_tag=text-classification&library=transformers.js&sort=trending |
| **翻译** | https://huggingface.co/models?pipeline_tag=translation&library=transformers.js&sort=trending |
| **摘要** | https://huggingface.co/models?pipeline_tag=summarization&library=transformers.js&sort=trending |
| **问答** | https://huggingface.co/models?pipeline_tag=question-answering&library=transformers.js&sort=trending |
| **图像分类** | https://huggingface.co/models?pipeline_tag=image-classification&library=transformers.js&sort=trending |
| **目标检测** | https://huggingface.co/models?pipeline_tag=object-detection&library=transformers.js&sort=trending |
| **图像分割** | https://huggingface.co/models?pipeline_tag=image-segmentation&library=transformers.js&sort=trending |
| **语音识别** | https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&library=transformers.js&sort=trending |
| **音频分类** | https://huggingface.co/models?pipeline_tag=audio-classification&library=transformers.js&sort=trending |
| **图像到文本** | https://huggingface.co/models?pipeline_tag=image-to-text&library=transformers.js&sort=trending |
| **特征提取** | https://huggingface.co/models?pipeline_tag=feature-extraction&library=transformers.js&sort=trending |
| **零样本分类** | https://huggingface.co/models?pipeline_tag=zero-shot-classification&library=transformers.js&sort=trending |

**排序选项：**
- `&sort=trending` - 最近最流行
- `&sort=downloads` - 总体下载最多
- `&sort=likes` - 社区最喜爱
- `&sort=modified` - 最近更新

### 选择正确的模型

选择模型时考虑这些因素：

**1. 模型大小**
- **小型（< 100MB）**：快速，适合浏览器，精度有限
- **中型（100MB - 500MB）**：平衡性能，适合大多数用例
- **大型（> 500MB）**：高精度，较慢，更适合Node.js或强大设备

**2. 量化**
模型通常有不同的量化级别：
- `fp32` - 全精度（最大，最准确）
- `fp16` - 半精度（更小，仍准确）
- `q8` - 8位量化（小得多，轻微精度损失）
- `q4` - 4位量化（最小，明显精度损失）

**3. 任务兼容性**
检查模型卡片：
- 支持的任务（某些模型支持多个任务）
- 输入/输出格式
- 语言支持（多语言vs仅英语）
- 许可证限制

**4. 性能指标**
模型卡片通常显示：
- 准确率分数
- 基准测试结果
- 推理速度
- 内存需求

### 示例：查找文本生成模型

```javascript
// 1. 访问: https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending

// 2. 浏览并选择模型（例如，onnx-community/gemma-3-270m-it-ONNX）

// 3. 检查模型卡片：
//    - 模型大小: ~270M参数
//    - 量化: 提供q4
//    - 语言: 英语
//    - 用例: 指令跟随聊天

// 4. 使用模型：
import { pipeline } from '@huggingface/transformers';

const generator = await pipeline(
  'text-generation',
  'onnx-community/gemma-3-270m-it-ONNX',
  { dtype: 'q4' } // 使用量化版本以获得更快的推理
);

const output = await generator('Explain quantum computing in simple terms.', {
  max_new_tokens: 100
});

await generator.dispose();
```

### 模型选择提示

1. **从小开始**：首先测试较小的模型，然后根据需要升级
2. **检查ONNX支持**：确保模型有ONNX文件（在模型库中查找`onnx`文件夹）
3. **阅读模型卡片**：模型卡片包含使用示例、限制和基准测试
4. **本地测试**：在您的环境中基准测试推理速度和内存使用
5. **社区模型**：寻找`Xenova`（Transformers.js维护者）或`onnx-community`的模型
6. **版本固定**：在生产中使用特定的git提交以获得稳定性：
   ```javascript
   const pipe = await pipeline('task', 'model-id', { revision: 'abc123' });
   ```

## 高级配置

### 环境配置 (`env`)

`env`对象提供对Transformers.js执行、缓存和模型加载的全面控制。

**快速概述：**

```javascript
import { env } from '@huggingface/transformers';

// 查看版本
console.log(env.version); // 例如，'3.8.1'

// 常见设置
env.allowRemoteModels = true;  // 从Hugging Face Hub加载
env.allowLocalModels = false;  // 从文件系统加载
env.localModelPath = '/models/'; // 本地模型目录
env.useFSCache = true;         // 在磁盘上缓存模型（Node.js）
env.useBrowserCache = true;    // 在浏览器中缓存模型
env.cacheDir = './.cache';     // 缓存目录位置
```

**配置模式：**

```javascript
// 开发：使用远程模型快速迭代
env.allowRemoteModels = true;
env.useFSCache = true;

// 生产：仅本地模型
env.allowRemoteModels = false;
env.allowLocalModels = true;
env.localModelPath = '/app/models/';

// 自定义CDN
env.remoteHost = 'https://cdn.example.com/models';

// 禁用缓存（测试）
env.useFSCache = false;
env.useBrowserCache = false;
```

有关所有配置选项、缓存策略、缓存管理、预下载模型等的完整文档，请参阅：

**→ [配置参考](./references/CONFIGURATION.md)**

### 使用张量

```javascript
import { AutoTokenizer, AutoModel } from '@huggingface/transformers';

// 分别加载分词器和模型以获得更多控制
const tokenizer = await AutoTokenizer.from_pretrained('bert-base-uncased');
const model = await AutoModel.from_pretrained('bert-base-uncased');

// 标记化输入
const inputs = await tokenizer('Hello world!');

// 运行模型
const outputs = await model(inputs);
```

### 批处理

```javascript
const classifier = await pipeline('sentiment-analysis');

// 处理多个文本
const results = await classifier([
  'I love this!',
  'This is terrible.',
  'It was okay.'
]);
```

## 浏览器特定注意事项

### WebGPU使用
WebGPU在浏览器中提供GPU加速：

```javascript
const pipe = await pipeline('text-generation', 'onnx-community/gemma-3-270m-it-ONNX', {
  device: 'webgpu',
  dtype: 'fp32'
});
```

**注意**：WebGPU是实验性的。检查浏览器兼容性并在出现问题时报告。

### WASM性能
默认浏览器执行使用WASM：

```javascript
// 为浏览器优化，使用量化
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q8'  // 或'q4'以获得更小的尺寸
});
```

### 进度跟踪和加载指示器

模型可能很大（从几MB到几GB不等），由多个文件组成。通过向`pipeline()`函数传递回调来跟踪下载进度：

```javascript
import { pipeline } from '@huggingface/transformers';

// 跟踪每个文件的进度
const fileProgress = {};

function onProgress(info) {
  console.log(`${info.status}: ${info.file}`);
  
  if (info.status === 'progress') {
    fileProgress[info.file] = info.progress;
    console.log(`${info.file}: ${info.progress.toFixed(1)}%`);
  }
  
  if (info.status === 'done') {
    console.log(`✓ ${info.file} complete`);
  }
}

// 将回调传递给pipeline
const classifier = await pipeline('sentiment-analysis', null, {
  progress_callback: onProgress
});
```

**进度信息属性：**

```typescript
interface ProgressInfo {
  status: 'initiate' | 'download' | 'progress' | 'done' | 'ready';
  name: string;      // 模型ID或路径
  file: string;      // 正在处理的文件
  progress?: number; // 百分比（0-100，仅适用于'progress'状态）
  loaded?: number;   // 已下载字节数（仅适用于'progress'状态）
  total?: number;    // 总字节数（仅适用于'progress'状态）
}
```

有关完整示例，包括浏览器UI、React组件、CLI进度条和重试逻辑，请参阅：

**→ [Pipeline选项 - 进度回调](./references/PIPELINE_OPTIONS.md#progress-callback)**

## 错误处理

```javascript
try {
  const pipe = await pipeline('sentiment-analysis', 'model-id');
  const result = await pipe('text to analyze');
} catch (error) {
  if (error.message.includes('fetch')) {
    console.error('模型下载失败。检查互联网连接。');
  } else if (error.message.includes('ONNX')) {
    console.error('模型执行失败。检查模型兼容性。');
  } else {
    console.error('未知错误:', error);
  }
}
```

## 性能提示

1. **重用Pipeline**：创建一次pipeline，多次重用进行推理
2. **使用量化**：从`q8`或`q4`开始以获得更快的推理
3. **批处理**：尽可能一起处理多个输入
4. **缓存模型**：模型会自动缓存（有关浏览器Cache API、Node.js文件系统缓存和自定义实现的详细信息，请参阅**[缓存参考](./references/CACHE.md)**）
5. **大型模型使用WebGPU**：对受益于GPU加速的模型使用WebGPU
6. **修剪上下文**：对于文本生成，限制`max_new_tokens`以避免内存问题
7. **清理资源**：完成后调用`pipe.dispose()`以释放内存

## 内存管理

**重要：** 完成后始终调用`pipe.dispose()`以防止内存泄漏。

```javascript
const pipe = await pipeline('sentiment-analysis');
const result = await pipe('Great product!');
await pipe.dispose();  // ✓ 释放内存（每个模型100MB - 几GB）
```

**何时释放：**
- 应用程序关闭或组件卸载时
- 加载不同模型之前
- 长时间运行的应用程序中批处理后

模型消耗大量内存并占用GPU/CPU资源。释放对于浏览器内存限制和服务器稳定性至关重要。

有关详细模式（React清理、服务器、浏览器），请参阅**[代码示例](./references/EXAMPLES.md)**

## 故障排除

### 模型未找到
- 验证模型在Hugging Face Hub上存在
- 检查模型名称拼写
- 确保模型有ONNX文件（在模型库中查找`onnx`文件夹）

### 内存问题
- 使用较小的模型或量化版本（`dtype: 'q4'`）
- 减少批处理大小
- 使用`max_length`限制序列长度

### WebGPU错误
- 检查浏览器兼容性（Chrome 113+，Edge 113+）
- 如果`fp32`失败，尝试`dtype: 'fp16'`
- 如果WebGPU不可用，回退到WASM

## 参考文档

### 此技能
- **[Pipeline选项](./references/PIPELINE_OPTIONS.md)** - 使用`progress_callback`、`device`、`dtype`等配置`pipeline()`
- **[配置参考](./references/CONFIGURATION.md)** - 用于缓存和模型加载的全局`env`配置
- **[缓存参考](./references/CACHE.md)** - 浏览器Cache API、Node.js文件系统缓存和自定义缓存实现
- **[文本生成指南](./references/TEXT_GENERATION.md)** - 流式传输、聊天格式和生成参数
- **[模型架构](./references/MODEL_ARCHITECTURES.md)** - 支持的模型和选择提示
- **[代码示例](./references/EXAMPLES.md)** - 不同运行时的实际实现

### 官方Transformers.js
- 官方文档：https://huggingface.co/docs/transformers.js
- API参考：https://huggingface.co/docs/transformers.js/api/pipelines
- 模型中心：https://huggingface.co/models?library=transformers.js
- GitHub：https://github.com/huggingface/transformers.js
- 示例：https://github.com/huggingface/transformers.js/tree/main/examples

## 最佳实践

1. **始终释放Pipeline**：完成后调用`pipe.dispose()` - 对于防止内存泄漏至关重要
2. **从Pipeline开始**：使用pipeline API，除非您需要细粒度控制
3. **先本地测试**：部署前使用小输入测试模型
4. **监控模型大小**：注意Web应用程序的模型下载大小
5. **处理加载状态**：显示进度指示器以获得更好的用户体验
6. **版本固定**：为生产稳定性固定特定模型版本
7. **错误边界**：始终将pipeline调用包装在try-catch块中
8. **渐进增强**：为不支持的浏览器提供回退
9. **重用模型**：加载一次，多次使用 - 不要不必要地重新创建pipeline
10. **优雅关闭**：在服务器中处理SIGTERM/SIGINT时释放模型

## 快速参考：任务ID

| 任务 | 任务ID |
|------|---------|
| 文本分类 | `text-classification` 或 `sentiment-analysis` |
| 标记分类 | `token-classification` 或 `ner` |
| 问答 | `question-answering` |
| 填充掩码 | `fill-mask` |
| 摘要 | `summarization` |
| 翻译 | `translation` |
| 文本生成 | `text-generation` |
| 文本到文本生成 | `text2text-generation` |
| 零样本分类 | `zero-shot-classification` |
| 图像分类 | `image-classification` |
| 图像分割 | `image-segmentation` |
| 目标检测 | `object-detection` |
| 深度估计 | `depth-estimation` |
| 图像到图像 | `image-to-image` |
| 零样本图像分类 | `zero-shot-image-classification` |
| 零样本目标检测 | `zero-shot-object-detection` |
| 自动语音识别 | `automatic-speech-recognition` |
| 音频分类 | `audio-classification` |
| 文本到语音 | `text-to-speech` 或 `text-to-audio` |
| 图像到文本 | `image-to-text` |
| 文档问答 | `document-question-answering` |
| 特征提取 | `feature-extraction` |
| 句子相似度 | `sentence-similarity` |

---

此技能使您能够将最先进的机器学习功能直接集成到JavaScript应用程序中，无需单独的ML服务器或Python环境。