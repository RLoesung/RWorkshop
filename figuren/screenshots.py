"""RStudio-Screenshots für Kap. 1 aufbereiten: einheitlicher Maßstab, dünner Rahmen, grüne Bereichsnummer.

Aufgenommen in RStudio 2026.01 mit R 4.6.2, helles Theme, Zoom 200 % im Projekt R-Workshop (siehe NEWS, 17.11.2026).
Eingang: Ausschnitte (JPEG) und ihre Breite in Fenster-Einheiten; 1 Einheit = 0,871 RStudio-Pixel. Ausgang:
PNG in Bilder/rstudio/ mit doppelter Pixeldichte, damit die Schrift in allen Bildern gleich groß erscheint.

Aufruf: python3 figuren/screenshots.py <Ordner mit den Ausschnitten>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

GREEN, ORANGE, CARDLINE, WHITE = "#36A266", "#E6A033", "#D7D1C4", "#FFFFFF"
PX_JE_EINHEIT = 2560 / 1469 / 2            # Fensterpunkte je Einheit, geteilt durch den Zoom 200 %
DICHTE = 2                                 # Pixel je Bildschirmpixel im Buch
ZIEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Bilder", "rstudio")
SCHRIFT = ("/System/Library/Fonts/Menlo.ttc", 1)

# Name: (Breite in Einheiten, Bereichsnummer oder None, unten abschneiden in Rohpixeln, Hervorhebung in Rohpixeln)
BILDER = {
    "konsole": (788, 2, 0, None),
    "editor": (788, 1, 16, None),
    "environment": (660, 3, 0, None),
    "files": (660, 4, 0, None),
    "packages": (819, 4, 0, None),
    "help": (819, 4, 0, None),
    "optionen": (759, None, 76, (266, 352, 742, 478)),   # Abschnitt Workspace; Knöpfe sind bei 200 % abgeschnitten
    "projekt": (612, None, 0, None),
    # Tab Completion im Editor (Bildschirm-Ausschnitte, Breite auf Fenster-Einheiten umgerechnet: mal 1469/1456)
    "vorschlaege": (807, 1, 0, None),
    "argumente": (878, 1, 0, None),
    "paketliste": (1065, 1, 0, None),
}
QUELLE = {"optionen": "options", "projekt": "project"}
OHNE_REITERLEISTE = {"vorschlaege", "argumente", "paketliste"}   # Ausschnitte ohne Reiterleiste: nichts übermalen


def breite_im_buch(einheiten):
    """Anzeigebreite im Buch in CSS-Pixeln."""
    return round(einheiten * PX_JE_EINHEIT)


def aufbereiten(roh, einheiten, nummer=None, unten=0, markierung=None, reiterleiste=True):
    """Gibt das fertige Bild zurück: skaliert auf doppelte Dichte, mit Rahmen und Nummer."""
    if unten:
        roh = roh.crop((0, 0, roh.width, roh.height - unten))
    faktor = breite_im_buch(einheiten) * DICHTE / roh.width
    bild = roh.convert("RGB").resize((round(roh.width * faktor), round(roh.height * faktor)), Image.LANCZOS)
    d = ImageDraw.Draw(bild)
    if markierung:
        x0, y0, x1, y1 = (round(v * faktor) for v in markierung)
        d.rounded_rectangle((x0, y0, x1, y1), radius=10, outline=ORANGE, width=5)
    w, h = bild.size
    d.rectangle((0, 0, w - 1, h - 1), outline=CARDLINE, width=2)
    if nummer is not None:
        # die Knöpfe zum Verkleinern und Vergrößern rechts in der Reiterleiste mit deren Grundfarbe übermalen
        if reiterleiste:
            grund = bild.getpixel((w - 150, 6))
            d.rectangle((w - 120, 2, w - 3, 40), fill=grund)
        r = 22
        cx, cy = w - 14 - r, 8 + r
        d.ellipse((cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3), fill=WHITE)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN)
        schrift = ImageFont.truetype(SCHRIFT[0], 26, index=SCHRIFT[1])
        d.text((cx, cy), str(nummer), fill=WHITE, font=schrift, anchor="mm")
    return bild


def main(ordner):
    os.makedirs(ZIEL, exist_ok=True)
    for name, (einheiten, nummer, unten, markierung) in BILDER.items():
        roh = Image.open(os.path.join(ordner, QUELLE.get(name, name) + ".jpg"))
        bild = aufbereiten(roh, einheiten, nummer, unten, markierung, name not in OHNE_REITERLEISTE)
        pfad = os.path.join(ZIEL, name + ".png")
        bild.save(pfad, optimize=True)
        print(f"{name}.png {bild.size[0]}x{bild.size[1]}, im Buch {breite_im_buch(einheiten)} px breit")


if __name__ == "__main__":
    main(sys.argv[1])
