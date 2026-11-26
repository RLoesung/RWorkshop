"""Abbildungen für Kap. 8 „Latente Strukturen“ (BILDER.md §6). Werte aus den Buch-Chunks.

Alle Werte stammen aus ALLBUS 2023 (ALLBUS2023.sav), geprüft mit R 4.5.3 und mariposa 0.7.4, nach dem
Setup-Chunk von Kap. 8 (R/prep.R: mm02 und mm05 umgepolt zu mm02r und mm05r). EFA und Reliabilität rechnen
gewichtet (wghtpew).
"""
import math

from lego import (Canvas, R, P, text, stein, outline, connector, vline, polygon, arrow, kiste, text_width, _u, INK,
                  GRAY, GREEN, CARD, PT, MONO, C, RT)
from kap03 import mono, notiz, platte
from kap04 import kopf
import sprache
from sprache import t as tr

SPRACHFAEHIG = True  # alle Texte laufen über tr(); build.py --en baut dieses Modul

ITEMS = ["mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06"]
# Die ersten drei Befragten, die alle sechs Items beantwortet haben (Zeilen 1, 5, 6 von allbus)
REIHEN = [("1", ["5", "5", "4", "2", "2", "2"]), ("5", ["2", "4", "4", "3", "5", "6"]),
          ("6", ["3", "5", "3", "7", "2", "3"])]


def faktor(s, cx, cy, rx, ry, name, size=12.5):
    """Nicht gemessener (latenter) Faktor: gestrichelte Ellipse mit dunkler Kante, darin nur sein Name.
    Keine Werte und keine Noppen, damit er nicht wie ein leerer Stein (NA) aussieht."""
    lw = 1.5 * PT
    s.add(f'<ellipse cx="{_u(cx)}" cy="{_u(cy)}" rx="{_u(rx)}" ry="{_u(ry)}" fill="{CARD}" stroke="{INK}" '
          f'stroke-width="{lw:.2f}" stroke-dasharray="{4 * lw:.1f} {3 * lw:.1f}"/>')
    text(s, cx - rx, cy - ry, 2 * rx, 2 * ry, [P(R(name, size=size, bold=True, color=INK), align=C)], anchor="middle")


def pfeil(s, x0, y0, x1, y1, color=INK, width=1.25, spitze=0.13):
    """Linie von (x0, y0) mit Pfeilspitze bei (x1, y1)."""
    dx, dy = x1 - x0, y1 - y0
    ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
    bx, by = x1 - ux * spitze, y1 - uy * spitze
    b = spitze * 0.45
    connector(s, x0, y0, bx, by, color=color, width=width)
    polygon(s, [(x1, y1), (bx - uy * b, by + ux * b), (bx + uy * b, by - ux * b)], color)


def rand(cx, cy, rx, ry, tx, ty):
    """Punkt auf dem Rand der Ellipse in Richtung (tx, ty)."""
    dx, dy = tx - cx, ty - cy
    t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + t * dx, cy + t * dy


# 8.1 Konzept-Kasten „Was ist eine latente Variable?“ ----------------------------------------------
def latenter_faktor():
    s = Canvas(6.75, 3.2)
    ix, step, w, h, pitch, top = 1.0, 0.78, 0.56, 0.32, 0.42, 1.8
    xs = [ix + j * step for j in range(6)]
    mitten = [x + w / 2 for x in xs]
    cx, cy, rx, ry = (xs[0] + xs[-1] + w) / 2, 0.47, 1.05, 0.3
    faktor(s, cx, cy, rx, ry, tr("Islamfeindlichkeit"))
    text(s, cx + rx + 0.15, cy - 0.15, 1.6, 0.3, notiz(tr("nicht gemessen"), size=10.5, align="start"), anchor="middle")
    ky = 1.38
    for x, m, it in zip(xs, mitten, ITEMS):
        pfeil(s, *rand(cx, cy, rx, ry, m, ky - 0.04), m, ky - 0.04)
        kopf(s, x, w, ky, it, size=10.5)
    kopf(s, 0.15, 0.6, ky, "respid", size=10.5)
    for i, (rid, werte) in enumerate(REIHEN):
        y = top + i * pitch
        text(s, 0.15, y, 0.6, h, mono(rid, size=10.5, color=GRAY, align=RT), anchor="middle")
        for x, v in zip(xs, werte):
            stein(s, x, y, w, h, "num", v, size=11)
    unten = top + 2 * pitch + h
    platte(s, ix - 0.1, unten + 0.07, xs[-1] + w + 0.1 - (ix - 0.1))
    text(s, xs[-1] + w + 0.2, top, 1.0, unten - top, notiz(tr("gemessen"), size=10.5, align="start"), anchor="middle")
    return s


# 8.3.3 Ergebnisobjekt efa_vor aus den Chunks efa-vor, efa-bartlett, efa-msa und efa-1 -----------------
# efa_vor ist eine Liste mit 34 Elementen; gezeigt sind vier, in ihrer Reihenfolge in names(efa_vor)
# (loadings 1, eigenvalues 3, kmo 9, bartlett 10), dahinter Auslassungspunkte. $kmo und $bartlett sind selbst Listen.
LADUNGEN = ["0.811", "0.664", "0.753", "0.769", "0.657", "0.769"]       # efa-1, Component Matrix, Reihenfolge mm01 … mm06
EIGENWERTE = ["3.281", "0.833", "0.555", "0.479", "0.439", "0.412"]     # efa-1, Total Variance Explained
MSA = ["0.857", "0.876", "0.874", "0.849", "0.851", "0.867"]            # efa-msa, gerundet auf drei Stellen


def ergebnisobjekt():
    s = Canvas(7.45, 4.3)
    hh, tw, size = 0.27, 0.62, 10.5
    faecher = kiste(s, 0.15, 0.12, [("loadings", 1.0), ("eigenvalues", 1.2), ("kmo", 2.0), ("bartlett", 2.45)],
                    h=3.2, name=tr("efa_vor"), mehr=0.4)
    boden = faecher[0][3] - 0.24                                 # Unterkante aller Steine, in allen Fächern gleich
    # Türme in den beiden ersten Fächern
    for (fx, fo, fb, _), werte, spalte in [(faecher[0], LADUNGEN, "PC1"), (faecher[1], EIGENWERTE, None)]:
        tx = fx + (fb - tw) / 2
        _turm(s, tx, boden, tw, hh, werte, size)
        if spalte:
            text(s, tx, boden - 6 * (hh + 0.07) - 0.3, tw, 0.22, mono(spalte, size=10, color=GRAY, bold=False))
    # $kmo und $bartlett: Kisten in der Kiste
    innen = [(faecher[2], [("overall", 0.85), ("per_item", 0.95)], [["0.862"], MSA]),
             (faecher[3], [("chi_sq", 0.98), ("df", 0.5), ("p_value", 0.8)], [["6532.633"], ["15"], ["0"]])]
    for (fx, fo, fb, fu), unter, inhalte in innen:
        breite = sum(b for _, b in unter)
        ux = fx + (fb - breite) / 2
        ufaecher = kiste(s, ux, fo + 0.1, unter, h=fu - 0.1 - (fo + 0.1), size=10, kopf=0.3)
        for (gx, _, gb, _), werte in zip(ufaecher, inhalte):
            sw = tw if len(werte[0]) == 5 else max(0.4, 0.12 + text_width(werte[0], MONO, size, True))
            _turm(s, gx + (gb - sw) / 2, boden, sw, hh, werte, size)
            if werte is MSA:                                     # efa_vor$kmo$per_item
                hoehe = 6 * (hh + 0.07) - 0.07
                outline(s, gx + (gb - sw) / 2 - 0.07, boden - hoehe - 0.12, sw + 0.14, hoehe + 0.19, color=GREEN,
                        lw=1.75)
                code_mitte = gx + gb / 2
    text(s, code_mitte - 1.2, faecher[0][3] + 0.14, 2.4, 0.28, mono(tr("efa_vor$kmo$per_item"), size=11))
    return s


def _turm(s, x, boden, w, h, werte, size):
    """Turm von oben nach unten (erster Wert oben), die Unterkante des untersten Steins liegt bei boden."""
    top = boden - len(werte) * (h + 0.07) + 0.07
    for i, v in enumerate(werte):
        stein(s, x, top + i * (h + 0.07), w, h, "num", v, size=size)


# 8.7.4 Korrigierte Item-Total-Korrelation aus dem Chunk reliability-summary, Zeile mm05r --------------
def item_total():
    s = Canvas(7.6, 2.75)
    h, pitch, top, w, step, ix, ky = 0.32, 0.42, 0.74, 0.5, 0.6, 1.0, 0.27
    xs = [ix + j * step for j in range(6)]
    kopf(s, 0.15, 0.6, ky, "respid", size=10.5)
    for x, it in zip(xs, ITEMS):
        kopf(s, x, w, ky, it, size=10.5)
    sx, sw, mx = 5.5, 0.6, 6.55
    text(s, sx - 0.5, 0.1, sw + 1.0, 0.42, [P(R(tr("Summe ohne"), size=10.5, bold=True), align=C, ls=0.95),
                                            P(R("mm05r", font=MONO, size=10.5, bold=True), align=C, ls=0.95)],
         anchor="middle")
    kopf(s, mx, w, ky, "mm05r", size=10.5)
    for i, (rid, werte) in enumerate(REIHEN):
        y = top + i * pitch
        text(s, 0.15, y, 0.6, h, mono(rid, size=10.5, color=GRAY, align=RT), anchor="middle")
        for j, (x, v) in enumerate(zip(xs, werte)):
            stein(s, x, y, w, h, "dim" if j == 4 else "num", v, size=11)
        summe = sum(int(v) for j, v in enumerate(werte) if j != 4)
        stein(s, sx, y, sw, h, "num", str(summe), size=11)
        stein(s, mx, y, w, h, "num", werte[4], size=11)
    unten = top + 2 * pitch + h
    platte(s, ix - 0.1, unten + 0.07, xs[-1] + w + 0.1 - (ix - 0.1))
    text(s, xs[4] + w / 2 - 0.8, unten + 0.2, 1.6, 0.25, notiz(tr("nicht in der Summe"), size=10.5))
    mitte = (top + unten) / 2
    ax = xs[-1] + w + 0.2
    arrow(s, ax, mitte - 0.14, w=sx - 0.15 - ax, h=0.28, color=GREEN)
    platte(s, sx - 0.1, unten + 0.07, mx + w + 0.1 - (sx - 0.1))
    # Klammer unter den beiden Türmen, die korreliert werden
    k0, k1, by = sx + sw / 2, mx + w / 2, unten + 0.24
    vline(s, k0, unten + 0.16, by, color=INK, width=1.25)
    vline(s, k1, unten + 0.16, by, color=INK, width=1.25)
    connector(s, k0, by, k1, by, color=INK, width=1.25)
    vline(s, (k0 + k1) / 2, by, by + 0.08, color=INK, width=1.25)
    m = (k0 + k1) / 2
    text(s, m - 1.1, by + 0.12, 2.2, 0.45, [P(R("Corrected Item-Total", font=MONO, size=10, color=GRAY), align=C),
                                           P(R("0.520", font=MONO, size=12, bold=True), align=C, sb=1)])
    return s


FIGUREN = {
    "k08-latenter-faktor": latenter_faktor,
    "k08-ergebnisobjekt": ergebnisobjekt,
    "k08-item-total": item_total,
}
