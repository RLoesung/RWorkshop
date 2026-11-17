# Bausteine-Abbildungen, Erweiterung auf alle Kapitel — Umsetzungsplan

> Schritte mit Checkbox (`- [ ]`) abhaken. Ablauf wie beim ersten Plan (`BILDER-PLAN.md`, Task 6–10): je Task ein Kapitelblock, danach Prüfung, am Ende Gesamtprüfung und Veröffentlichen (von Yannick freigegeben).

**Ziel:** Die 31 Abbildungen Nr. 38–68 aus `BILDER.md` §6 („Erweiterung: alle Kapitel“) bauen und einbinden, dazu vier kleine Textkorrekturen, die bei der Durchsicht aufgefallen sind.

**Aufbau:** wie bisher — Zeichenmodule `figuren/kapNN.py` mit `FIGUREN`-Dict, Tests `figuren/test_kapNN.py` (für Kap. 3: `ERWARTET_KAP03` in `figuren/test_lego.py`), SVG nach `Bilder/figuren/`, Einbindung mit `{#fig-… .lightbox fig-alt="…"}`.

**Entwurf:** `BILDER.md` (bindend). Arbeitsnotizen der Durchsicht mit geprüften Werten: `.superpowers/sdd/BILDER-PLAN-2/survey/ergebnis-*.md`.

## Globale Vorgaben

- Alle Vorgaben aus `BILDER-PLAN.md` („Globale Vorgaben“) gelten unverändert: höchstens 8 Zoll Breite (768 Einheiten), kleinste Schrift 10 pt, Farben und Schriften wie dort, Einbindung mit `#fig-`, `.lightbox`, `fig-alt` und Verweis `@fig-`, Werte aus dem Buch-Chunk daneben, keine Überschrift, die eine Nummer verschiebt, kein KI-Ton, „Paket“ statt „Package“, Commits auf `modernisierung-2026`, nicht pushen.
- Neue Bildelemente (blasser Stein = von R wiederholt, Kiste mit Fächern/Schubladen = Liste, gestrichelter Umriss = nicht gemessener Faktor, Folien = ggplot-Ebenen) werden in `BILDER.md` §5.2 eingetragen, sobald sie zum ersten Mal gebaut werden. Ein Element sieht in allen Kapiteln gleich aus (die Kiste aus `k03-liste` ist dieselbe wie in `k08-ergebnisobjekt`).
- Gemeinsame Zeichenhelfer, die mehrere Kapitel brauchen, kommen in `figuren/lego.py` (mit Test), nicht in ein Kapitelmodul.
- „Kurz überlegen“ nur bei den Zeilen mit „ja“ in §6.
- Ein Bild, das sich beim Bauen als überflüssig erweist (zeigt nichts, was Text oder vorhandene Grafik nicht schon zeigt), wird nicht gebaut; das kommt mit Begründung in den Bericht.

## Worauf die Prüfung achten muss

1. Werte im Bild weichen von der Ausgabe ab, besonders bei gewichteten Zahlen (Kap. 6, 7, 9) und bei Werten, die kein Chunk druckt.
2. Ein Element sieht in verschiedenen Kapiteln verschieden aus (Kiste, Lineal, grauer Stein).
3. Abschnittsnummern verschieben sich — `python3 figuren/check_sections.py`.
4. Bild ohne Alternativtext, Verweis oder Lightbox — `python3 figuren/check_qmd.py`.
5. Text, der dem Bild widerspricht (Reihenfolge, Farben, Begriffe).

---

### Task 1: Kap. 1 und 2
Abbildungen Nr. 38–42. Dazu: In 2.11 liegt `ALLBUS2023.sav` im Ordnerbaum unter `data/`, das Buch liest die Datei aber überall ohne `data/` ein — Baum oder Satz so anpassen, dass beides zusammenpasst. Neue Module `figuren/kap01.py`/`kap02.py` erweitern, Tests in `figuren/test_kap01.py`/`test_kap02.py`. Rendern: `01-RStudio.qmd`, `02-Quarto.qmd`. Commit „Bausteine-Abbildungen 2: Kap. 1 und 2“.

### Task 2: Kap. 3
Abbildungen Nr. 43–47. Dazu: Prüfe den Satz zu `lm(y ~ ., data = .)` in 3.7.2 — der erste Punkt ist der Formelpunkt, nicht der Platzhalter; Text richtigstellen, falls er etwas anderes sagt. Rendern: `03-ProgrammierspracheR.qmd`. Commit „Bausteine-Abbildungen 2: Kap. 3“.

### Task 3: Kap. 4
Abbildungen Nr. 48–49. Rendern: `04-Datenimport.qmd`. Commit „Bausteine-Abbildungen 2: Kap. 4“.

### Task 4: Kap. 5
Abbildungen Nr. 50–55. Wenn `k05-std` Mittelwert und SD von `age` zeigt, die kein Chunk druckt, nennt der Text sie (BILDER §5.1). Rendern: `05-Datentransformation.qmd`. Commit „Bausteine-Abbildungen 2: Kap. 5“.

### Task 5: Kap. 6
Abbildungen Nr. 56–59 (neues Modul `figuren/kap06.py`, Test `figuren/test_kap06.py`). Für `k06-grammatik` ist ein kurzer Chunk erlaubt (BILDER §5.5), wenn kein vorhandener Chunk genau dieses Mapping zeigt. Dazu zwei Buchfehler in 6.3.2: Der Text nennt die Farbe bei `aes(fill = "steelblue")` „braungrau“, ggplot zeichnet `#F8766D` (lachsrot) — mit `layer_data()` prüfen und richtigstellen; der Chunk-Kommentar „ein Balken pro sex-Stufe“ stimmt nicht (ein Balken je Alter, nach `sex` gestapelt). Rendern: `06-Grafiken-Grundlagen.qmd`. Commit „Bausteine-Abbildungen 2: Kap. 6“.

### Task 6: Kap. 7 und 8
Abbildungen Nr. 60–63 (Modul `figuren/kap08.py` neu, Test `figuren/test_kap08.py`). `k08-latenter-faktor` ersetzt das Text-Diagramm im Konzept-Kasten „Was ist eine latente Variable?“ in 8.1. Rendern: `07-Uni-Bivariate-Analyse.qmd`, `08-Latente-Strukturen.qmd`. Commit „Bausteine-Abbildungen 2: Kap. 7 und 8“.

### Task 7: Kap. 9
Abbildungen Nr. 64–68 (Modul `figuren/kap09.py` neu, Test `figuren/test_kap09.py`). In 5.3.4 (`to_dummy()`) ein Halbsatz mit Verweis auf `@fig-dummy`, falls er passt. Rendern: `09-Erklaerungsmodelle.qmd`. Commit „Bausteine-Abbildungen 2: Kap. 9“.

### Task 8: Abschluss
- `BILDER.md`: §5.2 vollständig für alle neuen Elemente; §6 an die tatsächliche Einbindung angleichen (grep `Bilder/figuren/`), Status „Erweiterung umgesetzt am …“; §5.6 und `STYLE.md` §4: die Angabe „im ganzen Buch etwa zehn“ durch die tatsächliche Zahl und „sparsam, höchstens eine pro Abschnitt“ ersetzen.
- `NEWS.md`: Eintrag oben (Kapitel in aufsteigender Reihenfolge, Zahl der neuen Abbildungen, die Textkorrekturen aus Task 1, 2, 5 in einem Satz).
- Ganzes Buch rendern; `python3 -m unittest discover figuren`, `check_qmd.py`, `check_sections.py` → grün/0; bekannte Warnung „code-linking has been disabled“ (Kap. 5) ist alt.
- Commit „Bausteine-Abbildungen 2: NEWS und Abschluss“.
