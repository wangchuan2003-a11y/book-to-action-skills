# Book to Action Skills

把值得反复读的书，变成遇到真实问题时能调用的方法。

中文优先的开放 Agent Skills 书库：学习、解题、系统分析、预测、产品、策略与中西经典论证。每本书提供独立 Skill、来源说明、具体示例和行为评估案例。

首发的结构、交叉使用与真实Codex新会话验证见 [v0.1.0评估记录](evals/release-v0.1.0.md)。后续版本继续记录新增覆盖、失败与修复，不以书目数量代替实际效果。

[v0.2.0评估记录](evals/release-v0.2.0.md)覆盖新增12本、一次隐式加载和可重复准备案例的工具。

这里的“精选”是编辑选择，不是客观的世界排名。我们看重方法的解释力、来源的可核实性、跨情境的用途，以及能否说清什么时候不该用。

## 从一个问题开始

<!-- catalog:start -->
当前收录 **25 本书**、**72 条来源记录**、**96 个已编写行为案例**。来源记录不等于独立来源数量；案例已编写不代表全部执行。

| 你遇到的问题 | 书籍 / Skill |
| --- | --- |
| 区分知道与不知道 | [论语](.agents/skills/analects/SKILL.md) · `analects` |
| 筛选具有价值且可推进的技术问题 | [科学与工程的艺术（工作译名）](.agents/skills/art-of-doing-science/SKILL.md) · `art-of-doing-science` |
| 在资源约束下选择行动方案 | [孙子兵法](.agents/skills/art-of-war/SKILL.md) · `art-of-war` |
| 检查一个解释是否只是可任意改写的故事 | [无穷的开始](.agents/skills/beginning-of-infinity/SKILL.md) · `beginning-of-infinity` |
| 把相关问题改写为明确的干预问题 | [为什么：关于因果关系的新科学](.agents/skills/book-of-why/SKILL.md) · `book-of-why` |
| 理解商品、劳动与劳动力的差别 | [资本论：第一卷](.agents/skills/capital-volume-one/SKILL.md) · `capital-volume-one` |
| 诊断用户不知道如何操作的问题 | [设计心理学：日常事物的设计](.agents/skills/design-of-everyday-things/SKILL.md) · `design-of-everyday-things` |
| 诊断计划只有目标没有行动的问题 | [好战略，坏战略](.agents/skills/good-strategy-bad-strategy/SKILL.md) · `good-strategy-bad-strategy` |
| 诊断共享资源的过度使用与维护不足 | [公共事务的治理之道](.agents/skills/governing-the-commons/SKILL.md) · `governing-the-commons` |
| 把含糊题目转换成未知量和条件 | [怎样解题](.agents/skills/how-to-solve-it/SKILL.md) · `how-to-solve-it` |
| 区分概念证明与事实主张 | [人类理解研究](.agents/skills/human-understanding/SKILL.md) · `human-understanding` |
| 改造依赖重读和突击的学习计划 | [认知天性](.agents/skills/make-it-stick/SKILL.md) · `make-it-stick` |
| 面对批评时区分事实与评价 | [沉思录](.agents/skills/meditations/SKILL.md) · `meditations` |
| 分析行动目的与手段 | [尼各马可伦理学](.agents/skills/nicomachean-ethics/SKILL.md) · `nicomachean-ethics` |
| 审视团队规则对个人选择的限制 | [论自由](.agents/skills/on-liberty/SKILL.md) · `on-liberty` |
| 检验自然选择解释缺了哪些条件 | [物种起源](.agents/skills/origin-of-species/SKILL.md) · `origin-of-species` |
| 检验公平或正义的定义 | [理想国](.agents/skills/republic/SKILL.md) · `republic` |
| 判断所谓范式革命到底改变了什么 | [科学革命的结构](.agents/skills/scientific-revolutions/SKILL.md) · `scientific-revolutions` |
| 审查统一指标遗漏的工作情境 | [国家的视角](.agents/skills/seeing-like-a-state/SKILL.md) · `seeing-like-a-state` |
| 区分基因视角与个人自私的道德判断 | [自私的基因](.agents/skills/selfish-gene/SKILL.md) · `selfish-gene` |
| 把模糊趋势判断改为可结算预测 | [超预测](.agents/skills/superforecasting/SKILL.md) · `superforecasting` |
| 区分有用行动与过度干预 | [道德经](.agents/skills/tao-te-ching/SKILL.md) · `tao-te-ching` |
| 把引导性访谈问题改成事实问题 | [妈妈测试](.agents/skills/the-mom-test/SKILL.md) · `the-mom-test` |
| 诊断持续积压或产能失衡 | [系统之美](.agents/skills/thinking-in-systems/SKILL.md) · `thinking-in-systems` |
| 比较专业化收益与任务规模 | [国富论](.agents/skills/wealth-of-nations/SKILL.md) · `wealth-of-nations` |
<!-- catalog:end -->

如果只想开始：读过却记不住，选 `make-it-stick`；反复救火，选 `thinking-in-systems`；想开发但没验证需求，选 `the-mom-test`。

## 使用

克隆仓库，在仓库内打开 Codex，即可发现 `.agents/skills/` 中的 Skills：

```sh
git clone https://github.com/wangchuan2003-a11y/book-to-action-skills.git
cd book-to-action-skills
```

也可从 [Releases](https://github.com/wangchuan2003-a11y/book-to-action-skills/releases) 下载单本或完整集合。完整包解压后保留目录结构即可使用安装器，SHA256校验文件随包提供。

```text
用 $thinking-in-systems 分析：我们的客服越招人，待处理工单反而越多。
先指出需要核实的变量，给我一个最小干预和观察方法。
```

安装选定 Skills 到另一个项目（需要 Python 3.10+）：

```sh
python scripts/install.py --project /path/to/your-project --skills thinking-in-systems make-it-stick
```

Windows 示例：

```powershell
python scripts/install.py --project 'D:\MyProject' --skills thinking-in-systems make-it-stick
```

默认只预览；检查目标路径后追加 `--apply` 才复制。已存在的同名目录不会被覆盖。Claude Code 可用 `--host claude` 安装到目标项目的 `.claude/skills/`。其他支持 Agent Skills 的宿主可手动复制单个 Skill 文件夹；宿主兼容性需各自验证。

Codex 的本地加载位置和调用方式依据 [OpenAI 官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)，核对日期 2026-09-07。宿主可以自动匹配描述，但不能保证所有请求都会自动触发。

## 可信度与范围

- 方法说明由本项目独立撰写；不附电子书、完整译文、封面或受限数据库内容。
- 现代书籍主要依据可公开核实的作者材料、出版社摘录与相关研究；不会把未读全文写成“全书精读”。每本的 `book.json` 和来源说明列出具体覆盖范围。
- 原书论点、独立研究、现代应用推断、用户提供的事实分开处理。名气、销量、奖项与作者身份不能替代有效性证据。
- 自动校验检查结构、来源记录、引用路径和安装行为。独立代理案例只说明这些案例中的表现，不能证明用户学会或方法在真实项目中有效。
- 普通问题直接回答；只有用户要求练习才进入一问一答。不同书的框架不应挤占用户真正要完成的工作。

## 开发与验证

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build_catalog.py --check
```

改动书目后运行 `python scripts/build_catalog.py`。验证详情见 [评估说明](evals/README.md)，选书与来源标准见 [方法说明](docs/selection-method.md)。

与 [Book Dialogue](https://github.com/wangchuan2003-a11y/book-dialogue-skill) 配套：Book Dialogue 用你提供的文本开展读书对话；本项目提供已整理的单书方法。

## 许可

项目原创代码、说明与 Skill 指令采用 [MIT](LICENSE)。书籍、作者原文、译本及外部网站仍属于各自权利人；本许可不授予这些内容的再分发权。本项目不代表作者或出版社背书。
