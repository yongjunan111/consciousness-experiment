"""Shared helper for running OpenAI models via Codex CLI (codex exec --json).

This module provides a single entry point `codex_exec()` that:
- Builds the codex exec subprocess command
- Handles system prompt injection (prepended to user prompt)
- Parses the JSONL streaming output
- Returns (response_text, token_usage) on success
- Raises CodexExecError on non-zero exit or unparseable output
- Lets subprocess.TimeoutExpired propagate for caller handling

No OpenAI SDK dependency. No API key required.
"""

import json
import subprocess
from pathlib import Path


class CodexExecError(Exception):
    """Raised when codex exec fails or returns unparseable output."""
    pass


def codex_exec(
    prompt: str,
    *,
    model: str = "gpt-5.4",
    system_prompt: str | None = None,
    timeout: int = 120,
    cwd: str | Path | None = None,
    reasoning_effort: str | None = None,
) -> tuple[str, dict]:
    """Run `codex exec --json` and return (response_text, token_usage).

    Parameters
    ----------
    prompt : str
        The user prompt / task description.
    model : str
        Model name passed to `--model` (e.g. "gpt-5.4", "gpt-4.1").
    system_prompt : str | None
        Optional system instructions. Prepended to the prompt with a clear
        separator since codex exec has no native --system-prompt flag.
    timeout : int
        Subprocess timeout in seconds.
    cwd : str | Path | None
        Working directory for the codex process.
    reasoning_effort : str | None
        Optional reasoning effort level (e.g. "high"). Passed via
        `-c model_reasoning_effort=<value>`.

    Returns
    -------
    (response_text, token_usage)
        response_text: assistant's text reply.
        token_usage: dict with input_tokens, cached_input_tokens, output_tokens.

    Raises
    ------
    CodexExecError
        On non-zero exit code or when no response text could be parsed.
    subprocess.TimeoutExpired
        Propagated directly for the caller to handle.
    """
    full_prompt = prompt
    if system_prompt:
        full_prompt = (
            f"[System instructions — follow these for the entire response]\n"
            f"{system_prompt}\n\n"
            f"---\n\n"
            f"[User message]\n"
            f"{prompt}"
        )

    cmd = [
        "codex", "exec",
        "--model", model,
        "--json",
        "--ephemeral",
        "-s", "read-only",
    ]
    if reasoning_effort:
        cmd.extend(["-c", f"model_reasoning_effort={reasoning_effort}"])
    cmd.append("-")  # read prompt from stdin

    cwd_str = str(cwd) if cwd else None

    # subprocess.TimeoutExpired is NOT caught — caller decides how to handle it
    result = subprocess.run(
        cmd,
        input=full_prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd_str,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else "(no stderr)"
        raise CodexExecError(
            f"codex exec exited with code {result.returncode}: {stderr}"
        )

    response_text, token_usage = parse_codex_jsonl(result.stdout)

    # A successful codex exec that produces no usable assistant text is a parse
    # failure, not an empty-but-valid response. Without this check, execution
    # failures silently blend into experiment results as blank answers.
    if not response_text:
        raise CodexExecError(
            "codex exec returned exit 0 but no usable assistant response was parsed"
        )

    return response_text, token_usage


def parse_codex_jsonl(stdout: str) -> tuple[str, dict]:
    """Parse JSONL output from `codex exec --json`.

    Returns (response_text, token_usage). If no parseable assistant response
    is found, returns ("", default_usage) — an empty response is not an error
    because the model may legitimately produce empty output.

    This function is also used directly in tests for unit-level validation
    of the JSONL parsing logic.
    """
    response_text = ""
    token_usage = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
    }

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type", "")

        if event_type == "item.completed":
            item = event.get("item", {})
            # Primary format: {"type":"agent_message","text":"..."}
            if "text" in item:
                response_text = item["text"].strip()
            # Fallback: structured message format
            elif item.get("type") == "message" and item.get("role") == "assistant":
                for content_block in item.get("content", []):
                    if content_block.get("type") == "output_text":
                        response_text = content_block.get("text", "").strip()

        elif event_type == "turn.completed":
            usage = event.get("usage", {})
            token_usage["input_tokens"] = usage.get("input_tokens", 0)
            token_usage["cached_input_tokens"] = usage.get("cached_input_tokens", 0)
            token_usage["output_tokens"] = usage.get("output_tokens", 0)

    return response_text, token_usage
