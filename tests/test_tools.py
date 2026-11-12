import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guidance = load("guidance", "skills/lean-repo/scripts/check_guidance.py")
contract = load("contract", "skills/prompt-refactor/scripts/check_contract.py")


class GuidanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "docs").mkdir()
        (self.root / "AGENTS.md").write_text(
            "# Start\n[UI](docs/ui.md#keyboard)\n[external](https://example.com)\n",
            encoding="utf-8",
        )
        (self.root / "docs/ui.md").write_text(
            "# UI\n## Keyboard\nKeep focus.\n### Dialogs\nRestore focus.\n## Layout\nUse tokens.\n",
            encoding="utf-8",
        )

    def test_declared_routes_include_child_sections_and_repeated_reads(self):
        route = {
            "name": "ui",
            "reads": [{"path": "AGENTS.md"}, {"path": "docs/ui.md", "heading": "Keyboard"}, {"path": "AGENTS.md"}],
        }
        result = guidance.check(self.root, {"files": ["AGENTS.md"], "routes": [route]})
        self.assertEqual(result["errors"], [])
        reads = result["routes"][0]["reads"]
        self.assertEqual(reads[1]["bytes"], len("## Keyboard\nKeep focus.\n### Dialogs\nRestore focus.\n".encode()))
        self.assertEqual(result["routes"][0]["bytes"], sum(read["bytes"] for read in reads))
        self.assertEqual(result["external_urls_unchecked"], ["https://example.com"])

    def test_missing_file_and_missing_anchor_fail(self):
        (self.root / "AGENTS.md").write_text("[gone](missing.md)\n[wrong](docs/ui.md#missing)", encoding="utf-8")
        result = guidance.check(self.root, {"files": ["AGENTS.md"]})
        self.assertEqual(len(result["errors"]), 2)

    def test_fenced_examples_are_not_checked_as_live_links(self):
        text = "# Real\n````md\n[example](missing.md)\n```\n# Fake\n````\n~~~\n[also fake](absent.md)\n~~~\n"
        (self.root / "AGENTS.md").write_text(text, encoding="utf-8")
        result = guidance.check(self.root, {"files": ["AGENTS.md"]})
        self.assertEqual(result["errors"], [])
        self.assertEqual(guidance.anchors(text), {"real"})

    def test_reference_definitions_encoded_paths_and_duplicate_anchors(self):
        (self.root / "docs/with space.md").write_text("# Same\n# Same\n# Same-1\n", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("[guide][g]\n[g]: docs/with%20space.md#same-1-1\n", encoding="utf-8")
        self.assertEqual(guidance.check(self.root, {"files": ["AGENTS.md"]})["errors"], [])

    def test_missing_or_ambiguous_route_heading_fails(self):
        (self.root / "docs/ui.md").write_text("# UI\n## Same\na\n## Same\nb\n", encoding="utf-8")
        for heading in ["Missing", "Same"]:
            with self.subTest(heading=heading):
                result = guidance.check(self.root, {"files": ["AGENTS.md"], "routes": [{"name": "bad", "reads": [{"path": "docs/ui.md", "heading": heading}]}]})
                self.assertTrue(any("exactly once" in error for error in result["errors"]))

    def test_parent_escape_and_symlink_escape_fail(self):
        with tempfile.TemporaryDirectory() as outside:
            private = Path(outside) / "outside.md"
            private.write_text("not project guidance", encoding="utf-8")
            (self.root / "outside.md").symlink_to(private)
            result = guidance.check(self.root, {"files": ["outside.md"]})
            self.assertIn("escapes project root", result["errors"][0])
        with self.assertRaises(ValueError):
            guidance.local_path(self.root, str(self.root / "AGENTS.md"))

    def test_real_alias_passes_broken_alias_and_copy_fail(self):
        alias = self.root / "CLAUDE.md"
        manifest = {"files": ["AGENTS.md"], "aliases": [{"path": "CLAUDE.md", "target": "AGENTS.md"}]}
        alias.symlink_to("AGENTS.md")
        self.assertEqual(guidance.check(self.root, manifest)["errors"], [])
        alias.unlink()
        alias.symlink_to("missing.md")
        self.assertTrue(guidance.check(self.root, manifest)["errors"])
        alias.unlink()
        alias.write_text("copy", encoding="utf-8")
        self.assertTrue(guidance.check(self.root, manifest)["errors"])

    def test_invalid_manifest_shapes_fail(self):
        for manifest in [[], {}, {"files": []}, {"files": ["AGENTS.md"], "routes": "oops"}]:
            with self.subTest(manifest=manifest), self.assertRaises(ValueError):
                guidance.check(self.root, manifest)
        result = guidance.check(self.root, {"files": [None], "routes": [{}], "aliases": [{}]})
        self.assertEqual(len(result["errors"]), 3)


class ContractTests(unittest.TestCase):
    def test_removes_repetition_without_requiring_equal_occurrence_counts(self):
        result = contract.compare("Use tool_a. Use tool_a. Limit 10 MiB.", "Use tool_a; limit 10 MiB.", {"protected": ["tool_a", "10 MiB"]})
        self.assertEqual(result["errors"], [])
        self.assertGreater(result["byte_reduction_percent"], 0)

    def test_missing_baseline_and_missing_rewrite_are_distinct_failures(self):
        result = contract.compare("tool_a 10 MiB", "tool_a", {"protected": ["tool_a", "10 MiB", "imaginary"]})
        self.assertEqual(len(result["errors"]), 3)
        self.assertTrue(any("baseline" in error for error in result["errors"]))
        self.assertTrue(any("rewrite" in error for error in result["errors"]))

    def test_invalid_contracts_fail_instead_of_vacuous_success(self):
        for value in [[], {}, {"protected": []}, {"protected": [""]}, {"protected": [2]}, {"protected": [" "]}, {"protected": ["a", "a"]}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                contract.compare("a", "a", value)

    def test_unicode_counts_utf8_bytes_and_empty_baseline_is_not_a_saving(self):
        result = contract.compare("café café", "café", {"protected": ["café"]})
        self.assertEqual(result["before"], {"bytes": 11, "words": 2})
        self.assertEqual(result["after"], {"bytes": 5, "words": 1})
        empty = contract.compare("", "a", {"protected": ["a"]})
        self.assertIsNone(empty["byte_reduction_percent"])
        self.assertTrue(empty["errors"])

    def test_literal_pass_explicitly_does_not_certify_negation(self):
        result = contract.compare("Never send without approval.", "Send without approval.", {"protected": ["approval"]})
        self.assertEqual(result["errors"], [])
        self.assertIn("semantic equivalence", result["scope"])


class CliTests(unittest.TestCase):
    def run_script(self, relative, *arguments):
        return subprocess.run([sys.executable, str(ROOT / relative), *map(str, arguments)], capture_output=True, text=True)

    def test_missing_input_returns_json_and_failure(self):
        result = self.run_script("skills/prompt-refactor/scripts/check_contract.py", "--before", "/nonexistent/humistack-before", "--after", "/nonexistent/humistack-after", "--contract", "/nonexistent/humistack-contract")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)["errors"])

    def test_guidance_cli_reports_broken_links_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("[missing](gone.md)", encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"files": ["AGENTS.md"]}), encoding="utf-8")
            before = {path.name: path.read_bytes() for path in root.iterdir()}
            result = self.run_script("skills/lean-repo/scripts/check_guidance.py", "--root", root, "--manifest", manifest)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(json.loads(result.stdout)["errors"])
            self.assertEqual(before, {path.name: path.read_bytes() for path in root.iterdir()})


if __name__ == "__main__":
    unittest.main()
