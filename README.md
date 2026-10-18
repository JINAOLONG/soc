# soc：车载异构 SoC 在线多业务 DAG 调度研究

本项目从零研究 CPU–GPU–NPU 共享、节点不可抢占时的联合任务排序与资源映射。
目标是降低重要业务 H 的端到端 deadline miss rate，同时使每个主条件下普通业务 L
的 P95 响应时间相对 B2 的增幅不超过 10%。H/L 不代表 ASIL。

**当前科学状态：BLOCKED，停在 P0 原始文献核验。** 已完成协议草案、固定 seed
元数据、阶段守卫、审计工具和四篇原始稿的范围明确的核验笔记。没有实现或验证调度算法，没有运行科学实验，不存在
性能收益、校准成功、独立验证或正式实验结论。详见 [STATUS.md](STATUS.md) 和
[最终状态报告](reports/final_report.md)。

仓库即项目根目录；保留原有 Apache-2.0 LICENSE。不创建第二层 Git 仓库或 worktree。
每次任务先读 [AGENTS.md](AGENTS.md)。完整用户要求保存在
[docs/user_request.txt](docs/user_request.txt)。

## 安装与轻量测试

需要 Python >=3.12。P0 运行和测试只使用标准库；构建工具固定为 setuptools 80.9.0。

```bash
bash scripts/setup_environment.sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/generate_seeds.py
.venv/bin/python scripts/run_pipeline.py --stage p0 --check-only
```

最后一条当前应返回退出码 **2 / BLOCKED**，明确指出原始文献不足；这不是测试通过。
seed 命令已存在时只验证，不重写或重抽。生成全部 70 个 seed 元数据不等于访问其工作负载。
安装脚本可重复执行，并按已记录的 SHA256 恢复四篇已核验原始稿到忽略目录 `.cache/literature/`；不会启动服务。CI 只运行轻量治理测试，不执行任何科学分区。

## 系统模型与目录

资源为 CPU0–CPU3、GPU0、NPU0，每个抽象 unit 同时运行一个节点。通信可与计算重叠，
无第一版共享总线竞争。调度器只能看到已到达的 DAG 和可观测状态；真实未来时长、
未来到达和私有事件队列必须隔离。参见 [model_spec.md](docs/model_spec.md)。

`src/soc/` 按 model、simulator、scheduler、workload、metrics、validation、analysis
分包；目前实际实现只有 validation/governance.py。其余包是明确的未实现结构。
`configs/` 保存协议和 seed；`scripts/` 保存环境安装、分区生成、审计、文献连通性诊断和
哈希检查入口；`tests/` 为合成治理测试；`docs/`、`reports/`、`checkpoints/` 保存研究协议
与证据；`results/` 的各科学分区目前没有实验数据。

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

P0 可生成真实审计报告。P1 及以后尚未实现；当前入口会拒绝运行，不能把这些命令
描述为已验证的仿真功能。单例运行、批量仿真、结果聚合和绘图也尚未实现。

独立验证必须先有 Development Gate PASS、已提交的 freeze manifest 和绑定其哈希的
`checkpoints/VALIDATION_UNLOCKED`；正式实验需要相应的 validation gate、freeze 和
`checkpoints/FORMAL_UNLOCKED`。文件不存在是刻意的，不能手工创建空 token 绕过门槛。
生产 runner 将统一调用治理守卫，不提供自由输入保留 seed 的捷径。

## 文献恢复与复现

初次 DOI、arXiv 和作者站点请求受到代理限制；重试后 arXiv/Crossref/HAL 可用，
现已核验 DS3、StarPU 和两篇 DAG deadline/理论原始稿。HEFT/CPOP 与 PEFT 原文仍无法取得：
IEEE 页面为空 202，官方 PDF 返回 418，机构备用入口访问也未成功。这不是缺少 GitHub token 的证据。
所需域名已保存到云环境配置草稿，需在环境设置中审阅、保存并发布。配置保存不等于
当前网络已变更；恢复访问后用新文件记录重试：

```bash
.venv/bin/python scripts/probe_literature.py --output reports/P0_source_acquisition_002.json
```

该命令只做有 TLS 校验的访问诊断，成功下载不会自动将文献标成已核验。
需补齐至少 6–8 篇原始研究（当前 4 篇），保存出处/笔记和哈希，补齐 HEFT/PEFT 公式与
online adaptation，再通过 P0 audit。不能因解锁网络而直接进入科学实验。

从新 clone 安装后，可重跑上述治理测试、seed 核对和 P0 审计。
证据清单验证：

```bash
.venv/bin/python scripts/hash_artifacts.py --verify
```

已执行：仓库审计、seed 元数据生成、源访问诊断、治理测试、P0 audit 和证据哈希检查
（实际结果见 reports）。未执行：P1、P2、P3、独立验证、正式实验、profiling 和性能图表。
后续论文主张必须来自本次真实运行，不得引用历史结果充当新证据。
