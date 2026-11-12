---
name: claude-orchestrate
description: Coordinate coding and research through CLI workers with user-assigned roles and models. Use when asked to "Claude orchestrate", make Claude or Codex the coordinator, or delegate implementation and research to Codex, OpenCode, Cursor/Grok, or Gemini.
license: MIT
---

# Claude orchestrate

The main agent owns the plan, briefs, integration, and verification. Workers do
the assigned work. Claude or Codex can coordinate; the name does not lock the model.

## Choose the team

Read assignments from the request or the user's agent instructions. For example:

```text
Coordinator: Claude
Coding: Codex CLI, my configured GPT model
Research: Cursor CLI, my configured Grok model, read-only
Other: Gemini CLI, my configured model, only the tasks I assign
```

OpenCode can run the coding role instead. Honor explicit CLI, model, effort,
and role choices. Ask only for missing assignments that block work. Check installed
help/model discovery before launching; do not substitute an unavailable model.
The current session coordinates unless a different coordinator is actually launched
through a supported handoff. Report who is running, not who a label says is running.

## Assign bounded work

Read repository instructions and Git status. Split independent work into pieces
with no shared writable files. Start independent workers together; dependent work
waits for its prerequisite. A trivial fix may be faster to do directly unless
the user specifically assigned it to a worker.

Give each coding worker its own checkout from the actual task base, following
the host's isolation and project rules. Research is read-only and can share a
stable checkout. Keep UI/design with the coordinator unless the user assigns it.
Do not copy credentials, env files, or private conversation history into briefs.

Write a self-contained brief in local scratch:

```text
Goal: the outcome
Context: source files, contracts, and known facts
Scope: allowed files or exact research questions; working directory and base
Limits: project rules, forbidden changes, and the user's authority
Done: focused checks or cited findings
Report: STATUS done|blocked; CHANGED or FINDINGS; CHECKS; OPEN; SESSION
```

## Run the assigned CLI

Use the host's supported delegation/job controls and permission rules. Prefer
CLI workers where supported; if the host forbids them, report that limitation
and use only an authorized alternative. Keep job/session IDs and wait for completion
events where available; do not launch duplicate workers to replace a slow one.

These command shapes use installed CLI interfaces. Bind model, workspace, and
brief variables from the assignment; run in the assigned directory. `$TASK` is
the complete brief text and `$BRIEF` its absolute file path. Recheck flags for
the installed version. Run only the selected command, not all of them.

```bash
codex exec --cd "$WORKTREE" --model "$MODEL" --sandbox workspace-write - < "$BRIEF"
opencode run "Follow the attached brief." --dir "$WORKTREE" --model "$MODEL" --file "$BRIEF"
cursor-agent --print --mode ask --workspace "$REPO" --model "$MODEL" "$TASK"
gemini --model "$MODEL" --approval-mode plan --prompt "$TASK"
```

The Gemini example is read-only; coding assignments need an appropriate editing
mode. Keep research read-only. Honor the user's authorized permission settings;
do not add bypass flags automatically or install tools/change global configuration
just to start a worker. Put secrets through the host's credential mechanism.

## Verify and finish

Inspect actual diffs and results. Run relevant checks; open important research
sources and separate observed facts from inference. A worker's “done” is not proof.
Send precise corrections through supported follow-up controls. Reuse sessions
where the host permits; follow its rules if a fresh review task is required.

Integrate verified changes without overwriting unrelated work. Stop workers that
are replaced or no longer needed; preserve unlanded work. Do not merge, deploy,
or clean up branches without the required authority. Report worker/model, result,
checks, and remaining blockers briefly. Flag unverified model or context settings
rather than inventing them.
