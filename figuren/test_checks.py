"""Tests für die Prüfskripte der Bausteine-Abbildungen."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_qmd  # noqa: E402
import check_sections  # noqa: E402

GUT = ('Siehe @fig-turm.\n\n'
       '![Drei Türme.](Bilder/figuren/k03-turm.svg){#fig-turm .lightbox fig-alt="Drei Türme aus Steinen."}\n')


class TestCheckQmd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        os.makedirs(os.path.join(self.root, "Bilder", "figuren"))
        open(os.path.join(self.root, "Bilder", "figuren", "k03-turm.svg"), "w").write("<svg/>")

    def tearDown(self):
        self.tmp.cleanup()

    def run_on(self, inhalt):
        p = os.path.join(self.root, "03-Test.qmd")
        open(p, "w", encoding="utf-8").write(inhalt)
        return check_qmd.main(["--root", self.root, p])

    def test_alles_da(self):
        self.assertEqual(self.run_on(GUT), 0)

    def test_ohne_alt(self):
        self.assertEqual(self.run_on(GUT.replace(' fig-alt="Drei Türme aus Steinen."', "")), 1)

    def test_ohne_lightbox(self):
        self.assertEqual(self.run_on(GUT.replace(" .lightbox", "")), 1)

    def test_ohne_verweis(self):
        self.assertEqual(self.run_on(GUT.replace("Siehe @fig-turm.", "Siehe oben.")), 1)

    def test_datei_fehlt(self):
        self.assertEqual(self.run_on(GUT.replace("k03-turm.svg", "k03-fehlt.svg")), 1)


class TestCheckSections(unittest.TestCase):
    ALT = ('<h2 data-number="3.4" class="anchored">3.4 Operatoren</h2>'
           '<h3 data-number="3.5.1" class="anchored">3.5.1 Vektoren</h3>')

    def test_gleich_plus_neu(self):
        neu = self.ALT + '<h3 data-number="3.4.1" class="anchored">3.4.1 Arithmetisch</h3>'
        self.assertEqual(check_sections.compare(check_sections.sections(self.ALT), check_sections.sections(neu)), [])

    def test_verschoben(self):
        neu = ('<h2 data-number="3.4" class="anchored">3.4 Operatoren</h2>'
               '<h3 data-number="3.5.1" class="anchored">3.5.1 Neu davor</h3>')
        self.assertTrue(check_sections.compare(check_sections.sections(self.ALT), check_sections.sections(neu)))


if __name__ == "__main__":
    unittest.main()
