# Routing example

Read when choosing how to split existing guidance. This is a shape, not a policy
to impose on another repository.

## Small entry point

```markdown
# Contributor entry point

Read the nearest instructions and preserve existing work. Follow this project's
branch workflow. Keep credentials and private customer data out of evidence.

## Find the owner

- Web interaction: apps/web; follow docs/agents/ui.md.
- API or authorization: services/api; follow docs/agents/backend.md.
- Internal prose: docs; follow docs/agents/documentation.md.
- Unknown owner: use docs/architecture.md, then scoped source search.

Before changing a boundary, inspect its caller, contract, and owning tests.
Required final checks are in docs/agents/validation.md.
Publishing and deployments require the authority defined in docs/releases.md.
```

Link actual files and headings when applying this shape. Leave a universal
approval gate in the root if an agent could otherwise act before reading it.
Avoid a chain of indexes that eventually requires reading every policy.

## Requirement ledger

| Requirement | Original source | Destination | Proof |
| --- | --- | --- | --- |
| Keep local changes | Root contributor rules | Root entry point | Meaning-level diff review |
| Web keyboard behavior | UI instructions | UI owner, Accessibility section | UI task walk-through |
| Verify ownership before writes | Backend instructions | Backend owner, Authorization section | Risky API task walk-through |
| Release requires authorization | Release instructions | Root reminder + canonical release policy | Explicit restriction retained |

Use the actual conditions and exceptions from the repository. Do not replace
specific rules with vague advice such as “be careful with security.” A heading
inventory is useful but cannot prove that its contents retain the same meaning.

## Representative routes

For each task, list every instruction file or section needed until the agent can
edit and validate correctly. Examples:

- Small UI correction: root → UI owner → accessibility section → validation.
- Cross-tenant API bug: root → backend owner → authorization → contract/tests.
- Internal spelling fix: root → documentation owner → relevant check guidance.

Check that shared entry-point aliases do not cause the same content to be loaded
repeatedly. Inspect how the target harness discovers nested instruction files;
an ordinary Markdown link does not guarantee automatic loading.
