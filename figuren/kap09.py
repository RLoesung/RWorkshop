"""Abbildungen für Kap. 9 „Erklärungsmodelle“ (BILDER.md §6). Werte aus den Buch-Chunks.

Alle Werte stammen aus ALLBUS 2023 (ALLBUS2023.sav), geprüft mit R 4.5.3 und mariposa 0.7.4, nach dem Setup-Chunk von
Kap. 9 (R/prep.R, dazu educ_kat aus educ und to_label(eastwest, sex)). Die Zeilennummern von allbus sind dort gleich
der respid.
"""
from lego import (Canvas, R, P, text, card, stein, schild, arrow, outline, connector, polygon, referenz,
                  text_width, INK, GRAY, GREEN, ORANGE, DARKORANGE, WHITE, MONO, L, RT)
from kap03 import mono, notiz, platte
from kap04 import kopf, punkte, codezeile
from kap05 import code, klammer
import sprache
from sprache import t as tr

SPRACHFAEHIG = True  # alle Texte laufen über tr(); build.py --en baut dieses Modul


def nummer(s, x, y, w, h, t):
    """Graue Reihennummer wie in der Ausgabe eines Tibbles, rechtsbündig vor der Reihe."""
    text(s, x, y, w, h, mono(t, size=10.5, color=GRAY, bold=False, align=RT), anchor="middle")


def pfeile_je_reihe(s, x, ys, h, w=0.4):
    """Kleine graue Pfeile nach rechts, einer je Reihe (R rechnet Reihe für Reihe)."""
    for y in ys:
        arrow(s, x, y + h / 2 - 0.09, w=w, h=0.18)


# 9.3.1 Dummy-Codierung: Reihen 1, 2 und 8 von allbus; die Dummies wie model.matrix(~ educ_kat) -------------------
STUFEN = ["niedrig", "mittel", "hoch"]                                  # levels(allbus$educ_kat)
BILDUNG = [("1", "mittel"), ("2", "hoch"), ("8", "niedrig")]


def dummy():
    s = Canvas(7.6, 2.55)
    h, pitch, top, ky = 0.32, 0.42, 0.85, 0.42
    fx, fw = 0.45, 0.9                                                  # Faktor-Turm
    dummies = [(tr("educ_katmittel"), "mittel", 2.6), (tr("educ_kathoch"), "hoch", 3.95)]   # (Name, Stufe, Mitte)
    dw = 0.55
    kopf(s, fx, fw, ky, tr("educ_kat"), size=10.5)
    for name, _, mitte in dummies:
        kopf(s, mitte - dw / 2, dw, ky, name, size=10.5)
    text(s, 2.65, 0.1, 1.25, 0.28, notiz(tr("intern"), size=10.5))
    ys = [top, top + pitch, top + 2 * pitch + 0.3]                       # Lücke für die Reihen 3 bis 7
    for (nr, stufe), y in zip(BILDUNG, ys):
        nummer(s, 0.0, y, 0.35, h, nr)
        stein(s, fx, y, fw, h, "txt", tr(stufe), size=11)
        for _, d_stufe, mitte in dummies:
            stein(s, mitte - dw / 2, y, dw, h, "num", "1" if stufe == d_stufe else "0", size=11)
    pfeile_je_reihe(s, fx + fw + 0.15, ys, h, w=0.55)
    for x, w in [(fx, fw)] + [(m - dw / 2, dw) for _, _, m in dummies]:
        punkte(s, x, ys[1] + h + 0.0, w=w)
    unten = ys[-1] + h
    for _, _, mitte in dummies:
        outline(s, mitte - dw / 2 - 0.07, top - 0.13, dw + 0.14, unten - top + 0.19, color=GREEN, lw=1.75)
    platte(s, 0.35, unten + 0.1, 4.05)
    # Stufenleiste rechts wie in k03-faktor: die erste Stufe ist die Referenz
    cx, cw = 4.62, 2.88
    card(s, cx, 0.12, cw, unten + 0.17 - 0.12)
    text(s, cx + 0.15, 0.2, cw - 0.3, 0.28, mono(tr("levels(allbus$educ_kat)"), size=10.5, align=L))
    for i, st in enumerate(STUFEN):
        y = 0.6 + i * 0.44
        stein(s, cx + 0.2, y, 1.0, h, "txt", tr(st), size=11)
        if i == 0:
            referenz(s, cx + 1.3, y + h / 2, wort=tr("Referenz"))
    text(s, cx + 0.15, unten - 0.3, cw - 0.25, 0.28,
         mono(tr('[1] "niedrig" "mittel"  "hoch"'), size=10, color=GREEN, align=L))
    return s


# 9.4.1 Gemeinsames Fall-Set aus dem Chunk `model-compare`: die ersten acht Reihen von allbus, wie tibble sie druckt.
# drop_na() behält davon die Reihen 1 und 6. Reihe 5 fehlt nur populismus: m_basis rechnete auf allbus mit ihr,
# m_voll nicht. Maße: allbus 5,246 × 593, allbus_modell 1,881 × 593 (N = 1881 im Chunk `lm`) ------------------------
ALT, NEU = "ALTE BUNDESLAENDER", "NEUE BUNDESLAENDER"
SPALTEN = [("islamophobie", "num", 0.6), ("educ_kat", "txt", 0.78), ("age", "num", 0.42), ("eastwest", "txt", 1.64),
           ("sex", "txt", 0.6), ("populismus", "num", 0.6)]
UEBERSETZT = {"islamophobie", "educ_kat", "populismus"}                 # Namen, die tr() kennt; age, eastwest, sex bleiben
ACHT = [("3.33", "mittel", "50", ALT, "MANN", "2.29"), ("", "hoch", "51", ALT, "MANN", "3"),
        ("", "hoch", "69", ALT, "FRAU", "2.86"), ("", "mittel", "72", NEU, "MANN", "4.57"),
        ("4", "hoch", "18", ALT, "FRAU", ""), ("3.83", "hoch", "45", ALT, "FRAU", "3.71"),
        ("", "mittel", "26", ALT, "FRAU", ""), ("", "niedrig", "71", ALT, "FRAU", "4.14")]


WERTE_UEBERSETZT = {"niedrig", "mittel", "hoch", ALT, NEU, "MANN", "FRAU"}


def spalten_x(x0, spalten, size=10, gap=0.08):
    """x-Positionen der Steine nebeneinander; ein Spaltenkopf, der breiter ist als sein Stein, bekommt Platz.
    gap: Abstand zwischen den Spalten, eine Zahl oder eine Liste (ein Wert je Lücke)."""
    gaps = gap if isinstance(gap, (list, tuple)) else [gap] * (len(spalten) - 1)
    xs, x = [], x0
    for j, (name, _, w) in enumerate(spalten):
        kw = text_width(name, MONO, size, True) if name != "…" else 0
        rand = max(0.0, (kw - w) / 2)
        xs.append(x + rand)
        x += 2 * rand + w + (gaps[j] if j < len(gaps) else 0)
    return xs, x


def masse(s, x, y, name, dims):
    """Dunkles Namensschild mit den Maßen des Tibbles daneben; gibt das rechte Ende zurück."""
    w = max(1.0, text_width(name, MONO, 12.5, True) + 0.3)
    schild(s, x, y, name, w=w)
    tw = text_width(dims, MONO, 11, True) + 0.05
    text(s, x + w + 0.15, y, tw, 0.36, mono(dims, size=11, color=GRAY, align=L), anchor="middle")
    return x + w + 0.15 + tw


def fallset():
    s = Canvas(7.6, 4.85)
    h, pitch, top, ky = 0.28, 0.4, 1.1, 0.72
    spalten = [(tr(n) if n in UEBERSETZT else n, k, w) for n, k, w in SPALTEN]
    xs, rechts = spalten_x(0.5, spalten)
    # oben: allbus → drop_na() → allbus_modell
    ende = masse(s, 0.15, 0.18, "allbus", "5,246 × 593")
    ax = ende + 0.2
    text(s, ax - 0.1, 0.03, 1.3, 0.22, mono("drop_na()", size=10.5, color=GREEN))
    arrow(s, ax, 0.26, w=1.1, h=0.2, color=GREEN)
    masse(s, ax + 1.3, 0.18, tr("allbus_modell"), "1,881 × 593")
    for x, (name, _, w) in zip(xs, spalten):
        kopf(s, x, w, ky, name, size=10)
    for i, reihe in enumerate(ACHT):
        y = top + i * pitch
        bleibt = all(reihe)
        nummer(s, 0.0, y, 0.35, h, str(i + 1))
        for x, (_, kind, w), v in zip(xs, spalten, reihe):
            v = tr(v) if v in WERTE_UEBERSETZT else v
            stein(s, x, y, w, h, (kind if bleibt else "dim") if v else "na", v, size=10 if len(v) > 8 else 11)
    unten = top + 7 * pitch + h
    platte(s, 0.4, unten + 0.08, rechts + 0.1 - 0.4)
    # Reihe 5: nur populismus fehlt
    y5 = top + 4 * pitch
    outline(s, xs[0] - 0.08, y5 - 0.09, rechts + 0.08 - (xs[0] - 0.08), h + 0.13, color=ORANGE, lw=1.75)
    text(s, rechts + 0.14, y5 - 0.2, 7.58 - rechts - 0.14, h + 0.4,
         [P(R(tr("ohne "), size=10, italic=True, color=DARKORANGE), R("drop_na()", font=MONO, size=10, bold=True,
                                                                     color=DARKORANGE),
            R(":", size=10, italic=True, color=DARKORANGE), ls=1.05),
          P(R(tr("nur in "), size=10, italic=True, color=DARKORANGE), R(tr("m_basis"), font=MONO, size=10, bold=True,
                                                                       color=DARKORANGE), ls=1.05)],
         anchor="middle")
    text(s, 0.15, unten + 0.27, 7.4, 0.45, code([tr("allbus_modell <- allbus |>"),
                                                 tr("  drop_na(islamophobie, educ_kat, age, eastwest, sex, populismus)")],
                                                size=10.5))
    return s


# 9.6.3 augment() aus dem Chunk `augment-setup`: Reihen 1 und 2 von diagnose_df (respid 1 und 6, die beiden Reihen,
# die in k09-fallset bleiben), auf drei Stellen gerundet. eastwest und sex stehen als Auslassungspunkte (beide Reihen:
# ALTE BUNDESLAENDER; MANN und FRAU), ebenso .sigma, .cooksd und .std.resid. Rechnung für Reihe 1 mit B aus dem
# Chunk `lm-summary`; mit den gerundeten Koeffizienten ergibt sie 3.398, daher ≈ 3.40 --------------------------------
DIAGNOSE = [("islamophobie", "num", 0.62, ["3.333", "3.833"]), ("educ_kat", "txt", 0.66, ["mittel", "hoch"]),
            ("age", "num", 0.42, ["50", "45"]), ("…", None, 0.26, None),
            ("populismus", "num", 0.62, ["2.286", "3.714"]), ("(weights)", "dim", 0.6, ["1.252", "1.252"]),
            (".fitted", "num", 0.6, ["3.400", "3.829"]), (".resid", "num", 0.64, ["-0.067", "0.004"]),
            (".hat", "dim", 0.58, ["0.005", "0.003"]), ("…", None, 0.22, None)]
LUECKEN = [0.08, 0.08, 0.08, 0.08, 0.13, 0.13, 0.2, 0.13, 0.06]       # mehr Luft um die grünen Rahmen
RECHNUNG = [[".fitted", "=", ("0.808", "(Intercept)"), "+", ("0.012 · 1", "educ_katmittel"), "+",
             ("0.024 · 50", "age"), "+", ("0.603 · 2.286", "populismus"), "≈", ("3.40", "")],
            [".resid", "=", ("3.333", "islamophobie"), "-", ("3.400", ".fitted"), "=", ("-0.067", "")]]


def diagnose():
    """DIAGNOSE mit den Namen und Stufen der aktuellen Sprache."""
    namen = {"islamophobie", "educ_kat", "populismus"}
    stufen = {"mittel", "hoch"}
    return [(tr(n) if n in namen else n, k, w, None if v is None else [tr(x) if x in stufen else x for x in v])
            for n, k, w, v in DIAGNOSE]


def rechnung_zeilen():
    """RECHNUNG mit den Koeffizientennamen der aktuellen Sprache (educ_katmittel, populismus)."""
    namen = {"educ_katmittel", "populismus", "islamophobie"}
    return [[(el[0], tr(el[1]) if el[1] in namen else el[1]) if isinstance(el, tuple) else el for el in zeile]
            for zeile in RECHNUNG]


def rechnung(s, x, y, zeile, size=11, lsize=10):
    """Eine Rechenzeile: Name links, dann Werte mit grauer Beschriftung darunter und Operatoren dazwischen."""
    for el in zeile:
        if isinstance(el, str) and el.startswith("."):
            w = text_width(el, MONO, size, True) + 0.1
            text(s, x, y, w, 0.28, mono(el, size=size, align=L))
        elif isinstance(el, str):
            w = 0.32
            text(s, x, y, w, 0.28, mono(el, size=size, color=GRAY))
        else:
            wert, lab = el
            w = max(text_width(wert, MONO, size, True), text_width(lab, MONO, lsize, True)) + 0.08
            text(s, x, y, w, 0.28, mono(wert, size=size))
            if lab:
                text(s, x, y + 0.25, w, 0.25, mono(lab, size=lsize, color=GRAY, bold=False))
        x += w
    return x


def augment():
    s = Canvas(7.6, 3.3)
    h, pitch, top, ky = 0.3, 0.42, 1.0, 0.6
    text(s, 0.15, 0.12, 7.3, 0.28, codezeile(tr("diagnose_df <- modell |> augment()"), size=10.5))
    diag = diagnose()
    xs, rechts = spalten_x(0.45, [(n, k, w) for n, k, w, _ in diag], gap=LUECKEN)
    for j, (x, (name, kind, w, werte)) in enumerate(zip(xs, diag)):
        if werte is None:                                          # weitere Türme, nicht gezeigt
            for i in range(2):
                punkte(s, x, top + i * pitch - 0.05, w=w)
            continue
        kopf(s, x, w, ky, name, size=10)
        for i, v in enumerate(werte):
            stein(s, x, top + i * pitch, w, h, kind, v, size=11)
        if name in (".fitted", ".resid"):
            outline(s, x - 0.08, top - 0.14, w + 0.16, pitch + h + 0.2, color=GREEN, lw=1.75)
    unten = top + pitch + h
    platte(s, 0.4, unten + 0.1, rechts + 0.08 - 0.4)
    nummer(s, 0.0, top, 0.32, h, "1")
    nummer(s, 0.0, top + pitch, 0.32, h, "2")
    outline(s, 0.45, top - 0.1, rechts + 0.04 - 0.45, h + 0.15, color=ORANGE, lw=1.75)
    for k, zeile in enumerate(rechnung_zeilen()):
        rechnung(s, 0.15, unten + 0.4 + k * 0.62, zeile)
    return s


# 9.7.3 Randmittel: Mittelwerte von islamophobie je educ_kat aus summary() von oneway_anova() (7.6.2: 4.676, 4.452,
# 3.482) und die Estimated Marginal Means aus dem Chunk `ancova-summary` (4.414, 4.426, 3.601), wie im Text auf zwei
# Stellen gerundet. Beide Lineale haben dieselbe Skala; die gestrichelten Linien verbinden dieselbe Gruppe. Unten liegen
# niedrig und mittel 0.05 Zoll auseinander: niedrig zeigt von oben, mittel von unten auf das Lineal. Zahlen stehen nur
# an den ganzen Strichen, damit unter 4.5 Platz für den Pfeil von unten ist ------------------------------------------
OHNE = [("hoch", 3.48), ("mittel", 4.45), ("niedrig", 4.68)]
MIT = [("hoch", 3.60), ("niedrig", 4.41), ("mittel", 4.43)]
LINKS = {("hoch", 0), ("mittel", 0), ("hoch", 1), ("niedrig", 1)}         # Beschriftung links vom Pfeil
VON_UNTEN = {("mittel", 1)}                                             # Pfeil von unten auf das Lineal


def mittel_marke(s, x, y, t, rechts=True, unten=False, color=DARKORANGE, size=11):
    """Oranger Pfeil auf das Lineal (ein Mittelwert), Gruppe und Wert daneben. Form wie lego.down_arrow, dazu eine
    weiße Kante. unten=True: Der Pfeil zeigt von unten auf das Lineal."""
    w, h = 0.18, 0.28
    richtung = -1 if unten else 1                                       # 1: von oben nach unten
    spitze = y - richtung * 0.05
    ende, kopf_y = spitze - richtung * h, spitze - richtung * w / 2
    l, r = x - w / 4, x + w / 4
    polygon(s, [(l, ende), (r, ende), (r, kopf_y), (x + w / 2, kopf_y), (x, spitze), (x - w / 2, kopf_y), (l, kopf_y)],
            color, line=WHITE, lw=0.75)
    tw = text_width(t, MONO, size, True) + 0.05
    tx = x + 0.12 if rechts else x - 0.12 - tw
    text(s, tx, y + 0.12 if unten else y - 0.4, tw, 0.28, mono(t, size=size, color=color, align=L if rechts else RT))


def randmittel():
    s = Canvas(7.6, 2.55)
    x0, lo, hi, laenge = 1.95, 3.0, 5.0, 5.1
    X = lambda v: x0 + (v - lo) / (hi - lo) * laenge                       # noqa: E731
    y1, y2 = 0.72, 2.0
    # dieselbe Gruppe auf beiden Linealen, von Pfeil zu Pfeil; zu einem Pfeil von unten bis an das Lineal
    for (gruppe, v1) in OHNE:
        v2 = dict(MIT)[gruppe]
        bis = y2 if (gruppe, 1) in VON_UNTEN else y2 - 0.36
        connector(s, X(v1), y1 + 0.36, X(v2), bis, color=GRAY, width=1.0, dash=True)
    for k, (y, werte) in enumerate(((y1, OHNE), (y2, MIT))):
        connector(s, X(lo), y, X(hi), y, color=INK, width=2.0)
        for v, t in ((3.0, "3"), (3.5, None), (4.0, "4"), (4.5, None), (5.0, "5")):
            d = 0.07 if t else 0.045                                         # halbe Striche kürzer, ohne Zahl
            connector(s, X(v), y - d, X(v), y + d, color=INK, width=1.25)
            if t:
                text(s, X(v) - 0.3, y + 0.1, 0.6, 0.25, mono(t, size=10, color=GRAY, bold=False))
        for gruppe, v in werte:
            mittel_marke(s, X(v), y, f"{tr(gruppe)} {v:.2f}", rechts=(gruppe, k) not in LINKS,
                         unten=(gruppe, k) in VON_UNTEN)
    text(s, 0.15, y1 - 0.3, 1.7, 0.28, mono("oneway_anova()", size=10.5, color=GREEN, align=L))
    text(s, 0.15, y1 - 0.04, 1.7, 0.28, notiz(tr("Mittelwerte"), size=10.5, align=L))
    text(s, 0.15, y2 - 0.3, 1.7, 0.28, mono("ancova()", size=10.5, color=GREEN, align=L))
    text(s, 0.15, y2 - 0.04, 1.7, 0.28, mono("covariate = age", size=10, color=GRAY, bold=False, align=L))
    text(s, 0.15, y2 + 0.2, 1.7, 0.28, notiz(tr("Randmittel"), size=10.5, align=L))
    return s


# 9.8.1 AME aus dem Chunk `logreg-ame`: die ersten drei Personen im Modell modell_log (respid 1, 5, 6). Ihre
# vorhergesagten Wahrscheinlichkeiten mit predict(modell_log, newdata, type = "response"), educ_kat einmal auf niedrig,
# einmal auf hoch gesetzt, alle anderen Merkmale wie beobachtet (0.58359 → 0.31605, 0.39447 → 0.17681,
# 0.58141 → 0.31412). Der gewichtete Mittelwert der Differenzen über alle Personen im Modell ist -0.2519 ------------
PERSONEN = [("1", "mittel", "0.584", "0.316"), ("5", "hoch", "0.394", "0.177"), ("6", "hoch", "0.581", "0.314")]


def ame():
    s = Canvas(7.6, 3.2)
    h, pitch, top, ky = 0.32, 0.42, 0.95, 0.55
    ex, ew = 0.8, 0.8                                                  # educ_kat, wie beobachtet
    nx, hx, pw = 2.0, 2.95, 0.7                                        # vorhergesagt mit niedrig / hoch
    dx, dw = 4.45, 0.7                                                 # Differenz
    kopf(s, 0.12, 0.5, ky, "respid", size=10.5)
    kopf(s, ex, ew, ky, tr("educ_kat"), size=10.5)
    mitte_p = (nx + hx + pw) / 2                                         # über den Spalten niedrig und hoch
    kopf_p = tr("P(islam_hoch = 1)")
    kw = max(1.8, text_width(kopf_p, MONO, 10, True) + 0.1)                # englischer Name ist länger
    text(s, mitte_p - kw / 2, 0.07, kw, 0.4, mono(kopf_p, size=10, color=GRAY, bold=False)
         + mono(tr("bei educ_kat ="), size=10, color=GRAY, bold=False))
    kopf(s, nx, pw, ky, tr("niedrig"), size=10.5)
    kopf(s, hx, pw, ky, tr("hoch"), size=10.5)
    text(s, dx - 0.4, ky, dw + 0.8, 0.25, mono(tr("hoch - niedrig"), size=10.5))
    ys = [top + i * pitch for i in range(len(PERSONEN))]
    for y, (rid, bildung, p_n, p_h) in zip(ys, PERSONEN):
        nummer(s, 0.1, y, 0.5, h, rid)
        stein(s, ex, y, ew, h, "txt", tr(bildung), size=11)
        stein(s, nx, y, pw, h, "num", p_n, size=11)
        stein(s, hx, y, pw, h, "num", p_h, size=11)
        stein(s, dx, y, dw, h, "num", f"{float(p_h) - float(p_n):.2f}", size=11)
    pfeile_je_reihe(s, hx + pw + 0.18, ys, h, w=dx - hx - pw - 0.36)
    unten = ys[-1] + h
    for x, w in ((ex, ew), (nx, pw), (hx, pw), (dx, dw)):
        punkte(s, x, unten + 0.04, w=w)
    platte(s, 0.7, unten + 0.38, dx + dw + 0.1 - 0.7)
    outline(s, dx - 0.07, top - 0.13, dw + 0.14, unten + 0.34 - (top - 0.13), color=GREEN, lw=1.75)
    # gewichteter Mittelwert über alle Personen im Modell
    mitte = (top + unten + 0.3) / 2
    klammer(s, dx + dw + 0.14, top, unten + 0.3, color=INK)
    ax = dx + dw + 0.42
    arrow(s, ax, mitte - 0.12, w=0.6, h=0.24, color=GREEN)
    text(s, ax - 0.1, mitte - 0.48, 1.9, 0.28, notiz(tr("gewichteter Mittelwert"), size=10.5, align=L))
    stein(s, ax + 0.75, mitte - h / 2, 0.8, h, "num", "-0.252", size=11)
    text(s, ax + 0.65, mitte + 0.22, 1.0, 0.25, mono("AME", size=10.5))
    text(s, 0.15, unten + 0.62, 7.4, 0.28, codezeile(tr("modell_log |> marginal_effects()"), size=10.5))
    text(s, 0.15, unten + 0.9, 7.4, 0.28, mono(tr("educ_kat: hoch vs. niedrig: AME = -0.252, p < 0.001 ***"), size=10.5,
                                                color=GREEN, align=L))
    return s


FIGUREN = {
    "k09-dummy": dummy,
    "k09-fallset": fallset,
    "k09-augment": augment,
    "k09-randmittel": randmittel,
    "k09-ame": ame,
}
