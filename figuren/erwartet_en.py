"""Erwartete Abweichungen zwischen deutscher und englischer Fassung (Design §8.3).

ERWARTET: Kapitelname -> Liste (Teilstring der Meldung, Begründung).
Passende Meldungen zählen im Lauf von check_en.py nicht als Fehler und werden als „erwartet“ gedruckt.
Jede Meldung nennt die erste Codezeile ihrer Zelle; damit sind die Teilstrings eindeutig.
"""
ERWARTET = {
    "02-Quarto": [
        ("deutsche Setup-Datei: - Shared code goes into `R/`.",
         "advice for the reader's own project, not the book's setup"),
    ],
    "04-Datenimport": [
        ("Ausgabeblock 1 (allbus):",
         "za_nr 8831/8833 und version 1.3.0/1.0.0 sind Dateieigenschaften; splt23_2 zeigt -15 "
         "in der englischen Fassung als NA (Folge des beschlossenen set_na()-Schritts)"),
        ("Ausgabeblock 3 (allbus |> find_var(\"muslim\"))",
         "find_var() trifft die englischen Labels anders: \"muslim\" findet sechs Variablen"),
        ("Ausgabeblock 5 (allbus |> find_var(\"age\"",
         "find_var() trifft die englischen Labels anders: die deutsche Suche \"alter\" wurde zu \"age\""),
        ("Ausgabeblock 27 (allbus |>):",
         "gleiche Zahlen in anderer Zeilenreihenfolge (set_na()-Demo)"),
    ],
    "05-Datentransformation": [
        ("Ausgabeblock 4 (allbus |>):",
         "gleiche Zahlen in anderer Zeilenreihenfolge: count() sortiert die englischen Kategorien "
         "alphabetisch (high, low, medium statt hoch, mittel, niedrig)"),
        ("The six `mm` items are established in German-language research",
         "Autorennamen Decker & Brähler"),
        ("- Schulz, A., Müller, P.",
         "Autorenname Müller in der Literaturangabe"),
        ("- Decker, O., & Brähler, E.",
         "deutschsprachige Quelle: Autorenname und Originaltitel, englische Übersetzung in Klammern"),
        ("deutsche Setup-Datei: Everything you have built step by step",
         "R/prep.R ist der Dateiname im Projekt der Lesenden, wie in der Abbildung k05-pipeline und "
         "nach STYLE.md §13 (Dateien im Buchprojekt behalten ihren Namen); der versteckte Setup lädt R/_common_en.R"),
        ("deutsche Setup-Datei: In your own project, save the pipeline below",
         "Rat für das eigene Projekt der Lesenden; der Satz nennt R/prep_en.R als englische Fassung im Repository"),
        ("deutsche Setup-Datei: With this pipeline, the dataset is ready",
         "wie oben: source(\"R/prep.R\") im Fließtext, passend zur Abbildung k05-pipeline"),
    ],
    "06-Grafiken-Grundlagen": [
        ("deutsche Setup-Datei: All plots in this book automatically use the theme",
         "theme_rworkshop() ist in beiden Fassungen in R/_common.R definiert (R/_common_en.R lädt sie); "
         "source(\"R/_common.R\") ist ein Rat für das eigene Projekt der Lesenden"),
    ],
}
