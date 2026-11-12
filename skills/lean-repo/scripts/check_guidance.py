#!/usr/bin/env python3
"""Check an explicit local guidance manifest without crawling or writing files."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def prose(text):
    """Blank fenced code while retaining line positions for section slicing."""
    fence = None
    result = []
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            result.append("\n" if line.endswith("\n") else "")
        elif marker:
            fence = marker[1]
            result.append("\n" if line.endswith("\n") else "")
        else:
            result.append(line)
    return "".join(result)


def headings(text):
    result = []
    for index, line in enumerate(prose(text).splitlines()):
        match = re.match(r"^ {0,3}(#{1,6})\s+(.+?)\s*$", line)
        if match:
            title = re.sub(r"\s+#+$", "", match[2])
            result.append((index, len(match[1]), title))
    return result


def anchors(text):
    seen = set()
    for _, _, title in headings(text):
        plain = re.sub(r"<[^>]+>", "", title).lower()
        slug = re.sub(r"[^\w\- ]", "", plain).replace(" ", "-")
        candidate = slug
        suffix = 0
        while candidate in seen:
            suffix += 1
            candidate = "{}-{}".format(slug, suffix)
        seen.add(candidate)
    seen.update(re.findall(r'\bid=[\'"]([^\'"]+)[\'"]', prose(text)))
    return seen


def section(text, title):
    entries = headings(text)
    matches = [entry for entry in entries if entry[2] == title]
    if len(matches) != 1:
        raise ValueError("heading {!r} must occur exactly once".format(title))
    start, level, _ = matches[0]
    lines = text.splitlines(keepends=True)
    end = next((line for line, depth, _ in entries if line > start and depth <= level), len(lines))
    return "".join(lines[start:end])


def local_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("expected a nonempty root-relative path")
    resolved = (root / relative).resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError("path escapes project root: {}".format(relative))
    return resolved


def text_at(root, relative):
    return local_path(root, relative).read_text(encoding="utf-8")


def counts(text):
    return {"bytes": len(text.encode("utf-8")), "words": len(text.split())}


def links(text):
    content = prose(text)
    inline = re.findall(r"!?\[[^\]\n]*\]\(\s*<?([^\s)>]+)>?(?:\s+[^)]+)?\)", content)
    definitions = re.findall(r"^ {0,3}\[[^\]\n]+\]:\s*<?([^\s>]+)>?", content, re.MULTILINE)
    return inline + definitions


def check(root, manifest):
    errors = []
    external = set()
    result = {"files": [], "routes": [], "aliases": [], "external_urls_unchecked": [], "errors": errors}
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list) or not manifest["files"]:
        raise ValueError("manifest needs a nonempty files list")
    for key in ("routes", "aliases"):
        if not isinstance(manifest.get(key, []), list):
            raise ValueError("{} must be a list".format(key))
    for relative in manifest["files"]:
        try:
            text = text_at(root, relative)
            result["files"].append({"path": relative, **counts(text)})
            for target in links(text):
                try:
                    url = urlsplit(target)
                    if url.scheme or url.netloc:
                        external.add(target)
                        continue
                    destination = unquote(url.path)
                    if destination.startswith("/"):
                        raise ValueError("use relative local links: {}".format(target))
                    linked = str(Path(relative).parent / destination) if destination else relative
                    resolved = local_path(root, linked)
                    if url.fragment:
                        fragment = unquote(url.fragment)
                        if not resolved.is_file() or fragment not in anchors(resolved.read_text(encoding="utf-8")):
                            raise ValueError("missing heading/anchor: {}".format(target))
                except (OSError, ValueError, UnicodeError) as error:
                    errors.append("{}: {}".format(relative, error))
        except (OSError, ValueError, TypeError, UnicodeError) as error:
            errors.append("{}: {}".format(relative, error))
    for route in manifest.get("routes", []):
        try:
            if not isinstance(route, dict) or not isinstance(route.get("name"), str) or not route["name"]:
                raise ValueError("route needs a nonempty name")
            if not isinstance(route.get("reads"), list) or not route["reads"]:
                raise ValueError("route needs nonempty reads")
            reads = []
            for read in route["reads"]:
                if not isinstance(read, dict) or "path" not in read:
                    raise ValueError("each route read needs a path")
                text = text_at(root, read["path"])
                if "heading" in read:
                    if not isinstance(read["heading"], str) or not read["heading"]:
                        raise ValueError("heading must be a nonempty string")
                    text = section(text, read["heading"])
                reads.append({**read, **counts(text)})
            result["routes"].append({"name": route["name"], "reads": reads, "bytes": sum(read["bytes"] for read in reads)})
        except (OSError, ValueError, TypeError, UnicodeError) as error:
            errors.append("route {}: {}".format(route, error))
    for alias in manifest.get("aliases", []):
        try:
            if not isinstance(alias, dict) or "path" not in alias or "target" not in alias:
                raise ValueError("alias needs path and target")
            resolved = local_path(root, alias["path"])
            expected = local_path(root, alias["target"])
            if not (root / alias["path"]).is_symlink() or resolved != expected:
                raise ValueError("alias must be a symlink to {}".format(alias["target"]))
            result["aliases"].append(alias)
        except (OSError, ValueError, TypeError) as error:
            errors.append("alias {}: {}".format(alias, error))
    result["external_urls_unchecked"] = sorted(external)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("root must be a directory")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = check(root, manifest)
    except (OSError, ValueError, UnicodeError) as error:
        result = {"errors": [str(error)]}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
