---
name: hf-mem
description: Hugging Face CLI，用于估算从 Hugging Face Hub 加载 Safetensors 或 GGUF 模型权重进行推理所需的内存
---

`hf_mem` 使用 HTTP Range 请求，无需下载或在本地加载任何权重，即可估算 Hugging Face Hub 上 Safetensors 和 GGUF 模型进行推理所需的内存，包括模型权重和可选的 KV 缓存。

## 何时使用？

- 用户询问某个模型运行需要多少显存或内存
- 用户想知道某个模型是否能放进他们的 GPU 或某种特定实例
- 用户提到某个 Hugging Face 模型 ID 或 URL，并询问推理所需资源

## 有哪些前置要求？

- 已安装 `uv`（用于 `uvx`）
- 设置了 `HF_TOKEN` 环境变量或 `--hf-token` 参数（仅对受限或私有模型需要）

## 如何运行？

使用 `--model-id` 指向 Hugging Face Hub 仓库运行，该命令会检查仓库中是否包含 Safetensors（通过 `model.safetensors`、分片时的 `model.safetensors.index.json`，或 Diffusers 的 `model_index.json`）或 GGUF 模型权重。

```bash
uvx hf-mem --model-id <model-id> --json-output
```

如果仓库中包含多种精度/量化版本的 GGUF 模型权重，估算结果将按文件逐一给出，而推理时你并不会加载所有这些文件，只会加载其中一种精度。因此，对于 GGUF，你可能还需要提供 `--gguf-file` 来指定要运行的具体文件（如果是分片的，则指定路径）。

```bash
uvx hf-mem --model-id <model-id> --gguf-file <file-or-path> --json-output
```

此外，`hf-mem` 还提供了一个 `--experimental` 参数，可以同时计算 KV 缓存的内存需求，这对大语言模型很有用，意味着它适用于 LLM（`...ForCausalLM`）、VLM（`...ForConditionalGeneration`）和 GGUF 模型。

至于上下文窗口，它会读取默认值，或者用 `--max-model-len` 覆盖（类似 vLLM 的做法）。KV 缓存精度同理，默认与模型精度一致，除非通过 `--kv-cache-dtype` 手动设置（同样类似 vLLM 的做法）。

对于 Safetensors，用法如下：

```bash
uvx hf-mem --model-id <model-id> --experimental [--max-model-len N] [--batch-size N] [--kv-cache-dtype auto|bfloat16|fp8|fp8_ds_mla|fp8_e4m3|fp8_e5m2|fp8_inc] --json-output
```

对于 GGUF，用法如下：

```bash
uvx hf-mem --model-id <model-id> --gguf-file <file-or-path> --experimental [--max-model-len N] [--batch-size N] [--kv-cache-dtype auto|F32|F16|Q4_0|Q4_1|Q5_0|Q5_1|Q8_0|Q8_1|Q2_K|Q3_K|Q4_K|Q5_K|Q6_K|Q8_K|IQ2_XXS|IQ2_XS|IQ3_XXS|IQ1_S|IQ4_NL|IQ3_S|IQ2_S|IQ4_XS|I8|I16|I32|I64|F64|IQ1_M|BF16|TQ1_0|TQ2_0|MXFP4] --json-output
```

## 示例

对于使用 Safetensors 权重的 Transformers：

```bash
uvx hf-mem --model-id MiniMaxAI/MiniMax-M2 --json-output
```

对于使用 Safetensors 权重的 Diffusers：

```bash
uvx hf-mem --model-id Qwen/Qwen-Image --json-output
```

对于使用 Safetensors 权重的 Sentence Transformers：

```bash
uvx hf-mem --model-id google/embeddinggemma-300m --json-output
```

使用 `--experimental` 为 LLM 和 VLM 计算 KV 缓存估算：

```bash
uvx hf-mem --model-id mistralai/Mistral-7B-v0.1 --experimental --json-output
```

以及，对于使用 GGUF 权重的 LLM 或 VLM：

```bash
uvx hf-mem --model-id unsloth/Qwen3.5-397B-A17B-GGUF --gguf-file Q4_K_M --experimental --json-output
```
