# Book to Action Skills

[简体中文](README.md) · English

A Chinese-first, source-aware collection of Agent Skills for applying ideas from books to concrete questions. Topics include learning, reasoning, prediction, strategy, ethics, social analysis, and literary interpretation. Most skill instructions and references are in Chinese; this page provides an English entry point.

Selection is editorial, not an objective ranking of the world's greatest books. Methods should help with the task at hand. Literary works support close reading and competing interpretations rather than automatic rules for success. See the [Chinese README](README.md) for the current catalog and [Releases](https://github.com/wangchuan2003-a11y/book-to-action-skills/releases) for published snapshots.

## Get started

Clone the repository and open it in Codex:

```sh
git clone https://github.com/wangchuan2003-a11y/book-to-action-skills.git
cd book-to-action-skills
```

Skills live in `.agents/skills/`. Start with a real question and invoke one explicitly, for example:

```text
Use $thinking-in-systems to examine our growing support backlog.
Identify missing evidence and suggest one small intervention.
```

The [book selection guide](docs/choose-a-book.md) explains which kinds of questions different skills address. Automatic matching depends on the host and request; explicit invocation makes the intended skill clear.

## Install selected skills

With Python 3.10 or later, run this from the cloned repository or an extracted complete release:

```sh
python scripts/install.py --project /path/to/existing-project --skills thinking-in-systems make-it-stick
```

On Windows, replace the project argument with a quoted path such as `'D:\MyProject'`.

The default is a dry run: it previews destinations and copies nothing. Review the paths, then append `--apply` to copy. Existing skill directories are never overwritten. Codex installations use the selected project's `.agents/skills/`; add `--host claude` to use `.claude/skills/` instead. Compatibility with other hosts requires separate verification.

Releases provide individual skill archives and a complete collection. Preserve the complete archive's directory structure to use its installer. Compare downloaded archives with the accompanying `SHA256SUMS.txt`; a matching checksum checks integrity, not the quality of the advice.

## Sources and coverage

Each skill includes instructions, book metadata, source notes, an original example, UI metadata, and behavioral test cases. Source records identify URLs, access dates, what was actually read, what it supports, and its limits.

Coverage may be partial: an excerpt, author discussion, or academic interpretation does not imply that the whole book was read. Author arguments, independent research, historical context, and this project's applications remain distinct. The collection does not claim that every method has independent scientific validation. See the [selection and source standards](docs/selection-method.md).

## What validation means

- **Structural checks** test package, metadata, links, installation, and archive properties.
- **Cross-agent cases** provide reviewed behavior on specific recorded requests.
- **Host smoke tests** check actual loading and responses in a recorded host/session. A new session may still see global configuration or memory.
- **Real use** requires further evidence of useful outcomes. These checks do not establish user mastery or general effectiveness.

Run the documented checks:

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build_catalog.py --check
```

Preparing evaluation prompts is not executing them. The preparation tool separates prompts from review criteria; actual outputs still need independent review. See the [evaluation guide](evals/README.md) and release records for scope, failures, and fixes.

## License

Original code, instructions, and documentation use the [MIT license](LICENSE). Books, translations, and external materials retain their owners' rights. A publicly accessible URL does not grant permission to redistribute its full text. This project does not imply author or publisher endorsement.
