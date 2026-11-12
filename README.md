# humiStack

Practical agent skills for keeping repositories navigable and prompts lean.
Built from workflows I use on a real multi-app codebase, rewritten so you can
use them in yours.

## Skills

| Skill | Ask your agent | Result |
| --- | --- | --- |
| [lean-repo](skills/lean-repo/SKILL.md) | “Make this repo easier for coding agents to work in.” | Short entry instructions, clear ownership, task-specific references, and checked navigation. |
| [prompt-refactor](skills/prompt-refactor/SKILL.md) | “Shorten these agent prompts without losing their requirements.” | A focused rewrite with a requirement ledger, protected-literal checks, and an honest validation report. |

The skills are independent. Install either or both. They follow the
[Agent Skills format](https://agentskills.io/specification) and use ordinary
file, search, and terminal tools. They do not require subagents, a particular
model, a hosted index, or a paid API.

## Install

With the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add NiladriHazra/humiStack --skill lean-repo --skill prompt-refactor
```

Or clone the repository and copy the two skill directories into your agent's
skills directory. Common locations are:

| Agent | Personal skills directory |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenCode | `~/.config/opencode/skills/` |

```sh
git clone https://github.com/NiladriHazra/humiStack.git
```

Copy the whole skill directory, including its `references` and `scripts`.
Check for an existing skill with the same name before replacing anything.
Restart your session or refresh skill discovery as your agent requires.

## Use

**Repository cleanup**

> Use lean-repo on this repository. Keep the application layout and release
> requirements intact. Simplify the agent instructions and check the routes for
> a small UI change, a backend bug, and a documentation edit.

**Prompt cleanup**

> Use prompt-refactor on the support-agent instructions. Preserve tool names,
> approval rules, limits, and examples that encode edge cases. Keep the tool
> schema unchanged and show which requirements moved or were rewritten.

Audit-only requests stay read-only. The skills respect your existing repository
instructions and change only the requested scope. Your personal defaults belong
in your own agent instructions, so updating a skill does not overwrite them.

## Checks and requirements

The workflows can be followed without Python. Their optional helpers require
**Python 3.9+**, use only its standard library, read explicitly supplied local
files, print JSON, and do not modify your project or call a network service.

- `lean-repo` checks a selected guidance manifest: local links, heading targets,
  instruction aliases, and declared task-reading routes.
- `prompt-refactor` checks protected literal strings against the before/after
  text and reports byte and whitespace-word counts.

These are structural checks. A passing result does not prove that every policy
survived, that a model behaves identically, or that your bill will fall. The
skills also require a meaning-level review and task-specific verification.

Run this repository's checks:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_skills.py
```

See [evaluation cases and procedure](evals/README.md) for realistic tasks to run
with and without each skill. See [validation results](docs/validation.md) for
what has actually been exercised.

## Contributing

Keep each skill focused on one repeatable job. Include a realistic use case and
update its evaluation cases when behavior changes. Run the two checks above.
Avoid hardcoded personal paths, organization policies, and unverified savings
claims. Preserve permissions, exceptions, and source licensing when adapting
instructions.

## Credits and license

The simple, installable collection format was inspired by
[Theo's tstack](https://github.com/t3dotgg/tstack). These two workflows and helpers
were written for humiStack; tstack's skill text is not bundled here.

[MIT](LICENSE) © 2026 Niladri Hazra.
