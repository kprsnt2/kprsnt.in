# Ponytail Debt Skill — Technical Debt & Shortcut Ledger

Scans the codebase for `ponytail:` comments naming deliberate shortcuts, ceilings, and upgrade paths so temporary trade-offs stay visible and never silently rot into permanent technical debt.

## Scan Protocol

Search for deliberate ponytail shortcuts across code comments:
- Python / Bash: `# ponytail: <ceiling>, <upgrade path>`
- JS / CSS / JSON: `// ponytail: <ceiling>, <upgrade path>` or `/* ponytail: ... */`

## Output Format

One row per marker, grouped by file:
`<file>:<line>: <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

Flag any marker that lacks an upgrade trigger as `[no-trigger]` to highlight silent rot risk.

End with:
`<N> markers tracked, <M> with no trigger.`
Or if none found: `No ponytail debt. Clean ledger.`
