---
name: clinical-decision-support
description: 准备和验证仅用于研究的临床决策支持评估、证据概况、队列、生存分析、生物标志物/模型、隐私和治理相关的产物。支持汇总或合成研究文档及可追溯性，不包括患者护理和实时临床操作。
license: MIT
compatibility: Python 3.11+; local files only; bundled scripts use the standard library and require no network, credentials, API keys, LLMs, or image services.
metadata:
  version: "2.4"
  last-reviewed: "2026-09-30"
  skill-author: K-Dense Inc.
---

# 临床决策支持研究与评估

## 严格的安全边界

本技能仅生成**研究、评估、文档和治理类产物**。

永远不要用它来：

- 诊断或对某个人进行分类；
- 推荐、选择、排序、开始、停止或修改治疗；
- 计算或传达针对特定患者的剂量；
- 分诊、排序优先级、报警、警示或判定紧急程度；
- 做出或自动化针对特定患者的临床决策；
- 支持床旁、即时护理点或实时临床操作；
- 取代专业判断，或取代一个经过验证且获得授权的临床系统；
- 声称拥有FDA授权、符合监管合规性、符合HIPAA合规性或法律合规性。

如果某个请求可能影响对某个人的护理，请停止该工作流，并使用经过
本地验证且获得适当授权的系统，将此事转交给一名持证医疗专业人员。
不要将针对特定患者的护理转交给另一个技能处理。

## 适用范围

- 研究类产物的预期用途和局限性声明
- 带有披露控制的汇总队列表格框架
- 统计分析计划和生存分析计划审查
- 汇总模型或生物标志物性能评估
- 透明的GRADE证据概况核查清单
- 证据来源和决策逻辑的可追溯性
- 去标识化流程核查清单
- 公平性、子群体、校准、不确定性、外部验证、监测、变更控制、
  审计以及人因工程方面的文档

产出物在合格人员批准之前仍属于草稿。报告指南可以提高透明度；但
它不能确立研究质量、临床效用、安全性、有效性、授权或合规性。

## 数据门槛

在运行任何脚本之前：

1. 让负责的人工审核者确认并记录输入数据是合成的或经过汇总的。
   脚本无法通过字段名称或所声明的元数据来确定这一点。
2. 拒绝患者行、记录、叙述、标识符、自由文本、与个人关联的日期、
   图像、波形或基因组序列。
3. 保持源文件为本地文件。不要抓取URL、调用API、读取环境变量，或
   将数据发送给模型。
4. 在生成表格之前设定披露阈值。
5. 记录来源、数据截取日期、人群、排除标准、缺失情况以及转换过程。

这些脚本对文件大小、组数、行数和文本长度设有上限。它们会拒绝类似
URL的路径和常见的行级键。这些控制措施可以减少意外的误用；它们不
构成隐私判定。

## 必需的产物页眉

每个产物都必须明确包含：

- `artifact_type`、标题、版本、状态、所有者、日期以及变更摘要；
- 预期目的、预期用户、汇总人群范围以及决策角色；
- 硬性边界中的所有禁止用途；
- 数据级别以及未提供PHI或原始行数据的确认；
- 局限性、不确定性以及可预见的失效模式；
- 外部验证和子群体适用性的状态；
- 人工审核的角色、完成状态以及批准边界；
- 带版本或日期的来源引用；
- 监测、变更控制、退役以及审计方面的预期；
- 以下声明：**不用于患者护理或实时临床使用。**

从 `assets/artifact_intended_use_template.json` 开始。

## 工作流

### 1. 界定研究问题

- 在查看结果之前定义估计目标或评估目标。
- 区分描述性、预后性、预测性、诊断准确性和因果性问题。
- 预先指定结局指标、时间起点、时间范围、子群体、分界点、缺失数据
  处理、多重比较以及敏感性分析。
- 将探索性发现与验证性分析区分开来。

### 2. 选择产物

| 需求 | 资源 | 脚本 |
|---|---|---|
| 预期用途/治理审查 | `assets/artifact_intended_use_template.json` | `scripts/validate_cds_artifact.py` |
| GRADE证据概况 | `assets/evidence_profile_template.json` | `scripts/evidence_profile_check.py` |
| 汇总模型/生物标志物评估 | `assets/aggregate_model_evaluation_template.json` | `scripts/model_biomarker_evaluation.py` |
| 汇总队列表格 | `assets/aggregate_cohort_table_template.json` | `scripts/cohort_table_generator.py` |
| 生存分析计划 | `assets/survival_analysis_plan_template.json` | `scripts/survival_plan_validator.py` |
| 逻辑可追溯性矩阵 | `assets/decision_logic_traceability_template.json` | `scripts/decision_logic_traceability.py` |
| 去标识化流程审查 | `assets/deidentification_checklist_template.json` | `scripts/deidentification_checklist.py` |

### 3. 在本地运行

所有辅助工具都不依赖外部包。从技能目录下运行以下命令：

```bash
python3 scripts/validate_cds_artifact.py --help
python3 scripts/evidence_profile_check.py --help
python3 scripts/model_biomarker_evaluation.py --help
python3 scripts/cohort_table_generator.py --help
python3 scripts/survival_plan_validator.py --help
python3 scripts/decision_logic_traceability.py --help
python3 scripts/deidentification_checklist.py --help
```

只将输出写入一个经过审查的本地目录。永远不要将生成的报告放入
电子病历（EHR）、警报系统、临床门户或设备工作流中。

### 4. 人工审核

要求与产物相称的审核：

- 由方法学家/统计学家负责设计和分析；
- 由领域专家负责临床科学背景；
- 由隐私官或合格专家负责披露决策；
- 由监管或法律顾问负责特定司法辖区的解读；
- 由人因工程专家负责用户研究；
- 由获得授权的治理所有者负责发布和变更控制。

脚本运行成功只意味着已声明的字段和内部一致性检查通过了。

## GRADE证据概况

不要从文章文本、单独的研究设计、p值或关键词中推断确定性等级。
不要将旧式的`1A/2B`简写当作通用的GRADE输出来使用。

对于每一个重要的结局指标，一个人工小组必须记录：

- 偏倚风险；
- 不一致性；
- 间接性；
- 不精确性；
- 发表/传播偏倚；
- 任何适用的升级考量因素；
- 效应估计值及其不确定性；
- 每一项判断的理由和来源ID；
- 最终的确定性判断及被指名的审核角色。

该检查工具只验证完整性和引用链接。它从不计算确定性或推荐强度。
参见 `references/evidence_profiles.md`。

## 汇总模型与生物标志物评估

不要衍生阈值、分配分子或疾病类别、匹配疗法，或输出个体层面的
预测。

该评估工具只接受汇总的混淆计数和校准分箱数据。未定义的比例为
`null`；当任一观察到的结局类别缺失时，平衡准确率为`null`。无效
输入会产生诊断信息，而不会产生部分评估结果。它报告带有Wilson
区间的有限描述性指标、校准差距、子群体差异以及显式的抑制处理。
它不判定公平性、临床效用或适用性。需要：

- 已锁定的模型/检测方法/版本，以及预先指定的阈值来源；
- 具有代表性的内部验证以及独立的外部验证；
- 与目标相适应的校准性和鉴别力；
- 抽样设计和患病率：来自富集样本或病例对照样本的预测值和校准
  结果描述的是该样本，而不会自动适用于预期使用的人群。记录统计
  学家提供的任何独立合理的加权或患病率调整；不要从原始的选定
  样本计数推断总体预测值；
- 带有不确定性和样本量的子群体表现；
- 缺失情况、谱系/选择偏倚、数据集偏移以及检测方法的变异性；
- 相关时的人因工程和前瞻性评估；
- 监测、变更控制、回滚以及退役标准。

参见 `references/model_biomarker_evaluation.md`。

## 队列表格

仅使用汇总单元格。不要向生成器提供行级数据。

- 在已批准的披露政策下选择最小单元格阈值。
- 应用主要和补充性抑制。
- 报告分母和缺失情况。
- 避免将基线显著性检验用作平衡性诊断。
- 标注调整后、未调整、预先指定和探索性的结果。
- 不要将关联解读为因果关系或临床可操作性。

默认阈值是一种操作上的安全保障，不是HIPAA规则或保证。参见
`references/cohort_evaluation.md` 和
`references/privacy_and_disclosure.md`。

## 生存分析计划

将时间零点、事件、竞争事件、截尾、并发事件、估计目标、时间范围
以及分析人群一起定义。

- 在将风险比视为恒定之前评估比例风险假设。
- 预先指定替代方案，例如时变效应或限制性平均生存时间。
- 当竞争事件重要时，使用累积发生率方法。
- 处理不朽时间偏倚、信息性截尾、延迟进入、缺失数据以及多重比较
  方面的风险。
- 包含敏感性分析和不确定性，而不仅仅是p值。

随附的辅助工具验证的是一份计划；它不分析生存数据。参见
`references/survival_analysis.md`。

## 决策逻辑

只记录研究或治理逻辑，例如证据纳入、验证关卡、发布暂缓以及人工
审核检查点。每个节点都必须链接到来源ID、测试、所有者、版本和
状态。

不要编码护理路径、紧急程度、用药操作、诊断规则、警报或面向患者的
输出。参见 `references/decision_logic_traceability.md`。

## 隐私与去标识化

HHS规定的方法是专家判定法和安全港法。一份核查清单本身无法执行
这两种方法中的任何一种。不要声称移除一份字段列表、对标识符进行
哈希处理、使用最小单元格大小，或通过该脚本就能证明达成了去标识化
或符合HIPAA合规性。

该辅助工具会清点已记录的人工工作。它从不读取数据集。应将未解决的
项目、自由文本、日期、地理信息、罕见组合、关联风险、基因组学以及
纵向模式升级至合格的隐私审查。

## 报告指南的选择

- 队列/病例对照/横断面研究：STROBE；对于常规收集的数据，补充
  RECORD。
- 预测模型的开发/评估：TRIPOD+AI和PROBAST+AI；对于LLM特定的研究
  报告，使用TRIPOD-LLM。
- 肿瘤预后标志物研究：REMARK。
- AI诊断准确性：STARD-AI配合STARD。
- AI试验方案：SPIRIT-AI配合当前的SPIRIT基础声明。
- AI随机试验报告：CONSORT-AI配合当前的CONSORT基础声明。
- 早期实时AI评估：DECIDE-AI——但实时评估超出了本技能的执行范围。

这些是报告或评价工具，不是自动化的质量评分。参见
`references/study_reporting.md`。

## 监管与治理背景

FDA的设备身份认定取决于预期用途和功能，而不是文档标签。FDA在
2026年1月发布的CDS指南将某些非设备类CDS功能与设备软件功能区分
开来；其示例并不是一份自我认证核查清单。ONC HTI-1的要求适用于其
已定义的认证范围内。ICH E6(R3)和E9/E9(R1)为试验治理和统计规划提供
参考，但不能使某个产物因此合规。

有关带日期的背景信息，请使用
`references/regulatory_and_governance.md`。对于实际的产品、研究、
申报、部署或司法辖区问题，请获取合格的建议。

## 验证

从仓库根目录运行测试套件（pytest会加载共享的CLI契约）：

```bash
uv run --with pytest python -m pytest tests/clinical-decision-support -q
python tests/run_all.py --isolated clinical-decision-support
```

从技能目录下，运行不生成字节码的AST编译检查：

```bash
python3 -c "import ast,pathlib; [ast.parse(p.read_text()) for p in pathlib.Path('scripts').glob('*.py')]"
```

## 参考文件索引

- `references/README.md` — 范围和导航
- `references/safety_and_scope.md` — 拒绝和升级处理规则
- `references/regulatory_and_governance.md` — FDA、ONC、ICH背景
- `references/evidence_profiles.md` — 人工GRADE工作流
- `references/study_reporting.md` — EQUATOR和PROBAST+AI的选择
- `references/cohort_evaluation.md` — 汇总队列方法
- `references/survival_analysis.md` — 事件发生时间规划
- `references/model_biomarker_evaluation.md` — 模型/生物标志物评估
- `references/privacy_and_disclosure.md` — 去标识化和抑制
- `references/decision_logic_traceability.md` — 治理逻辑
- `references/sources.md` — 带日期的权威来源清单
- `references/security_validation.md` — 扫描结果以及已接受的LOW级
  发现

## 引用 Scientific Agent Skills

本技能是K-Dense的Scientific Agent Skills的一部分。如果它对一篇
手稿、报告、演示文稿或代码发布产生了实质性贡献，请将该论文添加到
参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。该DOI以及https://arxiv.org/abs/2609.00065 会解析
到最新的arXiv版本，因此永远不要附加如`v1`这样的版本后缀。当有网络
访问时，在撰写参考文献之前获取
https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录
中获取作者列表、年份和版本信息。如果该记录列出了期刊引用信息或
出版商DOI，则改为引用已发表的版本。
