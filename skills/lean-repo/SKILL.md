---
name: lean-repo
description: Simplify a repository's agent instructions, skills, and documentation navigation while preserving its rules. Use when asked to clean up bloated AGENTS.md or CLAUDE.md files, reduce unnecessary agent context, consolidate overlapping guidance, or make a large repo easier for coding agents to navigate. Not for ordinary feature work or application-directory migrations.
license: MIT
---

# Lean repo

Make the next real task easier to find and complete. A short root file is useful
only if the agent can still find the right rules and source code.

## Establish the boundary

1. Read the applicable repository instructions and working-tree status. Preserve
   existing changes and use the repository's required branch/worktree workflow.
2. Identify the requested surface: root instructions, a subtree, skill discovery,
   or a documentation set. An audit-only request authorizes inspection and a
   recommendation, not edits. Otherwise make the requested cleanup directly.
3. Inspect the current entry instructions and their immediate references. Follow
   relevant links selectively; do not start by reading every document or indexing
   the entire repository. Exclude dependencies, build output, generated files,
   secrets, private content, and unrelated checkouts.
4. Choose two or three representative tasks, including an exception or risky
   boundary. Establish their actual source owners from code, callers, package
   scripts, and relevant tests. Directory names alone do not establish ownership.

## Inventory what must survive

Keep a compact working ledger: **requirement → current source → intended owner**.
Include prohibitions, permissions, exceptions, validation/release gates, and
precedence. Record duplicate and contradictory instructions separately.

Distinguish rules from historical notes and examples. Preserve useful examples
that encode a boundary. Do not resolve a policy disagreement by silently deleting
the stricter wording; follow an existing precedence rule or ask about that
specific conflict while continuing independent work.

## Apply the smallest useful structure

- Keep universally needed constraints and direct task links in the root entry.
  Move task-specific detail to clearly named owners. Keep critical prohibitions
  visible enough that an agent cannot miss them before taking the relevant action.
- Reuse existing owners before creating files. Give each rule one canonical home;
  keep any other necessary entry points as short references. Respect the harness's
  supported discovery and alias behavior; do not assume every agent follows symlinks.
- Explain where the code lives, how to find its contracts, and which checks apply.
  Avoid copying source-owned catalogs or creating another permanent session log.
- Shorten skill metadata and entry instructions. Keep detailed references
  available on demand, with clear reasons to open them. Preserve licenses and
  provenance. Merge skills only when their triggers and outcomes genuinely overlap.
- Use scoped text search and connected symbol tools when available. Add a graph,
  hosted index, hooks, or another dependency only for a demonstrated need within
  the user's authority. Smaller guidance does not require new infrastructure.
- Preserve application layout, public APIs, security boundaries, and existing
  check/release requirements. This task does not authorize a runtime refactor,
  deleting unfamiliar files, publishing, or changing organization policy.

Read [the routing example](references/routing.md) if you need an example of a
small entry point and a requirement ledger. Adapt its shape, not its policies.

## Prove preservation and navigation

1. Reconcile every ledger entry with its destination and inspect the full diff.
   Check meaning, scope, conditions, and exceptions—not just matching headings.
2. Walk the representative tasks through the new entry points. Verify that the
   route reaches the code owner, applicable constraints, and required checks.
   Include downstream references in the reading budget; a tiny router that
   forces a full policy read has not solved the problem.
3. Check local links, heading targets, and any aliases. The optional read-only
   helper and its manifest are documented in
   [structural checks](references/checks.md). Use absolute paths to the installed
   skill's script; relative project paths are not the skill installation path.
4. Run the repository's applicable instruction/configuration checks. Reuse valid
   results until relevant files or assumptions change. Preserve its final gate;
   do not invent a full build for prose or skip one the repository requires.
5. Report selected file sizes and complete declared reading routes. Label bytes,
   words, or tokenizer estimates accurately. Claim speed or billing savings only
   from comparable tasks with actual timing/usage and a correctness check.

If a requested boundary cannot be preserved confidently, leave that part intact
and identify the specific unresolved requirement. Do not block unrelated cleanup.

## Handoff

Lead with the outcome, then give:

- the entry point and canonical owners;
- requirements preserved, conflicts resolved, and any open decisions;
- representative routes and the checks actually run;
- measurements with their scope, plus unverified behavior.

Keep the handoff concise. Put a durable map in the repository only when it serves
future work. Commit, push, or publish only when requested.
