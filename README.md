# humiStack

The agent skills I use to keep repositories and prompts lean, cleaned up so
anyone can use them. For Claude Code, Codex, and OpenCode.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `lean-repo` | "lean repo" | Cleans up bloated agent instructions and documentation so agents find the right code and rules faster. |
| `prompt-refactor` | "refactor this prompt" | Removes repetition from agent prompts while preserving their rules, exceptions, and tool contracts. |

Install either or both. They work independently.

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

A coding agent with file, search, and terminal tools. No extra dependencies.

## Make them yours

Edit the skills to fit your workflow. Keep project-specific rules in your
`AGENTS.md` or `CLAUDE.md` so skill updates stay separate from your settings.

## License

[MIT](LICENSE)
