---
name: lean-repo
description: Clean up bloated agent instructions, overlapping skills, and documentation navigation without losing repository rules. Use when asked for a "lean repo", to simplify AGENTS.md or CLAUDE.md, or to make a repository easier for coding agents to navigate.
license: MIT
---

# Lean repo

Make the next task easier to find and complete. A shorter root file helps only
if the agent can still reach the right source, rules, and checks.

## Find the problem

Read the applicable instructions and Git status. Preserve existing work and
follow the project's branch/worktree rules. Audit-only requests stay read-only;
otherwise apply the requested cleanup.

Start with the entry instructions and their immediate references. Follow links
selectively. Skip dependencies, generated output, secrets, and unrelated projects.
Use scoped search and symbol tools before adding an index or other infrastructure.

Choose two or three real tasks, including a risky boundary. Find their source
owners, callers, contracts, and relevant tests. Directory names are not proof
of ownership.

## Simplify the guidance

Keep a short working list: requirement → current source → canonical owner.
Include permissions, prohibitions, exceptions, precedence, and release/test gates.
Separate duplicates from contradictions. Use established precedence; ask about
unresolved policy conflicts rather than silently changing them.

- Keep universal constraints and direct task links in the root instructions.
- Move task-specific detail to existing owners where possible. Give each rule
  one home and link to it from other entry points.
- Keep critical gates visible before the action they govern. Check how the
  agent actually discovers nested instructions and aliases.
- Consolidate skills only when their triggers and outcomes overlap. Keep useful
  examples, references, licenses, and provenance.
- Explain where code lives and which checks apply. Avoid copied catalogs,
  chains of indexes, and permanent session reports.

Preserve application layout, APIs, security boundaries, and required gates.
Instruction cleanup does not authorize runtime refactoring, policy changes,
publishing, or deleting unfamiliar files.

## Check the result

Review every requirement against its destination. Matching headings alone do
not establish preservation; check scope, conditions, and exceptions.

Walk the chosen tasks through the new entry points to their source and checks.
Verify links, heading targets, and aliases. Include downstream references when
counting the reading needed; a tiny router that loads everything is not lean.

Run the project's applicable guidance checks and required gate. Reuse valid
results until relevant files or assumptions change. If a constraint remains
uncertain, keep it and identify the unresolved case.

Report the new entry point, canonical owners, checks, and open decisions briefly.
Label size estimates accurately. Claim faster tasks or lower bills only from
comparable timing/usage measurements with correctness checks. Commit or publish
only when requested.
