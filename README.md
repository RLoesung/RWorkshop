# R Workshop – Sozialwissenschaften

**Einführung in die statistische Datenanalyse mit tidyverse und mariposa**

📖 **Online lesen:** <https://rloesung.github.io/RWorkshop/>

Ein frei verfügbares, deutschsprachiges Lehrbuch für Studierende der Sozialwissenschaften, die R neu kennenlernen, oft mit Vorerfahrung in SPSS. Das Buch führt vom ersten Datenimport über deskriptive und inferenzstatistische Verfahren bis zu Faktorenanalyse und Regression. Der Werkzeugkasten ist bewusst klein gehalten: das [tidyverse](https://www.tidyverse.org/) für Datenmanipulation und Grafiken, [mariposa](https://yannickdiehl.github.io/mariposa/) für die statistische Analyse mit SPSS-artigen Ausgaben und [Quarto](https://quarto.org/) für reproduzierbare Berichte.

Durch alle Kapitel zieht sich eine Mini-Studie mit dem **ALLBUS 2023**:

> *Wer trägt islamfeindliche Einstellungen in Deutschland 2023, und wie hängen sie mit politischen Orientierungen und Soziostruktur zusammen?*

## Inhalt

| Kap. | Thema | Schwerpunkte |
|---:|---|---|
| 0 | Vorwort | Ziele, Voraussetzungen, Datensatz, Aufbau der Kapitel |
| 1 | RStudio | Installation, Oberfläche, Projekte, Pakete, Hilfe finden |
| 2 | Quarto und reproduzierbare Wissenschaft | Markdown, YAML, Code-Chunks, Literaturverweise, Publizieren als HTML/PDF/Word |
| 3 | Programmiersprache R | Variablen, Funktionen, Operatoren, Datentypen, `NA`, die Pipe `\|>` |
| 4 | Datenimport und Inspektion | `read_spss()`, `find_var()`, `codebook()`, Labels, fehlende Werte |
| 5 | Daten transformieren und Skalen bilden | dplyr-Verben, `rec()`, Umpolen, `row_means()`, `pomps()` |
| 6 | Visualisierung — Grundlagen | Grammar of Graphics mit ggplot2, Facets, Themes |
| 7 | Uni- und bivariate Analyse | Gewichtung, Inferenz, Kreuztabellen, Korrelation, t-Test, ANOVA |
| 8 | Latente Strukturen | KMO, EFA, Cronbachs α und McDonalds ω, CFA-Ausblick |
| 9 | Erklärungsmodelle | lineare und logistische Regression, VIF, Residuen, ANCOVA, AME |

Jedes Kapitel folgt dem Dreischritt **Frage → Code → Lesart** und endet mit Übungen (Lösungen zum Aufklappen) und einer Mini-Forschungsfrage.

## Buch lokal rendern

**Voraussetzungen**

- R ≥ 4.3 (empfohlen ≥ 4.5) und Quarto. Quarto ist in aktuellen RStudio-Versionen enthalten; gerendert wird derzeit mit Quarto 1.8.
- Die R-Pakete, alle von CRAN:

  ```r
  install.packages(c("tidyverse", "mariposa", "patchwork", "lavaan", "semPlot"))
  ```

  Das Buch ist auf **mariposa ≥ 0.7.4** abgestimmt. Ältere Versionen liefern an einigen Stellen andere Ausgaben oder brechen ab.
- Der Datensatz **ALLBUS 2023** als `ALLBUS2023.sav` im Projektordner. Bezug über den [GESIS-Datenbestandskatalog, Studiennummer ZA8901](https://search.gesis.org/research_data/ZA8901). Dafür brauchst du einen kostenlosen GESIS-Account.

**Rendern**

```bash
quarto render                               # ganzes Buch nach docs/
quarto render 07-Uni-Bivariate-Analyse.qmd  # nur ein Kapitel
```

Das Projekt nutzt `freeze: auto`: Beim Render des ganzen Buchs werden nur Kapitel neu gerechnet, deren Quelltext sich geändert hat. Alle anderen Kapitel kommen aus `_freeze/`. Wenn du ein einzelnes Kapitel gezielt renderst, wird es immer neu ausgeführt. Das ist der Weg nach einem Paket-Update.

Die Online-Fassung liefert GitHub Pages direkt aus `docs/` auf `main` aus. Nach dem Rendern werden deshalb `docs/` und `_freeze/` mit committet.

## Projektstruktur

```
├── index.qmd                 Vorwort (Kap. 0)
├── 01-RStudio.qmd … 09-Erklaerungsmodelle.qmd   Kapitel
├── R/
│   ├── _common.R             gemeinsames ggplot-Theme (theme_rworkshop)
│   └── prep.R                Datenpräp-Pipeline der Mini-Studie (Kap. 5)
├── Bilder/                   Screenshots für Kap. 1
├── _quarto.yml               Buch-Konfiguration
├── theme.scss                Theme-Anpassungen (auf Basis von cosmo)
├── _freeze/                  eingefrorene Rechenergebnisse (versioniert)
├── docs/                     gerendertes Buch für GitHub Pages (versioniert)
├── STYLE.md                  Stil- und Didaktik-Leitfaden
├── MIGRATION.md              Code-Konventionen und Funktions-Mapping (tidyverse + mariposa)
├── STUDIE.md                 Mini-Studie: Variablen, Pipeline, Methoden-Mapping, Befunde
└── NEWS.md                   Änderungsprotokoll
```

## Mitmachen

Fehler gefunden, etwas unklar, Idee für eine Übung? Über ein [Issue](https://github.com/RLoesung/RWorkshop/issues) oder einen Pull Request. Jede Kapitelseite hat rechts die Links „Seite editieren" und „Problem melden".

- Für Text- und Code-Korrekturen reicht eine Änderung an der jeweiligen `.qmd`-Datei. `docs/` und `_freeze/` musst du nicht mitliefern.
- Sprache, Kapitelaufbau und Callout-Typen regelt [`STYLE.md`](STYLE.md), die Code-Konventionen regelt [`MIGRATION.md`](MIGRATION.md).
- Viele Lesart-Texte zitieren konkrete Zahlen aus den Ausgaben. Wer Code ändert, prüft bitte, ob die Zahlen im Text noch stimmen.
- Probleme mit mariposa selbst gehören in den [mariposa-Issue-Tracker](https://github.com/YannickDiehl/mariposa/issues).

## Autor:innen

Yannick Diehl und Daniel Moosdorf, mit Beiträgen von Jakob Krüger.

Was sich wann geändert hat, steht in [`NEWS.md`](NEWS.md).
