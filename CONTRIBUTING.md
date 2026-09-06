# 如何加入一本书

先说明这本书解决哪一种现有 Skills 没有覆盖好的问题，再整理材料。名气不是唯一准入理由；有影响但存在重大局限的作品也可以入选，前提是局限会改变 Skill 的实际建议。

1. 阅读 [来源标准](docs/selection-method.md)，核实书名、作者与版本；为留用来源记录实际访问范围。
2. 在 `.agents/skills/<book-id>/` 创建一套完整文件，参照已有条目的结构，方法与例子必须针对这本书独立编写。
3. 分开作者的观点、支持或挑战观点的研究、你的应用设计。遇到无法取得的正文，降低覆盖声明，不用模型记忆补造页码、引语或作者立场。
4. 设计至少三个有诊断价值的案例：正常使用、适用边界、会诱发错误的情境。标准描述回答应该做什么，不规定必须出现的措辞。
5. 运行结构校验和目录生成。找未参与撰写的人或代理只看 Skill 与输入实际执行，再用保留的标准评审。记录失败、修复和未覆盖的部分。

```sh
python scripts/build_catalog.py
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build_catalog.py --check
python scripts/audit_evidence.py --require-complete
python scripts/package.py
```

保持 Skills 可单独安装。当前仓库使用简单 YAML：前置 `name`、`description` 为字符串，带标点的值使用 JSON 兼容双引号；`agents/openai.yaml` 的三项 UI 字符串也使用双引号。目录和 `book.json.id` 一致。

`sources[].kind` 可选 `primary_text`、`author_material`、`publisher`、`academic`、`independent_research`。作者团队的研究不自动算独立复制。未知年代可以在 `year` 字符串中保留争议。`limits` 不仅说明无法确认什么，也应提示实际使用时如何调整。

不提交个人书库、聊天记录、凭据、整本原文或未经许可的封面。版权已经过期的作品，其现代翻译、注释和排版也可能单独受保护。

总下载包的附加文件由 `distribution.json` 逐项选择，不递归收集研究临时文件。新增公开说明或评估证据时明确加入这个清单。ZIP固定时间戳、平台标识和权限，使用不压缩存储以消除zlib版本差异；仓库统一LF换行，CI比较Windows/Linux的全部包哈希。

优先修复已观察到的错误、补足来源和改善案例。没有行为证据时，不把更多文件、更多测试数量或更长回答作为质量升级。

发布时将逐题实际答案和非作者评审纳入`evals/results/`，并更新其`index.json`。审计脚本校验记录完整性，不能替代内容判断或证明实际运行；请记录固定来源版本、执行方式和限制。历史失败与修复后的重测分别保留。
