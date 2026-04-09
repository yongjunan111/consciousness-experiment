"""Unit tests for codex_helper — JSONL parsing, error handling, smoke.

Run: cd /home/dydwn/projects/consciousness-experiment && uv run python -m unittest scripts.test_codex_helper -v
Or:  cd /home/dydwn/projects/consciousness-experiment && uv run python scripts/test_codex_helper.py
"""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

# Ensure scripts/ is importable
_SCRIPTS_DIR = str(Path(__file__).parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from codex_helper import codex_exec, parse_codex_jsonl, CodexExecError  # noqa: E402


# ---------------------------------------------------------------------------
# parse_codex_jsonl — unit tests for JSONL output parsing
# ---------------------------------------------------------------------------


class TestParseCodexJsonl(unittest.TestCase):
    def test_normal_agent_message_format(self):
        stdout = (
            '{"type":"item.completed","item":{"type":"agent_message","text":"true"}}\n'
            '{"type":"turn.completed","usage":{"input_tokens":100,"cached_input_tokens":10,"output_tokens":5}}\n'
        )
        text, usage = parse_codex_jsonl(stdout)
        self.assertEqual(text, "true")
        self.assertEqual(usage["input_tokens"], 100)
        self.assertEqual(usage["cached_input_tokens"], 10)
        self.assertEqual(usage["output_tokens"], 5)

    def test_structured_message_format(self):
        item = {
            "type": "message",
            "role": "assistant",
            "content": [{"type": "output_text", "text": "  42  "}],
        }
        stdout = json.dumps({"type": "item.completed", "item": item}) + "\n"
        text, usage = parse_codex_jsonl(stdout)
        self.assertEqual(text, "42")

    def test_empty_output(self):
        text, usage = parse_codex_jsonl("")
        self.assertEqual(text, "")
        self.assertEqual(usage["input_tokens"], 0)

    def test_malformed_json_lines_skipped(self):
        stdout = "NOT JSON\n" + '{"type":"item.completed","item":{"text":"ok"}}\n'
        text, _ = parse_codex_jsonl(stdout)
        self.assertEqual(text, "ok")

    def test_no_item_completed_event(self):
        stdout = '{"type":"turn.completed","usage":{"input_tokens":50,"output_tokens":3}}\n'
        text, usage = parse_codex_jsonl(stdout)
        self.assertEqual(text, "")
        self.assertEqual(usage["input_tokens"], 50)

    def test_whitespace_stripped_from_response(self):
        stdout = '{"type":"item.completed","item":{"text":"  hello world  "}}\n'
        text, _ = parse_codex_jsonl(stdout)
        self.assertEqual(text, "hello world")


# ---------------------------------------------------------------------------
# codex_exec — subprocess mock tests
# ---------------------------------------------------------------------------


class TestCodexExec(unittest.TestCase):
    def _mock_run(self, returncode=0, stdout="", stderr=""):
        return mock.patch(
            "codex_helper.subprocess.run",
            return_value=mock.Mock(
                returncode=returncode, stdout=stdout, stderr=stderr,
            ),
        )

    def test_success_returns_parsed_response(self):
        fake_stdout = (
            '{"type":"item.completed","item":{"text":"not_sure"}}\n'
            '{"type":"turn.completed","usage":{"input_tokens":200,"cached_input_tokens":0,"output_tokens":2}}\n'
        )
        with self._mock_run(stdout=fake_stdout) as mock_run:
            text, usage = codex_exec("test prompt", model="gpt-5.4")

        self.assertEqual(text, "not_sure")
        self.assertEqual(usage["input_tokens"], 200)

        # Verify subprocess was called with correct args
        call_args = mock_run.call_args
        cmd = call_args.args[0] if call_args.args else call_args.kwargs.get("args", [])
        self.assertIn("codex", cmd)
        self.assertIn("gpt-5.4", cmd)

    def test_nonzero_exit_raises_error(self):
        with self._mock_run(returncode=1, stderr="rate limited"):
            with self.assertRaises(CodexExecError) as ctx:
                codex_exec("prompt")
            self.assertIn("rate limited", str(ctx.exception))

    def test_timeout_propagates(self):
        import subprocess as sp
        with mock.patch(
            "codex_helper.subprocess.run",
            side_effect=sp.TimeoutExpired(cmd="codex", timeout=60),
        ):
            with self.assertRaises(sp.TimeoutExpired):
                codex_exec("prompt", timeout=60)

    def test_system_prompt_prepended(self):
        fake_stdout = '{"type":"item.completed","item":{"text":"ok"}}\n'
        with self._mock_run(stdout=fake_stdout) as mock_run:
            codex_exec("user msg", system_prompt="be helpful")

        call_kwargs = mock_run.call_args.kwargs
        sent_input = call_kwargs.get("input", "")
        self.assertIn("be helpful", sent_input)
        self.assertIn("user msg", sent_input)

    def test_reasoning_effort_flag(self):
        fake_stdout = '{"type":"item.completed","item":{"text":"ok"}}\n'
        with self._mock_run(stdout=fake_stdout) as mock_run:
            codex_exec("prompt", reasoning_effort="high")

        cmd = mock_run.call_args.args[0]
        self.assertIn("-c", cmd)
        idx = cmd.index("-c")
        self.assertEqual(cmd[idx + 1], "model_reasoning_effort=high")

    def test_empty_stdout_raises_error(self):
        """Exit 0 but empty stdout → no usable response → CodexExecError."""
        with self._mock_run(stdout=""):
            with self.assertRaises(CodexExecError) as ctx:
                codex_exec("prompt")
            self.assertIn("no usable assistant response", str(ctx.exception))

    def test_malformed_only_stdout_raises_error(self):
        """Exit 0 but only garbage lines → no assistant text → CodexExecError."""
        with self._mock_run(stdout="NOT JSON\nALSO NOT JSON\n"):
            with self.assertRaises(CodexExecError) as ctx:
                codex_exec("prompt")
            self.assertIn("no usable assistant response", str(ctx.exception))

    def test_usage_only_no_message_raises_error(self):
        """Exit 0 with turn.completed usage but no item.completed → CodexExecError."""
        stdout = '{"type":"turn.completed","usage":{"input_tokens":50,"output_tokens":0}}\n'
        with self._mock_run(stdout=stdout):
            with self.assertRaises(CodexExecError) as ctx:
                codex_exec("prompt")
            self.assertIn("no usable assistant response", str(ctx.exception))


# ---------------------------------------------------------------------------
# run_experiment smoke — verify OpenAI SDK removal
# ---------------------------------------------------------------------------


class TestRunExperimentSmoke(unittest.TestCase):
    def test_no_openai_import(self):
        """run_experiment.py must not import the openai package."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "run_experiment",
            os.path.join(os.path.dirname(__file__), "run_experiment.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        # Patch sys.argv so argparse doesn't fire on import
        old_argv = sys.argv
        sys.argv = ["run_experiment.py"]
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.argv = old_argv

        self.assertFalse(hasattr(mod, "openai"), "openai should not be imported")
        self.assertTrue(hasattr(mod, "codex_exec"), "codex_exec should be available")
        self.assertTrue(callable(getattr(mod, "call_judge", None)))
        self.assertTrue(callable(getattr(mod, "call_coherence_judge", None)))
        self.assertTrue(callable(getattr(mod, "call_subject_codex", None)))
        self.assertTrue(callable(getattr(mod, "call_subject_claude", None)))
        # call_subject_openai and call_judge_openai must be gone
        self.assertFalse(hasattr(mod, "call_subject_openai"))
        self.assertFalse(hasattr(mod, "call_judge_openai"))
        self.assertFalse(hasattr(mod, "call_coherence_judge_openai"))


if __name__ == "__main__":
    unittest.main()
