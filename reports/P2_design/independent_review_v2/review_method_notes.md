# Review method and correction record

独立指重新编写metadata检查及反例，不依赖v1的94项checker结论；本审计由同一协作助手完成，
不主张人员/机构独立，也不是外部第三方背书。没有实施或运行M1/M2/科学runner。

CMD-069首次逻辑检查把ADV-03（dedup契约）列为FAIL。复核后发现v1已明确要求重复状态
只计一次，因此这个反例只证明full record ID不能直接当state key，不证明任何现有dedup
实现违反要求。已将ADV-03更正为NOT_VERIFIED契约缺口，归V2-F04；不计入最终已演示
设计验收失败。初版脚本/输出及原命令stdout完整保留为adversarial_checks_initial.*与ledger。
最终验收失败为ADV-01/ADV-02，两项；7个反例/代数辅助检查本身全部通过。
本记录不会将审计器的判断修正冒充项目源码缺陷。

STATUS.md未改：用户本轮明确仅新增本目录报告，优先于AGENTS.md日常同步状态的通用要求。
当前v2结论由本目录executive_decision/cross_decision_consistency表达，不覆盖v1声明或旧gate。
