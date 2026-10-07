---
name: azure-communication-callingserver-java
description: "⚠️ 已弃用：此 SDK 已重命名为 Call Automation。对于新项目，请改用 azure-communication-callautomation。此技能仅用于维护旧代码。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Azure Communication CallingServer (Java) - 已弃用

> **⚠️ 已弃用**：此 SDK 已重命名为 **Call Automation**。对于新项目，请改用 `azure-communication-callautomation`。此技能仅用于维护旧代码。

## 迁移到 Call Automation

```xml
<!-- 旧版（已弃用） -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-callingserver</artifactId>
    <version>1.0.0-beta.5</version>
</dependency>

<!-- 新版（请使用此版本） -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-callautomation</artifactId>
    <version>1.6.0</version>
</dependency>
```

## 类名更改

| CallingServer（旧） | Call Automation（新） |
|---------------------|----------------------|
| `CallingServerClient` | `CallAutomationClient` |
| `CallingServerClientBuilder` | `CallAutomationClientBuilder` |
| `CallConnection` | `CallConnection`（相同） |
| `ServerCall` | 已移除 - 使用 `CallConnection` |

## 旧版客户端创建

```java
// 旧方式（已弃用）
import com.azure.communication.callingserver.CallingServerClient;
import com.azure.communication.callingserver.CallingServerClientBuilder;

CallingServerClient client = new CallingServerClientBuilder()
    .connectionString("<connection-string>")
    .buildClient();

// 新方式
import com.azure.communication.callautomation.CallAutomationClient;
import com.azure.communication.callautomation.CallAutomationClientBuilder;

CallAutomationClient client = new CallAutomationClientBuilder()
    .connectionString("<connection-string>")
    .buildClient();
```

## 旧版录制

```java
// 旧方式
StartRecordingOptions options = new StartRecordingOptions(serverCallId)
    .setRecordingStateCallbackUri(callbackUri);

StartCallRecordingResult result = client.startRecording(options);
String recordingId = result.getRecordingId();

client.pauseRecording(recordingId);
client.resumeRecording(recordingId);
client.stopRecording(recordingId);

// 新方式 - 请参阅 azure-communication-callautomation 技能
```

## 用于新开发

**不要为新项目使用此 SDK。**

有关以下内容，请参阅 `azure-communication-callautomation-java` 技能：
- 拨打出站电话
- 接听来电
- 电话录制
- DTMF 识别
- 文本转语音 / 语音转文本
- 添加/移除参与者
- 通话转移

## 触发短语

- "callingserver legacy"、"deprecated calling SDK"（已弃用的通话 SDK）
- "migrate callingserver to callautomation"（将 callingserver 迁移到 callautomation）

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
