"""Zeichenbibliothek für die Bausteine-Abbildungen des Buchs (Vertrag: BILDER.md).

Bildet die Folien-Helfer aus dem Workshop nach (gleiche Namen und Argumente), schreibt aber
SVG statt PowerPoint. Koordinaten in Zoll wie auf den Folien; 1 Zoll = 96 SVG-Einheiten.
Nur Python-Standardbibliothek.
"""
from html import escape

DPI = 96
PT = DPI / 72            # SVG-Einheiten pro Punkt
MIN_PT = 10              # kleinste erlaubte Schrift (BILDER.md §5.4)

INK, GRAY, GREEN, ORANGE = "#1E2D3C", "#6E7882", "#36A266", "#E6A033"
CARD, CARDLINE, WHITE = "#FAF7F1", "#D7D1C4", "#FFFFFF"
PALE, LIGHT, STICKER, DARKORANGE = "#FBECD2", "#F3CF97", "#FAC775", "#B86E0A"
STEIN = {"num": ("#85B7EB", "#042C53"), "txt": ("#AFA9EC", "#26215C"), "log": ("#F4C0D1", "#4B1528"),
         "na": ("#FFFFFF", "#6E7882"), "dim": ("#E4E1D8", "#A8A69E")}

SANS = "'Source Sans Pro', 'Source Sans 3', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"
MONO = "Menlo, Consolas, 'DejaVu Sans Mono', monospace"
L, C, RT = "start", "middle", "end"
MONO_EM = 0.612          # breiteste der Monospace-Schriften (Menlo/DejaVu 0,602)

SANS_REG = {' ': 0.286, '!': 0.286, '"': 0.415, '#': 0.623, '$': 0.623, '%': 0.916, '&': 0.689, "'": 0.262, '(': 0.343, ')': 0.343, '*': 0.412, '+': 0.623, ',': 0.286, '-': 0.442, '.': 0.286, '/': 0.288, '0': 0.625, '1': 0.573, '2': 0.583, '3': 0.61, '4': 0.623, '5': 0.603, '6': 0.636, '7': 0.573, '8': 0.618, '9': 0.636, ':': 0.286, ';': 0.286, '<': 0.623, '=': 0.623, '>': 0.623, '?': 0.573, '@': 1.046, 'A': 0.687, 'B': 0.687, 'C': 0.744, 'D': 0.744, 'E': 0.687, 'F': 0.629, 'G': 0.801, 'H': 0.744, 'I': 0.286, 'J': 0.515, 'K': 0.687, 'L': 0.573, 'M': 0.858, 'N': 0.744, 'O': 0.801, 'P': 0.687, 'Q': 0.801, 'R': 0.744, 'S': 0.687, 'T': 0.629, 'U': 0.744, 'V': 0.687, 'W': 0.972, 'X': 0.687, 'Y': 0.687, 'Z': 0.635, '[': 0.332, '\\': 0.288, ']': 0.332, '^': 0.623, '_': 0.573, '`': 0.515, 'a': 0.573, 'b': 0.573, 'c': 0.516, 'd': 0.573, 'e': 0.573, 'f': 0.313, 'g': 0.573, 'h': 0.573, 'i': 0.229, 'j': 0.229, 'k': 0.515, 'l': 0.229, 'm': 0.858, 'n': 0.573, 'o': 0.573, 'p': 0.573, 'q': 0.573, 'r': 0.343, 's': 0.515, 't': 0.31, 'u': 0.573, 'v': 0.515, 'w': 0.744, 'x': 0.515, 'y': 0.515, 'z': 0.515, '{': 0.344, '|': 0.268, '}': 0.344, '~': 0.623, 'Ä': 0.687, 'Ö': 0.801, 'Ü': 0.744, 'ä': 0.573, 'ö': 0.573, 'ü': 0.573, 'ß': 0.629, '–': 0.573, '—': 1.03, '·': 0.343, '→': 1.03, '←': 1.03, '↑': 0.805, '↓': 0.805, '×': 0.623, '±': 0.623, '≥': 0.623, '≤': 0.623, '…': 1.03, '„': 0.375, '“': 0.375, '”': 0.375, '‚': 0.229, '‘': 0.229, '’': 0.229, '€': 0.623, '°': 0.412, '²': 0.343, '³': 0.343, 'α': 0.598, 'χ': 0.555, '√': 0.608, '≈': 0.623, '≠': 0.623}
SANS_BOLD = {' ': 0.286, '!': 0.343, '"': 0.488, '#': 0.672, '$': 0.672, '%': 0.916, '&': 0.744, "'": 0.282, '(': 0.358, ')': 0.358, '*': 0.445, '+': 0.672, ',': 0.286, '-': 0.477, '.': 0.286, '/': 0.311, '0': 0.675, '1': 0.573, '2': 0.63, '3': 0.658, '4': 0.672, '5': 0.651, '6': 0.687, '7': 0.608, '8': 0.667, '9': 0.687, ':': 0.343, ';': 0.343, '<': 0.672, '=': 0.672, '>': 0.672, '?': 0.629, '@': 1.004, 'A': 0.744, 'B': 0.744, 'C': 0.763, 'D': 0.755, 'E': 0.687, 'F': 0.629, 'G': 0.801, 'H': 0.778, 'I': 0.286, 'J': 0.573, 'K': 0.744, 'L': 0.629, 'M': 0.924, 'N': 0.778, 'O': 0.814, 'P': 0.687, 'Q': 0.814, 'R': 0.744, 'S': 0.687, 'T': 0.646, 'U': 0.775, 'V': 0.702, 'W': 1.028, 'X': 0.706, 'Y': 0.687, 'Z': 0.686, '[': 0.358, '\\': 0.311, ']': 0.358, '^': 0.672, '_': 0.586, '`': 0.556, 'a': 0.573, 'b': 0.629, 'c': 0.573, 'd': 0.629, 'e': 0.573, 'f': 0.343, 'g': 0.629, 'h': 0.629, 'i': 0.286, 'j': 0.286, 'k': 0.573, 'l': 0.286, 'm': 0.916, 'n': 0.629, 'o': 0.629, 'p': 0.629, 'q': 0.629, 'r': 0.401, 's': 0.573, 't': 0.343, 'u': 0.629, 'v': 0.573, 'w': 0.801, 'x': 0.573, 'y': 0.573, 'z': 0.52, '{': 0.401, '|': 0.288, '}': 0.401, '~': 0.672, 'Ä': 0.744, 'Ö': 0.814, 'Ü': 0.775, 'ä': 0.573, 'ö': 0.629, 'ü': 0.629, 'ß': 0.629, '–': 0.586, '—': 1.03, '·': 0.343, '→': 1.03, '←': 1.03, '↑': 0.869, '↓': 0.869, '×': 0.672, '±': 0.672, '≥': 0.672, '≤': 0.672, '…': 1.03, '„': 0.515, '“': 0.515, '”': 0.515, '‚': 0.286, '‘': 0.286, '’': 0.286, '€': 0.672, '°': 0.445, '²': 0.343, '³': 0.352, 'α': 0.646, 'χ': 0.599, '√': 0.657, '≈': 0.672, '≠': 0.672}


def text_width(t, font, size, bold=False):
    """Breite in Zoll, gerechnet mit der breitesten Ausweichschrift (Arial/Systemschrift, Menlo)."""
    if font == MONO:
        return len(t) * MONO_EM * size / 72
    tab = SANS_BOLD if bold else SANS_REG
    return sum(tab.get(c, 0.62) for c in t) * size / 72


def _u(v):
    """Zoll → SVG-Einheiten, gerundet."""
    return f"{v * DPI:.2f}".rstrip("0").rstrip(".")


class Canvas:
    """Eine Zeichenfläche von w × h Zoll."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.items, self.sizes = [], []

    def add(self, el):
        self.items.append(el)

    def svg(self):
        if self.sizes and min(self.sizes) < MIN_PT:
            raise ValueError(f"Schrift kleiner als {MIN_PT} pt: {min(self.sizes)}")
        W, H = round(self.w * DPI), round(self.h * DPI)
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
                f'font-family="{escape(SANS, quote=True)}">')
        return head + "".join(self.items) + "</svg>\n"

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())


# --- Text --------------------------------------------------------------------------------------

def R(text, font=SANS, size=14, bold=False, italic=False, color=INK):
    return (text, dict(font=font, size=size, bold=bold, italic=italic, color=color))


def P(*runs, align=L, sb=None, sa=None, ls=None):
    return dict(runs=list(runs), align=align, sb=sb, sa=sa, ls=ls)


def _attrs(st):
    a = f' fill="{st["color"]}" font-size="{st["size"] * PT:.2f}"'
    if st["font"] != SANS:
        a += f' font-family="{escape(st["font"], quote=True)}"'
    if st["bold"]:
        a += ' font-weight="700"'
    if st["italic"]:
        a += ' font-style="italic"'
    return a


def _wrap(runs, w):
    """Teilt Runs wortweise in Zeilen; gibt Liste von Zeilen zurück, jede eine Liste (text, style)."""
    words = []
    for t, st in runs:
        for i, part in enumerate(t.split(" ")):
            tok = part if i == len(t.split(" ")) - 1 else part + " "
            if tok:
                words.append((tok, st))
    lines, cur, cw = [], [], 0.0
    for tok, st in words:
        tw = text_width(tok.rstrip(" "), st["font"], st["size"], st["bold"])
        if cur and cw + tw > w + 1e-9:
            lines.append(cur); cur, cw = [], 0.0
        cur.append((tok, st))
        cw += text_width(tok, st["font"], st["size"], st["bold"])
    if cur:
        lines.append(cur)
    # gleiche Stile in einer Zeile zusammenfassen
    out = []
    for ln in lines:
        merged = []
        for tok, st in ln:
            if merged and merged[-1][1] is st:
                merged[-1] = (merged[-1][0] + tok, st)
            else:
                merged.append((tok, st))
        if merged:
            merged[-1] = (merged[-1][0].rstrip(" "), merged[-1][1])
        out.append(merged)
    return out


def text(s, x, y, w, h, paras, anchor=None):
    """Textblock mit Absätzen und Zeilenumbruch. anchor="middle" zentriert senkrecht in h."""
    blocks, total = [], 0.0
    for pa in paras:
        sizes = [st["size"] for _, st in pa["runs"]] or [12]
        for sz in sizes:
            s.sizes.append(sz)
        lines = _wrap(pa["runs"], w)
        ls = pa["ls"] or 1.0
        top = (pa["sb"] or 0) / 72
        lh_list = []
        for ln in lines:
            m = max(st["size"] for _, st in ln)
            lh_list.append(ls / 72 if ls > 4 else 1.2 * m * ls / 72)
        bot = (pa["sa"] or 0) / 72
        blocks.append((pa, lines, lh_list, top, bot))
        total += top + sum(lh_list) + bot
    cy = y + ((h - total) / 2 if anchor == "middle" else 0)
    for pa, lines, lh_list, top, bot in blocks:
        cy += top
        for ln, lh in zip(lines, lh_list):
            m = max(st["size"] for _, st in ln)
            base = cy + (lh - m / 72) / 2 + 0.8 * m / 72
            ax = {L: x, C: x + w / 2, RT: x + w}[pa["align"]]
            ta = "" if pa["align"] == L else f' text-anchor="{pa["align"]}"'
            if len(ln) == 1:
                t, st = ln[0]
                s.add(f'<text x="{_u(ax)}" y="{_u(base)}"{ta}{_attrs(st)} xml:space="preserve">{escape(t)}</text>')
            else:
                spans = "".join(f"<tspan{_attrs(st)}>{escape(t)}</tspan>" for t, st in ln)
                s.add(f'<text x="{_u(ax)}" y="{_u(base)}"{ta} xml:space="preserve">{spans}</text>')
            cy += lh
        cy += bot


# --- Formen ------------------------------------------------------------------------------------

def rect(s, x, y, w, h, fill, line=None, lw=0.5, dash=False, rx=0):
    st = f' stroke="{line}" stroke-width="{lw * PT:.2f}"' if line else ""
    if dash and line:
        st += f' stroke-dasharray="{4 * lw * PT:.1f} {3 * lw * PT:.1f}"'
    r = f' rx="{_u(rx)}"' if rx else ""
    s.add(f'<rect x="{_u(x)}" y="{_u(y)}" width="{_u(w)}" height="{_u(h)}"{r} fill="{fill or "none"}"{st}/>')


def card(s, x, y, w, h, fill=CARD):
    rect(s, x, y, w, h, fill, CARDLINE)


def hline(s, x, y, w, color=CARDLINE, width=0.5):
    connector(s, x, y, x + w, y, color=color, width=width)


def connector(s, x0, y0, x1, y1, color=GRAY, width=1.5, dash=False):
    d = f' stroke-dasharray="{4 * width * PT:.1f} {3 * width * PT:.1f}"' if dash else ""
    s.add(f'<line x1="{_u(x0)}" y1="{_u(y0)}" x2="{_u(x1)}" y2="{_u(y1)}" stroke="{color}" '
          f'stroke-width="{width * PT:.2f}"{d}/>')


def vline(s, x, y0, y1, color=INK, width=1.5, dash=False):
    connector(s, x, y0, x, y1, color=color, width=width, dash=dash)


def outline(s, x, y, w, h, color=ORANGE, lw=2.25):
    rect(s, x, y, w, h, None, color, lw)


def arrow(s, x, y, w=0.5, h=0.32, color=GRAY):
    """Pfeil nach rechts (Form wie PowerPoints RIGHT_ARROW)."""
    hl = min(w, h) * 0.5
    t, b = y + h * 0.25, y + h * 0.75
    pts = [(x, t), (x + w - hl, t), (x + w - hl, y), (x + w, y + h / 2), (x + w - hl, y + h), (x + w - hl, b), (x, b)]
    s.add('<polygon points="' + " ".join(f"{_u(a)},{_u(b_)}" for a, b_ in pts) + f'" fill="{color}"/>')


def down_arrow(s, x, y, w=0.32, h=0.45, color=GRAY):
    hl = min(w, h) * 0.5
    l, r = x + w * 0.25, x + w * 0.75
    pts = [(l, y), (r, y), (r, y + h - hl), (x + w, y + h - hl), (x + w / 2, y + h), (x, y + h - hl), (l, y + h - hl)]
    s.add('<polygon points="' + " ".join(f"{_u(a)},{_u(b_)}" for a, b_ in pts) + f'" fill="{color}"/>')


def label_box(s, x, y, w, h, t, fill, color=WHITE, size=10.5, font=MONO, bold=True, rounded=True, align=C, margin=0.08):
    rect(s, x, y, w, h, fill, rx=min(w, h) * 0.17 if rounded else 0)
    text(s, x + margin, y, w - 2 * margin, h, [P(R(t, font=font, size=size, bold=bold, color=color), align=align)],
         anchor="middle")


def chip(s, x, y, t, w=None, fill=WHITE, size=10.5):
    w = w or (0.22 + text_width(t, MONO, size, True))
    rect(s, x, y, w, 0.34, fill, CARDLINE, 0.75)
    text(s, x + 0.06, y, w - 0.12, 0.34, [P(R(t, font=MONO, size=size, bold=True), align=C)], anchor="middle")
    return w


def numdot(s, x, y, n, fill=INK, d=0.36, size=12):
    s.add(f'<circle cx="{_u(x + d / 2)}" cy="{_u(y + d / 2)}" r="{_u(d / 2)}" fill="{fill}"/>')
    text(s, x, y, d, d, [P(R(str(n), font=MONO, size=size, bold=True, color=WHITE), align=C)], anchor="middle")


def eyebrow(s, x, y, w, t, color=GRAY, size=10.5, bold=True):
    text(s, x, y, w, 0.3, [P(R(t, font=MONO, size=size, bold=bold, color=color))])


def codebox(s, x, y, w, lines, size=13, h=None, label=None, hash_gray=True):
    """Code-Kasten: weiß mit dunkler Kante. # grau, [1] grün (Ausgabe), Fehler orange."""
    lh = size * 1.42 / 72
    top = 0.14 + (0.26 if label else 0)
    h = h or top + len(lines) * lh + 0.14
    rect(s, x, y, w, h, WHITE, CARDLINE, 0.75)
    rect(s, x, y, 0.07, h, INK)
    if label:
        text(s, x + 0.22, y + 0.1, w - 0.3, 0.25, [P(R(label, font=MONO, size=max(MIN_PT, 9), bold=True, color=GRAY))])
    ps = []
    for ln in lines:
        st = ln.lstrip()
        if st.startswith("#") and not st.startswith("#|") and hash_gray:
            col, bold = GRAY, False
        elif st.startswith("[") or st.startswith("#  ") or st.startswith("# A"):
            col, bold = GREEN, True
        elif st.startswith(("Fehler", "Error", "Warnung")):
            col, bold = DARKORANGE, True
        else:
            col, bold = INK, True
        ps.append(P(R(ln if ln else " ", font=MONO, size=size, bold=bold, color=col), ls=size * 1.42))
    text(s, x + 0.22, y + top, w - 0.3, h - top, ps)
    return h


# --- Bausteine ---------------------------------------------------------------------------------

def tok(s, x, y, t, kind, size=15, h=0.46):
    """Ein Code-Baustein. kind: fun (grün), arg (orange), obj (dunkel), sym (neutral), log, txt."""
    fill, color = {"fun": (GREEN, WHITE), "arg": (PALE, INK), "obj": (INK, WHITE), "sym": (WHITE, INK),
                   "log": STEIN["log"], "txt": STEIN["txt"]}[kind]
    w = text_width(t, MONO, size) + (0.14 if kind != "sym" else 0.04)
    label_box(s, x, y, w, h, t, fill, color=color, size=size, rounded=False, margin=0)
    return w


def tokens(s, x, y, parts, size=15, h=0.46):
    """Setzt Code-Bausteine nebeneinander; gibt die Mitten und das rechte Ende zurück."""
    mids = []
    for t, kind in parts:
        w = tok(s, x, y, t, kind, size, h)
        mids.append(x + w / 2)
        x += w + 0.03
    return mids, x


def stein(s, x, y, w, h, kind, t, tag=None, size=13):
    """Ein Baustein: Noppen oben, Farbe je Datentyp; NA ist leer und gestrichelt."""
    fill, ink = STEIN[kind]
    n = max(2, round(w / 0.42))
    for i in range(n):
        rect(s, x + (i + 0.5) * w / n - 0.09, y - 0.06, 0.18, 0.07, fill, ink if kind == "na" else None, 0.5)
    rect(s, x, y, w, h, fill, ink, 0.75, dash=(kind == "na"))
    if t != "":
        tw = w - 0.08 - (0.6 if tag else 0)          # mit Aufkleber: Wert links davon
        text(s, x + 0.04, y, tw, h, [P(R(t, font=MONO, size=size, bold=True, color=ink), align=C)], anchor="middle")
    if tag:
        label_box(s, x + w - 0.57, y + h - 0.23, 0.55, 0.21, tag, STICKER, color=INK, size=10, rounded=False, margin=0.02)


def schild(s, x, y, name, w=1.1):
    """Das dunkle Namensschild: So heißt das Objekt."""
    label_box(s, x, y, w, 0.36, name, INK, size=12.5, rounded=False)


def turm(s, x, base, w, h, kind, werte):
    """Stapelt Steine von unten nach oben; die Grundlinie ist base. Erster Listenwert unten."""
    for i, t in enumerate(werte):
        k = kind(i) if callable(kind) else kind
        stein(s, x, base - (i + 1) * (h + 0.07), w, h, k, t)
