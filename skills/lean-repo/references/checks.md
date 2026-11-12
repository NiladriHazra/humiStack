# Structural checks

Read when using the bundled helper. It needs Python 3.9+, no third-party packages.
It reads selected local files and prints JSON; it does not edit anything.

Create a small JSON manifest in scratch or the project's existing check area:

```json
{
  "files": ["AGENTS.md", "docs/agents/ui.md", "docs/agents/validation.md"],
  "routes": [
    {
      "name": "small-ui-change",
      "reads": [
        {"path": "AGENTS.md"},
        {"path": "docs/agents/ui.md", "heading": "Accessibility"},
        {"path": "docs/agents/validation.md"}
      ]
    }
  ],
  "aliases": [{"path": "CLAUDE.md", "target": "AGENTS.md"}]
}
```

Omit `aliases` if the project does not use symlink aliases. Paths are relative to
the project root. A route's `heading` is the literal ATX heading title; its section
includes child headings and ends at the next equal/higher-level heading.

```sh
python3 /absolute/path/to/lean-repo/scripts/check_guidance.py \
  --root /path/to/project --manifest /path/to/guidance.json
```

Exit 0 means the declared structural checks pass. Exit 1 means a failed check or
invalid manifest. The output includes bytes and whitespace-separated word counts
for selected files and declared route reads. A repeated read is counted again.
These are declared retrieval budgets, not observed agent consumption or tokens.

The helper checks inline Markdown links and reference definitions outside fenced
code blocks. It checks existence of local targets and common GitHub-style ATX
heading anchors, including duplicate suffixes and HTML `id` anchors. It reports
external URLs without requesting them. It does not parse every Markdown dialect,
HTML links, Setext headings, dynamic MDX, or framework-generated routes. For
unsupported syntax use the repository's renderer/link checker or inspect it
directly. All file inputs/targets must resolve inside the project root.

Keep the manifest scoped. The helper does not crawl referenced files recursively;
add every guidance owner you want checked to `files`. A valid link does not prove
that its target gives correct advice. The requirement ledger and task walk-through
remain necessary.
