"""Tests für die Abbildungen von Kap. 1 „RStudio“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Namen aus dem Kapitel (Abschnitt 1.6 und die Chunks in 1.6.1, 1.6.2); nur Pakete und Funktionen, die Kap. 1 nennt
ERWARTET_KAP01 = {
    "k01-oekosystem": ["tidyverse", "dplyr", "tidyr", "ggplot2", "readr", "purrr", "tibble", "stringr", "forcats",
                       "lubridate", "mariposa", "read_spss()", "w_mean()", "Funktion", "Paket", "Ökosystem"],
    "k01-regal-werkbank": ["REGAL: INSTALLIERT", "WERKBANK: AKTIV", "tidyverse", "mariposa", "patchwork",
                           'install.packages("tidyverse")', 'install.packages("mariposa")',
                           'install.packages("patchwork")', "library(tidyverse)", "library(mariposa)",
                           "library(patchwork)", "einmal pro Rechner", "einmal pro R-Sitzung"],
    # 1.4.4: Pfad aus dem Chunk getwd-demo, Projekt R-Workshop (Übung 1), Skript aus der Checkliste, absoluter Pfad
    # aus dem Vorsicht-Kasten; der zweite Rechner (Boris, Windows) ist ein Beispiel
    "k01-arbeitsverzeichnis": ['read_spss("ALLBUS2023.sav")',
                               'read_spss("/Users/anna/Documents/R-Workshop/ALLBUS2023.sav")',
                               "RECHNER VON ANNA", "RECHNER VON BORIS", "getwd()",
                               '[1] "/Users/anna/Documents/R-Workshop"', '[1] "C:/Users/boris/Documents/R-Workshop"',
                               "R-Workshop", "R-Workshop.Rproj", "01-erste_schritte.qmd", "ALLBUS2023.sav",
                               "gefunden", "nicht gefunden"],
    # 1.7: ?mean in R 4.5.3 (Kopf, Überschriften, Usage und Examples wörtlich); Begriffe aus dem Satz in 1.7
    "k01-hilfeseite": ["mean {base}", "R Documentation", "Arithmetic Mean", "Description",
                       "Generic function for the (trimmed) arithmetic mean.", "Usage", "mean(x, ...)",
                       "## Default S3 method:", "trim = 0", "na.rm = FALSE", "Arguments", "na.rm", "trim",
                       "Value, References, See Also", "Examples", "x <- c(0:10, 50)", "xm <- mean(x)",
                       "c(xm, mean(x, trim = 0.10))", "Funktionsbeschreibung", "Default-Werte", "Argumente",
                       "Beispiele"],
    # 1.4: die vier Bereiche mit dem Beispiel aus 1.5.2 (Chunk mit var1 im Quarto-Dokument 01-erste_schritte.qmd aus
    # der Checkliste nach 1.7); Reiternamen wie in RStudio 2026.01, Zwecke wie in der Tabelle in 1.4
    "k01-oberflaeche": ["RStudio", "R-Workshop", "Code schreiben und speichern", "Code ausprobieren, Output ansehen",
                        "Objekte und Befehlsverlauf", "Dateien, Grafiken, Pakete, Hilfe", "01-erste_schritte.qmd", "Run", "```{r}", "```",
                        "var1 <- 2 + 3", "Console", "Terminal", "Background Jobs", "> var1 <- 2 + 3", "> var1",
                        "[1] 5", "Environment", "History", "Connections", "Tutorial", "Global Environment", "Values",
                        "Files", "Plots", "Packages", "Help", "Viewer", "Home > Documents > R-Workshop",
                        "ALLBUS2023.sav", "R-Workshop.Rproj"],
}


# Englische Fassung: gleiche Schlüssel; Code, Paket- und Funktionsnamen und RStudio-Wörter bleiben
ERWARTET_KAP01_EN = {
    "k01-oekosystem": ["tidyverse", "dplyr", "tidyr", "ggplot2", "readr", "purrr", "tibble", "stringr", "forcats",
                       "lubridate", "mariposa", "read_spss()", "w_mean()", "Function", "Package", "Ecosystem",
                       "data manipulation and visualisation", "statistical analysis"],
    "k01-regal-werkbank": ["SHELF: INSTALLED", "WORKBENCH: ACTIVE", "tidyverse", "mariposa", "patchwork",
                           'install.packages("tidyverse")', 'install.packages("mariposa")',
                           'install.packages("patchwork")', "library(tidyverse)", "library(mariposa)",
                           "library(patchwork)", "once per computer", "once per R session"],
    "k01-arbeitsverzeichnis": ['read_spss("ALLBUS2023.sav")',
                               'read_spss("/Users/anna/Documents/R-Workshop/ALLBUS2023.sav")',
                               "ANNA\u2019S COMPUTER", "BORIS\u2019S COMPUTER", "getwd()",
                               '[1] "/Users/anna/Documents/R-Workshop"', '[1] "C:/Users/boris/Documents/R-Workshop"',
                               "R-Workshop", "R-Workshop.Rproj", "01-first_steps.qmd", "ALLBUS2023.sav",
                               "found", "not found"],
    "k01-hilfeseite": ["mean {base}", "R Documentation", "Arithmetic Mean", "Description",
                       "Generic function for the (trimmed) arithmetic mean.", "Usage", "mean(x, ...)",
                       "## Default S3 method:", "trim = 0", "na.rm = FALSE", "Arguments", "na.rm", "trim",
                       "Value, References, See Also", "Examples", "x <- c(0:10, 50)", "xm <- mean(x)",
                       "c(xm, mean(x, trim = 0.10))", "function description", "default values", "arguments",
                       "examples"],
    "k01-oberflaeche": ["RStudio", "R-Workshop", "Write and save code", "Try out code, view output",
                        "Objects and command history", "Files, plots, packages, help", "01-first_steps.qmd", "Run",
                        "```{r}", "```", "var1 <- 2 + 3", "Console", "Terminal", "Background Jobs",
                        "> var1 <- 2 + 3", "> var1", "[1] 5", "Environment", "History", "Connections", "Tutorial",
                        "Global Environment", "Values", "Files", "Plots", "Packages", "Help", "Viewer",
                        "Home > Documents > R-Workshop", "ALLBUS2023.sav", "R-Workshop.Rproj"],
}


def text_elemente(svg):
    """(Text, x, y) je <text>, in Zoll."""
    from lego import DPI
    return [("".join(e.itertext()), float(e.get("x")) / DPI, float(e.get("y")) / DPI)
            for e in ET.fromstring(svg).iter(NS + "text")]


class TestKap01(unittest.TestCase):
    def test_kap01_constraints(self):
        import kap01
        self.assertEqual(set(kap01.FIGUREN), set(ERWARTET_KAP01))
        for name, fn in kap01.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP01[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")
            if name == "k01-oberflaeche":                                  # Reitername in RStudio, wie im Text
                texte = texte.replace("\nPackages\n", "\n")
            self.assertNotIn("Package", texte, f"{name}: Fachbegriff im Buch ist „Paket“")

    def test_arbeitsverzeichnis_ergebnisse(self):
        """Der Dateiname findet die Datei auf beiden Rechnern, der absolute Pfad nur bei Anna (links)."""
        import kap01
        s = kap01.arbeitsverzeichnis()
        els = text_elemente(s.svg())
        mitte = s.w / 2
        gefunden = [x for t, x, y in els if t == "gefunden"]
        nicht = [x for t, x, y in els if t == "nicht gefunden"]
        self.assertEqual(len(gefunden), 3)
        self.assertEqual(len(nicht), 1)
        self.assertEqual(sum(1 for x in gefunden if x < mitte), 2)          # Anna: beide Zeilen
        self.assertGreater(nicht[0], mitte)                               # Boris: der absolute Pfad
        anna = [x for t, x, y in els if t == "RECHNER VON ANNA"][0]
        boris = [x for t, x, y in els if t == "RECHNER VON BORIS"][0]
        self.assertLess(anna, mitte)
        self.assertGreater(boris, mitte)

    def test_hilfeseite_reihenfolge(self):
        """Abschnitte in der Reihenfolge der Hilfeseite; jede Beschriftung steht auf Höhe ihres Abschnitts."""
        import kap01
        els = text_elemente(kap01.hilfeseite().svg())
        y = {t: yy for t, x, yy in els}
        reihe = ["Arithmetic Mean", "Description", "Usage", "Arguments", "Value, References, See Also", "Examples"]
        self.assertEqual(sorted(reihe, key=y.get), reihe)
        for abschnitt, wort in [("Description", "Funktionsbeschreibung"), ("Usage", "Default-Werte"),
                                ("Arguments", "Argumente"), ("Examples", "Beispiele")]:
            self.assertLess(abs(y[abschnitt] - y[wort]), 0.1, wort)

    def test_oberflaeche_quadranten(self):
        """Editor oben links, Konsole unten links, Environment oben rechts, Files unten rechts (wie in 1.4)."""
        import kap01
        s = kap01.oberflaeche()
        els = text_elemente(s.svg())
        pos = {t: (x, y) for t, x, y in els}
        mx, my = s.w / 2, s.h / 2
        self.assertLess(pos["Code schreiben und speichern"][0], mx)
        self.assertLess(pos["Code schreiben und speichern"][1], my)
        self.assertLess(pos["Code ausprobieren, Output ansehen"][0], mx)
        self.assertGreater(pos["Code ausprobieren, Output ansehen"][1], my)
        self.assertGreater(pos["Objekte und Befehlsverlauf"][0], mx)
        self.assertLess(pos["Objekte und Befehlsverlauf"][1], my)
        self.assertGreater(pos["Dateien, Grafiken, Pakete, Hilfe"][0], mx)
        self.assertGreater(pos["Dateien, Grafiken, Pakete, Hilfe"][1], my)
        # jede Nummer steht links neben ihrer Überschrift, auf derselben Höhe
        for n, titel in enumerate(["Code schreiben und speichern", "Code ausprobieren, Output ansehen",
                                   "Objekte und Befehlsverlauf", "Dateien, Grafiken, Pakete, Hilfe"], start=1):
            nah = [(x, y) for t, x, y in els if t == str(n)
                   and 0 < pos[titel][0] - x < 0.5 and abs(pos[titel][1] - y) < 0.1]
            self.assertEqual(len(nah), 1, titel)

    def test_oberflaeche_ergebnis_zweimal(self):
        """[1] 5 steht im Editor unter dem Chunk (oben links) und in der Konsole (unten links)."""
        import kap01
        s = kap01.oberflaeche()
        els = text_elemente(s.svg())
        treffer = sorted((y, x) for t, x, y in els if t == "[1] 5")
        self.assertEqual(len(treffer), 2)
        self.assertTrue(all(x < s.w / 2 for y, x in treffer))
        grenze = kap01.BEREICHE[1][1] + kap01.BEREICHE[1][3]              # Unterkante des Editors
        self.assertLess(treffer[0][0], grenze)
        self.assertGreater(treffer[1][0], grenze)
        ende = [y for t, x, y in els if t == "```" and x < s.w / 2]
        self.assertTrue(ende and treffer[0][0] > max(ende), "Ergebnis unter dem Chunk")

    def test_oberflaeche_reiter_im_bereich(self):
        """Die Reiter jedes Bereichs passen in seine Breite."""
        import kap01
        for n, (x, w, reiter) in kap01.reiterzeilen().items():
            self.assertLessEqual(reiter, x + w - 0.08, f"Bereich {n}")


class TestKap01Englisch(unittest.TestCase):
    def tearDown(self):
        import sprache
        sprache.setze("de")

    def test_schluessel_gleich(self):
        self.assertEqual(set(ERWARTET_KAP01_EN), set(ERWARTET_KAP01))

    def test_englische_texte(self):
        import kap01
        import sprache
        sprache.setze("en")
        for name, fn in kap01.FIGUREN.items():
            texte = alle_texte(fn().svg())
            for wert in ERWARTET_KAP01_EN[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_kein_deutscher_rest(self):
        import check_en
        import kap01
        import sprache
        sprache.setze("en")
        for name, fn in kap01.FIGUREN.items():
            self.assertEqual(check_en.deutsch_reste(alle_texte(fn().svg())), [], name)

    def test_deutsch_unveraendert(self):
        import kap01
        import sprache
        sprache.setze("en")
        en_texte = alle_texte(kap01.oekosystem().svg())
        sprache.setze("de")
        self.assertIn("Ökosystem", alle_texte(kap01.oekosystem().svg()))
        self.assertNotIn("Ökosystem", en_texte)

    def test_englisch_arbeitsverzeichnis_und_oberflaeche(self):
        """Dieselben Prüfungen wie im Deutschen, mit englischen Wörtern; Reiter passen in die Breite."""
        import kap01
        import sprache
        sprache.setze("en")
        els = text_elemente(kap01.arbeitsverzeichnis().svg())
        self.assertEqual(len([1 for t, x, y in els if t == "found"]), 3)
        self.assertEqual(len([1 for t, x, y in els if t == "not found"]), 1)
        for n, (x, w, ende) in kap01.reiterzeilen().items():
            self.assertLessEqual(ende, x + w - 0.08, f"Bereich {n}")
        s = kap01.oberflaeche()
        pos = {t: (x, y) for t, x, y in text_elemente(s.svg())}
        self.assertLess(pos["Write and save code"][1], s.h / 2)
        self.assertGreater(pos["Try out code, view output"][1], s.h / 2)


if __name__ == "__main__":
    unittest.main()
