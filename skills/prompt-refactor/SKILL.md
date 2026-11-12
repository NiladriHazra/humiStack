---
name: prompt-refactor
description: Shorten agent prompts and skill instructions while preserving requirements, exceptions, and tool contracts. Use when asked to "refactor this prompt", compress system instructions, or remove repeated guidance without changing intended behavior.
license: MIT
---

# Prompt refactor

Remove unnecessary words without changing what the agent must, may, or must
not do.

## Read what actually runs

Follow the project's instructions and preserve existing work. Find the prompt,
its loader, references, tool declarations, and relevant tests. For pasted text,
work from what was supplied and identify missing runtime context. Audit-only
requests stay read-only.

Check which instructions and schemas reach each request path. A file on disk
is not necessarily loaded, and a linked document is not necessarily retrievable.
Keep a before snapshot in local scratch or use a known Git revision. Keep private
content out of public fixtures and external tools.

## Preserve the contract

Make a short working list of requirements and where each will survive:

- Permissions, prohibitions, approval gates, and ownership/privacy boundaries.
- Conditions, exceptions, sequence, cancellation, recovery, and unsupported cases.
- Exact tool names, parameters, enums, numeric limits, units, and URLs.
- Examples that encode behavior, precedence, and differences between clients.

Use established precedence for conflicts; ask about unresolved contradictions.
A compression task does not authorize a behavior change.

## Rewrite

Remove filler and genuine repetition. Use direct verbs and concrete conditions.
Combine rules only when their actor, scope, timing, and exceptions agree.
Preserve negation and the distinction between a requirement and a permission.

Remove duplicated tool descriptions only after confirming the schema supplies
them in every affected path. Keep workflow rules the schema does not express.
Move detail to references only if the runtime can retrieve it when needed;
otherwise keep the necessary instructions inline.

Keep schemas, handlers, approval policies, and loading behavior unchanged.
Preserve useful examples, metadata, licensing, and project conventions. Prefer
a direct text edit over a new loader or abstraction.

## Check the result

Review the full diff against every requirement, including conditions and
exceptions. Inspect assembled payloads for each affected path or skill combination.
Check exact identifiers and constants separately; matching strings cannot prove
that a rule still means the same thing.

Run applicable contract, loader, authorization, and regression checks, including
the project's required gate. Walk through representative tasks, including an
approval/refusal boundary and a recovery or exception case. Keep the original
constraint where equivalence remains uncertain. Use live-model tests only within
the user's data and spending authority.

Report the rewrite, preserved contracts, checks, and unverified behavior briefly.
Distinguish bytes, words, tokenizer estimates, and provider usage. Shorter text
alone does not prove identical model behavior, lower latency, or lower bills.
Commit or publish only when requested.
