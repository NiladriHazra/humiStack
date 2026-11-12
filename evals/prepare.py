#!/usr/bin/env python3
"""Create fresh, paired synthetic evaluation fixtures in a new directory."""

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new directory; existing paths are rejected")
    args = parser.parse_args()
    args.destination.mkdir(parents=False, exist_ok=False)
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]
    for case in cases:
        for mode in ["with_skill", "without_skill"]:
            directory = args.destination / case["id"] / mode
            directory.mkdir(parents=True)
            for relative, text in case["files"].items():
                path = directory / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
        metadata = {key: value for key, value in case.items() if key != "files"}
        (args.destination / case["id"] / "case.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print("Prepared {} paired cases in {}".format(len(cases), args.destination))


if __name__ == "__main__":
    main()
