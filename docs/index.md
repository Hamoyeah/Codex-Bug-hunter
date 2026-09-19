---
title: Home
nav_order: 1
description: An Agent Skills bundle for bug hunting and external red-team work in Claude Code and Codex.
permalink: /
---

# Codex-Bug-hunter
{: .fs-9 }

A provider-neutral Agent Skills bundle for Claude Code and OpenAI Codex that supplies
bug-hunting techniques, chain templates, VRT mappings, platform CVE chains, validation
gates, and evidence hygiene.
{: .fs-6 .fw-300 }

[Get started](#quickstart){: .btn .btn-primary .mr-2 }
[Browse the skill catalog](./skills.html){: .btn }
[View on GitHub](https://github.com/Hamoyeah/Codex-Bug-hunter){: .btn }

---

## What you get

- **84 skills** across recon, 58 web-app vuln-class + framework skills, enterprise
  platform attack, red-team tradecraft, and reporting — all **auto-loading by topic**,
  no invocation by name.
- **681 disclosed-report patterns** curated from public HackerOne reports — 433 now individually cited & auditable.
- **Enterprise attack matrices** — M365/Entra, Okta, SharePoint, vCenter, SSL-VPN,
  Android APK, supply-chain — with current 2024–2026 CVE chains.
- **Reporting + validation** — 7-Question Gate, VRT mapping, evidence hygiene,
  and a client-facing red-team deliverable format.
- **Burp MCP integration** and an engagement-folder scaffold.

## Quickstart

```powershell
# Codex on Windows
git clone https://github.com/Hamoyeah/Codex-Bug-hunter.git
cd Codex-Bug-hunter
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexOnly
# Start a new Codex thread, then use: $bughunter hunt <authorized-target>
```

```bash
# Codex on macOS / Linux
git clone https://github.com/Hamoyeah/Codex-Bug-hunter.git
cd Codex-Bug-hunter
bash scripts/install.sh --codex-only
```

```powershell
# Claude Code on Windows (PowerShell)
git clone https://github.com/Hamoyeah/Codex-Bug-hunter.git
cd Codex-Bug-hunter
pwsh ./scripts/install.ps1
```

Then open Codex or Claude Code and describe what you're testing in plain English —
the relevant skill loads automatically. In Codex, `$bughunter hunt <target>` selects
the complete hunt workflow explicitly:

```
> I'm testing acme.com, an in-scope HackerOne target. Start recon and
  rank the attack surface.
```

See the full [Installation guide](https://github.com/Hamoyeah/Codex-Bug-hunter/blob/main/INSTALL.md)
and [Usage guide](https://github.com/Hamoyeah/Codex-Bug-hunter/blob/main/USAGE.md).

## Stay in scope

This bundle is for assets you **own** or are **authorized to assess** (in-scope
bug-bounty programs, signed-RoE pentests, CTFs, your own lab). It ships
validation gates that auto-trigger on ambiguity. See the
[Security policy](https://github.com/Hamoyeah/Codex-Bug-hunter/blob/main/SECURITY.md).

---

## Sponsored by

[Atlas Cloud](https://www.atlascloud.ai/console/coding-plan) — a full-modal AI
inference platform: one API for video, image, and LLM models (300+ curated).
Check out their [coding-plan promotion](https://www.atlascloud.ai/console/coding-plan)
for budget-friendly API access.
