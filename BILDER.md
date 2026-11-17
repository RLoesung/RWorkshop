# Bausteine-Abbildungen — Entwurf und Vertrag

**Zweck.** Dieses Dokument regelt, wie die Erklärgrafiken aus dem Workshop „Reading Week“ (Tag 1 „R-Einstieg“, Tag 2 „Daten und Analyse“, November 2026) ins Buch kommen. Es ist zugleich der Vertrag für alle späteren Abbildungen in dieser Bildsprache, so wie `STYLE.md` den Text und `MIGRATION.md` den Code regelt.

**Status.** Umgesetzt am 17.11.2026: 37 Abbildungen in Kap. 1, 2, 3, 4, 5 und 7. Die Abschnitte 5 und 6 beschreiben den gebauten Stand.

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
- Keine Bausteine-Grafik dort, wo das Buch schon eine bessere Abbildung hat (Inferenz-Simulationen in Kap. 7, ggplot-Ergebnisse in Kap. 6–9). Seit der Erweiterung vom 17.11.2026 (Abschnitt 6, Nr. 38–50) bekommen auch Kap. 6, 8 und 9 Bausteine-Bilder, aber nur für Konzepte, die dort bisher ohne Bild erklärt werden.
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
| grauer Stein | fällt im Ergebnis weg (`select()`, `filter()`, `drop_na()`) oder wird nur angezeigt, nicht gespeichert (ohne `<-`); bei `row_count()` ein Wert, der nicht mitgezählt wird (5.7.2); bei `augment()` eine Spalte, die im Ergebnis steht, in der gezeigten Rechnung aber keine Rolle spielt (9.6.3) |
| leerer Stein mit Aufkleber | fehlender Wert mit Missing-Code und Label |
| Name und grauer Typ über einem Turm | Spaltenkopf wie in der Ausgabe eines Tibbles, etwa `<dbl+lbl>` |
| graue Auslassungspunkte | weitere Türme oder Reihen, die nicht gezeigt sind |
| oranger Rahmen / grüner Rahmen | eine Reihe (ein Fall) / ein Turm (eine Variable, auch ein neuer Turm) |
| eckige Klammer neben Steinen | eine Gruppe von Werten (`rec()`, `dicho()`, Gewichtung) |
| orange gestrichelte Linie | Schnittpunkt bei `dicho()` |
| Lineal mit Pfeilmarken | Wertebereich einer Skala, der Pfeil zeigt einen Mittelwert (`pomps()`) |
| Zeitleiste mit grünen Nummernpunkten | Schritte einer Auswertung in ihrer Reihenfolge (Pipeline in 5.9) |
| Breite eines Steins | Gewicht eines Falls (7.2) |
| grüner Kasten / dunkel umrandeter Kasten / grün gestrichelter Rahmen | Funktion / Paket / Ökosystem (1.6) |
| Regal / Werkbank mit Paket-Kacheln | Paket installiert / mit `library()` geladen (1.6.2, 2.6.1) |
| Ordner mit Reiter und Datei-Kacheln | Projektordner, Arbeitsverzeichnis (1.4.4) |
| graue Balken auf einer Seite | Fließtext, der nicht wiedergegeben ist (1.7) |
| Operator zwischen den Steinen jeder Reihe | R rechnet oder vergleicht Stein für Stein (3.4.3, 3.5.1) |
| rosa Turm neben einem Turm | Wahrheitsturm als Schablone für `[ ]`: Steine neben `FALSE` werden grau und fallen weg (3.5.1) |
| blasser Stein (Farbe des Datentyps, heller, Kante in der vollen Farbe) | ein Wert, den R wiederholt (Recycling, 3.5.1); anders als ein grauer Stein geht er in die Rechnung ein (`lego.stein(…, blass=True)`) |
| weißes Schild „Referenz“ mit Spitze zum Stein | Referenzkategorie eines Faktors, die erste Stufe (3.5.2; `lego.referenz()`) |
| Kiste mit Fächern, oben je ein `$`-Name | Liste: Jedes Fach ist ein Element, die Inhalte können sich in Typ und Länge unterscheiden (3.5.4, auch für Ergebnisobjekte; `lego.kiste()`). Ein letztes Fach mit grauen Auslassungspunkten: Die Liste hat weitere Elemente (`kiste(…, mehr=…)`); eine Kiste in einem Fach ist eine Liste in der Liste (8.3.3) |
| graue Zahlen links neben einer Reihe | Reihennummer wie in der Ausgabe eines Tibbles; Lücken in der Zählung stehen für Reihen, die nicht gezeigt sind (4.5.2, 4.8) |
| leerer Stein mit blassem Aufkleber | fehlender Wert in einer Reihe, die im Ergebnis wegfällt (4.5.2; `kap04.lstein(…, blass=True)`) |
| Lineale untereinander mit gestrichelten Hilfslinien | dieselben Fälle auf verschiedenen Skalen: Die blauen Pfeile (einzelne Werte) bleiben an ihrer Stelle, Nullpunkt und Einheit ändern sich (`center()`, `std()`, 5.4); der orange Pfeil zeigt den Mittelwert |
| zwei Lineale mit derselben Skala, gestrichelte Linien von Pfeil zu Pfeil | derselbe Mittelwert je Gruppe ohne und mit Kontrolle einer Kovariate; die Linie zeigt, wohin sich eine Gruppe verschiebt (9.7.3). Liegen zwei Mittelwerte fast gleich, trennt eine weiße Kante die beiden orangen Pfeile (`kap09.mittel_marke()`) |
| Rechenzeile mit grauen Namen unter den Werten | wie R einen Wert einer Reihe ausrechnet; unter jeder Zahl steht, aus welcher Spalte oder welchem Koeffizienten sie kommt (`.fitted` und `.resid` in 9.6.3; `kap09.rechnung()`) |
| dunkles Namensschild über einem Turm | Spaltenname, der beim Umformen zum Wert wird oder aus Werten entsteht (`pivot_longer()`, `pivot_wider()`, 5.6) |
| oranger Rahmen um mehrere Reihen | ein Fall, der im Long-Format über mehrere Reihen verteilt ist (5.6.1) |
| grüner Funktionsname über einer Platte | die Platte ist das Ergebnis dieser Funktion (Join-Familie in 5.5, 5.6.2) |
| blassoranger Kasten mit `x`, `y`, `color`, `fill` oder `weight` | Zuordnung in `aes()`: Unter einem Turm sagt er, welche Eigenschaft der Grafik der Turm bestimmt; derselbe Kasten an der Grafik zeigt, wo sie erscheint (6.2, 6.3.2, 6.4.1; `kap06.etikett()`) |
| kleine Grafik mit Achsen, Gitter und Punkten, Balken oder Violinen | vereinfachte Ausgabe von ggplot2 mit den Farben und Werten aus `layer_data()`; in 6.2 ist jeder Punkt eine Reihe |
| Folie (helles Blatt mit umgeknickter Ecke) | eine Ebene einer ggplot-Grafik (`geom_*()`); `+` legt sie auf die Grafik aus `ggplot()`, was später kommt, liegt oben (6.3.3; `kap06.folie()`) |
| gestrichelte Ellipse mit dunkler Kante, darin nur ein Name | nicht gemessener (latenter) Faktor ohne Werte; Pfeile führen von ihm zu den Items, die er erzeugt. Anders als ein leerer Stein (`NA`) hat sie keine Noppen und steht auf keiner Platte (8.1; `kap08.faktor()`) |

### 5.3 Werkzeug

- Neuer Ordner `figuren/` im Repository:
  - `figuren/lego.py` — Zeichenbibliothek. Gleiche Funktionsnamen und Argumente wie die Folien-Helfer (`R`, `P`, `text`, `rect`, `card`, `label_box`, `tok`, `tokens`, `stein`, `schild`, `turm`, `arrow`, `connector`, `vline`, `outline`, `chip`, `numdot`, `eyebrow`, `codebox` …), aber mit SVG statt PowerPoint als Ausgabe. Koordinaten in Zoll wie auf den Folien. Nur Python-Standardbibliothek, damit niemand etwas installieren muss.
  - `figuren/kap01.py` … `figuren/kap07.py` — je Kapitel die Abbildungen als Funktionen.
  - `figuren/build.py` — erzeugt alle SVG-Dateien neu: `python3 figuren/build.py`.
- Ausgabe: `Bilder/figuren/<kapitel>-<name>.svg`, z. B. `Bilder/figuren/k03-pipe.svg`. Die SVG-Dateien werden committet; zum Rendern des Buchs braucht man Python nicht.
- Die Bibliothek ist eine eigenständige Kopie im Repository und importiert nichts aus dem Methoden-Ib-Ordner.
- Prüfen: `python3 -m unittest discover figuren` (Werte und Grenzen jeder Abbildung), `python3 figuren/check_qmd.py` (Einbindung in den Kapiteln) und `python3 figuren/check_sections.py` (keine verschobenen Abschnittsnummern).

### 5.4 Aussehen

- Farben exakt wie auf den Folien (Palette aus `_build_folien.py` und `_build_folien_s4.py`, in `lego.py` übernommen).
- Schrift: Das Buch nutzt die Webschrift Source Sans Pro; ein als Bild eingebundenes SVG kann sie nicht nachladen. Beschriftungen bekommen deshalb die Schriftliste `'Source Sans Pro', 'Source Sans 3', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif`, Code `Menlo, Consolas, 'DejaVu Sans Mono', monospace`. Keine eingebetteten Schriften. Text bleibt Text, damit er scharf zoomt. *(Entscheidung des Umsetzers)*
- Größe: Folien sind 13,33 Zoll breit; im Buch wäre so ein Bild winzig. Jede Abbildung wird deshalb für die Textspalte neu angeordnet: höchstens 8 Zoll breit, kleinste Schrift 10 pt. Die Bausteine und ihre Zeichenbefehle bleiben, die Anordnung ändert sich.
- Handy: Keine zweite Fassung, die Breite bleibt bei höchstens 8 Zoll (Entscheidung von Yannick, 17.11.2026). Im Hochformat (375 px) ist eine Abbildung etwa 324 px breit; gut lesbar ist sie dann erst mit Zwei-Finger-Zoom oder im Querformat. Jede Abbildung hat die Klasse `.lightbox` und öffnet sich per Antippen größer.
- Klickfolgen werden zu nummerierten Schritten nebeneinander oder untereinander (grüne Nummernpunkte wie auf den Folien).
- Im Bild steht nur, was zum Bild gehört: Namen, Werte, Code, kurze Beschriftungen. Erklärsätze stehen in der Bildunterschrift oder im Text.

### 5.5 Einbindung ins Buch

- Markdown-Syntax mit Querverweis und Alternativtext:
  `![Bildunterschrift.](Bilder/figuren/k03-pipe.svg){#fig-pipe .lightbox fig-alt="…"}`
- Jede Abbildung wird im Fließtext mit `@fig-…` angesprochen und in ein bis zwei Sätzen eingeordnet. Sie begleitet Frage → Code → Lesart (`STYLE.md` §1) und ersetzt keinen Code.
- Bildunterschriften: ein bis zwei sachliche Sätze im Du-Stil des Buchs.
- Höchstens eine Abbildung pro Unterabschnitt, außer wenn ein Abschnitt zwei getrennte Konzepte erklärt.
- Wo das Buch ein Konzept der Folie noch gar nicht erklärt (Typumwandlung beim Mischen, Ausführung von oben nach unten, Gewichtung in 7.2), kommen ein kurzer Chunk und ein bis zwei Absätze dazu, innerhalb des bestehenden Abschnitts und ohne neue Überschrift. Das folgt aus dem Auftrag, die Erklärfolien zu übertragen.

### 5.6 Format „Kurz überlegen“

Wo eine Folie eine starke Vorhersagefrage hatte (etwa „Was ist y?“ oder „Welcher Datentyp setzt sich durch?“), bekommt das Buch eine kurze Denkpause: ein Absatz mit **Kurz überlegen.** und der Frage, direkt darunter die Auflösung als eingeklappter `.callout-tip` mit `title="Auflösung" collapse="true"`. Sparsam: höchstens eine pro Abschnitt, im ganzen Buch etwa zehn. Das Format wird vor der ersten Verwendung in `STYLE.md` §4 eingetragen.

Die Abbildung bleibt immer sichtbar, sie ist die Erklärung. Die Frage greift deshalb einen neuen Fall auf, den das Bild nicht zeigt, meist die Zusatzaufgabe oder das Puzzle der Folie (bei der Pipe etwa: „Wie schreibst du `sqrt(sum(c(9, 16)))` als Pipe?“). Die Auflösung im eingeklappten Callout ist Text und Code, ohne eigenes Bild. *(Entscheidung des Umsetzers)*

### 5.7 Text im Buch

- Die Bildsprache wird in Kap. 3 einmal eingeführt, als `.callout-note` („Hintergrund“) am Anfang von 3.5 „Objekte und Datentypen“, mit einer kleinen Legende als Abbildung. Keine neue Überschrift.
- Die ersten Bausteine-Bilder stehen schon in 3.2 und 3.3. Ein Satz in 3.2 sagt, dass ein Wert ein Stein und ein Name ein dunkles Schild ist, und verweist auf 3.5.
- Danach nutzen Bildunterschriften und Text die Begriffe Stein, Turm, Bauplatte und Aufkleber, ohne sie neu zu erklären.
- Fachbegriffe in den Bildern folgen dem Buch, nicht den Folien: „Paket“ statt „Package“, „Skript“ wo das Buch Skript sagt.

## 6 — Abbildungsliste

Quelle: T1 = `ReadingWeek_Folien.pptx` (Tag 1), T2 = `Tag2_Folien.pptx` (Tag 2), jeweils Foliennummer. Abschnitt = Ort im Buch. Die Spalte „Inhalt“ beschreibt das fertige Bild; Bildidee und Bausteine kommen von der Folie, Namen und Werte aus dem Buch (5.1).

| Nr | Datei | Abschnitt | Quelle | Inhalt | Kurz überlegen |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | `k01-oekosystem` | 1.6 | T1 9 | Funktion → Paket → Ökosystem; das Ökosystem tidyverse und das Paket mariposa | |
| 2 | `k01-regal-werkbank` | 1.6.2 | T1 11 | `install.packages()` stellt ins Regal, `library()` holt auf die Werkbank | |
| 3 | `k02-qmd-schichten` | 2.4 | T1 21 | YAML-Kopf, Text und Chunk eines `.qmd` und was beim Rendern daraus wird | |
| 4 | `k03-legende` | 3.5 | T1 40, 41, 44 | Legende der Bildsprache (Stein, Farben, NA, Turm, Platte, Schild, Aufkleber, Code-Farben) | |
| 5 | `k03-name-inhalt` | 3.2 | T1 27 | Pfeil legt den Stein unter einem Namensschild ab; Environment | |
| 6 | `k03-reihenfolge` | 3.2 | T1 29 | `x <- 5; y <- x + 2; x <- 10` → `y` bleibt 7 | ja |
| 7 | `k03-funktion` | 3.3 | T1 37 | Werte rein → `seq()` → Ergebnis raus; Code-Farben (Chunk `fn-basics`) | |
| 8 | `k03-argumente` | 3.3.1 | T1 38 | `round()` als Formular: Pflichtfeld `x`, `digits` mit 0 vorausgefüllt und mit 1 überschrieben | ja |
| 9 | `k03-turm` | 3.5.1 | T1 40 | `c()` stapelt Steine zu einem Turm; ein Turm hat eine Farbe | |
| 10 | `k03-rangfolge` | 3.5.1 | T1 41 | logical < numeric < character beim Mischen | ja |
| 11 | `k03-tibble` | 3.5.3 | T1 44 | Türme nebeneinander = Tibble; Reihe = Fall, Turm = Variable | |
| 12 | `k04-dollar-select` | 4.5.1 | T1 45 | `$` gibt einen Turm, `select()` eine Platte mit Turm (dort, wo `select()` eingeführt wird) | ja |
| 13 | `k03-na` | 3.6 | T1 43, 52 | leerer Stein; `mean()` gibt `NA`, mit `na.rm = TRUE` den Wert | |
| 14 | `k03-pipe` | 3.7.1 | T1 46 | Ergebnis wandert ins erste Feld von `round()`, dann `head()`; zwei Schritte (Chunk `pipe-native`) | ja |
| 15 | `k03-analyseplan` | 3.7.3 | T1 48 | Plan in Worten ↔ Pipe-Zeilen | |
| 16 | `k04-einlesen` | 4.3 | T1 51 | `.sav`-Datei → `read_spss()` → Objekt `allbus` als Bauplatte | |
| 17 | `k04-platte` | 4.4 | T1 52 | Ausschnitt aus `allbus` (`respid`, `age`, `mm01`); 5.246 Reihen, 579 Türme; Reihe = Fall, Turm = Variable, leerer Stein | |
| 18 | `k04-select` | 4.5.1 | T2 7 | nur die gewählten Türme bleiben auf der Platte | |
| 19 | `k04-filter` | 4.5.2 | T2 8 | nur die Reihen, die die Bedingung erfüllen, bleiben | |
| 20 | `k04-dbl-lbl` | 4.6 | T2 11 | Zahl mit Aufkleber: `<dbl+lbl>` | |
| 21 | `k04-to-label` | 4.6.1 | T2 12 | `to_label()`: Aufkleber wird Wert; `to_numeric()`: Aufkleber ab | |
| 22 | `k04-labels` | 4.7 | T1 53 | Variablenname, Variablenlabel, Wertelabels am Beispiel `mm01` (Chunk `labels-read`) | |
| 23 | `k04-missing-codes` | 4.8 | T2 15, 16 | vier Gründe für eine Lücke; Split-Design | ja |
| 24 | `k04-set-na` | 4.8 | T2 17 | gültige Codes werden zu Lücken; valid N sinkt | |
| 25 | `k05-mutate` | 5.2.1 | T2 19 | neuer Turm aus vorhandenem, Reihe für Reihe | |
| 26 | `k05-zuweisung` | 5.2.1 | T2 20 | ohne `<-` nur angezeigt, mit `<-` gespeichert | ja |
| 27 | `k05-case-when` | 5.2.2 | T2 21 | Bedingungen von oben nach unten, die erste zutreffende gilt; beim Warnkasten „Reihenfolge zählt“ | |
| 28 | `k05-summarise` | 5.2.3 | T2 22 | viele Steine je Gruppe → ein Stein je Gruppe | |
| 29 | `k05-rec` | 5.3.1 | T2 23 | Regel-Zeichenkette ordnet die Codes von `educ` drei Stufen zu, `else=NA` den Rest | |
| 30 | `k05-dicho` | 5.3.2 | T2 24 | Schnittpunkt 50, zwei Gruppen 0 und 1, ohne Wertelabels | |
| 31 | `k05-umpolen` | 5.3.3 | T2 25, 26 | Turm auf dem Kopf, `8 − x`; Gegenprobe alt gegen neu | ja |
| 32 | `k05-skala` | 5.7.1 | T2 1, 30 | sechs Türme → `row_means()` → ein Skalenturm; `min_valid` bei fehlenden Steinen | ja |
| 33 | `k05-polung` | 5.7.3 | T2 32 | falsch gepolte Skala misst das Gegenteil | |
| 34 | `k05-pomps` | 5.8 | T2 33 | zwei Skalen auf 0–100 umgerechnet | |
| 35 | `k05-pipeline` | 5.9 | T2 34, 27 | sechs Schritte der Pipeline mit ihren Abschnitten; `R/prep.R` und der Setup-Chunk von Kap. 6 bis 9 | |
| 36 | `k07-gewichtung` | 7.2 | T2 36 | Gewicht als Breite des Steins, ungewichtet und gewichtet; Ost etwa 0.5, West etwa 1.2 | |
| 37 | `k07-zeilenprozente` | 7.5.1 | T2 41 | jede Zeile ein 100-%-Balken | |

### Erweiterung: alle Kapitel (17.11.2026)

Yannick wollte das Buch „endgültig abrunden“; vier Durchsichten haben jedes Kapitel Abschnitt für Abschnitt auf Bildpotenzial geprüft. Die meisten Bilder haben keine Folienvorlage („neu“). Prio A = deutlicher Gewinn, B = hilfreich. Die Notizen der Durchsicht mit allen geprüften Werten liegen beim Bau als Arbeitsgrundlage vor; im fertigen Bild gelten die Regeln aus 5.1.

| Nr | Datei | Abschnitt | Quelle | Inhalt | Prio | Kurz überlegen |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 38 | `k01-arbeitsverzeichnis` | 1.4.4 | neu | Projektordner als Arbeitsverzeichnis auf zwei Rechnern; `read_spss("ALLBUS2023.sav")` findet die Datei auf beiden, der absolute Pfad aus dem Vorsicht-Kasten nur auf einem | A | |
| 39 | `k01-hilfeseite` | 1.7 | T1 39 | Hilfeseite zu `?mean` als Schema: Usage mit Standardwerten, `na.rm` unter Arguments, Examples | B | |
| 40 | `k02-chunk-optionen` | 2.6 | neu | derselbe Chunk viermal: ohne Option, `echo=FALSE`, `eval=FALSE`, `include=FALSE` — was im Bericht steht und ob er ausgeführt wird | B | |
| 41 | `k02-render-sitzung` | 2.6.1 | neu | Rendern startet eine neue, leere R-Sitzung; erst der Setup-Chunk legt Pakete auf die Werkbank und `allbus` ins Environment | A | ja |
| 42 | `k02-zitieren` | 2.9 | neu | Schlüssel aus der `.bib`-Datei und `@Goodman2016` im Text → nach dem Rendern Zitat und Literaturliste | B | |
| 43 | `k03-vergleich` | 3.4.3 | neu | Turm `alter`, die Bedingungen `alter >= 18` und `alter <= 65` als Wahrheitstürme, `&` verknüpft sie Stein für Stein (Chunk `operators-demo`) | B | |
| 44 | `k03-index` | 3.5.1 | neu | `zahlen > 25` ergibt einen Wahrheitsturm, der als Schablone die Steine auswählt: `30 40 50` (Chunk `boolean-indexing`) | A | |
| 45 | `k03-recycling` | 3.5.1 | neu | `zahlen * 2` und `c(1, 2, 3, 4) + c(10, 20)`: R wiederholt den kürzeren Vektor (blasse Steine) | B | |
| 46 | `k03-faktor` | 3.5.2 | neu | Faktor `geschlecht` mit Stufenleiste (Reihenfolge), internen Codes und erster Stufe als Referenz (Chunk `factors`) | A | ja |
| 47 | `k03-liste` | 3.5.4 | neu | Liste `ergebnis` als Kiste mit Fächern unterschiedlicher Größe; `ergebnis$konfidenz[1]` in zwei Schritten (Chunk `list`) | A | |
| 48 | `k04-filter-na` | 4.5.2 | T2 14 | `sex == 1` ergibt bei leeren Steinen wieder leere Steine; `filter()` behält nur TRUE (Chunk `filter-na-trio`) | A | ja |
| 49 | `k04-drop-na` | 4.8 | neu | `drop_na()` auf `mm01`–`mm03`: Eine Lücke kostet die ganze Reihe (Chunk `drop-na`) | B | |
| 50 | `k05-std` | 5.4 | neu | `age` auf dem Lineal: `center()` zieht den Mittelwert ab, `std()` teilt durch die SD (Chunk `std-center`) | B | |
| 51 | `k05-join` | 5.5 | neu | `left_join()` über den Schlüssel `eastwest`: Kontextwerte werden zu neuen Türmen, alle Reihen bleiben (Chunks `join-kontext`, `join-demo`) | A | |
| 52 | `k05-join-familie` | 5.5 | neu | Schema: zwei kleine Platten mit teils fehlenden Schlüsseln → `left_join()`, `inner_join()`, `full_join()` | B | |
| 53 | `k05-pivot-longer` | 5.6.1 | neu | aus sechs Item-Türmen werden ein Turm `item` und ein Turm `antwort`; Namensschilder werden Steine (Chunks `pivot-wide-show`, `pivot-longer-demo`) | A | |
| 54 | `k05-pivot-wider` | 5.6.2 | neu | `names_from` liefert die Namensschilder, `values_from` die Steine (Chunks `pivot-mw-long`, `pivot-wider-demo`) | B | |
| 55 | `k05-row-count` | 5.7.2 | neu | `row_count(count = 7)` zählt pro Reihe; Lücken ergeben 0, nicht NA (Chunk `row-count-demo`) | B | |
| 56 | `k06-grammatik` | 6.2 | neu | `aes()` ordnet Türme der x-Achse, der y-Achse und der Farbe zu; jede Reihe wird ein Punkt (neuer Chunk `grammatik-vier`) | A | |
| 57 | `k06-aes-konstante` | 6.3.2 | neu | in `aes()` ein Turm (Farbe je Stufe, Legende), außerhalb ein einzelner Wert (alle gleich, keine Legende) (Chunk `aes-vs-konstant`) | A | ja |
| 58 | `k06-ebenen` | 6.3.3 | neu | bis `ggplot()` läuft die Bauplatte durch `\|>`, danach legt `+` Ebenen übereinander (Chunks `boxviolin`, `combo`) | B | |
| 59 | `k06-bar-zaehlt` | 6.4.1 | neu | `geom_bar()` zählt erst (gewichtet) je Stufe, `after_stat(prop)` zeichnet die Anteile (Chunk `bar-prop`) | A | |
| 60 | `k07-haeufigkeit` | 7.4.1 | neu | Turm `mm01`: N, Raw % und Valid %; leere Steine zählen bei den gültigen Prozent nicht mit (Chunk `freq-mm`) | A | |
| 61 | `k08-latenter-faktor` | 8.1 | neu | sechs gemessene Item-Türme und ein nicht gemessener Faktor als gestrichelte Ellipse, die auf alle zeigt; ersetzt das Text-Diagramm im Konzept-Kasten | A | |
| 62 | `k08-ergebnisobjekt` | 8.3.3 | T2 42 | `efa_vor` als Kiste mit Fächern (`$loadings`, `$eigenvalues`, `$kmo`, `$bartlett`, dahinter weitere); `$kmo` und `$bartlett` sind Kisten in der Kiste, `efa_vor$kmo$per_item` nimmt in zwei Schritten ein Fach heraus (Chunks `efa-vor`, `efa-bartlett`, `efa-msa`, `efa-1`) | A | |
| 63 | `k08-item-total` | 8.7.4 | neu | korrigierte Item-Total-Korrelation: Summe der anderen fünf Items gegen `mm05r` (Chunk `reliability-summary`) | B | |
| 64 | `k09-dummy` | 9.3.1 | neu | der Faktor `educ_kat` (Reihen 1, 2, 8) wird zu zwei 0/1-Türmen, `niedrig` ist die Referenz (Stufenleiste mit Schild wie in `k03-faktor`) | B | ja |
| 65 | `k09-fallset` | 9.4.1 | neu | `drop_na()` über alle Modellvariablen: Die Split-Module lassen 1.881 von 5.246 Reihen übrig; die ersten acht Reihen, nur 1 und 6 bleiben; Reihe 5 orange, weil ohne gemeinsames `drop_na()` nur `m_basis` mit ihr rechnen würde (Chunk `model-compare`) | A | |
| 66 | `k09-augment` | 9.6.3 | neu | `augment()` stellt `.fitted` und `.resid` neben die Daten; Rechnung für Reihe 1 aus der Koeffiziententabelle; `(weights)` und `.hat` grau, `eastwest`/`sex` und die übrigen Diagnosespalten als Auslassungspunkte (8 Zoll reichen nicht für alle Türme); die Reihen sind respid 1 und 6 aus `k09-fallset` (Chunks `augment-setup`, `lm-summary`) | A | |
| 67 | `k09-randmittel` | 9.7.3 | neu | Gruppenmittel ohne und mit Kontrolle für Alter auf zwei Linealen (`oneway_anova()` aus 7.6.2 gegen die Randmittel aus Chunk `ancova-summary`) | B | |
| 68 | `k09-ame` | 9.8.1 | neu | vorhergesagte Wahrscheinlichkeit je Person (respid 1, 5, 6) bei niedriger und hoher Bildung, Differenz je Reihe, gewichteter Mittelwert = AME (Chunk `logreg-ame`, Vorhersagen mit `predict()` geprüft) | B | |

Nach der Durchsicht verworfen: Inline-Code in 2.7 (Quelle und Ergebnis stehen schon untereinander), Geom-Wahl in 6.4 (die Tabelle zeigt es, und Steinfarbe ist nicht dasselbe wie kategorial/kontinuierlich), Facets in 6.5 (die Panels zeigen die Aufteilung selbst), Gruppenvergleich in 7.6.1 (zeigt `k05-summarise`), Korrelationsmatrix in 8.2.2 (Heatmap in 8.2.4), Vorhersage in 9.2.2 (geht in `k09-augment` auf), VIF in 9.5.3 (drei Chunks zeigen die Schritte).

Bewusst nicht übernommen: Zeitleiste (T1 13, Anekdoten), RStudio-Bereiche (T1 14, Kap. 1 hat Screenshots), Testwahl (T2 40, Text statt Bild), t-Test-Glocken und Korrelationswolken (T2 42, 43, Kap. 7 hat Simulationen), Ratespiele ohne Grafik.

## 7 — Reihenfolge

0. Die Überschriften mit Funktionsnamen und die Tastenkürzel-Tabelle (Stand 17.11.2026, noch nicht committet) bekommen vorher ihren eigenen Commit, damit die Abbildungen getrennt bleiben. Die Abschnittsnummern in Abschnitt 6 beziehen sich auf diesen Stand.
1. Werkzeug (`lego.py`, `build.py`), `STYLE.md`-Eintrag für „Kurz überlegen“.
2. **Pilot Kap. 3** mit fünf Abbildungen: Nr. 4 Legende, 9 Turm, 10 Rangfolge, 11 Tibble, 14 Pipe, dazu die Einführung der Bildsprache und eine Denkpause. Durchsicht im Browser mit Yannick; Stil, Größe und Ton werden hier festgelegt.
3. Rest von Kap. 3, dann Kap. 4, Kap. 5, Kap. 1/2 und Kap. 7, jeweils mit Durchsicht im Browser.
4. Commit pro Kapitelblock auf `modernisierung-2026`; veröffentlicht wird nur nach Freigabe (`main` vorspulen, pushen).

## 8 — Prüfung

- Buch rendert ohne neue Warnungen; Abschnittsnummern vor und nach dem Rendern verglichen, keine verschoben.
- Jede Abbildung im Browser angesehen, in voller Breite und bei Handybreite (375 px); auf dem Desktop ist die kleinste Schrift ohne Zoom lesbar, auf dem Handy mit Zwei-Finger-Zoom oder im Querformat (5.4).
- Jede Abbildung hat Bildunterschrift, `fig-alt` und einen Verweis im Text.
- Jede Zahl im Bild gegen die Ausgabe in R 4.5.3 und mariposa 0.7.4 geprüft.
- Bildunterschriften und neue Absätze auf Slogans und Folienton gelesen.

## 9 — Dem Umsetzenden überlassen

- Genaue Anordnung jeder Abbildung innerhalb der Grenzen aus 5.4.
- Wortlaut von Bildunterschriften, Alternativtexten und Einordnungssätzen.
- Interne Struktur von `lego.py`, solange die Funktionsnamen der Folien-Helfer erhalten bleiben.
- Messung von Textbreiten (Näherung reicht, mit Spielraum für Ausweichschriften).
