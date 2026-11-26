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


def zelle(code, out):
    return ("::: {.cell layout-align=\"center\"}\n\n```{.r .cell-code}\n" + code + "\n```\n\n"
            "::: {.cell-output .cell-output-stdout}\n\n```\n" + out + "\n```\n\n:::\n:::\n")


class TestVierBackticks(unittest.TestCase):
    def test_ueberschrift_im_vier_backtick_block_zaehlt_nicht(self):
        qmd = "## A\n\n````markdown\n```{r}\n1\n```\n## B\n````\n\n## C\n"
        self.assertEqual(check_en.aufbau(qmd)["h2"], 2)

    def test_chunk_im_vier_backtick_block_zaehlt_nicht(self):
        qmd = "````markdown\n```{r demo}\n1\n```\n````\n\n```{r echt}\n1\n```\n"
        a = check_en.aufbau(qmd)
        self.assertEqual(a["chunks"], 1)
        self.assertEqual(a["ids"], {"echt"})

    def test_ohne_code_nach_dem_block(self):
        qmd = "````\n```{r}\n````\ntext\n"
        self.assertEqual(check_en.ohne_code(qmd), [(4, "text")])


class TestCodeReste(unittest.TestCase):
    def test_deutscher_kommentar(self):
        qmd = "```{r}\nx <- 1  # Mittelwert\n```\n"
        m = check_en.code_reste(qmd)
        self.assertEqual(len(m), 1)
        self.assertIn("Zeile 2", m[0])

    def test_deutsche_zeichenkette_und_option(self):
        qmd = "```{r}\n#| fig-cap: \"Die Verteilung\"\nplot(x, main = \"Größe\")\n```\n"
        self.assertEqual(len(check_en.code_reste(qmd)), 2)

    def test_reiner_code_unberuehrt(self):
        qmd = "```{r}\nmittelwert <- mean(groesse)\nder <- 1\n```\n"
        self.assertEqual(check_en.code_reste(qmd), [])

    def test_hash_in_zeichenkette_ist_kein_kommentar(self):
        qmd = "```{r}\nx <- \"a # und b\"\ny <- 1 # fine\n```\n"
        self.assertEqual(len(check_en.code_reste(qmd)), 1)

    def test_text_ausserhalb_von_chunks_ignoriert(self):
        self.assertEqual(check_en.code_reste("Der Text # und\n```bash\n# Mittelwert\n```\n"), [])


class TestAusgabeReste(unittest.TestCase):
    def test_label_wort(self):
        m = check_en.ausgabe_reste(ausgabe("1 KEINE ANGABE 5"))
        self.assertEqual(len(m), 1)

    def test_umlaut(self):
        self.assertEqual(len(check_en.ausgabe_reste(ausgabe("Größe"))), 1)

    def test_englisch_sauber_und_nur_ausgaben(self):
        self.assertEqual(check_en.ausgabe_reste(ausgabe("1 NO ANSWER 5")), [])
        self.assertEqual(check_en.ausgabe_reste("Text mit MANN\n"), [])

    def test_mehrere_label_woerter(self):
        for w in ["STIMME", "WEISS NICHT", "TNZ", "MANN", "FRAU", "DATENFEHLER"]:
            self.assertEqual(len(check_en.ausgabe_reste(ausgabe(f"2 {w}"))), 1, w)


class TestMechanik(unittest.TestCase):
    KOPF = "---\noutput-file: x.html\n---\n"

    def test_sauber(self):
        qmd = self.KOPF + "```{r}\nsource(\"R/_common_en.R\")\n```\n![a](Bilder/figuren/en/k04-a.svg)\n"
        self.assertEqual(check_en.mechanik(qmd), [])

    def test_deutsche_quelle(self):
        qmd = self.KOPF + "```{r}\nsource(\"R/_common.R\")\nsource(\"R/prep.R\")\n```\n"
        self.assertEqual(len(check_en.mechanik(qmd)), 2)

    def test_abbildungspfad_ohne_en(self):
        qmd = self.KOPF + "![a](Bilder/figuren/k04-a.svg)\n"
        m = check_en.mechanik(qmd)
        self.assertEqual(len(m), 1)
        self.assertIn("k04-a.svg", m[0])

    def test_output_file_fehlt(self):
        self.assertEqual(len(check_en.mechanik("## A\n")), 1)


class TestZellen(unittest.TestCase):
    def test_meldung_nennt_erste_codezeile(self):
        de = check_en.ausgabe_zahlen(zelle("mean(x)", "[1] 5"))
        en_md = zelle("mean(x)", "[1] 6")
        en = check_en.ausgabe_zahlen(en_md)
        m = check_en.vergleiche_zahlen(de, en, check_en.ausgabe_codes(en_md))
        self.assertEqual(len(m), 1)
        self.assertIn("mean(x)", m[0])

    def test_codes_je_block(self):
        md = zelle("a <- 1\nb", "1") + zelle("sum(y)", "2")
        self.assertEqual(check_en.ausgabe_codes(md), ["a <- 1", "sum(y)"])

    def test_verschiedene_blockzahl_nur_eine_meldung(self):
        de = check_en.ausgabe_zahlen(zelle("a", "1") + zelle("b", "2"))
        en = check_en.ausgabe_zahlen(zelle("a", "9"))
        self.assertEqual(len(check_en.vergleiche_zahlen(de, en)), 1)


class TestErwartet(unittest.TestCase):
    def _wurzel(self, d, en_text):
        with open(os.path.join(d, "x.qmd"), "w", encoding="utf-8") as f:
            f.write("---\noutput-file: x.html\n---\n## A\n")
        with open(os.path.join(d, "x.en.qmd"), "w", encoding="utf-8") as f:
            f.write(en_text)

    def test_erwartete_meldung_gibt_exit_0(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            self._wurzel(d, "---\noutput-file: x.html\n---\n## A\n\nDie Daten und der Code\n")
            self.assertEqual(check_en.main(["x"], root=d, erwartet={}), 1)
            erw = {"x": [("Deutscher Rest", "bekannt")]}
            self.assertEqual(check_en.main(["x"], root=d, erwartet=erw), 0)

    def test_nur_passende_werden_ausgenommen(self):
        offen, bekannt = check_en.filtere("x", ["x: a eins", "x: b zwei"], {"x": [("eins", "r")]})
        self.assertEqual(offen, ["x: b zwei"])
        self.assertEqual(bekannt, [("x: a eins", "r")])

    def test_erwartet_en_eintraege_fuer_04(self):
        import erwartet_en
        self.assertEqual(len(erwartet_en.ERWARTET["04-Datenimport"]), 4)


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
