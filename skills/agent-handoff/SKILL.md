---
name: agent-handoff
description: Transfer an ongoing task to another agent or fresh session with verified working state and a compact continuation brief. Use when asked to "hand this off", switch agents, prepare an agent handoff, or resume someone else's work. MaxMEM is optional.
license: MIT
---

# Agent handoff

Transfer enough state for the next agent to act correctly without rereading the
whole conversation. A handoff transfers a task; ordinary delegation leaves the
coordinator responsible for integration.

## Capture the actual state

Confirm the task, recipient, and whether the user wants a prepared brief or a
live transfer. Use the requested agent/model and host. If none is specified,
prepare the brief and ask only for the missing delivery target.

Read applicable instructions, Git status, branch, HEAD, and relevant diff. Record
the actual repository/worktree, including uncommitted changes and who owns them.
Do not stash, commit, push, discard, or relocate work just to make the handoff
look clean. Preserve the project's authorization and release gates.

Keep a compact brief:

```text
Goal: outcome and requested scope
Location: repository/worktree, branch, HEAD, access requirements
State: completed work, changed files, uncommitted work, active jobs
Decisions: important choices, constraints, and rejected approaches
Checks: exact commands, results, revision/environment, skipped paths
Open: blockers, failures, uncertainties, and pending decisions
Next: first concrete action, then remaining steps
Authority: what the user authorized and what still needs a decision
```

Use exact paths and results, but exclude credentials and unnecessary private
content. Distinguish completed checks from proposed checks. Include source links
and file locations instead of a transcript dump. Keep the brief in the response
or approved scratch; do not create a permanent HANDOFF.md by default.

## Deliver

Use the host's supported handoff/thread/CLI transport when the user requests a
live transfer. Send the brief and give the recipient access to the actual work.
A fresh checkout does not contain uncommitted changes; resolve that explicitly
without overwriting them. Follow host isolation rules rather than inventing a
shared writable workspace.

If MaxMEM is available and appropriate, save a compact capsule with raw chat off
and pass its context to the recipient. MaxMEM is optional: a plain brief works.
Do not claim shared memory, local paths, or running processes are accessible on
another machine without verifying it.

Coordinate active writers before changing ownership. Use supported wait/stop
controls, preserve their partial results, and avoid two agents editing the same
files. Do not delete a worktree or terminate unrelated jobs as handoff cleanup.

## Resume and verify

The receiving agent reads the current request and local instructions, then checks
the actual path, branch, revision, and diff against the brief. Reconcile drift
before editing; do not reset newer work to match stale context. Reuse check results
only while the relevant source and environment still match.

Report the actual state: **prepared** means a brief exists; **delivered** means it
was sent through the transport; **resumed** means the recipient has acknowledged
and verified the working state. A saved capsule or opened terminal alone proves
neither resumption nor completion. If delivery is unavailable, give the brief
and the precise remaining step.
