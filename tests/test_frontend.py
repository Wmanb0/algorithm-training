import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class LocalAssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "script" and attributes.get("src"):
            self.assets.append(attributes["src"])
        if tag == "link" and attributes.get("href"):
            self.assets.append(attributes["href"])


class FrontendTests(unittest.TestCase):
    def test_all_local_html_assets_exist(self):
        html_path = PROJECT_ROOT / "docs/index.html"
        parser = LocalAssetParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        for reference in parser.assets:
            parsed = urlparse(reference)
            if parsed.scheme in {"data", "http", "https"}:
                continue
            target = (html_path.parent / parsed.path).resolve()
            self.assertTrue(target.is_file(), f"Missing frontend asset: {reference}")

    def test_generated_payloads_are_valid(self):
        for name in ("problems.json", "taxonomy.json"):
            path = PROJECT_ROOT / "docs/data" / name
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version" if name == "problems.json" else "version"], 1)

    def test_rating_controls_and_columns_exist(self):
        html = (PROJECT_ROOT / "docs/index.html").read_text(encoding="utf-8")
        script = (PROJECT_ROOT / "docs/app.js").read_text(encoding="utf-8")
        self.assertIn('id="ratingMin"', html)
        self.assertIn('id="ratingMax"', html)
        self.assertIn('id="ratingFilters" hidden', html)
        self.assertIn("<th>Rating</th>", html)
        self.assertIn('value="rating-desc" hidden disabled', html)
        self.assertIn("function problemRating(problem)", script)
        self.assertIn('selected === "codeforces" || selected === "atcoder"', script)


if __name__ == "__main__":
    unittest.main()
