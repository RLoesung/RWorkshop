"""Tests für das Prüfskript der englischen Fassung (check_en.py)."""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_en


def ausgabe(text):
    return "::: {.cell-output .cell-output-stdout}\n\n```\n" + text + "\n```\n\n:::\n"


class TestAufbau(unittest.TestCase):
    def test_aufbau_zaehlt_ueberschriften_ohne_code(self):
        qmd = "## A\n\n```\n## B\n```\n"
        self.assertEqual(check_en.aufbau(qmd)["h2"], 1)

    def test_aufbau_ids(self):
        qmd = "## X {#sec-x}\n\n```{r foo}\n1 + 1\n```\n"
        self.assertEqual(check_en.aufbau(qmd)["ids"], {"sec-x", "foo"})

    def test_aufbau_kaesten_und_abbildungen(self):
        qmd = ("::: {.callout-note title=\"T\"}\nText\n:::\n\n"
               "::: {.callout-tip}\nText\n:::\n\n![Bild](a.png)\n")
        a = check_en.aufbau(qmd)
        self.assertEqual(a["callout-note"], 1)
        self.assertEqual(a["callout-tip"], 1)
        self.assertEqual(a["abbildungen"], 1)
        self.assertEqual(a["kaesten-mit-titel"], 1)

    def test_vergleich_meldet_fehlenden_kasten(self):
        de = check_en.aufbau("::: {.callout-note}\na\n:::\n\n::: {.callout-note}\nb\n:::\n")
        en = check_en.aufbau("::: {.callout-note}\na\n:::\n")
        meldungen = check_en.vergleiche_aufbau(de, en)
        self.assertEqual(len(meldungen), 1)
        self.assertIn("callout-note", meldungen[0])

    def test_vergleich_meldet_fehlende_id(self):
        de = check_en.aufbau("## X {#sec-x}\n")
        en = check_en.aufbau("## X\n")
        meldungen = check_en.vergleiche_aufbau(de, en)
        self.assertEqual(len(meldungen), 1)
        self.assertIn("sec-x", meldungen[0])


class TestZahlen(unittest.TestCase):
    def test_zahlen_gleich_trotz_labels(self):
        de = check_en.ausgabe_zahlen(ausgabe("MANN 2574 49.1"))
        en = check_en.ausgabe_zahlen(ausgabe("MALE 2574 49.1"))
        self.assertEqual(check_en.vergleiche_zahlen(de, en), [])
        en2 = check_en.ausgabe_zahlen(ausgabe("MALE 2574 49.2"))
        self.assertEqual(len(check_en.vergleiche_zahlen(de, en2)), 1)

    def test_bloecke_in_reihenfolge(self):
        md = ausgabe("[1] 8") + "\ntext 99\n\n" + ausgabe("a 1.5, -2")
        self.assertEqual(check_en.ausgabe_zahlen(md), [["8"], ["1.5", "-2"]])

    def test_anderer_blockanzahl(self):
        de = check_en.ausgabe_zahlen(ausgabe("1") + ausgabe("2"))
        en = check_en.ausgabe_zahlen(ausgabe("1"))
        self.assertEqual(len(check_en.vergleiche_zahlen(de, en)), 1)

    def test_lies_freeze(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "html.json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"hash": "x", "result": {"markdown": "abc"}}, f)
            self.assertEqual(check_en.lies_freeze(p), "abc")


class TestDeutschReste(unittest.TestCase):
    def test_deutsch_reste(self):
        meldungen = check_en.deutsch_reste("The data und the code\n")
        self.assertEqual(len(meldungen), 1)
        self.assertIn("1", meldungen[0])

    def test_inline_code_und_url_ignoriert(self):
        self.assertEqual(check_en.deutsch_reste("Use `und` here.\n"), [])
        self.assertEqual(check_en.deutsch_reste("See https://uni.de/Universität/x now.\n"), [])

    def test_code_block_ignoriert(self):
        self.assertEqual(check_en.deutsch_reste("```\nund Größe\n```\n"), [])

    def test_umlaut(self):
        self.assertEqual(len(check_en.deutsch_reste("Line one\nGröße here\n")), 1)


class TestPruefe(unittest.TestCase):
    def test_fehlende_englische_datei(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "x.qmd"), "w", encoding="utf-8") as f:
                f.write("## A\n")
            self.assertEqual(check_en.pruefe("x", d), ["x: x.en.qmd fehlt"])
            self.assertEqual(check_en.main(["x"], root=d), 1)

    def test_fehlende_deutsche_datei(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(check_en.pruefe("y", d), ["y: y.qmd fehlt"])
            self.assertEqual(check_en.main(["y"], root=d), 1)


if __name__ == "__main__":
    unittest.main()
