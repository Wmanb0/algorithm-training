import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import manage


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TaxonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy = manage.Taxonomy(PROJECT_ROOT / "data/taxonomy.yaml")

    def test_nested_dp_path(self):
        topic = self.taxonomy.topics["multiple-knapsack"]
        self.assertEqual(
            topic.path,
            ("dynamic-programming", "knapsack", "multiple-knapsack"),
        )
        self.assertEqual(self.taxonomy.resolve("bounded-knapsack"), "multiple-knapsack")

    def test_parent_group_requires_specific_topic(self):
        with self.assertRaisesRegex(manage.NotebookError, "more specific"):
            self.taxonomy.resolve("dp")


class MetadataTests(unittest.TestCase):
    def test_multiline_note(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "solution.cpp"
            path.write_text(
                """/*
@url https://codeforces.com/contest/1900/problem/A
@primary simulation
@topics greedy-construction
@note
First line.
Second line.
@endnote
*/
int main() {}
""",
                encoding="utf-8",
            )
            metadata = manage.parse_metadata(path)
            self.assertEqual(metadata["primary"], "simulation")
            self.assertEqual(metadata["note"], "First line.\nSecond line.")

    def test_platform_url_parsing(self):
        problem = manage.parse_problem_url(
            "https://codeforces.com/contest/1900/problem/A", {}
        )
        self.assertEqual(problem["id"], "codeforces:1900:A")
        self.assertEqual(problem["platform_meta"]["problem_index"], "A")


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()
        shutil.copy(PROJECT_ROOT / "data/taxonomy.yaml", self.root / "data/taxonomy.yaml")
        (self.root / "data/problems.json").write_text(
            '{"schema_version": 1, "problems": []}\n', encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_processes_and_builds_all_views(self):
        daily = self.root / "daily/2026-09-19"
        daily.mkdir(parents=True)
        source = daily / "solution.cpp"
        source.write_text(
            """/*
@url https://codeforces.com/contest/1900/problem/A
@primary multiple-knapsack
@topics binary-splitting
@rating 1400
@division div2
@note
Split counts into powers of two.
@endnote
*/
#include <bits/stdc++.h>
int main() { return 0; }
""",
            encoding="utf-8",
        )

        count, warnings = manage.process_daily(
            self.root, "2026-09-19", fetch=False
        )
        self.assertEqual(count, 1)
        self.assertEqual(warnings, [])

        destination = (
            self.root
            / "solutions/dynamic-programming/knapsack/multiple-knapsack"
            / "codeforces-1900A/2026-09-19.cpp"
        )
        self.assertTrue(destination.is_file())
        self.assertFalse(source.exists())

        readme = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn("[Codeforces 1900A](https://codeforces.com/contest/1900/problem/A)", readme)
        self.assertIn("Div.2 · 1400 · A", readme)
        self.assertNotIn("solutions/", readme)

        payload = json.loads((self.root / "docs/data/problems.json").read_text(encoding="utf-8"))
        problem = payload["problems"][0]
        self.assertEqual(problem["primary_topic"], "multiple-knapsack")
        self.assertIn("binary-splitting", problem["topics"])
        self.assertIn("Split counts into powers of two.", problem["attempts"][0]["note"])
        self.assertIn("int main()", problem["attempts"][0]["code"])

    def test_unknown_topic_does_not_move_file(self):
        daily = self.root / "daily/2026-09-19"
        daily.mkdir(parents=True)
        source = daily / "bad.py"
        source.write_text(
            """# @url https://leetcode.com/problems/two-sum/
# @primary imaginary-algorithm
print('still here')
""",
            encoding="utf-8",
        )
        with self.assertRaises(manage.NotebookError):
            manage.process_daily(self.root, "2026-09-19", fetch=False)
        self.assertTrue(source.exists())


if __name__ == "__main__":
    unittest.main()

