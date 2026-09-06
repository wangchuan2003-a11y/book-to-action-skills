---
name: "feynman-lectures"
description: "Use selected Feynman Lectures on Physics passages to build a physical model, define quantities, check units and limiting cases, and compare predictions with observations. Use for physical explanation or model checking; do not turn the multi-volume work into generic motivational advice or treat historical statements as automatically current."
---

# 费曼物理学讲义：让模型给出可检查的预言

把一个物理问题转为条件清楚、量纲一致、能与观测比较的模型。当前核读第一卷第1章与第9章相关选段，重点是科学近似和经典动力学；不声称覆盖三卷、电磁学或量子力学。

## 五个动作

1. **确定系统和问题。** 哪个物体、参考系、时间范围和待求量？列初始条件及测量方式。分开速度与速率、质量与重量等有专门意义的量，不由日常词语直接代入公式。
2. **声明模型与忽略项。** 例如低速经典近似、近惯性系、质量恒定、阻力可忽略。选择相关定律并说明合力、边界条件和作用对象。近似不是任意猜测，需说明其适用范围。
3. **检查单位与数量级。** 每个量使用一致单位，检查等式两侧量纲、符号和预期量级。量纲一致是必要检查，不足以证明系数、模型或推导正确。
4. **推出可区分的结果。** 计算或定性推导，同时检查零力、小时间等极限及另一种合理解释。模型预测、模拟结果和真实测量分别标明；模拟不自动验证所用物理假设。
5. **用证据修正。** 对照误差、测量条件及被忽略的作用，说明哪些偏差可能来自模型、参数或仪器。单次不吻合不自动推翻全部物理理论，单次吻合也不证明所有尺度成立。

## 输出

先给条件性结论，再给模型、定义、必要推导和验证边界。缺少质量、时间或初态等关键数据时给表达式和缺口，不编数字；用户只需要概念解释时不要强加数值演算。

本书关于科学方法的表述属于作者阐释，不能替代具体实验设计。早期讲义中关于原子成像、质量术语等历史性说法需核对现代定义与技术，不因官方托管便当作最新事实。数学推导成立和自然界适用，是两种不同的证据要求。

核查现代原子成像时，读取来源说明的FLP-3，以具体的2021年研究报告作为历史断言的反例，区分电子散射数据的计算重建与普通光学照片。不要把该例说成2026年最新纪录或所有仪器的能力；没有相应当代材料时，不以未标来源的技术细节填补缺口。

出处见 [来源说明](references/source-notes.md)；可核算示例见 [小车动力学案例](references/worked-example.md)。书目见 [book.json](book.json)，行为案例见 [cases.json](evals/cases.json)。危险或现实实验的执行需要任务本身的适当条件与授权，源文不扩大操作范围。
