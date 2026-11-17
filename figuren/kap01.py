"""Abbildungen für Kap. 1 „RStudio“ (BILDER.md §6). Namen aus dem Kapitel.

Gezeigt werden nur Pakete und Funktionen, die Kap. 1 selbst nennt: die Pakete aus 1.6.1 (tidyverse mit dplyr,
tidyr, ggplot2, readr, purrr, tibble, stringr, forcats und lubridate; mariposa; patchwork) und die
mariposa-Funktionen read_spss() (1.4.4, 1.5.1) und w_mean() (1.5.3).

1.4.4: Annas Pfad aus dem Chunk getwd-demo, das Projekt R-Workshop aus Übung 1, das Dokument 01-erste_schritte.qmd aus
der Checkliste nach 1.7, der absolute Pfad aus dem Vorsicht-Kasten (getwd-demo + Dateiname). Der zweite Rechner
(Boris, Windows) ist ein Beispiel; Boris Müller ist der Co-Autor aus 2.5. Geprüft in R 4.5.3: read_spss() mit dem
absoluten Pfad bricht auf einem Rechner ohne diesen Ordner ab („File '…' does not exist.“).
1.4: Die vier Bereiche von RStudio 2026.01 mit dem Chunk aus 1.5.2 im Quarto-Dokument 01-erste_schritte.qmd; Reiter
wie in RStudio, die Zwecke nach der Tabelle in 1.4.
1.7: Die Hilfeseite zu ?mean in R 4.5.3 (Kopf, Titel, Überschriften, Usage und Examples wörtlich, Fließtext als
graue Balken).
"""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, arrow, codebox, connector, numdot, kachel,
                  werkbank, kreis, text_width, INK, GRAY, GREEN, ORANGE, CARD, CARDLINE, DARKORANGE, WHITE, PALE,
                  MONO_EM, SANS, C, L, RT)
from kap03 import mono, notiz


def paket(s, x, y, w, h, name, size=11, fill=WHITE):
    """Ein Paket: Kasten mit dunkler Kante und dem Paketnamen."""
    rect(s, x, y, w, h, fill, INK, 1.0)
    text(s, x, y, w, h, mono(name, size=size), anchor="middle")


def funktion(s, x, y, w, h, name, size=11):
    """Eine Funktion: grüner Kasten."""
    label_box(s, x, y, w, h, name, GREEN, size=size, rounded=False)


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
    eyebrow(s, 4.1, 0.12, 3.0, "WERKBANK: AKTIV", size=10.5)
    werkbank(s, 4.15, 1.42, 3.3, pakete, beine=b2 + 0.08 - 1.56, th=th)
    text(s, 4.1, 1.9, 3.3, 0.25, notiz("einmal pro R-Sitzung", size=10.5, align=L))
    codebox(s, 4.1, 2.2, 2.85, [f"library({p})" for p in pakete], size=10)
    return s


# 1.4.4 Arbeitsverzeichnis auf zwei Rechnern (Chunk getwd-demo, Vorsicht-Kasten) ------------------
ABSOLUT = "/Users/anna/Documents/R-Workshop/ALLBUS2023.sav"
DATEIEN = ["R-Workshop.Rproj", "01-erste_schritte.qmd", "ALLBUS2023.sav"]


def ordner(s, x, y, name, dateien, w=1.92, size=10, fh=0.27, gap=0.06):
    """Ein Ordner: Reiter mit dem Namen, darin die Dateien als Kacheln untereinander. Gibt die Höhe zurück."""
    tw = 0.24 + len(name) * 0.612 * size / 72
    rect(s, x, y, tw, 0.27, CARD, GRAY, 1.0)
    text(s, x, y, tw, 0.27, mono(name, size=size), anchor="middle")
    bh = 0.1 + len(dateien) * fh + (len(dateien) - 1) * gap + 0.1
    rect(s, x, y + 0.25, w, bh, CARD, GRAY, 1.0)
    for k, d in enumerate(dateien):
        fy = y + 0.35 + k * (fh + gap)
        rect(s, x + 0.08, fy, w - 0.16, fh, WHITE, CARDLINE, 0.75)
        text(s, x + 0.08, fy, w - 0.16, fh, mono(d, size=size), anchor="middle")
    return 0.25 + bh


def arbeitsverzeichnis():
    s = Canvas(7.6, 3.6)
    # die beiden Zeilen wie in einem Code-Kasten, mit Platz für die Nummern
    zeilen = ['read_spss("ALLBUS2023.sav")', f'read_spss("{ABSOLUT}")']
    zh, bh = 0.3, 0.12 + 2 * 0.3 + 0.12
    rect(s, 0.5, 0.15, 5.8, bh, WHITE, CARDLINE, 0.75)
    rect(s, 0.5, 0.15, 0.07, bh, INK)
    for k, z in enumerate(zeilen):
        yy = 0.27 + k * zh
        numdot(s, 0.15, yy + zh / 2 - 0.12, k + 1, fill=GREEN, d=0.24, size=10)
        text(s, 0.72, yy, 5.5, zh, mono(z, size=10.5, align="start"), anchor="middle")
    rechner = [("RECHNER VON ANNA", "/Users/anna/Documents/R-Workshop", [True, True]),
               ("RECHNER VON BORIS", "C:/Users/boris/Documents/R-Workshop", [True, False])]
    cw, ch, cy = 3.68, 2.38, 1.1
    for j, (wer, pfad, ok) in enumerate(rechner):
        x0 = 0.12 + j * (cw + 0.08)
        card(s, x0, cy, cw, ch)
        eyebrow(s, x0 + 0.12, cy + 0.08, cw - 0.2, wer, size=10.5)
        text(s, x0 + 0.12, cy + 0.42, cw - 0.2, 0.22, mono("getwd()", size=10, align="start"))
        text(s, x0 + 0.12, cy + 0.63, cw - 0.15, 0.22, mono(f'[1] "{pfad}"', size=10, color=GREEN, align="start"))
        oy = cy + 0.98
        oh = ordner(s, x0 + 0.12, oy, "R-Workshop", DATEIEN)
        mitte = oy + 0.25 + (oh - 0.25) / 2
        rx = x0 + 0.12 + 1.92 + 0.16
        for k, gut in enumerate(ok):
            yy = mitte - 0.31 + k * 0.38
            numdot(s, rx, yy, k + 1, fill=GREEN if gut else DARKORANGE, d=0.24, size=10)
            text(s, rx + 0.32, yy - 0.01, cw - (rx - x0) - 0.36, 0.26,
                 [P(R("gefunden" if gut else "nicht gefunden", size=10.5, bold=True,
                      color=GREEN if gut else DARKORANGE))], anchor="middle")
    return s


# 1.7 Hilfeseite zu ?mean (R 4.5.3) --------------------------------------------------------------
def balken(s, x, y, w):
    """Graue Linie: Fließtext, der hier nicht wiedergegeben ist."""
    rect(s, x, y, w, 0.07, CARDLINE, rx=0.03)


def code_markiert(s, x, y, teile, size=10, h=0.22):
    """Eine Code-Zeile aus Stücken; markierte Stücke (Argumente) bekommen den hellorangen Grund der Code-Farben.
    Jedes Stück steht an seiner eigenen Stelle, damit der Grund auch bei schmaleren Schriften unter dem Text bleibt."""
    for t, markiert in teile:
        w = len(t) * MONO_EM * size / 72
        kern = t.strip()
        vorne = (len(t) - len(t.lstrip())) * MONO_EM * size / 72
        if markiert:
            rect(s, x + vorne - 0.03, y, len(kern) * MONO_EM * size / 72 + 0.06, h, PALE)
        text(s, x + vorne, y, w + 0.1, h, mono(kern, size=size, align="start"), anchor="middle")
        x += w


def hilfeseite():
    s = Canvas(7.3, 4.92)
    px, pw = 0.15, 4.75
    ix, iw = px + 0.2, pw - 0.35
    rect(s, px, 0.12, pw, 4.68, WHITE, CARDLINE, 1.0)
    text(s, ix, 0.2, iw, 0.22, [P(R("mean {base}", size=10, color=GRAY))])
    text(s, ix, 0.2, iw, 0.22, [P(R("R Documentation", size=10, color=GRAY), align=RT)])
    text(s, ix, 0.42, iw, 0.3, [P(R("Arithmetic Mean", size=14, bold=True))])
    lh = 0.21
    beschriftung = {}

    def kopf(yy, titel, wort=None, farbe=INK):
        text(s, ix, yy, iw, 0.24, [P(R(titel, size=11.5, bold=True, color=farbe))])
        if wort:
            beschriftung[wort] = yy

    kopf(0.78, "Description", "Funktionsbeschreibung")
    text(s, ix, 1.0, iw, 0.22, [P(R("Generic function for the (trimmed) arithmetic mean.", size=10.5))])
    kopf(1.32, "Usage", "Default-Werte")
    text(s, ix, 1.56, iw, lh, mono("mean(x, ...)", size=10, align="start"))
    text(s, ix, 1.56 + lh, iw, lh, mono("## Default S3 method:", size=10, color=GRAY, align="start"))
    code_markiert(s, ix, 1.56 + 2 * lh, [("mean(x, ", False), ("trim = 0", True), (", ", False),
                                         ("na.rm = FALSE", True), (", ...)", False)])
    kopf(2.32, "Arguments", "Argumente")
    for k, (name, laenge) in enumerate([("x", 3.2), ("trim", 3.4), ("na.rm", 3.4), ("...", 2.6)]):
        yy = 2.56 + k * 0.22
        code_markiert(s, ix, yy, [(name, name == "na.rm")], h=0.2)
        balken(s, ix + 0.75, yy + 0.07, laenge)
    kopf(3.5, "Value, References, See Also", farbe=GRAY)
    kopf(3.84, "Examples", "Beispiele")
    for k, z in enumerate(["x <- c(0:10, 50)", "xm <- mean(x)", "c(xm, mean(x, trim = 0.10))"]):
        text(s, ix, 4.08 + k * lh, iw, lh, mono(z, size=10, align="start"))
    # Beschriftungen rechts, auf Höhe der Überschriften
    lx = px + pw + 0.35
    for wort, yy in beschriftung.items():
        connector(s, px + pw + 0.06, yy + 0.12, lx - 0.08, yy + 0.12, color=GRAY, width=1.0)
        text(s, lx, yy, s.w - 0.1 - lx, 0.24, [P(R(wort, size=11.5, bold=True))])
    return s


# 1.4 Die vier Bereiche (Tabelle in 1.4, Beispiel aus 1.5.2) ------------------------------------
# Nummer: (x, y, Breite, Höhe, Zweck, Reiter, aktiver Reiter)
BEREICHE = {
    1: (0.2, 0.5, 3.5, 2.1, "Code schreiben und speichern", ["01-erste_schritte.qmd"], 0),
    2: (0.2, 2.7, 3.5, 1.85, "Code ausprobieren, Output ansehen", ["Console", "Terminal", "Background Jobs"], 0),
    3: (3.8, 0.5, 3.6, 2.1, "Objekte und Befehlsverlauf", ["Environment", "History", "Connections", "Tutorial"], 0),
    4: (3.8, 2.7, 3.6, 1.85, "Dateien, Grafiken, Pakete, Hilfe", ["Files", "Plots", "Packages", "Help", "Viewer"], 0),
}
REITER_PT, REITER_PAD = 10.5, 0.16


def reiterzeilen():
    """Je Bereich: (x, Breite, rechtes Ende der Reiterzeile) in Zoll."""
    out = {}
    for n, (x, y, w, h, zweck, reiter, aktiv) in BEREICHE.items():
        ende = x + 0.1 + sum(text_width(r, SANS, REITER_PT, k == aktiv) + REITER_PAD for k, r in enumerate(reiter))
        if n == 1:
            ende += 0.1 + 0.62                                  # Run-Knopf rechts in der Zeile
        out[n] = (x, w, ende)
    return out


def bereich(s, n):
    """Ein Bereich: Nummer und Zweck, darunter die Reiter wie in RStudio, darunter ein weißes Inhaltsfeld.
    Gibt (x, y) der ersten Inhaltszeile und die Breite des Feldes zurück."""
    x, y, w, h, zweck, reiter, aktiv = BEREICHE[n]
    rect(s, x, y, w, h, CARD, CARDLINE, 0.75)
    numdot(s, x + 0.1, y + 0.1, n, fill=GREEN, d=0.28, size=10)
    text(s, x + 0.46, y + 0.08, w - 0.56, 0.32, [P(R(zweck, size=11.5, bold=True))], anchor="middle")
    rx = x + 0.1
    for k, r in enumerate(reiter):
        rw = text_width(r, SANS, REITER_PT, k == aktiv) + REITER_PAD
        if k == aktiv:
            rect(s, rx, y + 0.46, rw, 0.27, WHITE, CARDLINE, 0.75)
        text(s, rx, y + 0.46, rw, 0.27, [P(R(r, size=REITER_PT, bold=k == aktiv, color=INK if k == aktiv else GRAY),
                                          align=C)], anchor="middle")
        rx += rw
    rect(s, x + 0.1, y + 0.73, w - 0.2, h - 0.83, WHITE, CARDLINE, 0.75)
    return x + 0.2, y + 0.8, w - 0.4


def zeile(s, x, y, w, t, color=INK, font="mono", bold=False, size=10):
    """Eine Zeile im Inhaltsfeld, linksbündig."""
    if font == "mono":
        text(s, x, y, w, 0.21, mono(t, size=size, color=color, bold=bold, align="start"), anchor="middle")
    else:
        text(s, x, y, w, 0.21, [P(R(t, size=size, bold=bold, color=color))], anchor="middle")


def oberflaeche():
    s = Canvas(7.6, 4.75)
    wx, wy, ww, wh = 0.1, 0.1, 7.4, 4.55
    rect(s, wx, wy, ww, wh, WHITE, INK, 1.5)
    rect(s, wx, wy, ww, 0.3, INK)
    for k, farbe in enumerate(["#E06C5A", ORANGE, GREEN]):
        kreis(s, wx + 0.19 + k * 0.2, wy + 0.15, 0.06, farbe)
    text(s, wx, wy, ww, 0.3, [P(R("RStudio", size=10.5, bold=True, color=WHITE), align=C)], anchor="middle")
    text(s, wx, wy, ww - 0.15, 0.3, [P(R("R-Workshop", size=10, color=WHITE), align=RT)], anchor="middle")
    lh = 0.21
    # 1 Editor: der Chunk aus 1.5.2 mit seinem Ergebnis darunter, rechts der Run-Knopf
    x, y, w = bereich(s, 1)
    bx, by = BEREICHE[1][0] + BEREICHE[1][2] - 0.72, BEREICHE[1][1] + 0.47
    rect(s, bx, by, 0.62, 0.25, WHITE, CARDLINE, 0.75)
    text(s, bx, by, 0.62, 0.25, [P(R("→ ", size=10, bold=True, color=GREEN), R("Run", size=10, bold=True),
                                   align=C)], anchor="middle")
    rect(s, x - 0.06, y - 0.02, w + 0.12, 4 * lh + 0.04, CARD)            # Chunk: grau hinterlegt wie in RStudio
    for k, (z, farbe) in enumerate([("```{r}", GRAY), ("var1 <- 2 + 3", INK), ("var1", INK), ("```", GRAY)]):
        zeile(s, x, y + k * lh, w, z, color=farbe)
    oy = y + 4 * lh + 0.06
    rect(s, x - 0.06, oy, w + 0.12, lh + 0.06, WHITE, CARDLINE, 0.75)     # Ergebnis unter dem Chunk
    zeile(s, x, oy + 0.03, w, "[1] 5", color=GREEN)
    # 2 Konsole: dieselben Zeilen, ausgeführt
    x, y, w = bereich(s, 2)
    for k, (z, farbe) in enumerate([("> var1 <- 2 + 3", INK), ("> var1", INK), ("[1] 5", GREEN), (">", INK)]):
        zeile(s, x, y + k * lh, w, z, color=farbe)
    # 3 Environment: var1 mit dem Wert 5
    x, y, w = bereich(s, 3)
    zeile(s, x, y, w, "Global Environment", color=GRAY, font="sans")
    zeile(s, x, y + lh, w, "Values", color=GRAY, font="sans", bold=True)
    zeile(s, x, y + 2 * lh, 1.2, "var1")
    zeile(s, x + 1.4, y + 2 * lh, 1.0, "5")
    # 4 Files: der Projektordner aus 1.4.4
    x, y, w = bereich(s, 4)
    zeile(s, x, y, w, "Home > Documents > R-Workshop", color=GRAY, font="sans")
    for k, d in enumerate(["01-erste_schritte.qmd", "ALLBUS2023.sav", "R-Workshop.Rproj"]):
        zeile(s, x, y + (k + 1) * lh, w, d)
    return s


FIGUREN = {
    "k01-oberflaeche": oberflaeche,
    "k01-oekosystem": oekosystem,
    "k01-regal-werkbank": regal_werkbank,
    "k01-arbeitsverzeichnis": arbeitsverzeichnis,
    "k01-hilfeseite": hilfeseite,
}
