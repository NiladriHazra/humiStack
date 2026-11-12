---
name: prompt-refactor
description: Refactor agent prompts and skill instructions for clarity and less repetition while preserving requirements, exceptions, tool contracts, and approval gates. Use when asked to shorten system prompts, compress SKILL.md instructions, remove duplicate tool guidance, or optimize prompt context without changing intended behavior. Not for bypassing safeguards, ordinary prose editing, or changing the agent's product behavior.
license: MIT
---

# Prompt refactor

Reduce unnecessary instruction text. Preserve what the agent is required,
allowed, and forbidden to do, including when those rules apply.

## Establish the actual input

1. Follow applicable instructions and preserve existing work. Locate the requested
   prompt source, its caller/loader, references, tool declarations, and relevant
   tests. For a pasted prompt, work from that text and state missing runtime context.
2. Determine what the model actually receives: always-loaded instructions,
   dynamically selected skills, tool schemas/descriptions, history, and retrieved
   references. Do not optimize a file that is not used or count an entire on-disk
   library as if it loads on every turn.
3. Keep an unchanged before snapshot in approved local scratch or use a known Git
   revision. Do not copy secrets or private user content into public fixtures,
   reports, or external tools. An audit-only request stays read-only.

## Inventory requirements before rewriting

Keep a compact ledger with **requirement, source wording, intended meaning,
conditions/exceptions, and destination**. Include:

- permissions, prohibitions, approval gates, and ownership/privacy boundaries;
- sequencing, recovery, cancellation, and deferred/unsupported cases;
- exact tool/function names, parameters, enums, numeric limits, units, and URLs;
- examples or counterexamples that encode behavior the prose does not;
- precedence, dynamically loaded references, and cross-surface differences.

Separate intentional behavior from inherited inconsistencies. If the sources
conflict, use an established precedence rule or ask about the specific conflict.
Do not turn a compression task into a behavior fix without authority.

## Rewrite for decisions

- Remove genuine repetition, filler, and duplicated descriptions. Prefer direct
  verbs and concrete conditions. Keep the reason where it helps resolve ambiguity.
- Combine statements only when scope, actor, timing, and exceptions agree. Keep
  “must,” “may,” and “must not” distinct. Do not erase negation, units, or examples
  merely to reduce a count.
- Keep exact identifiers and callable contracts unchanged. Do not modify tool
  schemas, execution handlers, approval policies, or loading timing to obtain a
  smaller prompt.
- Remove a description duplicated by a tool schema only after verifying that the
  schema is present in every affected request path. Keep workflow-specific rules
  and selection guidance that the schema does not carry.
- Move detail to references only when the runtime can retrieve it at the correct
  time. A link in a system prompt is not an implementation of retrieval. If the
  runtime cannot load references, keep the necessary instructions inline.
- Prefer the smallest coherent edit over a new loader or abstraction. Preserve
  frontmatter, examples, licensing, and repository conventions where applicable.

Read [preservation review](references/preservation.md) for a ledger example and
high-risk rewrite patterns.

## Verify the result

1. Review the diff against every ledger entry. Check semantic equivalence of
   scope, negation, timing, fallback, and exceptions. Review the assembled payload
   for each affected activation/request path, not just individual files.
2. Run applicable schema, registry, authorization, loader, and regression checks.
   Keep the repository's required validation gates. Add a focused regression case
   when a meaningful lost condition was reproduced; avoid tests of prose spelling.
3. Optionally run the local protected-literal checker described in
   [mechanical checks](references/checks.md). It checks exact strings and sizes;
   it cannot prove meaning or model behavior. Check unchanged schemas/handlers
   separately with the source diff or an existing contract test.
4. Exercise representative tasks, including a refusal/approval boundary and an
   exception or recovery case. Use existing local fixtures first. Live-model
   evaluation requires the user's authority for its data and cost. If available,
   compare matched model/settings/tools/tasks and record correctness alongside
   usage and time. Do not silently buy inference to validate a text edit.
5. Label measurements precisely: bytes, words, tokenizer-specific estimates,
   provider-reported usage, or actual spend. Show what was included/excluded.
   A shorter source file does not establish a faster agent or a lower bill.

If equivalence remains uncertain, retain the original constraint and identify
the unresolved case. Structural checks alone are insufficient for an unqualified
“behavior preserved” claim.

## Handoff

State what was shortened, where the active instructions come from, and what
contracts stayed unchanged. Summarize the requirement review, checks, measured
scope, and remaining unverified behavior. Do not add a permanent report or extra
prompt layer unless it has a clear owner and ongoing use. Commit/publish only
when requested.
