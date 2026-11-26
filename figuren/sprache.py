"""Sprachschalter für die Abbildungsskripte: aktuelle Sprache und Übersetzungs-Lookup."""
import en

_SPRACHEN = ("de", "en")
_aktuell = "de"


def setze(sprache):
    global _aktuell
    if sprache not in _SPRACHEN:
        raise ValueError(f"Unbekannte Sprache: {sprache!r} (erlaubt: de, en)")
    _aktuell = sprache


def aktuell():
    return _aktuell


def t(text):
    """Deutsch: text unverändert. Englisch: Eintrag aus en.EN, sonst KeyError."""
    if _aktuell == "de":
        return text
    try:
        return en.EN[text]
    except KeyError:
        raise KeyError(f"Keine englische Übersetzung für: {text!r}") from None
