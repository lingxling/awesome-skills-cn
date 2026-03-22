---
name: "speech"
description: "当用户要求通过 OpenAI 音频 API 进行文本转语音旁白、配音、可访问性阅读、音频提示或批量语音生成时使用；使用内置语音运行捆绑的 CLI（`scripts/text_to_speech.py`）并需要 `OPENAI_API_KEY` 进行实时调用。自定义语音创建超出范围。"
---


# 语音生成技能

为当前项目生成口语音频（旁白、产品演示配音、IVR 提示、可访问性阅读）。默认为 `gpt-4o-mini-tts-2025-12-15` 和内置语音，并且更喜欢捆绑的 CLI 以实现确定性、可重现的运行。

## 何时使用
- 从文本生成单个口语片段
- 生成一批提示（多行、多个文件）

## 决策树（单个 vs 批量）
- 如果用户提供多行/提示或想要多个输出 → **批量**
- 否则 → **单个**

## 工作流程
1. 确定意图：单个 vs 批量（见上面的决策树）。
2. 提前收集输入：精确文本（逐字）、所需的语音、交付风格、格式以及任何约束。
3. 如果是批量：在 tmp/ 下编写临时 JSONL（每行一个作业），运行一次，然后删除 JSONL。
4. 将指令增强为简短的标记规范，而不重写输入文本。
5. 使用合理的默认值运行捆绑的 CLI（`scripts/text_to_speech.py`）（见 references/cli.md）。
6. 对于重要片段，验证：可理解性、节奏、发音和遵守约束。
7. 使用单一目标更改（语音、速度或指令）进行迭代，然后重新检查。
8. 保存/返回最终输出并注意使用的最终文本 + 指令 + 标志。

## 临时和输出约定
- 使用 `tmp/speech/` 作为中间文件（例如 JSONL 批量）；完成后删除。
- 在此仓库中工作时，将最终工件写入 `output/speech/`。
- 使用 `--out` 或 `--out-dir` 控制输出路径；保持文件名稳定和描述性。

## 依赖项（如果缺少则安装）
更喜欢 `uv` 进行依赖管理。

Python 包：
```
uv pip install openai
```
如果 `uv` 不可用：
```
python3 -m pip install openai
```

## 环境
- 必须设置 `OPENAI_API_KEY` 才能进行实时 API 调用。

如果缺少密钥，请为用户提供这些步骤：
1. 在 OpenAI 平台 UI 中创建 API 密钥：https://platform.openai.com/api-keys
2. 在他们的系统中将 `OPENAI_API_KEY` 设置为环境变量。
3. 如果需要，提供引导他们为其操作系统/shell 设置环境变量的指导。
- 永远不要要求用户在聊天中粘贴完整的密钥。要求他们在本地设置并准备好时确认。

如果在此环境中无法安装，请告诉用户缺少哪个依赖项以及如何在本地安装它。

## 默认值和规则
- 除非用户请求其他模型，否则使用 `gpt-4o-mini-tts-2025-12-15`。
- 默认语音：`cedar`。如果用户想要更明亮的音调，更喜欢 `marin`。
- 仅内置语音。自定义语音超出此技能的范围。
- 支持 GPT-4o mini TTS 模型的 `instructions`，但不支持 `tts-1` 或 `tts-1-hd`。
- 每个请求的输入长度必须 <= 4096 个字符。将较长的文本分成块。
- 强制执行 50 个请求/分钟。CLI 将 `--rpm` 上限为 50。
- 在任何实时 API 调用之前要求 `OPENAI_API_KEY`。
- 向最终用户提供明确的披露，表明语音是 AI 生成的。
- 对所有 API 调用使用 OpenAI Python SDK（`openai` 包）；不要使用原始 HTTP。
- 更喜欢捆绑的 CLI（`scripts/text_to_speech.py`）而不是编写新的一次性脚本。
- 永远不要修改 `scripts/text_to_speech.py`。如果缺少某些内容，请在做任何其他事情之前询问用户。

## 指令增强
将用户方向重新格式化为简短的、标记的规范。仅使隐含细节显式化；不要发明新的要求。

快速澄清（增强 vs 发明）：
- 如果用户说"演示的旁白"，您可以添加隐含的交付约束（清晰、稳定的节奏、友好的语气）。
- 不要引入用户未要求的新角色、口音或情感风格。

模板（仅包括相关行）：
```
语音效果：<语音的整体特征和纹理>
语气：<态度、正式度、温暖度>
节奏：<慢、稳定、轻快>
情感：<要传达的关键情感>
发音：<要清晰发音或强调的单词>
停顿：<添加有意停顿的位置>
强调：<要强调的关键单词或短语>
交付：<抑扬顿挫或节奏说明>
```

增强规则：
- 保持简短；仅添加用户已经暗示或别处提供的细节。
- 不要重写输入文本。
- 如果任何关键细节缺失并阻止成功，请提问；否则继续。

## 示例

### 单个示例（旁白）
```
输入文本："Welcome to the demo. Today we'll show how it works."
指令：
语音效果：温暖和镇定。
语气：友好和自信。
节奏：稳定和适中。
强调：强调"demo"和"show"。
```

### 批量示例（IVR 提示）
```
{"input":"Thank you for calling. Please hold.","voice":"cedar","response_format":"mp3","out":"hold.mp3"}
{"input":"For sales, press 1. For support, press 2.","voice":"marin","instructions":"Tone: Clear and neutral. Pacing: Slow.","response_format":"wav"}
```

## 指令最佳实践（简短列表）
- 将方向构建为：效果 → 语气 → 节奏 → 情感 → 发音/停顿 → 强调。
- 保持 4 到 8 行简短；避免冲突的指导。
- 对于名称/缩写，添加发音提示（例如，"清晰发音 A-I"）或在文本中提供语音拼写。
- 对于编辑/迭代，重复不变量（例如，"保持节奏稳定"）以减少漂移。
- 使用单一更改后续进行迭代。

更多原则：`references/prompting.md`。复制/粘贴规范：`references/sample-prompts.md`。

## 按用例的指导
当请求是针对特定交付风格时，使用这些模块。它们提供有针对性的默认值和模板。
- 旁白/解释器：`references/narration.md`
- 产品演示/配音：`references/voiceover.md`
- IVR/电话提示：`references/ivr.md`
- 可访问性阅读：`references/accessibility.md`

## CLI + 环境说明
- CLI 命令 + 示例：`references/cli.md`
- API 参数快速参考：`references/audio-api.md`
- 指令模式 + 示例：`references/voice-directions.md`
- 如果网络批准/沙盒设置阻碍：`references/codex-network.md`

## 参考地图
- **`references/cli.md`**：如何通过 `scripts/text_to_speech.py` 运行语音生成/批量（命令、标志、配方）。
- **`references/audio-api.md`**：API 参数、限制、语音列表。
- **`references/voice-directions.md`**：指令模式和示例。
- **`references/prompting.md`**：指令最佳实践（结构、约束、迭代模式）。
- **`references/sample-prompts.md`**：复制/粘贴指令配方（仅示例；没有额外的理论）。
- **`references/narration.md`**：旁白和解释器的模板 + 默认值。
- **`references/voiceover.md`**：产品演示配音的模板 + 默认值。
- **`references/ivr.md`**：IVR/电话提示的模板 + 默认值。
- **`references/accessibility.md`**：可访问性阅读的模板 + 默认值。
- **`references/codex-network.md`**：环境/沙盒/网络批准故障排除。
