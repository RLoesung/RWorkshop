"""Abbildungen für Kap. 6 „Visualisierung — Grundlagen“ (BILDER.md §6). Werte aus den Buch-Chunks.

Alle Werte stammen aus ALLBUS 2023 (ALLBUS2023.sav), geprüft mit R 4.5.3, mariposa 0.7.4 und ggplot2 4.0.2, nach dem
Setup-Chunk von Kap. 6 (R/prep.R, educ_kat, to_label(eastwest, sex)). Was ggplot2 aus den Daten berechnet (Lage der
Punkte, Zählungen, Anteile, Umrisse der Violinen, Kennwerte der Boxen), stammt aus layer_data(); die Farben sind die,
die layer_data() ausgibt (Standardpalette von ggplot2 und die Farben aus den Chunks).
"""
from lego import (Canvas, R, P, text, rect, label_box, stein, schild, arrow, outline, connector, kreis, polygon,
                  tokens, eyebrow, text_width, INK, GRAY, GREEN, ORANGE, CARDLINE, WHITE, PALE, STEIN, MONO, C, RT)
from kap03 import mono, notiz, platte, _maschine, _pfeil_pipe
from kap04 import kopf, punkte
from kap05 import code
import sprache
from sprache import t as tr

SPRACHFAEHIG = True  # alle Texte laufen über tr(); build.py --en baut dieses Modul

# Farben aus layer_data(): Standardpalette (scales::hue_pal()) bei zwei und drei Stufen, NA, Farben aus den Chunks
HUE2 = ("#F8766D", "#00BFC4")
HUE3 = ("#F8766D", "#00BA38", "#619CFF")
GREY50, STEELBLUE, GRAU20 = "#7F7F7F", "#4682B4", "#333333"
GITTER = "#ECE8DF"                                         # Gitterlinien der kleinen Grafiken
FOLIE, FOLIE_KANTE, FOLIE_ECKE = "#EEF3F8", "#9DB0C3", "#D3DEE9"


def etikett(s, cx, y, t, size=10.5, h=0.28):
    """aes()-Zuordnung: blassoranger Kasten mit dem Namen der Eigenschaft (x, y, color, fill), mittig bei cx."""
    w = text_width(t, MONO, size, True) + 0.16
    label_box(s, cx - w / 2, y, w, h, t, PALE, color=INK, size=size, rounded=False, margin=0)
    return w


def flaeche(s, x, y, w, h, xs=(), ys=()):
    """Zeichenfläche einer kleinen Grafik mit Gitterlinien bei xs (senkrecht) und ys (waagerecht)."""
    rect(s, x, y, w, h, WHITE, CARDLINE, 0.75)
    for gx in xs:
        connector(s, gx, y, gx, y + h, color=GITTER, width=0.75)
    for gy in ys:
        connector(s, x, gy, x + w, gy, color=GITTER, width=0.75)


def achsentext(s, t, x, y, w, align=C):
    """Beschriftung an einer Achse, wie ggplot2 sie setzt: Systemschrift, grau, 10 pt; (x, y) ist die Mitte der Zeile
    bei align=C, sonst die rechte Kante (RT)."""
    links = x - w / 2 if align == C else x - w
    text(s, links, y - 0.11, w, 0.22, [P(R(t, size=10, color=GRAY), align=align)], anchor="middle")


def folie(s, x, y, w, h, ecke=0.16):
    """Eine Ebene (Layer) als Folie: helles, durchsichtiges Blatt mit umgeknickter Ecke oben rechts."""
    rect(s, x, y, w, h, FOLIE, FOLIE_KANTE, 0.75)
    polygon(s, [(x + w - ecke, y - 0.01), (x + w + 0.01, y - 0.01), (x + w + 0.01, y + ecke)], WHITE)
    polygon(s, [(x + w - ecke, y), (x + w, y + ecke), (x + w - ecke, y + ecke)], FOLIE_ECKE, line=FOLIE_KANTE)


# 6.2 Grammar of Graphics aus dem neuen Chunk `grammatik-vier`: die ersten vier Reihen mit Werten in educ_kat,
# islamophobie und sex (respid 1, 5, 6, 9). Die Grafik hat wie die Ausgabe nur die Stufen mittel und hoch; Bereich der
# y-Achse 1.375 bis 4.125 mit Teilstrichen 1.5 bis 4.0 (ggplot_build()). ---------------------------------------------
VIER = [("1", "mittel", "3.33", "MANN", 10 / 3), ("5", "hoch", "4", "FRAU", 4.0), ("6", "hoch", "3.83", "FRAU", 23 / 6),
        ("9", "hoch", "1.5", "MANN", 1.5)]


def grammatik():
    s = Canvas(7.7, 3.7)
    text(s, 0.15, 0.12, 7.3, 0.45, code([tr("vier |> ggplot(aes(x = educ_kat, y = islamophobie, color = sex)) +"),
                                         "  geom_point(size = 3)"], size=10.5))
    h, pitch, top, ky, ty = 0.3, 0.42, 1.42, 0.82, 3.3
    spalten = [(0.85, 0.8, tr("educ_kat"), "<fct>", "txt", "x"), (1.85, 0.8, tr("islamophobie"), "<dbl>", "num", "y"),
               (2.85, 0.75, "sex", "<fct>", "txt", "color")]
    kopf(s, 0.15, 0.55, ky, "respid", size=10.5)
    for x, w, name, typ, _, aes_ in spalten:
        kopf(s, x, w, ky, name, typ, size=10.5)
        etikett(s, x + w / 2, ty, aes_)
    for i, (rid, bildung, wert, geschlecht, _) in enumerate(VIER):
        y = top + i * pitch
        text(s, 0.15, y, 0.55, h, mono(rid, size=10.5, color=GRAY, align=RT), anchor="middle")
        for (x, w, _, _, kind, _), t in zip(spalten, (bildung, wert, geschlecht)):
            stein(s, x, y, w, h, kind, tr(t) if t in ("mittel", "hoch", "MANN", "FRAU") else t, size=11)
    unten = top + 3 * pitch + h
    platte(s, 0.75, unten + 0.07, 2.95)
    outline(s, 0.77, top - 0.09, 2.91, h + 0.13, color=ORANGE, lw=1.75)
    # geom_point() macht aus jeder Reihe einen Punkt
    mitte = (top + unten) / 2
    arrow(s, 3.88, mitte - 0.14, w=0.62, h=0.28, color=GREEN)
    text(s, 3.66, mitte + 0.2, 1.06, 0.28, mono("geom_point()", size=10, color=GREEN))
    px, py, pw, ph = 5.1, 1.2, 1.7, 1.78
    X = lambda i: px + (i - 0.4) / 2.2 * pw                    # noqa: E731  (1 = mittel, 2 = hoch)
    Y = lambda v: py + (4.125 - v) / 2.75 * ph                 # noqa: E731
    brueche = [(1.5, "1.5"), (2, "2.0"), (2.5, "2.5"), (3, "3.0"), (3.5, "3.5"), (4, "4.0")]
    flaeche(s, px, py, pw, ph, xs=[X(1), X(2)], ys=[Y(b) for b, _ in brueche])
    for b, t in brueche:
        achsentext(s, t, px - 0.08, Y(b), 0.5, align=RT)
    for i, t in ((1, "mittel"), (2, "hoch")):
        achsentext(s, tr(t), X(i), py + ph + 0.15, 0.8)
    etikett(s, px + pw / 2, ty, "x")
    etikett(s, px - 0.25, py - 0.4, "y")
    for rid, bildung, _, geschlecht, v in VIER:
        cx, cy = X(1 if bildung == "mittel" else 2), Y(v)
        kreis(s, cx, cy, 0.06, HUE2[0] if geschlecht == "MANN" else HUE2[1])
        if rid == "5":                                         # 5 und 6 liegen dicht übereinander
            text(s, cx - 0.42, cy - 0.11, 0.32, 0.22, mono(rid, size=10, color=GRAY, align=RT), anchor="middle")
        else:
            dx = 0.17 if rid == "1" else 0.1
            text(s, cx + dx, cy - 0.11, 0.32, 0.22, mono(rid, size=10, color=GRAY, align="start"), anchor="middle")
    kreis(s, X(1), Y(10 / 3), 0.12, None, ORANGE, lw=1.75)
    # Legende rechts
    lx = 6.97
    etikett(s, lx + 0.25, py + 0.3, "color")
    for k, (t, farbe) in enumerate(zip(("MANN", "FRAU"), HUE2)):
        y = py + 0.82 + k * 0.3
        kreis(s, lx, y, 0.05, farbe)
        text(s, lx + 0.1, y - 0.11, 0.6, 0.22, [P(R(tr(t), size=10.5, color=INK))], anchor="middle")
    return s


# 6.3.2 Innerhalb oder außerhalb von aes() aus dem Chunk `aes-vs-konstant` (eval=FALSE). Die ersten drei Werte von sex;
# die Balken für 18 bis 24 Jahre mit den Zählungen aus layer_data() (MANN, FRAU, DIVERS; NA kommt dort nicht vor). ---
ALTER = ["18", "19", "20", "21", "22", "23", "24"]
STAPEL = [(20, 21, 0), (25, 31, 1), (26, 28, 0), (19, 24, 1), (31, 28, 2), (30, 30, 0), (29, 26, 1)]


def aes_konstante():
    s = Canvas(7.6, 4.4)
    einheit = 0.85 / 61                        # Zoll je Person; der höchste Balken (22 Jahre, 61 Personen) 0.85 Zoll
    bx0, bw, bstep = 2.55, 0.3, 0.38
    teile = [(0.12, tr("INNERHALB aes()"), "ggplot(allbus, aes(x = age, fill = sex)) + geom_bar()", True),
             (2.32, tr("AUSSERHALB aes()"), 'ggplot(allbus, aes(x = age)) + geom_bar(fill = "steelblue")', False)]
    for y0, titel, zeile, innen in teile:
        eyebrow(s, 0.15, y0, 1.7, titel)
        text(s, 1.85, y0 - 0.01, 5.7, 0.28, mono(zeile, size=10.5, align="start"))
        basis = y0 + 1.73
        mitte = y0 + 1.2
        if innen:
            kopf(s, 0.3, 0.8, y0 + 0.38, "sex", "<fct>", size=10.5)
            for i, t in enumerate(["MANN", "MANN", "FRAU"]):
                stein(s, 0.3, y0 + 0.84 + i * 0.33, 0.8, 0.25, "txt", tr(t), size=10.5)
            punkte(s, 0.55, y0 + 1.7, w=0.3)
            quelle = 1.2
        else:
            w = text_width('"steelblue"', MONO, 10.5, True) + 0.2
            stein(s, 0.15, mitte - 0.14, w, 0.28, "txt", '"steelblue"', size=10.5)
            quelle = 0.15 + w + 0.1
        arrow(s, quelle, mitte - 0.12, w=bx0 - 0.15 - quelle, h=0.24, color=GREEN)
        etikett(s, (quelle + bx0 - 0.15) / 2, mitte - 0.48, "fill")
        connector(s, bx0 - 0.04, basis, bx0 + 6 * bstep + bw + 0.04, basis, color=CARDLINE, width=0.75)
        for k, (alter, (mann, frau, divers)) in enumerate(zip(ALTER, STAPEL)):
            x = bx0 + k * bstep
            if innen:
                y = basis
                for n, farbe in ((divers, HUE3[2]), (frau, HUE3[1]), (mann, HUE3[0])):
                    if n:
                        rect(s, x, y - n * einheit, bw, n * einheit, farbe)
                        y -= n * einheit
            else:
                n = mann + frau + divers
                rect(s, x, basis - n * einheit, bw, n * einheit, STEELBLUE)
            text(s, x - 0.1, basis + 0.03, bw + 0.2, 0.22, mono(alter, size=10, color=GRAY, bold=False))
        lx = bx0 + 6 * bstep + bw + 0.45
        if innen:
            etikett(s, lx + 0.2, y0 + 0.42, "fill")
            for k, (t, farbe) in enumerate(zip(("MANN", "FRAU", "DIVERS", "NA"), HUE3 + (GREY50,))):
                y = y0 + 0.86 + k * 0.27
                rect(s, lx, y, 0.16, 0.16, farbe)
                text(s, lx + 0.25, y - 0.03, 1.0, 0.22, [P(R(tr(t) if t != "NA" else t, size=10.5, color=INK))], anchor="middle")
        else:
            text(s, lx - 0.05, mitte - 0.14, 1.6, 0.28, notiz(tr("keine Legende"), size=10.5, align="start"),
                 anchor="middle")
    connector(s, 0.1, 2.2, 7.5, 2.2, color=CARDLINE, width=0.75)
    return s


# 6.3.3 Ebenen aus den Chunks `boxviolin` und `combo`. Violinen und Boxen aus layer_data(): je Stufe von educ_kat die
# Breite der Violine (violinwidth) an 33 gleich verteilten Stellen von 1 bis 7 und die Kennwerte der Box (ymin, lower,
# middle, upper, ymax; keine Ausreißer). Bereich der y-Achse 0.7 bis 7.3, Teilstriche 2, 4, 6. ------------------------
VIOLINEN = [
    [0.028, 0.043, 0.065, 0.097, 0.138, 0.184, 0.23, 0.275, 0.324, 0.381, 0.447, 0.514, 0.577, 0.627, 0.667, 0.704,
     0.737, 0.768, 0.79, 0.796, 0.788, 0.773, 0.76, 0.748, 0.731, 0.704, 0.667, 0.624, 0.591, 0.581, 0.591, 0.585,
     0.518],
    [0.059, 0.083, 0.108, 0.135, 0.17, 0.211, 0.255, 0.306, 0.375, 0.461, 0.545, 0.602, 0.628, 0.646, 0.681, 0.734,
     0.781, 0.807, 0.808, 0.794, 0.772, 0.739, 0.689, 0.632, 0.593, 0.593, 0.623, 0.644, 0.629, 0.586, 0.545, 0.509,
     0.442],
    [0.202, 0.293, 0.371, 0.437, 0.505, 0.585, 0.68, 0.788, 0.894, 0.97, 0.999, 0.991, 0.959, 0.906, 0.836, 0.765,
     0.711, 0.664, 0.615, 0.56, 0.501, 0.445, 0.393, 0.349, 0.316, 0.29, 0.264, 0.237, 0.214, 0.202, 0.199, 0.192,
     0.161]]
BOXEN = [(1, 11 / 3, 29 / 6, 6.0, 7), (1, 3.5, 4.5, 35 / 6, 7), (1, 2.5, 10 / 3, 4.5, 7)]


def _skala(px, py, pw, ph):
    """Lage in einer kleinen Grafik wie in der Ausgabe von `combo`: x = Stufe 1 bis 3, y = islamophobie."""
    return (lambda i: px + (i - 0.4) / 3.2 * pw), (lambda v: py + (7.3 - v) / 6.6 * ph)


def _violinen(s, X, Y):
    for i, breiten in enumerate(VIOLINEN):
        ys = [1 + k * 6 / 32 for k in range(len(breiten))]
        rechts = [(X(i + 1 + 0.45 * b), Y(y)) for b, y in zip(breiten, ys)]
        links = [(X(i + 1 - 0.45 * b), Y(y)) for b, y in zip(breiten, ys)]
        polygon(s, rechts + links[::-1], HUE3[i], line=GRAU20, deckkraft=0.4)


def _boxen(s, X, Y):
    for i, (lo, q1, med, q3, hi) in enumerate(BOXEN):
        m = i + 1
        connector(s, X(m), Y(hi), X(m), Y(q3), color=GRAU20, width=0.75)
        connector(s, X(m), Y(q1), X(m), Y(lo), color=GRAU20, width=0.75)
        rect(s, X(m - 0.05), Y(q3), X(m + 0.05) - X(m - 0.05), Y(q1) - Y(q3), WHITE, GRAU20, 0.75)
        connector(s, X(m - 0.05), Y(med), X(m + 0.05), Y(med), color=GRAU20, width=1.5)


def _mini_platte(s, x, base, n, w=0.1, gap=0.03):
    """Kleine Bauplatte ohne Werte: drei Türme (lila, blau, blau) mit n Steinen."""
    for j, kind in enumerate(("txt", "num", "num")):
        for i in range(n):
            rect(s, x + j * (w + gap), base - (i + 1) * 0.1, w, 0.08, STEIN[kind][0], STEIN[kind][1], 0.5)
    rect(s, x - 0.03, base, 3 * w + 2 * gap + 0.06, 0.04, GRAY)


def ebenen():
    s = Canvas(7.7, 3.7)
    # bis ggplot(): die Bauplatte läuft durch |>
    ya, mh = 0.3, 0.75
    _, x = tokens(s, 0.15, ya + mh / 2 - 0.18, [("g_base", "obj"), ("<-", "sym")], size=12, h=0.36)
    schild(s, x + 0.1, ya - 0.08, "allbus", w=0.8)
    _mini_platte(s, x + 0.31, ya + mh - 0.02, 3)
    x += 1.0
    for name, rest, n in (("filter(", ", …)", 3), ("ggplot(", ", aes(…))", 2)):
        _pfeil_pipe(s, x, ya + mh / 2 - 0.13)
        fx, fw, w = _maschine(s, x + 0.55, ya, name, rest, h=mh, size=11, fw=0.42)
        _mini_platte(s, fx + 0.04, ya + mh - 0.16, n)
        x += 0.55 + w + 0.1
    # danach legt + Ebenen übereinander
    yb, pw, ph = 1.5, 1.45, 1.3
    bx, f1, f2, ex = 0.32, 2.1, 3.88, 5.98
    ys = (2, 4, 6)
    for px in (bx, ex):
        X, Y = _skala(px, yb, pw, ph)
        flaeche(s, px, yb, pw, ph, xs=[X(i) for i in (1, 2, 3)], ys=[Y(v) for v in ys])
        for v in ys:
            achsentext(s, str(v), px - 0.06, Y(v), 0.3, align=RT)
        for i, t in enumerate(("niedrig", "mittel", "hoch")):
            achsentext(s, tr(t), X(i + 1), yb + ph + 0.15, 0.6)
    X, Y = _skala(ex, yb, pw, ph)
    _violinen(s, X, Y)
    _boxen(s, X, Y)
    folie(s, f1, yb, pw, ph)
    _violinen(s, *_skala(f1, yb, pw, ph))
    folie(s, f2, yb, pw, ph)
    _boxen(s, *_skala(f2, yb, pw, ph))
    for zeichen, x0 in (("+", bx + pw), ("+", f1 + pw), ("=", f2 + pw)):
        breite = (f1 - bx - pw) if zeichen == "+" else (ex - 0.25 - f2 - pw)
        text(s, x0, yb + ph / 2 - 0.2, breite, 0.4,
             mono(zeichen, size=18, color=GREEN if zeichen == "+" else GRAY), anchor="middle")
    schild(s, bx + pw / 2 - 0.45, yb + ph + 0.33, "g_base", w=0.9)
    for x0, zeilen in ((f1, ["geom_violin(", "  alpha = 0.4)"]),
                       (f2, ["geom_boxplot(", "  width = 0.1,", '  fill = "white")'])):
        text(s, x0, yb + ph + 0.1, 2.0, 0.7, code(zeilen, size=10))
    return s


# 6.4.1 geom_bar() mit after_stat(prop) aus dem Chunk `bar-prop`. Links die ersten zwei Befragten je Stufe von educ_kat
# (respid 8, 11 / 1, 4 / 2, 3) mit ihrem Gewicht; count und prop aus layer_data() (Summe von count 5084.858); Bereich
# der y-Achse -0.0247 bis 0.5184, Teilstriche 0 bis 0.5 (ggplot_build()). ---------------------------------------------
GRUPPEN = [("niedrig", ["1.20", "1.20"]), ("mittel", ["1.25", "0.545"]), ("hoch", ["1.20", "1.20"])]
ZAEHLUNG = [("niedrig", "1049.6", "0.206", 1049.630), ("mittel", "1524.7", "0.300", 1524.693),
            ("hoch", "2510.5", "0.494", 2510.535)]
SUMME = 5084.858


def bar_zaehlt():
    s = Canvas(7.6, 4.35)
    text(s, 0.15, 0.12, 7.3, 0.45, code([tr("ggplot(aes(x = educ_kat, weight = wghtpew)) +"),
                                         '  geom_bar(aes(y = after_stat(prop), group = 1), fill = "steelblue")'],
                                        size=10.5))
    h, pitch, gtop, gstep = 0.25, 0.33, 1.3, 0.83
    ex, ew, wx, ww = 0.15, 0.8, 1.05, 0.65
    kopf(s, ex, ew, 0.78, tr("educ_kat"), "<fct>", size=10.5)
    kopf(s, wx, ww, 0.78, "wghtpew", "<dbl+lbl>", size=10.5)
    for g, (stufe, gewichte) in enumerate(GRUPPEN):
        top = gtop + g * gstep
        for i, gw in enumerate(gewichte):
            stein(s, ex, top + i * pitch, ew, h, "txt", tr(stufe), size=10.5)
            stein(s, wx, top + i * pitch, ww, h, "num", gw, size=10.5)
        punkte(s, 0.75, top + pitch + h - 0.03, w=0.4)
    unten = gtop + 2 * gstep + pitch + h + 0.25
    platte(s, 0.05, unten, wx + ww + 0.1 - 0.05)
    ty = unten + 0.17                                      # aes()-Zuordnungen unter der Platte und an der Grafik
    etikett(s, ex + ew / 2, ty, "x")
    etikett(s, wx + ww / 2, ty, "weight")
    # geom_bar() zählt: je Stufe die Summe der Gewichte (count) und ihr Anteil (prop)
    mitte = (gtop + unten) / 2
    arrow(s, 1.97, mitte - 0.14, w=0.55, h=0.28, color=GREEN)
    text(s, 1.79, mitte - 0.46, 0.91, 0.28, mono("geom_bar()", size=10, color=GREEN))
    tx, tw = 2.72, [(tr("educ_kat"), 0.78, "txt"), ("count", 0.68, "num"), ("prop", 0.58, "num")]
    th, tpitch = 0.28, 0.36
    ttop = mitte - (2 * tpitch + th) / 2
    x = tx
    spalten_x = []
    for name, w, _ in tw:
        kopf(s, x, w, ttop - 0.4, name, size=10.5)
        spalten_x.append(x)
        x += w + 0.07
    for i, (stufe, n, p, _) in enumerate(ZAEHLUNG):
        y = ttop + i * tpitch
        for (name, w, kind), sx, t in zip(tw, spalten_x, (tr(stufe), n, p)):
            stein(s, sx, y, w, th, kind, t, size=10.5)
    tunten = ttop + 2 * tpitch + th
    platte(s, tx - 0.08, tunten + 0.07, x - 0.07 + 0.08 - (tx - 0.08))
    px_, pw_ = spalten_x[2], tw[2][1]
    outline(s, px_ - 0.06, ttop - 0.12, pw_ + 0.12, tunten - ttop + 0.17, color=GREEN, lw=1.75)
    arrow(s, px_ + pw_ + 0.15, mitte - 0.14, w=0.42, h=0.28, color=GREEN)
    # after_stat(prop) auf der y-Achse
    cx, cy, cw, ch = 5.88, 1.32, 1.57, 2.15
    X = lambda i: cx + (i - 0.4) / 3.2 * cw                    # noqa: E731
    Y = lambda v: cy + (0.518414 + v * -1) / 0.543100 * ch     # noqa: E731
    brueche = [(k / 10, f"{k * 10}%") for k in range(6)]
    flaeche(s, cx, cy, cw, ch, xs=[X(i) for i in (1, 2, 3)], ys=[Y(b) for b, _ in brueche])
    for b, t in brueche:
        achsentext(s, t, cx - 0.06, Y(b), 0.45, align=RT)
    for i, (stufe, _, _, n) in enumerate(ZAEHLUNG):
        rect(s, X(i + 0.55), Y(n / SUMME), X(i + 1.45) - X(i + 0.55), Y(0) - Y(n / SUMME), STEELBLUE)
        achsentext(s, tr(stufe), X(i + 1), cy + ch + 0.15, 0.6)
    etikett(s, cx + cw / 2, ty, "x")
    t = "y = after_stat(prop)"
    etikett(s, cx - 0.45 + (text_width(t, MONO, 10.5, True) + 0.16) / 2, cy - 0.45, t)
    return s


FIGUREN = {
    "k06-grammatik": grammatik,
    "k06-aes-konstante": aes_konstante,
    "k06-ebenen": ebenen,
    "k06-bar-zaehlt": bar_zaehlt,
}
