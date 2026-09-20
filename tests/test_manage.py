import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

        atcoder = manage.parse_problem_url(
            "https://atcoder.jp/contests/abc350/tasks/abc350_c", {}
        )
        self.assertEqual(atcoder["platform_meta"]["task_id"], "abc350_c")

    def test_atcoder_display_rating(self):
        self.assertEqual(manage.display_atcoder_rating(800), 800)
        self.assertEqual(manage.display_atcoder_rating(0), 147)

    def test_atcoder_rating_is_fetched_once_and_normalized(self):
        first = manage.parse_problem_url(
            "https://atcoder.jp/contests/abc350/tasks/abc350_c", {}
        )
        second = manage.parse_problem_url(
            "https://atcoder.jp/contests/abc350/tasks/abc350_d", {}
        )
        models = {
            "abc350_c": {"difficulty": 799.6},
            "abc350_d": {"difficulty": 0},
        }
        with mock.patch.object(manage, "_ATCODER_MODELS_CACHE", None), mock.patch.object(
            manage, "http_json", return_value=models
        ) as request:
            first.update(manage.fetch_atcoder_metadata(first))
            second.update(manage.fetch_atcoder_metadata(second))

        self.assertEqual(request.call_count, 1)
        self.assertEqual(manage.problem_rating(first), 800)
        self.assertEqual(manage.problem_rating(second), 147)
        self.assertEqual(first["platform_meta"]["rating_source"], "atcoder-problems")

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
        self.assertIn("| Div.2 · A | CF 1400 |", readme)
        self.assertNotIn("solutions/", readme)

        payload = json.loads((self.root / "docs/data/problems.json").read_text(encoding="utf-8"))
        problem = payload["problems"][0]
        self.assertEqual(problem["primary_topic"], "multiple-knapsack")
        self.assertEqual(problem["level_label"], "Div.2 · A")
        self.assertEqual(problem["rating"], 1400)
        self.assertEqual(problem["rating_system"], "codeforces")
        self.assertEqual(problem["rating_label"], "CF 1400")
        self.assertEqual(problem["rating_source"], "manual")
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

    def test_existing_rating_survives_a_later_offline_attempt(self):
        first_daily = self.root / "daily/2026-09-19"
        first_daily.mkdir(parents=True)
        (first_daily / "first.py").write_text(
            """# @url https://atcoder.jp/contests/abc350/tasks/abc350_c
# @primary simulation
# @rating 800
print('first')
""",
            encoding="utf-8",
        )
        manage.process_daily(self.root, "2026-09-19", fetch=False)

        second_daily = self.root / "daily/2026-09-20"
        second_daily.mkdir(parents=True)
        (second_daily / "second.py").write_text(
            """# @url https://atcoder.jp/contests/abc350/tasks/abc350_c
# @primary simulation
print('second')
""",
            encoding="utf-8",
        )
        manage.process_daily(self.root, "2026-09-20", fetch=False)

        database = json.loads((self.root / "data/problems.json").read_text(encoding="utf-8"))
        problem = database["problems"][0]
        self.assertEqual(problem["platform_meta"]["difficulty_rating"], 800)
        self.assertEqual(problem["platform_meta"]["rating_source"], "manual")

    def test_same_topic_same_day_never_overwrites_solutions(self):
        daily = self.root / "daily/2026-09-20"
        daily.mkdir(parents=True)
        sources = {
            "a.cpp": "https://codeforces.com/contest/1900/problem/A",
            "b.cpp": "https://codeforces.com/contest/1900/problem/B",
            "a-again.cpp": "https://codeforces.com/contest/1900/problem/A",
        }
        for filename, url in sources.items():
            (daily / filename).write_text(
                f"""/*
@url {url}
@primary simulation
*/
int main() {{ return 0; }}
""",
                encoding="utf-8",
            )

        count, warnings = manage.process_daily(self.root, "2026-09-20", fetch=False)
        self.assertEqual(count, 3)
        self.assertEqual(warnings, [])

        topic_dir = self.root / "solutions/fundamentals/simulation"
        self.assertTrue((topic_dir / "codeforces-1900A/2026-09-20.cpp").is_file())
        self.assertTrue((topic_dir / "codeforces-1900A/2026-09-20-2.cpp").is_file())
        self.assertTrue((topic_dir / "codeforces-1900B/2026-09-20.cpp").is_file())

        database = json.loads((self.root / "data/problems.json").read_text(encoding="utf-8"))
        self.assertEqual(len(database["problems"]), 2)
        attempts = {problem["id"]: len(problem["attempts"]) for problem in database["problems"]}
        self.assertEqual(attempts["codeforces:1900:A"], 2)
        self.assertEqual(attempts["codeforces:1900:B"], 1)

if __name__ == "__main__":
    unittest.main()
