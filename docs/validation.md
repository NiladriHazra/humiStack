# Validation

## Local checks

The collection uses standard Agent Skills directories and simple YAML metadata.
Its Python helpers target Python 3.9+ and the standard library. Local checks are:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_skills.py
```

The unit tests cover broken links/anchors, fenced examples, route section
boundaries, encoded paths, aliases, path escapes, malformed manifests, literal
loss, invalid baselines, UTF-8 counts, and CLI failure/no-write behavior.
The collection validator checks metadata and selected local Markdown links.
It intentionally supports this collection's single-line frontmatter, rather
than acting as a general YAML validator.

## Agent-task evaluation

The [paired evaluation procedure](../evals/README.md) and four synthetic cases
are included so results can be reproduced. On November 13, 2026, all four were
executed in fresh OpenCode general-agent sessions, once with the relevant skill
and once without it. The eight runs used separate, identical local fixtures.
Baseline runs were instructed not to load humiStack. The native task interface
did not expose per-run provider/model settings or usage counters, so those are
not treated as verified matched settings or used for performance claims.

The initial review checked all 19 case assertions in each configuration:

- Repository edit: authorization, UI constraints, required gate, source owners,
  local links, and unchanged application files were preserved.
- Read-only audit: both runs left source files unchanged and identified the
  contradictory deployment rules.
- Prompt boundaries: both runs retained approval/drafting/workspace distinctions,
  binary file limits, retry eligibility/cap, cancellation, and draft retention.
- Prompt payloads: both runs kept required guidance inline and preserved the web
  and offline loader behavior.

All assertions passed for both configurations. The with-skill outputs included
explicit requirement ledgers and bounded measurement/verification scopes. These
small cases establish a useful smoke test, **not a demonstrated advantage over
the baseline**, broad semantic equivalence, or measured cost/latency savings.
Review was performed by the skill author against output files and execution
handoffs; it was not a blinded or independently graded study. Hosted CI and
interactive installation across Claude Code, Codex, and OpenCode are separate
from these local fixture checks.

## Scope

No live product-model inference, production deployment, provider-billing
benchmark, or cross-harness integration certification is implied. The helper
checks are structural. The skills require a separate requirement review and
representative task verification before claiming behavior preservation.
