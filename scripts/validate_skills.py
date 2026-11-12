#!/usr/bin/env python3
"""Validate this collection's intentionally simple, single-line frontmatter."""

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    spec = importlib.util.spec_from_file_location("guidance", ROOT / "skills/lean-repo/scripts/check_guidance.py")
    guidance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guidance)
    errors = []
    files = ["README.md", "evals/README.md", "docs/validation.md"]
    for directory in sorted((ROOT / "skills").iterdir()):
        if not directory.is_dir():
            continue
        entry = directory / "SKILL.md"
        if not entry.is_file():
            errors.append("{}: missing SKILL.md".format(directory.name))
            continue
        text = entry.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append("{}: missing frontmatter".format(directory.name))
            continue
        fields = {}
        for line in match[1].splitlines():
            key, separator, value = line.partition(": ")
            if not separator or key in fields:
                errors.append("{}: expected unique single-line frontmatter fields".format(entry))
            fields[key] = value
        name = fields.get("name", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64 or name != directory.name:
            errors.append("{}: invalid skill name".format(entry))
        description = fields.get("description", "")
        if not 1 <= len(description) <= 1024:
            errors.append("{}: description must be 1–1024 characters".format(entry))
        if len(text.splitlines()) > 500:
            errors.append("{}: move detail to references".format(entry))
        files.extend(str(path.relative_to(ROOT)) for path in directory.rglob("*.md"))
    result = guidance.check(ROOT, {"files": files})
    errors.extend(result["errors"])
    print(json.dumps({"skills": ["lean-repo", "prompt-refactor"], "files_checked": len(files), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
