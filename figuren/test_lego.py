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

    def test_werkbank(self):
        """Werkbank (1.6.2, 2.6.1): Platte mit zwei Beinen, die Paket-Kacheln stehen nebeneinander darauf."""
        s = L.Canvas(4, 2)
        L.werkbank(s, 0.2, 1.2, 3.0, ["tidyverse", "mariposa"])
        els = alle_elemente(s.svg())
        texte = ["".join(e.itertext()) for e in els if e.tag == NS + "text"]
        self.assertEqual(texte, ["tidyverse", "mariposa"])
        rects = [e for e in els if e.tag == NS + "rect"]
        holz = [r for r in rects if r.get("fill") == L.INK]
        self.assertEqual(len(holz), 3)                                    # Platte und zwei Beine
        platte = max(holz, key=lambda r: float(r.get("width")))
        self.assertAlmostEqual(float(platte.get("width")), 3.0 * L.DPI, places=1)
        oben = float(platte.get("y"))
        kacheln = [r for r in rects if r.get("fill") == L.WHITE]
        self.assertEqual(len(kacheln), 2)
        for k in kacheln:
            unten = float(k.get("y")) + float(k.get("height"))
            self.assertLessEqual(unten, oben)
            self.assertGreaterEqual(unten, oben - 0.05 * L.DPI)
            self.assertGreaterEqual(float(k.get("x")), 0.2 * L.DPI)
            self.assertLessEqual(float(k.get("x")) + float(k.get("width")), 3.2 * L.DPI)

    def test_werkbank_leer(self):
        s = L.Canvas(4, 2)
        L.werkbank(s, 0.2, 1.2, 3.0, [])
        els = alle_elemente(s.svg())
        self.assertFalse([e for e in els if e.tag == NS + "text"])
        self.assertEqual(len([e for e in els if e.tag == NS + "rect"]), 3)

    def test_stein_blass(self):
        """Blasser Stein (ein Wert, den R wiederholt): Farbe des Datentyps, aber heller; weder grau noch gestrichelt."""
        def hell(farbe):
            return sum(int(farbe[i:i + 2], 16) for i in (1, 3, 5))

        for kind in ("num", "txt", "log"):
            s = L.Canvas(2, 1)
            L.stein(s, 0.2, 0.3, 1, 0.4, kind, "2", blass=True)
            svg = s.svg()
            self.assertNotIn("stroke-dasharray", svg)
            els = alle_elemente(svg)
            fills = {e.get("fill") for e in els if e.tag == NS + "rect"}
            fuellung, schrift = L.STEIN_BLASS[kind]
            self.assertEqual(fills, {fuellung})                              # Körper und Noppen
            self.assertNotIn(fuellung, (L.STEIN[kind][0], L.STEIN["dim"][0], L.STEIN["na"][0]))
            self.assertGreater(hell(fuellung), hell(L.STEIN[kind][0]))
            kanal = lambda f: max(range(3), key=lambda i: int(f[1 + 2 * i:3 + 2 * i], 16))   # noqa: E731
            self.assertEqual(kanal(fuellung), kanal(L.STEIN[kind][0]))     # gleicher Farbton
            koerper = [e for e in els if e.tag == NS + "rect" and e.get("stroke")]
            self.assertEqual([e.get("stroke") for e in koerper], [L.STEIN[kind][0]])
            wert = [e for e in els if e.tag == NS + "text" and "".join(e.itertext()) == "2"]
            self.assertEqual([e.get("fill") for e in wert], [schrift])

    def test_kiste(self):
        """Kiste mit Fächern (Liste): Fächer nebeneinander in Listenreihenfolge, je mit $-Namen, in einem Rahmen."""
        s = L.Canvas(5, 3)
        faecher = L.kiste(s, 0.2, 0.2, [("a", 1.0), ("bb", 1.5), ("c", 0.8)], h=1.4, name="liste")
        els = alle_elemente(s.svg())
        texte = [e for e in els if e.tag == NS + "text"]
        self.assertEqual(["".join(e.itertext()) for e in texte], ["liste", "$a", "$bb", "$c"])
        self.assertEqual(len(faecher), 3)
        rahmen = [e for e in els if e.tag == NS + "rect" and e.get("fill") == L.CARD and e.get("stroke") == L.INK]
        self.assertEqual(len(rahmen), 1)
        rx, ry = float(rahmen[0].get("x")) / L.DPI, float(rahmen[0].get("y")) / L.DPI
        rw, rh = float(rahmen[0].get("width")) / L.DPI, float(rahmen[0].get("height")) / L.DPI
        self.assertAlmostEqual(rw, 3.3, places=2)
        links = rx
        for (x, oben, b, boden), soll, label in zip(faecher, [1.0, 1.5, 0.8], texte[1:]):
            self.assertAlmostEqual(x, links, places=6)                     # lückenlos nebeneinander
            self.assertAlmostEqual(b, soll, places=6)
            self.assertGreater(oben, ry)
            self.assertAlmostEqual(boden, ry + rh, places=6)
            self.assertLess(float(label.get("y")) / L.DPI, oben)            # Name über der Inhaltsfläche
            self.assertAlmostEqual(float(label.get("x")) / L.DPI, x + b / 2, places=2)
            links += b
        schild_y = float(texte[0].get("y")) / L.DPI
        self.assertLess(schild_y, ry)                                       # Schild über der Kiste

    def test_kiste_mehr(self):
        """mehr = Breite eines letzten Fachs mit grauen Auslassungspunkten: Die Liste hat weitere Elemente.
        Es hat keinen $-Namen und keinen Inhalt; zurück kommen nur die benannten Fächer."""
        s = L.Canvas(5, 3)
        faecher = L.kiste(s, 0.2, 0.2, [("a", 1.0), ("bb", 1.5)], h=1.4, mehr=0.4)
        els = alle_elemente(s.svg())
        texte = [e for e in els if e.tag == NS + "text"]
        self.assertEqual(["".join(e.itertext()) for e in texte], ["$a", "$bb", "…"])
        self.assertEqual(texte[-1].get("fill"), L.GRAY)
        self.assertEqual(len(faecher), 2)
        rahmen = [e for e in els if e.tag == NS + "rect" and e.get("fill") == L.CARD and e.get("stroke") == L.INK]
        self.assertAlmostEqual(float(rahmen[0].get("width")) / L.DPI, 2.9, places=2)
        x_punkte = float(texte[-1].get("x")) / L.DPI
        self.assertAlmostEqual(x_punkte, 0.2 + 2.5 + 0.2, places=2)        # mittig im letzten Fach
        # ohne mehr: dieselbe Kiste wie bisher (k03-liste bleibt byte-gleich)
        a, b = L.Canvas(5, 3), L.Canvas(5, 3)
        L.kiste(a, 0.2, 0.2, [("a", 1.0)], h=1.0, name="x")
        L.kiste(b, 0.2, 0.2, [("a", 1.0)], h=1.0, name="x", mehr=None)
        self.assertEqual(a.svg(), b.svg())

    def test_referenz(self):
        """Markierung der Referenzkategorie: Schild mit Spitze nach links, Spitze an der angegebenen Stelle."""
        s = L.Canvas(3, 1)
        rechts = L.referenz(s, 1.0, 0.5)
        els = alle_elemente(s.svg())
        self.assertEqual(["".join(e.itertext()) for e in els if e.tag == NS + "text"], ["Referenz"])
        poly = [e for e in els if e.tag == NS + "polygon"]
        self.assertEqual(len(poly), 1)
        punkte = [tuple(float(v) / L.DPI for v in p.split(",")) for p in poly[0].get("points").split()]
        spitze = min(punkte)
        self.assertAlmostEqual(spitze[0], 1.0, places=2)
        self.assertAlmostEqual(spitze[1], 0.5, places=2)
        self.assertAlmostEqual(rechts, max(p[0] for p in punkte), places=2)
        self.assertGreater(rechts - 1.0, L.text_width("Referenz", L.SANS, 10.5, True))


    def test_kreis(self):
        """Kreis um einen Mittelpunkt (Punkte in einer Grafik, Ring um einen Punkt), auch gestrichelt."""
        s = L.Canvas(2, 2)
        L.kreis(s, 1.0, 0.5, 0.25, L.WHITE)
        L.kreis(s, 0.5, 1.5, 0.1, None, L.ORANGE, lw=1.5, dash=True)
        k = [e for e in alle_elemente(s.svg()) if e.tag == NS + "circle"]
        self.assertEqual(len(k), 2)
        self.assertEqual([float(k[0].get(a)) / L.DPI for a in ("cx", "cy", "r")], [1.0, 0.5, 0.25])
        self.assertEqual(k[0].get("fill"), L.WHITE)
        self.assertIsNone(k[0].get("stroke"))
        self.assertEqual((k[1].get("fill"), k[1].get("stroke")), ("none", L.ORANGE))
        self.assertTrue(k[1].get("stroke-dasharray"))

    def test_polygon(self):
        """Fläche aus Punkten in Zoll, wahlweise mit Kante und Deckkraft (Violinen in k06-ebenen)."""
        s = L.Canvas(2, 2)
        L.polygon(s, [(0.1, 0.1), (1.0, 0.1), (0.5, 1.0)], "#F8766D", line=L.INK, deckkraft=0.4)
        L.polygon(s, [(0.2, 0.2), (0.4, 0.2), (0.3, 0.4)], L.GRAY)
        p = [e for e in alle_elemente(s.svg()) if e.tag == NS + "polygon"]
        self.assertEqual(len(p), 2)
        punkte = [tuple(float(v) / L.DPI for v in q.split(",")) for q in p[0].get("points").split()]
        for ist, soll in zip(punkte, [(0.1, 0.1), (1.0, 0.1), (0.5, 1.0)]):
            self.assertAlmostEqual(ist[0], soll[0], places=4)
            self.assertAlmostEqual(ist[1], soll[1], places=4)
        self.assertEqual(len(punkte), 3)
        self.assertEqual((p[0].get("fill"), p[0].get("stroke"), p[0].get("fill-opacity")), ("#F8766D", L.INK, "0.4"))
        self.assertIsNone(p[1].get("stroke"))
        self.assertIsNone(p[1].get("fill-opacity"))


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
    "k03-vergleich": ["alter", "22", "45", "67", "18", "33", "alter >= 18", "alter <= 65", "&", "TRUE", "FALSE",
                      "alter >= 18 & alter <= 65", "[1]  TRUE  TRUE FALSE  TRUE  TRUE"],
    "k03-index": ["zahlen", "10", "20", "30", "40", "50", "zahlen > 25", "TRUE", "FALSE", "zahlen[zahlen > 25]",
                  "[1] FALSE FALSE  TRUE  TRUE  TRUE", "[1] 30 40 50"],
    "k03-recycling": ["zahlen * 2", "c(1, 2, 3, 4) + c(10, 20)", "*", "+", "10", "50", "2", "100", "11", "22", "13",
                      "24", "[1]  20  40  60  80 100", "[1] 11 22 13 24"],
    "k03-faktor": ["geschlecht", "Mann", "Frau", "Divers", "1", "2", "3", "intern", "levels(geschlecht)",
                   '[1] "Mann"   "Frau"   "Divers"', "Referenz",
                   'geschlecht <- factor(c("Mann", "Frau", "Mann", "Divers"),',
                   'levels = c("Mann", "Frau", "Divers"))'],
    "k03-liste": ["ergebnis", "$koeffizient", "$p_wert", "$konfidenz", "$modell", "0.42", "0.001", "0.31", "0.53",
                  '"lm"', "[1]", "ergebnis$konfidenz[1]", "[1] 0.31"],
}


def texte_pos(svg):
    """(Text, x, y, Farbe) je <text>, in Zoll; x ist bei zentrierten Steinwerten die Mitte."""
    return [("".join(e.itertext()), float(e.get("x")) / L.DPI, float(e.get("y")) / L.DPI, e.get("fill"))
            for e in ET.fromstring(svg).iter(NS + "text")]


def spalten(svg, werte):
    """Gruppiert Texte aus `werte` nach x (Spalten von links nach rechts), je Spalte von oben nach unten."""
    sp = {}
    for t, x, y, _ in texte_pos(svg):
        if t in werte:
            sp.setdefault(round(x, 2), []).append((y, t))
    return [[t for _, t in sorted(v)] for _, v in sorted(sp.items())]


class TestKap03Bilder(unittest.TestCase):
    def test_vergleich_stein_fuer_stein(self):
        """`&` verknüpft die beiden Wahrheitstürme Reihe für Reihe; die Reihe mit 67 ist markiert."""
        import kap03
        svg = kap03.vergleich().svg()
        self.assertEqual(spalten(svg, {"22", "45", "67", "18", "33"}), [["22", "45", "67", "18", "33"]])
        self.assertEqual(spalten(svg, {"TRUE", "FALSE"}),
                         [["TRUE"] * 5, ["TRUE", "TRUE", "FALSE", "TRUE", "TRUE"], ["TRUE", "TRUE", "FALSE", "TRUE", "TRUE"]])
        self.assertEqual(len([t for t in texte_pos(svg) if t[0] == "&"]), 5)
        y67 = [y for t, _, y, _ in texte_pos(svg) if t == "67"][0]
        rahmen = [r for r in ET.fromstring(svg).iter(NS + "rect") if r.get("stroke") == L.ORANGE]
        self.assertEqual(len(rahmen), 1)
        oben = float(rahmen[0].get("y")) / L.DPI
        self.assertTrue(oben < y67 < oben + float(rahmen[0].get("height")) / L.DPI)

    def test_index_schablone(self):
        """Neben FALSE werden die Steine grau (fallen weg), rechts bleibt der Turm 30, 40, 50."""
        import kap03
        svg = kap03.index_fig().svg()
        grau = [t for t, _, _, f in texte_pos(svg) if f == L.STEIN["dim"][1]]
        self.assertEqual(grau, ["10", "20"])
        self.assertEqual(spalten(svg, {"10", "20", "30", "40", "50"}),
                         [["10", "20", "30", "40", "50"], ["30", "40", "50"]])
        self.assertEqual(spalten(svg, {"TRUE", "FALSE"}), [["FALSE", "FALSE", "TRUE", "TRUE", "TRUE"]])

    def test_recycling_blass(self):
        """Blass sind genau die Werte, die R wiederholt: viermal die 2, einmal 10 und 20."""
        import kap03
        svg = kap03.recycling().svg()
        blass = [t for t, _, _, f in texte_pos(svg) if f == L.STEIN_BLASS["num"][1]]
        self.assertEqual(blass, ["2", "2", "2", "2", "10", "20"])
        voll_links = [t for t, x, _, f in texte_pos(svg) if f == L.STEIN["num"][1] and x < 3.65]   # zahlen * 2
        self.assertEqual(voll_links.count("2"), 1)
        self.assertIn(["20", "40", "60", "80", "100"], spalten(svg, {"20", "40", "60", "80", "100"}))
        self.assertEqual(spalten(svg, {"11", "22", "13", "24"}), [["11", "22", "13", "24"]])

    def test_faktor_stufen(self):
        """Intern 1 2 1 3 neben Mann, Frau, Mann, Divers; die Stufenleiste 1–3 mit Mann als Referenz."""
        import kap03
        svg = kap03.faktor_fig().svg()
        self.assertEqual(spalten(svg, {"Mann", "Frau", "Divers"}),
                         [["Mann", "Frau", "Mann", "Divers"], ["Mann", "Frau", "Divers"]])
        self.assertEqual(spalten(svg, {"1", "2", "3"}), [["1", "2", "1", "3"], ["1", "2", "3"]])
        pos = texte_pos(svg)
        ref = [y for t, _, y, _ in pos if t == "Referenz"]
        mann_leiter = max((x, y) for t, x, y, _ in pos if t == "Mann")
        self.assertEqual(len(ref), 1)
        self.assertAlmostEqual(ref[0], mann_leiter[1], delta=0.05)

    def test_liste_kiste(self):
        """Vier Fächer in Listenreihenfolge; im Fach konfidenz steht 0.31 über 0.53; Ergebnis 0.31 ganz rechts."""
        import kap03
        svg = kap03.liste_fig().svg()
        pos = texte_pos(svg)
        namen = [t for t, *_ in pos if t.startswith("$")]
        self.assertEqual(namen, ["$koeffizient", "$p_wert", "$konfidenz", "$modell", "$konfidenz"])  # Fächer, Schritt 1
        self.assertEqual(spalten(svg, {"0.31", "0.53"})[0], ["0.31", "0.53"])
        x_fach = [x for t, x, *_ in pos if t == "$konfidenz"][0]
        x_031 = sorted(x for t, x, *_ in pos if t == "0.31")
        self.assertAlmostEqual(x_031[0], x_fach, delta=0.05)
        self.assertEqual(len(x_031), 3)                                       # in der Kiste, Turm, Ergebnis


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
