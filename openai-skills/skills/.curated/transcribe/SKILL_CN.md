---
name: "transcribe"
description: "使用可选的说话人分离和已知说话人提示将音频文件转录为文本。当用户要求从音频/视频转录语音、从录音中提取文本或在采访或会议中标记说话人时使用。"
---


# 音频转录

使用 OpenAI 转录音频，并在请求时进行可选的说话人分离。更喜欢捆绑的 CLI 以实现确定性、可重现的运行。

## 工作流程
1. 收集输入：音频文件路径（一个或多个）、所需的响应格式（text/json/diarized_json）、可选的语言提示以及任何已知的说话人参考。
2. 验证 `OPENAI_API_KEY` 已设置。如果缺少，请要求用户在本地设置它（不要要求他们粘贴密钥）。
3. 使用合理的默认值（快速文本转录）运行捆绑的 `transcribe_diarize.py` CLI。
4. 验证输出：转录质量、说话人标签和段边界；如果需要，使用单一目标更改进行迭代。
5. 在此仓库中工作时，将输出保存在 `output/transcribe/` 下。

## 决策规则
- 默认使用 `gpt-4o-mini-transcribe` 和 `--response-format text` 进行快速转录。
- 如果用户想要说话人标签或分离，请使用 `--model gpt-4o-transcribe-diarize --response-format diarized_json`。
- 如果音频长于约 30 秒，请保持 `--chunking-strategy auto`。
- 不支持 `gpt-4o-transcribe-diarize` 的提示。

## 输出约定
- 使用 `output/transcribe/<job-id>/` 进行评估运行。
- 使用 `--out-dir` 处理多个文件以避免覆盖。

## 依赖项（如果缺少则安装）
更喜欢 `uv` 进行依赖管理。

```
uv pip install openai
```
如果 `uv` 不可用：
```
python3 -m pip install openai
```

## 环境
- 必须设置 `OPENAI_API_KEY` 才能进行实时 API 调用。
- 如果缺少密钥，请指示用户在 OpenAI 平台 UI 中创建密钥并在其 shell 中导出。
- 永远不要要求用户在聊天中粘贴完整的密钥。

## 技能路径（设置一次）

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export TRANSCRIBE_CLI="$CODEX_HOME/skills/transcribe/scripts/transcribe_diarize.py"
```

用户范围的技能安装在 `$CODEX_HOME/skills` 下（默认：`~/.codex/skills`）。

## CLI 快速开始
单个文件（快速文本默认）：
```
python3 "$TRANSCRIBE_CLI" \
  path/to/audio.wav \
  --out transcript.txt
```

带有已知说话人的分离（最多 4 个）：
```
python3 "$TRANSCRIBE_CLI" \
  meeting.m4a \
  --model gpt-4o-transcribe-diarize \
  --known-speaker "Alice=refs/alice.wav" \
  --known-speaker "Bob=refs/bob.wav" \
  --response-format diarized_json \
  --out-dir output/transcribe/meeting
```

纯文本输出（明确）：
```
python3 "$TRANSCRIBE_CLI" \
  interview.mp3 \
  --response-format text \
  --out interview.txt
```

## 参考地图
- `references/api.md`：支持的格式、限制、响应格式和已知说话人说明。
