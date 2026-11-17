"""Abbildungen für Kap. 1 „RStudio“ (BILDER.md §6). Namen aus dem Kapitel.

Gezeigt werden nur Pakete und Funktionen, die Kap. 1 selbst nennt: die Pakete aus 1.6.1 (tidyverse mit dplyr,
tidyr, ggplot2, readr, purrr, tibble, stringr, forcats und lubridate; mariposa; patchwork) und die
mariposa-Funktionen read_spss() (1.4.4, 1.5.1) und w_mean() (1.5.3).
"""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, arrow, codebox, INK, GRAY, GREEN, ORANGE,
                  CARDLINE, WHITE, C, L)
from kap03 import mono, notiz


def paket(s, x, y, w, h, name, size=11, fill=WHITE):
    """Ein Paket: Kasten mit dunkler Kante und dem Paketnamen."""
    rect(s, x, y, w, h, fill, INK, 1.0)
    text(s, x, y, w, h, mono(name, size=size), anchor="middle")


def funktion(s, x, y, w, h, name, size=11):
    """Eine Funktion: grüner Kasten."""
    label_box(s, x, y, w, h, name, GREEN, size=size, rounded=False)


def kachel(s, x, y, w, h, name, size=11):
    """Ein installiertes Paket als Kachel im Regal oder auf der Werkbank."""
    rect(s, x, y, w, h, WHITE, CARDLINE, 1.0, rx=0.07)
    text(s, x, y, w, h, mono(name, size=size), anchor="middle")


# 1.6 Funktion, Paket, Ökosystem (Pakete aus 1.6.1, Funktionen aus 1.4.4 und 1.5.3) -------------
def oekosystem():
    s = Canvas(7.6, 3.3)
    # Ökosystem: das tidyverse mit den Paketen, die install.packages("tidyverse") laut 1.6.1 installiert
    fx, fy, fw, fh = 0.15, 0.15, 4.7, 2.2
    rect(s, fx, fy, fw, fh, None, GREEN, 1.5, dash=True)
    text(s, fx, fy + 0.08, fw, 0.3, mono("tidyverse", size=13, color=GREEN))
    text(s, fx, fy + 0.38, fw, 0.25, notiz("Datenmanipulation und Visualisierung", size=10.5))
    pakete = ["dplyr", "tidyr", "ggplot2", "readr", "purrr", "tibble", "stringr", "forcats", "lubridate"]
    tw, th, gx, gy = 1.3, 0.36, 0.13, 0.12
    x0 = fx + (fw - 3 * tw - 2 * gx) / 2
    for i, name in enumerate(pakete):
        paket(s, x0 + (i % 3) * (tw + gx), fy + 0.8 + (i // 3) * (th + gy), tw, th, name)
    # Paket: mariposa mit zwei seiner Funktionen
    mx, mw = 5.2, 2.25
    rect(s, mx, fy, mw, fh, WHITE, INK, 1.25)
    text(s, mx, fy + 0.08, mw, 0.3, mono("mariposa", size=13))
    text(s, mx, fy + 0.38, mw, 0.25, notiz("statistische Analyse", size=10.5))
    for k, fn in enumerate(["read_spss()", "w_mean()"]):
        funktion(s, mx + 0.25, fy + 0.8 + k * (th + gy), mw - 0.5, th, fn)
    text(s, mx, fy + 0.8 + 2 * (th + gy) - 0.04, mw, 0.3, [P(R("…", size=16, bold=True, color=GRAY), align=C)])
    # Legende: drei Ebenen, von klein nach groß
    ly, lh = 2.6, 0.55
    lw = (7.45 - 0.15 - 2 * 0.15) / 3
    for k, wort in enumerate(["Funktion", "Paket", "Ökosystem"]):
        x = 0.15 + k * (lw + 0.15)
        card(s, x, ly, lw, lh)
        bx, by, bw, bh = x + 0.18, ly + 0.13, 0.6, 0.29
        if k == 0:
            rect(s, bx, by, bw, bh, GREEN)
        elif k == 1:
            rect(s, bx, by, bw, bh, WHITE, INK, 1.0)
        else:
            rect(s, bx, by, bw, bh, None, GREEN, 1.5, dash=True)
        text(s, bx + bw + 0.18, ly, lw - bw - 0.45, lh, [P(R(wort, size=12, bold=True))], anchor="middle")
    return s


# 1.6.2 Regal und Werkbank: Chunks in 1.6.1 (install.packages) und 1.6.2 (library) ----------------
def regal_werkbank():
    s = Canvas(7.6, 3.25)
    pakete = ["tidyverse", "mariposa", "patchwork"]
    th = 0.42
    # Regal: zwei Bretter zwischen zwei Seitenwänden
    rx, rw = 0.25, 2.5
    eyebrow(s, 0.15, 0.12, 2.8, "REGAL: INSTALLIERT", size=10.5)
    b1, b2 = 1.0, 1.7
    for by in (b1, b2):
        rect(s, rx, by, rw, 0.08, INK)
    for sx in (rx, rx + rw - 0.06):
        rect(s, sx, 0.45, 0.06, b2 + 0.08 - 0.45, INK)
    iw = (rw - 0.12 - 3 * 0.07) / 2
    kachel(s, rx + 0.06 + 0.07, b1 - th - 0.02, iw, th, pakete[0])
    kachel(s, rx + 0.06 + 0.14 + iw, b1 - th - 0.02, iw, th, pakete[1])
    kachel(s, rx + 0.06 + 0.07, b2 - th - 0.02, iw, th, pakete[2])
    text(s, 0.15, 1.9, 2.8, 0.25, notiz("einmal pro Rechner", size=10.5, align=L))
    codebox(s, 0.15, 2.2, 2.85, [f'install.packages("{p}")' for p in pakete], size=10)
    # vom Regal auf die Werkbank
    arrow(s, 3.2, 1.0, w=0.75, h=0.36, color=ORANGE)
    # Werkbank: Platte mit zwei Beinen, darauf die drei Pakete
    wx, ww = 4.15, 3.3
    eyebrow(s, 4.1, 0.12, 3.0, "WERKBANK: AKTIV", size=10.5)
    rect(s, wx, 1.42, ww, 0.14, INK)
    for lx in (wx + 0.15, wx + ww - 0.27):
        rect(s, lx, 1.56, 0.12, b2 + 0.08 - 1.56, INK)
    kw = (ww - 0.1 - 2 * 0.08) / 3
    for k, p in enumerate(pakete):
        kachel(s, wx + 0.05 + k * (kw + 0.08), 1.42 - th - 0.02, kw, th, p)
    text(s, 4.1, 1.9, 3.3, 0.25, notiz("einmal pro R-Sitzung", size=10.5, align=L))
    codebox(s, 4.1, 2.2, 2.85, [f"library({p})" for p in pakete], size=10)
    return s


FIGUREN = {
    "k01-oekosystem": oekosystem,
    "k01-regal-werkbank": regal_werkbank,
}
