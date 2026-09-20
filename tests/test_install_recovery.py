"""A failed batch is retryable and never removes preexisting user files."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import copy_plan

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plan = []
        for name in ('one', 'two'):
            source = self.root / 'source' / name
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text(name)
            self.plan.append((source, self.root / 'dest' / name))
        self.note = self.root / 'dest/personal.txt'
        self.note.parent.mkdir()
        self.note.write_text('keep')

    def test_second_prepare_failure_leaves_no_installed_skills_and_can_retry(self):
        original = shutil.copytree
        def fail(src, dst, **kwargs):
            if Path(src) == self.plan[1][0]:
                Path(dst).mkdir()
                (Path(dst) / 'partial').write_text('partial')
                raise OSError('disk failure')
            return original(src, dst, **kwargs)
        with patch('install.shutil.copytree', side_effect=fail), self.assertRaises(OSError):
            copy_plan(self.plan)
        self.assertEqual(['personal.txt'], sorted(p.name for p in self.note.parent.iterdir()))
        copy_plan(self.plan)
        for source, target in self.plan:
            self.assertEqual((source / 'SKILL.md').read_bytes(), (target / 'SKILL.md').read_bytes())
        self.assertEqual('keep', self.note.read_text())

    def test_commit_failure_rolls_back_partial_and_prior_targets(self):
        original = shutil.copytree
        def fail(src, dst, **kwargs):
            if Path(dst) == self.plan[1][1]:
                (Path(dst) / 'partial').write_text('partial')
                raise OSError('commit failure')
            return original(src, dst, **kwargs)
        with patch('install.shutil.copytree', side_effect=fail), self.assertRaises(OSError):
            copy_plan(self.plan)
        self.assertTrue(all(not t.exists() for _, t in self.plan))
        self.assertEqual('keep', self.note.read_text())
        copy_plan(self.plan)

    def test_new_conflict_is_preserved_and_prior_install_rolled_back(self):
        target = self.plan[1][1]
        target.mkdir()
        (target / 'user').write_text('user')
        with self.assertRaises(FileExistsError):
            copy_plan(self.plan)
        self.assertFalse(self.plan[0][1].exists())
        self.assertEqual('user', (target / 'user').read_text())

    def test_keyboard_interrupt_also_rolls_back(self):
        original = shutil.copytree
        def interrupt(src, dst, **kwargs):
            if Path(dst) == self.plan[1][1]:
                raise KeyboardInterrupt()
            return original(src, dst, **kwargs)
        with patch('install.shutil.copytree', side_effect=interrupt), self.assertRaises(KeyboardInterrupt):
            copy_plan(self.plan)
        self.assertTrue(all(not t.exists() for _, t in self.plan))
