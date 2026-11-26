"""Abbildungen für Kap. 4 „Datenimport und Inspektion“ (BILDER.md §6). Werte aus den Buch-Chunks.

Alle Werte stammen aus ALLBUS 2023 (ALLBUS2023.sav), geprüft mit R 4.5.3 und mariposa 0.7.4.
Wo ein Bild „die ersten Werte“ zeigt, sind es die ersten Zeilen des Datensatzes (head()).
"""
from lego import (Canvas, R, P, text, rect, label_box, tokens, stein, schild, arrow, card, eyebrow, outline,
                  connector, vline, codebox, text_width, INK, GRAY, GREEN, ORANGE, CARDLINE, DARKORANGE, WHITE,
                  STICKER, STEIN, MONO, C, L, RT)
from kap03 import mono, notiz, platte
import sprache
from sprache import t as tr

SPRACHFAEHIG = True  # alle Texte laufen über tr(); build.py --en baut dieses Modul


def aufkleber(s, x, y, w, h, t, size=10):
    """Gelber Aufkleber (Wertelabel) mit beliebiger Breite."""
    label_box(s, x, y, w, h, t, STICKER, color=INK, size=size, rounded=False, margin=0.03)


def lstein(s, x, y, w, h, kind, wert, label, size=12, lsize=10, nw=0.42, blass=False):
    """Stein mit breitem Aufkleber: Wert links, Wertelabel rechts. Ohne Wert füllt der Aufkleber den Stein.
    Bei einem grauen Stein (kind "dim") und mit blass=True ist auch der Aufkleber blass: Die Reihe fällt weg."""
    stein(s, x, y, w, h, kind, "")
    if wert:
        text(s, x + 0.02, y, nw, h, mono(wert, size=size, color=STEIN[kind][1]), anchor="middle")
        kx = x + nw + 0.04
    else:
        kx = x + 0.08
    if blass or kind == "dim":
        label_box(s, kx, y + 0.06, x + w - 0.08 - kx, h - 0.12, label, BLASS[0], color=BLASS[1], size=lsize,
                  rounded=False, margin=0.03)
    else:
        aufkleber(s, kx, y + 0.06, x + w - 0.08 - kx, h - 0.12, label, size=lsize)


def lstein_breite(label, lsize=10, wert=True, nw=0.42):
    """Breite eines Steins, in den der Aufkleber mit diesem Label passt."""
    return (nw + 0.04 if wert else 0.08) + text_width(label, MONO, lsize, True) + 0.06 + 0.12


BLASS = ("#F3EFE6", STEIN["dim"][1])        # Aufkleber auf einem grauen Stein, der wegfällt


def saeule(s, x, top, w, h, kinds, werte, size=11, tags=None, gap=0.07):
    """Turm von oben nach unten: erster Wert oben. Gibt die Unterkante des untersten Steins zurück.
    kind "dim": grauer Stein, der im Ergebnis wegfällt (auch sein Aufkleber wird grau)."""
    for i, t in enumerate(werte):
        k = kinds[i] if isinstance(kinds, (list, tuple)) else kinds
        tag = tags[i] if tags else None
        y = top + i * (h + gap)
        stein(s, x, y, w, h, k, t, tag=tag, size=size)
        if tag and k == "dim":                  # gleiche Lage wie der Aufkleber in lego.stein, nur blass
            label_box(s, x + w - 0.57, y + h - 0.23, 0.55, 0.21, tag, BLASS[0], color=BLASS[1], size=10,
                      rounded=False, margin=0.02)
    return top + (len(werte) - 1) * (h + gap) + h


def kopf(s, x, w, y, name, typ=None, size=11):
    """Spaltenkopf wie im Tibble: Name, darunter grau der Typ."""
    text(s, x - 0.15, y, w + 0.3, 0.25, mono(name, size=size))
    if typ:
        text(s, x - 0.15, y + 0.22, w + 0.3, 0.22, mono(typ, size=10, color=GRAY, bold=False))


def punkte(s, x, y, w=0.3):
    """Graue Auslassungspunkte: Hier gibt es mehr Türme."""
    text(s, x, y, w, 0.3, [P(R("…", size=16, bold=True, color=GRAY), align=C)])


def codezeile(t, size=10.5):
    """Code in einer Zeile; jedes |> grün."""
    teile = t.split(" |> ")
    runs = []
    for i, teil in enumerate(teile):
        if i:
            runs.append(R(" |> ", font=MONO, size=size, bold=True, color=GREEN))
        runs.append(R(teil, font=MONO, size=size, bold=True))
    return [P(*runs)]


# 4.3 Einlesen aus den Chunks `read-allbus` und `read-show` -----------------------------------
def einlesen():
    en = sprache.aktuell() == "en"          # englisch: zweite Codezeile mit set_na()
    s = Canvas(7.6, 3.27 if en else 2.85)
    cy = 1.25
    rect(s, 0.15, cy - 0.3, 1.75, 0.6, WHITE, CARDLINE, 0.75)
    text(s, 0.15, cy - 0.3, 1.75, 0.6, mono("ALLBUS2023.sav", size=11), anchor="middle")
    arrow(s, 2.05, cy - 0.14, w=0.45, h=0.28)
    label_box(s, 2.65, cy - 0.3, 1.55, 0.6, "read_spss()", GREEN, size=13)
    arrow(s, 4.35, cy - 0.14, w=0.45, h=0.28)
    schild(s, 4.95, 0.12, "allbus", w=1.05)
    text(s, 6.12, 0.17, 1.4, 0.3, mono("5,246 × 579", size=11, color=GRAY, align="start"))
    for k, kind in enumerate(["num", "txt", "txt", "num"]):         # za_nr, doi, version, respid
        saeule(s, 5.0 + k * 0.52, 0.75, 0.45, 0.2, kind, ["", "", "", ""])
    punkte(s, 7.08, 1.12)
    platte(s, 4.92, 1.83, 2.58)
    for mitte, txt in [(1.025, "Datei im Projektordner"), (3.425, "Funktion aus mariposa"), (6.2, "Objekt in R")]:
        text(s, mitte - 1.1, 1.98, 2.2, 0.25, notiz(tr(txt), size=10.5))
    tokens(s, 0.15, 2.42, [("allbus", "obj"), ("<-", "sym"), ("read_spss", "fun"), ("(", "sym"),
                           ('"ALLBUS2023.sav"', "arg"), (")", "sym")], size=12, h=0.36)
    if en:
        tokens(s, 0.15, 2.84, [("|>", "sym"), ("set_na", "fun"), ("(", "sym"), ("-56, …, -6", "arg"), (")", "sym")],
               size=12, h=0.36)
    return s


# 4.4 Bauplatte aus dem Chunk `first-look` (nrow, ncol); erste fünf Zeilen von respid, age, mm01 --
def platte_fig():
    s = Canvas(7.6, 3.2)
    schild(s, 0.15, 0.12, "allbus", w=1.05)
    xs, w, h, top = [0.3, 1.2, 2.1], 0.75, 0.32, 1.0
    spalten = [("respid", ["1", "2", "3", "4", "5"]), ("age", ["50", "51", "69", "72", "18"]),
               ("mm01", ["5", "", "", "", "2"])]
    for x, (name, werte) in zip(xs, spalten):
        kopf(s, x, w, 0.62, name)
        unten = saeule(s, x, top, w, h, ["na" if v == "" else "num" for v in werte], werte, size=12)
    punkte(s, 2.95, top + 2 * 0.39 - 0.02)
    platte(s, 0.15, unten + 0.07, 3.15)
    outline(s, 0.2, top - 0.1, 2.75, h + 0.16, color=ORANGE, lw=1.75)
    outline(s, xs[1] - 0.07, top - 0.12, w + 0.14, 5 * (h + 0.07) + 0.1, color=GREEN, lw=1.75)
    cx, cw = 3.65, 3.8
    card(s, cx, 0.62, cw, 0.8)
    text(s, cx + 0.15, 0.68, cw - 0.3, 0.75, [P(R(tr("Eine Reihe ist ein Fall:"), size=11.5, bold=True, color=DARKORANGE)),
                                             P(R("nrow(allbus)", font=MONO, size=10.5, bold=True), sb=3),
                                             P(R("[1] 5246", font=MONO, size=10.5, bold=True, color=GREEN), sb=1)])
    card(s, cx, 1.55, cw, 0.8)
    text(s, cx + 0.15, 1.61, cw - 0.3, 0.75, [P(R(tr("Ein Turm ist eine Variable:"), size=11.5, bold=True, color=GREEN)),
                                             P(R("ncol(allbus)", font=MONO, size=10.5, bold=True), sb=3),
                                             P(R("[1] 579", font=MONO, size=10.5, bold=True, color=GREEN), sb=1)])
    card(s, cx, 2.48, cw, 0.55)
    stein(s, cx + 0.15, 2.6, 0.6, 0.3, "na", "")
    text(s, cx + 0.9, 2.48, cw - 1.0, 0.55, [P(R(tr("Ein leerer Stein ist ein fehlender Wert."), size=11.5, bold=True,
                                                 color=GRAY))], anchor="middle")
    return s


# 4.5.1 select() aus dem Chunk `select-basic`; erste fünf Zeilen --------------------------------
def select_fig():
    s = Canvas(7.8, 3.3)
    w, h, top, step = 0.55, 0.28, 0.95, 0.66
    werte = {"respid": ["1", "2", "3", "4", "5"], "mm01": ["5", "", "", "", "2"], "mm02": ["3", "", "", "", "4"],
             "mm03": ["4", "", "", "", "4"], "mm04": ["2", "", "", "", "3"]}

    def turm_mit_kopf(x, name, bleibt=True):
        kopf(s, x, w, 0.6, name, size=10.5)
        kinds = ["na" if v == "" else ("num" if bleibt else "dim") for v in werte[name]]
        return saeule(s, x, top, w, h, kinds, werte[name], size=10.5)

    schild(s, 0.15, 0.12, "allbus", w=1.05)
    text(s, 1.32, 0.17, 1.5, 0.3, mono("5,246 × 579", size=11, color=GRAY, align="start"))
    unten = turm_mit_kopf(0.2, "respid", bleibt=False)
    punkte(s, 0.8, top + 2 * (h + 0.07) - 0.05, w=0.3)
    for k, name in enumerate(["mm01", "mm02", "mm03", "mm04"]):
        turm_mit_kopf(1.15 + k * step, name, bleibt=(name != "mm04"))
    punkte(s, 3.72, top + 2 * (h + 0.07) - 0.05, w=0.3)
    platte(s, 0.1, unten + 0.07, 3.98)
    mitte = (top + unten) / 2
    text(s, 4.12, mitte - 0.45, 0.9, 0.28, mono("select()", size=11, color=GREEN))
    arrow(s, 4.27, mitte - 0.14, w=0.6, h=0.28, color=GREEN)
    text(s, 5.05, 0.17, 1.5, 0.3, mono("5,246 × 3", size=11, color=GRAY, align="start"))
    for k, name in enumerate(["mm01", "mm02", "mm03"]):
        turm_mit_kopf(5.1 + k * step, name)
    platte(s, 5.0, unten + 0.07, 2.07)
    text(s, 0.15, 2.95, 7.5, 0.28, codezeile("allbus |> select(mm01, mm02, mm03)", size=11))
    return s


# 4.5.1 $ und select() im Vergleich (neuer Chunk `dollar-select`) --------------------------------
def dollar_select():
    s = Canvas(7.6, 3.6)
    werte = ["50", "51", "69", "72", "18"]
    w, h, top = 0.8, 0.3, 1.33
    # links: $ gibt einen Turm allein
    text(s, 0.15, 0.15, 3.5, 0.28, codezeile("allbus$age |> head(5)", size=11))
    unten = saeule(s, 0.45, top, w, h, "num", werte, size=12)
    platte(s, 0.35, unten + 0.07, w + 0.2)
    text(s, 1.5, top + 0.75, 2.2, 0.3, mono("[1] 50 51 69 72 18", size=10.5, color=GREEN, align="start"))
    text(s, 0.15, unten + 0.17, 1.4, 0.25, notiz(tr("Vektor"), size=10.5))
    vline(s, 3.8, 0.15, unten + 0.4, color=CARDLINE, width=0.75)
    # rechts: select() gibt eine Bauplatte mit einem Turm; die Platte hat Platz für weitere Türme
    text(s, 3.95, 0.15, 3.6, 0.28, codezeile("allbus |> select(age) |> head(5)", size=11))
    px, pw = 4.1, 2.9
    text(s, px + 0.05, 0.5, 1.5, 0.3, mono("5 × 1", size=11, color=GRAY, align="start"))
    kopf(s, px + 0.15, w, 0.8, "age", "<dbl+lbl>")
    saeule(s, px + 0.15, top, w, h, "num", werte, size=12)
    platte(s, px, unten + 0.07, pw)
    text(s, px, unten + 0.17, pw, 0.25, notiz("Tibble", size=10.5))
    return s


# 4.5.2 filter() aus dem Chunk `filter-basic`; erste sechs Zeilen von sex, age, educ ------------
def filter_fig():
    s = Canvas(7.8, 3.6)
    h, top = 0.28, 0.95
    zeilen = [("1", "MANN", "50", "3"), ("1", "MANN", "51", "4"), ("2", "FRAU", "69", "4"),
              ("1", "MANN", "72", "3"), ("2", "FRAU", "18", "5"), ("2", "FRAU", "45", "5")]
    spalten = [(1.05, "sex"), (0.6, "age"), (0.6, "educ")]

    def platte_mit(x0, reihen):
        x = x0
        kinds = ["num" if r[1] == "FRAU" else "dim" for r in reihen]   # sex == 2 bleibt, der Rest fällt weg
        for k, (w, name) in enumerate(spalten):
            kopf(s, x, w, 0.6, name, size=10.5)
            if k == 0:
                unten = saeule(s, x, top, w, h, kinds, [r[0] for r in reihen], size=10.5, tags=[tr(r[1]) for r in reihen])
            else:
                unten = saeule(s, x, top, w, h, kinds, [r[k + 1] for r in reihen], size=10.5)
            x += w + 0.1
        return x, unten

    schild(s, 0.15, 0.12, "allbus", w=1.05)
    text(s, 1.32, 0.17, 1.5, 0.3, mono("5,246 × 579", size=11, color=GRAY, align="start"))
    ende, unten = platte_mit(0.2, zeilen)
    punkte(s, ende - 0.05, top + 2 * (h + 0.07) - 0.05)
    platte(s, 0.1, unten + 0.07, ende + 0.25 - 0.1)
    mitte = (top + unten) / 2
    text(s, 3.13, mitte - 0.45, 1.0, 0.28, mono("sex == 2", size=11, color=GREEN))
    arrow(s, 3.33, mitte - 0.14, w=0.6, h=0.28, color=GREEN)
    text(s, 4.2, 0.17, 1.5, 0.3, mono("2,672 × 3", size=11, color=GRAY, align="start"))
    ende2, unten2 = platte_mit(4.25, [r for r in zeilen if r[1] == "FRAU"])
    platte(s, 4.15, unten2 + 0.07, ende2 - 4.15)
    text(s, 4.15, unten2 + 0.15, ende2 - 4.15, 0.3, [P(R("…", size=16, bold=True, color=GRAY), align=C)])
    text(s, 0.15, 3.25, 7.5, 0.28, codezeile("allbus |> filter(sex == 2) |> select(sex, age, educ)", size=11))
    return s


# 4.6 Zahl mit Aufkleber aus dem Chunk `class-show` (Wertelabel 1 = MANN aus `labelled-demo`) ----
def dbl_lbl():
    s = Canvas(7.6, 2.2)
    x, y, w, h = 0.3, 0.75, 2.3, 0.75
    zahl, aufk = STEIN["num"][1], DARKORANGE
    text(s, x, 0.12, w, 0.3, mono("sex", size=11))
    text(s, x, 0.36, w, 0.3, [P(R("<", font=MONO, size=12, bold=True, color=GRAY),
                                R("dbl", font=MONO, size=12, bold=True, color=zahl),
                                R("+", font=MONO, size=12, bold=True, color=GRAY),
                                R("lbl", font=MONO, size=12, bold=True, color=aufk),
                                R(">", font=MONO, size=12, bold=True, color=GRAY), align=C)])
    stein(s, x, y, w, h, "num", "")
    text(s, x, y, 0.8, h, mono("1", size=20, color=zahl), anchor="middle")
    aufkleber(s, x + 0.82, y + 0.13, w - 0.94, h - 0.26, tr("MANN"), size=14)
    for mitte, wort, typ, farbe in [(x + 0.4, tr("Zahl"), "double", zahl), (x + 0.82 + (w - 0.94) / 2, tr("Wertelabel"),
                                                                          "haven_labelled", aufk)]:
        text(s, mitte - 0.9, y + h + 0.12, 1.8, 0.6, [P(R(wort, size=11.5, bold=True), align=C),
                                                       P(R(typ, font=MONO, size=10.5, bold=True, color=farbe),
                                                         align=C, sb=2)])
    codebox(s, 3.05, 0.75, 4.45, ["class(allbus$sex)", '[1] "haven_labelled" "vctrs_vctr"     "double"'], size=10.5)
    return s


# 4.6.1 to_label() und to_numeric() aus dem Chunk `to-label`; erste drei Werte von sex -----------
def to_label_fig():
    s = Canvas(7.2, 3.95)
    h = 0.32
    # Ausgangsturm: Zahl mit Aufkleber
    kopf(s, 0.25, 1.25, 1.12, "sex", "<dbl+lbl>")
    unten = saeule(s, 0.25, 1.67, 1.25, h, "num", ["1", "1", "2"], size=12, tags=[tr("MANN"), tr("MANN"), tr("FRAU")])
    platte(s, 0.15, unten + 0.07, 1.45)
    mitte = (1.67 + unten) / 2
    oben_m, unten_m = 1.2, 3.2
    connector(s, 1.6, mitte, 1.9, mitte, color=GRAY, width=1.5)
    vline(s, 1.9, oben_m, unten_m, color=GRAY, width=1.5)
    for ym, fn in [(oben_m, "to_label()"), (unten_m, "to_numeric()")]:
        connector(s, 1.9, ym, 2.1, ym, color=GRAY, width=1.5)
        arrow(s, 2.1, ym - 0.13, w=1.5, h=0.26, color=GREEN)
        text(s, 1.95, ym - 0.47, 1.8, 0.3, mono(fn, size=12, color=GREEN))
    # oben: Faktor, das Label ist der Wert
    kopf(s, 4.0, 1.05, 0.12, "sex", "<fct>")
    u1 = saeule(s, 4.0, 0.68, 1.05, h, "txt", [tr("MANN"), tr("MANN"), tr("FRAU")], size=12)
    platte(s, 3.9, u1 + 0.07, 1.25)
    text(s, 5.3, oben_m - 0.13, 1.8, 0.3, notiz(tr("Faktor"), size=10.5, align="start"))
    # unten: Zahl ohne Aufkleber
    kopf(s, 4.0, 1.05, 2.12, "sex", "<dbl>")
    u2 = saeule(s, 4.0, 2.68, 1.05, h, "num", ["1", "1", "2"], size=12)
    platte(s, 3.9, u2 + 0.07, 1.25)
    text(s, 5.3, unten_m - 0.13, 1.8, 0.3, notiz(tr("Zahl ohne Label"), size=10.5, align="start"))
    return s


# 4.7 Drei Beschriftungen von mm01 aus dem Chunk `labels-read` (Wertelabels: val_labels()) -------
def labels_fig():
    s = Canvas(7.7, 2.3)
    tx = 5.5
    lab1, lab7 = tr("STIMME GAR NICHT ZU"), tr("STIMME VOLL+GANZ ZU")
    lw = max(lstein_breite(lab1), lstein_breite(lab7))
    zeilen = [(0.12, 0.55, tr("Variablenname"), None), (0.77, 0.55, tr("Variablenlabel"), "var_label()"),
              (1.42, 0.72, tr("Wertelabels"), "val_labels()")]
    for y, hh, wort, fn in zeilen:
        card(s, 0.1, y, 7.5, hh)
        ps = [P(R(wort, size=12, bold=True))]
        if fn:
            ps.append(P(R(fn, font=MONO, size=10.5, bold=True, color=GREEN), sb=2))
        text(s, tx, y, 2.05, hh, ps, anchor="middle")
    schild(s, 0.25, 0.215, "mm01", w=1.0)
    rect(s, 0.25, 0.855, 4.6, 0.38, WHITE, CARDLINE, 0.75)
    text(s, 0.25, 0.855, 4.6, 0.38, mono(tr('"ISLAMAUSUEBUNG IN DEUTSCHL. BESCHRAENKEN"'), size=10.5), anchor="middle")
    lstein(s, 0.25, 1.6, lw, 0.42, "num", "1", lab1, size=12)
    text(s, 0.25 + lw, 1.6, 0.36, 0.42, [P(R("…", size=14, bold=True, color=GRAY), align=C)], anchor="middle")
    lstein(s, 0.61 + lw, 1.6, lw, 0.42, "num", "7", lab7, size=12)
    return s


# 4.8 Vier Gründe für eine Lücke aus dem Chunk `na-freq-demo`; Split-Design -----------------------
def missing_codes():
    s = Canvas(7.8, 3.15)
    text(s, 0.15, 0.12, 4.4, 0.3, codezeile("na_frequencies(allbus$mm01)", size=11))
    zeilen = [("-42", tr("DATENFEHLER: MFN"), "2", tr("NA(a)")), ("-11", tr("TNZ: SPLIT"), "1647", tr("NA(b)")),
              ("-9", tr("KEINE ANGABE"), "73", tr("NA(c)")), ("-8", tr("WEISS NICHT"), "123", tr("NA(d)"))]
    sx, sw = 0.8, 2.0
    for t, x, w, al in [("code", 0.1, 0.55, RT), ("label", sx, sw, C), ("n", 2.95, 0.6, RT), ("tag", 3.75, 0.6, L)]:
        text(s, x, 0.5, w, 0.25, mono(t, size=10, color=GRAY, bold=False, align=al))
    for k, (code, label, n, tag) in enumerate(zeilen):
        y = 0.9 + k * 0.56
        text(s, 0.1, y, 0.55, 0.4, mono(code, size=11, align=RT), anchor="middle")
        lstein(s, sx, y, sw, 0.4, "na", "", label, lsize=10)
        text(s, 2.95, y, 0.6, 0.4, mono(n, size=11, align=RT), anchor="middle")
        text(s, 3.75, y, 0.8, 0.4, mono(tag, size=11, color=GRAY, align="start"), anchor="middle")
    outline(s, 0.15, 0.9 + 0.56 - 0.12, 4.3, 0.58, color=ORANGE, lw=1.75)
    # rechts: Split-Design, schematisch
    eyebrow(s, 4.95, 0.12, 2.8, tr("SPLIT-DESIGN"), size=10.5)
    gx, gw, gp, top, h, gap = 4.98, 0.38, 0.45, 0.98, 0.3, 0.16    # Abstand lässt Platz für den Rahmen
    for j in range(6):
        text(s, gx + j * gp - 0.08, 0.55, gw + 0.16, 0.25, mono(f"mm0{j + 1}", size=10))
        unten = saeule(s, gx + j * gp, top, gw, h, ["num", "num", "na"], ["", "", ""], gap=gap)
    platte(s, gx - 0.08, unten + gap, 5 * gp + gw + 0.16)
    leer = top + 2 * (h + gap)                   # Oberkante der leeren Reihe; Rahmen mittig in den Lücken
    outline(s, gx - 0.06, leer - 0.11, 5 * gp + gw + 0.12, h + 0.19, color=ORANGE, lw=1.75)
    unter = unten + gap + 0.13                   # Text unter der Platte
    text(s, 4.7, unter, 3.05, 0.5, [P(R(tr("zwei Drittel: Fragen gestellt"), size=10.5, italic=True, color=GRAY),
                                     align=C),
                                   P(R(tr("knapp ein Drittel: TNZ: SPLIT"), size=10.5, italic=True,
                                       color=DARKORANGE), align=C, sb=2)])
    return s


# 4.8 set_na() aus dem Chunk `set-na-demo` ---------------------------------------------------
def set_na_fig():
    s = Canvas(7.6, 2.3)
    codes = [("6", tr("ANDERER ABSCHLUSS"), "18"), ("7", tr("NOCH SCHUELER"), "26")]
    lw = lstein_breite(codes[0][1])
    rw = lstein_breite(codes[0][1], wert=False)
    rx = 7.0 - rw
    eyebrow(s, 0.15, 0.12, 1.5, tr("GÜLTIG"), size=10.5)
    teile = [("set_na", "fun"), ("(", "sym"), ("educ = c(6, 7)", "arg"), (")", "sym")]
    ende = tokens(Canvas(1, 1), 0.15 + lw + 0.2, 0.1, teile, size=11, h=0.32)[1]
    eyebrow(s, max(rx, ende + 0.1), 0.12, 1.5, tr("FEHLEND"), size=10.5)   # englische Labels: Kopf rückt nach rechts
    text(s, 7.05, 0.12, 0.45, 0.3, mono("N", size=10, color=GRAY, bold=False, align=RT))
    tokens(s, 0.15 + lw + 0.2, 0.1, teile, size=11, h=0.32)
    for k, (wert, label, n) in enumerate(codes):
        y = 0.65 + k * 0.6
        lstein(s, 0.15, y, lw, 0.42, "num", wert, label, size=12)
        arrow(s, 0.15 + lw + 0.2, y + 0.08, w=rx - lw - 0.55, h=0.26, color=GREEN)
        lstein(s, rx, y, rw, 0.42, "na", "", label)
        text(s, 7.05, y, 0.45, 0.42, mono(n, size=11, align=RT), anchor="middle")
    text(s, 0.15, 1.9, 7.3, 0.3, [P(R("# total N=5246 valid N=5093", font=MONO, size=10.5, bold=True, color=GREEN),
                                    R(tr("   18 + 26 = 44 gültige Werte weniger"), size=10.5, italic=True, color=GRAY),
                                    align=C)])
    return s


# 4.5.2 Fehlende Werte in filter() (Kasten „Vorsicht“, Chunk `filter-na-trio`, eval=FALSE): die Reihen 1 bis 3
# und Reihe 110, die erste ohne gültigen Wert bei sex (NA(b) KEINE ANGABE) -----------------------------------------
def filter_na():
    s = Canvas(5.65, 3.1)
    h, pitch, top = 0.3, 0.37, 0.72
    sw = lstein_breite(tr("KEINE ANGABE"), wert=False)
    sx, lx, lw = 0.65, 0.65 + sw + 0.25, 0.8
    reihen = [("1", "num", "1", tr("MANN"), "TRUE"), ("2", "num", "1", tr("MANN"), "TRUE"),
              ("3", "dim", "2", tr("FRAU"), "FALSE"), None, ("110", "na", "", tr("KEINE ANGABE"), "")]
    kopf(s, sx, sw, 0.12, "sex", "<dbl+lbl>")
    text(s, lx - 0.3, 0.12, lw + 0.6, 0.25, mono("sex == 1", size=11))
    y = top
    for r in reihen:
        if r is None:                                     # weitere Reihen, nicht gezeigt
            punkte(s, sx, y - 0.06, w=sw)
            punkte(s, lx, y - 0.06, w=lw)
            y += 0.3
            continue
        nr, kind, wert, label, vergleich = r
        text(s, 0.05, y, 0.45, h, mono(nr, size=10.5, color=GRAY, bold=False, align=RT), anchor="middle")
        lstein(s, sx, y, sw, h, kind, wert, label, size=11, blass=(kind == "na"))
        stein(s, lx, y, lw, h, "log" if vergleich else "na", vergleich, size=11)
        if not vergleich:
            text(s, lx, y, lw, h, mono("NA", size=11, color=GRAY), anchor="middle")
        y += pitch
    base = y - pitch + h + 0.07
    platte(s, sx - 0.1, base, lx + lw + 0.1 - (sx - 0.1))
    mitte = (top + base) / 2
    ax, aw = lx + lw + 0.2, 0.75
    text(s, ax - 0.2, mitte - 0.45, aw + 0.4, 0.28, mono("filter()", size=11, color=GREEN))
    arrow(s, ax, mitte - 0.14, w=aw, h=0.28, color=GREEN)
    # Ergebnis: nur die Reihen mit TRUE, auf derselben Höhe wie vorher
    rx = ax + aw + 0.2
    kopf(s, rx, sw, 0.12, "sex", "<dbl+lbl>")
    for i in range(2):
        lstein(s, rx, top + i * pitch, sw, h, "num", "1", tr("MANN"), size=11)
    unten = top + pitch + h
    platte(s, rx - 0.1, unten + 0.07, sw + 0.2)
    punkte(s, rx, unten + 0.17, w=sw)
    text(s, 0.15, base + 0.2, 5.4, 0.28, codezeile("allbus |> filter(sex == 1)", size=11))
    return s


# 4.8 drop_na() aus dem Chunk `drop-na`: Reihe 1 (vollständig), Reihe 2 (drei Lücken) und Reihe 53, die erste
# mit genau einer Lücke ---------------------------------------------------------------------------------------
def drop_na_fig():
    s = Canvas(5.85, 2.85)
    w, h, pitch, step, top = 0.55, 0.3, 0.37, 0.65, 0.55
    namen = ["mm01", "mm02", "mm03"]
    reihen = [("1", ["5", "3", "4"], "num"), ("2", ["", "", ""], "num"), None, ("53", ["1", "", "4"], "dim")]
    x0 = 0.65
    for k, name in enumerate(namen):
        kopf(s, x0 + k * step, w, 0.15, name, size=10.5)
    y = top
    for r in reihen:
        if r is None:
            for k in range(3):
                punkte(s, x0 + k * step, y - 0.06, w=w)
            y += 0.3
            continue
        nr, werte, kind = r
        text(s, 0.05, y, 0.45, h, mono(nr, size=10.5, color=GRAY, bold=False, align=RT), anchor="middle")
        for k, v in enumerate(werte):
            stein(s, x0 + k * step, y, w, h, kind if v else "na", v, size=11)
        y += pitch
    y53 = y - pitch
    base = y53 + h + 0.1                                  # etwas Luft für den Rahmen um die unterste Reihe
    breite = 2 * step + w
    platte(s, x0 - 0.1, base, breite + 0.2)
    outline(s, x0 - 0.08, y53 - 0.1, breite + 0.16, h + 0.14, color=ORANGE, lw=1.75)
    text(s, x0 + breite + 0.18, y53, 1.0, h, notiz(tr("eine Lücke"), size=10.5, color=DARKORANGE, align="start"),
         anchor="middle")
    mitte = (top + base) / 2 - 0.15
    ax, aw = x0 + breite + 0.25, 0.75
    text(s, ax - 0.2, mitte - 0.45, aw + 0.4, 0.28, mono("drop_na()", size=11, color=GREEN))
    arrow(s, ax, mitte - 0.14, w=aw, h=0.28, color=GREEN)
    rx = ax + aw + 0.25
    for k, name in enumerate(namen):
        kopf(s, rx + k * step, w, 0.15, name, size=10.5)
        stein(s, rx + k * step, top, w, h, "num", reihen[0][1][k], size=11)
    platte(s, rx - 0.1, top + h + 0.07, breite + 0.2)
    punkte(s, rx, top + h + 0.17, w=breite)
    text(s, 0.15, base + 0.2, 5.6, 0.28, codezeile("allbus |> select(mm01, mm02, mm03) |> drop_na() |> nrow()",
                                                  size=11))
    text(s, 0.15, base + 0.48, 2.0, 0.28, mono("[1] 3285", size=11, color=GREEN, align="start"))
    return s


FIGUREN = {
    "k04-einlesen": einlesen,
    "k04-platte": platte_fig,
    "k04-select": select_fig,
    "k04-dollar-select": dollar_select,
    "k04-filter": filter_fig,
    "k04-dbl-lbl": dbl_lbl,
    "k04-to-label": to_label_fig,
    "k04-labels": labels_fig,
    "k04-missing-codes": missing_codes,
    "k04-set-na": set_na_fig,
    "k04-filter-na": filter_na,
    "k04-drop-na": drop_na_fig,
}
