---
name: datalad
description: 使用DataLad和git-annex检索、版本化和发布科学数据集，并通过datalad run、rerun和containers-run记录计算溯源。当从OpenNeuro、DANDI、datasets.datalad.org或任何DataLad数据集克隆或获取数据时使用；当数据集中的文件读取为损坏的符号链接或小型指针文件而非真实数据时使用；当分析需要每个输出如何生成的机器可读记录以便重新执行时使用；或在将数据集发布到诸如GitHub仓库加存储remote的sibling时使用。也可用于为携带数据的仓库在DataLad和纯Git之间做出选择。
compatibility: Requires Python 3.10+, DataLad 1.6.5, Git, and git-annex 10.x. Tested with git-annex 10.20260901 and datalad-container 1.2.6 on macOS ARM64. Containers additionally require Singularity, Apptainer, or Docker. Remote data access needs network access and may need provider credentials. Local filesystem workflows work offline.
license: MIT
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.2"
  last-reviewed: "2026-09-30"
  skill-author: Dylan Pulver
---

# DataLad

## 概述

DataLad 是构建在 Git 和 git-annex 之上的数据管理层。Git 跟踪数据集的
结构、小型文本文件和历史记录。git-annex 跟踪大文件的*内容*，将每个
文件存储为一个键，并将其字节保存在一个不一定是本地仓库的位置。

一次普通的克隆会检索 Git 历史记录和顶层文件清单，而将已纳入 annex 的
字节留在未获取状态。已安装的子数据集有各自的历史记录；克隆不会自动
填充它们。克隆成本取决于 Git 历史记录和文件数量，而不仅仅是数据量。
使用 `datalad get` 选择性地检索已纳入 annex 的字节。

DataLad 添加的第二件事是溯源。`datalad run` 执行一个命令，并将结果
与该命令、其输入和输出的机器可读记录一起提交。`datalad rerun` 读回
该记录并重新执行它。这把"这张图是怎么产生的"从一个考古问题变成了
一条命令。

## 何时使用 DataLad 而非纯 Git

在以下任何情况下使用 DataLad：

- 文件对 Git 来说太大，无法舒适地处理，或者总量超过了每位协作者希望
  保存在磁盘上的量。
- 数据存在于多个位置（实验室服务器、集群临时存储、S3、超级计算机），
  你需要知道存在哪些副本。
- 分析必须是可重新执行的，仅靠提交信息不足以作为证据。
- 你正在使用来自 OpenNeuro、DANDI 或 `datasets.datalad.org` 的已发布
  数据集，它们以 DataLad 数据集的形式分发。
- 项目内部嵌套了其他数据集，并且你希望每个数据集保留各自独立的历史
  记录。

当仓库只包含代码和文本、一切都能舒适地放入 Git、并且没有人需要部分
检出时，使用纯 Git。在一个小型纯代码仓库上叠加 DataLad 只会增加间接
层，而没有任何好处。

## 安装

```bash
# git-annex 并非用 Python 编写，但如果你已经安装了 git 本身，
# 可以从 PyPI 获取：
uv pip install git-annex
# 你也可以先从系统安装它
# （Debian/Ubuntu: apt install git-annex；macOS: brew install git-annex；
#  conda-forge: conda install -c conda-forge git-annex）
uv pip install "datalad==1.6.5"
uv pip install "datalad-container==1.2.6"   # 仅用于containers-run

datalad wtf --section dependencies   # 确认git-annex版本可见
```

PyPI 的 `git-annex` 包提供平台特定的二进制文件。经过审查的
10.20260901.post1 wheel 涵盖 Linux glibc 2.34+（x86_64/ARM64）、macOS
ARM64 14+ 和 x86_64 15+，以及 Windows x86_64。当没有匹配的 wheel 时，
使用系统包。保持其环境在 `PATH` 中，并验证可执行文件；该 wheel 本身
不提供 Git。在创建或保存数据集之前先配置 Git 作者姓名/邮箱。

`datalad wtf` 会打印解析后的环境，当行为看起来不可能时，这是首先要
运行的命令。过旧或缺失的 git-annex 是导致大量令人困惑错误的常见原因。

DataLad 采用 MIT 许可；git-annex 拥有单独的 AGPL 许可。在重新分发
任一工具时，请查阅上游许可。

## 首先碰到的失败：指针不是数据

执行 `datalad clone` 后，已纳入 annex 的文件以指向
`.git/annex/objects/` 的符号链接形式存在（或者在符号链接不可用的
情况下，例如在 Windows 或受限文件系统上，以小型指针文件的形式存在）。
此时内容尚未被下载。

这是一个示意性的远程数据示例；请检查所选修订版本以获取确切路径，
并在 Python 读取之前安装 NiBabel。此次复核在不下载影像数据的情况下
测试了等效的本地指针/get 行为。

```bash
datalad clone https://github.com/OpenNeuroDatasets/ds000001.git
cd ds000001
ls sub-01/anat/            # 文件已列出
python -c "import nibabel; nibabel.load('sub-01/anat/sub-01_T1w.nii.gz')"   # 失败
datalad get sub-01/anat/sub-01_T1w.nii.gz                                   # 现在可以工作了
```

需要识别的失败模式：某个工具报告文件为空、被截断、损坏、"不是 gzip
文件"，或是一个损坏的符号链接，且磁盘上的文件大小只有几百字节。这些
症状可能表示一个尚未获取的 annex 指针；在诊断为损坏之前，先用 annex
状态确认。**在读取数据之前运行 `datalad get`，并将"文件存在"视为其
内容已存在的不充分证据。**

在分析触及某个目录之前，明确地获取它：

```bash
datalad get sub-01/                  # 某路径下的所有内容
datalad get -r .                     # 所有内容，包括子数据集
datalad get -n -r .                  # 仅子数据集结构，不含文件内容
```

`datalad status --annex availability` 检查本地当前存在哪些内容，而
`git annex whereis <path>` 报告哪些仓库持有给定文件。`whereis` 读取
记录的状态，不会联系 remote，因此它告诉你的是 git-annex 最后一次了解
到的情况，而不是当前真实的情况。

有关查找数据集、子数据集行为、安全地丢弃内容以及修复数据集的内容，
请参阅 [data-access.md](references/data-access.md)。

## 用 datalad run 记录溯源

`datalad run` 是在方法学背景下选择使用 DataLad 的原因。它将命令与其
效果一起保存在同一个提交中：

一个示意性的 FSL 示例（需要 `bet` 以及一个已存在的 `derivatives/`
目录）：

```bash
datalad run -m "extract brain and mask" \
  --input "sub-01/anat/sub-01_T1w.nii.gz" \
  --output "derivatives/sub-01_brain.nii.gz" \
  --output "derivatives/sub-01_brain_mask.nii.gz" \
  "bet {inputs[0]} {outputs[0]} -m"
```

每个部分的作用，以及跳过它为何会带来问题：

- `--input` 会在运行之前检索内容，因此命令不会因为指针而失败。它还
  会记录依赖关系，这正是让 `rerun` 能在另一台机器上获取相同输入的
  原因。
- `--output` 会先解锁或移除目标，这样 git-annex 就不会拒绝覆写它正在
  保护的内容。如果不这样做，同一命令的第二次运行通常会在一个看起来
  只读的已纳入 annex 的文件上失败，报出权限错误。
- `{inputs}` 和 `{outputs}` 会展开为这些值。`{pwd}`、`{dspath}` 和
  `{tmpdir}` 也可用，`{inputs[0]}` 用于索引单个条目。
- 提交信息在 `=== Do not change lines below ===` 和
  `^^^ Do not change lines above ^^^` 之间携带一条 JSON 运行记录。
  不要手动编辑该区块；`rerun` 会解析它。

当数据集存在未保存的修改时，`datalad run` 会拒绝启动，因为不干净的
起始状态会使记录不可靠。先保存或丢弃变更，或者传入 `--explicit`
以仅保存声明的输出。这不会捕获未保存的输入变更；在声称运行是可重现
的之前，保存所有依赖项。使用 `--dry-run basic` 或 `--dry-run command`
在提交之前检查命令。

一次不改变任何内容的运行不会产生提交，这与 `datalad save` 的行为
完全相同。

`run` 记录的是命令和数据集状态；它不会冻结任意的主机安装软件或外部
服务。将环境锁定文件和脚本作为声明的输入进行版本控制，或者使用
`containers-run` 搭配一个受跟踪的容器镜像。记录随机种子和相关的运行
时设置，然后在声称具有计算可重现性之前，在一个全新环境中测试
`rerun`。

### 重新执行

```bash
datalad rerun                       # 重做记录在HEAD处的运行
datalad rerun --report              # 显示将要执行的内容，不改变任何东西
datalad rerun --script recompute.sh # 提取命令而不是运行它们
datalad rerun --since <commit> -b check <revision>   # 将一个范围重放到新分支
```

`--report` 只检查计划，不会执行或验证结果。分支（`-b`）会保留原始的
提交记录，但使用相同的工作树。有关从首次运行之前开始的
`--since`/`--onto` 重放，请参阅参考文档，并同时比较 annex 键或内容
校验和以及科学输出。

### 容器

借助 `datalad-container` 扩展，注册一次镜像，此后每次运行都会记录是
哪个镜像产生了这些输出：

一个使用先前构建的本地 SIF 镜像的示意性容器工作流（在本次复核中
未执行；需要运行时和镜像才能实际执行）：

```bash
datalad containers-add fsl --url /path/to/fsl.sif \
  --call-fmt 'apptainer exec {img} {cmd}'
datalad containers-run -n fsl -m "brain and mask in container" \
  --input "sub-01/anat/sub-01_T1w.nii.gz" \
  --output "derivatives/sub-01_brain.nii.gz" \
  --output "derivatives/sub-01_brain_mask.nii.gz" \
  "bet {inputs[0]} {outputs[0]} -m"
```

镜像本身被跟踪在数据集中，因此软件环境会随着数据和溯源记录一起
传播，而不是停留在某人的 shell 历史记录中。当只配置了一个容器时，
可以省略 `-n`。

有关 STAMPED 原则和 YODA 项目布局、运行记录格式、`--explicit` 和
`--assume-ready` 语义，以及向 W3C PROV 导出溯源信息，请参阅
[provenance.md](references/provenance.md)。

## 保存和检查变更

```bash
datalad status                 # 发生了什么变化，包括子数据集状态
datalad save -m "add QC report" path/to/file
datalad save -m "checkpoint" -r                 # 递归进入子数据集
datalad save -m "small text file" --to-git notes.md
```

`datalad save` 会根据数据集的 `.gitattributes`，为每个文件决定内容
应放入 Git 还是 git-annex。使用 `--to-git` 可以强制将一个文件放入
Git，这对于应保持直接可读的代码和小型文本文件是正确的选择。
`yoda` 流程（`datalad create -c yoda`）会自动为 `code/`、`README.md`
和 `CHANGELOG.md` 设置好这一点。

## 创建数据集

```bash
datalad create my_dataset               # 普通数据集
datalad create -c yoda my_analysis      # 分析布局（code/被Git跟踪，
                                        # README.md和CHANGELOG.md已预配置）
datalad create -d . inputs/raw          # 在现有数据集下注册一个新子数据集
```

`-c yoda` 应用了在 [provenance.md](references/provenance.md) 中描述的
分析项目布局。`-d .` 的作用是将一个新数据集注册为父数据集的子数据集，
而不是在其中留下一个无关的仓库。

## 发布

一个 DataLad 数据集通常会同时发布到两个地方：一个用于历史记录的 Git
托管服务，以及一个用于已纳入 annex 内容的存储 remote。

一个示意性的已认证发布示例（会创建远程资源；需要 GitHub 令牌和 S3
凭据）。仅在组织命名空间场景下使用 `myorg/mydataset`。

```bash
datalad create-sibling-github mydataset
git annex initremote store type=S3 bucket=my-bucket protocol=https \
  encryption=none autoenable=true
datalad siblings configure -s github --publish-depends store
datalad push --to github
```

Git sibling 和存储 sibling 是故意由不同工具创建的。Git sibling 是一
个 Git remote，`datalad create-sibling-*` 处理的是面向托管服务的那些。
一个 S3 存储桶（或 WebDAV，或一个 SSH 目录）是一个 *git-annex 特殊
remote*，不是一个 Git remote，因此要用 `git annex initremote` 来创建
它。之后 `datalad siblings` 会拾取该特殊 remote，并将其当作其他任何
sibling 来处理。在这里使用 `datalad siblings add --url s3://...` 正是
本节要防止的错误：`--url` 是一个 Git remote URL，而 S3 不是，接下来
的 `push --to github` 就会在 `--publish-depends` 这一步失败。

`--publish-depends` 正是用来阻止那种常见的损坏发布的：一个 Git 仓库
的历史记录引用了从未上传过的内容，于是协作者成功克隆之后，却发现每
一次 `datalad get` 都失败。声明这个依赖关系能保证存储 sibling 每次
都先发布。

`datalad push` 默认会发送 Git 历史记录，以及（`--data
auto-if-wanted`）由目标的 wanted 设置所选定的已纳入 annex 的内容；
如果没有 wanted 设置，则会传输所有已选定的当前内容。`--data anything`
会绕过首选内容过滤，但不会恢复缺失的本地字节，也不会归档每一个历史
版本。

有关 RIA 存储、特殊 remote、凭据处理以及配置哪个 sibling 持有哪些
内容，请参阅 [publishing.md](references/publishing.md)。

## 释放磁盘空间

```bash
git annex whereis sub-01/                 # 先检查记录的位置
datalad drop sub-01/                      # 移除本地内容，保留指针
```

`datalad drop` 默认会检查所需的副本数和可用性。`--nocheck` 已被弃用，
取而代之的是 `--reckless availability`，它会禁用这些保护措施。
`--if-dirty` 已被弃用并会被忽略；它不是一个可用性检查选项。`--what`
用于在 `filecontent`（默认值）、`allkeys`、`datasets` 和 `all` 之间
选择。

## 值得了解的失败模式

| 症状 | 原因 | 修复方法 |
|---|---|---|
| 文件读取为空、被截断或是一个损坏的符号链接 | 内容未被检索；只存在指针 | `datalad get <path>` |
| 写入一个已存在的输出时"权限被拒绝" | git-annex对已纳入annex的内容进行了写保护 | 用`--output`声明它，或使用`datalad unlock <path>` |
| `datalad run`拒绝启动 | 数据集有未保存的修改 | 先执行`datalad save`，或传入`--explicit` |
| `datalad drop`拒绝执行 | 该内容没有经验证的第二份副本 | 推送到一个可访问的sibling，然后重试安全检查 |
| 协作者克隆成功，但每次`get`都失败 | 历史记录在没有内容的情况下被发布 | 发布存储sibling，并设置`--publish-depends` |
| 克隆成功，子数据集目录为空 | 子数据集默认不会被安装 | `datalad get -n -r .`，然后对需要的路径执行`get` |
| 命令行为异常 | git-annex缺失或过旧 | `datalad wtf --section dependencies` |

## 详细参考

- [data-access.md](references/data-access.md)：查找已发布数据集
  （`registry.datalad.org`、OpenNeuro、DANDI、`datasets.datalad.org`
  以及 `///` 快捷方式）、克隆和获取选项、子数据集处理、annex 内容
  状态、丢弃和移除，以及 `fsck` 修复。
- [provenance.md](references/provenance.md)：STAMPED 原则和 YODA
  布局、运行记录格式、`run` 和 `rerun` 的完整选项、`containers-run`，
  以及将 DataLad 溯源信息向 W3C PROV 导出的当前状态。
- [publishing.md](references/publishing.md)：sibling 及其操作、
  `create-sibling-*` 变体、RIA 存储、特殊 remote、`push` 语义，以及
  凭据处理。

## 相关技能

`bids` 技能涵盖脑影像数据结构（Brain Imaging Data Structure），即大
多数通过 DataLad 分发的神经影像数据集所采用的组织方式。一个典型的
工作流是用 DataLad 克隆一个 BIDS 数据集，用 BIDS 工具链验证它，然后
在 `datalad containers-run` 下运行一个 BIDS-App，这样衍生数据就会带
有溯源信息。

## 验证范围

于 2026-09-30 针对 DataLad 1.6.5 和 datalad-container 1.2.6 的源代码
以及当前官方手册进行了复核。小型本地测试涵盖了克隆/获取/丢弃、解锁
后的保存、子数据集安装、run/rerun、默认的 push 选择，以及
RIA 发布/克隆/获取。远程托管、凭据、FSL 以及容器执行示例均为示意性
内容；未执行任何经认证的远程发布或科学数据下载。

## 主要来源

- DataLad 文档：<https://docs.datalad.org/en/stable/>
- DataLad 手册：<https://handbook.datalad.org/en/latest/>
- `datalad run` 章节：<https://handbook.datalad.org/en/latest/basics/101-108-run.html>
- YODA 原则：<https://handbook.datalad.org/en/latest/basics/101-127-yoda.html>
- STAMPED 原则（从 YODA 操作化而来）：<https://stamped-principles.org>
- datalad-container：<https://docs.datalad.org/projects/container/en/stable/>
- git-annex：<https://git-annex.branchable.com/>
- 数据集注册表：<https://registry.datalad.org>

## 致谢

本技能的主题范围部分参考了 @bcmcpher 采用 MIT 许可的
[datalad-cli](https://github.com/bcmcpher/my-skills/tree/main/plugins/datalad-cli)
插件（十九个按命令划分的斜杠命令技能）。此处的文字是独立撰写的，并
以上游 DataLad 文档为基础；由于两者都涉及 DataLad，重叠是不可避免
的，但结构、风格和具体的技术性论断是不同的。
