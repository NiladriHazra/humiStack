# Mechanical checks

Read when using the optional Python 3.9+ helper. It uses no external packages,
does not call a model, and does not write files.

Save the unchanged before text and proposed after text locally. Create a JSON
contract containing exact strings selected from the requirement ledger:

```json
{
  "protected": [
    "send_message",
    "TEMPORARY_UNAVAILABLE",
    "DENIED",
    "10 MiB"
  ]
}
```

```sh
python3 /absolute/path/to/prompt-refactor/scripts/check_contract.py \
  --before /path/to/before.md --after /path/to/after.md \
  --contract /path/to/contract.json
```

Each protected string must occur in both texts. A missing before string is an
invalid baseline/contract, not a successful preservation check. The protected
list must be nonempty, contain unique nonempty strings, and be chosen before
the rewrite. Strings can be whole constraints when wording must remain exact.
Repetition counts are not required to remain equal because duplicate removal
is one purpose of this skill.

Exit 0 means all selected literal checks pass. Exit 1 means a missing literal
or invalid input. JSON output reports per-text UTF-8 bytes and whitespace-word
counts, the byte reduction percentage, and individual check results. These are
not tokenizer counts, per-request usage, latency, or billing measurements.

The helper cannot identify every important constant, check meaning, validate
numeric bounds, or certify unchanged schemas. Review the complete ledger and
source diff, and run the owning tests. Do not keep a long protected-text list
in the runtime prompt; it is validation material, not another instruction layer.
