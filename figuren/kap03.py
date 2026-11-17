"""Abbildungen für Kap. 3 „Programmiersprache R“ (BILDER.md §6). Werte aus den Buch-Chunks."""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, tok, tokens, stein, schild, turm, arrow,
                  outline, numdot, codebox, hline, text_width, INK, GRAY, GREEN, ORANGE, CARDLINE, DARKORANGE,
                  WHITE, MONO, C, RT)


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
    schild(s, 3.35, 0.45, "zahlen", w=1.0)
    text(s, 3.05, 0.85, 1.6, 0.25, notiz("Name", size=10.5))
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


def _unter(s, mitte, y, t, w=1.3, color=GRAY):
    """Kurze Beschriftung, mittig unter einem Code-Baustein."""
    text(s, mitte - w / 2, y, w, 0.25, notiz(t, size=10.5, color=color))


# 3.2 Name und Inhalt aus dem Chunk `var1` -----------------------------------------------------
def name_inhalt():
    s = Canvas(5.85, 2.2)
    mids, ende = tokens(s, 0.15, 0.4, [("var1", "obj"), ("<-", "sym"), ("2 * 4", "sym")], size=15, h=0.46)
    _unter(s, mids[0], 0.9, "Name", w=0.9)
    _unter(s, mids[2], 0.9, "Ausdruck", w=0.9)
    w = tok(s, 0.15, 1.5, "var1", "obj", size=15, h=0.46)
    text(s, 0.15 + w + 0.2, 1.5, 1.2, 0.46, mono("[1] 8", size=15, color=GREEN, align="start"), anchor="middle")
    arrow(s, ende + 0.2, 0.48, w=0.7, h=0.3, color=ORANGE)
    card(s, 3.2, 0.15, 2.5, 1.2)
    eyebrow(s, 3.38, 0.24, 2.2, "ENVIRONMENT", size=10)
    schild(s, 3.4, 0.75, "var1", w=1.0)
    stein(s, 4.58, 0.72, 0.9, 0.42, "num", "8", size=13)
    return s


# 3.2 Reihenfolge der Ausführung (neuer Chunk `reihenfolge`) ---------------------------------
def reihenfolge():
    s = Canvas(7.7, 2.05)
    zeilen = ["x <- 5", "y <- x + 2", "x <- 10", "y", "[1] 7"]
    size, top, oben = 13, 0.14, 0.2
    lh = size * 1.42 / 72
    codebox(s, 0.38, oben, 1.8, zeilen, size=size, h=1.65)
    for k in range(4):
        y = oben + top + k * lh + 0.008
        text(s, 0.0, y, 0.3, lh, [P(R(str(k + 1), font=MONO, size=11, color=GRAY), align=RT, ls=size * 1.42)])
    stand = [[("x", "5")], [("x", "5"), ("y", "7")], [("x", "10"), ("y", "7")]]
    for k, objekte in enumerate(stand):
        x = 2.35 + k * 1.78
        card(s, x, oben, 1.68, 1.65)
        eyebrow(s, x + 0.13, oben + 0.07, 1.5, f"NACH ZEILE {k + 1}", size=10)
        for j, (name, wert) in enumerate(objekte):
            y = 0.75 + j * 0.58
            schild(s, x + 0.15, y, name, w=0.5)
            stein(s, x + 0.78, y - 0.03, 0.75, 0.42, "num", wert, size=13)
            if k == 2 and name == "x":
                outline(s, x + 0.72, y - 0.13, 0.87, 0.56, color=ORANGE, lw=1.75)
    return s


# 3.3 Funktion aus dem Chunk `fn-basics` -------------------------------------------------------
def funktion():
    s = Canvas(7.2, 3.3)
    base, h = 2.15, 0.3
    mitte = base - 5 * (h + 0.07) / 2
    for k, (arg, wert) in enumerate([("from", "1"), ("to", "10"), ("by", "2")]):
        x = 0.15 + k * 0.78
        tw = text_width(arg, MONO, 11) + 0.14
        tok(s, x + 0.33 - tw / 2, mitte - 0.62, arg, "arg", size=11, h=0.3)
        stein(s, x, mitte - 0.21, 0.66, 0.42, "num", wert, size=13)
    arrow(s, 2.5, mitte - 0.15, w=0.5, h=0.3)
    label_box(s, 3.15, mitte - 0.35, 1.3, 0.7, "seq()", GREEN, size=18)
    arrow(s, 4.6, mitte - 0.15, w=0.5, h=0.3)
    turm(s, 5.25, base, 0.75, h, "num", ["9", "7", "5", "3", "1"])
    platte(s, 5.15, base, 0.95)
    teile = [("seq", "fun"), ("(", "sym"), ("from = 1", "arg"), (",", "sym"), ("to = 10", "arg"), (",", "sym"),
             ("by = 2", "arg"), (")", "sym")]
    y = 2.5
    mids, ende = tokens(s, 0.15, y, teile, size=12, h=0.36)
    text(s, ende + 0.25, y, 2.0, 0.36, mono("[1] 1 3 5 7 9", size=12, color=GREEN, align="start"), anchor="middle")
    links = mids[2] - (text_width("from = 1", MONO, 12) + 0.14) / 2
    rechts = mids[6] + (text_width("by = 2", MONO, 12) + 0.14) / 2
    hline(s, links, y + 0.44, rechts - links, color=GRAY, width=0.75)
    _unter(s, mids[0], y + 0.48, "Funktion", w=1.0)
    _unter(s, (links + rechts) / 2, y + 0.48, "Argumente", w=1.2)
    return s


# 3.3.1 Argumente von round() aus dem Chunk `grundfunktionen` ---------------------------------
def argumente():
    s = Canvas(7.5, 3.1)
    h = 0.32
    mitte = 1.22
    base = mitte + 3 * (h + 0.07) / 2
    turm(s, 0.2, base, 0.95, h, "num", ["3.987", "2.345", "1.222"])
    platte(s, 0.1, base, 1.15)
    arrow(s, 1.28, mitte - 0.14, w=0.45, h=0.28, color=GREEN)
    card(s, 1.85, 0.2, 3.75, 2.05)
    label_box(s, 2.0, 0.33, 1.25, 0.42, "round()", GREEN, size=13)
    # Feld x: Pflichtfeld, bekommt den Turm
    fy, fh = mitte - 0.31, 0.62
    tok(s, 2.0, mitte - 0.18, "x", "arg", size=12, h=0.36)
    text(s, 2.78, mitte - 0.18, 0.22, 0.36, mono("=", size=13), anchor="middle")
    rect(s, 3.05, fy, 0.75, fh, "#FAF7F1", GRAY, 1.0, dash=True)
    _mini_turm(s, 3.17, fy + fh - 0.11, 0.51, 3)
    text(s, 3.95, mitte - 0.13, 1.6, 0.25, notiz("Pflichtfeld", size=10.5, align="start"))
    # Feld digits: vorausgefüllt, hier mit 1 überschrieben
    dy = 1.92
    tok(s, 2.0, dy - 0.18, "digits", "arg", size=12, h=0.36)
    text(s, 2.78, dy - 0.18, 0.22, 0.36, mono("=", size=13), anchor="middle")
    rect(s, 3.05, dy - 0.2, 0.75, 0.4, WHITE, INK, 1.0)
    text(s, 3.05, dy - 0.2, 0.75, 0.4, mono("1", size=13), anchor="middle")
    text(s, 3.95, dy - 0.13, 1.6, 0.25, notiz("vorausgefüllt mit 0", size=10.5, align="start"))
    arrow(s, 5.75, mitte - 0.14, w=0.45, h=0.28)
    turm(s, 6.35, base, 0.85, h, "num", ["4.0", "2.3", "1.2"])
    platte(s, 6.25, base, 1.05)
    text(s, 1.85, 2.42, 3.75, 0.25, mono("round(c(1.222, 2.345, 3.987), digits = 1)", size=10.5))
    text(s, 1.85, 2.7, 3.75, 0.25, mono("[1] 1.2 2.3 4.0", size=10.5, color=GREEN))
    return s


# 3.6 Fehlende Werte aus den Chunks `na-basic`, `na-arith`, `na-rm` ---------------------------
def na_fig():
    s = Canvas(7.4, 3.0)
    base, h = 2.75, 0.32
    oben = base - 5 * (h + 0.07)
    schild(s, 0.3, oben - 0.5, "x", w=0.8)
    werte = ["5", "4", "NA", "2", "1"]
    turm(s, 0.3, base, 0.8, h, lambda i: "na" if werte[i] == "NA" else "num", werte)
    platte(s, 0.2, base, 1.0)
    reihen = [(1.2, [("mean", "fun"), ("(", "sym"), ("x", "obj"), (")", "sym")], "na", "NA", "[1] NA"),
              (2.2, [("mean", "fun"), ("(", "sym"), ("x", "obj"), (",", "sym"), ("na.rm = TRUE", "arg"),
                     (")", "sym")], "num", "3", "[1] 3")]
    for y, teile, kind, wert, aus in reihen:
        arrow(s, 1.25, y - 0.14, w=0.45, h=0.28)
        _, ende = tokens(s, 1.85, y - 0.2, teile, size=13, h=0.4)
        arrow(s, ende + 0.12, y - 0.14, w=5.4 - ende - 0.12, h=0.28)
        stein(s, 5.55, y - 0.21, 0.8, 0.42, kind, wert, size=13)
        text(s, 6.5, y - 0.21, 0.75, 0.42, mono(aus, size=12, color=GREEN, align="start"), anchor="middle")
    return s


# 3.7.3 Analyseplan aus dem Chunk `real-pipe` (eval=FALSE: nur Code) ---------------------------
def _codezeile(t, size):
    """Eine Code-Zeile; ein |> am Ende wird grün."""
    if t.endswith(" |>"):
        return [R(t[:-3], font=MONO, size=size, bold=True), R(" |>", font=MONO, size=size, bold=True, color=GREEN)]
    return [R(t, font=MONO, size=size, bold=True)]


def analyseplan():
    s = Canvas(7.7, 3.0)
    size = 11
    lh = size * 1.45 / 72
    schritte = [(['allbus <- read_spss("ALLBUS2023.sav") |>'], [R("Datensatz einlesen", size=11.5, bold=True)]),
                (['  rec(mm02, rules = "rev", suffix = "r") |>'],
                 [R("mm02", font=MONO, size=11, bold=True), R(" umpolen", size=11.5, bold=True)]),
                (['  rec(mm05, rules = "rev", suffix = "r") |>'],
                 [R("mm05", font=MONO, size=11, bold=True), R(" umpolen", size=11.5, bold=True)]),
                (["  mutate(", "    islamophobie = row_means(pick(mm01, mm02r, mm03, mm04, mm05r, mm06),",
                  "                             min_valid = 5)", "  )"], [R("Skala bilden", size=11.5, bold=True)])]
    eyebrow(s, 0.55, 0.12, 3.0, "DIE PIPE", size=10)
    eyebrow(s, 5.2, 0.12, 2.4, "DER PLAN IN WORTEN", size=10, color=GREEN)
    y = 0.5
    for k, (code, plan) in enumerate(schritte):
        bh = len(code) * lh + 0.16
        card(s, 0.1, y, 7.5, bh)
        z = y + 0.08
        numdot(s, 0.18, z + lh / 2 - 0.14, k + 1, fill=GREEN, d=0.28, size=10.5)
        text(s, 0.55, z, 7.0, len(code) * lh, [P(*_codezeile(t, size), ls=size * 1.45) for t in code])
        arrow(s, 4.75, z + lh / 2 - 0.1, w=0.32, h=0.2, color=GREEN)
        text(s, 5.2, z, 2.35, lh, [P(*plan, ls=size * 1.45)])
        y += bh + 0.07
    return s


FIGUREN = {
    "k03-legende": legende,
    "k03-turm": turm_fig,
    "k03-rangfolge": rangfolge,
    "k03-tibble": tibble_fig,
    "k03-pipe": pipe,
    "k03-name-inhalt": name_inhalt,
    "k03-reihenfolge": reihenfolge,
    "k03-funktion": funktion,
    "k03-argumente": argumente,
    "k03-na": na_fig,
    "k03-analyseplan": analyseplan,
}
