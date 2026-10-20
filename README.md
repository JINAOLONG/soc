# soc：车载异构 SoC 在线多业务 DAG 调度研究

本项目从零研究 CPU–GPU–NPU 共享、节点不可抢占时的联合任务排序与资源映射。
目标是降低重要业务 H 的端到端 deadline miss rate，同时使每个主条件下普通业务 L
的 P95 响应时间相对 B2 的增幅不超过 10%。H/L 不代表 ASIL。

**当前 P0 文献与协议审计：PASS（实际退出码 0）。** 两份用户提供的 HEFT/CPOP、PEFT
原文已完成全文及页码审查，原有四篇原稿也重新核验了计数资格；17 项治理测试通过。
P1 已实现事件引擎、只读视图、B1–B5 和独立 Trace Validator；当前正确性证据见
[P1 报告](reports/P1_correctness_report.md) 与 [STATUS.md](STATUS.md)。科学工作负载运行数为 0，
P2 科学运行、P3、独立验证、正式评估均未启动。原 [P0 文献关闭报告](reports/P0_literature_gap_closure.md)
和 [P0 最终报告](reports/final_report.md) 保留为历史交付，不充当 P1 结果。

仓库即项目根目录；保留原有 Apache-2.0 LICENSE。不创建第二层 Git 仓库或 worktree。
每次任务先读 [AGENTS.md](AGENTS.md)。完整用户要求保存在
[docs/user_request.txt](docs/user_request.txt)。

## 安装与轻量测试

需要 Python >=3.12。P0/P1 运行和测试只使用标准库；构建工具固定为 setuptools 80.9.0。

```bash
bash scripts/setup_environment.sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/generate_seeds.py
.venv/bin/python scripts/run_pipeline.py --stage p0 --check-only
```

最后一条在六份原稿均已置于忽略缓存且哈希吻合时，当前应返回 **0 / PASS**。
缓存缺失或哈希不符会使原有检查失败；不能仅依据文档状态宣告通过。
seed 命令已存在时只验证，不重写或重抽。生成全部 70 个 seed 元数据不等于访问其工作负载。
安装脚本使用 `.cache/literature/`：四篇既有公开原稿可按 URL/SHA256 恢复；
两篇用户提供的私有阅读副本必须先手动补入并核对 SHA256（见下文）。当前实例六份均已核验。
CI 运行治理和手工合成正确性单测，不需要论文 PDF，不执行任何科学分区；正式 P0/P1 审计需要原文缓存。

## 系统模型与目录

资源为 CPU0–CPU3、GPU0、NPU0，每个抽象 unit 同时运行一个节点。通信可与计算重叠，
无第一版共享总线竞争。调度器只能看到已到达的 DAG 和可观测状态；真实未来时长、
未来到达和私有事件队列必须隔离。参见 [model_spec.md](docs/model_spec.md)。

`src/soc/` 按 model、simulator、scheduler、workload、metrics、validation、analysis
分包；P1 实现位于 model/schema.py、model/observation.py、simulator/engine.py、
scheduler/kernels.py、metrics/fixture.py、validation/trace.py 和 validation/p1.py。
P2 生成数值与分析原语已有工程实现；正式科学生成/执行流水线尚未部署，候选方法尚未定义。
`configs/` 保存协议和 seed；`scripts/` 保存环境安装、分区生成、审计、文献连通性诊断和
哈希检查入口；`tests/` 为治理和手工合成正确性测试；`docs/`、`reports/`、`checkpoints/` 保存研究协议
与证据；`results/` 的各科学分区目前没有实验数据。

## 当前云端 P2 工程验证

已记录用户接受的 D01–D10 限定条款、SP01–SP40、A2/B3，见
[批准记录](docs/P2_design/accepted/README.md)。`src/soc/p2/` 新增确定性数值、
S2 校验边界、B1 诊断、资格/分析原语、SQLite A 协调、A2/B3 与证据保存组件。
原 simulator、scheduler、种子和科学统计协议未改动。

当前完整正确性流程 **110 项测试通过、0 失败、0 跳过**；原45正例/20负例和精确重放通过。
另完成只读、非root、无网络/无Docker socket 的容器手工fixture检查，并核对镜像内源码哈希。
失败历史、真实子进程退出码/日志、fixture轨迹和清单位于
[本轮工程报告](reports/P2_engineering/implementation_001/README.md)。这些不是科学样本或性能结果。

```bash
.venv/bin/python -B scripts/run_p2_correctness.py
.venv/bin/python -B scripts/verify_p2_container.py
```

第二条需要Docker；每次生成独立工程验证目录。生产CALIBRATION编排和权威部署尚未接通，
持久化、lease、权限及独立科学授权未就绪，正式入口保持退出2并报告阻断原因。
工程测试通过不表示P2 PASS，不解锁后续分区。

## 阶段命令与锁

```bash
.venv/bin/python scripts/run_pipeline.py --stage p0
.venv/bin/python scripts/run_pipeline.py --stage p1
.venv/bin/python scripts/run_pipeline.py --stage calibration
.venv/bin/python scripts/run_pipeline.py --stage development
.venv/bin/python scripts/run_pipeline.py --stage validation
.venv/bin/python scripts/run_pipeline.py --stage formal
.venv/bin/python scripts/run_pipeline.py --stage report
```

本轮只执行 P0/P1；上面的后续阶段命令列为接口说明，不构成运行授权。
复现 P1（只运行手工 fixture）并验证产物：

```bash
.venv/bin/python scripts/run_p1_correctness.py
.venv/bin/python scripts/run_pipeline.py --stage p1
.venv/bin/python scripts/hash_artifacts.py --verify --output checkpoints/P1_artifact_manifest.json
```

P1 门禁重新检查 P0、用户批准的 D1–D5、代码/测试/输入/Trace 哈希、逐项测试身份、
45 份完整轨迹的独立校验和精确重放，以及 20 个非法轨迹的实际拒绝结果。
P2 工程组件已有正确性证据；完整生产科学编排及后续阶段尚未部署，科学批量运行和绘图未执行。

独立验证必须先有 Development Gate PASS、已提交的 freeze manifest 和绑定其哈希的
`checkpoints/VALIDATION_UNLOCKED`；正式实验需要相应的 validation gate、freeze 和
`checkpoints/FORMAL_UNLOCKED`。文件不存在是刻意的，不能手工创建空 token 绕过门槛。
生产 runner 将统一调用治理守卫，不提供自由输入保留 seed 的捷径。

## 文献恢复与复现

两篇本轮原稿的来源记录为 `USER_PROVIDED_LOCAL_COPY_SOURCE_UNVERIFIED`，没有虚构下载 URL。
现有 schema 的 `primary_url` 保存实际 `sediment://` 附件定位符，`download_url` 为 null；
附件定位符不代表 HTTP 自动下载接口。身份、版本、实际输入路径与 SHA256 位于
[源获取记录](reports/P0_source_acquisition_014.json) 和 [证据清单](docs/literature_evidence.json)。

PDF 不进入 Git。当前实例的两份副本位于忽略目录：

- `.cache/literature/HEFT_CPOP_Topcuoglu_2002.pdf`
- `.cache/literature/PEFT_Arabnejad_Barbosa_2014.pdf`

从新 clone 开始时，先重新提供这两份合法阅读副本，按清单核对实际 SHA256 并放入上述
路径，再运行安装和审计。现有 fetch helper 对已存在文件会核验哈希；它不能在缺少
私有副本时解析 `sediment://`。本次未修改该 helper，也未声称六份原稿可以从 GitHub 自动
恢复。历史网络获取失败和 BLOCKED 审计均保留在 reports/history 与原获取日志中。

原始算法与未来在线扩展的边界、全部必查公式/图号见
[HEFT/CPOP 原文审查](docs/literature_reviews/heft_cpop.md) 和
[PEFT 原文审查](docs/literature_reviews/peft.md)。P1 在线适配是经用户批准的项目定义，
见 [P1 实现规格](docs/P1_implementation_spec.md)，不能称为静态原算法复现。

从新 clone 安装后，可重跑上述治理测试、seed 核对和 P0 审计。
证据清单验证：

```bash
.venv/bin/python scripts/hash_artifacts.py --verify --output checkpoints/P1_artifact_manifest.json
```

P0_artifact_manifest.json 绑定历史 P0 提交的文件；它不会被覆盖为 P1 清单，不能用来验证
有意改变过的 P1 源码树。当前文件身份以 P1_artifact_manifest.json 为准。

已执行：P0 原文审查、治理审计及 P1 手工合成正确性测试（实际结果见 reports）。
未执行：P2、P3、独立验证、正式实验、profiling 和性能图表。
后续论文主张必须来自本次真实运行，不得引用历史结果充当新证据。
