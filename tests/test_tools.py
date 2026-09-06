"""Behavioral tests for publication tooling; these do not judge book advice."""

from __future__ import annotations

from datetime import date, datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_catalog import render
from audit_evidence import audit
from install import copy_plan, plan_install
from package import package
from prepare_eval import prepare
from validate import latest_civil_date, safe_url, validate_collection, validate_skill


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def fixture(root: Path, sid: str = "sample-book") -> Path:
    folder = root / ".agents/skills" / sid
    write(folder / "SKILL.md", f'---\nname: {sid}\ndescription: "Review a sample decision."\n---\n'
          '# Sample\nRead [sources](references/source-notes.md) and '
          '[example](references/worked-example.md).\n')
    write(folder / "agents/openai.yaml", 'interface:\n  display_name: "Sample book"\n'
          '  short_description: "Practice one well grounded decision"\n'
          f'  default_prompt: "Use ${sid} to review this decision."\n')
    book = {
        "id": sid, "title": "Sample", "title_zh": "示例", "authors": ["A"],
        "year": "2000", "domains": ["reasoning"], "use_cases": ["Review a claim"],
        "summary": "Test fixture only", "selection_rationale": "Test packaging",
        "limits": ["Not a real book"], "sources": [{
            "id": "S1", "title": "Example source", "url": "https://example.org/book",
            "kind": "publisher", "accessed": date.today().isoformat(),
            "coverage": "Fixture", "used_for": "Test metadata", "limitations": "No factual claim",
        }],
    }
    write(folder / "book.json", json.dumps(book, ensure_ascii=False))
    write(folder / "references/source-notes.md", '# Sources\nS1: test fixture only.\n')
    write(folder / "references/worked-example.md", '# Example\nA test, not an actual book summary.\n')
    cases = [{"id": str(i), "prompt": "Review a claim", "must_include": ["Evidence gap"],
              "must_avoid": ["Invented data"]} for i in range(3)]
    write(folder / "evals/cases.json", json.dumps(cases))
    return folder


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.collection = self.root / "collection"
        self.skill = fixture(self.collection)
        self.project = self.root / "project"
        self.project.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def mutate_book(self, mutation):
        path = self.skill / "book.json"
        book = json.loads(path.read_text(encoding="utf-8"))
        mutation(book)
        write(path, json.dumps(book))

    def test_valid_package(self):
        self.assertEqual(([], 1), validate_collection(self.collection))

    def evidence_fixture(self):
        cases = json.loads((self.skill / "evals/cases.json").read_text(encoding="utf-8"))
        records = [{"skill": "sample-book", "case_id": c["id"], "prompt": c["prompt"],
                    "answer": "Observed answer", "review": {"verdict": "pass", "reason": "Reviewed"}}
                   for c in cases]
        base = self.collection / "evals/results"
        write(base / "index.json", json.dumps({"initial_runs": ["initial.json"], "retest_runs": []}))
        write(base / "initial.json", json.dumps({"cases": records}))
        return base, records

    def test_evidence_requires_matching_prompts(self):
        base, records = self.evidence_fixture()
        self.assertEqual([], audit(self.collection)["errors"])
        records[0]["prompt"] = "Different test"
        write(base / "initial.json", json.dumps({"cases": records}))
        self.assertTrue(audit(self.collection)["errors"])

    def test_evidence_retest_preserves_initial_failure(self):
        base, records = self.evidence_fixture()
        records[0]["review"]["verdict"] = "fail"
        write(base / "initial.json", json.dumps({"cases": records}))
        self.assertEqual(["sample-book:0"], audit(self.collection)["latest_not_pass"])
        corrected = {**records[0], "review": {"verdict": "pass", "reason": "Retested"}}
        write(base / "retest.json", json.dumps({"cases": [corrected]}))
        write(base / "index.json", json.dumps({"initial_runs": ["initial.json"],
                                               "retest_runs": ["retest.json"]}))
        result = audit(self.collection)
        self.assertEqual(1, result["initial_verdicts"]["fail"])
        self.assertEqual([], result["latest_not_pass"])
        self.assertEqual([], result["errors"])

    def test_evidence_reports_missing_cases(self):
        base, records = self.evidence_fixture()
        write(base / "initial.json", json.dumps({"cases": records[:1]}))
        self.assertEqual(["sample-book:1", "sample-book:2"], audit(self.collection)["missing_cases"])

    def test_evidence_rejects_duplicate_authored_ids(self):
        base, records = self.evidence_fixture()
        path = self.skill / "evals/cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        cases.append({**cases[0], "prompt": "Shadowed first question"})
        write(path, json.dumps(cases))
        records[0]["prompt"] = "Shadowed first question"
        write(base / "initial.json", json.dumps({"cases": records}))
        self.assertTrue(audit(self.collection)["errors"])

    def test_access_dates_allow_the_researchers_local_date(self):
        instant = datetime(2026, 9, 6, 16, 10, tzinfo=timezone.utc)
        self.assertEqual(date(2026, 9, 7), latest_civil_date(instant))
        early = datetime(2026, 9, 6, 9, 0, tzinfo=timezone.utc)
        self.assertEqual(date(2026, 9, 6), latest_civil_date(early))

    def test_eval_prompts_do_not_contain_the_rubric(self):
        output = self.collection / ".local/eval-test"
        result = prepare(self.collection, ["sample-book"], output)
        self.assertEqual(3, result["case_count"])
        for file in (output / "prompts").glob("*.md"):
            text = file.read_text(encoding="utf-8")
            self.assertIn("Review a claim", text)
            self.assertNotIn("Invented data", text)
            self.assertNotIn("must_include", text)
        rubrics = json.loads((output / "reviewer-rubrics.json").read_text(encoding="utf-8"))
        self.assertEqual(["Invented data"], rubrics[0]["must_avoid"])
        with self.assertRaises(ValueError):
            prepare(self.collection, ["sample-book"], output)

    def test_eval_preflight_does_not_write_for_invalid_selection(self):
        output = self.collection / ".local/invalid-eval"
        with self.assertRaises(ValueError):
            prepare(self.collection, ["sample-book", "missing"], output)
        self.assertFalse(output.exists())
        with self.assertRaises(ValueError):
            prepare(self.collection, ["sample-book"], self.root / "outside")

    def test_eval_outputs_cannot_pollute_the_skill_collection(self):
        output = self.collection / ".agents/skills/eval-output"
        with self.assertRaises(ValueError):
            prepare(self.collection, ["sample-book"], output)
        self.assertFalse(output.exists())

    def test_empty_collection_rejected(self):
        self.assertTrue(validate_collection(self.project)[0])

    def test_missing_source_field_rejected(self):
        self.mutate_book(lambda b: b["sources"][0].pop("coverage"))
        self.assertTrue(validate_skill(self.skill))

    def test_duplicate_source_id_rejected(self):
        self.mutate_book(lambda b: b["sources"].append(b["sources"][0].copy()))
        self.assertTrue(validate_skill(self.skill))

    def test_book_identity_mismatch_rejected(self):
        self.mutate_book(lambda b: b.update(id="wrong-book"))
        self.assertTrue(validate_skill(self.skill))

    def test_unsafe_urls_rejected(self):
        for url in ("file:///tmp/book", "https://user:secret@example.org/x", "https:///bad", "javascript:alert(1)"):
            with self.subTest(url=url):
                self.assertFalse(safe_url(url))
        self.assertTrue(safe_url("https://example.org/chapter?q=1#section"))

    def test_reference_escape_rejected_even_if_target_exists(self):
        write(self.skill.parent / "outside.md", "Outside the portable package")
        with (self.skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[Escape](../outside.md)\n")
        self.assertTrue(validate_skill(self.skill))

    def test_invalid_json_fails_without_crashing(self):
        write(self.skill / "book.json", "{")
        self.assertTrue(validate_skill(self.skill))

    def test_invalid_metadata_types_fail_without_crashing(self):
        self.mutate_book(lambda b: b.update(sources=["bad"]))
        self.assertTrue(validate_skill(self.skill))

    def test_install_preview_has_no_side_effect(self):
        before = list(self.project.rglob("*"))
        plan = plan_install(self.collection, self.project, ["sample-book"], "codex")
        self.assertEqual(before, list(self.project.rglob("*")))
        # Windows runners may supply an 8.3 TEMP path; the installer returns its canonical form.
        self.assertEqual(plan[0][1], (self.project / ".agents/skills/sample-book").resolve())

    def test_copy_matches_every_source_byte(self):
        plan = plan_install(self.collection, self.project, ["sample-book"], "claude")
        copy_plan(plan)
        target = self.project / ".claude/skills/sample-book"
        for source in self.skill.rglob("*"):
            if source.is_file():
                self.assertEqual(source.read_bytes(), (target / source.relative_to(self.skill)).read_bytes())
        self.assertEqual([], validate_skill(target))

    def test_existing_install_is_never_overwritten(self):
        target = self.project / ".agents/skills/sample-book"
        write(target / "user-note.md", "Keep this")
        with self.assertRaises(ValueError):
            plan_install(self.collection, self.project, ["sample-book"], "codex")
        self.assertEqual("Keep this", (target / "user-note.md").read_text())

    def test_all_targets_are_checked_before_copying(self):
        fixture(self.collection, "second-book")
        (self.project / ".agents/skills/second-book").mkdir(parents=True)
        with self.assertRaises(ValueError):
            plan_install(self.collection, self.project, ["sample-book", "second-book"], "codex")
        self.assertFalse((self.project / ".agents/skills/sample-book").exists())

    def test_skill_name_cannot_traverse(self):
        for name in ("../sample-book", "../../outside", "/tmp/book"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                plan_install(self.collection, self.project, [name], "codex")

    def test_duplicate_names_rejected(self):
        with self.assertRaises(ValueError):
            plan_install(self.collection, self.project, ["sample-book", "sample-book"], "codex")

    def test_symlinked_destination_escape_rejected(self):
        external = self.root / "external"
        external.mkdir()
        try:
            (self.project / ".agents").symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest("OS account cannot create symlinks")
        with self.assertRaises(ValueError):
            plan_install(self.collection, self.project, ["sample-book"], "codex")
        self.assertEqual([], list(external.iterdir()))

    def test_catalog_is_deterministic_and_preserves_readme(self):
        write(self.collection / "README.md", "Intro\n<!-- catalog:start -->\nold\n<!-- catalog:end -->\nFooter\n")
        first = render(self.collection)
        write(self.collection / "README.md", first[1])
        self.assertEqual(first, render(self.collection))
        self.assertTrue(first[1].startswith("Intro\n"))
        self.assertTrue(first[1].endswith("Footer\n"))
        self.assertEqual("sample-book", json.loads(first[0])["books"][0]["id"])

    def test_ebook_is_not_a_distributable_skill_asset(self):
        write(self.skill / "full-book.epub", "Do not distribute")
        self.assertTrue(validate_skill(self.skill))

    def test_complete_archive_can_be_repacked(self):
        write(self.collection / "README.md", "<!-- catalog:start -->\n<!-- catalog:end -->\n")
        write(self.collection / "LICENSE", "Fixture license")
        write(self.collection / "distribution.json", json.dumps({
            "files": ["README.md", "LICENSE", "catalog.json"]}))
        catalog, readme = render(self.collection)
        write(self.collection / "catalog.json", catalog)
        write(self.collection / "README.md", readme)
        original = {p.name: p.read_bytes() for p in package(self.collection)}
        extracted = self.root / "extracted"
        with zipfile.ZipFile(self.collection / "dist/book-to-action-skills.zip") as bundle:
            self.assertTrue(all((extracted / n).resolve().is_relative_to(extracted.resolve())
                                for n in bundle.namelist()))
            bundle.extractall(extracted)
        rebuilt = {p.name: p.read_bytes() for p in package(extracted)}
        self.assertEqual(original, rebuilt)

    def test_archive_reproducibility_and_private_file_exclusion(self):
        write(self.collection / "README.md", "<!-- catalog:start -->\n<!-- catalog:end -->\n")
        write(self.collection / "LICENSE", "Fixture license")
        write(self.collection / ".local/private.txt", "PRIVATE")
        write(self.collection / "book.epub", "PRIVATE BOOK")
        write(self.collection / "docs/book.epub", "PRIVATE BOOK")
        write(self.collection / "evals/.env", "PRIVATE SETTINGS")
        write(self.collection / "docs/private-notes.md", "PRIVATE NOTES")
        write(self.collection / "distribution.json", json.dumps({
            "files": ["README.md", "LICENSE", "catalog.json"]}))
        catalog, readme = render(self.collection)
        write(self.collection / "catalog.json", catalog)
        write(self.collection / "README.md", readme)
        first = {p.name: p.read_bytes() for p in package(self.collection)}
        second = {p.name: p.read_bytes() for p in package(self.collection)}
        self.assertEqual(first, second)
        with zipfile.ZipFile(self.collection / "dist/book-to-action-skills.zip") as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertNotIn("book.epub", bundle.namelist())
            self.assertNotIn(".local/private.txt", bundle.namelist())
            self.assertNotIn("docs/book.epub", bundle.namelist())
            self.assertNotIn("evals/.env", bundle.namelist())
            self.assertNotIn("docs/private-notes.md", bundle.namelist())
            self.assertIn(".agents/skills/sample-book/SKILL.md", bundle.namelist())
            self.assertEqual(len(bundle.namelist()), len(set(bundle.namelist())))
        with patch("sys.platform", "win32"):
            windows = {p.name: p.read_bytes() for p in package(self.collection)}
        with patch("sys.platform", "linux"):
            linux = {p.name: p.read_bytes() for p in package(self.collection)}
        self.assertEqual(windows, linux)


if __name__ == "__main__":
    unittest.main()
