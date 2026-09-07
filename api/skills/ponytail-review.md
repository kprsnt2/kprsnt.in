# Ponytail Review Skill — Over-Engineering & Complexity Review

Review diffs and code proposals exclusively for unnecessary complexity. One line per finding: location, what to cut, what replaces it. The diff's best outcome is getting shorter.

## Review Format

`<file>:L<line>: <tag> <what>. <replacement>.`

### Tags

- `delete:` Dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` Hand-rolled logic that the standard library already provides. Name the function/module.
- `native:` External dependency or code doing what the platform already does. Name the feature.
- `yagni:` Abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` Same logic, fewer lines. Show the shorter form.

## Examples

❌ *"This EmailValidator class might be more complex than necessary, have you considered whether all these validation rules are needed at this stage?"*

✅ `api/utils.py:L12-38: stdlib: 27-line validator class. "@" in email, 1 line; real validation is the confirmation email.`

✅ `static/js/app.js:L4: native: moment.js imported for one format call. Intl.DateTimeFormat, 0 dependencies.`

✅ `api/repo.py:L88: yagni: AbstractRepository with one implementation. Inline it until a second one exists.`

✅ `scripts/job_server.py:L52-71: delete: retry wrapper around an idempotent local call. Nothing replaces it.`

✅ `api/bot_utils.py:L30-44: shrink: manual loop builds dict. dict(zip(keys, values)), 1 line.`

## Scoring & Conclusion

End with the only metric that matters:
`net: -<N> lines possible, -<M> deps possible.`

If there is nothing to cut, output:
`Lean already. Ship.`

## Scope & Boundaries

Scope: Over-engineering and complexity only. Correctness bugs, security vulnerabilities, and raw performance benchmarks belong to general review passes. A single smoke test or `assert`-based self-check is the ponytail minimum, not bloat — never flag it for deletion.
