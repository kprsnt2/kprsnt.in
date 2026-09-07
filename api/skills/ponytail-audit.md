# Ponytail Audit Skill — Whole-Repo Bloat & Over-Engineering Audit

Whole-codebase audit for over-engineering. Scans the entire project tree instead of an individual diff: returns a ranked list of what to delete, simplify, or replace with stdlib/native equivalents.

## Hunt Targets

1. **Unneeded Dependencies**: Libraries in `package.json` or `requirements.txt` where stdlib or platform native covers the usage.
2. **Single-Implementation Abstractions**: Interfaces, abstract base classes, or factory patterns with exactly one caller.
3. **Pass-Through Wrappers**: Classes or functions that only forward parameters without adding real value.
4. **Dead Flags & Speculative Configuration**: Settings and environment variables that are never toggled.
5. **Hand-Rolled Logic**: Custom parsers, formatters, and helpers that duplicate standard library functions.

## Audit Output Format

Rank findings biggest reduction first:
`<tag> <what to cut>. <replacement>. [<path>]`

### Tags
- `delete:` Dead or speculative code.
- `stdlib:` Replace with Python/JS stdlib.
- `native:` Replace with browser/platform native.
- `yagni:` Remove speculative abstraction.
- `shrink:` Condense multi-line logic.

End with:
`net: -<N> lines, -<M> deps possible.`
Or if clean: `Lean already. Ship.`
