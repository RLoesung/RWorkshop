"""Abbildungen für Kap. 3 „Programmiersprache R“ (BILDER.md §6). Werte aus den Buch-Chunks."""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, tokens, stein, schild, turm, arrow,
                  outline, numdot, INK, GRAY, GREEN, ORANGE, CARDLINE, DARKORANGE, MONO, C, RT)


def mono(t, size=11, color=INK, bold=True, align=C):
    return [P(R(t, font=MONO, size=size, bold=bold, color=color), align=align)]


def notiz(t, size=11, color=GRAY, align=C, italic=True):
    return [P(R(t, size=size, italic=italic, color=color), align=align, ls=1.0)]


def platte(s, x, base, w):
    rect(s, x, base, w, 0.07, GRAY)


# 3.5 Legende der Bildsprache -------------------------------------------------------------------
def legende():
    s = Canvas(7.8, 4.55)
    eyebrow(s, 0.15, 0.12, 2.6, "WERT = STEIN")
    zeilen = [("num", "1", "Zahl", "numeric", None), ("txt", '"Anna"', "Text", "character", None),
              ("log", "TRUE", "Wahrheitswert", "logical", None), ("na", "", "fehlender Wert", "NA", None),
              ("num", "1", "mit Wertelabel", "Aufkleber", "MANN")]
    for k, (kind, v, lab, typ, tag) in enumerate(zeilen):
        y = 0.62 + k * 0.62
        stein(s, 0.15, y, 1.2, 0.4, kind, v, tag=tag, size=11)
        text(s, 1.5, y - 0.03, 1.7, 0.25, [P(R(lab, size=11.5, bold=True))])
        text(s, 1.5, y + 0.2, 1.7, 0.22, mono(typ, size=10, color=GRAY, bold=False, align="start"))

    eyebrow(s, 3.3, 0.12, 1.6, "VEKTOR = TURM")
    schild(s, 3.35, 0.5, "zahlen", w=1.0)
    turm(s, 3.35, 2.45, 1.0, 0.34, "num", ["3", "2", "1"])
    platte(s, 3.25, 2.45, 1.2)
    text(s, 3.05, 2.6, 1.6, 0.25, notiz("ein Datentyp", size=10.5))

    eyebrow(s, 4.9, 0.12, 2.9, "DATENSATZ = BAUPLATTE")
    text(s, 4.9, 0.55, 1.3, 0.25, mono("geschlecht", size=10.5))
    text(s, 6.3, 0.55, 1.1, 0.25, mono("alter", size=10.5))
    for i, (g, a) in enumerate([("Mann", "34"), ("Frau", "41"), ("Divers", "52")]):
        y = 0.92 + i * 0.47
        stein(s, 5.0, y, 1.1, 0.36, "txt", g, size=10.5)
        stein(s, 6.3, y, 1.0, 0.36, "num", a, size=10.5)
    platte(s, 4.9, 2.27, 2.5)
    outline(s, 4.92, 1.32, 2.46, 0.48, color=ORANGE, lw=1.75)
    text(s, 4.85, 2.4, 2.65, 0.25, notiz("eine Reihe = ein Fall", size=10.5, color=DARKORANGE))
    text(s, 4.85, 2.65, 2.65, 0.25, notiz("ein Turm = eine Variable", size=10.5))

    rect(s, 0.15, 3.68, 7.5, 0.01, CARDLINE)
    eyebrow(s, 0.15, 3.82, 2.0, "CODE-FARBEN")
    mids, _ = tokens(s, 2.0, 3.77, [("zahlen", "obj"), ("|>", "sym"), ("round", "fun"), ("(", "sym"),
                                     ("digits = 1", "arg"), (")", "sym")], size=12, h=0.34)
    for i, lab in [(0, "Objekt"), (2, "Funktion"), (4, "Argument")]:
        text(s, mids[i] - 0.7, 4.16, 1.4, 0.25, notiz(lab, size=10.5))
    return s


# 3.5.1 Drei Türme aus dem Chunk `vectors` ----------------------------------------------------
def turm_fig():
    s = Canvas(6.0, 3.15)
    base, h = 2.75, 0.34
    oben = base - 5 * (h + 0.07) - 0.5
    spalten = [(0.35, 1.0, "zahlen", "num", ["5", "4", "3", "2", "1"], "numeric"),
               (2.3, 1.35, "namen", "txt", ['"Carla"', '"Boris"', '"Anna"'], "character"),
               (4.4, 1.2, "flags", lambda i: ["na", "log", "log"][i], ["", "FALSE", "TRUE"], "logical")]
    for x, w, name, kind, werte, typ in spalten:
        schild(s, x, oben, name, w=w)
        turm(s, x, base, w, h, kind, werte)
        platte(s, x - 0.1, base, w + 0.2)
        text(s, x - 0.3, base + 0.12, w + 0.6, 0.25, mono(typ, size=10.5, color=GRAY, bold=False))
    text(s, 4.4, base - 0.38 + 0.02, 1.2, 0.3, mono("NA", size=11, color=GRAY))
    return s


# 3.5.1 Rangfolge beim Mischen (neuer Chunk `coercion`) ---------------------------------------
def rangfolge():
    s = Canvas(7.8, 3.45)
    base, h, w = 2.3, 0.36, 0.95
    beispiele = [(0.15, "c(1, TRUE, FALSE)", ["log", "log", "num"], ["FALSE", "TRUE", "1"],
                  "num", ["0", "1", "1"], "[1] 1 1 0", "numeric"),
                 (3.0, 'c(1, "Anna", TRUE)', ["log", "txt", "num"], ["TRUE", '"Anna"', "1"],
                  "txt", ['"TRUE"', '"Anna"', '"1"'], '[1] "1" "Anna" "TRUE"', "character")]
    for x, code, kinds, vorher, neu, nachher, out, typ in beispiele:
        turm(s, x + 0.1, base, w, h, (lambda kk: (lambda i: kk[i]))(kinds), vorher)
        arrow(s, x + 1.2, base - 0.75, w=0.4, h=0.28, color=GREEN)
        turm(s, x + 1.75, base, w, h, neu, nachher)
        platte(s, x, base, 2.7)
        text(s, x - 0.05, base + 0.12, 2.95, 0.25, mono(code, size=10.5))
        text(s, x - 0.05, base + 0.4, 2.95, 0.25, mono(out, size=10.5, color=GREEN))
        label_box(s, x + 1.67, 0.2, 1.1, 0.27, typ, GREEN, size=10)
    card(s, 5.95, 0.15, 1.75, 3.1)
    eyebrow(s, 6.07, 0.24, 1.6, "RANGFOLGE")
    for k, (kind, v, lab) in enumerate([("log", "TRUE", "logical"), ("num", "1", "numeric"), ("txt", '"1"', "character")]):
        y = 0.75 + k * 0.85
        stein(s, 6.07, y, 0.7, 0.34, kind, v, size=10.5)
        text(s, 6.85, y + 0.06, 0.85, 0.22, mono(lab, size=10, color=GRAY, bold=False, align="start"))
        if k < 2:
            from lego import down_arrow
            down_arrow(s, 6.3, y + 0.42, w=0.24, h=0.34, color=GREEN)
    return s


# 3.5.3 Tibble aus dem Chunk `tibble-create` --------------------------------------------------
def tibble_fig():
    s = Canvas(7.4, 3.5)
    schild(s, 0.15, 0.15, "befragte", w=1.25)
    text(s, 1.55, 0.2, 1.6, 0.3, mono("4 × 2", size=11, color=GRAY, align="start"))
    xs, ws = [0.3, 1.85], [1.3, 1.1]
    for x, w, n, typ in zip(xs, ws, ["geschlecht", "alter"], ["<fct>", "<dbl>"]):
        text(s, x - 0.1, 0.62, w + 0.2, 0.25, mono(n, size=11))
        text(s, x - 0.1, 0.84, w + 0.2, 0.22, mono(typ, size=10, color=GRAY, bold=False))
    base, h = 3.05, 0.38
    for i, (g, a) in enumerate([("Mann", "34"), ("Frau", "41"), ("Mann", "28"), ("Divers", "52")]):
        y = base - (4 - i) * (h + 0.07)
        stein(s, xs[0], y, ws[0], h, "txt", g, size=11)
        stein(s, xs[1], y, ws[1], h, "num", a, size=11)
    platte(s, 0.15, base, 3.0)
    y1 = base - 3 * (h + 0.07)
    outline(s, 0.2, y1 - 0.1, 2.9, h + 0.16, color=ORANGE, lw=1.75)
    outline(s, xs[1] - 0.07, base - 4 * (h + 0.07) - 0.11, ws[1] + 0.14, 4 * (h + 0.07) + 0.06, color=GREEN, lw=1.75)
    card(s, 3.55, 1.28, 3.7, 0.66)
    text(s, 3.7, 1.35, 3.45, 0.6, [P(R("Eine Reihe ist ein Fall:", size=11.5, bold=True, color=DARKORANGE)),
                                   P(R("die zweite befragte Person, Frau, 41 Jahre.", size=11), sb=2, ls=1.0)])
    card(s, 3.55, 2.12, 3.7, 0.93)
    text(s, 3.7, 2.2, 3.45, 0.85, [P(R("Ein Turm ist eine Variable:", size=11.5, bold=True, color=GREEN)),
                                    P(R("befragte$alter", font=MONO, size=10.5, bold=True), sb=3),
                                    P(R("[1] 34 41 28 52", font=MONO, size=10.5, bold=True, color=GREEN), sb=1)])
    return s


# 3.7.1 Pipe aus dem Chunk `pipe-native` ------------------------------------------------------
def _maschine(s, x, y, name, rest, h=0.95, size=12):
    """Funktion als Kasten: Name, leeres erstes Feld (gestrichelt), Rest der Klammer. Gibt Feld-x und Breite zurück."""
    from lego import text_width
    wn = text_width(name, MONO, size, True)
    wr = text_width(rest, MONO, size, True)
    fw = 0.6
    w = 0.12 + wn + 0.06 + fw + 0.06 + wr + 0.12
    rect(s, x, y, w, h, "#FFFFFF", GREEN, 1.75)
    text(s, x + 0.12, y, wn + 0.05, h, mono(name, size=size, color=GREEN, align="start"), anchor="middle")
    fx = x + 0.12 + wn + 0.06
    rect(s, fx, y + 0.1, fw, h - 0.2, "#FAF7F1", GRAY, 1.0, dash=True)
    text(s, fx + fw + 0.06, y, wr + 0.05, h, mono(rest, size=size, align="start"), anchor="middle")
    return fx, fw, w


def _pfeil_pipe(s, x, y):
    text(s, x, y - 0.32, 0.5, 0.3, mono("|>", size=12, color=GREEN))
    arrow(s, x + 0.05, y, w=0.4, h=0.26, color=GREEN)


def _mini_turm(s, x, base, w, n):
    for i in range(n):
        rect(s, x, base - (i + 1) * 0.11, w, 0.08, "#85B7EB", "#042C53", 0.5)


def pipe():
    s = Canvas(7.2, 4.75)
    h = 0.28
    reihen = [
        (1.35, "zahlen", ["1.55", "1.44", "1.33", "1.22", "1.11"], "round(", ", digits = 1)", 5,
         ["1.6", "1.4", "1.3", "1.2", "1.1"], "round(zahlen, digits = 1)"),
        (3.65, None, ["1.6", "1.4", "1.3", "1.2", "1.1"], "head(", ", n = 3)", 5,
         ["1.3", "1.2", "1.1"], "head(round(zahlen, digits = 1), n = 3)"),
    ]
    for k, (mitte, name, werte, fname, rest, n, ergebnis, aus) in enumerate(reihen):
        base = mitte + 0.9
        numdot(s, 0.1, mitte - 0.55, k + 1, fill=GREEN, d=0.3, size=11)
        if name:
            schild(s, 0.42, base - 5 * (h + 0.07) - 0.5, name, w=0.86)
        turm(s, 0.5, base, 0.7, h, "num", werte)
        platte(s, 0.45, base, 0.8)
        _pfeil_pipe(s, 1.35, mitte - 0.13)
        fx, fw, mw = _maschine(s, 1.9, mitte - 0.47, fname, rest)
        _mini_turm(s, fx + 0.12, mitte + 0.38, fw - 0.24, n)
        text(s, 1.6, mitte + 0.55, mw + 0.6, 0.25, mono("= " + aus, size=10, color=GREEN))
        ax = 1.9 + mw + 0.15
        arrow(s, ax, mitte - 0.13, w=0.4, h=0.26, color=GRAY)
        turm(s, ax + 0.55, base, 0.7, h, "num", ergebnis)
        platte(s, ax + 0.5, base, 0.8)
    return s


FIGUREN = {
    "k03-legende": legende,
    "k03-turm": turm_fig,
    "k03-rangfolge": rangfolge,
    "k03-tibble": tibble_fig,
    "k03-pipe": pipe,
}
