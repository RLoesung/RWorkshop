"""Übersetzungstabelle deutscher Abbildungstexte ins Englische (deutscher Text → englischer Text).

Wertelabels und Variablenlabels stammen aus ZA8833 (ALLBUS2023_en.sav); die Kennbuchstaben der fehlenden
Werte (NA(g), NA(l), NA(n), NA(o)) aus na_frequencies(allbus$mm01) nach set_na() mit den Codes aus Design §5.3.
"""

EN = {
    # Kap. 4: Beschriftungen
    "Datei im Projektordner": "File in the project folder",
    "Funktion aus mariposa": "Function from mariposa",
    "Objekt in R": "Object in R",
    "Eine Reihe ist ein Fall:": "A row is a case:",
    "Ein Turm ist eine Variable:": "A tower is a variable:",
    "Ein leerer Stein ist ein fehlender Wert.": "An empty brick is a missing value.",
    "Vektor": "Vector",
    "Zahl": "Number",
    "Wertelabel": "Value label",
    "Faktor": "Factor",
    "Zahl ohne Label": "Number without label",
    "Variablenname": "Variable name",
    "Variablenlabel": "Variable label",
    "Wertelabels": "Value labels",
    "SPLIT-DESIGN": "SPLIT DESIGN",
    "zwei Drittel: Fragen gestellt": "two thirds: questions asked",
    "knapp ein Drittel: TNZ: SPLIT": "just under a third: NAP: SPLIT",
    "GÜLTIG": "VALID",
    "FEHLEND": "MISSING",
    "   18 + 26 = 44 gültige Werte weniger": "   18 + 26 = 44 fewer valid values",
    "eine Lücke": "one gap",
    # Kap. 4: Labels aus ZA8833
    "MANN": "MALE",
    "FRAU": "FEMALE",
    '"ISLAMAUSUEBUNG IN DEUTSCHL. BESCHRAENKEN"': '"EXERCISE OF MUSLIM FAITH SHLD BE LIMITED"',
    "STIMME GAR NICHT ZU": "COMPLETELY DISAGREE",
    "STIMME VOLL+GANZ ZU": "COMPLETELY AGREE",
    "DATENFEHLER: MFN": "DATA ERROR: MR",
    "TNZ: SPLIT": "NAP: SPLIT",
    "KEINE ANGABE": "NO ANSWER",
    "WEISS NICHT": "DO NOT KNOW",
    "NA(a)": "NA(g)",
    "NA(b)": "NA(l)",
    "NA(c)": "NA(n)",
    "NA(d)": "NA(o)",
    "ANDERER ABSCHLUSS": "OTHER SCHOOL CERTIF.",
    "NOCH SCHUELER": "STILL AT SCHOOL",
    # Kap. 1: Abbildungen (RStudio-Wörter wie Console, Environment, Files bleiben)
    "Datenmanipulation und Visualisierung": "data manipulation and visualisation",
    "statistische Analyse": "statistical analysis",
    "Funktion": "Function",
    "Paket": "Package",
    "Ökosystem": "Ecosystem",
    "REGAL: INSTALLIERT": "SHELF: INSTALLED",
    "WERKBANK: AKTIV": "WORKBENCH: ACTIVE",
    "einmal pro Rechner": "once per computer",
    "einmal pro R-Sitzung": "once per R session",
    "RECHNER VON ANNA": "ANNA\u2019S COMPUTER",
    "RECHNER VON BORIS": "BORIS\u2019S COMPUTER",
    "gefunden": "found",
    "nicht gefunden": "not found",
    "01-erste_schritte.qmd": "01-first_steps.qmd",
    "Funktionsbeschreibung": "function description",
    "Default-Werte": "default values",
    "Argumente": "arguments",
    "Beispiele": "examples",
    "Code schreiben und speichern": "Write and save code",
    "Code ausprobieren, Output ansehen": "Try out code, view output",
    "Objekte und Befehlsverlauf": "Objects and command history",
    "Dateien, Grafiken, Pakete, Hilfe": "Files, plots, packages, help",
    # Kap. 2: Abbildungen
    "Mein erster Bericht": "My first report",
    "Einleitung": "Introduction",
    "In diesem Bericht analysiere ich den ALLBUS 2023.": "In this report I analyse the ALLBUS 2023.",
    "YAML-Header": "YAML header",
    "Markdown-Lauftext": "Markdown text",
    "Code-Chunk": "Code chunk",
    "OPTION": "OPTION",
    "IM BERICHT": "IN THE REPORT",
    "AUSGEFÜHRT": "EXECUTED",
    "ohne Option": "no option",
    "ja": "yes",
    "nein": "no",
    "NEUE R-SITZUNG": "NEW R SESSION",
    "NACH DEM SETUP-CHUNK": "AFTER THE SETUP CHUNK",
    "WERKBANK": "WORKBENCH",
    "nur base R": "base R only",
    "leer": "empty",
    "analyse.qmd": "analysis.qmd",
    "literatur.bib": "references.bib",
    "Wie @Goodman2016 zeigt, lässt sich Reproduzierbarkeit unterschiedlich definieren.":
        "As @Goodman2016 show, reproducibility can be defined in different ways.",
    "Für eine ausführliche Behandlung siehe auch [@Wickham2023].":
        "For a detailed discussion, see also [@Wickham2023].",
    "Wie Goodman, Fanelli, und Ioannidis (2016) zeigt, lässt sich Reproduzierbarkeit unterschiedlich "
    "definieren. Für eine ausführliche Behandlung siehe auch (Wickham, Çetinkaya-Rundel, und Grolemund 2023).":
        "As Goodman, Fanelli, and Ioannidis (2016) show, reproducibility can be defined in different ways. "
        "For a detailed discussion, see also (Wickham, Çetinkaya-Rundel, and Grolemund 2023).",
    "Literatur": "References",
    "Goodman, Steven N., Daniele Fanelli, und John P. A. Ioannidis. 2016. „What does research "
    "reproducibility mean?“ ":
        "Goodman, Steven N., Daniele Fanelli, and John P. A. Ioannidis. 2016. \u201cWhat does research "
        "reproducibility mean?\u201d ",
    "Wickham, Hadley, Mine Çetinkaya-Rundel, und Garrett Grolemund. 2023.":
        "Wickham, Hadley, Mine Çetinkaya-Rundel, and Garrett Grolemund. 2023.",
    ". 2. Aufl. O’Reilly.": ". 2nd ed. O\u2019Reilly.",
    # Titelbild
    "Sozialwissenschaften": "Social Sciences",
    "Einführung in die statistische Datenanalyse mit tidyverse und mariposa":
        "An introduction to statistical data analysis with tidyverse and mariposa",
}
