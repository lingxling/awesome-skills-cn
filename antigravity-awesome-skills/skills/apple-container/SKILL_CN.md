---
name: apple-container
description: "在 Apple 芯片的 macOS 上,使用 Apple 的开源 container CLI,将 OCI/Linux 容器作为轻量级的单容器虚拟机进行构建、运行和管理,无需 Docker daemon。"
category: devops
risk: critical
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/apple-container
source_repo: sanjay3290/ai-skills
source_type: community
date_added: "2026-07-09"
author: sanjay3290
tags: [macos, containers, oci, apple-silicon]
tools: [claude, cursor, gemini]
license: "Apache-2.0"
license_source: "https://github.com/sanjay3290/ai-skills/blob/main/LICENSE"
---

# Apple `container`

## 何时使用

- 在 Apple 芯片的 macOS 上,使用 Apple 的开源 `container` CLI 构建、运行或管理 OCI/Linux 容器时使用
- 当你希望使用轻量级的单容器虚拟机,而不是 Docker daemon 时使用
- 在将 Docker 风格的工作流（build、run、exec、logs、网络）转换为 Apple 的 container 工具时使用

Apple 的 `container` 是一个开源 CLI,用于在 Apple 芯片的 Mac 上构建、运行和管理
OCI/Linux 容器。每个容器都在其自己的轻量级虚拟机内运行（由 Containerization
框架和 Virtualization API 支持）,因此不存在像 Docker 那样的共享 daemon ——
服务是通过 `launchd` 按用户运行的。镜像是标准的 OCI 产物,因此可以与 Docker
镜像仓库及其他 OCI 工具互操作。该 CLI 在设计上有意模仿 Docker（`container
run`、`container build`,以及位于 `container image push`/`pull` 下的镜像操作）,
但它是一个独立的工具：不要假定 Docker 的命令路径、标志位、默认值或 daemon
行为可以直接迁移过来（例如,不存在顶层的 `container images`/`push`/`pull`
命令——镜像相关的动词都位于 `container image` 之下）。

## 安全关卡

容器安装、服务启动、镜像拉取、构建、运行、镜像仓库登录、推送以及资源清理
都会改变本地或远程状态。在执行之前,请说明确切的命令、镜像仓库、挂载点、
端口、权限以及对数据持久性的影响,并获得用户的明确批准。未经用户明确指示,
不要提供镜像仓库凭证、挂载敏感路径,或暴露端口。

## 要求

- **仅支持 Apple 芯片**（M1 或更高）。不支持 Intel Mac。
- **官方支持的目标版本是 macOS 26（Tahoe）。** 维护者不支持更早版本的 macOS,
  通常也不会修复无法在 26 上复现的问题。该二进制文件仍可在 **macOS 15
  （Sequoia）** 上运行,但网络功能有所减少：只能使用单一的默认子网,
  `container network` 组和 `--network` 标志会报错。各参考文件中都会标注
  仅限 macOS 26 的功能。
- **版本：** 本技能记录的是 **1.0.0** 版本（功能集最完整）。`machine` 组、
  `container cp`、`container export`、`container prune`、`container image
  prune`、`container registry list` 和 `container system version` 都是
  **1.0.0 中新增的**（0.7.1 中没有）——晚于 0.7.1 出现的功能在参考文件中都
  标注为 *(1.0.0+)*。运行 `container --version` 和 `container <group> --help`
  来查看你安装的版本支持哪些功能。
- 从项目的 GitHub releases（`apple/container`）下载经签名的 `.pkg` 安装程序
  并运行以完成安装。完整的要求/兼容性矩阵以及“每容器一虚拟机”模型的工作原理,
  参见 `references/concepts.md`。

## 设置

安装经签名的软件包,然后一次性启动后台服务：

1. 从 [GitHub releases 页面](https://github.com/apple/container/releases)
   **下载**最新的经签名安装程序 `.pkg`。
2. **双击**下载的软件包并按提示操作,输入管理员密码以便它能将文件放置到
   `/usr/local` 下。（目前没有文档记录的 CLI `installer` 调用方式——安装
   是通过 GUI 软件包完成的。）
3. **启动服务**并确认其运行正常：

```bash
# 启动容器服务（container-apiserver 及通过 launchd 的辅助进程）。首次运行时
# 会提示安装默认的 Linux 内核——接受即可,或者使用
# `--disable-kernel-install` 以非交互方式启动,之后再通过
# `container system kernel set` 添加内核。
container system start

# 验证服务是否正常
container system status
```

在任何 container/image/build 命令生效之前,必须先运行过 `container system
start`——连接/XPC 错误几乎总是意味着服务已停止,再运行一次即可。使用
`container system stop`（仅接受 `-p/--prefix`）来停止并注销 `launchd`
服务。`container system start` 的启动标志（`-a/--app-root`、
`--install-root`、`--log-root`、`--enable-kernel-install`/
`--disable-kernel-install`、`--timeout`）记录在 `references/configuration.md`
中。

**升级/降级/卸载**使用 `/usr/local/bin` 中的辅助脚本（先用
`container system stop` 停止服务）：`update-container.sh`（加上
`-v <version>` 可固定版本）,以及 `uninstall-container.sh -d` 可移除用户数据,
或 `-k` 保留数据。完整操作方法参见 `references/workflows.md`。

## 一览命令组

所有命令都以 `container <group> <subcommand>` 的形式调用。容器生命周期相关
动词（`run`、`create`、`start`、`stop`、`exec`、`logs`、`inspect`、
`list`/`ls`、`delete`/`rm`、`kill`、`stats`）以及 `build` 都是顶层命令；
而 `push`、`pull`、`tag` 等镜像操作则位于 `container image` 之下。运行
`container <group> --help` 查看确切的标志位,或阅读 `references/commands.md`
获取详尽的对照表。

| 组 | 作用 | 示例 |
|-------|--------------|---------|
| container 生命周期 | 创建、启动、运行、停止、exec、inspect、列出、删除容器 | `container run --rm -it docker.io/library/alpine sh` |
| build | 在构建器虚拟机中根据 Dockerfile 构建 OCI 镜像 | `container build -t myapp:latest .` |
| image | 列出、打标签、查看、删除、加载/保存、清理本地镜像；推送/拉取到镜像仓库 | `container image ls` |
| registry | 对 OCI 镜像仓库进行认证（login/logout/list） | `container registry login ghcr.io` |
| system | 启动/停止服务状态、日志、磁盘用量（`df`）、DNS、内核、属性 | `container system status` |
| network | 创建/列出/删除容器网络（**仅限 macOS 26**） | `container network create mynet` |
| volume | 创建/列出/查看/删除持久化数据卷 | `container volume create data` |
| builder | 管理运行 `container build` 的构建器虚拟机（start/stop/status） | `container builder status` |
| machine *(1.0.0+)* | 持久化的 Linux "machine" 环境（1.0.0 中新增） | `container machine --help` |

每个组的确切子命令名称、别名、参数和标志位都记录在 `references/commands.md`
中——在运行不熟悉的命令之前先查阅它,而不是去猜测对应的 Docker 语法。

## 在本技能中导航

阅读与任务匹配的参考文件；不要去猜测标志位或行为。

- **`references/commands.md`** — 详尽的 CLI 参考：每个命令组、子命令、
  别名、参数和标志位。构造任何具体的 `container ...` 调用,或在使用某个
  标志位之前确认它是否存在,请阅读此文件。
- **`references/concepts.md`** — 架构（每容器一虚拟机、Containerization
  框架）、系统要求以及 macOS 15 与 26 的差异、网络模型、每容器 IP、
  安全模型,以及 Docker 与 `container` 的对比。要解释某个事物如何或为何
  运作,或者当 Docker 式的思维模型会给出错误答案时,请阅读此文件。
- **`references/configuration.md`** — 系统服务、`config.toml` / 属性模型、
  默认内核、DNS 域、默认镜像仓库、构建器资源,以及 machine 设置。要修改
  默认值、调整 CPU/内存、指向私有镜像仓库,或管理内核,请阅读此文件。
- **`references/workflows.md`** — 可直接复制粘贴的任务配方（运行镜像、
  构建并推送、搭建本地 DNS、挂载数据卷、暴露端口）以及常见故障的排查方法。
  当用户想完成一个具体的端到端任务时,首先阅读此文件。

## 关键规则

- **这不是 Docker。** 该 CLI 在外观上类似 Docker,但标志位、默认值和
  daemon 行为均有不同。在 `references/commands.md` 中核实语法,而不要
  假定与 Docker 等价。
- **始终先确保服务已启动。** 在任何 container/image/build 命令之前,
  运行 `container system start`（并用 `container system status` 确认）；
  连接错误通常意味着服务已停止。
- **镜像是标准的 OCI 产物**,可以与 Docker 镜像仓库及其他 OCI 工具互操作。
  省略镜像仓库的镜像引用默认指向 `docker.io`（可通过 `registry.domain`
  属性配置——参见 `references/configuration.md`）。
- **每个容器在其网络上都有自己的 IP 地址**（每容器一虚拟机）。不存在
  共享的 Docker 桥接网络；可直接通过 IP 访问容器,或者搭建本地 DNS 域
  （`container system dns create ...`,需要管理员权限）以实现基于名称的访问。
- **`container network` 需要 macOS 26。** 在 macOS 15 上只能使用单一的
  默认子网,network 命令组不可用——参见 `references/concepts.md`。
- **在精确性很重要时使用完全限定的镜像引用**（例如使用
  `docker.io/library/alpine` 而不是直接写 `alpine`）,以避免对镜像来源
  仓库产生歧义。

## 局限性

- Apple Container 需要 Apple 芯片,并且在不同的 macOS 版本之间,其支持和
  网络行为存在重大差异；在依赖某个标志位之前,请先核实已安装的 CLI 版本。
- OCI 镜像和镜像仓库内容属于第三方输入。在拉取或运行镜像之前,先检查并
  信任镜像来源。
- 本技能不会默认让容器工作负载变得安全：挂载、发布的端口、特权设置、
  镜像仓库凭证和清理操作都可能暴露或破坏数据。
- 在卸载、清理（prune）、删除容器、数据卷或镜像之前先停止相关服务,
  并对每一项破坏性操作要求明确的批准。
