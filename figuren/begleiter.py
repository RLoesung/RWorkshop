"""Begleitfiguren für die Kästen im Buch (Design „Baukasten“): ein Baustein aus den Abbildungen des Buchs mit Gesicht, Strichärmchen und -beinen.

Der Körper ist der Stein aus figuren/lego.py (zwei Noppen, Füllung und Kante in den Steinfarben),
es gibt keinen eigenen Kopf. Je Kastentyp eine Steinfarbe und eine Haltung.

Aufruf: python3 figuren/begleiter.py — schreibt Bilder/begleiter/*.svg und begleiter.scss.
"""
import os
import sys

INK = "#1E2D3C"
CARD = "#FAF7F1"
ORANGE = "#E6A033"
WANGE = "#F29BB8"

STEINE = {
    "num":     ("#85B7EB", "#042C53"),
    "txt":     ("#AFA9EC", "#26215C"),
    "log":     ("#F4C0D1", "#4B1528"),
    "gruen":   ("#BFE6CD", "#1E5C3A"),
    "tuerkis": ("#BDE6E1", "#1D5753"),
    "orange":  ("#FAC775", "#7A4A00"),
    "creme":   ("#FBECD2", "#7A4A00"),
}

FIGUREN = {
    #  name        Stein      Haltung
    "hallo":     ("num",     "winken"),
    "hinweis":   ("txt",     "buch"),
    "tipp":      ("gruen",   "lampe"),
    "spss":      ("tuerkis", "lampe"),
    "vorsicht":  ("orange",  "stopp"),
    "mariposa":  ("log",     "falter"),
    "uebung":    ("num",     "stemmen"),
    "denken":    ("txt",     "denken"),
    "journal":   ("creme",   "block"),
}


def _glied(x0, y0, x1, y1):
    return f'<path d="M{x0} {y0} L{x1} {y1}" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" fill="none"/>'


def _hand(x, y, r=4.2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CARD}" stroke="{INK}" stroke-width="2.2"/>'


def figur(name):
    stein, haltung = FIGUREN[name]
    fill, kante = STEINE[stein]
    p = []
    # Beine und Füße
    p.append(_glied(48, 92, 46, 114) + _glied(72, 92, 74, 114))
    p.append(f'<ellipse cx="42" cy="116" rx="7" ry="3.6" fill="{INK}"/><ellipse cx="78" cy="116" rx="7" ry="3.6" fill="{INK}"/>')
    # Arme (Schulter am Stein, Hand am Ende)
    arme = {
        "winken":  [(28, 70, 15, 86), (92, 66, 108, 44)],
        "buch":    [(28, 70, 15, 86), (92, 70, 104, 84)],
        "lampe":   [(28, 70, 15, 86), (92, 64, 106, 42)],
        "stopp":   [(28, 70, 15, 86), (92, 62, 108, 52)],
        "falter":  [(28, 70, 15, 86), (92, 64, 106, 44)],
        "stemmen": [(30, 52, 42, 22), (90, 52, 78, 22)],
        "denken":  [(28, 70, 15, 86), (92, 72, 82, 80)],
        "block":   [(28, 70, 16, 82), (92, 70, 104, 80)],
    }[haltung]
    for x0, y0, x1, y1 in arme:
        p.append(_glied(x0, y0, x1, y1))
    # Körper: Stein mit zwei Noppen (wie lego.stein)
    p.append(f'<rect x="38" y="31" width="15" height="8" rx="2" fill="{fill}" stroke="{kante}" stroke-width="2.4"/>')
    p.append(f'<rect x="67" y="31" width="15" height="8" rx="2" fill="{fill}" stroke="{kante}" stroke-width="2.4"/>')
    p.append(f'<rect x="26" y="38" width="68" height="55" rx="6" fill="{fill}" stroke="{kante}" stroke-width="2.6"/>')
    # Gesicht auf dem Stein
    if haltung == "stopp":
        p.append(f'<path d="M42 54 L51 57 M78 54 L69 57" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
    p.append(f'<circle cx="49" cy="63" r="3.8" fill="{INK}"/><circle cx="71" cy="63" r="3.8" fill="{INK}"/>')
    p.append(f'<circle cx="50.3" cy="61.7" r="1.2" fill="#FFFFFF"/><circle cx="72.3" cy="61.7" r="1.2" fill="#FFFFFF"/>')
    p.append(f'<circle cx="40" cy="73" r="4.6" fill="{WANGE}" opacity="0.75"/><circle cx="80" cy="73" r="4.6" fill="{WANGE}" opacity="0.75"/>')
    if haltung == "stopp":
        p.append(f'<ellipse cx="60" cy="77" rx="4" ry="3.6" fill="{INK}"/>')
    elif haltung == "denken":
        p.append(f'<path d="M53 76 Q60 79 67 75" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    else:
        p.append(f'<path d="M51 73 Q60 82 69 73" stroke="{INK}" stroke-width="2.8" fill="none" stroke-linecap="round"/>')
    # Hände und Dinge
    if haltung == "winken":
        p.append(f'<path d="M113 34 q5 4 3 10 M118 29 q7 6 4 15" stroke="{ORANGE}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    if haltung == "buch":
        p.append(f'<g transform="translate(106 88) rotate(-8)"><rect x="-8" y="-14" width="22" height="28" rx="2" fill="{CARD}" stroke="{INK}" stroke-width="2.2"/>'
                 f'<rect x="-8" y="-14" width="5" height="28" fill="#36A266" stroke="{INK}" stroke-width="2.2"/>'
                 f'<path d="M1 -6 H10 M1 0 H10 M1 6 H7" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/></g>')
    if haltung == "lampe":
        p.append(f'<circle cx="108" cy="24" r="10" fill="#FAC775" stroke="{INK}" stroke-width="2.2"/>')
        p.append(f'<rect x="103" y="33" width="10" height="6" rx="1.5" fill="{CARD}" stroke="{INK}" stroke-width="2"/>')
        p.append(f'<path d="M108 8 V3 M95 14 L91 11 M121 14 L125 11" stroke="{ORANGE}" stroke-width="2.4" stroke-linecap="round"/>')
    if haltung == "stopp":
        p.append(f'<rect x="103" y="38" width="15" height="19" rx="6" fill="{CARD}" stroke="{INK}" stroke-width="2.2"/>')
        p.append(f'<text x="112" y="27" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, sans-serif" font-weight="700" font-size="17" fill="{ORANGE}">!</text>')
    if haltung == "falter":
        p.append(f'<g transform="translate(110 26) rotate(-14)">'
                 f'<ellipse cx="-8" cy="-5" rx="8" ry="10" fill="#AFA9EC" stroke="{INK}" stroke-width="2"/>'
                 f'<ellipse cx="8" cy="-5" rx="8" ry="10" fill="#85B7EB" stroke="{INK}" stroke-width="2"/>'
                 f'<ellipse cx="-6" cy="8" rx="5.5" ry="6.5" fill="#85B7EB" stroke="{INK}" stroke-width="2"/>'
                 f'<ellipse cx="6" cy="8" rx="5.5" ry="6.5" fill="#AFA9EC" stroke="{INK}" stroke-width="2"/>'
                 f'<line x1="0" y1="-12" x2="0" y2="14" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/></g>')
    if haltung == "stemmen":
        f2, k2 = STEINE["log"]
        p.append(f'<rect x="48" y="0" width="9" height="6" rx="1.5" fill="{f2}" stroke="{k2}" stroke-width="2"/>')
        p.append(f'<rect x="63" y="0" width="9" height="6" rx="1.5" fill="{f2}" stroke="{k2}" stroke-width="2"/>')
        p.append(f'<rect x="38" y="5" width="44" height="19" rx="4" fill="{f2}" stroke="{k2}" stroke-width="2.2"/>')
    if haltung == "denken":
        p.append(f'<circle cx="100" cy="32" r="3" fill="{CARD}" stroke="{INK}" stroke-width="1.8"/>')
        p.append(f'<circle cx="106" cy="22" r="4.2" fill="{CARD}" stroke="{INK}" stroke-width="1.8"/>')
        p.append(f'<circle cx="114" cy="8" r="10" fill="{CARD}" stroke="{INK}" stroke-width="2.2"/>')
        p.append(f'<text x="114" y="13.5" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, sans-serif" font-weight="700" font-size="15" fill="{INK}">?</text>')
    if haltung == "block":
        p.append(f'<g transform="translate(10 78) rotate(-6)"><rect x="-9" y="-13" width="20" height="26" rx="2" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
                 f'<path d="M-5 -4 H7 M-5 2 H7 M-5 8 H3" stroke="{ORANGE}" stroke-width="1.8" stroke-linecap="round"/>'
                 f'<path d="M-5 -13 v-4 M1 -13 v-4 M7 -13 v-4" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/></g>')
        p.append(f'<g transform="translate(104 80) rotate(30)"><rect x="-2.6" y="-22" width="5.2" height="20" fill="{ORANGE}" stroke="{INK}" stroke-width="1.6"/>'
                 f'<path d="M-2.6 -2 L0 4 L2.6 -2 Z" fill="{CARD}" stroke="{INK}" stroke-width="1.4"/></g>')
    for x0, y0, x1, y1 in arme:
        if not (haltung == "stopp" and x1 > 100):
            p.append(_hand(x1, y1))
    return "".join(p)


def svg(name):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -4 128 126" width="128" height="126">'
            f'{figur(name)}</svg>\n')


HIER = os.path.dirname(os.path.abspath(__file__))
SVG_ORDNER = os.path.join(HIER, "..", "Bilder", "begleiter")
SCSS = os.path.join(HIER, "..", "begleiter.scss")


def scss():
    """Die Figuren als SCSS-Variablen $fig-<name> mit Daten-URL (für theme.scss und zusatz.scss)."""
    import base64
    zeilen = ["/*-- scss:defaults --*/", "",
              "// Erzeugt von figuren/begleiter.py: die Begleitfiguren als Daten-URL. Nicht von Hand ändern.", ""]
    for n in FIGUREN:
        b64 = base64.b64encode(svg(n).encode("utf-8")).decode()
        zeilen.append(f'$fig-{n}: url("data:image/svg+xml;base64,{b64}");')
    return "\n".join(zeilen + ["", "/*-- scss:rules --*/", ""])


if __name__ == "__main__":
    os.makedirs(SVG_ORDNER, exist_ok=True)
    for n in FIGUREN:
        open(os.path.join(SVG_ORDNER, f"{n}.svg"), "w").write(svg(n))
    open(SCSS, "w").write(scss())
    print(f"{len(FIGUREN)} Figuren nach Bilder/begleiter/, begleiter.scss geschrieben")
