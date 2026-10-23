---
typ: kontrolle
kurz: Neun mechanische Prüfungen für den Vault. Sieben davon sind an einem bekannt falschen Eingang rot und an einem korrekten grün geworden; quellen.py und die Tabellenskripte erzeugen nur Übersichten.
quelle:
- Werkzeugaufrufe der Arbeitssitzung vom 07.10.2026
status: belegt
entscheide:
- E-090
- E-123
- E-130
- E-166
verwandt:
- "[[Befundliste]]"
- "[[Entscheidungsprotokoll]]"
- "[[Einstiegsfrage prüfen]]"
- "[[Operatoren und K-Stufen]]"
---

## Kurz

Neun mechanische Prüfungen für den Vault. Sieben davon sind an einem bekannt falschen Eingang rot und an einem korrekten grün geworden; quellen.py und die Tabellenskripte erzeugen nur Übersichten.

## Aufruf

Alle Skripte liegen in diesem Ordner und werden von hier aus aufgerufen:

```
cd "00 Start/Prüfungen"
python3 <skript>.py
```

Exit 0 heisst keine Befunde, Exit 1 Befunde, Exit 2 die Prüfung selbst ist nicht lauffähig, etwa weil eine Quelldatei fehlt.

Den Skillordner suchen die Skripte selbst: den neusten installierten Stand des Plugins unterrichten, weil der Ordnername bei jedem Sync wechselt (E-166). Fehlt er, melden sie Exit 2.

## Die neun Prüfungen

| Skript | prüft | Exit am 16.10.2026 | warum |
|---|---|---|---|
| `quellen.py` | liest die Operatorenzuordnungen aus sechs Quellen und gibt sie als JSON aus | 0 | Datengrundlage, kein Urteil |
| `raster_proben.py` | das Fragetyp-Raster an sechzehn Proben, davon acht echte Dossierfragen | 0 | Raster stimmt |
| `lk1_abgleich.py` | die Zeilen «Lehren kompakt 1, S. 70» in den sechs K-Stufen-Notizen gegen das Original | 0 | seit E-085 bereinigt |
| `abschrift_check.py` | die Skill-Abschrift der Palette gegen das Original-PDF | 1 | K6-Zeile im Skill, E-084 betrifft nur den Vault; der Skillumbau steht noch aus |
| `operatoren_check.py` | die Notizen in «40 Aufgaben und Operatoren» gegen die Palette | 1 | die zwölf fehlenden und sieben mehrdeutigen Operatoren (E-083) sind im Vault beschlossen, im Skill noch nicht eingetragen |
| `fragecheck.py` | Einstiegs- und Ergebnissicherungsfragen der Arbeitsdossiers | 1 | sieben Fragen zu hoch, acht Dossiers nicht prüfbar |
| `slp_check.py` | Lernziele des Schullehrplans gegen die Leistungsziele des Bildungsplans | 1 | vierzig Fälle, siehe [[Rangfolge Bildungsplan und Schullehrplan]] |
| `methoden_pruefung.py` | sechs Prüfarten über die 327 Methoden | 1 | Duplikate, Eignungsskala und Synchronität offen |
| `tabelle.py`, `md_tabelle.py` | erzeugen die Vergleichstabelle der Operatoren | 0 | Hilfsskripte |

## Gegenproben

Eine Prüfung, die noch nie rot war, ist unbelegt. Darum sind die sieben urteilenden Prüfungen an einem absichtlich beschädigten Eingang geprüft:

| Prüfung | rot geworden bei | wieder grün bei |
|---|---|---|
| `operatoren_check.py` | vier eingebaute Schäden (erfundener Operator, falsche K-Stufe, Fliesstext gegen Frontmatter, falsche Typennummer), alle vier gefunden | Ausnahmedatei mit den quittierten Istbefunden |
| `abschrift_check.py` | zwei eingebaute Schäden in der Abschrift | Abschrift auf dem Originalstand |
| `lk1_abgleich.py` | zehn nicht belegte Operatoren im Istzustand | Notizen auf dem Originalbestand |
| `raster_proben.py` | nach Entfernen eines Bewertungsmusters ein Fehlurteil | vollständiges Raster |
| `fragecheck.py` | alte Fassung von LS 2.04 mit fünf Bewertungsfragen | LS 2.01 und LS 1.02 einzeln |
| `slp_check.py` | Istzustand, vierzig Fälle | BiP-Ziel von LS 1.02 künstlich auf K3 gehoben, Fall verschwindet |
| `methoden_pruefung.py` | vier eingebaute Schäden (K6, erfundene Eignungsstufe, wortgleiche Dublette, Zielverb über der Bloom-Stufe), alle vier gefunden | Ausnahmedatei mit 237 quittierten Istbefunden |
| Pfadsuche der Skripte (E-166) | künstlicher Pluginordner ohne Skilldateien: Exit 2 bei operatoren_check, slp_check, methoden_pruefung und abschrift_check; von zwei künstlichen Ständen wird der höhere gewählt | installierter Stand 0.16.1 |

Fehlende Quelldateien ergeben überall Exit 2 mit Klartextmeldung, nicht Exit 0.

## Was die Prüfungen nicht können

- `fragecheck.py` kann acht Dossiers (LS 2.11 bis 2.18) nicht beurteilen, weil sie keine Teilstruktur und keine K-Stufen tragen. Die Prüfung meldet das als eigenen Befund, statt sie zu überspringen.
- `methoden_pruefung.py lsstufe` meldet bei Abstand 1 vierhundertfünfundfünfzig Fälle und ist dann als Gate unbrauchbar; die Schwelle liegt darum bei zwei Stufen.
- Keine Prüfung ersetzt die Sichtkontrolle an gerenderten Word-Dateien.

## Entscheid David (E-090, 07.10.2026)

Die Prüfungen kommen in den Vault. Vorbild für den Ort ist «00 Start/Navigator/navigator.py». Befund B-061.
