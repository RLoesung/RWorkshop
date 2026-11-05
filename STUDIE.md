# Mini-Studie — Roter Faden durch den RWorkshop

**Datensatz.** ALLBUS 2023 (`ALLBUS2023.sav`, N = 5246, 579 Variablen), GESIS-Studiennummer ZA8901.

**Skala.** Sechs Items zur Einstellung gegenüber Muslimen / dem Islam in Deutschland. In der deutschsprachigen Forschung etabliert unter dem Begriff **Muslimfeindlichkeit / Islamfeindlichkeit** (vgl. Decker & Brähler; Pickel/Pickel). Wir verwenden im Lehrbuch durchgängig den Skalennamen `islamophobie` aus pragmatischen Gründen (kurz, international anschlussfähig).

**Stand.** Kapitelnummern und Befunde beziehen sich auf die 9-Kapitel-Fassung, gerendert mit mariposa 0.7.4 (November 2026).

---

## 1 — Forschungsfrage

> *Wer trägt islamfeindliche Einstellungen in Deutschland 2023, und wie hängen sie mit politischen Orientierungen und Soziostruktur zusammen?*

Diese Frage trägt sich durch den gesamten Daten- und Methodenteil (Kap. 4–9) und ist der inhaltliche rote Faden, an dem jede Methode mindestens einmal demonstriert wird.

---

## 2 — Variablen-Inventar

### 2.1 Skalen-Items (latente AV)

Alle sechs Items 7-stufig (1 = „stimme gar nicht zu" … 7 = „stimme voll und ganz zu"); Missing-Codes -42, -11, -9, -8. Die Skala ist Teil eines **Split-Moduls** (TNZ-Code -11 für die andere Stichprobenhälfte), gültige N pro Item ≈ 3300–3450.

| Variable | Wortlaut (Kurzform) | Polung |
|---|---|---|
| `mm01` | Islamausübung in Deutschland beschränken | hoch = islamfeindlich |
| `mm02` → `mm02r` | Islam passt in die deutsche Gesellschaft | **umpolen** |
| `mm03` | Anwesenheit von Muslimen bringt Konflikt | hoch = islamfeindlich |
| `mm04` | Staat sollte islamische Gruppen beobachten | hoch = islamfeindlich |
| `mm05` → `mm05r` | Muslimischer Bürgermeister in Ordnung | **umpolen** |
| `mm06` | Unter Muslimen sind viele rel. Fanatiker | hoch = islamfeindlich |

**Gebildete Skala:** `islamophobie` = Mittelwert aus `mm01, mm02r, mm03, mm04, mm05r, mm06` mit `min_valid = 5` (5 von 6 Items müssen valide sein).

### 2.2 Korrelate / weitere AV

| Variable | Bedeutung | Verwendung |
|---|---|---|
| `pa29`–`pa35` | Populismus-Items (Schulz et al. 2017), 5-stufig **invers** → `pa29r`–`pa35r` | Skala `populismus` (`min_valid = 6`), zentraler Prädiktor in Kap. 7–9 |
| `ps03` | Zufriedenheit mit der Demokratie in Deutschland (1 = sehr zufrieden … 6 = sehr unzufrieden) | Übungen Kap. 7 und 9 |
| `ls01` | Allgemeine Lebenszufriedenheit (0–10) | Übung Kap. 7 |
| `st01` | Vertrauen in Mitmenschen | Übung Kap. 7 |

Reserve, derzeit nicht im Buch verwendet: `pt03`, `pt15` (Vertrauen Bundestag / Parteien), `agec` (Alter kategorial), `incc` (Nettoeinkommen kategorial).

### 2.3 Unabhängige Variablen (Soziostruktur)

| Variable | Rolle |
|---|---|
| `eastwest` | Erhebungsgebiet West (1) / Ost (2) |
| `sex` | Geschlecht (1 Mann, 2 Frau, 3 Divers, -9 KA, -42 Datenfehler) |
| `age` | Alter metrisch |
| `educ` | Allgemeiner Schulabschluss (1–7; 6 = anderer Abschluss, 7 = noch Schüler:in) — primäre Bildungsvariable |
| `educ_kat` | aus `educ` abgeleitet: 1–2 = niedrig, 3 = mittel, 4–5 = hoch, sonst NA (Setup-Chunks von Kap. 6, 7 und 9) |
| `isced97` | ISCED 1997 — Alternative für internationale Vergleichbarkeit (Kap. 5, Kontrollvariable in Kap. 7) |

### 2.4 Gewicht

| Variable | Zweck |
|---|---|
| `wghtpew` | Personenbezogenes Ost-West-Gewicht (Standardanwendung in allen Analysen) |

---

## 3 — Datenpräp-Pipeline (Kap. 5)

Die verbindliche Fassung steht in **`R/prep.R`**. Kap. 5 baut sie Schritt für Schritt auf (der Abschnitt „Die komplette Datenpräp-Pipeline" zeigt sie am Stück); Kap. 6–9 laden sie im Setup-Chunk per `source("R/prep.R")`, damit jedes Kapitel allein rendert. Änderungen an der Pipeline immer in Kap. 5 **und** in `R/prep.R` nachziehen.

Die Schritte:

1. `read_spss("ALLBUS2023.sav")` — fehlende Werte werden als *tagged NAs* gelesen.
2. `mm02` und `mm05` mit `rec(rules = "rev", suffix = "r")` umpolen.
3. Alle sieben `pa`-Items umpolen (5-stufig invers: `1 = stimme zu` → `5 = lehne ab`).
4. Skalen bilden: `islamophobie` (6 Items, `min_valid = 5`) und `populismus` (7 Items, `min_valid = 6`) mit `row_means()`.
5. POMPS-Versionen `islamophobie_p` und `populismus_p` (0–100) mit `pomps()`.

**Polungs-Hinweis.** Die `mm`-Items sind 7-stufig (`1 = lehne ab` → `7 = stimme zu`); die `pa`-Items sind 5-stufig und **invers**. Beide Skalen werden so umgepolt, dass am Ende einheitlich hoch = mehr von der gemessenen Einstellung gilt. Seit mariposa 0.7.4 nimmt `rules = "rev"` die Skalengrenzen aus den Wertelabels — Kap. 5 zeigt den Kontroll-Chunk `count(mm02, mm02r)`.

**Kapitelspezifische Ergänzungen** (nicht in `R/prep.R`): `educ_kat` in Kap. 6, 7 und 9; der Dummy `islam_hoch = as.integer(islamophobie >= 4)` (Skalenmitte) für die logistische Regression in Kap. 9.

---

## 4 — Methoden-Mapping pro Kapitel

### Kap. 4 — Datenimport und Inspektion
- `read_spss("ALLBUS2023.sav")`, Daten ansehen, Variablen finden mit `find_var()`, `codebook()`.
- `select()`, `filter()`, `arrange()`; Datentypen und labelled-Vektoren.
- Variablen- und Wertelabels lesen und setzen (`var_label()`, `val_labels()`).
- **Split-Design** anhand der `mm`-Items erklären (TNZ-Code -11); fehlende Werte mit `set_na()` deklarieren, `na_frequencies()`.

### Kap. 5 — Daten transformieren und Skalen bilden
- `mutate()`, `case_when()`, `recode_values()`, `group_by()`/`summarise()`, Joins, `pivot_*()`.
- **Rekodierung** mit `rec()` (Bildung kategorisieren, Dichotomisieren, Quartile), Dummies mit `to_dummy()`, Standardisieren.
- **Reverse Coding** als zentrales Lehrstück; Skalen `islamophobie` und `populismus` mit `row_means()`, Antwortstil mit `row_count()`, Vergleichbarkeit mit `pomps()`.
- Die komplette Pipeline (Abschnitt 3).

### Kap. 6 — Visualisierung Grundlagen
- Grammar of Graphics; Geoms für kategoriale und kontinuierliche Variablen.
- Facets (Ost/West, Bildung), Farben und `theme_rworkshop()`, Beschriftungen, Ausblick auf `patchwork`.

### Kap. 7 — Uni- und bivariate Analyse
- Gewichtung; Inferenz-Grundlagen (p-Wert, Standardfehler, Konfidenzintervall, Effektgröße).
- `frequency()`, `describe()`, `w_*()`-Kennwerte, `binomial_test()`, `chisq_gof()`.
- `crosstab()` (inkl. Residuen) und `chi_square()` für Bildung × Region.
- `pearson_cor()` (Islamfeindlichkeit ↔ Populismus, Item-Matrix), `partial_cor()`, `normality_test()`.
- `t_test()` Ost vs. West, `oneway_anova()` nach Bildung mit Tukey-Post-Hoc, nicht-parametrische Alternativen.

### Kap. 8 — Latente Strukturen
- Inter-Item-Korrelationen, KMO (inkl. MSA pro Item) und Bartlett.
- Anzahl der Faktoren (Eigenwerte, Scree-Plot); **EFA** mit `efa()` als Einfaktor- und Zwei-Faktor-Lösung mit Rotation.
- **Reliabilität** mit `reliability()` (Cronbachs α, McDonalds ω, Item-Statistiken, α-if-deleted).
- **CFA-Ausblick** mit `lavaan::cfa()` und `semPlot::semPaths()`.

### Kap. 9 — Erklärungsmodelle
- Einfache und multiple lineare Regression mit `linear_regression()`, Dummy-Codierung, Modellvergleich.
- VIF händisch und aus `summary()`, Residuen-Diagnostik händisch.
- `factorial_anova()` (Bildung × Region), `ancova()` mit Randmitteln.
- `logistic_regression()` für `islam_hoch`, Odds Ratios und `marginal_effects()`.
- Coefficient-Plot und Komposition mit `patchwork`.

---

## 5 — Erwartungen und Befunde

Die Erwartungen wurden vor der Auswertung als didaktischer Spannungsbogen formuliert. Die Befunde stammen aus den gerenderten Kapiteln (mariposa 0.7.4, gewichtet mit `wghtpew`).

| Erwartung | Befund | Kapitel |
|---|---|---|
| **Bildung** ist ein robuster Prädiktor (negativ). | Bestätigt, vor allem für *hohe* Bildung: Gruppenmittel 4.68 / 4.45 / 3.48 (niedrig / mittel / hoch), η² = .125. Nach Kontrolle des Alters verschwindet der Abstand niedrig–mittel; hohe Bildung senkt die Wahrscheinlichkeit hoher Islamfeindlichkeit um rund 25 Prozentpunkte (AME). | 7, 9 |
| **Ost/West** zeigt moderate Unterschiede (Ost höher). | Bestätigt: West 3.90, Ost 4.55 (Hedges' g ≈ −0.43); der Unterschied bleibt im multiplen Modell bestehen. Die Interaktion Bildung × Region ist **nicht** signifikant (p = .19) — der Bildungseffekt ist in Ost und West ähnlich. | 7, 9 |
| **Alter** korreliert positiv. | Bestätigt, aber klein: OR = 1.028 pro Lebensjahr in der logistischen Regression. | 9 |
| **Politische Variablen** sind die stärksten Korrelate: Populismus positiv, Demokratiezufriedenheit negativ. | Bestätigt: r(Islamfeindlichkeit, Populismus) = .40, partiell (Alter, Bildung kontrolliert) .37; Populismus ist mit Beta ≈ 0.32 der stärkste Prädiktor, das Gesamtmodell erklärt R² = .30. Demokratie-Unzufriedenheit (`ps03`, hoch = unzufrieden) korreliert mit r = .33. | 7, 9 |
| **EFA** ergibt eine sparsame Einfaktor-Lösung; eine Zwei-Faktor-Lösung trennt „kognitiv-stereotyp" von „politisch-restriktiv". | Einfaktor-Lösung bestätigt (54.7 % erklärte Varianz). Die Zwei-Faktor-Lösung trennt aber die beiden umgepolten Items (`mm02r`, `mm05r`) ab — ein **Methodenfaktor**, keine inhaltliche Dimension. | 8 |
| **Reliabilität**: Cronbachs α ≈ .85–.90. | Knapp darunter: α = .83, ω = .84 — gut reliabel. | 8 |

---

## 6 — Was die Wahl bewusst ausschließt

- **CFA als Hauptmethode**: als Ausblick in Kap. 8, nicht als zentrale Übung. Lavaan-Code als sauberes, gekapseltes Beispiel (`lavaan::`-Präfix, weil `library(lavaan)` mariposas `efa()` überdeckt); keine SEM-Pfadmodelle.
- **Längsschnittvergleich** mit früheren ALLBUS-Wellen: zu komplex für ein Einsteigerbuch, wäre eine Erweiterungsidee für eine spätere Auflage.
- **Item-Response-Theorie**: Die Skala bleibt klassisch über Faktorenanalyse + Reliabilität; IRT wäre Overkill.
- **Anderer Datensatz** für einzelne Beispiele: erlaubt (z. B. ein kleiner Demo-Datensatz für einen sehr einfachen Einstieg), aber jede Methode wird **mindestens einmal** an der ALLBUS-Islamfeindlichkeits-Pipeline demonstriert.

---

## 7 — Verifikations-Pflichten

Wenn ein Pass ein Kapitel anfasst, gilt:

- [ ] Die Datenpräp-Pipeline (`R/prep.R`) läuft fehlerfrei im Setup-Chunk.
- [ ] Mindestens eine Methode des Kapitels ist an der `islamophobie`-Skala demonstriert.
- [ ] Die Befunde aus Abschnitt 5 werden im Kapitel angesprochen oder abweichend kommentiert.
- [ ] Die Forschungsfrage aus Abschnitt 1 ist im Kapitelfließtext sichtbar — nicht nur im Setup.

Nach einem **mariposa-Update** zusätzlich: jedes Kapitel mit `error = TRUE` knitten, auch die `eval=FALSE`-Lösungschunks einmal erzwungen ausführen, und jede Zahl in den Lesart-Texten gegen die echte Ausgabe prüfen. Die Lesarten zitieren viele konkrete Werte; kompakter Print und `summary()` zeigen unterschiedlich viel.
