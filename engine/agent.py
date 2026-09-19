#!/usr/bin/env python3
"""Provider-neutral LLM dispatch for the deterministic hunt engine.

Claude Code and OpenAI Codex are supported. Agents end with a fenced JSON block,
which the engine parses into structured data.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import time

ENGINE = os.path.dirname(os.path.abspath(__file__))
MCP_CONFIG = os.path.join(ENGINE, "burp-mcp.json")
ALLOWED_TOOLS = " ".join([
    "mcp__burp__send_http1_request", "mcp__burp__send_http2_request",
    "mcp__burp__get_collaborator_interactions", "mcp__burp__generate_collaborator_payload",
    "Bash(curl:*)", "Bash(python3:*)", "Bash(jq:*)", "Bash(openssl:*)", "Bash(base64:*)",
])


def _find_cli(provider):
    candidates = ("codex.cmd", "codex") if provider == "codex" else ("claude.cmd", "claude")
    return next((shutil.which(name) for name in candidates if shutil.which(name)), None)


def resolve_provider(provider="auto", model=None):
    """Resolve an explicit provider or preserve the historical Claude-first default."""
    provider = (os.environ.get("CBH_AGENT_PROVIDER") or provider or "auto").lower()
    if provider not in {"auto", "claude", "codex"}:
        raise ValueError(f"unsupported provider: {provider}")
    if provider != "auto":
        return provider
    if model:
        lowered = model.lower()
        if lowered.startswith("claude"):
            return "claude"
        if lowered.startswith(("gpt-", "o1", "o3", "o4", "codex")):
            return "codex"
    if _find_cli("claude"):
        return "claude"
    if _find_cli("codex"):
        return "codex"
    return "claude"


def _run_claude(task, skills_on, model, max_turns, timeout, cwd):
    exe = _find_cli("claude")
    if not exe:
        return {"result": "", "error": "exec:Claude Code CLI not found"}
    cmd = [exe, "-p", task]
    if os.path.isfile(MCP_CONFIG):
        cmd += ["--mcp-config", MCP_CONFIG, "--strict-mcp-config"]
    cmd += ["--permission-mode", "bypassPermissions", "--allowedTools", ALLOWED_TOOLS,
            "--max-turns", str(max_turns), "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    if not skills_on:
        cmd.append("--disable-slash-commands")
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    try:
        data = json.loads(p.stdout)
    except Exception as exc:
        return {"result": p.stdout[:300], "error": f"parse:{exc}"}
    result = data.get("result") or ""
    if "usage limit" in result.lower() or "session limit" in result.lower():
        return {"result": result, "error": "rate-limited"}
    if p.returncode and not result:
        return {"result": "", "error": f"exit:{p.returncode}:{p.stderr[:200]}"}
    return {"result": result, "cost_usd": data.get("total_cost_usd"),
            "num_turns": data.get("num_turns"), "error": None}


def _run_codex(task, model, timeout, cwd):
    exe = _find_cli("codex")
    if not exe:
        return {"result": "", "error": "exec:Codex CLI not found"}
    fd, output_path = tempfile.mkstemp(prefix="cbh-codex-", suffix=".txt")
    os.close(fd)
    try:
        cmd = [exe, "exec", "--ephemeral", "--skip-git-repo-check",
               "--approve-for-me", "--sandbox", "workspace-write",
               "--config", "sandbox_workspace_write.network_access=true",
               "--cd", cwd, "--output-last-message", output_path]
        if model:
            cmd += ["--model", model]
        cmd.append("-")
        p = subprocess.run(cmd, input=task, capture_output=True, text=True,
                           timeout=timeout, cwd=cwd)
        try:
            with open(output_path, encoding="utf-8") as handle:
                result = handle.read()
        except OSError:
            result = ""
        combined = "\n".join((result, p.stdout, p.stderr)).lower()
        if "usage limit" in combined or "rate limit" in combined:
            return {"result": result, "error": "rate-limited"}
        if p.returncode:
            detail = (p.stderr or p.stdout or "Codex execution failed")[:300]
            return {"result": result, "error": f"exit:{p.returncode}:{detail}"}
        if not result.strip():
            return {"result": "", "error": "parse:Codex produced no final message"}
        return {"result": result, "cost_usd": None, "num_turns": None, "error": None}
    finally:
        try:
            os.remove(output_path)
        except OSError:
            pass


def run_agent(task, skills_on=False, model=None, max_turns=40, timeout=600,
              provider="auto", cwd=None):
    """Run one agent and return a provider-independent result dictionary."""
    t0 = time.time()
    cwd = os.path.abspath(os.path.expanduser(cwd or os.getcwd()))
    try:
        selected = resolve_provider(provider, model)
        if selected == "codex":
            result = _run_codex(task, model, timeout, cwd)
        else:
            result = _run_claude(task, skills_on, model, max_turns, timeout, cwd)
    except subprocess.TimeoutExpired:
        result = {"result": "", "error": "timeout"}
    except (FileNotFoundError, OSError, ValueError) as exc:
        result = {"result": "", "error": f"exec:{exc}"}
    result["provider"] = locals().get("selected", provider)
    result["duration_s"] = round(time.time() - t0, 1)
    return result


def extract_json(text):
    """Pull the last valid JSON array/object out of an agent reply."""
    if not text:
        return None
    blocks = re.findall(r"```json\s*(.*?)```", text, re.S)
    blocks += re.findall(r"```\s*(\[.*?\]|\{.*?\})\s*```", text, re.S)
    for b in reversed(blocks):
        try:
            return json.loads(b.strip())
        except Exception:
            pass
    for b in reversed(re.findall(r"(\[.*\]|\{.*\})", text, re.S)):
        try:
            return json.loads(b)
        except Exception:
            pass
    return None


if __name__ == "__main__":
    # offline self-test of the JSON extractor (no agent call)
    assert extract_json('blah ```json\n[{"a":1}]\n``` end') == [{"a": 1}]
    assert extract_json('text {"x": "y"} more') == {"x": "y"}
    assert extract_json("no json here") is None
    assert extract_json('first {"a":1} then ```json\n{"b":2}\n```') == {"b": 2}  # prefers fenced/last
    print("agent.py extractor self-test: PASS")
