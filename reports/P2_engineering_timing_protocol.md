# P2 engineering timing protocol — BLOCKED / NOT_FROZEN

现有 metric_spec.md 给出完整决策路径的 host P95 <=2 ms 目标，并要求 P2 在
candidate timing 前冻结精确 inputs、warmup、repetitions、timer 和 aggregation。
当前没有这些登记值；本轮只核验缺口，不把此文件当作已批准 timing 协议，不计时，
不修改 2 ms 目标，也不推断汽车硬件时延。

P2_calibration.md 列出本轮实验前阻断。恢复执行前应明确既有协议下的具体 timing
定义和实现范围；本文件仅保留 NOT_FROZEN 状态，不引入新的验收条件。
