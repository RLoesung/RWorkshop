# Bausteine-Abbildungen — Entwurf und Vertrag

**Zweck.** Dieses Dokument regelt, wie die Erklärgrafiken aus dem Workshop „Reading Week“ (Tag 1 „R-Einstieg“, Tag 2 „Daten und Analyse“, November 2026) ins Buch kommen. Es ist zugleich der Vertrag für alle späteren Abbildungen in dieser Bildsprache, so wie `STYLE.md` den Text und `MIGRATION.md` den Code regelt.

---

## 1 — Worum es geht

Für den Workshop ist eine Bildsprache entstanden, mit der sich Grundbegriffe von R anschaulich erklären lassen: Ein Wert ist ein Baustein, seine Farbe ist der Datentyp, ein Vektor ist ein Turm, ein Datensatz eine Bauplatte mit Türmen, ein Label ein Aufkleber, ein fehlender Wert ein leerer Stein. Dazu kommen Code-Farben (Objekte dunkel, Funktionen grün, Argumente orange) und Ablaufbilder, etwa wie die Pipe das Ergebnis ins erste Feld der nächsten Funktion setzt.

Im Buch werden genau diese Begriffe bisher nur mit Text und Code erklärt: Kap. 3 und 4 haben keine einzige Abbildung, Kap. 5 nur ein Diagramm. Die Grafiken aus dem Workshop sollen dort hin, wo das Buch dasselbe Konzept erklärt. Warum: Im Workshop haben sie beim Verstehen geholfen, in ihnen steckt viel Arbeit, und wer den Workshop besucht hat, findet im Buch dieselbe Bildsprache wieder. Die Folien sind dabei Ausgangspunkt, nicht Vorlage: Die Abbildungen folgen den Beispielen des Buchs.

## 2 — Ziele, Nicht-Ziele, was es nicht werden darf

**Ziele**

- Jede Erklärgrafik aus Tag 1 und Tag 2, die ein Konzept des Buchs anschaulicher macht, steht im passenden Abschnitt (Liste in Abschnitt 6).
- Folien und Buch teilen eine Bildsprache: gleiche Farben, gleiche Formen, gleiche Bedeutung.
- Die Bildsprache wird im Buch einmal eingeführt und danach in den Bildunterschriften genutzt.

**Nicht-Ziele**

- Keine Übernahme der Aktivitätsformate (ZURUF, HANDZEICHEN, Daumen hoch), keine Zeitangaben, keine Animationen.
- Keine Anekdoten ohne Lehrwert (etwa die Alltagsereignisse aus der Zeitleiste), siehe `STYLE.md` §10.
- Keine Bausteine-Grafik dort, wo das Buch schon eine bessere Abbildung hat (Inferenz-Simulationen in Kap. 7, alle Kapitel ab Kap. 6, die mit echten ggplot-Grafiken arbeiten).
- Keine Änderung an den Folien.

**Was es nicht werden darf**

- Kein Folienstil im Buch: keine Aufforderungen wie „Ruft rein“, keine Schilder mit Formatnamen, kein Text, der nur im Hörsaal Sinn ergibt.
- Keine Slogans und kein KI-Ton in Bildern und Bildunterschriften (siehe die Überarbeitung der Folien vom 16.11.2026).
- Keine verschobenen Abschnittsnummern: Folien und Lehrmaterial verweisen auf Nummern wie „R-Workshop 4.5.1“.
- Keine Grafik, die R-Verhalten falsch zeigt. Jede Zahl im Bild stimmt mit der Ausgabe von R 4.5 und mariposa 0.7.4 überein.

## 3 — Rahmenbedingungen

- Das Buch ist ein Quarto-Buch (Theme cosmo, nur hell), ausgegeben nach `docs/`, Text in Systemschrift ohne Serifen, Textspalte etwa 800 px breit.
- Die Folien entstehen mit python-pptx und den Helfern aus Methoden Ib (`_build_folien*.py`, außerhalb dieses Repositorys). Ihre Grafiken bestehen aus PowerPoint-Formen mit Klick-Animationen.
- `STYLE.md` §4 verbietet neue Callout-Typen ohne Eintrag dort.
- Abschnittsnummern dürfen sich nicht verschieben. Neue Überschriften nur, wo sie nichts verschieben; Texte zur Bildsprache kommen deshalb in vorhandene Abschnitte oder Callouts.
- Wer am Buch mitarbeitet, ändert normalerweise nur `.qmd`-Dateien (siehe `README.md`).

## 4 — Wege, die wir abgewogen haben

| Weg | Vorteil | Nachteil |
| :-- | :-- | :-- |
| **A: Folien als Bild exportieren** | schnell | Folientext und Ratefragen stecken im Bild, Pixelgrafik, jede Änderung doppelt |
| **B: in R mit ggplot2 neu zeichnen** | passt zur Werkzeugkette des Buchs | jede Grafik neu gebaut, sieht anders aus als auf den Folien |
| **C: Zeichenbefehle der Folien als SVG ausgeben** | nutzt die Folienarbeit direkt, scharfe Vektorgrafik, ein Bildsystem für Folien und Buch | ein kleines Python-Skript im Repository |

**Gewählt: C** (Entscheidung von Yannick, 17.11.2026). Begründung: Dieser Weg nutzt die investierte Arbeit am direktesten, und Folien und Buch bleiben ein gemeinsames Bildsystem.

## 5 — Entscheidungen

### 5.1 Beispiele: das Buch gibt den Ton an

Wenn Folie und Buch verschiedene Beispiele nutzen, passt sich die Abbildung dem Buch an (Entscheidung von Yannick, 17.11.2026). Bildidee, Bausteine und Farben kommen von der Folie; Objektnamen, Werte, Code und Ausgaben kommen aus dem Buch. Der Code im Buch bleibt, wie er ist. Jede Zahl im Bild entspricht der Ausgabe des Chunks, neben dem das Bild steht. Wo das Buch für ein Konzept noch keinen Chunk hat (siehe 5.5), wird das neue Beispiel im Stil der vorhandenen Buchbeispiele gewählt.

### 5.2 Bildsprache

| Element | Bedeutung |
| :-- | :-- |
| Stein mit Noppen | ein Wert |
| Farbe des Steins: blau / lila / rosa | Datentyp numeric / character / logical |
| leerer, gestrichelter Stein | fehlender Wert `NA` |
| Turm (gestapelte Steine, erster Wert oben) | Vektor, eine Spalte |
| Bauplatte mit Türmen gleicher Höhe | Datensatz (Tibble); eine Reihe ist ein Fall |
| dunkles Namensschild | Name eines Objekts |
| gelber Aufkleber am Stein | Wertelabel |
| Code-Bausteine dunkel / grün / orange | Objekt / Funktion / Argument |
| grüner Kasten mit gestricheltem Feld | Funktion mit ihrem ersten Argument |

### 5.3 Werkzeug

- Neuer Ordner `figuren/` im Repository:
  - `figuren/lego.py` — Zeichenbibliothek. Gleiche Funktionsnamen und Argumente wie die Folien-Helfer (`R`, `P`, `text`, `rect`, `card`, `label_box`, `tok`, `tokens`, `stein`, `schild`, `turm`, `arrow`, `connector`, `vline`, `outline`, `chip`, `numdot`, `eyebrow`, `codebox` …), aber mit SVG statt PowerPoint als Ausgabe. Koordinaten in Zoll wie auf den Folien. Nur Python-Standardbibliothek, damit niemand etwas installieren muss.
  - `figuren/kap01.py` … `figuren/kap07.py` — je Kapitel die Abbildungen als Funktionen.
  - `figuren/build.py` — erzeugt alle SVG-Dateien neu: `python3 figuren/build.py`.
- Ausgabe: `Bilder/figuren/<kapitel>-<name>.svg`, z. B. `Bilder/figuren/k03-pipe.svg`. Die SVG-Dateien werden committet; zum Rendern des Buchs braucht man Python nicht.
- Die Bibliothek ist eine eigenständige Kopie im Repository und importiert nichts aus dem Methoden-Ib-Ordner.

### 5.4 Aussehen

- Farben exakt wie auf den Folien (Palette aus `_build_folien.py` und `_build_folien_s4.py`, in `lego.py` übernommen).
- Schrift: Das Buch nutzt die Webschrift Source Sans Pro; ein als Bild eingebundenes SVG kann sie nicht nachladen. Beschriftungen bekommen deshalb die Schriftliste `'Source Sans Pro', 'Source Sans 3', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif`, Code `Menlo, Consolas, 'DejaVu Sans Mono', monospace`. Keine eingebetteten Schriften. Text bleibt Text, damit er scharf zoomt. *(Entscheidung des Umsetzers)*
- Größe: Folien sind 13,33 Zoll breit; im Buch wäre so ein Bild winzig. Jede Abbildung wird deshalb für die Textspalte neu angeordnet: höchstens 8 Zoll breit, kleinste Schrift 10 pt. Die Bausteine und ihre Zeichenbefehle bleiben, die Anordnung ändert sich.
- Handy: Keine zweite Fassung. Jede Abbildung bekommt die Klasse `.lightbox`, damit sie sich per Antippen vergrößert; so ist sie auch bei 375 px Breite lesbar. *(Entscheidung des Umsetzers)*
- Klickfolgen werden zu nummerierten Schritten nebeneinander oder untereinander (grüne Nummernpunkte wie auf den Folien).
- Im Bild steht nur, was zum Bild gehört: Namen, Werte, Code, kurze Beschriftungen. Erklärsätze stehen in der Bildunterschrift oder im Text.

### 5.5 Einbindung ins Buch

- Markdown-Syntax mit Querverweis und Alternativtext:
  `![Bildunterschrift.](Bilder/figuren/k03-pipe.svg){#fig-pipe fig-alt="…"}`
- Jede Abbildung wird im Fließtext mit `@fig-…` angesprochen und in ein bis zwei Sätzen eingeordnet. Sie begleitet Frage → Code → Lesart (`STYLE.md` §1) und ersetzt keinen Code.
- Bildunterschriften: ein bis zwei sachliche Sätze im Du-Stil des Buchs.
- Höchstens eine Abbildung pro Unterabschnitt, außer wenn ein Abschnitt zwei getrennte Konzepte erklärt.
- Wo das Buch ein Konzept der Folie noch gar nicht erklärt (Typumwandlung beim Mischen, Ausführung von oben nach unten, Gewichtung in 7.2), kommen ein kurzer Chunk und ein bis zwei Absätze dazu, innerhalb des bestehenden Abschnitts und ohne neue Überschrift. Das folgt aus dem Auftrag, die Erklärfolien zu übertragen.

### 5.6 Format „Kurz überlegen“

Wo eine Folie eine starke Vorhersagefrage hatte (etwa „Was ist y?“ oder „Welcher Datentyp setzt sich durch?“), bekommt das Buch eine kurze Denkpause: ein Absatz mit **Kurz überlegen.** und der Frage, direkt darunter die Auflösung als eingeklappter `.callout-tip` mit `title="Auflösung" collapse="true"`. Sparsam: höchstens eine pro Abschnitt, im ganzen Buch etwa zehn. Das Format wird vor der ersten Verwendung in `STYLE.md` §4 eingetragen.

Die Abbildung bleibt immer sichtbar, sie ist die Erklärung. Die Frage greift deshalb einen neuen Fall auf, den das Bild nicht zeigt, meist die Zusatzaufgabe oder das Puzzle der Folie (bei der Pipe etwa: „Wie schreibst du `sqrt(sum(c(9, 16)))` als Pipe?“). Die Auflösung im eingeklappten Callout ist Text und Code, ohne eigenes Bild. *(Entscheidung des Umsetzers)*

### 5.7 Text im Buch

- Die Bildsprache wird in Kap. 3 einmal eingeführt, als `.callout-note` („Hintergrund“) am Anfang von 3.5 „Objekte und Datentypen“, mit einer kleinen Legende als Abbildung. Keine neue Überschrift.
- Danach nutzen Bildunterschriften und Text die Begriffe Stein, Turm, Bauplatte und Aufkleber, ohne sie neu zu erklären.
- Fachbegriffe in den Bildern folgen dem Buch, nicht den Folien: „Paket“ statt „Package“, „Skript“ wo das Buch Skript sagt.

## 6 — Abbildungsliste

Quelle: T1 = `ReadingWeek_Folien.pptx` (Tag 1), T2 = `Tag2_Folien.pptx` (Tag 2), jeweils Foliennummer. Abschnitt = Ziel im Buch. Die Spalte „Inhalt“ beschreibt die Bildidee der Folie; Namen und Werte im fertigen Bild kommen aus dem Buch (5.1).

| Nr | Datei | Abschnitt | Quelle | Inhalt | Kurz überlegen |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | `k01-oekosystem` | 1.6 | T1 9 | Funktion → Package → Ökosystem (tidyverse, mariposa) | |
| 2 | `k01-regal-werkbank` | 1.6.2 | T1 11 | `install.packages()` stellt ins Regal, `library()` holt auf die Werkbank | |
| 3 | `k02-qmd-schichten` | 2.4 | T1 21 | YAML-Kopf, Text, Chunk, Inline-Code in einem `.qmd` | |
| 4 | `k03-legende` | 3.5 | T1 40, 41, 44 | Legende der Bildsprache (Stein, Farben, NA, Turm, Platte, Schild, Aufkleber) | |
| 5 | `k03-name-inhalt` | 3.2 | T1 27 | Pfeil legt den Stein unter einem Namensschild ab; Environment | |
| 6 | `k03-reihenfolge` | 3.2 | T1 29 | `x <- 5; y <- x + 2; x <- 10` → `y` bleibt 7 | ja |
| 7 | `k03-funktion` | 3.3 | T1 37 | Werte rein → `mean()` → Ergebnis raus; Code-Farben | |
| 8 | `k03-argumente` | 3.3 | T1 38 | `round(x, digits = 0)` als Formular mit Pflichtfeld und vorausgefülltem Feld | ja |
| 9 | `k03-turm` | 3.5.1 | T1 40 | `c()` stapelt Steine zu einem Turm; ein Turm hat eine Farbe | |
| 10 | `k03-rangfolge` | 3.5.1 | T1 41 | logical < numeric < character beim Mischen | ja |
| 11 | `k03-tibble` | 3.5.3 | T1 44 | Türme nebeneinander = Tibble; Reihe = Fall, Turm = Variable | |
| 12 | `k04-dollar-select` | 4.5.1 | T1 45 | `$` gibt einen Turm, `select()` eine Platte mit Turm (dort, wo `select()` eingeführt wird) | ja |
| 13 | `k03-na` | 3.6 | T1 43, 52 | leerer Stein; `mean()` gibt `NA`, mit `na.rm = TRUE` den Wert | |
| 14 | `k03-pipe` | 3.7.1 | T1 46 | Ergebnis wandert ins erste Feld von `mean()`, dann `round()`; vier Schritte | ja |
| 15 | `k03-analyseplan` | 3.7.3 | T1 48 | Plan in Worten ↔ Pipe-Zeilen | |
| 16 | `k04-einlesen` | 4.3 | T1 51 | `.sav`-Datei → `read_spss()` → Objekt `allbus` als Bauplatte | |
| 17 | `k04-platte` | 4.4 | T1 52 | 5.246 Reihen × 579 Türme; obs. = Reihe, variable = Turm, leerer Stein | |
| 18 | `k04-select` | 4.5.1 | T2 7 | nur die gewählten Türme bleiben auf der Platte | |
| 19 | `k04-filter` | 4.5.2 | T2 8 | nur die Reihen, die die Bedingung erfüllen, bleiben | |
| 20 | `k04-dbl-lbl` | 4.6 | T2 11 | Zahl mit Aufkleber: `<dbl+lbl>` | |
| 21 | `k04-to-label` | 4.6.1 | T2 12 | `to_label()`: Aufkleber wird Wert; `to_numeric()`: Aufkleber ab | |
| 22 | `k04-labels` | 4.7 | T1 53 | Variablenname, Variablenlabel, Wertelabels am Beispiel `pt03` | |
| 23 | `k04-missing-codes` | 4.8 | T2 15, 16 | vier Gründe für eine Lücke; Split-Design | ja |
| 24 | `k04-set-na` | 4.8 | T2 17 | gültige Codes werden zu Lücken; valid N sinkt | |
| 25 | `k05-mutate` | 5.2.1 | T2 19 | neuer Turm aus vorhandenem, Reihe für Reihe | |
| 26 | `k05-zuweisung` | 5.2.1 | T2 20 | ohne `<-` nur angezeigt, mit `<-` gespeichert | ja |
| 27 | `k05-case-when` | 5.2.2 | T2 21 | Bedingungen von oben nach unten, die erste zutreffende gilt | |
| 28 | `k05-summarise` | 5.2.3 | T2 22 | viele Steine je Gruppe → ein Stein je Gruppe | |
| 29 | `k05-rec` | 5.3.1 | T2 23 | Regel-Zeichenkette ordnet 1–7 drei Kategorien zu | |
| 30 | `k05-dicho` | 5.3.2 | T2 24 | Schnittpunkt 50, zwei Gruppen mit Labels | |
| 31 | `k05-umpolen` | 5.3.3 | T2 25, 26 | Turm auf dem Kopf, `8 − x`; Gegenprobe alt gegen neu | ja |
| 32 | `k05-skala` | 5.7 | T2 1, 30 | sechs Türme → ein Skalenturm; `min_valid` bei fehlenden Steinen | ja |
| 33 | `k05-polung` | 5.7.3 | T2 32 | falsch gepolte Skala misst das Gegenteil | |
| 34 | `k05-pomps` | 5.8 | T2 33 | zwei Skalen auf 0–100 umgerechnet | |
| 35 | `k05-pipeline` | 5.9 | T2 34, 27 | vom Arbeitsheft zum Setup-Chunk; Schritte einer Auswertung | |
| 36 | `k07-gewichtung` | 7.2 | T2 36 | Gewicht als Größe des Steins; Ost etwa 0,5, West etwa 1,2 | |
| 37 | `k07-zeilenprozente` | 7.5.1 | T2 41 | jede Zeile ein 100-%-Balken | |

Bewusst nicht übernommen: Zeitleiste (T1 13, Anekdoten), RStudio-Bereiche (T1 14, Kap. 1 hat Screenshots), Testwahl (T2 40, Text statt Bild), t-Test-Glocken und Korrelationswolken (T2 42, 43, Kap. 7 hat Simulationen), Ratespiele ohne Grafik.

## 7 — Reihenfolge

0. Die Überschriften mit Funktionsnamen und die Tastenkürzel-Tabelle (Stand 17.11.2026, noch nicht committet) bekommen vorher ihren eigenen Commit, damit die Abbildungen getrennt bleiben. Die Abschnittsnummern in Abschnitt 6 beziehen sich auf diesen Stand.
1. Werkzeug (`lego.py`, `build.py`), `STYLE.md`-Eintrag für „Kurz überlegen“.
2. **Pilot Kap. 3** mit fünf Abbildungen: Nr. 4 Legende, 9 Turm, 10 Rangfolge, 11 Tibble, 14 Pipe, dazu die Einführung der Bildsprache und eine Denkpause. Durchsicht im Browser mit Yannick; Stil, Größe und Ton werden hier festgelegt.
3. Rest von Kap. 3, dann Kap. 4, Kap. 5, Kap. 1/2 und Kap. 7, jeweils mit Durchsicht im Browser.
4. Commit pro Kapitelblock auf `modernisierung-2026`; veröffentlicht wird nur nach Freigabe (`main` vorspulen, pushen).

## 8 — Prüfung

- Buch rendert ohne neue Warnungen; Abschnittsnummern vor und nach dem Rendern verglichen, keine verschoben.
- Jede Abbildung im Browser angesehen, in voller Breite und bei Handybreite (375 px); auf dem Desktop ist die kleinste Schrift ohne Zoom lesbar, auf dem Handy nach Antippen.
- Jede Abbildung hat Bildunterschrift, `fig-alt` und einen Verweis im Text.
- Jede Zahl im Bild gegen die Ausgabe in R 4.5.3 und mariposa 0.7.4 geprüft.
- Bildunterschriften und neue Absätze auf Slogans und Folienton gelesen.

## 9 — Dem Umsetzenden überlassen

- Genaue Anordnung jeder Abbildung innerhalb der Grenzen aus 5.4.
- Wortlaut von Bildunterschriften, Alternativtexten und Einordnungssätzen.
- Interne Struktur von `lego.py`, solange die Funktionsnamen der Folien-Helfer erhalten bleiben.
- Messung von Textbreiten (Näherung reicht, mit Spielraum für Ausweichschriften).
