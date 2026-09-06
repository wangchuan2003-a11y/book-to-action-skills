# 来源与理论边界

核实日期：2026-09-07。以下中文均为独立解释，没有再分发章节。

## BW1 · 原书公开工作稿

[Chapter 1: The Ladder of Causation](https://bayes.cs.ucla.edu/WHY/why-ch1.pdf)实际读取三层、图模型、关联、干预、反事实的相关段落。正文区分观察正发生的X、主动改变X以及对同一已发生案例询问另一种情形。

PDF标有 Unedited working copy, do not quote。本项目不从它摘引句子或给正式版页码。作者关于远古认知变化和动物能力的叙事，与因果层级的形式结论不同；未作为进化学共识或当前AI能力证据。

## BW2 · 技术补充来自另一本教材

[The Effects of Interventions](https://bayes.cs.ucla.edu/PRIMER/primer-ch3.pdf)为Pearl、Madelyn Glymour和Nicholas Jewell的《Causal Inference in Statistics: A Primer》（2016）第三章，实际读取3.1—3.3相关正文。

干预在模型中改变变量的生成方式；观察条件化仅选择满足条件的样本，两者不同。后门准则提供图假设成立时的调整集合规则；它并不从数据自动证实图。教材也给出碰撞点参与有效调整集合的情形，故不能把单个节点标签当作所有模型的禁调规则。复杂图应检查整个集合对路径的作用。

公式能否从有限样本可靠估计，还需要支持范围、测量和统计方法等条件。本Skill的项目记录与试验卡属于应用设计，不是这本书的逐字步骤。

## BW3 · 书目与公开来源链

[UCLA作者书页](https://bayes.cs.ucla.edu/WHY/index.html)明确列出Judea Pearl与Dana Mackenzie、Basic Books、2018年5月15日，以及BW1公开章节链接。书页还有勘误，未逐项核对；因此不声称已校验正式版所有细节。

## 实用原则映射

- 先确定关联/干预/反事实：BW1。
- 因果图陈述假设、区分看到与做到：BW1、BW2第3.1节。
- 判断目标可识别后再估计：BW2第3.2—3.3节。
- 调整集合与碰撞路径：BW2第3.3节。
- 记录人群、时间、处理版本、重叠及验证设计：本项目补充；真实效果需要任务数据。

曾尝试的Hachette链接返回集团首页而非书页，未作为书目证据。
