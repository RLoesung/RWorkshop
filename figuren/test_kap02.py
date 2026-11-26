"""Tests für die Abbildungen von Kap. 2 „Quarto“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Das erste .qmd aus 2.4 (Zeile für Zeile) und seine gerenderte Ausgabe; mean(c(1, 2, 3, 4, 5)) ergibt [1] 3
ERWARTET_KAP02 = {
    "k02-qmd-schichten": ["---", 'title: "Mein erster Bericht"', 'author: "Anna Schmidt"', "format: html",
                          "## Einleitung", "In diesem Bericht analysiere ich den ALLBUS 2023.", "```{r}",
                          "mean(c(1, 2, 3, 4, 5))", "```", "YAML-Header", "Markdown-Lauftext", "Code-Chunk",
                          "Render", "Mein erster Bericht", "Anna Schmidt", "Einleitung", "[1] 3"],
    # 2.6: Chunk mein-chunk mit mean(mtcars$mpg); Ausgabe in R 4.5.3 [1] 20.09062, Verhalten mit quarto render geprüft
    "k02-chunk-optionen": ["OPTION", "IM BERICHT", "AUSGEFÜHRT", "ohne Option", "echo=FALSE", "eval=FALSE",
                           "include=FALSE", "mean(mtcars$mpg)", "[1] 20.09062", "ja", "nein"],
    # 2.6.1: Setup-Chunk wörtlich; Werkbank wie in 1.6.2
    "k02-render-sitzung": ["NEUE R-SITZUNG", "NACH DEM SETUP-CHUNK", "WERKBANK", "ENVIRONMENT", "nur base R",
                           "leer", "tidyverse", "mariposa", "allbus", "```{r setup, include=FALSE}",
                           "library(tidyverse)", "library(mariposa)", 'allbus <- read_spss("ALLBUS2023.sav")'],
    # 2.9: Verweise aus dem Beispiel; Ausgabe von quarto render 1.8.25 (Standardstil, lang: de)
    "k02-zitieren": ["literatur.bib", "@article{Goodman2016,", "@book{Wickham2023,", "analyse.qmd",
                     "Wie @Goodman2016 zeigt, lässt sich Reproduzierbarkeit unterschiedlich definieren.",
                     "Für eine ausführliche Behandlung siehe auch [@Wickham2023].", "Render", "Literatur"],
}

# Englische Fassung: gleiche Schlüssel; set_na() im Setup-Chunk, drei Autoren bei R for Data Science
ERWARTET_KAP02_EN = {
    "k02-qmd-schichten": ["---", 'title: "My first report"', 'author: "Anna Schmidt"', "format: html",
                          "## Introduction", "In this report I analyse the ALLBUS 2023.", "```{r}",
                          "mean(c(1, 2, 3, 4, 5))", "```", "YAML header", "Markdown text", "Code chunk",
                          "Render", "My first report", "Anna Schmidt", "Introduction", "[1] 3"],
    "k02-chunk-optionen": ["OPTION", "IN THE REPORT", "EXECUTED", "no option", "echo=FALSE", "eval=FALSE",
                           "include=FALSE", "mean(mtcars$mpg)", "[1] 20.09062", "yes", "no"],
    "k02-render-sitzung": ["NEW R SESSION", "AFTER THE SETUP CHUNK", "WORKBENCH", "ENVIRONMENT", "base R only",
                           "empty", "tidyverse", "mariposa", "allbus", "```{r setup, include=FALSE}",
                           "library(tidyverse)", "library(mariposa)", 'allbus <- read_spss("ALLBUS2023.sav")',
                           "  |> set_na(-56, \u2026, -6)"],
    "k02-zitieren": ["references.bib", "@article{Goodman2016,", "@book{Wickham2023,", "analysis.qmd",
                     "As @Goodman2016 show, reproducibility can be defined in different ways.",
                     "For a detailed discussion, see also [@Wickham2023].", "Render", "References"],
}

# gerenderter Text in k02-zitieren, über Zeilenumbrüche hinweg
ZITIERT = ["Wie Goodman, Fanelli, und Ioannidis (2016) zeigt, lässt sich Reproduzierbarkeit unterschiedlich "
           "definieren. Für eine ausführliche Behandlung siehe auch (Wickham, Çetinkaya-Rundel, und Grolemund 2023).",
           "Goodman, Steven N., Daniele Fanelli, und John P. A. Ioannidis. 2016. „What does research "
           "reproducibility mean?“ Science Translational Medicine 8 (341): 341ps12.",
           "Wickham, Hadley, Mine Çetinkaya-Rundel, und Garrett Grolemund. 2023. R for Data Science. 2. Aufl. O’Reilly."]
ZITIERT_EN = ["As Goodman, Fanelli, and Ioannidis (2016) show, reproducibility can be defined in different ways. "
              "For a detailed discussion, see also (Wickham, Çetinkaya-Rundel, and Grolemund 2023).",
              "Goodman, Steven N., Daniele Fanelli, and John P. A. Ioannidis. 2016. “What does research "
              "reproducibility mean?” Science Translational Medicine 8 (341): 341ps12.",
              "Wickham, Hadley, Mine Çetinkaya-Rundel, and Garrett Grolemund. 2023. R for Data Science. 2nd ed. "
              "O’Reilly."]


def text_elemente(svg):
    """(Text, x, y) je <text>, in Zoll."""
    from lego import DPI
    return [("".join(e.itertext()), float(e.get("x")) / DPI, float(e.get("y")) / DPI)
            for e in ET.fromstring(svg).iter(NS + "text")]


class TestKap02(unittest.TestCase):
    def test_kap02_constraints(self):
        import kap02
        self.assertEqual(set(kap02.FIGUREN), set(ERWARTET_KAP02))
        for name, fn in kap02.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP02[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")
            # das Beispiel im Buch hat keinen Inline-Code
            self.assertNotIn("`r ", texte, name)
            self.assertNotIn("Inline", texte, name)

    def test_chunk_optionen_zeilen(self):
        """Je Option: Code und Ausgabe im Bericht, ausgeführt ja/nein (geprüft mit quarto render)."""
        import kap02
        els = text_elemente(kap02.chunk_optionen().svg())
        optionen = ["ohne Option", "echo=FALSE", "eval=FALSE", "include=FALSE"]
        zeile = {t: y for t, x, y in els if t in optionen}
        self.assertEqual(sorted(optionen, key=zeile.get), optionen)

        def wo(t):
            return sorted(min(optionen, key=lambda o: abs(zeile[o] - y)) for tt, x, y in els if tt == t)
        self.assertEqual(wo("mean(mtcars$mpg)"), sorted(["ohne Option", "eval=FALSE"]))
        self.assertEqual(wo("[1] 20.09062"), sorted(["ohne Option", "echo=FALSE"]))
        self.assertEqual(wo("ja"), sorted(["ohne Option", "echo=FALSE", "include=FALSE"]))
        self.assertEqual(wo("nein"), ["eval=FALSE"])

    def test_render_sitzung_vorher_nachher(self):
        """Links die leere Sitzung, rechts nach dem Setup-Chunk: Pakete auf der Werkbank, allbus im Environment."""
        import kap02
        s = kap02.render_sitzung()
        els = text_elemente(s.svg())
        links = [x for t, x, y in els if t == "NEUE R-SITZUNG"][0]
        rechts = [x for t, x, y in els if t == "NACH DEM SETUP-CHUNK"][0]
        self.assertLess(links, rechts)
        mitte = s.w / 2
        for t in ["nur base R", "leer"]:
            self.assertTrue(all(x < mitte for tt, x, y in els if tt == t), t)
        for t in ["tidyverse", "mariposa", "allbus"]:
            xs = [x for tt, x, y in els if tt == t]
            self.assertEqual(len(xs), 1, t)                    # nur nach dem Setup-Chunk, nicht vorher
            self.assertGreater(xs[0], mitte, t)

    def test_zitieren_ausgabe(self):
        import kap02
        import re
        texte = re.sub(r"\s+", " ", " ".join(t for t, x, y in text_elemente(kap02.zitieren().svg())))
        for satz in ZITIERT:
            self.assertIn(satz, texte)

    def test_zitieren_kursiv_ohne_langen_vorlauf(self):
        """Ein kursiver Lauf steht am Zeilenanfang oder nach einem kurzen geraden Lauf. Nach einem langen <tspan>
        setzt WebKit (Safari, macOS-Vorschau) mit der Systemschrift eine zu große Lücke („2023.  R for Data“)."""
        import kap02
        for t in ET.fromstring(kap02.zitieren().svg()).iter(NS + "text"):
            vorher = 0
            for sp in t.iter(NS + "tspan"):
                if sp.get("font-style") == "italic":
                    self.assertLessEqual(vorher, 10, "".join(t.itertext()))
                vorher += len(sp.text or "")


class TestKap02Englisch(unittest.TestCase):
    def tearDown(self):
        import sprache
        sprache.setze("de")

    def test_schluessel_gleich(self):
        self.assertEqual(set(ERWARTET_KAP02_EN), set(ERWARTET_KAP02))

    def test_englische_texte(self):
        import kap02
        import sprache
        sprache.setze("en")
        for name, fn in kap02.FIGUREN.items():
            svg = fn().svg()
            self.assertLessEqual(float(ET.fromstring(svg).get("viewBox").split()[2]), 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP02_EN[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_kein_deutscher_rest(self):
        import check_en
        import kap02
        import sprache
        sprache.setze("en")
        for name, fn in kap02.FIGUREN.items():
            self.assertEqual(check_en.deutsch_reste(alle_texte(fn().svg())), [], name)

    def test_chunk_optionen_englisch(self):
        import kap02
        import sprache
        sprache.setze("en")
        els = text_elemente(kap02.chunk_optionen().svg())
        optionen = ["no option", "echo=FALSE", "eval=FALSE", "include=FALSE"]
        zeile = {t: y for t, x, y in els if t in optionen}
        self.assertEqual(sorted(optionen, key=zeile.get), optionen)
        nein = [y for t, x, y in els if t == "no"]
        self.assertEqual(len(nein), 1)
        self.assertLess(abs(nein[0] - zeile["eval=FALSE"]), 0.5)

    def test_render_sitzung_set_na_im_chunk(self):
        """Die Setup-Zeile steht mit der Pipe und set_na() unter dem Einlesen, innerhalb der Leinwand."""
        import kap02
        import sprache
        sprache.setze("en")
        s = kap02.render_sitzung()
        els = text_elemente(s.svg())
        y_read = [y for t, x, y in els if t == 'allbus <- read_spss("ALLBUS2023.sav")'][0]
        y_na = [y for t, x, y in els if t == "  |> set_na(-56, \u2026, -6)"][0]
        self.assertGreater(y_na, y_read)
        self.assertLess(max(y for t, x, y in els), s.h)

    def test_zitieren_ausgabe_englisch(self):
        import re
        import kap02
        import sprache
        sprache.setze("en")
        texte = re.sub(r"\s+", " ", " ".join(t for t, x, y in text_elemente(kap02.zitieren().svg())))
        for satz in ZITIERT_EN:
            self.assertIn(satz, texte)


if __name__ == "__main__":
    unittest.main()
