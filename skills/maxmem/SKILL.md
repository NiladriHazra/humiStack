---
name: maxmem
description: Use MaxMEM to save or restore local project memory, create compact handoff capsules, or continue work in another agent. Use when asked for "maxmem", to remember a project decision, recover session context, or make a MaxMEM handoff. Requires the MaxMEM application or MCP integration.
license: MIT
---

# MaxMEM

Keep the useful task state between sessions without carrying the entire chat.
This skill uses [MaxMEM](https://github.com/NiladriHazra/MaxMEM); it does not
install the application or its hooks.

## Choose the action

If the user only says “maxmem”, offer: resume, save handoff, project memory,
companion, or launch Claude/Codex/OpenCode. Do not launch another agent merely
because the skill was loaded.

Use the current task's actual repository/worktree. Prefer available MaxMEM MCP
tools; server prefixes vary. If unavailable, use the installed CLI. Check its
help before assuming flags. If MaxMEM is missing, explain the setup needed.
Keep installation and hook repair separate from memory operations. The CLI can
auto-repair integrations; use `MAXMEM_SKIP_AUTO_SETUP=1` for calls that should
only work with existing memory/setup.

## Resume

Fetch `maxmem_get_latest_handoff` and relevant `maxmem_list_project_memory`, or
run `maxmem inject` and `maxmem memory` in the correct repository. Read only what
helps the current task. Compare the capsule's branch, revision, changed files,
and checks with live Git state before continuing. Retrieve supporting evidence
before relying on an exact historical error, value, identifier, or test result;
mark unavailable evidence unverified. Old memory is context, not permission to
overwrite work or override the current request.

## Save

Record durable decisions, blockers, verification results, and completed tasks
with the matching `maxmem_save_*` or `maxmem_mark_task_done` tool. Keep notes
specific and current. Distinguish proposed checks from executed commands, recording
the result, revision, environment, and evidence location. Do not mark unfinished
work done. A handoff captures the goal, worktree/revision, changes, decisions,
checks, blockers, and next action.
Save missing task details as project memory; pass a known transcript path when
available, never an invented one. Call `maxmem_save_handoff` with supported fields,
compact verbosity, and raw chat off, then inspect the saved result.

Do not save secrets or unnecessary private content. Review extracted state;
automatic redaction is not a reason to include sensitive material. Full verbosity,
raw transcripts, clipboard export, and external sharing need the user's request.

CLI equivalents, run from the relevant repository with auto-setup disabled:

```bash
MAXMEM_SKIP_AUTO_SETUP=1 maxmem inject
MAXMEM_SKIP_AUTO_SETUP=1 maxmem memory
MAXMEM_SKIP_AUTO_SETUP=1 maxmem memory --kind decision --add "The durable decision"
MAXMEM_SKIP_AUTO_SETUP=1 maxmem handoff --agent claude --goal "Continue the task" --verbosity compact
```

Replace the example source agent and goal with the actual session. MaxMEM's
source-agent adapters are Claude, Codex, and OpenCode; do not invent adapter names.

## Continue elsewhere

When asked, use `maxmem launch TARGET --from SOURCE --goal "The task"`, or
`maxmem companion` for the local viewer. Keep auto-setup disabled unless setup
was requested. Launch targets are `claude`, `codex`, and `opencode`; the target
CLI must already be available. Saving a capsule is not starting a recipient.

Report what was saved, restored, or launched and any missing state. A read event
or launched terminal does not prove the next agent finished the task. Keep
capsules in MaxMEM's local store rather than adding session reports to the repo.
