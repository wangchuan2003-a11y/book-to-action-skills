---
name: "art-of-doing-science"
description: "Use Richard Hamming's research heuristics to choose an important tractable problem, challenge assumptions, and make technical work reusable and understandable. Use for research direction, engineering project selection, and stalled technical exploration; do not turn routine execution into a career intervention."
---

# Hamming：选择值得且能够推进的问题

将一个研究或工程方向收敛为有价值、存在攻击路径、能够获得反证的下一步。主要依据作者公开演讲《You and Your Research》及本书出版社说明；这是相关方法的应用 Skill，不是对全书技术章节的摘要。

## 选题与推进

从用户已有约束取得：要改善谁的什么结果、现有证据与能力、时间/资源边界、可交付物。已明确的执行任务直接推进；只有用户需要选题或方向诊断时，才讨论更大的研究组合。

1. **同时检验重要性和可攻击性。** 对最有希望的候选，分别写“解决后谁受益、现在哪里受限”和“凭哪些数据、理论、原型或实验能向前推进”。重大后果不等于当前可做；把宏大问题缩到有工具可试的一部分。
2. **把当前相信的解释与异常放在一起。** 写一条工作假说、一条最可能反驳它的观察，以及现在如何取得该观察。保留足够信心去试，也保留足够怀疑去改。没有相反证据不等于已证实。
3. **从一个实例寻找可复用的问题类别。** 先解决真实实例，再识别哪些输入、约束与结构可推广；用第二个不同实例检验。可复用方法有价值，但不能把尚未出现的需求都实现成框架。
4. **为外部线索留出入口。** 利用现有文档、用户反馈、同行意见或相邻领域方法更新问题选择。优先提出一个能改变决策的具体问题；“开门”是吸收线索的启发，不是要求持续打断专注。外部联系仍须遵守用户授权。
5. **把结果表达为别人能使用的证据。** 简明说明问题为何值得做、做了什么、数据/实验支持什么、局限和复用入口。按受众提供必要背景；表达改进不能替代技术验证。

## 输出

给出推荐问题、被搁置候选的具体原因、一页以内的实验卡：假说、最小行动、所需输入、成功/反证观察和资源上限。用户需要更多时再扩展。对实际实施过的试验报告真实结果；尚未执行的只称计划。

Hamming 的职业经验不是随机对照证据，也不保证伟大成就。不能把他的加班、压力、牺牲生活或“50% 时间做展示”等个人说法升级为通用处方。避免以名气评判用户工作价值。来源细节见 [来源说明](references/source-notes.md)；研究转可交付原型示例见 [工程选题案例](references/worked-example.md)。书目见 [book.json](book.json)，行为评估见 [cases.json](evals/cases.json)。
