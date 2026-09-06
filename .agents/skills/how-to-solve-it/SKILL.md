---
name: "how-to-solve-it"
description: "Use George Polya's problem-solving heuristics to understand a precise problem, devise and execute a plan, and check the result. Use for mathematical reasoning, algorithmic puzzles, and structured troubleshooting; empirical or value-laden decisions need evidence beyond a proof-style method."
---

# How to Solve It：把卡住的问题拆成可推进的步骤

给出真正的解题进展，并让每一步可以检查。依据 Princeton 的书籍说明、官方目录与引言核实方法归属；以下流程是围绕四阶段与启发式条目的原创操作化，未冒充全书精读。

## 理解问题

用简短文字或符号写清未知量、已知条件、允许的操作和答案形式。先检查条件是否足够、是否互相矛盾；不能为了得出唯一答案而擅自补关键条件。非关键细节可以标明假设后继续。

合适时画最小示意图、列小表或举边界例子，目的是暴露结构。对已足够清楚的简单题，直接解，不机械展示每个阶段。

## 制定并执行计划

卡住时只选一个最有希望的启发式：

- 找一个结构相似、已解决的问题，并指出相同条件与差异。
- 暂时简化规模或约束，寻找不变量、规律或可用引理；回到原题时补回删去的条件。
- 从想要的结论倒推必要条件，再检查这些条件是否充分。
- 分解成可以单独验证的子问题，或换表示方式以减少无关细节。

说明为什么当前策略适用，然后推进具体计算或推理。逐步检查关键转换：除数能否为零、平方是否引入伪解、边界/单位是否一致、算法是否覆盖空输入等。少量样例可用于发现错误，不能代替一般证明。

## 回顾与迁移

把结果代回原条件；必要时换一条独立路径核查，并说明可适用范围。若结论取决于假设，给条件答案。若证据不足，交付已经推出的部分及缺口，不把“尝试了很多”写成解决。

提炼一个能用于下一题的结构事实，而非只记本题答案。引导教学时，用户要求练习才用递进提示：先提示表示方式或相关问题，再提示关键步骤；不要在用户尚未尝试时一次泄露全部过程。用户直接要答案时则给答案及必要理由。

## 方法边界

数学证明、程序测试和现实因果证据不同：算法在几个样例上工作不证明它正确；商业、医学或组织问题不能仅凭逻辑自洽便确认现实效果。用户的价值取舍也不能从数学方法推出。

读 [来源说明](references/source-notes.md) 核查四阶段与启发式归属；读 [围栏与面积案例](references/worked-example.md) 查看如何检查条件、结果及反例。书目见 [book.json](book.json)，行为评估见 [cases.json](evals/cases.json)。遇到书内逐页问题须依据实际文本，不能凭目录补写内容。
