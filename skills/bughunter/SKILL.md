---
name: bughunter
description: Route authorized bug-bounty, WAPT, and external red-team work through Codex-Bug-hunter workflows. Use for hunt, autopilot, recon, scope, surface ranking, triage, validation, reporting, chaining, intelligence, token scanning, Web3 audit, and hunt-memory operations in Codex or another Agent Skills client.
---

# BugHunter workflow router

Use this skill as the provider-neutral entry point for the bundle. Treat a request such as
`bughunter hunt target.com`, `$bughunter recon target.com`, or "run the BugHunter validate
workflow" as selecting one mode below.

Only operate on assets the operator is authorized to assess. Before active HTTP requests,
establish an explicit allowlist and apply the deny-wins scope gate. Never widen scope from
recon results, never submit a report automatically, and keep state-changing proof of concept
actions behind explicit operator approval.

## Dispatch

Read exactly one primary workflow reference first. Load another only when that workflow's
handoff table requires it:

- `hunt` -> [hunt](references/commands/hunt.md)
- `autopilot` -> [autopilot](references/commands/autopilot.md)
- `recon` -> [recon](references/commands/recon.md)
- `scope` -> [scope](references/commands/scope.md)
- `surface` -> [surface](references/commands/surface.md)
- `triage` -> [triage](references/commands/triage.md)
- `validate` -> [validate](references/commands/validate.md)
- `report` -> [report](references/commands/report.md)
- `chain` -> [chain](references/commands/chain.md)
- `intel` -> [intel](references/commands/intel.md)
- `token-scan` -> [token scan](references/commands/token-scan.md)
- `web3-audit` -> [Web3 audit](references/commands/web3-audit.md)
- `remember` -> [remember](references/commands/remember.md)
- `pickup` -> [pickup](references/commands/pickup.md)
- `memory-gc` -> [memory GC](references/commands/memory-gc.md)

The references originated as Claude Code slash commands. Ignore their YAML frontmatter and
translate `/mode` notation into the selected BugHunter mode. Do not assume Claude-specific
built-ins or tools exist. In Codex, use available shell, browser, and MCP tools with the same
safety gates. If a reference names a specialist such as `hunt-ssrf`, `triage-validation`, or
`report-writing`, load that skill before applying its methodology.

## Codex execution notes

- Project instructions live in `AGENTS.md`; `CLAUDE.md` is only a compatibility copy.
- Installed skills live under `~/.agents/skills`; do not assume `~/.claude/skills` exists.
- The deterministic CLI is `cbh`. The autonomous engine supports
  `python engine/engine.py --provider codex ...`.
- Burp tools are optional. If unavailable, use safe direct requests and say which evidence
  could not be collected; never invent MCP output.

Keep credentials and raw evidence out of tracked files. Redact cookies, tokens, PII, HARs,
and screenshots before sharing or reporting.
