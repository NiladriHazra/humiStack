#!/usr/bin/env python3
"""Check selected literal invariants and sizes, not prompt semantics."""

import argparse
import json
import sys
from pathlib import Path


def compare(before, after, contract):
    if not isinstance(contract, dict):
        raise ValueError("contract must be an object")
    protected = contract.get("protected")
    if not isinstance(protected, list) or not protected:
        raise ValueError("contract needs a nonempty protected list")
    if any(not isinstance(value, str) or not value.strip() for value in protected):
        raise ValueError("protected values must be nonempty strings")
    if len(set(protected)) != len(protected):
        raise ValueError("protected values must be unique")
    checks = []
    errors = []
    for value in protected:
        in_before = value in before
        in_after = value in after
        checks.append({"literal": value, "in_before": in_before, "in_after": in_after})
        if not in_before:
            errors.append("protected literal missing from baseline: {!r}".format(value))
        if not in_after:
            errors.append("protected literal missing from rewrite: {!r}".format(value))
    before_bytes = len(before.encode("utf-8"))
    after_bytes = len(after.encode("utf-8"))
    return {
        "before": {"bytes": before_bytes, "words": len(before.split())},
        "after": {"bytes": after_bytes, "words": len(after.split())},
        "byte_reduction_percent": round((1 - after_bytes / before_bytes) * 100, 2) if before_bytes else None,
        "checks": checks,
        "errors": errors,
        "scope": "Selected literals only; semantic equivalence and model behavior are unverified.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    args = parser.parse_args()
    try:
        before = args.before.read_text(encoding="utf-8")
        after = args.after.read_text(encoding="utf-8")
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        result = compare(before, after, contract)
    except (OSError, ValueError, UnicodeError) as error:
        result = {"errors": [str(error)]}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
