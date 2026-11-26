"""Tests für die Abbildungen von Kap. 3 „Programmiersprache R“ (BILDER.md §6, §10)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Werte aus den Chunks neben den Abbildungen (Kap. 3)
ERWARTET_KAP03 = {
    "k03-legende": ["WERT = STEIN", "VEKTOR = TURM", "DATENSATZ = BAUPLATTE", "CODE-FARBEN", "Zahl", "Text",
                    "Wahrheitswert", "fehlender Wert", "mit Wertelabel", "Aufkleber", "MANN", "zahlen",
                    "geschlecht", "alter", "Mann", "Frau", "Divers", "34", "41", "52", "round", "digits = 1",
                    "numeric", "character", "logical", "NA", "Objekt", "Funktion", "Argument", "ein Datentyp",
                    "eine Reihe = ein Fall", "ein Turm = eine Variable"],
    "k03-turm": ["zahlen", "namen", "flags", "numeric", "character", "logical", "NA", "Anna", "Boris", "Carla",
                 "TRUE", "FALSE", "1", "5"],
    "k03-rangfolge": ["c(1, TRUE, FALSE)", 'c(1, "Anna", TRUE)', "[1] 1 1 0", '[1] "1" "Anna" "TRUE"',
                      "RANGFOLGE", "numeric", "character", "logical"],
    "k03-tibble": ["befragte", "4 × 2", "geschlecht", "alter", "<fct>", "<dbl>", "Mann", "Frau", "Divers", "34",
                   "41", "28", "52", "Eine Reihe ist ein Fall:", "die zweite befragte Person, Frau, 41 Jahre.",
                   "Ein Turm ist eine Variable:", "befragte$alter", "[1] 34 41 28 52"],
    "k03-pipe": ["zahlen", "round(", "head(", ", digits = 1)", ", n = 3)", "1.55", "1.6", "1.3",
                 "= round(zahlen, digits = 1)", "= head(round(zahlen, digits = 1),", "|>"],
    "k03-name-inhalt": ["var1", "<-", "2 * 4", "Name", "Ausdruck", "[1] 8", "ENVIRONMENT", "8"],
    "k03-reihenfolge": ["x <- 5", "y <- x + 2", "x <- 10", "y", "[1] 7", "NACH ZEILE 1", "NACH ZEILE 2",
                        "NACH ZEILE 3", "5", "7", "10"],
    "k03-funktion": ["from", "to", "by", "seq()", "1", "10", "2", "from = 1", "to = 10", "by = 2",
                     "[1] 1 3 5 7 9", "Funktion", "Argumente"],
    "k03-argumente": ["round()", "x", "digits", "Pflichtfeld", "vorausgefüllt mit 0", "3.987", "4.0",
                      "round(c(1.222, 2.345, 3.987), digits = 1)", "[1] 1.2 2.3 4.0"],
    "k03-na": ["x", "mean", "na.rm = TRUE", "[1] NA", "[1] 3", "NA", "5", "4", "2", "1", "3"],
    "k03-analyseplan": ['allbus <- read_spss("ALLBUS2023.sav")', "mutate(", 'mm02r = rec(mm02, rules = "rev"),',
                        'mm05r = rec(mm05, rules = "rev")', "islamophobie = row_means(pick(mm01, mm02r, mm03, "
                        "mm04, mm05r, mm06),", "min_valid = 5)", "DIE PIPE", "DER PLAN IN WORTEN",
                        "Datensatz einlesen", "mm02", "mm05", "umpolen", "Skala bilden"],
    "k03-vergleich": ["alter", "alter >= 18", "alter <= 65", "&", "22", "45", "67", "18", "33", "TRUE", "FALSE",
                      "alter >= 18 & alter <= 65", "[1]  TRUE  TRUE FALSE  TRUE  TRUE"],
    "k03-index": ["zahlen", "zahlen > 25", "zahlen[zahlen > 25]", "[1] FALSE FALSE  TRUE  TRUE  TRUE",
                  "[1] 30 40 50", "10", "20", "30", "40", "50"],
    "k03-recycling": ["zahlen * 2", "c(1, 2, 3, 4) + c(10, 20)", "[1]  20  40  60  80 100", "[1] 11 22 13 24",
                      "*", "+", "2", "10", "20", "11", "22", "13", "24"],
    "k03-faktor": ["geschlecht", "intern", "levels(geschlecht)", "Referenz", "Mann", "Frau", "Divers",
                   '[1] "Mann"   "Frau"   "Divers"', "1", "2", "3",
                   'geschlecht <- factor(c("Mann", "Frau", "Mann", "Divers"),',
                   'levels = c("Mann", "Frau", "Divers"))'],
    "k03-liste": ["ergebnis", "$koeffizient", "$p_wert", "$konfidenz", "$modell", "0.42", "0.001", "0.31", "0.53",
                  '"lm"', "ergebnis$konfidenz[1]", "[1] 0.31", "[1]"],
}


# Englische Fassung: eigene Namen nach STYLE.md §13 (numbers, first_names, age, gender, respondents, result,
# coefficient, p_value, conf_int, model), Stufen male/female/non-binary, ALLBUS-Label MALE aus ZA8833.
# Die Faktorausgabe entspricht dem R-Druck von levels(gender); k03-analyseplan zeigt set_na() nach read_spss().
ERWARTET_KAP03_EN = {
    "k03-legende": ["VALUE = BRICK", "VECTOR = TOWER", "DATASET = BASEPLATE", "CODE COLOURS", "Number", "Text",
                    "Logical value", "Missing value", "With value label", "sticker", "MALE", "numbers",
                    "gender", "age", "male", "female", "non-binary", "34", "41", "52", "round", "digits = 1",
                    "numeric", "character", "logical", "NA", "Object", "Function", "Argument", "one data type",
                    "one row = one case", "one tower = one variable"],
    "k03-turm": ["numbers", "first_names", "flags", "numeric", "character", "logical", "NA", "Anna", "Boris",
                 "Carla", "TRUE", "FALSE", "1", "5"],
    "k03-rangfolge": ["c(1, TRUE, FALSE)", 'c(1, "Anna", TRUE)', "[1] 1 1 0", '[1] "1" "Anna" "TRUE"',
                      "TYPE ORDER", "numeric", "character", "logical"],
    "k03-tibble": ["respondents", "4 × 2", "gender", "age", "<fct>", "<dbl>", "male", "female", "non-binary",
                   "34", "41", "28", "52", "A row is a case:", "the second respondent, female, 41 years old.",
                   "A tower is a variable:", "respondents$age", "[1] 34 41 28 52"],
    "k03-pipe": ["numbers", "round(", "head(", ", digits = 1)", ", n = 3)", "1.55", "1.6", "1.3",
                 "= round(numbers, digits = 1)", "= head(round(numbers, digits = 1), n = 3)", "|>"],
    "k03-name-inhalt": ["var1", "<-", "2 * 4", "Name", "Expression", "[1] 8", "ENVIRONMENT", "8"],
    "k03-reihenfolge": ["x <- 5", "y <- x + 2", "x <- 10", "y", "[1] 7", "AFTER LINE 1", "AFTER LINE 2",
                        "AFTER LINE 3", "5", "7", "10"],
    "k03-funktion": ["from", "to", "by", "seq()", "1", "10", "2", "from = 1", "to = 10", "by = 2",
                     "[1] 1 3 5 7 9", "Function", "Arguments"],
    "k03-argumente": ["round()", "x", "digits", "required", "default: 0", "3.987", "4.0",
                      "round(c(1.222, 2.345, 3.987), digits = 1)", "[1] 1.2 2.3 4.0"],
    "k03-na": ERWARTET_KAP03["k03-na"],
    "k03-analyseplan": ['allbus <- read_spss("ALLBUS2023.sav")', "set_na(-56, …, -6)", "mutate(",
                        'mm02r = rec(mm02, rules = "rev"),', 'mm05r = rec(mm05, rules = "rev")',
                        "islamophobia = row_means(pick(mm01, mm02r, mm03, mm04, mm05r, mm06),", "min_valid = 5)",
                        "THE PIPE", "THE PLAN IN WORDS", "Read in the dataset", "Set missing codes to NA",
                        "Reverse-code", "mm02", "mm05", "Build the scale"],
    "k03-vergleich": ["age", "age >= 18", "age <= 65", "&", "22", "45", "67", "18", "33", "TRUE", "FALSE",
                      "age >= 18 & age <= 65", "[1]  TRUE  TRUE FALSE  TRUE  TRUE"],
    "k03-index": ["numbers", "numbers > 25", "numbers[numbers > 25]", "[1] FALSE FALSE  TRUE  TRUE  TRUE",
                  "[1] 30 40 50", "10", "20", "30", "40", "50"],
    "k03-recycling": ["numbers * 2", "c(1, 2, 3, 4) + c(10, 20)", "[1]  20  40  60  80 100", "[1] 11 22 13 24",
                      "*", "+", "2", "10", "20", "11", "22", "13", "24"],
    "k03-faktor": ["gender", "internal", "levels(gender)", "Reference", "male", "female", "non-binary",
                   '[1] "male"       "female"     "non-binary"', "1", "2", "3",
                   'gender <- factor(c("male", "female", "male", "non-binary"),',
                   'levels = c("male", "female", "non-binary"))'],
    "k03-liste": ["result", "$coefficient", "$p_value", "$conf_int", "$model", "0.42", "0.001", "0.31", "0.53",
                  '"lm"', "result$conf_int[1]", "[1] 0.31", "[1]"],
}


class TestKap03(unittest.TestCase):
    def tearDown(self):
        import sprache
        sprache.setze("de")

    def test_kap03_constraints(self):
        import kap03
        self.assertEqual(set(kap03.FIGUREN), set(ERWARTET_KAP03))
        for name, fn in kap03.FIGUREN.items():
            svg = fn().svg()
            breite = float(ET.fromstring(svg).get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP03[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")


class TestKap03Englisch(unittest.TestCase):
    def tearDown(self):
        import sprache
        sprache.setze("de")

    def test_schluessel_gleich(self):
        self.assertEqual(set(ERWARTET_KAP03_EN), set(ERWARTET_KAP03))

    def test_sprachfaehig(self):
        import kap03
        self.assertTrue(getattr(kap03, "SPRACHFAEHIG", False))

    def test_bautest_englisch(self):
        import kap03
        import sprache
        sprache.setze("en")
        for name, fn in kap03.FIGUREN.items():
            svg = fn().svg()
            breite = float(ET.fromstring(svg).get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)

    def test_englische_texte(self):
        import kap03
        import sprache
        sprache.setze("en")
        for name, fn in kap03.FIGUREN.items():
            texte = alle_texte(fn().svg())
            for wert in ERWARTET_KAP03_EN[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_kein_deutscher_rest(self):
        import check_en
        import kap03
        import sprache
        sprache.setze("en")
        for name, fn in kap03.FIGUREN.items():
            reste = check_en.deutsch_reste(alle_texte(fn().svg()))
            self.assertEqual(reste, [], name)

    def test_deutsche_namen_nicht_im_englischen(self):
        import kap03
        import sprache
        sprache.setze("en")
        for name, fn in kap03.FIGUREN.items():
            texte = alle_texte(fn().svg())
            for alt in ("zahlen", "geschlecht", "alter", "befragte", "ergebnis", "namen", "Mann", "Frau", "Divers"):
                self.assertNotIn(alt, texte, f"{name}: {alt}")

    def test_deutsch_unveraendert(self):
        import kap03
        import sprache
        sprache.setze("en")
        en_texte = alle_texte(kap03.faktor_fig().svg())
        sprache.setze("de")
        self.assertIn("Referenz", alle_texte(kap03.faktor_fig().svg()))
        self.assertNotIn("Referenz", en_texte)


if __name__ == "__main__":
    unittest.main()
