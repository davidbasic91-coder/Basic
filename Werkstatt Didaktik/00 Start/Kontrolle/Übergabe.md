---
typ: kontrolle
kurz: 'Übergabe für die nächste Sitzung nach der Neuausrichtung vom 29.09.2026: Einstieg, Quellen, offene Etappen, Arbeitsregeln und Prompt.'
quelle:
- Entscheidungsprotokoll E-058 bis E-069
status: belegt
entscheide:
- E-065
- E-111
- E-158
- E-168
- E-171
- E-172
- E-182
- E-186
- E-190
- E-201
verwandt: []
---

## Kurz

Übergabe für die nächste Sitzung nach der Neuausrichtung vom 29.09.2026: Einstieg, Quellen, offene Etappen, Arbeitsregeln und Prompt.

## Einstieg

In dieser Reihenfolge lesen: [[CLAUDE]], [[Start]], [[Arbeitsplan]], [[Stand]]. Nachschlagen bei Bedarf: [[Entscheidungsprotokoll]] (besonders E-058 bis E-069, E-110 bis E-112 und E-122 bis E-203) und [[Befundliste]].

## Quellen und Pfade

- iCloud-Ordner «Studienskripte Didaktik» (`~/Library/Mobile Documents/com~apple~CloudDocs/Studienskripte Didaktik`): Studienskripte (als Beleg zugelassen, E-039) und Kopien der PDFs AVIVA-Buch Teil 1, Teil 2, Anhang, AVIVA-Kurzinformation, Lehren und Lernen Kap. 12, bpb Methoden-Kiste.
- Tresor: `~/Desktop/BFS/BFS` (eigene CLAUDE.md und Belegregel; Rohquellen nur lesen).
- Primärquellen für Etappe 3 und Skill-Quellen für Etappe 4 unter `~/Desktop/BFS` (EHB, Unterrichtsplanung/Didaktische Dokumente, Didaktik Skills); Pfade in [[Index Quellen]]. Der Ordner muss in der Sitzung verbunden sein.
- PDF-Text: `pdftotext -layout`; Druckseiten aus den Kopfzeilen lesen, nicht PDF-Seiten.

## Offen

Etappe 3 für die Ordner 40 und 20 ist die nächste Etappe, Ordner 40 zuerst (E-201); 70 und 50 sind erledigt, die übrigen entfallen nach E-186. Offen bleibt Etappe 8 (Skillumbau) im [[Arbeitsplan]]. Die [[Befundliste]] hat keine offenen Befunde (Stand 22.10.2026).

## Arbeitsregeln

- Davids Regeln zum Entscheidungsrecht gelten: offene Punkte in einer Runde vorlegen, erst nach «mach» bauen. David will möglichst eine Frage aufs Mal, kurz, mit Empfehlung.
- Umfang und Anzahl Durchgänge vor jeder Etappe schätzen und nennen.
- Die Methodensammlung ist eine Ideensammlung (E-059): keine Prüfung am Original, ausser David wählt eine Methode für eine Lektion.
- Ändern sich aviva_phase oder k_stufe einer Notiz, das Feld verwandt nachführen (E-052).
- Web nur mit WebFetch. Verweigert WebFetch den Wortlaut oder meldet eine Sperre: anhalten und David fragen, nie mit curl oder Python ausweichen. Nie persönliche Daten in Anfragen an fremde Dienste.
- Keine Sicherungskopien, Hilfsdateien am Schluss löschen.
- Nach jeder Änderung im Vault Basic Skills neu erzeugen und an dieselbe Adresse veröffentlichen (ständige Freigabe E-167); Aufruf in der CLAUDE.md des Vaults.
- Obsidian per Bildschirmsteuerung: Dateien über «Schnell öffnen» (cmd+O); Öffnen einer Base schreibt die Datei neu (nur Anführungszeichen, Inhalt gleich).

## Prompt zum Weiterarbeiten

```
Wir arbeiten an meinem Obsidian-Vault «Werkstatt Didaktik» weiter (~/Desktop/BFS/Werkstatt Didaktik). Lies zuerst die CLAUDE.md des Vaults, dann in «00 Start/Kontrolle» die Notizen Übergabe, Arbeitsplan und Stand. Meine Regeln zum Entscheidungsrecht gelten.

Heute: Etappe [Nummer] aus dem Arbeitsplan. Prüf zuerst Material und Zugriff, schätz Umfang und Durchgänge und leg mir die offenen Punkte vor, eine Frage aufs Mal, kurz, mit Empfehlung. Gebaut wird erst nach meinem «mach».
```
