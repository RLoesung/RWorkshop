"""Cover des Buchs (Design „Baukasten“): Titel, drei Türme aus Bausteinen und die Begleitfigur „hallo“.

Aufruf: python3 figuren/cover.py — schreibt Bilder/cover.svg.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lego  # noqa: E402
from lego import R, P, text, rect, L  # noqa: E402


def cover_spiel(path, bg, ink, sub, steine, plate, frame=None):
    """Pastell-Cover mit Begleitfigur neben drei Türmen."""
    import begleiter as figur
    W, H = 3.0, 4.2
    s = lego.Canvas(W, H)
    rund = "'Fredoka', 'Nunito', 'Arial Rounded MT Bold', system-ui, sans-serif"
    rect(s, 0, 0, W, H, bg, frame, 1.5 if frame else 0.5)
    x = 0.24
    text(s, x, 0.28, W - 2 * x, 0.3, [P(R("ALLBUS 2023 · tidyverse · mariposa", size=10, bold=True, color=sub), align=L)])
    text(s, x, 0.56, W - 2 * x, 0.6, [P(R("R Workshop", font=rund, size=26, bold=True, color=ink), align=L)])
    text(s, x, 1.02, W - 2 * x, 0.4, [P(R("Sozialwissenschaften", font=rund, size=16, color=ink), align=L)])
    text(s, x, 1.42, W - 2 * x, 0.6, [P(R("Einführung in die statistische Datenanalyse mit tidyverse und mariposa", size=11, color=sub), align=L)])
    bw, bh, gap = 0.5, 0.28, 0.1
    px, base = 0.3, 3.62
    for i, (fill, line) in enumerate(steine):
        tx = px + i * (bw + gap)
        for j in range(3 + (i % 2)):
            n = 2
            for k in range(n):
                rect(s, tx + (k + 0.5) * bw / n - 0.08, base - (j + 1) * (bh + 0.07) - 0.06, 0.16, 0.07, fill, line, 0.75, rx=0.02)
            rect(s, tx, base - (j + 1) * (bh + 0.07), bw, bh, fill, line, 0.75, rx=0.04)
    rect(s, 0.14, base, W - 0.28, 0.12, plate, None, 0.5, rx=0.04)
    s.add(f'<g transform="translate({round(2.0 * 96)} {round(2.42 * 96)}) scale(0.88)">{figur.figur("hallo")}</g>')
    text(s, x, 3.82, W - 2 * x, 0.3, [P(R("Yannick Diehl · Daniel Moosdorf", size=10, color=sub), align=L)])
    s.save(path)


if __name__ == "__main__":
    ziel = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Bilder", "cover.svg")
    cover_spiel(ziel, "#FFF4E8", "#1E2D3C", "#6E6157",
                [("#BFE3F7", "#86B9DE"), ("#CDEFD9", "#8FCBA6"), ("#DCD6F8", "#A79FE2")], "#F7C9DA")
    print("Bilder/cover.svg geschrieben")
