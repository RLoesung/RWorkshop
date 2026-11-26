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
    # Titelbild
    "Sozialwissenschaften": "Social Sciences",
    "Einführung in die statistische Datenanalyse mit tidyverse und mariposa":
        "An introduction to statistical data analysis with tidyverse and mariposa",
}
