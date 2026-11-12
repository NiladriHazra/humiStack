# Preservation review

Read when building the requirement ledger or reviewing a risky rewrite.

## Example ledger

| ID | Requirement | Conditions and exceptions | Destination/proof |
| --- | --- | --- | --- |
| R1 | Obtain approval before `send_message` | Drafting alone needs no approval | Rewritten approval paragraph + approved/unapproved scenarios |
| R2 | Never send outside the selected workspace | Applies even after approval | Ownership paragraph + cross-workspace case |
| R3 | Retry at most 2 times | Only on `TEMPORARY_UNAVAILABLE`; never on `DENIED` | Recovery paragraph + boundary cases |

Record the real source wording as well. Exact-string checks can preserve names
and constants while still missing a reversed rule:

- Original: “Never send without approval.”
- Broken rewrite: “Send without approval.”

Both contain `send` and `approval`. Only a meaning-level check catches the loss.

## Risky simplifications

- “Always ask” replacing “ask before a remote write, not before local drafts.”
- “Retry twice” losing the allowed error codes, backoff, or cancellation rule.
- “Use the native screen” losing the distinction between active and deferred UI.
- “Follow the schema” deleting a cross-tool sequence absent from the schema.
- “Read the linked guide” when the runtime has no retrieval tool.
- Removing a numeric unit: `10 MB`, `10 MiB`, and `10` are not equivalent.
- Keeping every heading while deleting the restriction inside one.

## Payload paths

For conditional skills, inspect no-skill, one-skill, and relevant combined-skill
payloads. For multiple clients, inspect each actual rendering path. Confirm the
tool names and schemas available there before removing duplicated descriptions.
If two paths differ, keep a shared constraint where both receive it or retain
the relevant inline wording. Avoid adding a new loading system just for this task.

## Evidence levels

1. Byte/word counts: size of selected text only.
2. Protected literals and source diffs: selected structural invariants.
3. Ledger review and local scenarios: scoped requirement preservation.
4. Matched live-model runs: observed behavior/usage on those tasks and settings.
5. Comparable provider billing: measured spend for the stated workload.

Do not present one level as proof of another. Keep a useful rewrite even if a
matched live-model benchmark was not authorized; describe that limit plainly.
