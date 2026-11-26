"""Tests für figuren/kapitelkarten.py (deutscher und englischer Pfad)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kapitelkarten  # noqa: E402

DE = "# Eins {#sec-eins}\n\n## Was du nach diesem Kapitel kannst {-}\n\n- Ziel **A**.\n- Ziel `b`.\n- Ziel C.\n\n## Weiter\n"
EN = ("---\nformat: html\n---\n\n# One {#sec-eins}\n\n## What you will be able to do after this chapter {-}\n\n"
      "- Goal **A**.\n- Goal `b`.\n- Goal C.\n\n## Next\n")
INDEX_DE = "# V\n\n## Die Kapitel im Überblick {-}\n\nalt\n\n## Wie liest du dieses Buch? {-}\n\nText\n"
INDEX_EN = "# P\n\n## Overview of the chapters {-}\n\nold\n\n## How to read this book {-}\n\nText\n"


class TestKapitelkarten(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        for n, t in [("01-Eins.qmd", DE), ("01-Eins.en.qmd", EN), ("index.qmd", INDEX_DE), ("index.en.qmd", INDEX_EN)]:
            open(os.path.join(self.root, n), "w", encoding="utf-8").write(t)

    def tearDown(self):
        self.tmp.cleanup()

    def lies(self, n):
        return open(os.path.join(self.root, n), encoding="utf-8").read()

    def test_deutsch_ignoriert_englische_dateien(self):
        kapitelkarten.main(root=self.root)
        t = self.lies("index.qmd")
        self.assertEqual(t.count("kapitel-karte\""), 1)
        self.assertIn('<div class="titel">Eins</div>', t)
        self.assertIn("<li>Ziel <strong>A</strong>.</li><li>Ziel <code>b</code>.</li>", t)
        self.assertNotIn("Ziel C", t)

    def test_deutsch_idempotent(self):
        kapitelkarten.main(root=self.root)
        a = self.lies("index.qmd")
        kapitelkarten.main(root=self.root)
        self.assertEqual(a, self.lies("index.qmd"))

    def test_englisch(self):
        kapitelkarten.main(en=True, root=self.root)
        t = self.lies("index.en.qmd")
        self.assertIn("## Overview of the chapters {-}", t)
        self.assertNotIn("old", t)
        self.assertEqual(t.count('kapitel-karte"'), 1)
        self.assertIn('href="01-Eins.html"', t)
        self.assertIn('<div class="titel">One</div>', t)
        self.assertIn("<li>Goal <strong>A</strong>.</li><li>Goal <code>b</code>.</li>", t)
        self.assertNotIn("Goal C", t)
        self.assertIn("## How to read this book {-}\n\nText", t)
        self.assertEqual(self.lies("index.qmd"), INDEX_DE)

    def test_englisch_idempotent(self):
        kapitelkarten.main(en=True, root=self.root)
        a = self.lies("index.en.qmd")
        kapitelkarten.main(en=True, root=self.root)
        self.assertEqual(a, self.lies("index.en.qmd"))


if __name__ == "__main__":
    unittest.main()
