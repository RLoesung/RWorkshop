"""Abbildungen für Kap. 2 „Quarto“ (BILDER.md §6). Inhalt aus dem Buch.

Das .qmd ist das erste Beispiel aus 2.4, Zeile für Zeile. Es hat keinen Inline-Code, darum zeigt das Bild drei
Schichten. Die gerenderte Seite rechts ist geprüft: quarto render mit genau diesem Dokument zeigt Titel, Autorin,
Überschrift, Absatz, die Code-Zeile und die Ausgabe [1] 3 (R 4.5.3).
"""
from lego import (Canvas, R, P, text, rect, label_box, outline, arrow, numdot, codebox, text_width, GRAY, GREEN,
                  WHITE, CARD, CARDLINE, SANS, C)
from kap03 import mono

QMD = ["---", 'title: "Mein erster Bericht"', 'author: "Anna Schmidt"', "format: html", "---", "",
       "## Einleitung", "", "In diesem Bericht analysiere ich den ALLBUS 2023.", "", "```{r}",
       "mean(c(1, 2, 3, 4, 5))", "```"]
SCHICHTEN = [(0, 4, "YAML-Header"), (6, 8, "Markdown-Lauftext"), (10, 12, "Code-Chunk")]


# 2.4 Das erste .qmd und was beim Rendern daraus wird ---------------------------------------------
def qmd_schichten():
    s = Canvas(8.0, 3.2)
    size, oben, cw = 10, 0.18, 4.5
    lh = size * 1.42 / 72
    h = codebox(s, 0.1, oben, cw, QMD, size=size, hash_gray=False)
    z0 = oben + 0.14
    mitten = []
    for k, (a, b, name) in enumerate(SCHICHTEN):
        y0, hh = z0 + a * lh - 0.02, (b - a + 1) * lh + 0.05
        outline(s, 0.2, y0, cw - 0.16, hh, color=GREEN, lw=1.5)
        # Beschriftung rechts auf der ersten Zeile der Schicht (---, ## Einleitung, ```{r}: alle kurz)
        bw = text_width(name, SANS, 10, True) + 0.24
        ym = z0 + a * lh + lh / 2
        label_box(s, 0.1 + cw - 0.2 - bw, ym - 0.12, bw, 0.24, name, GREEN, size=10, font=SANS, rounded=False)
        numdot(s, 0.1 + cw - 0.2 - bw - 0.32, ym - 0.13, k + 1, fill=GREEN, d=0.26, size=10)
        mitten.append((y0, hh))
    # Rendern
    text(s, 4.6, oben + h / 2 - 0.42, 0.7, 0.28, [P(R("Render", size=10.5, bold=True), align=C)])
    arrow(s, 4.72, oben + h / 2 - 0.14, w=0.46, h=0.28, color=GRAY)
    # die gerenderte Seite
    px, pw = 5.3, 2.6
    rect(s, px, oben, pw, h, WHITE, CARDLINE, 1.0)
    ix, iw = px + 0.42, pw - 0.5
    # jeder Teil beginnt auf der Höhe seiner Schicht
    (y1, _), (y2, _), (y3, _) = mitten
    t1 = y1 + 0.02
    numdot(s, px + 0.08, t1 + 0.04, 1, fill=GREEN, d=0.26, size=10)
    text(s, ix, t1, iw, 0.3, [P(R("Mein erster Bericht", size=13, bold=True))])
    text(s, ix, t1 + 0.31, iw, 0.25, [P(R("Anna Schmidt", size=10.5, color=GRAY))])
    t2 = y2 + 0.01
    numdot(s, px + 0.08, t2 + 0.04, 2, fill=GREEN, d=0.26, size=10)
    text(s, ix, t2, iw, 0.3, [P(R("Einleitung", size=12, bold=True))])
    text(s, ix, t2 + 0.3, iw, 0.4, [P(R("In diesem Bericht analysiere ich den ALLBUS 2023.", size=10.5), ls=1.0)])
    t3 = y3 + 0.01
    numdot(s, px + 0.08, t3 + 0.05, 3, fill=GREEN, d=0.26, size=10)
    rect(s, ix, t3, iw, 0.36, CARD, CARDLINE, 0.75)
    text(s, ix + 0.06, t3, iw - 0.1, 0.36, mono("mean(c(1, 2, 3, 4, 5))", size=10, align="start"), anchor="middle")
    text(s, ix + 0.06, t3 + 0.4, iw - 0.1, 0.25, mono("[1] 3", size=10, color=GREEN, align="start"))
    return s


FIGUREN = {
    "k02-qmd-schichten": qmd_schichten,
}
