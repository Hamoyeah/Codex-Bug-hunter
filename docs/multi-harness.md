---
title: Multi-harness install
nav_order: 3
description: Run the Claude-BugHunter skills on OpenCode, Codex, Hermes Agent, and Google AntiGravity — not just Claude Code.
---

# Multi-harness install

The 84 skills are plain **Agent Skills** (`SKILL.md` = `name` + `description` frontmatter + Markdown). This page shows how to install them on **OpenCode**, **OpenAI Codex CLI**, **Hermes Agent**, and **Google AntiGravity**.

> **Codex workflow parity.** Claude's 15 slash commands remain available in Claude Code. Codex loads the `bughunter` router skill and exposes the same modes as `$bughunter hunt`, `$bughunter recon`, `$bughunter triage`, and so on. The deterministic engine also supports `--provider codex`. **Burp MCP** is optional and portable.

## Compatibility matrix (verified mid-2026)

| Harness | Reads `SKILL.md`? | Skill path it loads | MCP (Burp) | Slash commands |
|---|---|---|---|---|
| **Claude Code** (baseline) | ✅ native | `~/.claude/skills/` | ✅ | ✅ (`/hunt`, …) |
| **OpenCode** | ✅ native | reads `~/.claude/skills/` **and** `~/.agents/skills/` | ✅ `opencode.json` | ✅ own format |
| **Codex CLI** | ✅ native | `~/.agents/skills/` (does *not* read `~/.claude/`) | ✅ `~/.codex/config.toml` | ✅ `bughunter` router |
| **Hermes Agent** | ✅ (agentskills.io) | `~/.hermes/skills/` | ✅ | ✅ own format |
| **Google AntiGravity** | ✅ native | `~/.gemini/config/skills/` | ✅ `~/.gemini/config/mcp_config.json` | ✅ own format |

**Key:** `~/.agents/skills/` is the shared path read by **Codex + OpenCode**. So copies cover everything: `~/.claude/skills/` (Claude) + `~/.agents/skills/` (Codex + OpenCode), plus `~/.hermes/skills/` for Hermes, and `~/.gemini/config/skills/` for Google AntiGravity. Required frontmatter is identical across all harnesses (`name` lowercase-hyphen ≤64, `description` ≤1024) — our `scripts/lint_skills.py` enforces it, so **no per-skill conversion is needed**.

## Install

One command installs the skills to every harness's path (copy install; existing skills are backed up outside the loading path):

```bash
# macOS / Linux
git clone https://github.com/Hamoyeah/Codex-Bug-hunter.git
cd Codex-Bug-hunter
bash scripts/install.sh --all          # Claude + ~/.agents/skills (Codex/OpenCode) + ~/.hermes/skills + ~/.gemini/config/skills
bash scripts/install.sh --codex-only   # Codex only; leaves Claude and shell startup files untouched
```

```powershell
# Windows (PowerShell)
git clone https://github.com/Hamoyeah/Codex-Bug-hunter.git
cd Codex-Bug-hunter
pwsh ./scripts/install.ps1 -All         # Claude + ~/.agents/skills (Codex/OpenCode) + ~/.hermes/skills + ~/.gemini/config/skills
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexOnly
```

Pick specific harnesses instead:

```bash
# macOS / Linux
bash scripts/install.sh                 # Claude Code only (default)
bash scripts/install.sh --codex-only    # Codex only (~/.agents/skills)
bash scripts/install.sh --agents        # Claude + Codex & OpenCode
bash scripts/install.sh --hermes        # + Hermes Agent (~/.hermes/skills)
bash scripts/install.sh --antigravity   # + Google AntiGravity (~/.gemini/config/skills)
```

```powershell
# Windows (PowerShell)
pwsh ./scripts/install.ps1              # Claude Code only (default)
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexOnly
pwsh ./scripts/install.ps1 -Agents      # Claude + Codex & OpenCode
pwsh ./scripts/install.ps1 -Hermes      # + Hermes Agent (~/.hermes/skills)
pwsh ./scripts/install.ps1 -AntiGravity # + Google AntiGravity (~/.gemini/config/skills)
```

- **OpenCode** already reads `~/.claude/skills/`, so the plain installer (no flags) is enough for OpenCode — you don't need `--agents`/`-Agents` for it. That flag exists mainly for **Codex** (which reads only `~/.agents/skills/`).
  - *Caveat:* OpenCode reads **both** `~/.claude/skills/` and `~/.agents/skills/`. If both are populated, it may log harmless duplicate-skill warnings and load one copy.
- **Codex enforces Agent Skills metadata limits.** Source descriptions are kept within 1024 characters, and the installers validate/truncate the Codex copy as a final safeguard. `--normalize-frontmatter` (`-NormalizeFrontmatter`) can also strip legacy metadata keys.

## Burp MCP on other harnesses

Your Burp MCP is a stdio command, so it translates 1:1. `--burp-mcp` (`-BurpMcp`, with a harness flag) wires it automatically by translating your **existing** Claude Code Burp definition (from `~/.claude.json`) — it backs up each config first:

```bash
# macOS / Linux
bash scripts/install.sh --all --burp-mcp     # writes OpenCode, Codex, and AntiGravity MCP config; prints Hermes guidance
```

```powershell
# Windows (PowerShell)
pwsh ./scripts/install.ps1 -All -BurpMcp      # writes OpenCode, Codex, and AntiGravity MCP config; prints Hermes guidance
```

Or do it manually (replace the jar path / port with yours):

**OpenCode** — `~/.config/opencode/opencode.json`
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "burp": {
      "type": "local",
      "command": ["java", "-jar", "~/.BurpSuite/mcp-proxy/mcp-proxy-all.jar", "--sse-url", "http://127.0.0.1:9876"],
      "enabled": true
    }
  }
}
```

**Codex** — `~/.codex/config.toml`
```bash
codex mcp add burp -- java -jar ~/.BurpSuite/mcp-proxy/mcp-proxy-all.jar --sse-url http://127.0.0.1:9876
codex mcp list
```

Equivalent configuration:
```toml
[mcp_servers.burp]
command = "java"
args = ["-jar", "~/.BurpSuite/mcp-proxy/mcp-proxy-all.jar", "--sse-url", "http://127.0.0.1:9876"]
```

**Google AntiGravity** — `~/.gemini/config/mcp_config.json`
```json
{
  "mcpServers": {
    "burp": {
      "command": "java",
      "args": ["-jar", "~/.BurpSuite/mcp-proxy/mcp-proxy-all.jar", "--sse-url", "http://127.0.0.1:9876"]
    }
  }
}
```

**Hermes** — see the [Hermes MCP guide](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes); use the same `java -jar … --sse-url …` command.

## Verify it loaded
- **Codex:** start a new thread and invoke `$bughunter recon <authorized-target>` or select the `bughunter` skill. A direct task such as *"test this authorized endpoint for SSRF"* may also auto-load `hunt-ssrf`.
- **OpenCode / Hermes / Google AntiGravity:** open the tool and describe a task; the matching skill should auto-load by description.
- **Hermes:** `hermes skills` should list the bundle from `~/.hermes/skills/`.
