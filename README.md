# humiStack

The agent skills I use for coding, delegation, and handoffs, cleaned up so
anyone can use them. For Claude Code, Codex, and OpenCode.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `lean-repo` | "lean repo" | Cleans up bloated agent instructions and documentation so agents find the right code and rules faster. |
| `prompt-refactor` | "refactor this prompt" | Removes repetition from agent prompts while preserving their rules, exceptions, and tool contracts. |
| `claude-orchestrate` | "Claude orchestrate" | Lets Claude or Codex coordinate CLI workers, with models and tasks assigned by you. |
| `maxmem` | "maxmem" | Saves and restores compact project memory across agent sessions using MaxMEM. |
| `agent-handoff` | "hand this off" | Prepares and transfers a task to another agent with its current state, checks, and next steps. |

Install the ones you need. They work independently.

## Install

```bash
npx skills add NiladriHazra/humiStack
```

Or copy them directly:

```bash
git clone https://github.com/NiladriHazra/humiStack
cp -R humiStack/skills/* ~/.claude/skills/           # Claude Code
cp -R humiStack/skills/* ~/.codex/skills/            # Codex
cp -R humiStack/skills/* ~/.config/opencode/skills/  # OpenCode
```

## Requirements

- A coding agent with file, search, and terminal tools.
- `claude-orchestrate` needs the worker CLIs and model access you assign.
- `maxmem` needs [MaxMEM](https://github.com/NiladriHazra/MaxMEM) installed and configured; its CLI requires Bun.
- `agent-handoff` works with a plain brief; MaxMEM is optional.

## Make them yours

Edit the skills to fit your workflow. Keep project-specific rules in your
`AGENTS.md` or `CLAUDE.md` so skill updates stay separate from your settings.

## License

[MIT](LICENSE)
