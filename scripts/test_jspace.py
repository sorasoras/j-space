"""Controller regressions; all mutable fixtures live in temporary directories."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).with_name('jspace.py')
spec = importlib.util.spec_from_file_location('controller_under_test', SCRIPT)
j = importlib.util.module_from_spec(spec)
spec.loader.exec_module(j)


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.previous = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, self.previous)
        j.select_task('alpha')

    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(SCRIPT), *args],
                                cwd=self.root, capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def note(self, *args, expected=0):
        return self.cli('note', '--task', 'alpha', *args, expected=expected)

    def init(self):
        self.note('--goal', 'Fix controller', '--next', 'Test it', '--core', 'state - durable')

    def snapshot(self):
        return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob('*') if p.is_file()}

    def test_goal_survives_noop_core_swap(self):
        self.init()
        self.note('--goal', 'New goal', '--core', 'state - durable', '--core-slot', '1')
        self.assertEqual(j.read_ledger()['Goal'], ['New goal'])

    def test_valid_mixed_update(self):
        self.init()
        self.note('--goal', 'Complete fix', '--open', 'Race?', '--settled-by', 'Concurrent test',
                  '--check', 'Parser holds', '--scope', 'Unicode scalar inputs', '--evidence', 'unit test',
                  '--next', 'Run integration')
        book = j.read_ledger()
        self.assertEqual(book['Next'], ['Run integration'])
        self.assertIn('scope: Unicode scalar inputs; evidence: unit test', book['Verified'][0])
        self.assertEqual(len(book['Open']), 1)

    def test_bad_input_is_transactional(self):
        self.init()
        for args in [('--goal', 'Changed', '--check', 'unsupported'),
                     ('--next', 'Changed', '--close', '99'),
                     ('--core-slot', '2'), ('--scope', 'only'), ('--goal', '## Open')]:
            before = self.snapshot()
            self.note(*args, expected=2)
            self.assertEqual(before, self.snapshot())

    def test_unicode_separators_rejected(self):
        self.init()
        for separator in '\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029':
            before = self.snapshot()
            self.note('--next', 'first' + separator + 'second', expected=2)
            self.assertEqual(before, self.snapshot())

    def test_schema_loss_is_rejected(self):
        self.init()
        path = Path(j.LEDGER)
        original = path.read_text(encoding='utf-8')
        for content in [original + '\n## Extra\nkeep me\n',
                        original.replace('Fix controller', 'Fix controller\nSecond goal'),
                        original + '\n## Core\n- extra\n',
                        original.replace('state - durable', 'state\u2028lost'),
                        original.replace('next-question=1', 'next-question=0')]:
            path.write_text(content, encoding='utf-8')
            before = self.snapshot()
            self.note('--next', 'Changed', expected=2)
            self.assertEqual(before, self.snapshot())

    def test_question_ids_survive_closure_and_restart(self):
        self.init()
        for number in range(1, 4):
            self.note('--open', 'Question', '--settled-by', 'Test')
            self.assertTrue(j.read_ledger()['Open'][0].startswith('?%02d ' % number))
            self.note('--close', str(number), '--verified', 'Resolved', '--by', 'Manual observation')
        self.assertEqual(j.read_ledger()['_next_question'], 4)

    def test_task_isolation_and_legacy_reads(self):
        self.init()
        legacy = self.root / '.jspace' / 'WORKSPACE.md'
        text = Path(j.LEDGER).read_text(encoding='utf-8')
        legacy.write_text('\n'.join(line for line in text.split('\n') if not line.startswith('<!--')), encoding='utf-8')
        before = legacy.read_bytes()
        self.cli('note', '--goal', 'no task', '--next', 'x', expected=2)
        self.cli('note', '--task', '../escape', '--goal', 'x', '--next', 'y', expected=2)
        self.cli('note', '--task', 'beta', '--next', 'cannot inherit', expected=2)
        self.cli('--task', 'beta', 'note', '--goal', 'Other task', '--next', 'Independent')
        self.assertEqual(j.read_ledger()['Goal'], ['Fix controller'])
        self.assertIn('Other task', self.cli('status', '--task', 'BETA'))
        self.assertIn('Fix controller', self.cli('status'))
        self.assertEqual(legacy.read_bytes(), before)

    def test_reads_create_nothing_and_do_not_write(self):
        for cmd in ('status', 'seam', 'resume'):
            self.cli(cmd, '--task', 'missing')
            self.cli(cmd)
        self.assertEqual(self.snapshot(), {})
        self.init()
        Path(j.LEDGER).with_name('history.json').write_text('obsolete invalid history', encoding='utf-8')
        before = self.snapshot()
        for cmd in ('status', 'seam', 'resume'):
            output = self.cli(cmd, '--task', 'alpha')
            self.assertTrue(output.startswith('Goal:'))
            for phrase in ('premise', 'invariants', 'sweep', 'confidence', 'history', 'stall', 'Not working if:'):
                self.assertNotIn(phrase, output)
        self.assertEqual(self.cli('resume', '--task', 'alpha'), self.cli('status', '--task', 'alpha'))
        self.assertEqual(before, self.snapshot())
        with mock.patch.object(j, 'atomic_write_text', side_effect=AssertionError('write')), \
             mock.patch.object(j, 'ensure_dir', side_effect=AssertionError('mkdir')), \
             contextlib.redirect_stdout(io.StringIO()):
            for cmd in ('status', 'seam', 'resume'):
                self.assertEqual(j.main([cmd, '--task', 'alpha']), 0)

    def test_roundtrip_preserves_state(self):
        self.init()
        self.note('--open', 'Unicode café?', '--settled-by', 'Observe', '--check', 'Works', '--by', 'manual')
        before = j.read_ledger()
        self.assertIsNone(j.write_ledger(before))
        self.assertEqual(before, j.read_ledger())

    def test_concurrent_process_writes(self):
        self.init()
        processes = [subprocess.Popen([sys.executable, '-X', 'utf8', '-B', str(SCRIPT), 'note',
                     '--task', 'alpha', '--open', 'Question %d' % i, '--settled-by', 'Test'],
                     cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in range(16)]
        try:
            for process in processes:
                stdout, stderr = process.communicate(timeout=40)
                self.assertEqual(process.returncode, 0, (stdout, stderr))
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                    process.wait()
        book = j.read_ledger()
        self.assertEqual(len(book['Open']), 16)
        self.assertEqual({row.split()[0] for row in book['Open']}, {'?%02d' % i for i in range(1, 17)})
        self.assertEqual(book['_next_question'], 17)

    def test_ship_is_advisory_without_math_code_false_positives(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(j.mode_ship('A ⊆ B ⇒ C ∴ D\nconst value = x ?? y;\n```\nGRRR\n```'), 0)
        self.assertNotIn('WARNING:', output.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(j.mode_ship('GRRR'), 0)
        self.assertIn('WARNING:', output.getvalue())


if __name__ == '__main__':
    unittest.main()
