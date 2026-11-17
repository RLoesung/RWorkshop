"""Tests für die Zeichenbibliothek der Bausteine-Abbildungen (BILDER.md)."""
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lego as L  # noqa: E402

NS = "{http://www.w3.org/2000/svg}"


def alle_elemente(svg):
    return list(ET.fromstring(svg).iter())


class TestCanvas(unittest.TestCase):
    def test_svg_wellformed(self):
        s = L.Canvas(4, 2)
        L.text(s, 0.1, 0.1, 2, 0.5, [L.P(L.R("Text", size=12)), L.P(L.R("zweite Zeile", size=11, italic=True))])
        L.rect(s, 0, 0, 1, 1, L.WHITE, L.CARDLINE, dash=True)
        L.card(s, 0, 0, 1, 1)
        L.eyebrow(s, 0, 0, 2, "ÜBERSCHRIFT")
        L.label_box(s, 0, 0, 1, 0.3, "<-", L.ORANGE)
        L.tok(s, 0, 0, "mean", "fun")
        L.tokens(s, 0, 0, [("zahlen", "obj"), ("|>", "sym"), ("round", "fun"), ("digits", "arg")])
        L.stein(s, 0, 1, 0.8, 0.3, "num", "5", tag="MANN")
        L.schild(s, 0, 0, "zahlen")
        L.turm(s, 2, 1.8, 0.8, 0.25, "txt", ["Anna", "Boris"])
        L.arrow(s, 0, 0)
        L.down_arrow(s, 0, 0)
        L.connector(s, 0, 0, 1, 1, dash=True)
        L.vline(s, 1, 0, 1)
        L.outline(s, 0, 0, 1, 1)
        L.chip(s, 0, 0, "sum()")
        L.numdot(s, 0, 0, 1)
        L.codebox(s, 0, 0, 3, ["x <- 1", "x", "[1] 1", "# Kommentar"], size=11)
        ET.fromstring(s.svg())

    def test_viewbox(self):
        self.assertIn('viewBox="0 0 768 288"', L.Canvas(8, 3).svg())

    def test_min_font(self):
        s = L.Canvas(2, 1)
        L.text(s, 0, 0, 1, 1, [L.P(L.R("x", size=9))])
        with self.assertRaises(ValueError):
            s.svg()


class TestBausteine(unittest.TestCase):
    def test_stein_colors(self):
        s = L.Canvas(2, 1)
        L.stein(s, 0.2, 0.3, 1, 0.4, "num", "5")
        els = alle_elemente(s.svg())
        fills = [e.get("fill") for e in els if e.tag == NS + "rect"]
        self.assertIn("#85B7EB", fills)
        texte = [e for e in els if e.tag in (NS + "text", NS + "tspan") and (e.text or "").strip() == "5"]
        self.assertTrue(texte)
        self.assertTrue(any(e.get("fill") == "#042C53" for e in texte))

        s = L.Canvas(2, 1)
        L.stein(s, 0.2, 0.3, 1, 0.4, "na", "")
        self.assertIn("stroke-dasharray", s.svg())

    def test_stein_tag_laesst_wert_frei(self):
        s = L.Canvas(2, 1)
        L.stein(s, 0.2, 0.3, 1.2, 0.4, "num", "1", tag="MANN")
        els = alle_elemente(s.svg())
        wert = [e for e in els if e.tag == NS + "text" and "".join(e.itertext()).strip() == "1"][0]
        sticker = [e for e in els if e.tag == NS + "rect" and e.get("fill") == L.STICKER][0]
        mitte = float(wert.get("x")) / L.DPI
        rechts = mitte + L.text_width("1", L.MONO, 13, True) / 2
        self.assertLessEqual(rechts, float(sticker.get("x")) / L.DPI)

    def test_turm_order(self):
        s = L.Canvas(2, 2.2)
        L.turm(s, 0, 2, 1, 0.3, "num", ["a", "b"])
        y = {}
        for e in alle_elemente(s.svg()):
            if e.tag in (NS + "text", NS + "tspan") and (e.text or "").strip() in ("a", "b"):
                yy = e.get("y") or e.get("data-y")
                if yy is not None:
                    y[e.text.strip()] = float(yy)
        self.assertGreater(y["a"], y["b"])


class TestText(unittest.TestCase):
    def test_text_wraps(self):
        s = L.Canvas(4, 3)
        satz = ("Ein Vektor ist eine Sammlung von Werten desselben Datentyps, "
                "und jeder Wert steht als eigener Stein im Turm, ") * 2
        satz = satz[:200]
        L.text(s, 0.2, 0.2, 3, 2.5, [L.P(L.R(satz, size=12))])
        zeilen = [e for e in alle_elemente(s.svg()) if e.tag == NS + "text"]
        self.assertGreater(len(zeilen), 1)
        for z in zeilen:
            inhalt = "".join(z.itertext())
            self.assertLessEqual(L.text_width(inhalt, L.SANS, 12), 3.0 + 1e-6, inhalt)

    def test_text_fits_fallback(self):
        try:
            from PIL import ImageFont
        except ImportError:
            self.skipTest("PIL fehlt")
        kandidaten = {
            L.SANS: ["/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/SFNS.ttf"],
            L.MONO: [("/System/Library/Fonts/Menlo.ttc", 0)],
        }
        proben = ["Mittelwert", "Wertelabels", "WWWWW", "iiiii", "Bauplatte mit Türmen", "round(digits = 1)"]
        geprueft = 0
        for font, pfade in kandidaten.items():
            for p in pfade:
                pfad, idx = (p if isinstance(p, tuple) else (p, 0))
                if not os.path.exists(pfad):
                    continue
                f = ImageFont.truetype(pfad, 1000, index=idx)
                for t in proben:
                    gemessen = f.getlength(t) / 1000 * 12 / 72      # Zoll bei 12 pt
                    self.assertGreaterEqual(L.text_width(t, font, 12), gemessen, (pfad, t))
                    geprueft += 1
        if not geprueft:
            self.skipTest("keine Vergleichsschriften gefunden")


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


ERWARTET_KAP03 = {
    "k03-legende": ["numeric", "character", "logical", "NA", "Name", "Objekt", "Funktion", "Argument"],
    "k03-turm": ["zahlen", "namen", "flags", '"Anna"', '"Boris"', '"Carla"', "TRUE", "FALSE", "NA", "5"],
    "k03-rangfolge": ["c(1, TRUE, FALSE)", 'c(1, "Anna", TRUE)', "[1] 1 1 0", '[1] "1" "Anna" "TRUE"',
                      "logical", "numeric", "character"],
    "k03-tibble": ["befragte", "geschlecht", "alter", "<fct>", "<dbl>", "Divers", "52", "[1] 34 41 28 52"],
    "k03-pipe": ["zahlen", "1.11", "1.55", "round(", "digits = 1)", "head(", "n = 3)", "1.6", "1.3"],
    "k03-name-inhalt": ["var1", "<-", "2 * 4", "8", "[1] 8", "ENVIRONMENT", "Name", "Ausdruck"],
    "k03-reihenfolge": ["x <- 5", "y <- x + 2", "x <- 10", "[1] 7", "NACH ZEILE 1", "NACH ZEILE 3",
                        "x", "y", "5", "7", "10"],
    "k03-funktion": ["seq", "from", "to", "by", "from = 1", "to = 10", "by = 2", "[1] 1 3 5 7 9",
                     "1", "3", "5", "7", "9", "10", "2", "Funktion", "Argumente"],
    "k03-argumente": ["round()", "x", "digits", "1.222", "2.345", "3.987", "1.2", "2.3", "4.0", "1",
                      "round(c(1.222, 2.345, 3.987), digits = 1)", "[1] 1.2 2.3 4.0", "Pflichtfeld",
                      "vorausgefüllt mit 0"],
    "k03-na": ["x", "1", "2", "NA", "4", "5", "mean", "na.rm = TRUE", "[1] NA", "[1] 3"],
    "k03-analyseplan": ['allbus <- read_spss("ALLBUS2023.sav") |>', '  rec(mm02, rules = "rev", suffix = "r") |>',
                        '  rec(mm05, rules = "rev", suffix = "r") |>', "  mutate(",
                        "    islamophobie = row_means(pick(mm01, mm02r, mm03, mm04, mm05r, mm06),",
                        "min_valid = 5)", "Datensatz einlesen", "mm02", "mm05", "umpolen", "Skala bilden"],
}


class TestKap03(unittest.TestCase):
    def test_kap03_constraints(self):
        import kap03
        self.assertEqual(set(kap03.FIGUREN), set(ERWARTET_KAP03))
        for name, fn in kap03.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP03[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")


if __name__ == "__main__":
    unittest.main()
