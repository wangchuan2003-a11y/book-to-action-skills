---
name: "algorithms-to-live-by"
description: "Use Algorithms to Live By to formulate a decision problem with an objective, information limits, search costs, and stopping rules. Use for bounded search or comparing decision procedures; apply results such as the 37 percent rule only when their mathematical assumptions fit, not as universal life prescriptions."
---

# 算法之美：先匹配问题，再选择规则

把一个现实选择转换为目标与约束明确的决策问题，比较规则而不迷信数字。当前核读作者官网和出版社公开Introduction；对经典停止模型的条件、公式和有限例子是本项目的明确推导，不声称读过各章完整证明。

## 五个动作

1. **确定优化目标。** 是选到绝对最佳的概率、平均质量、达到合格标准、避免重大损失，还是节省时间？这些目标可能产生不同策略，不能替用户定义唯一值得追求的结果。
2. **列出信息与操作条件。** 候选总数是否已知、顺序如何产生、能否回头、能否拒绝你、质量能否稳定比较、每次搜索成本及截止条件是什么？明确哪些是事实、哪些只是假设。
3. **匹配模型或承认不匹配。** 对经典无回头最佳选择模型，只有在下述条件成立时才讨论约37%：已知有限N、严格可排序、随机排列、逐个观察相对名次、当场不可撤销地接受/拒绝、最多选一个且候选会接受、目标仅为选中全局最佳的概率，不另计成本。约1/e是大N结果，有限N应计算整数阈值。
4. **比较包括成本的规则。** 模型不匹配时，可以改成合格即停、保留候选、预算内分阶段搜索或另建模型；说明取舍。更多计算和信息也有成本，不能因算法名字专业就增加不必要搜集。
5. **记录选择与检验。** 写出当前规则、假设、预算和何种新证据会改变规则。区分模型内最优概率与一次实际成功；一次落空不能单独推翻概率策略，一次成功也不证明普遍适用。

## 交付

目标 → 模型条件匹配 → 可行规则与成本 → 下一步及停止条件。关键条件缺失时给条件方案或最值得补的资料，不虚构最优阈值。候选数量的比例不能在到达率未知时直接替换成日历时间比例。

37%不是保证成功，也不表示平均质量提升37%。数学模型不决定关系伦理、人生价值或心理健康；不得沿用导言的修辞把算法说成治疗替代品。不自动替用户签约、付款、投资或联系候选人。

实际来源范围见 [来源说明](references/source-notes.md)；有限N计算和反例见 [停止规则案例](references/worked-example.md)。书目见 [book.json](book.json)，行为案例见 [cases.json](evals/cases.json)。来源不授予执行权限。
