# Bausteine-Abbildungen — Umsetzungsplan

> **Für die Umsetzung:** Schritte mit Checkbox (`- [ ]`) abhaken. Nach Task 5 (Pilot) ist eine Durchsicht mit Yannick Pflicht, bevor es weitergeht.

**Ziel:** Die Erklärgrafiken aus Tag 1 und Tag 2 des Workshops als SVG-Abbildungen in die passenden Abschnitte von Kap. 1–5 und 7 bringen, mit den Beispielen des Buchs.

**Aufbau:** Eine kleine Python-Bibliothek `figuren/lego.py` bildet die Zeichenbefehle der Folien-Helfer nach und schreibt SVG statt PowerPoint. Je Kapitel definiert ein Modul die Abbildungen; `figuren/build.py` erzeugt alle Dateien nach `Bilder/figuren/`. Die `.qmd`-Kapitel binden sie mit Querverweis, Alternativtext und Lightbox ein.

**Werkzeuge:** Python 3 (nur Standardbibliothek), Quarto (RStudio-Bundle: `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto`), R 4.5.3 mit mariposa 0.7.4.

**Entwurf:** `BILDER.md` (freigegeben am 17.11.2026). Der Plan argumentiert aus dem Entwurf; bei Widerspruch gilt der Entwurf.

## Globale Vorgaben

- Ausgabe: `Bilder/figuren/<kNN>-<name>.svg`, Dateinamen wie in `BILDER.md` §6.
- SVG-Einheit: 1 Zoll = 96 Nutzereinheiten; Breite der `viewBox` höchstens 768 (8 Zoll).
- Kleinste Schrift 10 pt (13,33 Nutzereinheiten).
- Farben: INK `#1E2D3C`, GRAY `#6E7882`, GREEN `#36A266`, ORANGE `#E6A033`, CARD `#FAF7F1`, CARDLINE `#D7D1C4`, WHITE `#FFFFFF`, PALE `#FBECD2`, LIGHT `#F3CF97`, STICKER `#FAC775`; Steine (Füllung/Schrift): num `#85B7EB`/`#042C53`, txt `#AFA9EC`/`#26215C`, log `#F4C0D1`/`#4B1528`, na `#FFFFFF`/`#6E7882` gestrichelt, dim `#E4E1D8`/`#A8A69E`.
- Schriften: Beschriftung `'Source Sans Pro', 'Source Sans 3', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif`; Code `Menlo, Consolas, 'DejaVu Sans Mono', monospace`. Keine eingebetteten Schriften.
- Einbindung: `![Bildunterschrift.](Bilder/figuren/<datei>.svg){#fig-<name> .lightbox fig-alt="<Alternativtext>"}`; jede Abbildung wird im Text mit `@fig-<name>` angesprochen (Ausnahme: keine).
- Namen, Werte, Code und Ausgaben im Bild kommen aus dem Buch-Chunk, neben dem das Bild steht (`BILDER.md` §5.1). Buch-Code wird nicht geändert; neue Chunks nur dort, wo `BILDER.md` §5.5 es vorsieht.
- Keine neue nummerierte Überschrift, die eine bestehende Abschnittsnummer verschiebt; keine Folienformate, keine Slogans (`BILDER.md` §2).
- „Kurz überlegen“: Absatz mit **Kurz überlegen.** + Frage zu einem neuen Fall, darunter `::: {.callout-tip title="Auflösung" collapse="true"}` mit Text und Code, ohne Bild.
- Fachbegriffe wie im Buch („Paket“, nicht „Package“).
- Commits auf `modernisierung-2026`; nicht pushen.

## Worauf die Prüfung achten muss

1. **Ausweichschrift breiter als gedacht** (Windows ohne Source Sans/Menlo): Text läuft aus Kästen. Erwartung: Jede Beschriftung passt auch mit Arial bzw. Consolas. → Test `test_text_fits_fallback` in Task 1.
2. **Bildwerte weichen von der Ausgabe ab** (Faktorstufen alphabetisch, `round(1.55, 1)` ergibt 1.6): Erwartung: jede Zahl im Bild = Ausgabe des Chunks. → Prüfschritt mit `Rscript` in jedem Abbildungs-Task.
3. **Abschnittsnummern verschieben sich** durch neue Überschriften. → `figuren/check_sections.py` in Task 2, Lauf in jedem Kapitel-Task.
4. **Abbildung ohne Alternativtext, Querverweis oder Lightbox.** → `figuren/check_qmd.py` in Task 2.
5. **Handybreite**: Abbildung ohne Antippen unlesbar und Lightbox funktioniert nicht. → Browserprüfung bei 375 px in Task 5, Schritt 7.

---

### Task 0: Offene Änderungen sichern

**Dateien:** alle bisher nicht committeten Änderungen (Überschriften mit Funktionsnamen, Tastenkürzel-Tabelle, `NEWS.md`, `_freeze/`, `docs/`), dazu `BILDER.md`, `BILDER-PLAN.md`.

- [ ] **Schritt 1:** `git status --short` zeigt nur diese Dateien (plus `.claude/`, das nicht committet wird).
- [ ] **Schritt 2:** Commit „modernisierung-2026 Phase 6w: Funktionsnamen in den Überschriften“ mit den Kapitel-, `NEWS.md`-, `_freeze/`- und `docs/`-Dateien.
- [ ] **Schritt 3:** Commit „Bausteine-Abbildungen: Entwurf und Plan“ mit `BILDER.md` und `BILDER-PLAN.md`.

### Task 1: Zeichenbibliothek `figuren/lego.py`

**Dateien:** neu `figuren/lego.py`, `figuren/test_lego.py`.

**Schnittstellen:**
- Erzeugt: `Canvas(w: float, h: float)` (Zoll) mit `.svg() -> str`; Zeichenfunktionen mit den Signaturen der Folien-Helfer, erstes Argument ist das Canvas: `R(text, font=SANS, size=14, bold=False, italic=False, color=INK)`, `P(*runs, align=L, sb=None, sa=None, ls=None)`, `text(s, x, y, w, h, paras, anchor=None)`, `rect(s, x, y, w, h, fill, line=None, lw=0.5, dash=False)`, `card(s, x, y, w, h, fill=CARD)`, `eyebrow(s, x, y, w, t, color=GRAY, size=10.5, bold=True)`, `label_box(s, x, y, w, h, t, fill, color=WHITE, size=10.5, font=MONO, bold=True, rounded=True, align=C)`, `tok(s, x, y, t, kind, size=15, h=0.46) -> float`, `tokens(s, x, y, parts, size=15, h=0.46) -> (list[float], float)`, `stein(s, x, y, w, h, kind, t, tag=None, size=13)`, `schild(s, x, y, name, w=1.1)`, `turm(s, x, base, w, h, kind, werte)`, `arrow(s, x, y, w=0.5, h=0.32, color=GRAY)`, `down_arrow(s, x, y, w=0.32, h=0.45, color=GRAY)`, `connector(s, x0, y0, x1, y1, color=GRAY, width=1.5, dash=False)`, `vline(...)`, `outline(s, x, y, w, h, color=ORANGE, lw=2.25)`, `chip(s, x, y, t, w=None, fill=WHITE, size=10.5) -> float`, `numdot(s, x, y, n, fill=INK, d=0.36, size=12)`, `codebox(s, x, y, w, lines, size=13, h=None)`, `text_width(t, font, size, bold=False) -> float` (Zoll).
- Konstanten wie in „Globale Vorgaben“; `SANS`, `MONO` sind die Schriftlisten.

- [ ] **Schritt 1: Tests schreiben** (`unittest`):
  - `test_svg_wellformed`: `Canvas(4, 2)` mit je einem Aufruf jeder Zeichenfunktion → `xml.etree.ElementTree.fromstring(svg)` wirft nicht.
  - `test_viewbox`: `Canvas(8, 3).svg()` enthält `viewBox="0 0 768 288"`.
  - `test_stein_colors`: `stein(..., "num", "5")` erzeugt ein Rechteck mit `fill="#85B7EB"` und Text `5` in `#042C53`; `"na"` erzeugt `stroke-dasharray`.
  - `test_turm_order`: `turm(s, 0, 2, 1, 0.3, "num", ["a", "b"])` setzt `a` unten (größeres y) und `b` darüber; im Buch steht der erste Vektorwert oben, also ruft der Aufrufer `turm` mit umgekehrter Liste auf (wie auf den Folien).
  - `test_text_wraps`: ein Absatz von 200 Zeichen in 3 Zoll Breite ergibt mehrere `<tspan>`-Zeilen, keine breiter als 3 Zoll laut `text_width`.
  - `test_text_fits_fallback`: `text_width("Mittelwert", SANS, 12)` mit Arial-Breiten ≥ Messung mit Source-Sans-Breiten; Layout rechnet mit dem größeren Wert.
  - `test_min_font`: `R("x", size=9)` in einem Canvas → `Canvas.svg()` wirft `ValueError` (kleinste Schrift 10 pt).
- [ ] **Schritt 2:** `python3 -m unittest figuren/test_lego.py` → schlägt fehl (Modul fehlt).
- [ ] **Schritt 3:** `lego.py` umsetzen. Zeichenbreiten: Tabelle mittlerer Zeichenbreiten je Schrift (Arial für SANS, Consolas für MONO als breiteste Ausweichschriften), Zeilenumbruch wortweise.
- [ ] **Schritt 4:** Tests laufen grün.
- [ ] **Schritt 5:** Commit „Bausteine-Abbildungen: Zeichenbibliothek“.

### Task 2: Bau- und Prüfskripte

**Dateien:** neu `figuren/build.py`, `figuren/check_qmd.py`, `figuren/check_sections.py`, `figuren/README.md` (drei Sätze: wofür, wie bauen, wo der Vertrag steht).

**Schnittstellen:**
- Jedes Kapitelmodul `figuren/kapNN.py` hat `FIGUREN: dict[str, Callable[[], Canvas]]`, Schlüssel = Dateiname ohne Endung.
- `build.py [name ...]` schreibt alle (oder die genannten) Abbildungen nach `Bilder/figuren/` und gibt pro Datei eine Zeile aus.
- `check_qmd.py` prüft alle `0*.qmd`: jede Bildzeile mit `Bilder/figuren/` hat `#fig-…`, `.lightbox`, nicht leeres `fig-alt`, die Datei existiert, und `@fig-…` kommt im selben Kapitel vor. Exit-Code 1 bei Fehlern.
- `check_sections.py` vergleicht die nummerierten Abschnitte in `docs/0*.html` mit einem Referenzstand (`git show <ref>:docs/…`): Jede alte Nummer existiert noch und ihr Titel beginnt gleich. Exit-Code 1 bei Abweichung. Referenz ist der Commit „Phase 6w“ aus Task 0; das Skript findet ihn mit `git log --grep='Phase 6w' -1 --format=%H`, `--ref` überschreibt.

- [ ] **Schritt 1:** Test für `check_qmd.py` als `figuren/test_checks.py`: eine Beispieldatei ohne `fig-alt` ergibt Exit-Code 1, mit allem ergibt 0.
- [ ] **Schritt 2:** Skripte umsetzen; `python3 -m unittest figuren/test_checks.py` grün.
- [ ] **Schritt 3:** `python3 figuren/check_sections.py` auf dem Stand nach Task 0 → 0 Abweichungen.
- [ ] **Schritt 4:** Commit „Bausteine-Abbildungen: Bau- und Prüfskripte“.

### Task 3: Format „Kurz überlegen“ eintragen

**Dateien:** `STYLE.md` (§4 und neuer §12).

- [ ] **Schritt 1:** `STYLE.md` §4 bekommt den Eintrag **Kurz überlegen** (Form wie in „Globale Vorgaben“, höchstens eine pro Abschnitt, Frage zu einem neuen Fall, Auflösung ohne Bild). Neuer §12 „Abbildungen“ verweist auf `BILDER.md` als Vertrag.
- [ ] **Schritt 2:** Commit „STYLE.md: Kurz überlegen und Abbildungen“.

### Task 4: Pilot-Abbildungen Kap. 3

**Dateien:** neu `figuren/kap03.py`; `Bilder/figuren/k03-*.svg`.

Abbildungen und ihre Inhalte (Werte geprüft mit R 4.5.3):

| Datei | Steht bei | Zeigt |
| :-- | :-- | :-- |
| `k03-legende` | Anfang 3.5 | Legende: Stein (Wert), drei Farben (numeric/character/logical), leerer Stein (`NA`), Turm (Vektor), Bauplatte (Datensatz), Namensschild, Aufkleber (Wertelabel), Code-Farben Objekt/Funktion/Argument |
| `k03-turm` | Chunk `vectors` | drei Türme mit Namensschild: `zahlen` 1–5 (blau), `namen` "Anna", "Boris", "Carla" (lila), `flags` TRUE, FALSE, NA (rosa, NA leer); erster Wert oben |
| `k03-rangfolge` | neuer Chunk `coercion` nach `recycling`-Callout | Rangfolge logical → numeric → character; Beispiele `c(1, TRUE, FALSE)` → `1 1 0` (numeric) und `c(1, "Anna", TRUE)` → `"1" "Anna" "TRUE"` (character) |
| `k03-tibble` | Chunk `tibble-create` | Bauplatte `befragte`: Turm `geschlecht` (lila, `<fct>`: Mann, Frau, Mann, Divers), Turm `alter` (blau: 34, 41, 28, 52); eine Reihe markiert = ein Fall; `befragte$alter` holt einen Turm |
| `k03-pipe` | Chunk `pipe-native` | drei Schritte: Turm `zahlen` (1.11 … 1.55) → erstes Feld von `round( , digits = 1)` → 1.1 1.2 1.3 1.4 1.6 → erstes Feld von `head( , n = 3)` → 1.1 1.2 1.3 |

- [ ] **Schritt 1:** Werte prüfen: `Rscript -e 'zahlen <- c(1.11, 1.22, 1.33, 1.44, 1.55); print(round(zahlen, 1)); print(zahlen |> round(digits = 1) |> head(n = 3)); print(c(1, TRUE, FALSE)); print(c(1, "Anna", TRUE))'` → `1.1 1.2 1.3 1.4 1.6`, `1.1 1.2 1.3`, `1 1 0`, `"1" "Anna" "TRUE"`.
- [ ] **Schritt 2:** Test in `figuren/test_lego.py` ergänzen: `test_kap03_constraints` baut jede Abbildung aus `kap03.FIGUREN` und prüft Wohlgeformtheit, `viewBox`-Breite ≤ 768 und dass alle Werte aus der Tabelle oben als Text im SVG vorkommen.
- [ ] **Schritt 3:** `kap03.py` umsetzen; `python3 figuren/build.py` und Tests grün.
- [ ] **Schritt 4:** Jede SVG im Browser ansehen (Datei direkt öffnen): nichts überlappt, nichts läuft aus Kästen.

### Task 5: Pilot ins Buch, Durchsicht mit Yannick

**Dateien:** `03-ProgrammierspracheR.qmd`, `_freeze/03-…`, `docs/…`.

- [ ] **Schritt 1:** Am Anfang von 3.5 ein `.callout-note` „Hintergrund: Die Bildsprache dieses Buchs“ (drei bis vier Sätze) mit `@fig-legende`.
- [ ] **Schritt 2:** `k03-turm` nach Chunk `vectors`, ein bis zwei Einordnungssätze.
- [ ] **Schritt 3:** Neuer Chunk `coercion` (Code wie in Task 4) mit Lesart, `k03-rangfolge`, danach **Kurz überlegen.** „Was ergibt `c(TRUE, "ja")`?“ mit Auflösung: `"TRUE" "ja"`, character, weil Text alle anderen Typen aufnehmen kann.
- [ ] **Schritt 4:** `k03-tibble` nach Chunk `tibble-create`, ein Satz zu Reihe = Fall und `$`.
- [ ] **Schritt 5:** `k03-pipe` nach Chunk `pipe-native`, Satz zum ersten Feld; **Kurz überlegen.** „Wie schreibst du `sqrt(sum(c(9, 16)))` als Pipe?“ mit Auflösung `c(9, 16) |> sum() |> sqrt()` → `[1] 5`.
- [ ] **Schritt 6:** Rendern (`quarto render 03-ProgrammierspracheR.qmd`), dann `python3 figuren/check_qmd.py` und `python3 figuren/check_sections.py` → beide 0.
- [ ] **Schritt 7:** Im Browser (lokaler Server auf `docs/`) Kap. 3 bei voller Breite und bei 375 px ansehen, Abbildung antippen. Öffnet sich keine Lightbox, `lightbox: auto` unter `format: html` in `_quarto.yml` setzen, neu rendern und erneut prüfen; vorhandene ggplot-Abbildungen dürfen dadurch nicht anders aussehen.
- [ ] **Schritt 8:** Commit „Bausteine-Abbildungen: Pilot Kap. 3“.
- [ ] **Schritt 9: Halt.** Yannick sieht den Pilot im Browser an. Stil, Größe, Ton und das Format „Kurz überlegen“ werden hier bestätigt oder geändert; Änderungen fließen in `BILDER.md` und in die folgenden Tasks.

### Task 6: Rest von Kap. 3

Abbildungen Nr. 5, 6, 7, 8, 13, 15 aus `BILDER.md` §6 (`k03-name-inhalt` 3.2, `k03-reihenfolge` 3.2 mit neuem Chunk und Kurz überlegen, `k03-funktion` 3.3, `k03-argumente` 3.3 mit Kurz überlegen, `k03-na` 3.6, `k03-analyseplan` 3.7.3). Werte aus den Chunks `var1`, `fn-basics`, `grundfunktionen`, `na-basic`/`na-rm`, `real-pipe`.

- [ ] **Schritt 1:** Werte der Chunks mit `Rscript` ausgeben und notieren.
- [ ] **Schritt 2:** `test_kap03_constraints` um die neuen Werte erweitern; rot.
- [ ] **Schritt 3:** Abbildungen in `kap03.py`, bauen, Tests grün, SVGs im Browser ansehen.
- [ ] **Schritt 4:** Einbinden wie in Task 5; neuer Chunk in 3.2 für die Ausführungsreihenfolge (`x <- 5`, `y <- x + 2`, `x <- 10`, `y` → `[1] 7`); rendern; `check_qmd.py`, `check_sections.py` → 0; Browser.
- [ ] **Schritt 5:** Commit „Bausteine-Abbildungen: Kap. 3 vollständig“.

### Task 7: Kap. 4

Abbildungen Nr. 12, 16–24 (`k04-dollar-select` 4.5.1, `k04-einlesen` 4.3, `k04-platte` 4.4, `k04-select` 4.5.1, `k04-filter` 4.5.2, `k04-dbl-lbl` 4.6, `k04-to-label` 4.6.1, `k04-labels` 4.7, `k04-missing-codes` 4.8, `k04-set-na` 4.8). Werte aus den Chunks, neben denen das Bild steht (ALLBUS 2023, `ALLBUS2023.sav` im Projektordner). Kurz überlegen bei Nr. 12 und 23 laut `BILDER.md` §6.

- [ ] Schritte wie Task 6 (Werte mit `Rscript` ermitteln, Test-Werte ergänzen, `kap04.py`, einbinden, rendern, Prüfskripte, Browser), Commit „Bausteine-Abbildungen: Kap. 4“.

### Task 8: Kap. 5

Abbildungen Nr. 25–35 (`k05-*`, Abschnitte 5.2.1–5.9). Kurz überlegen bei Nr. 26, 31, 32.

- [ ] Schritte wie Task 6, Commit „Bausteine-Abbildungen: Kap. 5“.

### Task 9: Kap. 1, 2 und 7

Abbildungen Nr. 1–3 (`k01-oekosystem` 1.6, `k01-regal-werkbank` 1.6.2, `k02-qmd-schichten` 2.4) und Nr. 36–37 (`k07-gewichtung` 7.2 mit neuem Chunk `frequency(eastwest)` ungewichtet und mit `weights = wghtpew`, `k07-zeilenprozente` 7.5.1). Kap. 7 rechnet gewichtet: Werte aus den gerenderten Ausgaben übernehmen.

- [ ] Schritte wie Task 6, Commit „Bausteine-Abbildungen: Kap. 1, 2 und 7“.

### Task 10: Abschluss

- [ ] **Schritt 1:** `NEWS.md`-Eintrag (welche Kapitel Abbildungen bekommen haben, neues Format „Kurz überlegen“, `figuren/` zum Neubauen).
- [ ] **Schritt 2:** Ganzes Buch rendern; keine neuen Warnungen gegenüber dem Stand nach Task 0; `check_qmd.py` und `check_sections.py` → 0; `python3 -m unittest discover figuren` grün.
- [ ] **Schritt 3:** Alle Bildunterschriften und neuen Absätze einmal am Stück auf Slogans und Folienton lesen.
- [ ] **Schritt 4:** Commit „Bausteine-Abbildungen: NEWS und Abschluss“. Veröffentlichen nur nach Freigabe durch Yannick.
