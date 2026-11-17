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
}


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


if __name__ == "__main__":
    unittest.main()
