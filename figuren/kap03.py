"""Abbildungen für Kap. 3 „Programmiersprache R“ (BILDER.md §6). Werte aus den Buch-Chunks."""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, tok, tokens, stein, schild, turm, arrow,
                  outline, numdot, codebox, hline, vline, kiste, referenz, text_width, INK, GRAY, GREEN, ORANGE,
                  CARDLINE, DARKORANGE, WHITE, MONO, C, RT)
import sprache
from sprache import t as tr

SPRACHFAEHIG = True  # alle Texte laufen über tr(); build.py --en baut dieses Modul


def mono(t, size=11, color=INK, bold=True, align=C):
    return [P(R(t, font=MONO, size=size, bold=bold, color=color), align=align)]


def notiz(t, size=11, color=GRAY, align=C, italic=True):
    return [P(R(t, size=size, italic=italic, color=color), align=align, ls=1.0)]


def platte(s, x, base, w):
    rect(s, x, base, w, 0.07, GRAY)


# 3.5 Legende der Bildsprache -------------------------------------------------------------------
def legende():
    s = Canvas(7.8, 4.55)
    eyebrow(s, 0.15, 0.12, 2.6, tr("WERT = STEIN"))
    zeilen = [("num", "1", tr("Zahl"), "numeric", None), ("txt", '"Anna"', tr("Text"), "character", None),
              ("log", "TRUE", tr("Wahrheitswert"), "logical", None), ("na", "", tr("fehlender Wert"), "NA", None),
              ("num", "1", tr("mit Wertelabel"), tr("Aufkleber"), tr("MANN"))]
    for k, (kind, v, lab, typ, tag) in enumerate(zeilen):
        y = 0.62 + k * 0.62
        stein(s, 0.15, y, 1.2, 0.4, kind, v, tag=tag, size=11)
        text(s, 1.5, y - 0.03, 1.7, 0.25, [P(R(lab, size=11.5, bold=True))])
        text(s, 1.5, y + 0.2, 1.7, 0.22, mono(typ, size=10, color=GRAY, bold=False, align="start"))

    eyebrow(s, 3.3, 0.12, 1.6, tr("VEKTOR = TURM"))
    schild(s, 3.35, 0.45, tr("zahlen"), w=1.0)
    text(s, 3.05, 0.85, 1.6, 0.25, notiz(tr("Name"), size=10.5))
    turm(s, 3.35, 2.45, 1.0, 0.34, "num", ["3", "2", "1"])
    platte(s, 3.25, 2.45, 1.2)
    text(s, 3.05, 2.6, 1.6, 0.25, notiz(tr("ein Datentyp"), size=10.5))

    eyebrow(s, 4.9, 0.12, 2.9, tr("DATENSATZ = BAUPLATTE"))
    text(s, 4.9, 0.55, 1.3, 0.25, mono(tr("geschlecht"), size=10.5))
    text(s, 6.3, 0.55, 1.1, 0.25, mono(tr("alter"), size=10.5))
    for i, (g, a) in enumerate([(tr("Mann"), "34"), (tr("Frau"), "41"), (tr("Divers"), "52")]):
        y = 0.92 + i * 0.47
        stein(s, 5.0, y, 1.1, 0.36, "txt", g, size=10.5)
        stein(s, 6.3, y, 1.0, 0.36, "num", a, size=10.5)
    platte(s, 4.9, 2.27, 2.5)
    outline(s, 4.92, 1.32, 2.46, 0.48, color=ORANGE, lw=1.75)
    text(s, 4.85, 2.4, 2.65, 0.25, notiz(tr("eine Reihe = ein Fall"), size=10.5, color=DARKORANGE))
    text(s, 4.85, 2.65, 2.65, 0.25, notiz(tr("ein Turm = eine Variable"), size=10.5))

    rect(s, 0.15, 3.68, 7.5, 0.01, CARDLINE)
    eyebrow(s, 0.15, 3.82, 2.0, tr("CODE-FARBEN"))
    mids, _ = tokens(s, 2.0, 3.77, [(tr("zahlen"), "obj"), ("|>", "sym"), ("round", "fun"), ("(", "sym"),
                                     ("digits = 1", "arg"), (")", "sym")], size=12, h=0.34)
    for i, lab in [(0, "Objekt"), (2, "Funktion"), (4, "Argument")]:
        text(s, mids[i] - 0.7, 4.16, 1.4, 0.25, notiz(tr(lab), size=10.5))
    return s


# 3.5.1 Drei Türme aus dem Chunk `vectors` ----------------------------------------------------
def turm_fig():
    s = Canvas(6.0, 3.15)
    base, h = 2.75, 0.34
    oben = base - 5 * (h + 0.07) - 0.5
    spalten = [(0.35, 1.0, tr("zahlen"), "num", ["5", "4", "3", "2", "1"], "numeric"),
               (2.3, 1.35, tr("namen"), "txt", ['"Carla"', '"Boris"', '"Anna"'], "character"),
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
    eyebrow(s, 6.07, 0.24, 1.6, tr("RANGFOLGE"))
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
    name = tr("befragte")
    sw = max(1.25, text_width(name, MONO, 12.5, True) + 0.3)       # englisch: längerer Name
    schild(s, 0.15, 0.15, name, w=sw)
    text(s, 0.15 + sw + 0.15, 0.2, 1.6, 0.3, mono("4 × 2", size=11, color=GRAY, align="start"))
    xs, ws = [0.3, 1.85], [1.3, 1.1]
    for x, w, n, typ in zip(xs, ws, [tr("geschlecht"), tr("alter")], ["<fct>", "<dbl>"]):
        text(s, x - 0.1, 0.62, w + 0.2, 0.25, mono(n, size=11))
        text(s, x - 0.1, 0.84, w + 0.2, 0.22, mono(typ, size=10, color=GRAY, bold=False))
    base, h = 3.05, 0.38
    for i, (g, a) in enumerate([(tr("Mann"), "34"), (tr("Frau"), "41"), (tr("Mann"), "28"), (tr("Divers"), "52")]):
        y = base - (4 - i) * (h + 0.07)
        stein(s, xs[0], y, ws[0], h, "txt", g, size=11)
        stein(s, xs[1], y, ws[1], h, "num", a, size=11)
    platte(s, 0.15, base, 3.0)
    y1 = base - 3 * (h + 0.07)
    outline(s, 0.2, y1 - 0.1, 2.9, h + 0.16, color=ORANGE, lw=1.75)
    outline(s, xs[1] - 0.07, base - 4 * (h + 0.07) - 0.11, ws[1] + 0.14, 4 * (h + 0.07) + 0.06, color=GREEN, lw=1.75)
    card(s, 3.55, 1.28, 3.7, 0.66)
    text(s, 3.7, 1.35, 3.45, 0.6, [P(R(tr("Eine Reihe ist ein Fall:"), size=11.5, bold=True, color=DARKORANGE)),
                                   P(R(tr("die zweite befragte Person, Frau, 41 Jahre."), size=11), sb=2, ls=1.0)])
    card(s, 3.55, 2.12, 3.7, 0.93)
    text(s, 3.7, 2.2, 3.45, 0.85, [P(R(tr("Ein Turm ist eine Variable:"), size=11.5, bold=True, color=GREEN)),
                                    P(R(f"{name}${tr('alter')}", font=MONO, size=10.5, bold=True), sb=3),
                                    P(R("[1] 34 41 28 52", font=MONO, size=10.5, bold=True, color=GREEN), sb=1)])
    return s


# 3.7.1 Pipe aus dem Chunk `pipe-native` ------------------------------------------------------
def _maschine(s, x, y, name, rest, h=0.95, size=12, fw=0.6):
    """Funktion als Kasten: Name, leeres erstes Feld (gestrichelt, Breite fw), Rest der Klammer.
    Gibt Feld-x, Feldbreite und Gesamtbreite zurück."""
    from lego import text_width
    wn = text_width(name, MONO, size, True)
    wr = text_width(rest, MONO, size, True)
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
    z = tr("zahlen")
    for k, (mitte, name, werte, fname, rest, n, ergebnis, aus) in enumerate(reihen):
        aus = aus.replace("zahlen", z)
        base = mitte + 0.9
        numdot(s, 0.1, mitte - 0.55, k + 1, fill=GREEN, d=0.3, size=11)
        if name:
            schild(s, 0.42, base - 5 * (h + 0.07) - 0.5, z, w=max(0.86, text_width(z, MONO, 12.5, True) + 0.2))
        turm(s, 0.5, base, 0.7, h, "num", werte)
        platte(s, 0.45, base, 0.8)
        _pfeil_pipe(s, 1.35, mitte - 0.13)
        fx, fw, mw = _maschine(s, 1.9, mitte - 0.47, fname, rest)
        _mini_turm(s, fx + 0.12, mitte + 0.38, fw - 0.24, n)
        if sprache.aktuell() == "de":
            bx, bw = 1.6, mw + 0.6
        else:                                   # englisch: längerer Name, die Zeile bleibt einzeilig und mittig
            bw = max(mw + 0.6, text_width("= " + aus, MONO, 10, True) + 0.1)
            bx = 1.9 + mw / 2 - bw / 2
        text(s, bx, mitte + 0.55, bw, 0.25, mono("= " + aus, size=10, color=GREEN))
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
    _unter(s, mids[0], 0.9, tr("Name"), w=0.9)
    _unter(s, mids[2], 0.9, tr("Ausdruck"), w=0.9)
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
        eyebrow(s, x + 0.13, oben + 0.07, 1.5, f"{tr('NACH ZEILE')} {k + 1}", size=10)
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
    _unter(s, mids[0], y + 0.48, tr("Funktion"), w=1.0)
    _unter(s, (links + rechts) / 2, y + 0.48, tr("Argumente").capitalize(), w=1.2)
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
    text(s, 3.95, mitte - 0.13, 1.6, 0.25, notiz(tr("Pflichtfeld"), size=10.5, align="start"))
    # Feld digits: vorausgefüllt, hier mit 1 überschrieben
    dy = 1.92
    tok(s, 2.0, dy - 0.18, "digits", "arg", size=12, h=0.36)
    text(s, 2.78, dy - 0.18, 0.22, 0.36, mono("=", size=13), anchor="middle")
    rect(s, 3.05, dy - 0.2, 0.75, 0.4, WHITE, INK, 1.0)
    text(s, 3.05, dy - 0.2, 0.75, 0.4, mono("1", size=13), anchor="middle")
    text(s, 3.95, dy - 0.13, 1.6, 0.25, notiz(tr("vorausgefüllt mit 0"), size=10.5, align="start"))
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
    en = sprache.aktuell() == "en"          # englisch: eigener Schritt für set_na() nach read_spss()
    ib = tr("islamophobie")
    fett = dict(size=11.5, bold=True)
    mm = dict(font=MONO, size=11, bold=True)
    einlesen = (['allbus <- read_spss("ALLBUS2023.sav") |>'], [R(tr("Datensatz einlesen"), **fett)])
    umpolen = (["  mutate(", '    mm02r = rec(mm02, rules = "rev"),', '    mm05r = rec(mm05, rules = "rev")', "  ) |>"],
               [R("Reverse-code ", **fett), R("mm02", **mm), R(" and ", **fett), R("mm05", **mm)] if en else
               [R("mm02", **mm), R(" und ", **fett), R("mm05", **mm), R(" umpolen", **fett)])
    skala = (["  mutate(", f"    {ib} = row_means(pick(mm01, mm02r, mm03, mm04, mm05r, mm06),",
              " " * (len(ib) + 17) + "min_valid = 5)", "  )"], [R(tr("Skala bilden"), **fett)])
    if en:
        schritte = [(['allbus <- read_spss("ALLBUS2023.sav") |>'], einlesen[1]),
                    (["  set_na(-56, …, -6) |>"], [R(tr("Missing-Codes setzen"), **fett)]), umpolen, skala]
    else:
        schritte = [einlesen, umpolen, skala]
    s = Canvas(7.7, 3.2 + (len(schritte) - 3) * 0.45)
    size = 11
    lh = size * 1.45 / 72
    eyebrow(s, 0.55, 0.12, 3.0, tr("DIE PIPE"), size=10)
    eyebrow(s, 5.2, 0.12, 2.4, tr("DER PLAN IN WORTEN"), size=10, color=GREEN)
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


# Gemeinsam für die Bilder 3.4.3 und 3.5.1: Türme von oben nach unten, Operator zwischen den Steinen einer Reihe
STEP = 0.39                     # Steinhöhe 0.32 plus Fuge 0.07


def saeule(s, x, top, w, werte, kinds, h=0.32, size=12, blass=None):
    """Turm von oben nach unten (erster Wert oben); gibt die Grundlinie unter dem untersten Stein zurück."""
    for i, t in enumerate(werte):
        k = kinds[i] if isinstance(kinds, (list, tuple)) else kinds
        stein(s, x, top + i * STEP, w, h, k, t, size=size, blass=bool(blass and blass[i]))
    return top + len(werte) * STEP - 0.07


def zeichen(s, mitte, top, n, t, h=0.32, size=13):
    """Ein Operator zwischen den Steinen jeder Reihe (Stein für Stein)."""
    for i in range(n):
        text(s, mitte - 0.2, top + i * STEP, 0.4, h, mono(t, size=size), anchor="middle")


def pfeile(s, x, top, n, w=0.34, h=0.32):
    for i in range(n):
        arrow(s, x, top + i * STEP + h / 2 - 0.09, w=w, h=0.18)


def kopfzeile(s, mitte, y, t, w=1.6, size=11):
    text(s, mitte - w / 2, y, w, 0.28, mono(t, size=size))


# 3.4.3 Vergleich und & aus dem Chunk `operators-demo` (dritte Zeile) ----------------------------
def vergleich():
    s = Canvas(6.2, 3.25)
    a = tr("alter")
    alter = ["22", "45", "67", "18", "33"]
    ab18 = ["TRUE" if int(a) >= 18 else "FALSE" for a in alter]
    bis65 = ["TRUE" if int(a) <= 65 else "FALSE" for a in alter]
    beide = ["TRUE" if a == b == "TRUE" else "FALSE" for a, b in zip(ab18, bis65)]
    top, w = 0.7, 0.85
    xa, x1, x2, xe = 0.3, 1.6, 3.1, 4.95
    schild(s, xa - 0.05, top - 0.52, a, w=0.85)
    base = saeule(s, xa, top, 0.75, alter, "num")
    platte(s, xa - 0.1, base + 0.07, 0.95)
    for x, werte, kopf in [(x1, ab18, f"{a} >= 18"), (x2, bis65, f"{a} <= 65")]:
        kopfzeile(s, x + w / 2, top - 0.5, kopf)
        saeule(s, x, top, w, werte, ["log"] * 5)
        platte(s, x - 0.1, base + 0.07, w + 0.2)
    zeichen(s, (x1 + w + x2) / 2, top, 5, "&")
    pfeile(s, x2 + w + 0.2, top, 5, w=0.45)
    saeule(s, xe, top, w, beide, ["log"] * 5)
    platte(s, xe - 0.1, base + 0.07, w + 0.2)
    outline(s, xa - 0.1, top + 2 * STEP - 0.1, xe + w + 0.1 - (xa - 0.1), 0.32 + 0.16, color=ORANGE, lw=1.75)
    text(s, xa - 0.1, base + 0.22, 5.8, 0.28, mono(f"{a} >= 18 & {a} <= 65", size=11, align="start"))
    text(s, xa - 0.1, base + 0.5, 5.8, 0.28, mono("[1]  TRUE  TRUE FALSE  TRUE  TRUE", size=11, color=GREEN,
                                                    align="start"))
    return s


# 3.5.1 Boolesche Indizierung aus dem Chunk `boolean-indexing` --------------------------------
def index_fig():
    s = Canvas(5.9, 3.35)
    z = tr("zahlen")
    zahlen = ["10", "20", "30", "40", "50"]
    maske = ["TRUE" if int(z) > 25 else "FALSE" for z in zahlen]
    top, xz, xm, xe = 0.7, 0.3, 1.4, 3.75
    schild(s, xz - 0.05, top - 0.52, z, w=max(0.9, text_width(z, MONO, 12.5, True) + 0.2))
    base = saeule(s, xz, top, 0.8, zahlen, ["num" if m == "TRUE" else "dim" for m in maske])
    kopfzeile(s, xm + 0.45, top - 0.5, f"{z} > 25", w=1.3)
    saeule(s, xm, top, 0.9, maske, "log")
    platte(s, xz - 0.1, base + 0.07, xm + 0.9 + 0.1 - (xz - 0.1))
    bleibt = [z for z, m in zip(zahlen, maske) if m == "TRUE"]
    oben = base + 0.07 - len(bleibt) * STEP
    arrow(s, 2.65, oben + (base - oben) / 2 - 0.14, w=0.75, h=0.28, color=GREEN)
    saeule(s, xe, oben, 0.8, bleibt, "num")
    platte(s, xe - 0.1, base + 0.07, 1.0)
    for k, (code, aus) in enumerate([(f"{z} > 25", "[1] FALSE FALSE  TRUE  TRUE  TRUE"),
                                     (f"{z}[{z} > 25]", "[1] 30 40 50")]):
        y = base + 0.22 + k * 0.28
        text(s, xz - 0.1, y, 2.1, 0.28, mono(code, size=11, align="start"))
        text(s, 2.3, y, 3.5, 0.28, mono(aus, size=11, color=GREEN, align="start"))
    return s


# 3.5.1 Recycling (Kasten „Vektorisierung“, Chunk `recycling`; zahlen aus `boolean-indexing`) -----
def recycling():
    s = Canvas(7.3, 3.1)
    z = tr("zahlen")
    top5 = 0.62
    base = top5 + 5 * STEP - 0.07
    beispiele = [(0.15, f"{z} * 2", "*", ["10", "20", "30", "40", "50"], ["2"] * 5,
                  [False, True, True, True, True], "[1]  20  40  60  80 100", 0.8),
                 (3.85, "c(1, 2, 3, 4) + c(10, 20)", "+", ["1", "2", "3", "4"], ["10", "20", "10", "20"],
                  [False, False, True, True], "[1] 11 22 13 24", 0.7)]
    for x0, code, op, links, rechts, blass, aus, we in beispiele:
        n = len(links)
        top = base + 0.07 - n * STEP
        ergebnis = [str(int(a) * int(b)) if op == "*" else str(int(a) + int(b)) for a, b in zip(links, rechts)]
        text(s, x0, 0.12, 3.3, 0.28, mono(code, size=11, align="start"))
        xl, xr = x0 + 0.1, x0 + 1.15
        saeule(s, xl, top, 0.7, links, "num")
        zeichen(s, xl + 0.7 + (xr - xl - 0.7) / 2, top, n, op)
        saeule(s, xr, top, 0.7, rechts, "num", blass=blass)
        pfeile(s, xr + 0.85, top, n, w=0.4)
        saeule(s, xr + 1.4, top, we, ergebnis, "num")
        platte(s, x0, base + 0.07, xr + 1.4 + we + 0.1 - x0)
        text(s, x0, base + 0.22, 3.4, 0.28, mono(aus, size=11, color=GREEN, align="start"))
    vline(s, 3.65, 0.15, base + 0.5, color=CARDLINE, width=0.75)
    return s


# 3.5.2 Faktor aus dem Chunk `factors` ---------------------------------------------------------
def faktor_fig():
    g = tr("geschlecht")
    stufen = [tr("Mann"), tr("Frau"), tr("Divers")]
    werte = [stufen[0], stufen[1], stufen[0], stufen[2]]
    codes = [str(stufen.index(w) + 1) for w in werte]
    ausgabe = "[1] " + " ".join(f'"{x}"'.ljust(max(len(f'"{y}"') for y in stufen)) for x in stufen).rstrip()
    zeile1 = f'{g} <- factor(c(' + ", ".join(f'"{w}"' for w in werte) + "),"
    zeile2 = " " * (len(g) + 11) + "levels = c(" + ", ".join(f'"{x}"' for x in stufen) + "))"
    sw = max(1.1, text_width(max(stufen, key=len), MONO, 12, True) + 0.2)       # Steinbreite; englisch breiter
    d = sw - 1.1
    cx = 2.75 + d
    cw = max(3.5, text_width(ausgabe, MONO, 11, True) + 0.3)
    s = Canvas(max(6.4, cx + cw + 0.15, text_width(zeile2, MONO, 10.5, True) + 0.3), 3.15)
    top = 0.7
    schild(s, 0.25, top - 0.52, g, w=1.35)
    base = saeule(s, 0.3, top, sw, werte, "txt")
    text(s, 1.55 + d, top - 0.47, 0.8, 0.25, notiz(tr("intern"), size=10.5))
    saeule(s, 1.7 + d, top, 0.5, codes, "num")
    platte(s, 0.2, base + 0.07, 2.1 + d)
    card(s, cx, 0.12, cw, base + 0.15 - 0.12)
    text(s, cx + 0.15, 0.2, cw - 0.3, 0.28, mono(f"levels({g})", size=11, align="start"))
    for i, st in enumerate(stufen):
        y = 0.62 + i * 0.47
        stein(s, cx + 0.2, y, 0.5, 0.32, "num", str(i + 1), size=12)
        stein(s, cx + 0.85, y, sw, 0.32, "txt", st, size=12)
        if i == 0:
            referenz(s, cx + 0.85 + sw + 0.1, y + 0.16, wort=tr("Referenz"))
    text(s, cx + 0.15, 0.62 + 3 * 0.47 - 0.05, cw - 0.3, 0.28, mono(ausgabe, size=11, color=GREEN, align="start"))
    for k, zeile in enumerate([zeile1, zeile2]):
        text(s, 0.15, base + 0.3 + k * 0.27, s.w - 0.2, 0.27, mono(zeile, size=10.5, align="start"))
    return s


# 3.5.4 Liste aus dem Chunk `list` ------------------------------------------------------------
def liste_fig():
    s = Canvas(7.7, 2.6)
    h = 0.32
    faecher = kiste(s, 0.15, 0.12, [(tr("koeffizient"), 1.17), (tr("p_wert"), 0.85), (tr("konfidenz"), 1.0),
                                    (tr("modell"), 0.8)], h=1.42, name=tr("ergebnis"))
    boden = faecher[0][3] - 0.1
    inhalte = [(["0.42"], "num"), (["0.001"], "num"), (["0.31", "0.53"], "num"), (['"lm"'], "txt")]
    for (fx, _, fb, _), (werte, kind) in zip(faecher, inhalte):
        w = 0.78 if kind == "num" else 0.65
        saeule(s, fx + (fb - w) / 2, boden - len(werte) * STEP + 0.07, w, werte, kind)
    fx, _, fb, _ = faecher[2]
    oben = boden - 2 * STEP + 0.07
    outline(s, fx + (fb - 0.78) / 2 - 0.07, oben - 0.12, 0.78 + 0.14, boden - oben + 0.17, color=GREEN, lw=1.75)
    rechts = faecher[-1][0] + faecher[-1][2]
    mitte = boden - STEP
    xt = 5.4                                                   # herausgenommener Turm
    for k, (x, w, t) in enumerate([(rechts + 0.15, xt - 0.15 - rechts - 0.15, "$" + tr("konfidenz")), (6.33, 0.4, "[1]")]):
        arrow(s, x, mitte - 0.14, w=w, h=0.28, color=GREEN)
        tw = text_width(t, MONO, 11, True)
        lx = x + w / 2 - (tw + 0.32) / 2
        numdot(s, lx, mitte - 0.5, k + 1, fill=GREEN, d=0.26, size=10)
        text(s, lx + 0.32, mitte - 0.51, tw + 0.05, 0.28, mono(t, size=11, color=GREEN, align="start"))
    saeule(s, xt, oben, 0.78, ["0.31", "0.53"], "num")
    platte(s, xt - 0.1, boden + 0.07, 0.98)
    stein(s, 6.85, boden - h, 0.75, h, "num", "0.31", size=12)
    text(s, 0.15, boden + 0.3, 3.0, 0.28, mono(f"{tr('ergebnis')}${tr('konfidenz')}[1]", size=11, align="start"))
    text(s, 2.4, boden + 0.3, 2.0, 0.28, mono("[1] 0.31", size=11, color=GREEN, align="start"))
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
    "k03-vergleich": vergleich,
    "k03-index": index_fig,
    "k03-recycling": recycling,
    "k03-faktor": faktor_fig,
    "k03-liste": liste_fig,
}
