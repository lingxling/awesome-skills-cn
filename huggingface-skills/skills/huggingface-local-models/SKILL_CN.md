---
name: huggingface-local-models
description: "用于选择使用 llama.cpp 和 GGUF 在 CPU、Mac Metal、CUDA 或 ROCm 上本地运行的模型。涵盖查找 GGUFs、量化选择、运行服务器、精确 GGUF 文件查找、转换和 OpenAI 兼容的本地服务。"
---

# Hugging Face 本地模型

在 Hugging Face Hub 上搜索 llama.cpp 兼容的 GGUF 仓库，选择正确的量化版本，使用 `llama-cli` 或 `llama-server` 启动模型。

## 默认工作流

1. 使用 `apps=llama.cpp` 搜索 Hub。
2. 打开 `https://huggingface.co/<repo>?local-app=llama.cpp`。
3. 优先使用可见的精确 HF local-app 代码片段和量化推荐。
4. 使用 `https://huggingface.co/api/models/<repo>/tree/main?recursive=true` 确认精确的 `.gguf` 文件名。
5. 使用 `llama-cli -hf <repo>:<QUANT>` 或 `llama-server -hf <repo>:<QUANT>` 启动。
6. 当仓库使用自定义文件命名时，回退到 `--hf-repo` 加上 `--hf-file`。
7. 仅当仓库没有直接提供 GGUF 文件时才从 Transformers 权重转换。

## 快速开始

### 安装 llama.cpp

```bash
brew install llama.cpp
winget install llama.cpp
```

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
make
```

### 访问受限仓库的身份验证

```bash
hf auth login
```

### 搜索 Hub

```text
https://huggingface.co/models?apps=llama.cpp&sort=trending
https://huggingface.co/models?search=Qwen3.6&apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending
```

### 直接从 Hub 运行

```bash
llama-cli -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_M
llama-server -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_M
```

### 运行精确的 GGUF 文件

```bash
llama-server \
    --hf-repo unsloth/Qwen3.6-35B-A3B-GGUF \
    --hf-file Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
    -c 4096
```

### 仅在没有 GGUF 时转换

```bash
hf download <repo-without-gguf> --local-dir ./model-src
python convert_hf_to_gguf.py ./model-src \
    --outfile model-f16.gguf \
    --outtype f16
llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M
```

### 本地服务器冒烟测试

```bash
llama-server -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_M
```

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer no-key" \
  -d '{
    "messages": [
      {"role": "user", "content": "Write a limerick about exception handling"}
    ]
  }'
```

## 量化选择

- 优先使用 HF 在 `?local-app=llama.cpp` 页面上标记为兼容的精确量化版本。
- 保留仓库原生标签如 `UD-Q4_K_M`，而不是规范化它们。
- 默认为 `Q4_K_M`，除非仓库页面或硬件配置文件另有建议。
- 内存允许时，代码或技术工作负载优先考虑 `Q5_K_M` 或 `Q6_K`。
- 对于更紧张的 RAM 或显存预算，考虑 `Q3_K_M`、`Q4_K_S` 或仓库特定的 `IQ` / `UD-*` 变体。
- 将 `mmproj-*.gguf` 文件视为投影器权重，而非主检查点。

## 加载参考

- 阅读 [hub-discovery.md](references/hub-discovery.md) 了解 URL 优先工作流、模型搜索、树 API 提取和命令重构。
- 阅读 [quantization.md](references/quantization.md) 了解格式表格、模型缩放、质量权衡和 `imatrix`。
- 阅读 [hardware.md](references/hardware.md) 了解 Metal、CUDA、ROCm 或 CPU 构建和加速详情。

## 资源

- llama.cpp: `https://github.com/ggml-org/llama.cpp`
- Hugging Face GGUF + llama.cpp 文档: `https://huggingface.co/docs/hub/gguf-llamacpp`
- Hugging Face Local Apps 文档: `https://huggingface.co/docs/hub/main/local-apps`
- Hugging Face Local Agents 文档: `https://huggingface.co/docs/hub/agents-local`
- GGUF 转换器 Space: `https://huggingface.co/spaces/ggml-org/gguf-my-repo`
