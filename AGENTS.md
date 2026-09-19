# Codex-Bug-hunter contributor and runtime guidance

This is the Codex-first distribution. Keep shared content provider-neutral, expose the
primary workflow through `skills/bughunter/SKILL.md`, and retain Claude slash-command
behavior in `commands/` only as a compatibility layer.

For security work, require an explicit authorized scope before active requests. Deny rules
win, recon discoveries never widen scope automatically, state-changing proof of concept
actions require explicit operator approval, and reports are never submitted automatically.

When changing a workflow command, update its matching file under
`skills/bughunter/references/commands/`. Keep every skill description at 1024 characters or
less and use only supported Agent Skills frontmatter keys. Store grounding sources and hunt
report counts in `metadata/skill-provenance.json`. Run the plugin validator, skill
validator, document-count check, Python compile check, engine mock run, and shell syntax
checks before release.
