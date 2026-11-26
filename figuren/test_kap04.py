"""Tests für die Abbildungen von Kap. 4 „Datenimport und Inspektion“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4)
ERWARTET_KAP04 = {
    "k04-einlesen": ["ALLBUS2023.sav", "read_spss()", "allbus", "5,246 × 579", "<-", "read_spss",
                     '"ALLBUS2023.sav"'],
    "k04-platte": ["allbus", "respid", "age", "mm01", "1", "5", "50", "51", "69", "72", "18", "2",
                   "nrow(allbus)", "[1] 5246", "ncol(allbus)", "[1] 579"],
    "k04-select": ["allbus", "5,246 × 579", "respid", "mm01", "mm02", "mm03", "mm04", "5,246 × 3",
                   "allbus |> select(mm01, mm02, mm03)", "5", "3", "4", "2"],
    "k04-dollar-select": ["allbus$age |> head(5)", "allbus |> select(age) |> head(5)", "[1] 50 51 69 72 18",
                          "5 × 1", "age", "<dbl+lbl>", "50", "51", "69", "72", "18"],
    "k04-filter": ["allbus", "sex", "age", "educ", "MANN", "FRAU", "50", "51", "69", "72", "18", "45", "3", "4", "5",
                   "sex == 2", "2,672 × 3", "allbus |> filter(sex == 2) |> select(sex, age, educ)"],
    "k04-dbl-lbl": ["1", "MANN", "double", "haven_labelled", "<dbl+lbl>", "dbl", "lbl", "class(allbus$sex)",
                    '[1] "haven_labelled" "vctrs_vctr"     "double"'],
    "k04-to-label": ["sex", "<dbl+lbl>", "<fct>", "<dbl>", "to_label()", "to_numeric()", "MANN", "FRAU", "1", "2"],
    "k04-labels": ["mm01", '"ISLAMAUSUEBUNG IN DEUTSCHL. BESCHRAENKEN"', "STIMME GAR NICHT ZU",
                   "STIMME VOLL+GANZ ZU", "1", "7", "Variablenname", "Variablenlabel", "Wertelabels",
                   "var_label()", "val_labels()"],
    "k04-missing-codes": ["-42", "-11", "-9", "-8", "DATENFEHLER: MFN", "TNZ: SPLIT", "KEINE ANGABE", "WEISS NICHT",
                          "2", "1647", "73", "123", "NA(a)", "NA(b)", "NA(c)", "NA(d)", "code", "n", "tag",
                          "na_frequencies(allbus$mm01)", "mm01", "mm06", "SPLIT-DESIGN"],
    "k04-set-na": ["6", "7", "ANDERER ABSCHLUSS", "NOCH SCHUELER", "18", "26", "set_na", "educ = c(6, 7)",
                   "# total N=5246 valid N=5093", "GÜLTIG", "FEHLEND"],
    "k04-filter-na": ["sex", "<dbl+lbl>", "1", "2", "3", "110", "MANN", "FRAU", "KEINE ANGABE", "sex == 1", "TRUE",
                      "FALSE", "NA", "filter()", "allbus |> filter(sex == 1)"],
    "k04-drop-na": ["mm01", "mm02", "mm03", "1", "2", "53", "5", "3", "4", "drop_na()", "eine Lücke",
                    "allbus |> select(mm01, mm02, mm03) |> drop_na() |> nrow()", "[1] 3285"],
}


# Englische Fassung: gleiche Schlüssel, Zahlen/Code/Namen gleich, Beschriftungen und Wertelabels aus ZA8833
# (ALLBUS2023_en.sav; fehlende Codes nach set_na(), Kennbuchstaben g, l, n, o bei mm01)
ERWARTET_KAP04_EN = {
    "k04-einlesen": ["ALLBUS2023.sav", "read_spss()", "allbus", "5,246 × 579", "<-", "read_spss",
                     '"ALLBUS2023.sav"', "File in the project folder", "Function from mariposa", "Object in R"],
    "k04-platte": ["allbus", "respid", "age", "mm01", "1", "5", "50", "51", "69", "72", "18", "2",
                   "nrow(allbus)", "[1] 5246", "ncol(allbus)", "[1] 579", "A row is a case:",
                   "A tower is a variable:", "An empty brick is a missing value."],
    "k04-select": ERWARTET_KAP04["k04-select"],
    "k04-dollar-select": ["allbus$age |> head(5)", "allbus |> select(age) |> head(5)", "[1] 50 51 69 72 18",
                          "5 × 1", "age", "<dbl+lbl>", "50", "51", "69", "72", "18", "Vector", "Tibble"],
    "k04-filter": ["allbus", "sex", "age", "educ", "MALE", "FEMALE", "50", "51", "69", "72", "18", "45", "3", "4",
                   "5", "sex == 2", "2,672 × 3", "allbus |> filter(sex == 2) |> select(sex, age, educ)"],
    "k04-dbl-lbl": ["1", "MALE", "double", "haven_labelled", "<dbl+lbl>", "dbl", "lbl", "class(allbus$sex)",
                    '[1] "haven_labelled" "vctrs_vctr"     "double"', "Number", "Value label"],
    "k04-to-label": ["sex", "<dbl+lbl>", "<fct>", "<dbl>", "to_label()", "to_numeric()", "MALE", "FEMALE", "1", "2",
                     "Factor", "Number without label"],
    "k04-labels": ["mm01", '"EXERCISE OF MUSLIM FAITH SHLD BE LIMITED"', "COMPLETELY DISAGREE",
                   "COMPLETELY AGREE", "1", "7", "Variable name", "Variable label", "Value labels",
                   "var_label()", "val_labels()"],
    "k04-missing-codes": ["-42", "-11", "-9", "-8", "DATA ERROR: MR", "NAP: SPLIT", "NO ANSWER", "DO NOT KNOW",
                          "2", "1647", "73", "123", "NA(g)", "NA(l)", "NA(n)", "NA(o)", "code", "n", "tag",
                          "na_frequencies(allbus$mm01)", "mm01", "mm06", "SPLIT DESIGN",
                          "two thirds: questions asked", "just under a third: NAP: SPLIT"],
    "k04-set-na": ["6", "7", "OTHER SCHOOL CERTIF.", "STILL AT SCHOOL", "18", "26", "set_na", "educ = c(6, 7)",
                   "# total N=5246 valid N=5093", "VALID", "MISSING", "18 + 26 = 44 fewer valid values"],
    "k04-filter-na": ["sex", "<dbl+lbl>", "1", "2", "3", "110", "MALE", "FEMALE", "NO ANSWER", "sex == 1", "TRUE",
                      "FALSE", "NA", "filter()", "allbus |> filter(sex == 1)"],
    "k04-drop-na": ["mm01", "mm02", "mm03", "1", "2", "53", "5", "3", "4", "drop_na()", "one gap",
                    "allbus |> select(mm01, mm02, mm03) |> drop_na() |> nrow()", "[1] 3285"],
}


def texte_pos(svg):
    """(Text, x, y, Farbe) je <text>, in Zoll; x ist bei zentrierten Steinwerten die Mitte."""
    from lego import DPI
    return [("".join(e.itertext()), float(e.get("x")) / DPI, float(e.get("y")) / DPI, e.get("fill"))
            for e in ET.fromstring(svg).iter(NS + "text")]


def spalten(svg, werte):
    """Gruppiert Texte aus `werte` nach x (Spalten von links nach rechts), je Spalte von oben nach unten."""
    sp = {}
    for t, x, y, _ in texte_pos(svg):
        if t in werte:
            sp.setdefault(round(x, 2), []).append((y, t))
    return [[t for _, t in sorted(v)] for _, v in sorted(sp.items())]


def rahmen(svg, farbe):
    """Rechtecke ohne Füllung mit Kante in `farbe`: (x, y, w, h) in Zoll."""
    from lego import DPI
    return [tuple(float(r.get(k)) / DPI for k in ("x", "y", "width", "height"))
            for r in ET.fromstring(svg).iter(NS + "rect") if r.get("stroke") == farbe and r.get("fill") == "none"]


class TestKap04(unittest.TestCase):
    def test_kap04_constraints(self):
        import kap04
        self.assertEqual(set(kap04.FIGUREN), set(ERWARTET_KAP04))
        for name, fn in kap04.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP04[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_dollar_select_bauplatte(self):
        """Links ein Turm auf kurzem Sockel, rechts eine breite Bauplatte mit den Maßen darüber."""
        import kap04
        from lego import GRAY, DPI
        root = ET.fromstring(kap04.dollar_select().svg())
        platten = sorted(float(r.get("width")) for r in root.iter(NS + "rect")
                         if r.get("fill") == GRAY and r.get("height") == "6.72")
        turm = 0.8 * DPI
        self.assertEqual(len(platten), 2)
        self.assertLessEqual(platten[0], 1.5 * turm)        # Sockel unter dem Vektor
        self.assertGreaterEqual(platten[1], 3 * turm)       # Platte mit Platz für weitere Türme
        self.assertIn("5 × 1", ["".join(e.itertext()) for e in root.iter(NS + "text")])

    def test_filter_na_leerer_stein(self):
        """sex == 1 ergibt TRUE TRUE FALSE und bei der Lücke wieder eine Lücke; nur die TRUE-Reihen bleiben."""
        import kap04
        from lego import STEIN
        svg = kap04.filter_na().svg()
        root = ET.fromstring(svg)
        self.assertEqual(spalten(svg, {"TRUE", "FALSE", "NA"}), [["TRUE", "TRUE", "FALSE", "NA"]])
        self.assertEqual(spalten(svg, {"1", "2", "3", "110"})[0], ["1", "2", "3", "110"])   # Reihennummern
        # NA steht in einem leeren, gestrichelten Stein (Typ log: rosa Spalte)
        x_na, y_na = [(x, y) for t, x, y, _ in texte_pos(svg) if t == "NA"][0]
        leer = [r for r in root.iter(NS + "rect") if r.get("fill") == STEIN["na"][0] and r.get("stroke-dasharray")
                and float(r.get("y")) / 96 < y_na < (float(r.get("y")) + float(r.get("height"))) / 96
                and float(r.get("x")) / 96 < x_na < (float(r.get("x")) + float(r.get("width"))) / 96]
        self.assertEqual(len(leer), 1)
        # grau: Wert und Aufkleber der FALSE-Reihe, Aufkleber der Lücke (beide fallen weg);
        # das Ergebnis behält zweimal 1 MANN auf Höhe der Reihen 1 und 2
        grau = [t for t, _, _, f in texte_pos(svg) if f == STEIN["dim"][1]]
        self.assertEqual(grau, ["2", "FRAU", "KEINE ANGABE"])
        einsen = spalten(svg, {"1"})
        self.assertEqual(einsen[-1], ["1", "1"])
        y_quelle = sorted(y for t, x, y, f in texte_pos(svg) if t == "1" and f == STEIN["num"][1])
        self.assertEqual(len(y_quelle), 4)
        self.assertAlmostEqual(y_quelle[0], y_quelle[1], delta=0.01)
        self.assertEqual(len([t for t, *_ in texte_pos(svg) if t == "MANN"]), 4)
        self.assertEqual(len([t for t, *_ in texte_pos(svg) if t == "KEINE ANGABE"]), 1)

    def test_drop_na_ganze_reihe(self):
        """Reihe 53 hat eine Lücke: 1 und 4 werden grau und die Reihe ist orange umrandet; übrig bleibt Reihe 1."""
        import kap04
        from lego import STEIN, ORANGE
        svg = kap04.drop_na_fig().svg()
        grau = [t for t, _, _, f in texte_pos(svg) if f == STEIN["dim"][1]]
        self.assertEqual(grau, ["1", "4"])
        pos = texte_pos(svg)
        y53 = [y for t, _, y, _ in pos if t == "53"][0]
        orange = rahmen(svg, ORANGE)
        self.assertEqual(len(orange), 1)
        self.assertTrue(orange[0][1] < y53 < orange[0][1] + orange[0][3])
        blau = [(t, round(y, 2)) for t, _, y, f in pos if f == STEIN["num"][1]]
        self.assertEqual([t for t, _ in blau], ["5", "3", "4", "5", "3", "4"])     # Quelle und Ergebnis: Reihe 1
        self.assertEqual(len({y for _, y in blau}), 1)                           # auf gleicher Höhe


class TestKap04Englisch(unittest.TestCase):
    def tearDown(self):
        import sprache
        sprache.setze("de")

    def test_schluessel_gleich(self):
        self.assertEqual(set(ERWARTET_KAP04_EN), set(ERWARTET_KAP04))

    def test_englische_texte(self):
        import kap04
        import sprache
        sprache.setze("en")
        for name, fn in kap04.FIGUREN.items():
            texte = alle_texte(fn().svg())
            for wert in ERWARTET_KAP04_EN[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_kein_deutscher_rest(self):
        import check_en
        import kap04
        import sprache
        sprache.setze("en")
        for name, fn in kap04.FIGUREN.items():
            reste = check_en.deutsch_reste(alle_texte(fn().svg()))
            self.assertEqual(reste, [], name)

    def test_deutsch_unveraendert(self):
        import kap04
        import sprache
        sprache.setze("en")
        en_texte = alle_texte(kap04.labels_fig().svg())
        sprache.setze("de")
        self.assertIn("Variablenname", alle_texte(kap04.labels_fig().svg()))
        self.assertNotIn("Variablenname", en_texte)


if __name__ == "__main__":
    unittest.main()
