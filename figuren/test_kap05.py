"""Tests für die Abbildungen von Kap. 5 „Daten transformieren und Skalen bilden“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4)
ERWARTET_KAP05 = {
    "k05-mutate": ["age", "<dbl+lbl>", "geburtsjahr", "<dbl>", "50", "51", "69", "1973", "1972", "1954",
                   "2023 - 50", "2023 - 51", "2023 - 69", "mutate", "geburtsjahr = 2023 - age",
                   "allbus |> select(age) |> mutate(geburtsjahr = 2023 - age) |> head(3)"],
    "k05-zuweisung": ["OHNE <-", "MIT <-", "allbus |>", "allbus <- allbus |>", "mutate(geburtsjahr = 2023 - age)",
                      "allbus", "5,246 × 579",
                      "5,246 × 580", "age", "geburtsjahr", "50", "51", "69", "1973", "1972", "1954",
                      "nur angezeigt", "gespeichert"],
    "k05-case-when": ["FALSCH", "RICHTIG", 'age >= 18 ~ "erwachsen"', 'age >= 65 ~ "senior"',
                      '.default = "unter 18"', "50", "51", "69", "72", "18"],
    "k05-summarise": ["eastwest", "age", "ALTE BUNDESLAENDER", "NEUE BUNDESLAENDER", "50", "51", "69", "72",
                      "44", "60", "durchschnitt_alter", "51.7", "54.3", "3567", "1679", "mean()",
                      "group_by(eastwest) |> summarise(durchschnitt_alter = mean(age, na.rm = TRUE))"],
    "k05-rec": ["educ", "1", "2", "3", "4", "5", "6", "7", "OHNE ABSCHLUSS", "VOLKS-,HAUPTSCHULE", "MITTLERE REIFE",
                "FACHHOCHSCHULREIFE", "HOCHSCHULREIFE", "ANDERER ABSCHLUSS", "NOCH SCHUELER", "1:2=1 [niedrig]",
                "3=2 [mittel]", "4:5=3 [hoch]", "else=NA", "niedrig", "mittel", "hoch", "982", "1639", "2472", "153",
                "<fct>"],
    "k05-dicho": ["age", "age_d", "72", "69", "51", "50", "18", "1", "0", "dicho(50)", "2942", "2281",
                  "NICHT GENERIERBAR", "23", "bis 50", "über 50"],
    "k05-umpolen": ["mm02", "mm02r", "1", "2", "3", "4", "5", "6", "7", "STIMME GAR NICHT ZU", "STIMME VOLL+GANZ ZU",
                    "TNZ: SPLIT", "954", "515", "494", "629", "350", "235", "227", "1842", "8 - x",
                    "allbus |> count(mm02, mm02r)"],
    "k05-skala": ["respid", "mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06", "islamophobie", "1", "53", "120",
                  "5", "4", "2", "6", "3", "3.33", "3.4", "min_valid = 5", "6 gültig", "5 gültig", "4 gültig"],
    "k05-polung": ["mm01", "pa29", "pa29r", "STIMME GAR NICHT ZU", "STIMME VOLL+GANZ ZU", "STIMME VOLL ZU",
                   "LEHNE GANZ AB", "1", "5", "7", "hoch = islamophob", "niedrig = populistisch",
                   "hoch = populistisch", 'rec(pa29, rules = "rev", suffix = "r")'],
    "k05-pomps": ["islamophobie", "populismus", "islamophobie_p", "populismus_p", "4.11", "3.4", "51.9", "60.0",
                  "0", "25", "50", "75", "100", "1", "5", "7"],
    "k05-pipeline": ["1", "2", "3", "4", "5", "6", "R/prep.R", 'source("R/prep.R")', "4.3", "5.3.3", "5.7.1",
                     "5.7.3", "5.8", "read_spss()", "row_means()", "pomps()"],
}


class TestKap05(unittest.TestCase):
    def test_kap05_constraints(self):
        import kap05
        self.assertEqual(set(kap05.FIGUREN), set(ERWARTET_KAP05))
        for name, fn in kap05.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP05[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")


if __name__ == "__main__":
    unittest.main()
