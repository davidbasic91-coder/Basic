---
typ: index
kurz: Navigations- und Pflegeregeln der Werkstatt Didaktik für Claude.
quelle: []
status: belegt
entscheide:
- E-003
- E-004
- E-007
- E-035
- E-063
- E-071
- E-072
- E-197
- E-199
- E-205
verwandt: []
---

# CLAUDE.md: Werkstatt Didaktik

## Kurz

Navigations- und Pflegeregeln der Werkstatt Didaktik für Claude.

## Zweck

Didaktisches Wissen für Davids Unterricht an der BFS Basel (FaBe, BKU1 und BKU3, Kind und MmB) und seine EHB-Ausbildung. Deutsch, Schweizer «ss», Anführungszeichen «so». Dieser Vault ist die gültige Fassung des didaktischen Wissens; die Skills sind aufbereitetes Material dazu.

## Navigation: höchstens zwei Schritte

1. **Index lesen:** `Start.md` nennt die acht Bereichsindizes («Index …»). Oder direkt im Frontmatter suchen, zum Beispiel:
   - `grep -rl "^typ: methode" .`
   - `grep -rli "^kurz:.*sandwich" .`
   - `grep -rl -A3 "^aviva_phase:" "30 Methoden und Medien" | head`
2. **Frontmatter statt Volltext:** Zuerst `kurz` und die Felder lesen (etwa `head -30 Datei.md`); die ganze Notiz nur, wenn `kurz` passt.
3. Fachbücher nicht neu lesen, wenn eine Notiz mit `status: belegt` die Frage beantwortet. Seitenangaben stehen in `quelle`.

## Ordner

```
00 Start/     Vorlagen/, Bases/, Kontrolle/ (Protokoll, Befunde, Stand)
10 Lernende und Gruppen
20 Planung und didaktische Modelle
30 Methoden und Medien   (Methodensammlung/ mit 325 Methoden)
40 Aufgaben und Operatoren
50 Prüfen und Bewerten
60 Unterrichtsqualität und Reflexion
70 EHB-Qualifikation
80 Quellen               (Quellennotizen mit Pfad; PDFs liegen ausserhalb)
Start.md, CLAUDE.md, Brücke zum Tresor BFS.md
```

## Notiztypen (Feld `typ`)

| typ | wofür | Zusatzfelder |
|---|---|---|
| konzept | Theorie, Modell, Begriff | |
| verfahren | Vorgehen in Schritten | |
| methode | Unterrichtsmethode | nr, gruppe, aviva_phase, k_stufe, sozialform, dauer, eignung_fabe, herkunft (Ausnahme: die fünf Grossformen mit gruppe «Grossform AVIVA» tragen nur gruppe und aviva_phase, E-197) |
| aufgabentyp | Typ aus Davids Palette | nr, k_stufe, operatoren, aviva_phase, musterloesung |
| k-stufe | K1 bis K6 | stufe, bezeichnung |
| kriterium | Indikator oder Merkmal eines Rasters | raster, nummer, punkte_max, bezugssituation |
| vorgabe | verbindliche Regel (EHB, Prüfen) | gilt_fuer |
| quelle | Quelle mit Pfad | autor, titel, jahr, art, pfad, pfad_geprueft |
| index, kontrolle | Übersichten, Kontrollunterlagen | |

Pflichtfelder überall: `typ`, `kurz` (höchstens drei Sätze, gleich wie der erste Absatz im Abschnitt «Kurz»; weiterer Inhalt darf in diesem Abschnitt folgen, E-199), `quelle` (Autor, Titel, Seite), `status`, `entscheide`, `verwandt`. Optional `auslegung: true`, wenn die Notiz Auslegungen eines Skills enthält (im Text als «Auslegung» markiert).

## Belegregel

- `status: belegt` heisst: Die Primärfundstelle in `quelle` wurde geprüft (Kernbegriffe auf den angegebenen Seiten gefunden oder Wortlaut am Original gelesen). Das belegt die Fundstelle, nicht jeden Satz; Teile mit «laut Skill» sind nicht am Primärtext geprüft.
- `status: nicht geprüft`: nur aus Skills oder ohne erreichbare Primärquelle. Nur mit diesem Hinweis weitergeben oder vorher am Original prüfen.
- `status: sammlung`: Methode aus der Ideensammlung, Inhalt nicht am Original geprüft; vor dem Einsatz prüfen.
- `status: widerspruch`: Die Quellen widersprechen sich; beide Fassungen stehen in der Notiz. Nicht selbst auflösen, David entscheidet.
- Seitenzahlen sind Druckseiten; die Umrechnung zur PDF-Seite steht in der Quellennotiz.
- Nie aus dem Gedächtnis ergänzen. Was nicht belegt ist, als «nicht geprüft» ausweisen.

## Trennung zum Tresor BFS

Was nur für eine Lernsituation oder den FaBe-Stoff gilt, gehört in den Tresor (`~/Desktop/BFS/BFS`), nicht hierher. Lernziele, Leistungsziele mit K-Stufe, Fachbegriffe, QV-Material und Sonnenblick stehen dort; siehe [[Brücke zum Tresor BFS]]. Keine Daten von Lernenden in diesem Vault.

## Pflegeregeln

- Nichts ändern ohne Davids Freigabe; jede Änderung mit Entscheid-Nummer im Feld `entscheide` und im [[Entscheidungsprotokoll]].
- Neue Notiz: Vorlage aus `00 Start/Vorlagen/`, atomar (eine Sache), Frontmatter vollständig, Abschnitt «Kurz» zuerst.
- Wikilinks nur bei inhaltlicher Beziehung. Umbenennen und Verschieben nur in Obsidian, damit Links nachgeführt werden.
- Übersichten sind Obsidian Bases in `00 Start/Bases/`. Community-Plugins nur Claudian (Modus «normal», also mit Rückfrage), BRAT (E-035), Star NotebookLM und Native PowerPoint Doc Editor (E-205).
- Stil: Fliesstext, keine Gedankenstriche als Stilmittel, kein Mittelpunkt als Trennzeichen, Schweizer «ss».
- Widersprüche und Lücken in die [[Befundliste]], nicht still korrigieren.
- Basic Skills (Webseite, https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV): nach Änderungen im Vault neu erzeugen mit `python3 "00 Start/Navigator/navigator.py" . <Ausgabe.html> --fonts "00 Start/Navigator/Schriften"` und an dieselbe Adresse veröffentlichen, ohne Rückfrage (Davids ständige Freigabe, E-167). Die Schriften dort sind die aus der veröffentlichten Seite herausgelösten Teilschriften von TeX Gyre Adventor (16.10.2026); sie decken alle damals im Vault benutzten Zeichen ab; ist fonttools installiert, verkleinert das Skript die Schriften, und die Artikeladressen entstehen aus dem Namen (E-073); die Knotentexte stehen in «00 Start/Navigator/Verbindungstexte.md» (E-071). Auf der Seite entfernt das Skript alle Verweise auf Claude, Skills und KI-Werkzeuge; im Vault bleiben die Herkunftsangaben (E-072). Neue Formulierungen im Vault brauchen manchmal neue Ersatzeinträge in navigator.py; vor dem Veröffentlichen die erzeugte Seite nach «Skill», «Claude» und Ablageangaben durchsuchen (E-169).
