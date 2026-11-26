"""Tests für figuren/pruefe_kaesten.py (zweisprachig)."""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pruefe_kaesten  # noqa: E402

EN_GUT = '''# Test {#sec-test}

::: {.callout-note}
**Research journal: Where are you?** Text.
:::

Text.

::: {.callout-warning}
**Caution: Missing values.** Text.
:::

Text.

::: {.callout-note collapse="true"}
## Background: Why?

Text.
:::

Text.

::: {.callout-important collapse="true"}
## mariposa tip: Shortcut

Text.
:::

Text.

::: {.callout-tip}
**SPSS → R.** Text.
:::

Text.

::: {.callout-note title="Exercise 1 · Topic · Type"}
Do it.
:::

::: {.callout-tip title="Answer" collapse="true"}
Yes.
:::
'''
DE_GUT = '''# Test {#sec-test}

::: {.callout-warning}
**Vorsicht: Fehlende Werte.** Text.
:::
'''


def lauf(name, inhalt):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, name)
        open(p, "w", encoding="utf-8").write(inhalt)
        with contextlib.redirect_stdout(io.StringIO()):
            return pruefe_kaesten.main(p)


class TestSprache(unittest.TestCase):
    def test_endung(self):
        self.assertEqual(pruefe_kaesten.sprache("a/04-Datenimport.en.qmd"), "en")
        self.assertEqual(pruefe_kaesten.sprache("04-Datenimport.qmd"), "de")

    def test_englisch_gut(self):
        self.assertEqual(lauf("03-Test.en.qmd", EN_GUT), 0)

    def test_englisch_falscher_einstieg(self):
        self.assertEqual(lauf("03-Test.en.qmd", EN_GUT.replace("**Caution: Missing", "**Warning: Missing")), 1)

    def test_englisch_falsche_klasse(self):
        self.assertEqual(lauf("03-Test.en.qmd", EN_GUT.replace(".callout-warning", ".callout-tip")), 1)

    def test_englisch_zu_ohne_titelzeile(self):
        self.assertEqual(lauf("03-Test.en.qmd", EN_GUT.replace("## Background: Why?", "Background: Why?")), 1)

    def test_deutsche_woerter_im_englischen_kapitel_sind_fehler(self):
        self.assertEqual(lauf("03-Test.en.qmd", EN_GUT.replace("**Caution: Missing", "**Vorsicht: Missing")), 1)


if __name__ == "__main__":
    unittest.main()
