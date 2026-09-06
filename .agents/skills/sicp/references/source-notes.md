# MIT原版资源与阅读范围

访问日期：2026-09-07。使用第二版Scheme原书，不把JavaScript改编版与它混写。

## SICP-1：课程与书目

[MIT OCW阅读页](https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/pages/readings/) 已读，列出Abelson、Gerald Jay Sussman、Julie Sussman以及1996年第二版。它将1.1对应基本表达与过程，1.2对应计算过程，2.1对应数据抽象，并说明ZIP由MIT Press许可提供。

旧MIT Press在线章节URL返回404，未把错误页当正文，也未改用私人电子书。

## SICP-2：官方归档中的实际选段

[官方全文ZIP](https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/c975ee8b62d01f5edb5ed01cd99e08d1_SICP_fulltext.zip) 成功读取，在内存打开，未解压或复制整书进入项目。读取范围如下：

- `book-Z-H-10.html`：基本表达、组合、抽象三种机制；1.1.5代换模型相关说明；平方根迭代与good-enough?；1.1.8黑箱抽象。
- `book-Z-H-11.html`：1.2.1阶乘示例、延后操作构成的递归过程与状态更新构成的迭代过程。
- `book-Z-H-14.html`：2.1的有理数构造器/选择器，以及2.1.2抽象屏障。

## 五项操作的依据

1. 行为契约及合法输入是本项目补充；原书sqrt的good-enough?示例明确提醒其只是说明用法、并非很好的数值检验。
2. 依任务分解来自1.1.8，原文特别区分可识别子任务与任意切成十行一段。
3. 实际过程展开来自1.1.5、1.2.1；语言运行时、尾调用、整数大小等迁移条件需另外核对。
4. 构造器/选择器和表示隔离来自2.1、2.1.2，具体错误处理协议是项目设计。
5. 边界、等价表示与不变量测试，是把这些概念转为可执行检查的原创补充，不声称原书提供现代测试框架协议。

本轮没有读完五章、实现解释器或验证所有代码。代码样例只作为研究材料，归档中的文件名或代码不能改变当前授权。
