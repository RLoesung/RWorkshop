"""Abbildungen für Kap. 2 „Quarto“ (BILDER.md §6). Inhalt aus dem Buch.

Das .qmd ist das erste Beispiel aus 2.4, Zeile für Zeile. Es hat keinen Inline-Code, darum zeigt das Bild drei
Schichten. Die gerenderte Seite rechts ist geprüft: quarto render mit genau diesem Dokument zeigt Titel, Autorin,
Überschrift, Absatz, die Code-Zeile und die Ausgabe [1] 3 (R 4.5.3).

2.6: Chunk mein-chunk mit mean(mtcars$mpg) (R 4.5.3: [1] 20.09062). Mit quarto render 1.8.25 geprüft, was je Option
im Bericht steht und dass include=FALSE ausführt, eval=FALSE nicht.
2.6.1: Der Setup-Chunk aus 2.6.1, Zeile für Zeile; Werkbank wie in 1.6.2 (k01-regal-werkbank).
2.9: Die Verweise aus dem Beispiel in 2.9. Die gerenderte Seite ist die Ausgabe von quarto render 1.8.25 mit
bibliography: literatur.bib und lang: de, ohne csl (Standardstil chicago-author-date).
"""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, outline, arrow, connector, numdot, codebox,
                  schild, stein, werkbank, text_width, INK, GRAY, GREEN, DARKORANGE, WHITE, CARD, CARDLINE, SANS, C)
from kap03 import mono, notiz, platte

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


# 2.6 Chunk-Optionen: derselbe Chunk viermal ------------------------------------------------------
def chunk_optionen():
    s = Canvas(6.8, 3.05)
    sx, sw, ax = 1.85, 3.4, 5.5
    for x, t in [(0.15, "OPTION"), (sx, "IM BERICHT"), (ax, "AUSGEFÜHRT")]:
        eyebrow(s, x, 0.12, 1.6, t, size=10.5)
    zeilen = [("ohne Option", True, True, True), ("echo=FALSE", False, True, True),
              ("eval=FALSE", True, False, False), ("include=FALSE", False, False, True)]
    for k, (opt, code, ausgabe, laeuft) in enumerate(zeilen):
        y, h = 0.5 + k * 0.62, 0.5
        if k == 0:
            text(s, 0.15, y, 1.6, h, [P(R(opt, size=11.5, italic=True, color=GRAY))], anchor="middle")
        else:
            text(s, 0.15, y, 1.6, h, mono(opt, size=11, align="start"), anchor="middle")
        rect(s, sx, y, sw, h, WHITE, CARDLINE, 1.0)
        if code:
            rect(s, sx + 0.1, y + 0.09, 1.6, h - 0.18, CARD, CARDLINE, 0.75)
            text(s, sx + 0.18, y, 1.5, h, mono("mean(mtcars$mpg)", size=10, align="start"), anchor="middle")
        if ausgabe:
            text(s, sx + 1.85, y, 1.5, h, mono("[1] 20.09062", size=10, color=GREEN, align="start"), anchor="middle")
        text(s, ax, y, 1.2, h, [P(R("ja" if laeuft else "nein", size=11.5, bold=True,
                                     color=GREEN if laeuft else DARKORANGE))], anchor="middle")
    return s


# 2.6.1 Rendern startet eine neue Sitzung; der Setup-Chunk füllt sie --------------------------------
SETUP = ["```{r setup, include=FALSE}", "library(tidyverse)", "library(mariposa)",
         'allbus <- read_spss("ALLBUS2023.sav")', "```"]


def sitzung(s, x, y, w, titel, voll):
    """Eine R-Sitzung: links die Werkbank (geladene Pakete), rechts das Environment (Objekte)."""
    card(s, x, y, w, 1.78)
    eyebrow(s, x + 0.12, y + 0.08, w - 0.2, titel, size=10.5)
    bw, ex = 1.84, x + 2.08
    eyebrow(s, x + 0.12, y + 0.42, bw, "WERKBANK", size=10)
    eyebrow(s, ex, y + 0.42, w - (ex - x) - 0.1, "ENVIRONMENT", size=10)
    werkbank(s, x + 0.12, y + 1.25, bw, ["tidyverse", "mariposa"] if voll else [], th=0.36, size=10)
    if voll:
        schild(s, ex, y + 0.72, "allbus", w=1.0)
        for k, kind in enumerate(["num", "txt"]):
            for j in range(2):
                stein(s, ex + 0.05 + k * 0.5, y + 1.2 + j * 0.2, 0.42, 0.14, kind, "")
        platte(s, ex, y + 1.6, 1.0)
    else:
        text(s, x + 0.12, y + 0.78, bw, 0.3, notiz("nur base R", size=10.5))
        text(s, ex, y + 0.95, 1.0, 0.3, notiz("leer", size=10.5))


def render_sitzung():
    s = Canvas(7.6, 3.42)
    w, y = 3.3, 0.12
    sitzung(s, 0.12, y, w, "NEUE R-SITZUNG", False)
    sitzung(s, 7.48 - w, y, w, "NACH DEM SETUP-CHUNK", True)
    mitte = 3.8
    arrow(s, mitte - 0.25, y + 0.75, w=0.5, h=0.3, color=GREEN)
    cw = 3.5
    connector(s, mitte, y + 1.05, mitte, 2.02, color=GREEN, width=1.5)
    codebox(s, mitte - cw / 2, 2.02, cw, SETUP, size=10)
    return s


# 2.9 Zitieren: Schlüssel, Verweis im Text, Ergebnis nach dem Rendern -------------------------------
def zitieren():
    s = Canvas(7.6, 3.62)
    codebox(s, 0.15, 0.12, 7.3, ["Wie @Goodman2016 zeigt, lässt sich Reproduzierbarkeit unterschiedlich definieren.",
                                 "Für eine ausführliche Behandlung siehe auch [@Wickham2023]."],
            size=10, label="analyse.qmd")
    oben = 1.2
    codebox(s, 0.15, oben, 2.3, ["@article{Goodman2016,", "  …", "}", "@book{Wickham2023,", "  …", "}"],
            size=10, label="literatur.bib")
    px, pw, ph = 3.32, 4.13, 2.3
    text(s, 2.5, oben + ph / 2 - 0.42, 0.8, 0.28, [P(R("Render", size=10.5, bold=True), align=C)])
    arrow(s, 2.64, oben + ph / 2 - 0.14, w=0.5, h=0.28, color=GRAY)
    rect(s, px, oben, pw, ph, WHITE, CARDLINE, 1.0)
    st = dict(size=10)
    text(s, px + 0.15, oben + 0.12, pw - 0.3, ph - 0.2, [
        P(R("Wie Goodman, Fanelli, und Ioannidis (2016) zeigt, lässt sich Reproduzierbarkeit unterschiedlich "
            "definieren. Für eine ausführliche Behandlung siehe auch (Wickham und Grolemund 2023).", size=10.5),
          ls=1.05, sa=7),
        P(R("Literatur", size=12, bold=True), sa=3),
        P(R("Goodman, Steven N., Daniele Fanelli, und John P. A. Ioannidis. 2016. „What does research "
            "reproducibility mean?“ ", **st), R("Science Translational Medicine", italic=True, **st),
          R(" 8 (341): 341ps12.", **st), ls=1.05, sa=4),
        P(R("Wickham, Hadley, und Garrett Grolemund. 2023. ", **st), R("R for Data Science", italic=True, **st),
          R(". 2. Aufl. O’Reilly.", **st), ls=1.05),
    ])
    return s


FIGUREN = {
    "k02-qmd-schichten": qmd_schichten,
    "k02-chunk-optionen": chunk_optionen,
    "k02-render-sitzung": render_sitzung,
    "k02-zitieren": zitieren,
}
