# Mini-Studie — Roter Faden durch den RWorkshop

**Datensatz.** ALLBUS 2023 (`ALLBUS2023.sav`, N = 5246, 579 Variablen). Vertriebsstand GESIS.

**Skala.** Sechs Items zur Einstellung gegenüber Muslimen / dem Islam in Deutschland. In der deutschsprachigen Forschung etabliert unter dem Begriff **Muslimfeindlichkeit / Islamfeindlichkeit** (vgl. Decker & Brähler; Pickel/Pickel). Wir verwenden im Lehrbuch durchgängig den Skalennamen `islamophobie` aus pragmatischen Gründen (kurz, international anschlussfähig).

---

## 1 — Forschungsfrage

> *Wer trägt islamfeindliche Einstellungen in Deutschland 2023, und wie hängen sie mit politischen Orientierungen und Soziostruktur zusammen?*

Diese Frage trägt sich durch alle Methoden-Kapitel (3–6) und ist gleichzeitig der inhaltliche Roter Faden, an dem jede Methode mindestens einmal demonstriert wird.

---

## 2 — Variablen-Inventar

### 2.1 Skalen-Items (latente AV)

Alle sechs Items 7-stufig (1 = „stimme gar nicht zu" … 7 = „stimme voll und ganz zu"); Missing-Codes -42, -11, -9, -8. Skala ist Teil eines **Split-Moduls** (TNZ-Code -11 für die andere Stichprobenhälfte), gültige N pro Item ≈ 3300–3440.

| Variable | Wortlaut (Kurzform) | Polung |
|---|---|---|
| `mm01` | Islamausübung in Deutschland beschränken | hoch = islamophob |
| `mm02` → `mm02r` | Islam passt in die deutsche Gesellschaft | **umpolen** |
| `mm03` | Anwesenheit von Muslimen bringt Konflikt | hoch = islamophob |
| `mm04` | Staat sollte islamische Gruppen beobachten | hoch = islamophob |
| `mm05` → `mm05r` | Muslimischer Bürgermeister in Ordnung | **umpolen** |
| `mm06` | Unter Muslimen sind viele rel. Fanatiker | hoch = islamophob |

**Gebildete Skala:** `islamophobie` = `row_means(mm01, mm02r, mm03, mm04, mm05r, mm06, min_valid = 5)` (5 von 6 Items müssen valide sein).

### 2.2 Korrelate / weitere AV

| Variable | Bedeutung |
|---|---|
| `ls01` | Allgemeine Lebenszufriedenheit (0–10) |
| `st01` | Vertrauen in Mitmenschen |
| `ps03` | Zufriedenheit mit Demokratie in Deutschland |
| `pa29`–`pa35` | Populismus-Items (Schulz et al. 2017), als Skala `populismus` aggregierbar |
| `pt03`, `pt15` | Vertrauen Bundestag / Parteien (Einzel-Indikatoren politisches Vertrauen) |

### 2.3 Unabhängige Variablen (Soziostruktur)

| Variable | Rolle |
|---|---|
| `eastwest` | Erhebungsgebiet West (1) / Ost (2) |
| `sex` | Geschlecht (1 Mann, 2 Frau, 3 Divers, -9 KA, -42 Datenfehler) |
| `age` | Alter metrisch |
| `agec` | Alter kategorial (Reserve, falls Klassen gewünscht) |
| `educ` | Allgemeiner Schulabschluss (1–7) — primäre Bildungsvariable |
| `isced97` | ISCED 1997 — Alternative für internationale Vergleichbarkeit |
| `incc` | Nettoeinkommen kategorial (Reserve) |

### 2.4 Gewicht

| Variable | Zweck |
|---|---|
| `wghtpew` | Personenbezogenes Ost-West-Gewicht (Standardanwendung) |

---

## 3 — Datenpräp-Pipeline (Kap. 3)

Das, was in Kap. 3 verbindlich erzeugt wird und in Kap. 4–6 als Voraussetzung gilt:

```r
library(tidyverse)
library(mariposa)

allbus <- read_spss("ALLBUS2023.sav")

allbus <- allbus |>
  # Fehlende Werte deklarieren (Datenfehler, TNZ, KA, weiss-nicht)
  set_na(mm01, mm02, mm03, mm04, mm05, mm06,
         ls01, st01, ps03,
         pa29, pa30, pa31, pa32, pa33, pa34, pa35,
         pt03, pt15,
         sex, age, educ, isced97, incc,
         tag = TRUE) |>
  # Umpolen der inversen Items
  rec(mm02, rules = "1=7; 2=6; 3=5; 4=4; 5=3; 6=2; 7=1", suffix = "r") |>
  rec(mm05, rules = "1=7; 2=6; 3=5; 4=4; 5=3; 6=2; 7=1", suffix = "r") |>
  # Islamophobie-Skala
  row_means(mm01, mm02r, mm03, mm04, mm05r, mm06,
            min_valid = 5) |>
  # Populismus-Skala (alle in derselben Richtung)
  row_means(pa29, pa30, pa31, pa32, pa33, pa34, pa35,
            min_valid = 6)
```

**Lehrbuch-Klammer.** Diese Pipeline wird in Kap. 3 schrittweise aufgebaut, mit Halt für Erklärungen nach jedem Schritt (Frage → Code → Lesart). In Kap. 4–6 wird sie am Kapitelanfang in einem versteckten Setup-Chunk erneut ausgeführt, damit jedes Kapitel reproduzierbar bleibt.

---

## 4 — Methoden-Mapping pro Kapitel

### Kap. 3 — Datenmodifikation
- `read_spss("ALLBUS2023.sav")`, Daten ansehen.
- **Split-Designs erklären** anhand `mm01`-Items (TNZ-Code -11 als Brücke zur Stichprobenarchitektur).
- Fehlende Werte mit `set_na()` deklarieren.
- `eastwest`, `sex`, `educ` als Faktor (`to_label()`).
- **Reverse Coding** mit `rec()` — zentrales Lehrbeispiel für Skalenbildung.
- Skala `islamophobie` mit `row_means()`.
- Populismus-Skala als zweite Übung mit gleichem Muster (alle Items in derselben Richtung — Kontrast zu mm).
- Codebook-Auszug mit `codebook(allbus, mm01:mm06)` als Abrundung.

### Kap. 4 — Uni- und Bivariate Datenanalyse
- Häufigkeiten einzelner Items: `frequency(allbus, mm03, weights = wghtpew)`.
- Deskriptive Statistik der Skala: `describe(allbus, islamophobie, weights = wghtpew)`.
- Kreuztabelle Bildungsstufen × Skalenterzile (Skala vorher in 3 Klassen geschnitten): `crosstab(...)` + χ² mit `chi_square()`.
- `t_test(allbus, islamophobie, group = eastwest, weights = wghtpew)` — klassischer Mittelwertvergleich Ost vs. West.
- Pearson-Korrelation Islamophobie ↔ Populismus, Islamophobie ↔ `ls01`, Islamophobie ↔ `ps03` — auch das mit `pearson_cor()`.

### Kap. 5 — Multivariate Datenanalyse
- Korrelationsmatrix der 6 Items: `pearson_cor(allbus, mm01, mm02r, mm03, mm04, mm05r, mm06)`.
- **EFA** mit `efa()`. Diskussion: 1-Faktor-Lösung (globale Islamfeindlichkeit) vs. 2-Faktor-Lösung (kognitiv-stereotyp vs. politisch-restriktiv). KMO + Bartlett aus dem `efa()`-Output ablesen.
- **Cronbachs α** mit `reliability(mm01, mm02r, mm03, mm04, mm05r, mm06)` — Erwartung α ≈ .85–.90.
- Multiple Regression `linear_regression(islamophobie ~ educ + age + eastwest + sex + populismus + ls01, weights = wghtpew)`.
- Logistische Regression: Dummy „hohe Islamophobie" (Skalenwert ≥ Median) ~ Soziostruktur mit `logistic_regression()`.
- **CFA-Ausblick** mit `lavaan::cfa()` — kurzer Restbedarf-Abschnitt, der zeigt, dass mariposa hier bewusst abgibt und das Lehrbuch nicht alles im Eigenpaket erzwingen will.

### Kap. 6 — Grafiken
- **Likert-Plot** der 6 Items (divergierende Farbskala, gewichtet) als zentrale Grafik.
- Histogramm / Boxplot der Skala nach Bildungsgruppen.
- Streudiagramm Islamophobie × Populismus mit Regressionsgerade nach Ost/West (facettiert).
- Koeffizienten-Plot der multiplen Regression aus Kap. 5.
- Multi-Plot-Komposition mit `patchwork`.

---

## 5 — Erwartete Befunde als didaktischer Spannungsbogen

Damit das Lehrbuch nicht in „wir rechnen jetzt mal" verfällt, formulieren wir am Kapitelanfang explizite Hypothesen und prüfen am Kapitelende:

- **Bildung** ist der robusteste Prädiktor (negativ): höher gebildete Befragte zeigen geringere Werte.
- **Ost/West** liefert moderate Unterschiede (Ost tendenziell höher).
- **Alter** korreliert positiv (ältere Kohorten höher).
- **Politische Variablen** sind die stärksten Korrelate: Populismus positiv, Demokratiezufriedenheit negativ.
- **EFA** ergibt 1-Faktor-Lösung als sparsame, vertretbare Lösung; 2-Faktor-Lösung ist methodisch verteidigbar, in einem Lehrbuch aber overkill (didaktischer Punkt: Sparsamkeit vor maximaler Erklärungskraft).

Diese Erwartungen sind Lehrmaterial — keine vorab-Prüfung gegen das Datenmaterial. Wenn die Auswertung in der Migration anders ausfällt, wird der Text entsprechend angepasst.

---

## 6 — Was die Wahl bewusst ausschließt

- **CFA als Hauptmethode**: Erwähnt als Ausblick in Kap. 5, nicht als zentrale Übung. Lavaan-Code als sauberes, gekapseltes Beispiel; keine SEM-Pfadmodelle.
- **Längsschnittvergleich** mit früheren ALLBUS-Wellen: zu komplex für ein Einsteigerbuch, wäre eine Erweiterungsidee für eine spätere Auflage.
- **Itemresponse-Theorie**: Skala bleibt klassisch über Faktorenanalyse + Cronbach; IRT wäre Overkill.
- **Anderer Datensatz** für einzelne Beispiele: erlaubt (z. B. ein eingebauter Tidyverse-Datensatz für einen sehr einfachen Einstieg), aber jede Methode wird **mindestens einmal** an der ALLBUS-Islamophobie-Pipeline demonstriert.

---

## 7 — Verifikations-Pflichten beim Migrieren

Wenn ein Migrations-Pass ein Kapitel anfasst, gilt:

- [ ] Datenpräp-Pipeline aus Abschnitt 3 läuft fehlerfrei am Kapitelanfang (Setup-Chunk).
- [ ] Mindestens eine Methode des Kapitels ist an der `islamophobie`-Skala demonstriert.
- [ ] Ergebnisse aus „Erwartete Befunde" (Abschnitt 5) werden im Kapitel angesprochen oder mit Hinweis abweichend kommentiert.
- [ ] Forschungsfrage aus Abschnitt 1 wird im Kapitelfließtext sichtbar — nicht nur im Setup.
