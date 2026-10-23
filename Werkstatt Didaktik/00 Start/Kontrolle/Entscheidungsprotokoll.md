---
typ: kontrolle
kurz: 'E-001 bis E-033: Entscheide, die Claude beim Aufbau anstelle von David getroffen hat und die David mit E-066 bestätigt hat; ab E-034 Davids eigene Entscheide. Je mit Optionen, Wahl, Begründung, betroffenen Notizen und Weg zurück.'
quelle:
- Werkzeugaufrufe dieser Arbeitssitzung (28.09.2026)
status: belegt
entscheide:
- E-061
- E-088
- E-111
verwandt: []
---

## Kurz

E-001 bis E-033: Entscheide, die Claude beim Aufbau anstelle von David getroffen hat und die David mit E-066 bestätigt hat; ab E-034 Davids eigene Entscheide. Je mit Optionen, Wahl, Begründung, betroffenen Notizen und Weg zurück.

## E-001 Welcher Stand der Plugin-Quellen gilt?

**Optionen:**
1. Ordner Didaktik Skills im verbundenen Ordner BFS
2. Installierte Plugins unter ~/.claude/plugins/marketplaces/local-desktop-app-uploads/
3. Beide vergleichen

**Wahl:** Didaktik Skills (unterrichten 0.16.0, lernkontrollen 0.2.9, qualifizierter-unterrichtsbesuch 0.3.3, fachliteratur 0.3.3)

**Begründung:** Der Pfad unter ~/.claude ist in dieser Sitzung nicht verbunden und nicht erreichbar; die Kopie der Plugins in Claudes Arbeitsumgebung trägt tiefere Versionen (unterrichten 0.14.1, fachliteratur 0.3.2). Didaktik Skills ist der neuste erreichbare Stand.

**Betroffen:** alle Notizen mit Quelle «Skill …»

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Notizen gegen den Plugin-Stand unter ~/.claude neu abgleichen, sobald der Ordner verbunden ist.

## E-002 Welche Primärtexte werden zur Prüfung herangezogen?

**Optionen:**
1. nur Skill-Referenzen und deren wortgetreue Abschriften
2. zusätzlich die Buch- und Dokument-PDFs in BFS/EHB, BFS/Unterrichtsplanung/Didaktische Dokumente, BFS/Didaktische Dokumente und BFS/3. BFS Megastarters

**Wahl:** zusätzlich die PDFs, nur lesend, Textebene per pdftotext in /tmp der Mac-Shell

**Begründung:** Der Auftrag nennt die Fachbücher als Primärquelle. Die PDFs liegen im verbundenen Ordner und haben eine Textebene; damit lassen sich Seitenangaben prüfen. Die Buch-PDFs des fachliteratur-Registers unter ~/Documents sind nicht erreichbar.

**Betroffen:** alle Notizen mit status belegt

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Status aller Notizen auf «nicht geprüft» setzen und nur die Skill-Referenzen gelten lassen.

## E-003 Was heisst status belegt?

**Optionen:**
1. belegt = Aussage steht in einer gelesenen Quelle (auch Skill-Referenz)
2. belegt = Fundstelle am Primärtext geprüft
3. belegt = jede Aussage einzeln am Primärtext geprüft

**Wahl:** belegt = die in «quelle» genannte Primärfundstelle wurde in dieser Sitzung geprüft: die Kernbegriffe der Notiz stehen auf den angegebenen Seiten (maschinell gesucht) oder der Wortlaut wurde am Originaldokument gelesen. Die Paraphrase stammt meist aus der Skill-Referenz. Auslegungen (etwa Stufenbeschreibungen der qub-Skills) sind im Text als «Auslegung» markiert und tragen das Feld auslegung: true. Nur aus Skills übernommene Teile sind im Text mit «laut Skill» gekennzeichnet.

**Begründung:** Die erste Option wäre zu weich, die dritte in einem Durchlauf nicht leistbar. Die gewählte Definition ist nachprüfbar und ehrlich über ihre Grenze: Sie belegt die Fundstelle, nicht jeden Satz. Die Stichproben dienen der Tiefenprüfung.

**Betroffen:** alle Notizen

**Notizen mit diesem Entscheid im Frontmatter:** [[Bewertungsskala EHB-Raster]], [[CLAUDE]], [[Stufe N nicht beobachtbar]]

**Rückgängig:** Definition in CLAUDE.md ändern und den Status neu setzen lassen.

## E-004 Wo liegen Startnotiz und CLAUDE.md?

**Optionen:**
1. im Wurzelordner (Bauprinzip 5)
2. in 00 Start (Ordnervorschlag)

**Wahl:** im Wurzelordner; 00 Start enthält nur Vorlagen, Bases und Kontrolle

**Begründung:** Der Auftrag widerspricht sich hier. Claude Code liest CLAUDE.md automatisch aus dem Wurzelordner, darum dort.

**Betroffen:** Start.md, CLAUDE.md

**Notizen mit diesem Entscheid im Frontmatter:** [[CLAUDE]], [[Start]]

**Rückgängig:** Beide Dateien nach 00 Start verschieben (in Obsidian, damit Links nachgeführt werden).

## E-005 Ordner 10: «Lerntheorien» oder anders?

**Optionen:**
1. 10 Lerntheorien wie vorgeschlagen
2. 10 Lernende und Gruppen

**Wahl:** 10 Lernende und Gruppen

**Begründung:** Das Material enthält keine klassischen Lerntheorien (Behaviorismus, Kognitivismus, Konstruktivismus als Theorien), sondern Erwachsenenlernen, Gedächtnis, Lernstile, Motivation, Rückmeldung, Gruppenphasen, Konflikte. Der Name folgt dem Material.

**Betroffen:** 10 Lernende und Gruppen/

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Ordner umbenennen; Links passt Obsidian an.

## E-006 Ordnernamen 20 und 30

**Optionen:**
1. 20 Didaktische Modelle und Planung / 30 Methoden
2. 20 Planung und didaktische Modelle / 30 Methoden und Medien

**Wahl:** 20 Planung und didaktische Modelle, 30 Methoden und Medien

**Begründung:** Planung ist der grösste Teil von 20; Medien (Katalog Nr. 97 bis 106, Lehren kompakt Kap. 9, Medienwahl) gehören zu den Methoden.

**Betroffen:** 20 Planung und didaktische Modelle/, 30 Methoden und Medien/

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Ordner umbenennen.

## E-007 Welche Notiztypen?

**Optionen:**
1. wenige breite Typen
2. Typen je Quelle
3. Typen nach Funktion: konzept, verfahren, methode, aufgabentyp, k-stufe, kriterium, vorgabe, quelle, index, kontrolle, vorlage

**Wahl:** Typen nach Funktion

**Begründung:** Die Funktion entscheidet, was Claude mit der Notiz tut: ein Konzept erklären, ein Verfahren anwenden, ein Kriterium prüfen, eine Vorgabe einhalten. Das hält die Suche kurz.

**Betroffen:** alle Notizen, CLAUDE.md

**Notizen mit diesem Entscheid im Frontmatter:** [[CLAUDE]]

**Rückgängig:** Feld typ per Suchen und Ersetzen umbenennen.

## E-008 Welche typspezifischen Felder?

**Optionen:**
1. nur Pflichtfelder
2. Pflichtfelder plus wenige Suchfelder je Typ
3. alle denkbaren Felder, auch leer

**Wahl:** Pflichtfelder plus Suchfelder: methode (nr, gruppe, aviva_phase, k_stufe, sozialform, dauer, eignung_fabe, herkunft); aufgabentyp (nr, k_stufe, operatoren, aviva_phase, musterloesung); k-stufe (stufe, bezeichnung); kriterium (raster, nummer, punkte_max, bezugssituation); vorgabe (gilt_fuer, wo vorhanden); auslegung wo zutreffend

**Begründung:** Nur Felder, die das Material wirklich füllt. gruppengroesse wurde nicht angelegt: keine Quelle nennt Gruppengrössen je Methode.

**Betroffen:** alle Notizen

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Felder in Vorlagen und per Skript ergänzen oder entfernen.

## E-009 EHB-Indikatoren: eine Notiz je Indikator oder je Raster?

**Optionen:**
1. eine Notiz je Raster
2. eine Notiz je Indikator (29)

**Wahl:** eine Notiz je Indikator; Leistungsnachweise mit wenigen binären Kriterien je eine Notiz mit Kriterien im Text

**Begründung:** Jeder Indikator trägt vier Punkte und hat eigene Stufen, Prüffragen und Stolpersteine; so findet Claude ihn in zwei Schritten. Die binären Kriterien der Leistungsnachweise sind zu klein für eigene Notizen.

**Betroffen:** 70 EHB-Qualifikation/

**Notizen mit diesem Entscheid im Frontmatter:** 30 Notizen, abrufbar in [[Alle Notizen.base]] (Spalte entscheide)

**Rückgängig:** Indikatornotizen je Raster zusammenführen.

## E-010 Wortlaut der Indikatoren und Leitfragen: zitieren oder paraphrasieren?

**Optionen:**
1. paraphrasieren (Bauprinzip 7)
2. wörtlich, weil prüfungsrelevante Vorgabe

**Wahl:** wörtlich, mit Seitenangabe; Leitfragen teilweise leicht gekürzt

**Begründung:** Punkte werden am Wortlaut vergeben; eine Paraphrase würde genau das verfälschen, worauf es ankommt. Abweichung von Bauprinzip 7.

**Betroffen:** Indikatornotizen, Leitfragen Fachgespräch, Modelllektion

**Notizen mit diesem Entscheid im Frontmatter:** 30 Notizen, abrufbar in [[Alle Notizen.base]] (Spalte entscheide)

**Rückgängig:** Wortlaut durch Paraphrase ersetzen.

## E-011 Beispiele aus dem Musterdossier eines Mitstudierenden übernehmen?

**Optionen:**
1. übernehmen wie im Skill
2. weglassen, nur die Gliederung übernehmen

**Wahl:** weglassen

**Begründung:** Die Beispiele betreffen die Arbeit einer Drittperson und Angaben zu deren Lernenden (etwa Nachteilsausgleich). Daten von Lernenden gehören nicht in den Vault; die Gliederung ist ohne sie brauchbar.

**Betroffen:** Gliederung Vorbereitungsdossier, Vorbereitung 01 bis 12

**Notizen mit diesem Entscheid im Frontmatter:** [[Gliederung Vorbereitungsdossier]]

**Rückgängig:** Beispiele aus qub-dossier/references/musterdossier.md nachtragen.

## E-012 Leistungsnachweise der Wegleitung aufnehmen, obwohl die Skills sie nicht behandeln?

**Optionen:**
1. nur was die Skills behandeln
2. alle Leistungsnachweise aus der Wegleitung

**Wahl:** alle, mit Kriterien im Wortlaut der Wegleitung

**Begründung:** Sie gehören zur EHB-Qualifikation, stehen im Primärdokument und sind vollständig prüfbar.

**Betroffen:** Standortbestimmung, Unterrichtsbesuche, Modelllektion, Fallstudie KOPING, Lernzuwachs, Portfolio

**Notizen mit diesem Entscheid im Frontmatter:** [[Fallstudie KOPING]], [[Modelllektion]], [[Portfolio Basismodul A]], [[Qualifikationsverfahren Basismodul A]], [[Reflexion persönlicher Lernzuwachs]], [[Standortbestimmung und Zielvereinbarung]], [[Unterrichtsbesuch bei erfahrener Lehrperson]], [[Unterrichtsbesuch durch Lehrbegleitung]]

**Rückgängig:** Notizen löschen.

## E-013 Methodensammlung: wie viele Notizen?

**Optionen:**
1. eine Sammelnotiz mit Tabelle
2. eine Notiz je Methode (330) per Skript
3. nur Methoden mit Eignung hoch

**Wahl:** eine Notiz je Methode, alle 330, per Skript aus den Referenzdateien

**Begründung:** Atomar und über die Felder filterbar; die Auswahl nach Eignung ist Davids Entscheid im Einzelfall. Status durchgehend «nicht geprüft», weil die Ursprungsquellen Web-Seiten sind und kein Web-Zugriff besteht.

**Betroffen:** 30 Methoden und Medien/Methodensammlung/

**Notizen mit diesem Entscheid im Frontmatter:** 331 Notizen, abrufbar in [[Alle Notizen.base]] (Spalte entscheide)

**Rückgängig:** Ordner Methodensammlung löschen und durch eine Sammelnotiz ersetzen.

## E-014 Pfade der Buch-PDFs aus dem fachliteratur-Register

**Optionen:**
1. Registerpfad ~/Documents/Claude/Projects/fachliteratur/books/ angeben
2. nur geprüfte Pfade im verbundenen Ordner angeben

**Wahl:** beide angeben, mit Feld pfad_geprueft

**Begründung:** Der Registerpfad liegt ausserhalb der verbundenen Ordner und liess sich nicht prüfen; die gefundenen Exemplare im Ordner BFS sind geprüft.

**Betroffen:** 80 Quellen/

**Notizen mit diesem Entscheid im Frontmatter:** 17 Notizen, abrufbar in [[Alle Notizen.base]] (Spalte entscheide)

**Rückgängig:** Pfade in den Quellennotizen anpassen.

## E-015 Dokumente im Ordner EHB, die nicht zu den genannten Quellen gehören (AUL-E-Skript SVEB, Dossier didaktische Starthilfe, Davids Selbststudium-Dossiers, bpb Methoden-Kiste, Fehrmann 2019)

**Optionen:**
1. auswerten
2. nur als Quellennotiz mit Pfad erfassen, nicht auswerten

**Wahl:** nur erfassen, nicht auswerten

**Begründung:** Der Auftrag begrenzt die Quellen auf die Plugins und das Register. Die Dokumente sind in Stand.md als möglicher nächster Schritt vermerkt.

**Betroffen:** 80 Quellen/

**Notizen mit diesem Entscheid im Frontmatter:** 17 Notizen, abrufbar in [[Alle Notizen.base]] (Spalte entscheide)

**Rückgängig:** Dokumente in einem weiteren Durchlauf auswerten.

## E-016 Welches Exemplar von «Was ist guter Unterricht?» gilt für Seitenangaben?

**Optionen:**
1. EHB/Was ist guter Unterricht.pdf
2. Unterrichtsplanung/Didaktische Dokumente/Hilbert.pdf

**Wahl:** EHB/Was ist guter Unterricht.pdf (Druckseite = PDF-Seite minus 2)

**Begründung:** Beide Dateien enthalten dasselbe Buch mit unterschiedlicher Seitenzählung; die Seitenangaben des Skills guter-unterricht passen zum EHB-Exemplar.

**Betroffen:** alle Notizen mit Quelle Meyer 2024

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Seitenangaben gegen das andere Exemplar umrechnen.

## E-017 Dateinamen der Notizen

**Optionen:**
1. sprechende Titel
2. Nummernpräfixe überall

**Wahl:** sprechende deutsche Titel; Nummern nur, wo die Quelle sie führt (EHB-Indikatoren, Meyer-Merkmale, Aufgabentypen)

**Begründung:** Wikilinks bleiben lesbar; Nummern helfen dort, wo man nach Nummer sucht. Kollisionen zwischen Methodenkatalog und anderen Notizen erhalten den Zusatz «(Methode)».

**Betroffen:** alle Notizen

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** In Obsidian umbenennen.

## E-018 Widersprüchliche Zuordnung von Operatoren zu K-Stufen

**Optionen:**
1. Liste des Skills aufgabentypen als gültig setzen
2. Widerspruch offen ausweisen

**Wahl:** offen ausweisen; K-Stufen-Notizen und Aufgabentypen mit Spanne tragen status widerspruch

**Begründung:** Vorgabe des Auftrags: Widersprüche nicht auflösen. Die Regel der Skills (für Lernkontrollen gilt aufgabentypen) ist als Regel der Skills vermerkt, nicht als Auflösung.

**Betroffen:** 40 Aufgaben und Operatoren/

**Notizen mit diesem Entscheid im Frontmatter:** [[Aufgabentyp 03 Multiple-Choice mit Begründung]], [[Aufgabentyp 06 Vergleichsauftrag]], [[Aufgabentyp 09 Recherche- oder Erkundungsauftrag]], [[Aufgabentyp 14 Peer-Feedback-Aufgabe]], [[Aufgabentyp 17 Portfolioaufgabe]], [[Aufgabentyp 18 Stationenlernen oder Postenlauf]], [[K-Stufen im Überblick]], [[K1 Wissen]], [[K2 Verstehen]], [[K3 Anwenden]], [[K4 Analysieren]], [[K5 Synthese oder Entwickeln]], [[K6 Bewerten oder Beurteilen]], [[Operatoren und K-Stufen]], [[Widerspruch Eine Aufgabe eine K-Stufe]]

**Rückgängig:** Nach Davids Entscheid eine Fassung als gültig markieren und den Status ändern.

## E-019 Beispielaufgaben der Aufgabentypen enthalten FaBe-Themen: übernehmen?

**Optionen:**
1. übernehmen
2. weglassen, weil FaBe-Fachinhalt

**Wahl:** übernehmen (Grenzfall)

**Begründung:** Die Beispiele zeigen, wie ein Typ aussieht; sie vermitteln keinen Fachinhalt. Ohne Beispiel verliert die Notiz ihren Zweck.

**Betroffen:** Aufgabentyp 01 bis 19

**Notizen mit diesem Entscheid im Frontmatter:** 20 Notizen, abrufbar in [[Alle Notizen.base]] (Spalte entscheide)

**Rückgängig:** Abschnitt «Beispielaufgabe» per Skript entfernen.

## E-020 Widerspruch Wiederholung (zweimal oder einmal)

**Optionen:**
1. Wegleitung gilt
2. offen ausweisen

**Wahl:** offen ausweisen

**Begründung:** Vorgabe des Auftrags.

**Betroffen:** Wiederholung ungenügender Kompetenznachweise

**Notizen mit diesem Entscheid im Frontmatter:** [[Wiederholung ungenügender Kompetenznachweise]]

**Rückgängig:** nach Klärung mit der Kursleitung Status ändern.

## E-021 Faustregel «Note = Durchschnittsstufe × 1,25 + 1» aufnehmen?

**Optionen:**
1. nur die Formel der Wegleitung
2. Formel plus nachgerechnete Faustregel

**Wahl:** Formel plus Faustregel, als nachgerechnet gekennzeichnet

**Begründung:** Die Faustregel folgt mathematisch aus der Formel bei vier Punkten je Indikator (5/4 = 1,25) und wurde nachgerechnet.

**Betroffen:** Notenformel EHB-Kompetenznachweise

**Notizen mit diesem Entscheid im Frontmatter:** [[Notenformel EHB-Kompetenznachweise]]

**Rückgängig:** Abschnitt «Folgerungen» löschen.

## E-022 Felder der Methodennotizen per Skript aus dem Freitext lesen?

**Optionen:**
1. Felder leer lassen
2. per Skript aus WANN, WER, Bloom-Passung und Eignung lesen

**Wahl:** per Skript: aviva_phase aus Schlüsselwörtern in WANN, k_stufe aus «Kx bis Ky», sozialform aus Schlüsselwörtern in WER, eignung_fabe aus dem ersten Wort; «Tief» und «Gering» vereinheitlicht zu «gering»

**Begründung:** Ohne Felder ist die Sammlung nicht filterbar. Das Lesen ist mechanisch und kann einzelne Werte verfehlen (vier Methoden ohne Phase, 13 ohne Sozialform); im Zweifel gilt der Text. Die Vereinheitlichung folgt dem Hinweis im Skill, beide Wörter meinten dasselbe.

**Betroffen:** 30 Methoden und Medien/Methodensammlung/

**Notizen mit diesem Entscheid im Frontmatter:** 331 Notizen, abrufbar in [[Alle Notizen.base]] (Spalte entscheide)

**Rückgängig:** Felder per Skript leeren oder anders zuordnen.

## E-023 Arbeitsauftrag: EHB-Fassung (vier Elemente) oder Kursmaterial (sechs Bestandteile)?

**Optionen:**
1. eine Fassung wählen
2. beide nebeneinander

**Wahl:** beide nebeneinander, EHB zuerst

**Begründung:** Die EHB-Fassung ist prüfungsrelevant, die Fassung des Kursmaterials ausführlicher; sie widersprechen sich nicht.

**Betroffen:** Arbeitsauftrag formulieren

**Notizen mit diesem Entscheid im Frontmatter:** [[Arbeitsauftrag formulieren]]

**Rückgängig:** eine Fassung streichen.

## E-024 Davids eigene Verfahren (Lernzielkette, Beziehungstypen, Leitfragen-Klammer): welche Quelle ist primär?

**Optionen:**
1. Skill gilt als aufbereitetes Material, status nicht geprüft
2. Skill gilt als Primärquelle, weil David der Urheber ist

**Wahl:** Skill als Primärquelle, status belegt

**Begründung:** Die Verfahren haben keine andere Quelle als Davids Festhalten im Skill.

**Betroffen:** Lernzielkette einer Lernsituation, Beziehungstypen zwischen Lernzielen, Leitfragen-Klammer zur Ergebnissicherung

**Notizen mit diesem Entscheid im Frontmatter:** [[Beziehungstypen zwischen Lernzielen]], [[Leitfragen-Klammer zur Ergebnissicherung]], [[Lernzielkette einer Lernsituation]]

**Rückgängig:** Status auf nicht geprüft setzen.

## E-025 Begriffs- und Zahlenwidersprüche zwischen Büchern (didaktische Analyse, Zielarten, Inputdauer)

**Optionen:**
1. eine Fassung wählen
2. eigene Widerspruchsnotiz oder Status widerspruch

**Wahl:** Status widerspruch in der betroffenen Notiz; bei der Inputdauer eine eigene Notiz

**Begründung:** Vorgabe des Auftrags. Die Inputdauer betrifft mehrere Notizen, darum eine eigene.

**Betroffen:** Didaktische Analyse, Zielarten Leitziel Richtziel Leistungsziel, Dauer von Inputphasen

**Notizen mit diesem Entscheid im Frontmatter:** [[Dauer von Inputphasen]], [[Didaktische Analyse]], [[Zielarten Leitziel Richtziel Leistungsziel]]

**Rückgängig:** nach Davids Entscheid Status ändern.

## E-026 Grenzfälle zum Tresor: Kommunikation, Feedback, Gruppenphasen, Konflikte, rechtliche Grundlagen

**Optionen:**
1. ganz in den Tresor verweisen
2. in der Werkstatt aus Sicht der Lehrperson behandeln, Fachinhalt im Tresor lassen

**Wahl:** Werkstatt behandelt das Handeln der Lehrperson in der eigenen Klasse (Lehren kompakt 1); der FaBe-Fachinhalt (Tuckman, Glasl, Kommunikationsquadrat, Ich-Botschaft, aktives Zuhören als Begriff) bleibt im Tresor und wird über die Brückennotiz erreicht

**Begründung:** Beide Blickwinkel sind nötig: der Unterrichtsstoff für die Lernenden und das Führungshandeln der Lehrperson. Überschneidungen im Wortlaut sind vermieden, nicht aber im Thema.

**Betroffen:** Kommunikation im Unterricht, Feedback und Kritik, Gruppenphasen, Konflikte in Lerngruppen bearbeiten, Rechtliche Grundlagen des Prüfens

**Notizen mit diesem Entscheid im Frontmatter:** [[Brücke zum Tresor BFS]], [[Feedback und Kritik]], [[Gruppenphasen]], [[Kommunikation im Unterricht]], [[Konflikte in Lerngruppen bearbeiten]], [[Rechtliche Grundlagen des Prüfens]]

**Rückgängig:** Notizen löschen und nur auf den Tresor verweisen.

## E-027 Musterbeispiel einer Prüfungssituation aus lk-praxissituation (MmB, Konflikt) übernehmen?

**Optionen:**
1. übernehmen
2. weglassen, weil FaBe-Fachinhalt mit Leistungszielen

**Wahl:** weglassen

**Begründung:** Das Beispiel enthält Leistungsziele und Fachinhalt einer Lernsituation; das gehört in den Tresor.

**Betroffen:** Praxissituation für Lernkontrollen

**Notizen mit diesem Entscheid im Frontmatter:** [[Praxissituation für Lernkontrollen]]

**Rückgängig:** Beispiel nachtragen.

## E-028 Methode 18 «Aktives Zuhören» überschneidet sich mit dem Tresor-Begriff

**Optionen:**
1. Methodennotiz weglassen
2. behalten und auf den Tresor verweisen

**Wahl:** behalten; der Tresor-Begriff bleibt die fachliche Fassung

**Begründung:** Die Methodennotiz beschreibt das Training im Unterricht; der Tresor den Fachbegriff. Grenzfall in der Befundliste.

**Betroffen:** Aktives Zuhören (Methodensammlung)

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Notiz löschen.

## E-029 Obsidian-Einstellungen im neuen Vault anlegen?

**Optionen:**
1. keine .obsidian-Dateien, Obsidian legt sie beim ersten Öffnen an
2. minimale Einstellungen vorgeben

**Wahl:** minimale Einstellungen: Kern-Plugins wie im Tresor (Bases und Vorlagen aktiv), Vorlagenordner 00 Start/Vorlagen

**Begründung:** Ohne aktivierte Bases zeigen die Übersichten nichts an; die Vorgabe spart David einen Handgriff.

**Betroffen:** .obsidian/

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Ordner .obsidian löschen; Obsidian legt Standardwerte an.

## E-030 Name des Tresors in den obsidian://-Links

**Optionen:**
1. vault=BFS (Ordnername)
2. vault=Tresor BFS (Name in Davids Notizen)

**Wahl:** vault=BFS

**Begründung:** Obsidian verwendet den Ordnernamen als Vault-Namen, solange er nicht umbenannt wurde. Ob der Vault bei David unter diesem Namen registriert ist, ist nicht geprüft.

**Betroffen:** Brücke zum Tresor BFS

**Notizen mit diesem Entscheid im Frontmatter:** [[Brücke zum Tresor BFS]]

**Rückgängig:** Parameter vault in der Brückennotiz ersetzen.

## E-031 Auslegungen der qub-Skills (Stufenbeschreibungen, Prüffragen) aufnehmen?

**Optionen:**
1. nur Wortlaut der Wegleitung
2. Wortlaut plus gekennzeichnete Auslegung

**Wahl:** Wortlaut plus Auslegung, mit Feld auslegung: true und Überschrift «Auslegung … nicht Wortlaut»

**Begründung:** Die Auslegung macht die Indikatoren erst anwendbar; die Kennzeichnung verhindert, dass sie als Vorgabe gelesen wird.

**Betroffen:** alle Notizen mit auslegung: true

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Abschnitte «Auslegung» entfernen.

## E-032 Aufbau- und Übertragungsweg der Dateien

**Optionen:**
1. direkt in der Mac-Shell schreiben
2. in Claudes Arbeitsumgebung per Skript bauen und als Paket über /tmp der Mac-Shell übertragen
3. in Claudes Arbeitsumgebung per Skript bauen und als ein Paket per Dateiübergabe in den Vault-Ordner legen

**Wahl:** Bau per Skript in der Arbeitsumgebung; Übertrag als ein komprimiertes Paket per Dateiübergabe. Das Paket wird im Vault unter dem Namen Start.md abgelegt, nach /tmp kopiert, dort entpackt, und beim Kopieren der Notizen in den Vault wird Start.md durch die echte Startnotiz überschrieben.

**Begründung:** Wenige lange Baudurchgänge, alle Notizen aus einem Skript reproduzierbar. Ein Übertrag als Text durch die Shell (rund 400 KB) wäre fehleranfällig gewesen; die Dateiübergabe einzelner Dateien hätte 585 Dateikarten im Gespräch erzeugt. So bleibt keine Paketdatei auf dem Mac zurück, und ausserhalb des Vaults wird nur in /tmp geschrieben. Die Zwischendateien in /tmp der Mac-Shell werden am Ende gelöscht.

**Betroffen:** ganzer Vault

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** keiner nötig

## E-033 Wie mit Text in gesperrter Schrift umgehen, wenn die Primärprüfung Begriffe nicht findet?

**Optionen:**
1. Notiz auf «nicht geprüft» setzen
2. Vergleich zusätzlich ohne Leerzeichen durchführen und die Fundstelle erneut lesen

**Wahl:** Vergleich zusätzlich ohne Leerzeichen; Fundstellen der drei Fehlschläge im Original gelesen

**Begründung:** In Lehren kompakt 1 sind Überschriften und Lead gesperrt gesetzt («E rwac h s e n e»); die Begriffe stehen auf den genannten Seiten. Zwei weitere Fehlschläge waren echte Fehler der Notizen und wurden korrigiert (B-029, B-030).

**Betroffen:** Lernbiografie und Lernerfahrungen, AVIVA-Modell, AVIVA Phase Informieren

**Notizen mit diesem Entscheid im Frontmatter:** keine

**Rückgängig:** Vergleich ohne Leerzeichen aus check.py entfernen, Prüfung wiederholen

# Davids Entscheide ab 29.09.2026

## E-034 Arbeitsplan als Notiz ablegen?

**Optionen:**
1. Plan nur im Gespräch
2. Notiz «Arbeitsplan» in 00 Start/Kontrolle

**Wahl:** Notiz «Arbeitsplan», laufend nachgeführt

**Entschieden von:** David, 29.09.2026

**Betroffen:** [[Arbeitsplan]], [[Start]]

**Rückgängig:** Notiz löschen, Link in Start entfernen

## E-035 Aufräumen Etappe 1

**Optionen:**
Mehrfachauswahl: Unbenannt.base löschen; Plugin-Regel anpassen und Claudian auf Rückfrage; Vorlagen aus Bases filtern; Plan als Notiz

**Wahl:** alle vier: Unbenannt.base gelöscht; CLAUDE.md erlaubt Claudian (Modus «normal») und BRAT; Claudian von «yolo» auf «normal»; Aufgabentypen.base und Quellen.base schliessen 00 Start aus

**Entschieden von:** David, 29.09.2026

**Betroffen:** CLAUDE.md, .claudian/claudian-settings.json, Aufgabentypen.base, Quellen.base

**Rückgängig:** Regel und Filter zurücksetzen, permissionMode wieder «yolo»

## E-036 Methodensammlung: Prüftiefe und Umgang mit Befunden

**Optionen:**
1. Alle 330, nur Bericht
2. Alle 330, direkt korrigieren
3. Felder plus Stichprobe
4. Nur Eignung hoch/mittel

**Wahl:** Alle 330 am Original prüfen und direkt korrigieren; jede Korrektur in der Befundliste

**Entschieden von:** David, 29.09.2026

**Betroffen:** 30 Methoden und Medien/Methodensammlung/

**Rückgängig:** Korrekturen anhand der Sammelbefunde zurücknehmen

## E-037 Prüftiefe der belegten Notizen

**Optionen:**
1. Gezielt satzgenau
2. Alle satzgenau
3. So lassen (E-003)

**Wahl:** Alle belegten Notizen Satz für Satz am Original prüfen

**Entschieden von:** David, 29.09.2026

**Betroffen:** alle Notizen mit status belegt

**Rückgängig:** Prüfung auf Fundstellenebene (E-003) zurückstufen

## E-038 Test von Bases und Tresor-Links

**Optionen:**
1. Claude per Bildschirmsteuerung
2. David nach Checkliste

**Wahl:** Claude per Bildschirmsteuerung, jedes Ergebnis mit Bildschirmfoto

**Entschieden von:** David, 29.09.2026

**Betroffen:** 00 Start/Bases/, [[Brücke zum Tresor BFS]]

**Rückgängig:** Test von Hand wiederholen

## E-039 Status der Studienskripte Didaktik (8 Skripte, epub)

**Optionen:**
1. Sekundärquelle, kein Beleg
2. Als Beleg zulassen
3. Nicht verwenden

**Wahl:** Als Beleg zulassen. Die Skripte sind nach Davids Worker-Prompt von Claude zusammengestellt; «Skript 8» trägt den Titel des in B-014 gesuchten Studienskripts 8

**Entschieden von:** David, 29.09.2026

**Betroffen:** Notizen, die sich auf Studienskript 8 stützen (B-014)

**Rückgängig:** Status der betroffenen Notizen auf «nicht geprüft» zurücksetzen

## E-040 Wogegen die Methodenfelder prüfen?

**Optionen:**
1. Gegen den Notiztext
2. Gegen Skill 0.14.1
3. Felder nicht prüfen

**Wahl:** aviva_phase, k_stufe, sozialform, eignung_fabe gegen die Abschnitte «Wann», «Wer und Sozialform», «K-Stufen», «Eignung» derselben Notiz; Beschreibung und Ablauf gegen die Ursprungsseite

**Entschieden von:** David, 29.09.2026

**Betroffen:** Methodensammlung

**Rückgängig:** Felder aus E-022 wiederherstellen

## E-041 Dokumentation der Methodenkorrekturen

**Optionen:**
1. Sammelbefund je Paket
2. Ein Befund je Notiz

**Wahl:** Ein Sammelbefund je Paket mit Tabelle Notiz, Änderung, Beleg

**Entschieden von:** David, 29.09.2026

**Betroffen:** [[Befundliste]]

**Rückgängig:** Sammelbefunde aufteilen

## E-042 Rest der Methodensammlung, deren Seite nicht mit WebFetch lesbar ist

**Optionen:**
1. Liegen lassen
2. WebFetch Satz für Satz

**Wahl:** Liegen lassen: die 30 Notizen aus Paket 8 und 5 Einzelfälle bleiben «nicht geprüft»; die 35 bpb-Methoden warten auf Zugriff

**Entschieden von:** David, 29.09.2026

**Betroffen:** Methodensammlung

**Rückgängig:** Prüfung nachholen

## E-043 Spannen mit «bis» in k_stufe und aviva_phase

**Optionen:**
1. Lückenlose Spanne
2. Nur Endpunkte

**Wahl:** Lückenlose Spanne; umgesetzt in 14 Notizen (B-042)

**Entschieden von:** David, 29.09.2026

**Betroffen:** Methodensammlung

**Rückgängig:** Mittelwerte wieder entfernen

## E-044 AVIVA-Zuordnung der Methoden

**Optionen:**
1. Überall «(laut Skill)»
2. Nie markieren
3. Am Fachbuch prüfen

**Wahl:** Nicht pauschal markieren, sondern die Zuordnung am AVIVA-Buch (Grassi u. a.) prüfen; David hat Teil 1, Teil 2, Anhang und die Kurzinformation hochgeladen

**Entschieden von:** David, 29.09.2026

**Betroffen:** Methodensammlung, Zeile «Wann» und Feld aviva_phase

**Rückgängig:** Prüfung verwerfen

## E-045 B-001 Wiederholung ungenügender Kompetenznachweise

**Optionen:**
1. Offen, EHB fragen
2. Wegleitung gilt
3. Ausbildungsprogramm gilt

**Wahl:** Offen, David fragt bei der EHB

**Entschieden von:** David, 29.09.2026

## E-046 B-005 Spannen bei Aufgabentypen

**Optionen:**
1. Typ Spanne, Aufgabe eine Stufe
2. Palette gilt
3. lk-grundlagen gilt

**Wahl:** Typ darf Spanne haben, jede konkrete Aufgabe genau eine K-Stufe

**Entschieden von:** David, 29.09.2026

## E-047 B-004 Massgebende Operatorenliste

**Optionen:**
1. Palette, SAVOIRSOCIAL fürs QV
2. Nur Palette
3. Nur SAVOIRSOCIAL

**Wahl:** Palette für Unterricht und Lernkontrollen, SAVOIRSOCIAL für QV-nahe Prüfungen

**Entschieden von:** David, 29.09.2026

## E-048 B-007 Begriff didaktische Analyse

**Optionen:**
1. EHB/Klafki
2. Lehren und Lernen
3. Beide gleichwertig

**Wahl:** EHB/Klafki

**Entschieden von:** David, 29.09.2026

## E-049 B-008 Zielarten

**Optionen:**
1. Lehren kompakt 1
2. Lehren und Lernen
3. Beide gleichwertig

**Wahl:** Lehren kompakt 1

**Entschieden von:** David, 29.09.2026

## E-050 B-009 Höchstdauer eines Inputs

**Optionen:**
1. 15 bis 20 Minuten
2. 15 Minuten
3. Alle nebeneinander

**Wahl:** 15 bis 20 Minuten, Becker 30 als Abweichung

**Entschieden von:** David, 29.09.2026

## E-051 AVIVA-Zuordnung der Methoden am Buch

**Optionen:**
1. Buch-Methoden korrigieren, Rest melden
2. Nur Buch-Methoden
3. Alles prüfen und korrigieren

**Wahl:** Alle Methoden gegen das AVIVA-Buch (Teil 1, Phasentabellen) prüfen und direkt korrigieren, mit Subagenten

**Entschieden von:** David, 29.09.2026

## E-052 Verbindungen der Methoden

**Optionen:**
1. Ins Feld verwandt
2. Feldwerte als Links
3. Noch nicht

**Wahl:** K-Stufen- und AVIVA-Phasen-Notizen als Wikilinks ins Feld verwandt; k_stufe und aviva_phase bleiben unverändert

**Entschieden von:** David, 29.09.2026

## E-053 Kapitel 12 «Methodensammlung A–Z» aus Lehren und Lernen

**Optionen:**
1. Beleg und neue Notizen
2. Nur Beleg
3. Nur neue Notizen
4. Später

**Wahl:** Als Beleg für bestehende Methoden (Quelleneintrag, status nur bei voller Stützung) und Liste fehlender Methoden zur Auswahl durch David

**Entschieden von:** David, 29.09.2026

## E-054 Listen S. 86 und S. 100 im AVIVA-Buch

**Optionen:**
1. Als ausdrückliche Zuordnung anwenden
2. Nicht als Zuordnung

**Wahl:** Nicht als Zuordnung; Ergänzung bei Lerntagebuch zurückgenommen. Lernjournal: Die Ergänzung stützt sich auf Teil 2 S. 117, nicht auf S. 100; die Frage an David war dazu ungenau, darum Entscheidkarte

**Entschieden von:** David, 29.09.2026

## E-055 Vorrang E-043 gegen das AVIVA-Buch

**Optionen:**
1. Das Buch geht vor
2. E-043 geht vor

**Wahl:** E-043 geht vor; Suggestopädie und Zukunftswerkstatt behalten die Mittelphase

**Entschieden von:** David, 29.09.2026

## E-056 Form der restlichen Entscheide

**Optionen:**
1. Notiz mit Entscheidkarten
2. Im Chat
3. Später

**Wahl:** Notiz «Entscheidkarten» im Ordner Kontrolle; David kreuzt an, Claude setzt danach um

**Entschieden von:** David, 29.09.2026

## E-057 Übergabe an die nächste Sitzung

**Optionen:**
1. Vault-Notiz «Übergabe»
2. Vault-Notiz und Projekt
3. Nur Projekt
PDFs: 1. Nicht kopieren, Pfade notieren 2. Kopien in «Studienskripte Didaktik»
Prompt: 1. Alles Offene 2. Nur Entscheidkarten

**Wahl:** Vault-Notiz «Übergabe» in 00 Start/Kontrolle; Kopien der sechs hochgeladenen PDFs im iCloud-Ordner «Studienskripte Didaktik»; Prompt für alles Offene, Entscheidkarten zuerst

**Entschieden von:** David, 29.09.2026

## E-058 Welche Methoden gehören in den Vault?

**Optionen:**
1. Nur Methoden aus den Fachbüchern (Lehren kompakt, AVIVA-Buch, Lehren und Lernen)
2. Keine; Methoden bleiben im Skill
3. Alle 330

**Wahl:** Alle 330 Methoden bleiben, als Repertoire zum Auswählen

**Entschieden von:** David, 29.09.2026

**Betroffen:** 30 Methoden und Medien/Methodensammlung/

**Rückgängig:** Methodensammlung verkleinern (Option 1 oder 2)

## E-059 Prüftiefe der Methodensammlung

**Optionen:**
1. Ideensammlung: Notizen bleiben, wie sie sind; eine Methode wird erst am Original geprüft, wenn David sie für eine Lektion auswählt
2. Weiter alle 330 am Original prüfen, mit Entscheiden zu Phasen und Feldern

**Wahl:** Ideensammlung (Option 1); ersetzt E-036 und E-042

**Entschieden von:** David, 29.09.2026

**Betroffen:** Methodensammlung; entfallen: Feld einsatz_phase, Claudian-Lauf über die Oldenburger Seiten, Karten A-02 bis A-17

**Rückgängig:** Prüfung nach E-036 wieder aufnehmen

## E-060 Prüftiefe des Kerns

**Optionen:**
1. Satzgenau nur, wo ein Fehler teuer wäre: Zahlen, Notenregeln, EHB-Indikatoren; der Rest bleibt auf Fundstellenebene (E-003)
2. Alle Kernnotizen satzgenau (E-037)
3. Nichts weiter prüfen

**Wahl:** Option 1; ersetzt E-037

**Entschieden von:** David, 29.09.2026

**Betroffen:** Notizen mit status belegt ausserhalb der Methodensammlung; die Prüfung ist eine eigene Etappe und braucht ~/Desktop/BFS

**Rückgängig:** E-037 wieder in Kraft setzen

## E-061 Methodenantworten aus der Sitzung vom 29.09.2026

**Optionen:**
1. Bereits gegebene Antworten in einem Durchgang umsetzen, danach ist die Methodensammlung abgeschlossen
2. Verwerfen, Methodensammlung bleibt wie am 29.09.2026

**Wahl:** Option 1; kein weiteres Recherchieren

**Entschieden von:** David, 29.09.2026

**Betroffen:** Methodensammlung; Umsetzung ausstehend, bis der Bericht der Sitzung mit der Liste der Antworten vorliegt

**Rückgängig:** Änderungen anhand des Sammelbefunds zurücknehmen

## E-062 Neue Inhalte (Etappe 7)

**Optionen:**
1. Vorerst keine; der Vault gilt mit dem heutigen Inhalt als fertig und wächst nach Bedarf
2. Quellen jetzt sichten und auswählen

**Wahl:** Option 1; Etappe 7 und Karte D-05 entfallen vorerst

**Entschieden von:** David, 29.09.2026

**Betroffen:** Arbeitsplan

**Rückgängig:** Etappe 7 wieder aufnehmen

## E-063 Status der Methodensammlung

**Optionen:**
1. Eigener Status «sammlung» für alle 330 Methoden
2. Status bleibt, nur eine Hinweiszeile

**Wahl:** Status «sammlung»; Definition in CLAUDE.md und Start.md: «Methode aus der Ideensammlung, Inhalt nicht am Original geprüft; vor dem Einsatz prüfen.»

**Entschieden von:** David, 29.09.2026

**Betroffen:** 330 Methodennotizen, CLAUDE.md, Start.md

**Rückgängig:** Status aus der Befundliste (B-032 bis B-046) und E-042 wiederherstellen

## E-064 Abschnitt «Einordnung FaBe» in den Methodennotizen

**Optionen:**
1. Überschrift zu «Einordnung FaBe (Einschätzung laut Skill)», Inhalt bleibt
2. So lassen
3. Abschnitt und Feld eignung_fabe entfernen

**Wahl:** Option 1; die Einschätzungen werden nicht mehr David zugeschrieben, weil unklar ist, ob sie von ihm stammen

**Entschieden von:** David, 29.09.2026

**Betroffen:** 330 Methodennotizen

**Rückgängig:** Überschrift per Suchen und Ersetzen zurücksetzen

## E-065 Kontrollordner

**Optionen:**
1. Entscheidkarten und Stichproben ins Archiv; Arbeitsplan, Stand und Übergabe neu; Befundliste und Protokoll bleiben
2. Wie 1, aber löschen statt archivieren
3. Alles bleibt, nur nachführen

**Wahl:** Option 1

**Entschieden von:** David, 29.09.2026

**Betroffen:** 00 Start/Kontrolle/

**Rückgängig:** Dateien aus Archiv zurückschieben

## E-066 Bestätigung der Aufbauentscheide E-001 bis E-033

**Optionen:**
1. Bestätigung bleibt, mit Vermerk
2. Einzeln neu vorlegen

**Wahl:** Option 1. David hatte E-001 bis E-033 am 29.09.2026 auf Claudes Empfehlung bestätigt; bestätigt nochmals im Licht von E-058 bis E-060: E-003 gilt für den Kern, E-013 entspricht E-058, E-022 liefert in der Ideensammlung nur Suchhilfen.

**Entschieden von:** David, 29.09.2026

**Betroffen:** E-001 bis E-033

**Rückgängig:** Entscheide einzeln neu vorlegen

## E-067 Verweis aus den Skills auf den Vault

**Optionen:**
1. In den didaktischen Skills je eine Zeile «Didaktische Grundlagen zuerst in der Werkstatt Didaktik nachschlagen» mit Pfad
2. Skills unangetastet, David verbindet den Vault bei Bedarf
3. Später entscheiden

**Wahl:** Option 1; ändert die Regel «Skills werden nicht angepasst» für diese eine Zeile. Umsetzung als eigener Schritt zusammen mit E-060, weil die Skill-Quellen unter ~/Desktop/BFS/Didaktik Skills liegen und die Plugins neu verpackt werden müssen. Die Liste der betroffenen Skills legt Claude vor dem Bau vor.

**Entschieden von:** David, 29.09.2026

**Betroffen:** didaktische Skills (Liste folgt)

**Rückgängig:** Zeile entfernen, Plugins neu verpacken

## E-068 Wer baut

**Optionen:**
1. Die Sitzung, in der E-058 bis E-067 entschieden wurden; die andere Sitzung liefert nur ihren Bericht und räumt ihre Hilfsdateien weg
2. Die andere Sitzung mit neuer Übergabe

**Wahl:** Option 1, ohne Subagenten

**Entschieden von:** David, 29.09.2026

**Betroffen:** Bau vom 29.09.2026

**Rückgängig:** entfällt

## E-069 Methodennotizen ausserhalb der Methodensammlung

**Optionen:**
1. Lernjournal, Berichtsheft und Lerndokumentation, Problem-based Learning, Flexibles Modellieren Flemo und Individualisierender Unterricht bleiben auf «belegt»
2. Auch sie auf «sammlung»

**Wahl:** Option 1; sie stützen sich auf das AVIVA-Buch, E-058 betrifft die 330 Methoden der Sammlung

**Entschieden von:** David, 29.09.2026

**Betroffen:** fünf Notizen in 30 Methoden und Medien/

**Rückgängig:** Status auf «sammlung» setzen

## E-070 Wer baut Etappe 2

**Optionen:**
1. Die Sitzung der Neuausrichtung baut (E-068)
2. Die Sitzung, in der die Methodenantworten gegeben wurden, baut Etappe 2

**Wahl:** Option 2; E-068 ist für Etappe 2 geändert. Davids Detailentscheide vor dem Bau: C-04, C-07, Vier-Ecken und Blindball nach Claudians Abruf umsetzen; Parlamentssimulation und Schulbuch so lassen; C-06 Ursprungszeile behalten, Klauer ohne Seitenzahl; D-04 Kap. 12 als Quelle bei Ampelquiz, beiden Rotierenden Partnergesprächen und Problem-based Learning; Hinweise D-01 und D-02 am Ende der Beschreibung; Seitengrenzen nur Textseiten; autor «Kap. 12: Schubiger, A.», Kap. 5 als «S. 72–74 (nur RITA)»; «(laut Skill)» nach AVIVA-Angaben: Buchphase mit Seite ohne Markierung, Rest markiert; Mind Map nur ausserhalb von aviva_phase; E-04 als Satz im Sammelbefund.

**Entschieden von:** David, 29.09.2026

**Betroffen:** 58 Notizen, Sammelbefund B-047

**Rückgängig:** Änderungen anhand von B-047 zurücknehmen

## E-071 Werkstatt-Wiki (Webseite aus dem Vault)

**Optionen und Wahl, je Punkt:**
1. Ablage: eigene private Webseite (gewählt) | HTML-Datei im Vault | beides
2. Design: Basix Pro (gewählt) | FaBe Basix; Aufbau wie Wikipedia mit Hauptseite, Artikeln, Steckbrief, «Links auf diese Seite», Einzelnachweisen, Suche, Methodenfinder mit Trichter
3. Verbindende Texte: von Claude, jede Aussage mit Verweis auf die Notiz, aus der sie stammt (gewählt) | nur Vault-Inhalte | ohne Kennzeichnung
4. Wo: nur auf rund 18 Knotenseiten, also Hauptseite, AVIVA-Phasen, K1 bis K6, vier Sozialformen, Aufgabentypen, Prüfen (gewählt) | zusätzlich auf jeder Methode
5. Status: klein im Steckbrief (gewählt) | Hinweisbalken oben
6. Nicht auf der Seite: Kontrollordner, Vorlagen, Archiv, CLAUDE.md (gewählt) | alles
7. Zeitbedarf: Bänder per Skript, Originaltext bleibt sichtbar (gewählt) | nur Text; dazu die Bänder «Lektionen und länger» und «nicht eindeutig»
8. Skript: Datei im Vault unter «00 Start/Navigator/navigator.py», Zeile in CLAUDE.md, Link in Start.md (gewählt) | nicht speichern
9. Dazu eine Seite «Über dieses Wiki»; Teilen mit anderen entscheidet David später

**Entschieden von:** David, 29.09.2026

**Betroffen:** neuer Ordner 00 Start/Navigator (navigator.py, Verbindungstexte.md), CLAUDE.md, Start.md; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV

**Rückgängig:** Ordner Navigator entfernen, Zeilen in CLAUDE.md und Start.md streichen, Seite löschen

## E-072 Name der Seite und Verweise auf Claude, Skills, KI

**Optionen und Wahl, je Punkt:**
1. Name: Basic Skills (gewählt) | Basicpedia | Basicum | andere
2. Verweise auf der Seite: ersatzlos entfernen (gewählt) | neutral umbenennen mit Zeichen «°» | nur Claude und KI entfernen
3. Einzelfälle: nach drei Regeln (gewählt): Überbringer-Verweis fällt weg und der Inhalt bleibt («Laut Skill nennt Meyer» wird «Meyer nennt»); Sätze nur über Skills fallen weg, die Notiz «Quelle Plugins Didaktik» kommt von der Seite; KI als Thema bleibt («KI-Unterstützung offenlegen», «KI-Werkzeuge», «Skills weiterentwickeln») | alle Sätze mit diesen Wörtern streichen

**Entschieden von:** David, 29.09.2026

**Folge:** Auf der Seite ist nicht mehr erkennbar, welche Aussagen aus der aufbereiteten Sammlung stammen; im Vault bleiben alle Herkunftsangaben unverändert. Umgesetzt im Skript navigator.py (Regeln ERSATZ, ZEILE_WEG, ABSCHNITT_WEG).

**Betroffen:** navigator.py, Verbindungstexte.md (Name), CLAUDE.md, Start.md; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV, Version 2

**Rückgängig:** Filter im Skript entfernen, Seite neu erzeugen und veröffentlichen

## E-073 Basic Skills: feste Adressen, Ablauf-Listen, Schriften

**Optionen und Wahl, je Punkt:**
1. Artikeladressen: fest aus dem Namen, etwa «#advance-organizer», Umlaute als ae, oe, ue (gewählt) | wie bisher nummeriert (#n0 bis #n559)
2. Alte Adressen (#n…, #k-…): führen zur Startseite (gewählt) | Übersetzungstabelle als Datei im Ordner Navigator
3. Sammelseiten mit derselben Adresse wie ein Artikel (vier AVIVA-Phasen): Sammelseite fällt weg, die Adresse gehört dem Artikel (gewählt) | Sammelseite mit Zusatz
4. Ablauf «1) 2) 3)» auf einer Zeile: nur in der Anzeige als nummerierte Liste (gewählt) | Notizen im Vault korrigieren; nicht getrennt wird innerhalb offener Klammern (gewählt) | Zeile ungetrennt lassen | Notiz umformulieren; Text vor «1)» wird eigener Absatz (gewählt) | so lassen; Kommas am Schrittende und Text nach dem letzten Schritt bleiben (gewählt) | Notizen anpassen; zwei Schutzregeln ohne heutige Wirkung bleiben (gewählt) | streichen
5. Schriften: aus der veröffentlichten Seite übernommen (gewählt) | Ordner mit den Schriften verbinden; verkleinert mit fonttools, wenn vorhanden, sonst ganz eingebettet (gewählt) | als verkleinerte Dateien im Ordner Navigator | unverändert
6. Zeichenkodierung: Zeile «meta charset utf-8» in der Vorlage (gewählt) | ohne
7. Vorschau vor jeder Veröffentlichung (gewählt) | direkt veröffentlichen

**Entschieden von:** David, 30.09.2026

**Folge:** Seite 1,8 statt 2,2 MB; 330 Ablaufzeilen als Liste; sonst unverändert.

**Betroffen:** navigator.py, CLAUDE.md; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV, Version 3

**Rückgängig:** Änderungen in navigator.py zurücknehmen (Funktionen slug, marken, ablaufTeile, schritte, vortextAblauf, zeichen_der_daten, Verkleinerung in font_css), Seite neu erzeugen und veröffentlichen

## E-074 Basic Skills: Startseite, Navigation, Methodenfinder, Artikel und Sammelseiten neu

**Optionen und Wahl, je Punkt:**
1. Zielpublikum: David und Kolleginnen (gewählt) | nur David | auch Lernende; Fachsprache bleibt, Vault-Sprache geht
2. Umfang: Startseite und Finder umbauen, Artikel und Sammelseiten leicht anpassen (gewählt) | nur Feinschliff | ganz neu; gebaut von zwei Subagenten parallel nach freigegebener Skizze
3. Startseite: Suchfeld, sechs Kacheln aus den häufigen Einstiegen mit Zielnamen, Kette in sechs Schritten mit aufklappbarem Zusammenhangstext, Bereichskarten, Zeile «Raster» (gewählt) | alte Schnellwahl; Welle entfällt
4. Kopfzeile: auf dem Handy eine Zeile mit Lupe und Menü, Lupe und Menü werden zum Kreuz, schrumpft beim Scrollen (gewählt)
5. Seitenleiste: nur auf Artikeln, nur der eigene Bereich ohne die Übersicht selbst; ab 60 Artikeln Bereichslink, Methodenfinder und je fünf Nachbarn (gewählt) | ganze Liste | wie bisher auf allen Seiten
6. Abschnittstitel klein in Grossbuchstaben mit feiner Linie statt brauner Balken, auf allen Seiten (gewählt)
7. Methodenfinder: sichtbar AVIVA-Phase, K-Stufe, Sozialform, Volltext; «Mehr Filter» für Zeitbedarf, Eignung, Status (öffnet sich bei entsprechender Voreinstellung); aktive Filter als entfernbare Chips; Karten mit AVIVA-Phase, K-Stufe, Sozialform; 24 Karten, dann «Weitere Methoden zeigen»; auf dem Handy Filterfenster mit Kreuz, Escape und «n Treffer anzeigen» (gewählt)
8. Artikel: Steckbrief auf dem Handy nach der Kurzfassung, aufklappbar; «Erwähnt in» ab 12 Einträgen zugeklappt; keine Sprungliste (gewählt) | Sprungliste ab vier Zwischentiteln
9. Phasen-, K-Stufen- und Sammelseiten: Methoden als Zahl mit Knopf «Im Methodenfinder filtern», übrige Artikel als Liste unter «Weitere Artikel zur Phase/Stufe …» bzw. «n weitere Artikel» (gewählt) | alles als Liste | alles weg; Gruppe, Raster und andere Arten bleiben Listen
10. Texte: «Notiz» wird «Artikel», «Notiztyp» wird «Art», «Links auf diese Seite» wird «Erwähnt in», Titel und Links ohne «Index», neue Einleitung, Fusszeile «Stand …», «Über dieses Wiki» ohne Obsidian und Vault; Einbettungen fallen weg, Links ins Leere und nach Obsidian werden Text; drei Vault-Stellen nur auf der Seite ersetzt (Ersatzliste im Skript) (gewählt) | im Vault ändern | so lassen
11. Sortierung überall nach dem angezeigten Namen; lange Adressen brechen um (gewählt)
12. Nach Einbau direkt veröffentlicht, ohne zweite Vorschau (gewählt)

**Entschieden von:** David, 30.09.2026

**Folge:** Methodenfinder auf dem Desktop rund 1800 statt 46 600 px hoch, Phasenseite «Verarbeiten» rund 2400 statt 8500 px, Startseite rund 1600 statt 2300 px; auf 390 px scrollt keiner der 560 Artikel seitwärts.

**Betroffen:** navigator.py; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV, Version 4

**Rückgängig:** navigator.py auf den Stand von E-073 zurücksetzen (Version 3 der Seite enthält die alte Vorlage), Seite neu erzeugen und veröffentlichen

## E-075 Basic Skills: privat, ohne Hinweise auf Schule und Personen; einfacherer Methodenfinder

**Optionen und Wahl, je Punkt:**
1. Titel: «Werkstatt Didaktik» statt «BFS Basel» und «Berufsfachschule Basel» in Kopfzeile und Startseite, «Basic Skills» grösser (26 px, Handy 22 px) (gewählt) | 30 px fett
2. Über dieses Wiki: «privates didaktisches Nachschlagewerk für den Unterricht in der beruflichen Grundbildung; es entsteht nicht im Auftrag einer Schule» (gewählt) | ohne Satz zur Unabhängigkeit
3. Auf der Seite, nicht im Vault: «Tresor BFS» wird «Tresor»; Aussagen über die Schule neutral; Dateipfade, Abschnitte «Ablage», Felder «Pfad» und Ortsangaben in Quellen entfernt; «Folien BFS-Tagung» wird «Tagungsfolien», «BFS Basel 2023» wird «2023»; Obsidian-Links werden Text; «Notiz» wird «Artikel»; zwei Arbeitssätze der Brücke entfallen (gewählt) | nur Pfade ausblenden, Zitate genau | so lassen. Die Bereinigung geschieht im Skript vor dem Erzeugen, damit auch der Quelltext der Seite nichts enthält.
4. Flaig: die vier Artikel, die auf seiner Diplomarbeit beruhen oder seinen Namen tragen (Raster-Bibliothek nach Flaig, Quelle Flaig Beurteilungsraster, Deskriptorenraster bauen, Reflexionszyklus nach Gibbs), kommen nicht auf die Seite, Verweise darauf entfallen (gewählt) | nur Namen entfernen
5. Strohmeier bleibt als Autor (gewählt) | entfernen; «Berufsfachschule» als Schultyp und «Region Basel» in EHB-Titeln bleiben (gewählt)
6. Methodenfinder: Kachel «Methode suchen» führt zum Finder; Einleitung ein Satz; Zählung «n von 335 Methoden» statt Trichter; Skript-Hinweis nur noch in «Über dieses Wiki» (gewählt)
7. K6 und andere Seiten ohne weitere Artikel: kein leerer Titel (gewählt)

**Entschieden von:** David, 30.09.2026

**Folge:** Die Seite zeigt 556 statt 560 Artikel. In der fertigen Datei samt Quelltext kommen «BFS», «Berufsfachschule Basel», die zwei Vornamen, «Megastarters», «Flaig», Dateipfade und Obsidian-Links nicht mehr vor (Suche vom 30.09.2026). Im Vault bleibt alles unverändert.

**Betroffen:** navigator.py (SEITE_ERSATZ, SEITE_OHNE, seite_bereinigen, quelle_bereinigen, Vorlage); Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV, Version 5

**Rückgängig:** Bereinigung und Ausschluss in navigator.py entfernen, Seite neu erzeugen und veröffentlichen

## E-076 Basic Skills: vier Werkzeuge auf der Startseite

**Optionen und Wahl, je Punkt:**
1. Idee (David): auf der Startseite Funktionen zum Machen statt nur Lesen; die Kacheln «Lektion planen», «Aufgabe formulieren», «Lernkontrolle bauen», «Lektion reflektieren» öffnen je ein Werkzeug, die Artikel stehen klein darunter (gewählt) | eigener Abschnitt «Werkzeuge»
2. Speichern: Entwurf nur im eigenen Browser, sonst drucken oder kopieren (gewählt) | nichts speichern | auf der Seite speichern
3. Angaben aus ungeprüften Artikeln mit Hinweis «Richtwert, nicht am Original geprüft» bzw. bei Arbeitsauftrag und Abhaklisten «nicht am Original geprüft» (gewählt) | nur belegte Angaben
4. Lektion planen: 2 bis 5 Lektionen zu 45 Minuten; Feld Pausen (0); Schalter «20 % Reserve einplanen» (aus); AVIVA-Zeitgerüst nach Davids Richtwerten, vorbelegt mit der Mitte; Methode aus dem Finder je Phase; «Phase hinzufügen»; Warnung bei Summe und bei Informieren über 20 Minuten (E-050); Verlaufsplan mit den EHB-Spalten (gewählt)
5. Aufgabe formulieren: K1 bis K5, Operatoren der Palette als Chips (am Satzanfang gross), Aufgabentypen nach Feld k_stufe, vier EHB-Elemente, Titel «Aufgabe N (Typ, K-Stufe)», Hinweis bei Operator einer anderen Stufe (gewählt)
6. Lernkontrolle bauen: Notenrechner nach «Notenformel und Sockelwert» mit Sockel (60) und Rundung (Zehntel vorbelegt), Notenskala, Einzelumrechnung; sieben Schritte, Pflichtangaben, Gütecheck C und D zum Abhaken (gewählt)
7. Lektion reflektieren: hermeneutischer Dreischritt mit Leitfragen; Zehnerkatalog mit Indikatorengruppen und Stichworten, Schlusssatz einmal oben, keine Skala, kein Joker; Datum und Thema (gewählt) | Skala in drei Stufen
8. Einheitlich: Rückfrage beim Zurücksetzen auf der Seite, «Dein Entwurf bleibt in diesem Browser gespeichert.», «Ergebnis kopiert.»; Kachel-Unterzeile «Werkzeug» (gewählt)
9. Bau durch zwei Subagenten parallel, Vorschau vor der Veröffentlichung (gewählt)

**Entschieden von:** David, 30.09.2026

**Folge:** Befunde B-049 (Inputdauer) und B-050 (Aufgabentypen K3) eingetragen, nicht korrigiert.

**Betroffen:** navigator.py (Blöcke «Werkzeuge C» und «Werkzeuge D», Router, RESERVIERT, seiteHaupt); Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV, Version 6

**Rückgängig:** Werkzeugblöcke, Routerzeilen und Kachelzuordnung in navigator.py entfernen, Seite neu erzeugen und veröffentlichen

## E-077 Umbau des Skills fertigen-unterricht-planen: Inhalte aus Tresor und Werkstatt

**Optionen und Wahl, je Punkt:**
1. Bestehenden Skill verschlanken, Inhalte aus Tresor und Werkstatt (gewählt) | zweiter Skill daneben
2. kette.md fällt weg, nachdem die Lücken als Werkstatt-Notizen übertragen sind (gewählt)
3. Ankerfall immer die Sonnenblick-Praxissituation der LS; QV-Aufgaben nur als Referenz für QV-nahe Aufgabenstellungen (gewählt)
4. Ohne verbundene Vaults hält der Skill an und meldet, welche Ordner fehlen (gewählt)
5. Beschreibung nennt nur, wann der Skill gilt, und die Abgrenzung (gewählt) | was und wann | unverändert
6. Prüfskript bleibt und läuft beim Bauen mit, neu mit Ankerfall, «sammlung» und Methodendauer (gewählt) | weglassen | unverändert
7. Methodenwahl nur über die Werkstatt (gewählt) | über den Skill unterrichtsmethoden
8. Bedingungsanalyse vorerst im Auftrag mitgegeben (gewählt) | Datei lesen
9. Ablage der fertigen Planung jedes Mal nachfragen (gewählt) | LS-Ordner | nur im Gespräch
10. Ergebnis: Kopf, Verlaufstabelle und Zeitbilanz (gewählt) | volles Dokument mit zwölf Abschnitten
11. Stehende Regeln im Skill: Sonnenblick immer; «keine Lernkontrolle» gilt wie geschrieben; Termine und Organisationsminuten immer fragen; die Zeile «entscheide du» entfällt (gewählt)
12. Übrige didaktische Skills (E-067) getrennt danach (gewählt)
13. Neue Notizen zu B1 und D8 mit Status «nicht geprüft»; Prüfung am Original später mit den übrigen ungeprüften Kettennotizen (gewählt)
14. Umsetzung in der Quelle Didaktik Skills als Version 0.15.0, unterrichten.plugin neu verpacken; erweitert E-067 für diesen Skill (gewählt)

**Grundlage:** Messlatte LS 2.02 Kind vom 30.09.2026 mit dem Skill 0.14.2, Tresor und Werkstatt verbunden: Lernziele, K-Stufen, Quellen und Ankerfall ohne Fehler; 15 Rückfragen; zwei Entscheide ohne Rückfrage (Termine, Organisationsminuten).

**Entschieden von:** David, 30.09.2026

**Betroffen:** Thema festlegen und Unterrichtseinheit einordnen (neu), Unterrichtseinheit begründen (neu), Planungskette fertigen Unterricht, Index Planung und didaktische Modelle; Skill fertigen-unterricht-planen (folgt)

**Rückgängig:** die zwei neuen Notizen löschen, Links und Indexeinträge entfernen; Skill auf 0.14.2 zurücksetzen

## E-078 fertigen-unterricht-planen 0.15.1: schneller und sparsamer

**Optionen und Wahl, je Punkt:**
1. skill_check.py, muster.py und gegenprobe.py bleiben im Quellordner liegen, werden nicht mehr gepflegt und nicht mehr verpackt (gewählt) | entfernen | weiter pflegen
2. Fundstellen: Verlaufsplan in der Zeile «Informieren», Vollplanung in der Sachanalyse, Schicht 1; das Prüfskript prüft entsprechend (gewählt)
3. Leseleiter: LS-Notiz und Praxissituation, dann geprüfte Notizen im Tresor (40 Begriffe, 15 Careum Volltexte), dann PDF als Text, Seitenbild nur als Letztes; keine anderen Skills laden; Werkstatt-Notizen nur bei Unklarheit (gewählt)
4. Auftragsvorlage mit festen Feldern für Termine, Organisationsminuten, Produkt und Ablage; steht es im Auftrag, wird nicht gefragt (gewählt)
5. Methoden: Claude schlägt je Phase eine Methode mit Nummer, Status und Alternative vor, David tauscht danach; zuerst die für die LS markierten, sonst aus der ganzen Sammlung. Leitfragen der Praxissituation bilden die Ergebnisklammer (gewählt)
6. Verlaufsplan ist der Normalfall, Vollplanung nur auf Verlangen (gewählt)
7. Widersprüche und fehlende Seiten werden vor der Fragerunde gesucht und kommen in dieselbe Runde; eine Fragerunde (gewählt)
8. Ohne Rückfrage: Titel laut SLP, «keine Lernkontrolle» gilt wie geschrieben, Input 15 bis 20 Minuten, Verteilung der Ziele nach den vier Bedingungen, Prüfskript mit Dateien in Claudes Arbeitsbereich (gewählt)
9. Sammelskript für das Lesen erst, wenn der Nachtest zeigt, dass das Lesen weiterhin am meisten kostet (gewählt)

**Grundlage:** Test LS 2.02 mit 0.14.2 (15 Fragen in zwei Runden, rund 20 Lesevorgänge vor der ersten Frage) und erste Runde des Nachtests mit 0.15.0 (12 Fragen).

**Entschieden von:** David, 30.09.2026

**Betroffen:** Skill fertigen-unterricht-planen (SKILL.md, Version 0.15.1, unterrichten.plugin)

**Rückgängig:** SKILL.md der Version 0.15.0 wiederherstellen und neu verpacken

## E-079 fertigen-unterricht-planen 0.15.2: weniger Fragen

**Optionen und Wahl, je Punkt:**
1. Lernprodukt und Spalte «Material» schlägt Claude vor, David ändert danach; keine Frage (gewählt)
2. Befunde ohne Entscheid, etwa Tippfehler in Tresor-Notizen, stehen unter «Offene Punkte» und kommen nicht in die Fragerunde (gewählt)
3. Quellen: Literatur laut SLP der Fachrichtung und geprüfte Tresor-Notizen; andere Quellen nur, wenn ein Lernziel sonst nicht belegt ist, dann als ein Punkt der Fragerunde (gewählt)
4. Kein weiterer grosser Nachtest; kette.md wird nach Freigabe gelöscht (gewählt)

**Grundlage:** Nachtest LS 2.02 mit 0.15.1: eine Fragerunde, stehende Entscheide eingehalten, 15 Fragen, davon mehrere aus breitem Lesen durch Subagenten und aus Befunden ohne Entscheid.

**Entschieden von:** David, 30.09.2026

**Betroffen:** Skill fertigen-unterricht-planen (SKILL.md, Version 0.15.2, unterrichten.plugin)

**Rückgängig:** die drei Regeln aus SKILL.md entfernen und neu verpacken

## E-080 B-053 Welche Fassung der Operatorenliste massgebend ist

**Optionen:**
1. Aggregatliste als eigene Quelle anerkennen und umbenennen
2. Liste verwerfen, nur typbezogen arbeiten
3. Lassen wie bisher

**Wahl:** Aggregatliste als eigene Quelle anerkennen; sie heisst künftig «Operatorenliste des Skills aufgabentypen, Zusammenstellung des Skills, nicht Teil der Palette». E-047 bleibt in Kraft und ist damit präziser formuliert.

**Grundlage:** Das Original-PDF der Palette führt keine Tabelle Operator zu K-Stufe, sondern nur Operatoren je Aufgabentyp. E-047 nannte eine Quelle, die es in dieser Form nicht gibt.

**Entschieden von:** David, 07.10.2026

**Betroffen:** 27 Notizen in «40 Aufgaben und Operatoren»

**Rückgängig:** Quellenzeile zurückbenennen

**Stand:** umgesetzt

## E-081 B-052 Vorrang gegenüber Master-Korpus Referenz 03

**Optionen:**
1. E-047 behält Vorrang, Korpus als überholt markieren
2. Korpus behält Vorrang, E-047 ändern
3. Beide gleichwertig

**Wahl:** E-047 behält Vorrang. Der Satz «Bei Konflikt gilt diese Liste» ist gestrichen und durch einen Verweis auf E-047 ersetzt; die Datei trägt im Kopf «überholt seit 29.09.2026».

**Grundlage:** Der Korpus erklärte sich gegenüber der Palette für vorrangig, was E-047 widerspricht; betroffen war namentlich «planen» (Korpus K3, Palette K5). Die Datei wird von keinem Skill und keiner Vaultnotiz gelesen; nur ihr Unterordner Quellen/ ist in Gebrauch.

**Entschieden von:** David, 07.10.2026

**Betroffen:** Master-Korpus, 03_taxonomie-operatoren.md in drei gleichen Fassungen

**Rückgängig:** die beiden Textstellen zurückschreiben

**Stand:** umgesetzt

## E-082 B-056 Zwölf Operatoren der Palette, die die Liste nicht kennt

**Optionen:**
1. In die Liste aufnehmen mit der Stufe des Typs
2. Aus der Palette streichen
3. Als nicht eingestuft führen

**Wahl:** Aufnehmen: recherchieren, beschaffen, zusammentragen, aufbereiten auf K2 bis K3; erstellen auf K3; auswählen auf K1 bis K2; zurückmelden auf K3 bis K4; unterscheiden ohne feste Stufe; dokumentieren, zusammenstellen, reflektieren, belegen ohne feste Stufe, prozessbegleitend.

**Grundlage:** Streichen würde den Typen 9, 14 und 17 ihre Operatoren nehmen.

**Entschieden von:** David, 07.10.2026

**Betroffen:** [[Operatoren und K-Stufen]] im Vault; im Skill noch offen (Schritt 8)

**Rückgängig:** Abschnitt «Beschlossene Ergänzungen» entfernen

**Stand:** im Vault umgesetzt, im Skill offen

## E-083 B-057 Sieben Stufenkonflikte zwischen Aufgabentyp und Liste

**Optionen:**
1. Mehrdeutigkeit in der Liste eintragen
2. Operatoren in den sieben Typen austauschen
3. Offen lassen wie bisher

**Wahl:** Mehrdeutigkeit eintragen: begründen K2 bis K4, einordnen K1 bis K2, entwickeln K3 bis K5, erschliessen und erarbeiten K4 bis K5, gestalten K3 bis K5. Die Notiz nennt damit sieben mehrdeutige Operatoren statt drei.

**Grundlage:** Ein Austausch würde Davids Palette ändern. Der Skill nannte bisher nur begründen, vergleichen und gestalten als mehrdeutig.

**Entschieden von:** David, 07.10.2026

**Betroffen:** [[Operatoren und K-Stufen]] im Vault; im Skill noch offen (Schritt 8)

**Rückgängig:** Abschnitt «Beschlossene Ergänzungen» entfernen

**Stand:** im Vault umgesetzt, im Skill offen

## E-084 B-054 K6 in der Skill-Abschrift der Palette

**Optionen:**
1. Abschrift und Notiz auf den Originalstand bringen

**Wahl:** Der Satz «K6: In der Palette und in den Büchern vorhanden» ist richtiggestellt: K6 steht in Lehren kompakt 1 und in Lehren und Lernen, die Palette schliesst es ausdrücklich aus. Die Korrektur der Abschrift selbst gehört zum Skillumbau.

**Grundlage:** Das Original-PDF führt «Kurzübersicht (K1 bis K5)», keine K6-Zeile und den Absatz «Wichtige Einschränkung». Belegt mit abschrift_check.py.

**Entschieden von:** David, 07.10.2026

**Betroffen:** [[K-Stufen im Überblick]]; Skill-Abschrift offen

**Rückgängig:** Satz zurückschreiben

**Stand:** im Vault umgesetzt, im Skill offen

## E-085 B-055 Zehn Operatoren falsch «Lehren kompakt 1, S. 70» zugeschrieben

**Optionen:**
1. Auf den Originalbestand zurücksetzen
2. Behalten und als nicht belegt markieren
3. Quelle entfernen

**Wahl:** Zurücksetzen. K1 nur wiedergeben und wiedererkennen; K3 nur anwenden und lösen; K4 nur analysieren und zerlegen; K5 konstruieren, verknüpfen, entfalten, erläutern; K6 bewerten und überprüfen. K2 bleibt. Die Zeile heisst jetzt «Klammerumschreibung, keine Operatorenliste».

**Grundlage:** Das Buch führt auf S. 70 keine Operatorenliste. Belegt mit lk1_abgleich.py: vorher 10 Befunde und Exit 1, nachher 0 Befunde und Exit 0.

**Entschieden von:** David, 07.10.2026

**Betroffen:** sechs K-Stufen-Notizen

**Rückgängig:** Zeilen aus der Sicherung zurückschreiben

**Stand:** umgesetzt

## E-087 B-058 «gestalten» war bei Typ 10 als Konflikt benannt

**Optionen:**
1. Satz richtigstellen und Typ 16 ergänzen

**Wahl:** Richtiggestellt. Die Liste führt «gestalten (auf Vorgabe)» auf K3, und Typ 10 ist K3; der Konflikt liegt bei Typ 16 (K5).

**Grundlage:** operatoren_check.py; Original-PDF der Palette

**Entschieden von:** David, 07.10.2026

**Betroffen:** [[Operatoren und K-Stufen]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-088 B-060 Veraltete Skillversion in den Notizen

**Optionen:**
1. Auf 0.16.0 nachführen
2. Versionsangabe weglassen
3. Lassen

**Wahl:** Nachführen. 395 Notizen tragen jetzt «unterrichten 0.16.0». Die Archivdatei Entscheidkarten.md behält bewusst den historischen Stand.

**Grundlage:** Die Referenzdateien sind zwischen 0.14.2 und 0.16.0 inhaltlich gleich, mit diff -r geprüft; die Änderung ist sachlich unschädlich.

**Entschieden von:** David, 07.10.2026

**Betroffen:** 395 Notizen

**Rückgängig:** aus der Sicherung zurückschreiben

**Stand:** umgesetzt

## E-089 B-080 Die QV-Lücke benennen

**Optionen:**
1. Neue Notiz anlegen
2. In [[Operatoren und K-Stufen]] einarbeiten
3. Nichts tun

**Wahl:** Neue Notiz [[Operatoren im QV gegen Operatoren im Unterricht]] mit der Punktetabelle von SAVOIRSOCIAL, den zwei abweichenden Fällen und der Praxisfolge. Keine der beiden Listen wird geändert.

**Grundlage:** «beschreiben» ist im QV Wissensfrage (1 Punkt), im Unterricht K2; «begründen» ist im QV Anwendungsfrage (2 Punkte), im Unterricht K4. E-047 trennt die Bereiche richtig.

**Entschieden von:** David, 07.10.2026

**Betroffen:** neue Notiz in «40 Aufgaben und Operatoren»

**Rückgängig:** Notiz löschen

**Stand:** umgesetzt

## E-090 B-061 Verfahren zum Prüfen bestehender Einstiegsfragen

**Optionen:**
1. Prüflistennotiz plus Prüfskripte im Vault
2. Nur die Prüflistennotiz
3. Den Skill praxis-ergebnissicherung erweitern

**Wahl:** Notiz [[Einstiegsfrage prüfen]] mit der Achtpunkt-Prüfliste und der Zuordnung Fragegrammatik zu K-Stufe, dazu elf Prüfskripte in «00 Start/Prüfungen» mit der Notiz [[Prüfungen]]. Der Skill bleibt zunächst unverändert.

**Grundlage:** Vorbild für den Ort ist «00 Start/Navigator/navigator.py». Das Raster ist an sechzehn Proben kalibriert, davon acht echte Dossierfragen, und wird rot, wenn ein Bewertungsmuster fehlt.

**Entschieden von:** David, 07.10.2026

**Betroffen:** neue Notizen und neuer Ordner «00 Start/Prüfungen»

**Rückgängig:** Notizen und Ordner löschen

**Stand:** umgesetzt

## E-092 B-063 LS 2.04 Teil 2: keine Leitfrage trifft K5

**Optionen:**
1. Frage 3 auf K5 umformulieren
2. Das K5-Ziel aus Teil 2 nehmen
3. Lassen

**Wahl:** Frage 3 ersetzen durch «Woran würde man erkennen, dass Pierres ‹Ja, klar› aus freiem Willen kommt, und welche Bedingungen müsste das Team dafür schaffen?» Das verlangt Bedingungen entwickeln, also K5, und behält Pierres Satz als Aufhänger. Frage 1 und 2 bleiben.

**Grundlage:** fragecheck.py: Frage 3 ist eine Bewertungsfrage, Frage 1 und 2 treffen K2.

**Entschieden von:** David, 07.10.2026

**Betroffen:** LS 2.04 Arbeitsdossier 2.docx

**Rückgängig:** Frage zurückschreiben

**Stand:** offen, Dossieränderung mit Sichtkontrolle in Word

## E-093 B-064 LS 2.08: Bewertungsfrage bei K4-Zielen

**Optionen:**
1. Frage auf K4 umformulieren
2. Lassen

**Wahl:** Ersetzen durch «Gliedern Sie, welche ethischen Prinzipien im Gespräch über Pierre ohne ihn aufeinandertreffen, und zeigen Sie auf, woran die Entscheidung hängt.» Die zwei flacheren Fragen bleiben als Hinführung.

**Grundlage:** fragecheck.py

**Entschieden von:** David, 07.10.2026

**Betroffen:** LS 2.08 Arbeitsdossier

**Rückgängig:** Frage zurückschreiben

**Stand:** offen, Dossieränderung mit Sichtkontrolle in Word

## E-094 B-065 LS 1.04 Teil 2: Wertfrage bei K2-Zielen

**Optionen:**
1. Frage auf K2 umformulieren
2. Lassen

**Wahl:** Ersetzen durch «Woran erkennen Sie, ob dieser Vorschlag zur Partizipationsstufe passt, die Sie eben bestimmt haben?»

**Grundlage:** fragecheck.py

**Entschieden von:** David, 07.10.2026

**Betroffen:** LS 1.04 Arbeitsdossier

**Rückgängig:** Frage zurückschreiben

**Stand:** offen, Dossieränderung mit Sichtkontrolle in Word

## E-096 B-066 Der Anlassfall ist in keiner Dossierfassung auffindbar

**Optionen:**
1. Im Befund festhalten, kein Handlungsbedarf

**Wahl:** Festgehalten. Die Frage «Darf Laura Cosi verlangen, dass …?» steht in keiner der 131 Dossierdateien; die aktuelle Fassung von LS 2.04 Teil 1 hat die Bewertungsfrage bereits zurückgenommen.

**Grundlage:** Vollsuche nach «Cosi» in 8024 docx-Dateien; fragecheck.py an beiden Fassungen

**Entschieden von:** David, 07.10.2026

**Betroffen:** keine

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-098 B-081 Entwicklungsquelle des Plugins nachführen

**Optionen:**
1. ehb-vorbereitungsdossier in die Quelle kopieren, Version auf 0.16.0, dann prüfen.py
2. Von der installierten Fassung aus neu packen
3. Skilländerungen lassen

**Wahl:** Vor jeder Skilländerung: ehb-vorbereitungsdossier aus der installierten Fassung in die Quelle kopieren, Version der Quelle auf 0.16.0 setzen, mit _pruefung/prüfen.py prüfen.

**Grundlage:** Die Quelle trägt 0.15.2 und enthält diesen Skill nicht; ein Neubau von dort würde ihn verlieren. Rumpftexte und references sind sonst gleich.

**Entschieden von:** David, 07.10.2026

**Betroffen:** ~/Desktop/BFS/Didaktik Skills/unterrichten

**Rückgängig:** entfällt

**Stand:** offen, erster Schritt jedes Skillumbaus

## E-099 B-068, B-069, B-070 Das Prüfskript der Methodensammlung in Ordnung bringen

**Optionen:**
1. Satz in SKILL.md richtigstellen, bloom erweitern, Docstring nachführen
2. Nur den Satz in SKILL.md streichen
3. methoden_pruefung.py als Ersatz übernehmen

**Wahl:** Erste und dritte Option zusammen: Der Satz in SKILL.md nennt künftig, was bloom wirklich prüft, und verweist für den Verbabgleich auf die neue Prüffunktion. methoden_pruefung.py kommt als zweites Werkzeug dazu. Beide in _pruefung/, nicht im gepackten Plugin.

**Grundlage:** bloom prüft nur K6-Vorkommen und K5-als-Bewerten, nicht den angekündigten Verbabgleich.

**Entschieden von:** David, 07.10.2026

**Betroffen:** Skill unterrichtsmethoden, SKILL.md Zeile 84; methoden_check.py

**Rückgängig:** Satz zurückschreiben

**Stand:** offen, Skillumbau

## E-100 B-071, B-072 Fast-Duplikate in der Methodensammlung

**Optionen:**
1. Je Paar zusammenlegen
2. Beide behalten und gegenseitig verweisen
3. Nur die drei echten Dubletten lösen

**Wahl:** Drei echte Dubletten zusammenlegen: Nr. 248 und 266 auf 248 (bpb ist die belegte Quelle, Varianten von 266 als Variante aufnehmen); Nr. 151 und 252 auf 151 mit K2; Nr. 232 und 280 auf 232. Die aufgegebenen Nummern bleiben frei, die zugehörigen Vaultnotizen werden gelöscht. Vier Paare sind am Eintrag als verschiedene Methoden bestätigt, Nr. 236 und 285 als zwei Durchführungen derselben Grundidee; dort genügt ein Verweis im Feld verwandt.

**Grundlage:** methoden_pruefung.py duplikate mit begründeter Negativliste; Einträge am Original verglichen. Fiktives Interview trägt K2, von David am 07.10.2026 entschieden.

**Entschieden von:** David, 07.10.2026

**Betroffen:** Skill unterrichtsmethoden, references; drei Vaultnotizen

**Rückgängig:** Einträge aus der Sicherung zurückschreiben

**Stand:** im Vault umgesetzt (E-160), im Skill offen (Skillumbau)

## E-101 B-073 Dreizehn Mal Bloom gegen WOZU

**Optionen:**
1. Bloom-Passung an das Zielverb anpassen
2. Zielverb an die Bloom-Passung anpassen
3. Je Fall einzeln entscheiden

**Wahl:** Je Fall einzeln, mit Regel: Wo das WOZU-Feld tiefer liegt als die Bloom-Angabe (Nr. 121, 133, 134, 138, 174, 219, 295, 317, 322), wird die Bloom-Angabe gesenkt. Wo das WOZU höher liegt (Nr. 25, 42, 122, 183), wird das Zielverb ersetzt.

**Grundlage:** methoden_pruefung.py bloomwozu; mehrdeutige Operatoren ausgenommen (B-057)

**Entschieden von:** David, 07.10.2026

**Betroffen:** Skill unterrichtsmethoden, 13 Einträge

**Rückgängig:** Einträge zurückschreiben

**Stand:** offen, Skillumbau, je Fall ein fachlicher Blick

## E-102 B-074, B-075 Eignungsskala und K-Stufen vereinheitlichen

**Optionen:**
1. Skill an den Vault anpassen
2. Vault an den Skill anpassen
3. Lassen

**Wahl:** Im Skill alle «Tief» auf «Gering» setzen, weil der Vault schon so steht und die Mehrheit der Einträge ebenfalls. Bei den K-Stufen gilt der Vault, der Spannen auflöst; im Skill wird die Bloom-Zeile dort auf die Spannenform gebracht, wo der Vault eine Spanne führt.

**Grundlage:** methoden_pruefung.py eignung und synchron; 18 gegen 41 Einträge, 35 K-Stufen-Abweichungen. Ziel ist Exit 0 bei synchron.

**Entschieden von:** David, 07.10.2026

**Betroffen:** Skill unterrichtsmethoden, references

**Rückgängig:** Einträge zurückschreiben

**Stand:** offen, Skillumbau

## E-103 B-076 Erweiterte Kurzdefinition bei Nr. 27

**Optionen:**
1. Vaultnotiz auf den Skillwortlaut zurücksetzen
2. Ergänzung behalten und als Auslegung markieren

**Wahl:** Zurücksetzen. Bei `status: sammlung` heisst das «Inhalt nicht am Original geprüft»; eine eigene Erweiterung gehört dort nicht hin.

**Grundlage:** methoden_pruefung.py synchron: vorher 54 Befunde, nachher 53.

**Entschieden von:** David, 07.10.2026

**Betroffen:** [[Deduktive Verfahren]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-104 B-077, B-078 Methoden, die ihre Lernsituation übersteigen

**Optionen:**
1. Die 36 groben Empfehlungen streichen
2. Alle 161 prüfen
3. Das Feld «Passende BKU1-LS» umbauen
4. Lassen und als Grenze dokumentieren

**Wahl:** Die 36 groben Fälle (Abstand drei) streichen. Die 125 Fälle mit Abstand zwei bleiben und werden als bekannte Grenze dokumentiert, weil Unterricht über das Prüfniveau hinausgehen darf.

**Grundlage:** methoden_pruefung.py lsstufe. Strukturelle Ursache: 13 der 26 Lernsituationen haben als höchstes Ziel K2, 95 der 330 Methoden beginnen erst bei K4. Ein Umbau des Feldes wäre ein Projekt von mehreren Tagen.

**Entschieden von:** David, 07.10.2026

**Betroffen:** Skill unterrichtsmethoden, 36 Einträge

**Rückgängig:** Empfehlungen zurückschreiben

**Stand:** offen, Skillumbau

## E-105 B-079 Nummernlücke Nr. 9

**Optionen:**
1. Grund eintragen oder «nicht dokumentiert» vermerken
2. Nummer neu belegen

**Wahl:** Im Index und im Kommentar des Prüfskripts vermerken, dass Nr. 9 nie belegt war. Die Nummer wird nicht neu belegt.

**Grundlage:** Geprüft in den Plugin-Ständen v0.12.2, v0.13.0, v0.13.2, v0.13.3 und im heutigen Bestand: die Nummer fehlt überall, auch im Index.

**Entschieden von:** David, 07.10.2026

**Betroffen:** Skill unterrichtsmethoden, 00_index.md

**Rückgängig:** entfällt

**Stand:** offen, Skillumbau

## E-106 B-059 Drei Operatoren aus Davids Arbeitswortschatz

**Optionen:**
1. Bauplan erfassen und die Operatoren daraus einordnen
2. Bauplan fallenlassen, die drei Operatoren belegt aufnehmen
3. Nichts tun

**Wahl:** Bauplan fallengelassen, die drei Operatoren aufgenommen: übertragen, berechnen und charakterisieren, alle K3. Die Spalte «Bauplan» entfällt aus der Vergleichstabelle.

**Grundlage:** Der Bauplan ist in keiner Datei auffindbar; David hat ihn am 07.10.2026 fallengelassen. Die drei Operatoren sind am Anforderungsbereich II belegt (KMK 2006, S. 9 bis 12, zitiert in «Operatoren in der beruflichen Bildung», Landesamt für Schule und Bildung Sachsen; für charakterisieren zudem Bildungsserver Mecklenburg-Vorpommern). Bereich II entspricht K3. Lehren und Lernen führt «übertragen» auf K2; David hat K3 entschieden.

**Entschieden von:** David, 07.10.2026

**Betroffen:** [[Operatoren und K-Stufen]] im Vault; im Skill noch offen

**Rückgängig:** Abschnitt «Beschlossene Ergänzungen» entfernen

**Stand:** im Vault umgesetzt, im Skill offen

## E-107 B-085, B-082, B-062 Rangfolge von Bildungsplan und Schullehrplan

**Optionen:**
1. Prüfung nach Bildungsplan, Unterricht nach der höheren Stufe, beide Stufen im Dossier
2. Alles nach Bildungsplan, höhere Aufgaben senken
3. Alles nach Schullehrplan, Bildungsplan nur fürs QV

**Wahl:** Erste Option. Lernkontrollen und QV-Vorbereitung richten sich nach der K-Stufe des Leistungsziels im Bildungsplan. Unterricht, Aufträge und Einstiegsfragen richten sich nach der höheren der beiden Stufen. Im Dossier stehen beide, etwa «a1.7.1 (K2, Bildungsplan) | Verstösse in Beispielen erkennen (K4, Schullehrplan)».

**Grundlage:** Der Schullehrplan zielt in 40 Lernzielen höher, achtmal mit mindestens zwei Quellen belegt (slp_check.py). Der Skill lk-grundlagen verlangt für Prüfungen die K-Stufe des Leistungsziels. Der Master-Korpus nennt das Constructive Alignment und führt Datenschutz ausdrücklich als Beispiel für K1, K2 und K3 am selben Thema. Der Schullehrplan ist für David nicht änderbar. Folge: Eine Frage, die das SLP-Lernziel trifft, ist nicht zu hoch; statt die Frage zu senken wird das Ziel benannt, das sie bedient.

**Entschieden von:** David, 07.10.2026

**Betroffen:** neue Notiz [[Rangfolge Bildungsplan und Schullehrplan]]; Dossiers folgen später

**Rückgängig:** Notiz löschen

**Stand:** Regel umgesetzt, Dossiers offen

## E-108 B-084 Drei falsche Seitenangaben zu Lehren und Lernen

**Optionen:**
1. Am PDF ausmessen und korrigieren

**Wahl:** Korrigiert: die K1-Operatoren stehen auf S. 56, K4 und K5 auf S. 57. K2, K3 und K6 stimmten.

**Grundlage:** Am PDF mit pdftotext ausgemessen, Kopfzeilen als Seitengrenzen.

**Entschieden von:** David, 07.10.2026

**Betroffen:** K1 Wissen, K4 Analysieren, K5 Synthese oder Entwickeln

**Rückgängig:** Seitenangaben zurückschreiben

**Stand:** umgesetzt

## E-109 Lektion planen: Vorbelegung aus der Methode und Word-Datei

**Optionen:**
1. Inhalt aus «Ablauf», «Beschreibung» oder Kurzbeschreibung übernehmen
2. Ergebnissicherung leer lassen mit Hinweis, letzten Ablaufschritt einsetzen oder ein neues Feld in allen Methoden
3. Bei Methodenwechsel nur leere und übernommene Felder füllen oder immer alles ersetzen
4. Herunterladen als HTML, Word-Datei oder PDF

**Wahl:** Wählt man im Werkzeug «Lektion planen» eine Methode, kommt ihr Abschnitt «Ablauf» (ohne Material und Zeit, ein Schritt pro Zeile) ins Feld «Inhalt» und ihr Feld «material» ins Feld «Medien und Material». Gefüllt werden nur leere Felder oder Felder, die noch den übernommenen Text der vorher gewählten Methode tragen; eigener Text bleibt stehen. «Ergebnissicherung» bleibt leer, darunter steht «Im Methodenartikel nicht angegeben». Bei den fünf Methoden ohne «Ablauf» und «Material» bleiben die Felder leer, ohne Hinweis. Neben «Drucken» steht der Knopf «Als Word-Datei herunterladen»: eine Tabelle A4 quer mit denselben Spalten wie der Verlaufsplan, ohne das Arbeitsdossier-Design. Die Seite trägt dafür die Erlaubnis zum Herunterladen.

**Grundlage:** Externe Personen mit Link konnten den Verlaufsplan nicht drucken (Vermutung: das Druckfenster wird in ihrer Ansicht blockiert, nicht geprüft). Die 330 Methoden der Sammlung haben «Ablauf» und «Material»; einen Abschnitt zur Ergebnissicherung hat keine Methode.

**Entschieden von:** David, 13.10.2026

**Betroffen:** 00 Start/Navigator/navigator.py (Teil «Lektion planen»), Basic Skills Version 7

**Rückgängig:** Teil «Lektion planen» in navigator.py auf den Stand vor E-109 zurücksetzen, Seite neu erzeugen und ohne Erlaubnis zum Herunterladen veröffentlichen

**Stand:** umgesetzt; Herunterladen bei externen Personen nicht geprüft

## E-110 B-001 Wiederholung ungenügender Kompetenznachweise

**Optionen:**
1. EHB-Studienverordnung gilt (zweimal)
2. Offen lassen bis zur Antwort der EHB

**Wahl:** Option 1. Die Verordnung steht über Wegleitung, Ausbildungsprogramm und Modulkarte; deren Angabe «einmal» gilt als Fehler dieser Dokumente. Löst E-045 ab.

**Grundlage:** EHB-Studienverordnung, Art. 18 Abs. 6: «Modulprüfungen und Abschlussarbeiten können zweimal wiederholt werden.» (fedlex, Stand am 1. März 2022, im eingebauten Browser abgerufen am 16.10.2026). Modulkarte Modul A ZBKU: S. 13 «einmal», S. 18 «zweimal». Studienplan ZBKU vom 21. März 2024 ohne eigene Regel (Ziff. 7).

**Entschieden von:** David, 16.10.2026

**Betroffen:** [[Wiederholung ungenügender Kompetenznachweise]], [[Qualifikationsverfahren Basismodul A]], neue Notizen [[Quelle EHB-Studienverordnung]], [[Quelle EHB-Modulkarte Modul A]], [[Quelle EHB-Studienplan ZBKU]]

**Rückgängig:** status auf widerspruch zurücksetzen, Abschnitt E-110 entfernen

**Stand:** umgesetzt

## E-111 Befunde mit den Quellen vom 16.10.2026 nachführen

**Optionen:**
1. Den vorgelegten Plan umsetzen
2. Nicht umsetzen

**Wahl:** Option 1: Entscheide E-046 bis E-050, E-080, E-082, E-083 und E-106 in Kurz und Stand der Notizen nachgeführt; Bildungsplan FaBe als Primärquelle der K-Stufen ergänzt; Grundlagen der Rangfolge ergänzt; Autor von Lehren und Lernen und Bibliografie von Städeli/Pfiffner korrigiert; B-019, B-048, B-049, B-050 behoben; Kurz-Felder der Index- und Kontrollnotizen angeglichen; neue Quellennotizen; Stand-Zeile für jeden Befund.

**Grundlage:** am Original geprüft am 16.10.2026: Bildungsplan FaBe (21.8.2020) S. 3 und 4; EHB, PEX-Handbuch, Kap. 4.1.2 und 4.1.3; Strohmeier, Handreichung, S. 8; EHB-Modulkarte Modul A; EHB-Studienpläne ZBKU 2019 und 2024; EHB-Studienverordnung auf fedlex; SAVOIRSOCIAL, BK-Hinweise (Fassung 2.11.2023); Katalogdaten lernmedien-shop und buchkatalog.de.

**Entschieden von:** David, 16.10.2026 («ergänze es im Vault»)

**Betroffen:** alle Notizen mit E-111 im Feld entscheide; Befundliste

**Rückgängig:** Änderungen anhand dieser Liste und der Befundliste zurücknehmen; nach Davids Regel gibt es keine Sicherungskopie

**Stand:** umgesetzt

## E-112 B-086 K-Stufe den Lernenden mitteilen

**Optionen:**
1. Die K-Stufe wird den Lernenden mitgeteilt
2. Nur das Ziel, die K-Stufe nicht

**Wahl:** Option 1. Die K-Stufe wird den Lernenden mitgeteilt; im Dossier stehen nach E-107 beide Stufen. Abweichend vom Skill fertigen-unterricht-planen.

**Grundlage:** Davids Entscheid. Eine Vorgabe dazu wurde am 16.10.2026 nicht gefunden. Das Merkblatt der BFS Basel für schriftliche Prüfungen (V5, 20.10.2025) sagt nur: «Die Lernziele der Lernkontrolle werden den Lernenden in der Regel zwei Wochen davor mitgeteilt.»

**Entschieden von:** David, 16.10.2026

**Betroffen:** [[Feinziele formulieren]], [[Rangfolge Bildungsplan und Schullehrplan]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-113 B-018 Zahl der Unterrichtsbesuche durch die Lehrbegleitung

**Optionen:**
1. Zwei Besuche (Wegleitung Kap. 5, zwei Raster)
2. Ein Besuch (Portfolioliste der Wegleitung, S. 4)
3. Offen lassen

**Wahl:** Option 1, zwei Besuche.

**Grundlage:** Wegleitung Kap. 5 mit zwei Rastern; Modulkarte Modul A ZBKU, S. 14, nennt «Unterrichtsbesuche im eigenen Unterricht durch Lehrbegleitung» im Plural.

**Entschieden von:** David, 16.10.2026

**Betroffen:** [[Unterrichtsbesuch durch Lehrbegleitung]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-114 B-002 und B-003 Umrechnung in das Prädikat und Stufe N

**Optionen:**
1. Schliessen: für Davids Arbeit nicht nötig
2. Offen lassen

**Wahl:** Option 1. Prädikat und Note vergibt die EHB; die Notizen bleiben, wie sie sind.

**Grundlage:** Keine EHB-Quelle nennt Punktgrenzen für A bis F oder regelt N in der Notenformel (Wegleitung, Ausbildungsprogramm, Modulkarte, Studienplan ZBKU 2024, geprüft 16.10.2026).

**Entschieden von:** David, 16.10.2026

**Betroffen:** Befundliste B-002, B-003

**Rückgängig:** Stand-Zeilen zurückschreiben

**Stand:** umgesetzt

## E-115 B-014, B-015, B-020, B-027 am Original geprüft

**Optionen:**
1. Mit den neuen Unterlagen prüfen und schliessen
2. Offen lassen

**Wahl:** Option 1. Städeli/Pfiffner an den Kapitel-PDFs, das Kursmaterial im Ordner EHB/Präsenzveranstaltungen, lk1.pdf im Ordner fachliteratur geprüft; Flaig nach Davids Auskunft. Dazu zwei Operatorenblätter der BFS Basel (Hold 2026, Flaig 2023) in [[Operatoren und K-Stufen]] ergänzt.

**Grundlage:** Unterlagen, die David am 16.10.2026 hochgeladen oder freigegeben hat; Davids Auskunft zu Flaig.

**Entschieden von:** David, 16.10.2026 («wieso überprüfst du es den nicht»)

**Betroffen:** alle Notizen mit E-115 im Feld entscheide; neue Quellennotizen

**Rückgängig:** Ergänzungen anhand dieser Liste entfernen

**Stand:** umgesetzt

## E-116 B-013 Auflage von Lehren und Lernen

**Optionen:**
1. Schliessen: für Davids Arbeit nicht nötig
2. Offen lassen bis zum Impressum

**Wahl:** Option 1. Der Autor ist geklärt (E-111); die Auflage des E-Books bleibt «nicht geprüft».

**Entschieden von:** David, 16.10.2026

**Betroffen:** Befundliste B-013

**Rückgängig:** Stand-Zeile zurückschreiben

**Stand:** umgesetzt

## E-117 B-063, B-064, B-065, B-083, B-067, B-087

**Optionen:**
1. Schliessen: Sache der Dossiers, nicht des Vaults; fehlende Nummern nicht vergeben
2. Offen lassen

**Wahl:** Option 1. Die neuen Einstiegsfragen sind mit E-092 bis E-094 entschieden; ob und wann sie ins Dossier kommen, entscheidet David ausserhalb des Vaults. E-086, E-091, E-095 und E-097 gelten als nicht vergeben.

**Entschieden von:** David, 16.10.2026

**Betroffen:** Befundliste B-063, B-064, B-065, B-067, B-083, B-087

**Rückgängig:** Stand-Zeilen zurückschreiben

**Stand:** umgesetzt

## E-118 Befunde zu Skills und Plugins

**Optionen:**
1. Schliessen: Sache der Skills und Plugins, nicht des Vaults
2. Offen lassen bis zum Skillumbau

**Wahl:** Option 1 für B-016, B-017, B-051, B-054, B-056, B-057, B-068, B-069, B-070, B-071, B-073, B-074, B-075, B-077, B-079, B-081. Die Beschlüsse bleiben im Protokoll; der Skillumbau ist Etappe 8 im Arbeitsplan.

**Entschieden von:** David, 16.10.2026

**Betroffen:** Befundliste

**Rückgängig:** Stand-Zeilen zurückschreiben

**Stand:** umgesetzt

## E-119 Geschlossene Befunde ins Archiv

**Optionen:**
1. Ins Archiv verschieben, leere Befundliste behalten
2. Ganz löschen

**Wahl:** Option 1. B-001 bis B-087 stehen in «Archiv/Befundliste Archiv 2026-10-16»; die Befundliste beginnt neu mit B-088.

**Entschieden von:** David, 16.10.2026

**Betroffen:** [[Befundliste]], [[Befundliste Archiv 2026-10-16]]

**Rückgängig:** Inhalt des Archivs in die Befundliste zurückschreiben

**Stand:** umgesetzt

## E-120 Davids eigenes Material als Quelle

**Optionen:**
1. Davids eigenes Material gilt als Quelle
2. Diese Notizen bleiben «nicht geprüft»

**Wahl:** Option 1, wie bei E-024 für Davids eigene Verfahren. Betrifft Notizen, deren einzige Quelle Davids eigenes Material ist: Selbststudium, eigene Skills, Zusammenstellungen für Basic Skills.

**Entschieden von:** David, 16.10.2026

**Betroffen:** [[Lernprodukt festlegen]], [[Unterrichtsmethoden Übersicht]], [[Verbindungstexte]]

**Rückgängig:** status auf «nicht geprüft» zurücksetzen

**Stand:** umgesetzt

## E-121 Sechs Notizen am Original geprüft

**Optionen:**
1. Prüfen und auf belegt setzen
2. Lassen

**Wahl:** Option 1. Geprüft an Meyer, Leitfaden (S. 102), Meyer, Was ist guter Unterricht? (S. 56), Fehrmann 2019 (Folie 16), Kursmaterial 2025/26, Wegleitung (S. 11 und 13), Städeli/Pfiffner 2018 (Kap. 1) und der Datei Studienskript 8. Berichtigt: das Meyer-Zitat in [[Unterrichtseinheit begründen]] auf den Wortlaut, die Seitenangabe in [[Thema festlegen und Unterrichtseinheit einordnen]] auf S. 102, die Kurzfassung und Indikator 10 in [[Gliederung Vorbereitungsdossier]].

**Entschieden von:** David, 16.10.2026 («ja mach das»)

**Betroffen:** alle Notizen mit E-121 im Feld entscheide

**Rückgängig:** Ergänzungen anhand dieser Liste entfernen

**Stand:** umgesetzt

## E-122 B-088 Verbindungstexte: Operatorenliste im Abschnitt K1

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1 mit Davids Wortlaut: «gilt die Operatorenliste der Aufgabentypen (E-047, präzisiert durch E-080)». Der Satz passiert den Filter von navigator.py unverändert (Probelauf am 16.10.2026). Basic Skills ist nicht neu erzeugt.

**Entschieden von:** David, 16.10.2026 («a1 mit ‹Operatorenliste der Aufgabentypen›»)

**Betroffen:** [[Verbindungstexte]]

**Rückgängig:** «gilt die Operatorenliste der Palette» zurückschreiben

**Stand:** umgesetzt

## E-123 B-089 Prüfungen: Gegenprobe nur bei sieben von neun

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: kurz und «## Kurz» nennen sieben Prüfungen mit Gegenprobe und die Übersichtsskripte; der Satz im Abschnitt «Gegenproben» ist gleich angepasst.

**Entschieden von:** David, 16.10.2026 («a2 bis a8 ja»)

**Betroffen:** [[Prüfungen]]

**Rückgängig:** die Sätze «Jede ist …» und «Darum ist jede …» zurückschreiben

**Stand:** umgesetzt

## E-124 B-090 K6: Kern der Palette zugeschrieben

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Kern als Zitat aus Lehren und Lernen, S. 58; FaBe-Deckelung mit dem Wortlaut des Bildungsplans, S. 4, und dem Ergebnis der Volltextsuche (K6 nur in der Stufenbeschreibung).

**Entschieden von:** David, 16.10.2026 («a2 bis a8 ja»)

**Betroffen:** [[K6 Bewerten oder Beurteilen]]

**Rückgängig:** Kern und Abschnitt «FaBe-Deckelung» zurückschreiben

**Stand:** umgesetzt

## E-125 B-091 Stufe N: Wortlaut und Wirkung

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: neue Kurzfassung; «Klären kann das nur die EHB (B-003)» heisst neu «Prädikat und Note vergibt die EHB (E-114)». Sonst bleibt die Notiz nach E-114 unverändert.

**Entschieden von:** David, 16.10.2026 («a2 bis a8 ja»)

**Betroffen:** [[Stufe N nicht beobachtbar]]

**Rückgängig:** Kurzfassung und Satz zurückschreiben

**Stand:** umgesetzt

## E-126 B-092 PEX-Handbuch 4.1.2 verschärft wiedergegeben

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Wortlaut von 4.1.2 und der Satz «Das ist eine Möglichkeit, keine Obergrenze; der Bildungsplan FaBe enthält Ziele auf K5.»

**Entschieden von:** David, 16.10.2026 («a2 bis a8 ja»)

**Betroffen:** [[Quelle PEX-Handbuch]]

**Rückgängig:** «bis höchstens K4» zurückschreiben

**Stand:** umgesetzt

## E-127 B-093 Index EHB: Vermerk «Widerspruch» veraltet

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Vermerk gestrichen.

**Entschieden von:** David, 16.10.2026 («a2 bis a8 ja»)

**Betroffen:** [[Index EHB-Qualifikation]], [[Wiederholung ungenügender Kompetenznachweise]]

**Rückgängig:** «(Widerspruch)» wieder anfügen

**Stand:** umgesetzt

## E-128 B-094 Einstiegsfrage prüfen: «begründen» nur K4

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: «begründen» K2 bis K4 (E-083).

**Entschieden von:** David, 16.10.2026 («a2 bis a8 ja»)

**Betroffen:** [[Einstiegsfrage prüfen]]

**Rückgängig:** «K4 laut Liste» zurückschreiben

**Stand:** umgesetzt

## E-129 B-095 Notenformel und Sockelwert: 95 Prozent und die Note 6

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Satz zur Rechnung und zur Rundung auf halbe Noten angefügt, als Rechnung gekennzeichnet.

**Entschieden von:** David, 16.10.2026 («a2 bis a8 ja»)

**Betroffen:** [[Notenformel und Sockelwert]]

**Rückgängig:** angefügten Satz entfernen

**Stand:** umgesetzt

## E-130 B-096 Prüfungen: «sieben strittige Operatoren»

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: «sieben mehrdeutigen Operatoren (E-083)».

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Prüfungen]]

**Rückgängig:** «sieben strittigen Operatoren» zurückschreiben

**Stand:** umgesetzt

## E-131 B-097 Einstiegsfrage prüfen: «Welche … darf» auf K3

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Kein Widerspruch, keine Änderung.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Einstiegsfrage prüfen]]

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-132 B-098 Einstiegsfrage prüfen: «Ist es richtig» und «Ist das …»

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Kein Widerspruch, keine Änderung.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Einstiegsfrage prüfen]]

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-133 B-099 Leitfragen-Klammer: Typ 04 im Band K1 bis K2

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Kein Widerspruch, keine Änderung.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Leitfragen-Klammer zur Ergebnissicherung]]

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-134 B-100 Feinziele formulieren: das Verb legt die K-Stufe fest

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Wortlaut nach dem Buch, mit dem Zusatz zu den mehrdeutigen Operatoren, in kurz, «## Kurz» und Tabelle.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Feinziele formulieren]]

**Rückgängig:** «das Tätigkeitswort legt die K-Stufe fest» und «das Verb legt die K-Stufe fest» zurückschreiben

**Stand:** umgesetzt

## E-135 B-101 Planungskette: Bedingungsanalyse einmal pro Klasse

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Kein Widerspruch, keine Änderung.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Planungskette fertigen Unterricht]], [[Bedingungsanalyse]]

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-136 B-102 Planungskette: Stellung der Bedingungsanalyse

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Absatz, der beide Fassungen nebeneinander nennt, ohne eine zu wählen.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Planungskette fertigen Unterricht]]

**Rückgängig:** Absatz entfernen

**Stand:** umgesetzt

## E-137 B-103 Sachanalyse: Bedeutung für die Lernenden

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Kurzfassung ohne diese Bedeutung, mit Hinweis auf E-048; Satz zu den Leitfragen 3 und 4.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Sachanalyse]]

**Rückgängig:** Kurzfassung zurückschreiben, Satz entfernen

**Stand:** umgesetzt

## E-138 B-104 Zeitplanung: Becker-Wert ohne E-050

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Satz zu E-050 angefügt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Zeitplanung einer Lektion]]

**Rückgängig:** Satz entfernen

**Stand:** umgesetzt

## E-139 B-105 Zahl der mehrdeutigen Operatoren nach E-083

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Kein Widerspruch in der Zahl; keine Änderung an Notizen und Protokoll. Der Wortlaut in [[Prüfungen]] ist mit E-130 angepasst.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Operatoren und K-Stufen]], [[K-Stufen im Überblick]]

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-140 B-106 Flaig: weitere Abweichungen von der Liste

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Abweichungen ergänzt; «entwickeln» liegt in der Spanne nach E-083.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Operatoren und K-Stufen]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-141 B-107 Reorganisation und Transfer in zwei Bedeutungen

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Hinweis auf die Herkunft der Zuordnung und auf die zwei Bedeutungen.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Operatoren und K-Stufen]]

**Rückgängig:** Zusätze entfernen

**Stand:** umgesetzt

## E-142 B-108 Hold: «einordnen» auf K4

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Abweichung ergänzt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Operatoren und K-Stufen]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-143 B-109 «begründen» in der Palette bei sechs Typen

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Typen ergänzt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[K-Stufen im Überblick]]

**Rückgängig:** Teilsatz zurückschreiben

**Stand:** umgesetzt

## E-144 B-110 Beschlossene Ergänzungen in K3 und K4

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: drei Einträge ergänzt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[K3 Anwenden]], [[K4 Analysieren]]

**Rückgängig:** Einträge entfernen

**Stand:** umgesetzt

## E-145 B-111 Methodensammlung: Nummer 49 frei

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Tabelle «16 bis 96 (ohne 49)» und Satz zu den freien Nummern 9 und 49.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Unterrichtsmethoden Übersicht]]

**Rückgängig:** Tabelle und Satz zurückschreiben

**Stand:** umgesetzt

## E-146 B-112 Typ 19: Titelkonvention mit K-Stufe

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Titel «Aufgabe N (Selbstreflexion)» ohne K-Stufe, als Ausnahme zu E-046; [[Aufgabentypen Übersicht]] nennt alle ausser Typ 19 mit K-Stufe.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Aufgabentyp 19 Selbstreflexion]], [[Aufgabentypen Übersicht]]

**Rückgängig:** Titelkonvention und Kurzfassung zurückschreiben

**Stand:** umgesetzt

## E-147 B-113 Musterlösung bei offenen Typen

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Liste der Typen ohne Musterlösung nach der Palette.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Aufgabentypen Übersicht]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-148 B-114 QV-Notiz: vier Operatoren fehlten

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Überschrift der Zeile präzisiert, vier Operatoren ergänzt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Operatoren im QV gegen Operatoren im Unterricht]]

**Rückgängig:** Zeile zurückschreiben

**Stand:** umgesetzt

## E-149 B-115 Rangfolge: Verteilung der 32 Einzelquellen-Fälle

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Satz mit der Verteilung.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Rangfolge Bildungsplan und Schullehrplan]]

**Rückgängig:** Satz zurückschreiben

**Stand:** umgesetzt

## E-150 B-116 Rangfolge: Feinziele «ohne Rangfolge»

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Kein Widerspruch, keine Änderung.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Rangfolge Bildungsplan und Schullehrplan]]

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-151 B-117 aviva_phase von Typ 15 und Typ 2

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Typ 15 Auswerten, Typ 2 dazu Verarbeiten. E-052 gilt für Methoden; die Aufgabentypen führen keine Phasennotizen im Feld verwandt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Aufgabentyp 15 Problembasierte Aufgabe]], [[Aufgabentyp 02 Kreuzworträtsel oder Begriffsnetz]]

**Rückgängig:** Feldwerte zurückschreiben

**Stand:** umgesetzt

## E-152 B-118 Problem-based Learning: eigener AVIVA-Durchlauf

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: alle fünf Phasen wie bei Projektunterricht; verwandt nach E-052 um vier Phasennotizen ergänzt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Problem-based Learning (AVIVA)]]

**Rückgängig:** Feldwerte zurückschreiben

**Stand:** umgesetzt

## E-153 B-119 Tiefste EHB-Note nach Lesart B

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Kurzfassung mit 2.25 für durchgehend Stufe 1 und 1.87 nach Lesart B; Rechnung im Abschnitt «Folgerungen».

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Notenformel EHB-Kompetenznachweise]]

**Rückgängig:** Kurzfassung zurückschreiben, Satz entfernen

**Stand:** umgesetzt

## E-154 B-120 Fachgespräch: Wortlaut der Kriterien

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Kriterien im vollen Wortlaut der Wegleitung.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Fachgespräch 01 Kritische Beurteilung]], [[Fachgespräch 02 Erlebte Beziehungen]], [[Fachgespräch 03 Rollenvielfalt]], [[Fachgespräch 04 Weiterentwicklung]]

**Rückgängig:** Zeilen zurückschreiben

**Stand:** umgesetzt

## E-155 B-121 Checkliste Gütecheck gegen E-107

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Leitfrage nach E-107, Verweis auf [[Rangfolge Bildungsplan und Schullehrplan]].

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Checklisten Gütecheck einer Lernkontrolle]]

**Rückgängig:** Leitfrage zurückschreiben

**Stand:** umgesetzt

## E-156 B-122 Indikator 04: Auslegung als Wortlaut

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Wortlaut des Indikators, Auslegung als solche gekennzeichnet; Quelle und auslegung: true ergänzt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Persönliche Entwicklungsaufgabe]]

**Rückgängig:** Satz und Felder zurückschreiben

**Stand:** umgesetzt

## E-157 B-123 Stichproben: kurz ungleich «## Kurz»

**Optionen:**
1. Vorschlag übernehmen
2. Lassen

**Wahl:** Option 1: Feld kurz gleich dem Abschnitt.

**Entschieden von:** David, 16.10.2026 («b. nehme alle deine empfehlunge an»)

**Betroffen:** [[Stichproben]]

**Rückgängig:** alten Wert zurückschreiben

**Stand:** umgesetzt

## E-158 Etappen 3, 4 und 6, Nachführung der Kontrollnotizen

**Optionen:**
1. Etappen 3, 4 und 6 streichen
2. Etappen 4 und 6 streichen, Etappe 3 behalten und anschliessen
3. Alle offen lassen

**Wahl:** Option 2. Etappe 3 (satzgenaue Prüfung von Zahlen, Notenregeln und EHB-Indikatoren, E-060) folgt als nächster Auftrag, zuerst Ordner 70 und 50. Etappe 4 (Verweiszeile in den Skills, E-067) und Etappe 6 (Vorschläge für Tresor und fachliteratur) entfallen. [[Arbeitsplan]], [[Stand]], [[Übergabe]] und [[Befundliste]] sind nachgeführt.

**Entschieden von:** David, 16.10.2026 («c1 ja»)

**Betroffen:** [[Arbeitsplan]], [[Stand]], [[Übergabe]], [[Befundliste]]

**Rückgängig:** Etappen 4 und 6 in den Arbeitsplan zurückschreiben

**Stand:** umgesetzt

## E-159 Methodensammlung bleibt Sammlung

**Optionen:**
1. Status «sammlung» behalten (E-059)
2. Methoden am Original prüfen

**Wahl:** Option 1. E-059 bleibt; «sammlung» ist kein Befund.

**Entschieden von:** David, 16.10.2026 («c2 ja»)

**Betroffen:** Methodensammlung, [[Stand]]

**Rückgängig:** entfällt

**Stand:** umgesetzt

## E-160 E-100 im Vault umgesetzt

**Optionen:**
1. Jetzt im Vault umsetzen
2. Mit dem Skillumbau

**Wahl:** Option 1. Zuordnung nach dem Feld nr und dem Wortlaut von E-100: Nr. 266 «Argumentationsmap» geht in Nr. 248 [[Auf den Punkt gebracht Argumentations-Map]] auf, Nr. 252 «Kreative Textarbeit Fiktives Interview» in Nr. 151 [[Fiktives Interview]], Nr. 280 «Rotierendes Partner*ingespräch» in Nr. 232 [[Rotierendes Partnergespräch (bpb-Fassung)]]. Was die aufgegebenen Notizen zusätzlich enthielten, steht im neuen Abschnitt «Variante» der Zielnotiz, die Quellenzeilen sind übernommen. Nr. 151 trägt nur noch K2: Feld k_stufe K2, im Feld verwandt fallen K3 und K4 weg (E-052), der Text nennt K2 als Stufe. Die drei aufgegebenen Notizen liegen im macOS-Papierkorb; Wikilinks auf sie gab es keine, die Nennungen im Archiv bleiben als historischer Stand. Die Methodensammlung zählt 327 Notizen; die Zahl ist in [[Unterrichtsmethoden Übersicht]], [[Index Methoden und Medien]], CLAUDE.md und [[Stand]] nachgeführt.

**Entschieden von:** David, 16.10.2026 («c3 ja»); Lesart von «mit K2»: David, 16.10.2026 («ja, nur K2»)

**Betroffen:** [[Auf den Punkt gebracht Argumentations-Map]], [[Fiktives Interview]], [[Rotierendes Partnergespräch (bpb-Fassung)]], [[Unterrichtsmethoden Übersicht]], [[Index Methoden und Medien]], CLAUDE.md, [[Stand]]

**Rückgängig:** die drei Notizen aus dem Papierkorb zurücklegen, Abschnitte «Variante» und Quellenzeilen entfernen, 330 zurückschreiben

**Stand:** im Vault umgesetzt; im Skill offen (Skillumbau)

## E-161 B-124 Lernungewohnte Lernende, nicht verlinkt

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: im [[Index Lernende und Gruppen]] unter «Lernen» aufgenommen.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Index Lernende und Gruppen]], [[Lernungewohnte Lernende]]

**Rückgängig:** Link im Index entfernen

**Stand:** umgesetzt

## E-162 B-125 Einstiegsfrage prüfen, Zahl der Stufen

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: «drei Stufen Unterschied».

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Einstiegsfrage prüfen]]

**Rückgängig:** «zwei» zurückschreiben

**Stand:** umgesetzt

## E-163 B-126 Titelformat ohne Ausnahme für Typ 19

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: Ausnahme in beiden Notizen ergänzt.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Aufgabentypen Übersicht]], [[Checklisten Gütecheck einer Lernkontrolle]]

**Rückgängig:** Zusätze entfernen

**Stand:** umgesetzt

## E-164 B-127 Hold, weitere Abweichungen

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: Abweichungen ergänzt.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Operatoren und K-Stufen]]

**Rückgängig:** Satz entfernen

**Stand:** umgesetzt

## E-165 B-128 Quellenpfade von Flaig, Hold und Palette

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: Pfade eingetragen und als geprüft vermerkt.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Quelle BFS Methodenblatt Operatoren Flaig]], [[Quelle BFS Operatoren-Tabelle Hold]], [[Quelle Aufgabentypen-Palette]]

**Rückgängig:** Pfadzeilen zurückschreiben

**Stand:** umgesetzt

## E-166 B-129 Prüfskripte nicht lauffähig

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: Die Skripte suchen den neusten installierten Stand selbst (am 16.10.2026: 0.16.1), fehlende Dateien geben Exit 2. Gegenprobe mit künstlichem Pluginordner. Tabelle in [[Prüfungen]] mit dem Lauf vom 16.10.2026. Die Menge MEHRDEUTIG in methoden_pruefung.py ist nicht geändert.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Prüfungen]]

**Rückgängig:** frühere Fassung der vier Skripte zurückschreiben

**Stand:** umgesetzt

## E-167 B-130 Basic Skills, Aktualisierung und Schriften

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: Ständige Freigabe, Basic Skills nach jeder Änderung im Vault neu zu erzeugen und an dieselbe Adresse zu veröffentlichen. Die drei Teilschriften aus der veröffentlichten Seite liegen in «00 Start/Navigator/Schriften» und decken alle im Vault benutzten Zeichen ab (Abgleich am 16.10.2026). CLAUDE.md nennt den Aufruf.

**Entschieden von:** David, 16.10.2026 («hier das dokument für das automatische aktualisieren. schliesse alle lücken, wo es nur geht.»)

**Betroffen:** [[CLAUDE]], [[Übergabe]]

**Rückgängig:** Freigabe zurücknehmen, Ordner Schriften entfernen, Zeile in CLAUDE.md zurückschreiben

**Stand:** umgesetzt

## E-168 Kontrollnotizen nach dem Lückenschluss

**Optionen:**
1. Nachführen

**Wahl:** Option 1. [[Befundliste]], [[Stand]], [[Arbeitsplan]] und [[Übergabe]] nennen B-124 bis B-130 und E-161 bis E-168.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Befundliste]], [[Stand]], [[Arbeitsplan]], [[Übergabe]]

**Rückgängig:** Nachführungen zurückschreiben

**Stand:** umgesetzt

## E-169 B-131 Basic Skills, Filter für Skill-Verweise

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: 31 Ersatzeinträge in navigator.py, auf der Seite nach Davids Wortwahl «Operatorenliste der Aufgabentypen»; «00 Start/Prüfungen» ist von der Seite ausgeschlossen. Danach 0 Verweise auf Claude, Skills oder Plugins und keine Ablageangaben; übrig bleibt «welche Skills weiterentwickeln» als Inhalt einer Leitfrage. Der Vault selbst bleibt unverändert.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[CLAUDE]], navigator.py

**Rückgängig:** frühere Fassung von navigator.py zurückschreiben

**Stand:** umgesetzt

## E-170 B-132 Rangfolge, Tippfehler

**Optionen:**
1. Lücke schliessen
2. Lassen

**Wahl:** Option 1: «Acht».

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Rangfolge Bildungsplan und Schullehrplan]]

**Rückgängig:** «Achte» zurückschreiben

**Stand:** umgesetzt

## E-171 Kontrollnotizen nach Basic Skills

**Optionen:**
1. Nachführen

**Wahl:** Option 1. [[Befundliste]], [[Stand]], [[Arbeitsplan]] und [[Übergabe]] nennen B-131, B-132 und E-169 bis E-171.

**Entschieden von:** David, 16.10.2026 («schliesse alle lücken, wo es nur geht»)

**Betroffen:** [[Befundliste]], [[Stand]], [[Arbeitsplan]], [[Übergabe]]

**Rückgängig:** Nachführungen zurückschreiben

**Stand:** umgesetzt

## E-172 B-133 Mehrdeutige Operatoren im Prüfskript der Methodensammlung

**Optionen:**
1. MEHRDEUTIG auf die sieben Operatoren aus E-083 umstellen
2. Lassen

**Wahl:** Option 1. MEHRDEUTIG umfasst begründen, einordnen, entwickeln, erschliessen, erarbeiten, gestalten und vergleichen; einordnen, entwickeln und vergleichen sind aus VERB_STUFE genommen, damit sie nicht zugleich mit fester Stufe zählen; einschätzen steht in VERB_STUFE auf K4 wie in der Operatorenliste. Der Kommentar nennt E-083 statt B-056. Wirkung im Lauf vom 16.10.2026: bloomwozu weiter 13 Befunde; Nr. 330 «Zeitstrahl» entfällt, Nr. 183 «Kennst du mich?» (einschätzen K4 gegen Bloom K2) kommt dazu.

**Entschieden von:** David, 16.10.2026 («ja, MEHRDEUTIG auf die sieben Operatoren aus E-083 umstellen und den Kommentar berichtigen»)

**Betroffen:** methoden_pruefung.py, [[Prüfungen]], [[Befundliste]], [[Stand]], [[Arbeitsplan]], [[Übergabe]]

**Rückgängig:** frühere Menge und VERB_STUFE zurückschreiben

**Stand:** umgesetzt

## E-173 B-134 EHB-Indikatoren: Skill-Auslegung kennzeichnen

**Optionen:**
1. Kurzfassungen und betroffene Hinweise mit «laut Skill» oder «Laut Auslegung Skill …» kennzeichnen, den belegten Teil aus dem Wortlaut voranstellen
2. Lassen

**Wahl:** Option 1. Höchstens drei Sätze je Kurzfassung; Prüffragen und Stolpersteine nur, wo sie etwas über Indikator, Stufe oder Raster sagen. In [[Fachgespräch 04 Weiterentwicklung]] trägt die Stufentabelle jetzt wie der Skill «aus der gehaltenen Sequenz abgeleitet».

**Entschieden von:** David, 16.10.2026 («ja setze alles um» und «ok» auf die angekündigte Umsetzung aller nachgeprüften Funde)

**Betroffen:** alle Notizen mit E-173 im Feld entscheide (32)

**Rückgängig:** Kennzeichnungen entfernen, frühere Kurzfassungen zurückschreiben

**Stand:** umgesetzt

## E-174 B-135 EHB-Wortlaut vervollständigen

**Optionen:**
1. Kriteriumsnamen, Ziele der Modelllektion und Leitfragen im vollen Wortlaut der Wegleitung
2. Lassen

**Wahl:** Option 1. Kriterium 2 der Vorbereitung mit «bzw. HF-Studierenden», Kriterium 3 mit «der zu unterrichtenden Themen», Kriterium 3 der Lehrprobe mit «zwischen der Lehrperson, den Lernenden und der Klassengemeinschaft»; die Leitfragen stehen ungekürzt (E-010 erlaubte Kürzungen, die Umformulierungen deckte es nicht). [[Themenwahl Lehrprobe]]: Überschrift «Vorgaben» statt «Wortlaut». [[Stufe N nicht beobachtbar]]: Zitat ungebeugt.

**Entschieden von:** David, 16.10.2026 («ja setze alles um»)

**Betroffen:** alle Notizen mit E-174 im Feld entscheide (13)

**Rückgängig:** gekürzte Fassungen zurückschreiben

**Stand:** umgesetzt

## E-175 B-136 Bezugssituation als Auslegung kennzeichnen

**Optionen:**
1. Zeile im Abschnitt «Wortlaut» mit «Zuordnung laut Skill …, Auslegung, nicht Wortlaut der Wegleitung» ergänzen, Feld bezugssituation behalten
2. Feld und Zeile streichen
3. Lassen

**Wahl:** Option 1. Das Feld bezugssituation bleibt als Suchfeld (E-008).

**Entschieden von:** David, 16.10.2026 («ja setze alles um»)

**Betroffen:** alle Notizen mit E-175 im Feld entscheide (12)

**Rückgängig:** Zusatz in Klammern entfernen

**Stand:** umgesetzt

## E-176 B-137 EHB-Vorgaben in der Verbindlichkeit der Quelle

**Optionen:**
1. Wortwahl und Umfang an die Wegleitung angleichen
2. Lassen

**Wahl:** Option 1. «soll» bleibt «soll», «Richtgrösse» bleibt Richtgrösse, Beispiele bleiben Beispiele; Titelblatt und Titel der Nachweise vollständig; Indikator 01 mit Quellenangaben, Orthografie und Syntax; Empfänger des Dossiers mit Lehrbegleitung; Kompetenzprofil mit «im Ausbildungsprogramm A bis I und M»; Modelllektion mit dem Hinweis, dass die Obergrenzen des Skill-Vorschlags 47 Minuten ergeben.

**Entschieden von:** David, 16.10.2026 («ja setze alles um»)

**Betroffen:** alle Notizen mit E-176 im Feld entscheide (10)

**Rückgängig:** frühere Wortwahl zurückschreiben

**Stand:** umgesetzt

## E-177 B-138 Seitenangaben in Ordner 70

**Optionen:**
1. Feld quelle um die fehlenden Seiten ergänzen
2. Lassen

**Wahl:** Option 1.

**Entschieden von:** David, 16.10.2026 («ja setze alles um»)

**Betroffen:** alle Notizen mit E-177 im Feld entscheide (7)

**Rückgängig:** Seitenangaben zurückschreiben

**Stand:** umgesetzt

## E-178 B-139 Prüfen und Bewerten: Skill-Aussagen kennzeichnen, Belege zuschreiben

**Optionen:**
1. Skill-Regeln mit «laut Skill» kennzeichnen; was in einer lokalen Primärquelle steht, dieser Quelle zuschreiben
2. Lassen

**Wahl:** Option 1.

**Entschieden von:** David, 16.10.2026 («ja setze alles um»)

**Betroffen:** alle Notizen mit E-178 im Feld entscheide (11)

**Rückgängig:** Kennzeichnungen und Zuschreibungen zurückschreiben

**Stand:** umgesetzt

## E-179 B-140 Seitenangaben in Ordner 50

**Optionen:**
1. Seiten und Folien im Feld quelle berichtigen und ergänzen
2. Lassen

**Wahl:** Option 1.

**Entschieden von:** David, 16.10.2026 («ja setze alles um»)

**Betroffen:** alle Notizen mit E-179 im Feld entscheide (12)

**Rückgängig:** Seitenangaben zurückschreiben

**Stand:** umgesetzt

## E-180 B-141 Prüfen und Bewerten: Abweichungen berichtigen

**Optionen:**
1. An die Quelle angleichen
2. Lassen

**Wahl:** Option 1. Fünf «Todsünden»; erste Portfoliophase mit Biografiearbeit, Planung der Lehrperson davor; Flaigs Raster mit ausformulierten Deskriptoren.

**Entschieden von:** David, 16.10.2026 («ja setze alles um»)

**Betroffen:** [[Benotungsregeln und Sechserbremse]], [[Portfolio als Prüfungsform]], [[Raster-Bibliothek nach Flaig]]

**Rückgängig:** frühere Fassungen zurückschreiben

**Stand:** umgesetzt

## E-181 B-142, B-143 Widersprüche ausweisen

**Optionen:**
1. Beide Fassungen in die Notiz, status widerspruch, Auflösung durch David
2. Selbst auflösen

**Wahl:** Option 1, nach der Belegregel der CLAUDE.md. [[Bezugsnormen]] und [[Erwartungshorizont und Punkte]] tragen status widerspruch und einen Abschnitt «Widerspruch»; [[Deskriptorenraster bauen]] verweist auf B-143.

**Entschieden von:** David, 16.10.2026 («ja setze alles um»); welche Fassung gilt, ist offen

**Betroffen:** [[Bezugsnormen]], [[Erwartungshorizont und Punkte]], [[Deskriptorenraster bauen]]

**Rückgängig:** Abschnitte «Widerspruch» entfernen, status belegt

**Stand:** umgesetzt; aufgelöst mit E-183 und E-184

## E-182 Kontrollnotizen nach Etappe 3

**Optionen:**
1. Nachführen

**Wahl:** Option 1. [[Befundliste]], [[Stand]], [[Arbeitsplan]] und [[Übergabe]] nennen B-134 bis B-144 und E-173 bis E-182. Für Basic Skills (E-167, E-169) hat navigator.py Ersatzeinträge für die neuen Kennzeichnungen erhalten: Auf der Seite wird «Laut (Auslegung) Skill qub-…» zu «Laut Auslegung», Skill-Regeln in Ordner 50 stehen ohne Verweis, der Hinweis auf die Flaig-Raster fällt weg (Entscheid 30.09.2026). Veröffentlicht als Version 9 am 16.10.2026; auf der Seite bleiben «Skill» nur im Titel und in der Leitfrage «welche Skills weiterentwickeln».

**Entschieden von:** David, 16.10.2026 («ja setze alles um»; Veröffentlichung nach E-167)

**Betroffen:** [[Befundliste]], [[Stand]], [[Arbeitsplan]], [[Übergabe]], navigator.py

**Rückgängig:** Nachführungen zurückschreiben

**Stand:** umgesetzt

## E-183 B-142 Individuelle Norm bei summativen Beurteilungen

**Optionen:**
1. Lehren und Lernen folgen: für summative Beurteilungen nicht erlaubt
2. Strohmeier folgen: für die summative Leistungsbeurteilung ebenso wichtig
3. Offen lassen

**Wahl:** Option 1, wie empfohlen, weil Erfahrungsnoten summativ sind; der Skill lk-grundlagen folgt ebenfalls Lehren und Lernen. [[Bezugsnormen]] trägt wieder status belegt; Strohmeiers Fassung steht als Gegenposition im Abschnitt «Entscheid zum Widerspruch».

**Entschieden von:** David, 16.10.2026 («1 deine empfehlungen»)

**Betroffen:** [[Bezugsnormen]], [[Befundliste]]

**Rückgängig:** status widerspruch und Abschnitt «Widerspruch» zurückschreiben

**Stand:** umgesetzt

## E-184 B-143 Gewichtung über die Punktevergabe

**Optionen:**
1. Strohmeier folgen: Punkte nach Anspruchsniveau, Relevanz und Bearbeitungszeit gewichten
2. Lehren und Lernen folgen: nicht über Punkte gewichten, über die Auswahl der Aufgaben steuern
3. Offen lassen

**Wahl:** Option 1, wie empfohlen, weil es Material der BFS-Tagung ist; der Skill lk-raster gewichtet ebenso. [[Erwartungshorizont und Punkte]] trägt wieder status belegt; [[Deskriptorenraster bauen]] nennt den Entscheid.

**Entschieden von:** David, 16.10.2026 («1 deine empfehlungen»)

**Betroffen:** [[Erwartungshorizont und Punkte]], [[Deskriptorenraster bauen]], [[Befundliste]]

**Rückgängig:** status widerspruch und Abschnitt «Widerspruch» zurückschreiben

**Stand:** umgesetzt

## E-185 B-144 Städeli/Pfiffner nicht auf dem Rechner

**Optionen:**
1. Kap. 1 und 6 nochmals hochladen und die 16 Sätze satzgenau prüfen
2. Lassen

**Wahl:** Option 2. Die Sätze bleiben, wie sie sind; sie sind auf Fundstellenebene belegt (Quellennotiz), satzgenau nicht geprüft.

**Entschieden von:** David, 16.10.2026 («2. lass es»)

**Betroffen:** [[Befundliste]]

**Rückgängig:** Kapitel hochladen und die Sätze prüfen

**Stand:** umgesetzt

## E-186 Umfang von Etappe 3 nach den Ordnern 70 und 50

**Optionen:**
1. Nur die Ordner 40 und 20 satzgenau prüfen, die übrigen streichen
2. Alle übrigen Ordner prüfen
3. Etappe 3 beenden

**Wahl:** Option 1, wie empfohlen. Für die Ordner 10, 30, 60 und 80 entfällt die satzgenaue Prüfung; dort heisst «belegt» weiter Fundstelle geprüft (E-003). [[Arbeitsplan]], [[Stand]], [[Übergabe]] und [[Befundliste]] sind nachgeführt; Basic Skills ist mit E-183 bis E-186 als Version 10 veröffentlicht (E-167).

**Entschieden von:** David, 16.10.2026 («3. ok»)

**Betroffen:** [[Arbeitsplan]], [[Stand]], [[Übergabe]], [[Befundliste]]

**Rückgängig:** übrige Ordner in den Arbeitsplan zurückschreiben

**Stand:** umgesetzt

## E-187 B-145 Restverweise auf der Seite Basic Skills

**Optionen:**
1. Nur auf der Seite ersetzen, über Einträge in navigator.py; Ordner-Erwähnungen ohne Pfad lassen
2. Wie 1, dazu die Ordner-Erwähnungen ausser im Artikeltitel neutral ersetzen
3. In den Notizen ändern

**Wahl:** Option 1, wie empfohlen. In navigator.py: zwei ERSATZ-Einträge («lk-grundlagen», «fertigen-unterricht-planen»), sieben SEITE_ERSATZ-Einträge («lk1.pdf», die Skriptnamen in zwei Sätzen, «03_taxonomie-operatoren.md», «260303_ppt», «Methoden.base» wird «Methodenfinder»), Vorschlaege_ausserhalb und Methoden.base in SEITE_OHNE (Linkziele ohne Artikel), in SEITE_ZEILE_WEG die Zeile zu Vorschlaege_ausserhalb und reine Einbettungszeilen, dazu der Kommentar «Einstiege der Startseite» in VORLAGE. Die Notizen behalten die Herkunftsangaben (E-072).

**Entschieden von:** David, 17.10.2026 («ja, alles so eintragen und die Ordner-Erwähnungen lassen»)

**Betroffen:** navigator.py, [[Befundliste]]; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV

**Rückgängig:** die Einträge mit E-187 aus navigator.py entfernen, Seite neu erzeugen und veröffentlichen

**Stand:** umgesetzt; als Version 11 am 17.10.2026 veröffentlicht (E-167). Suche in der veröffentlichten Fassung: keiner der genannten Verweise mehr vorhanden.

## E-188 Basic Skills: kleine Fassung des neuen Designs

**Optionen:**
1. Kleine Fassung: nur das neue Aussehen auf allen bestehenden Seiten
2. Volle Fassung nach der Vorgabe (Merkliste, Befehlspalette, Dunkelmodus, Bottom-Sheet, Lesefortschritt, neue Grafiken, Ziehen im Zeitbalken)

**Wahl:** Option 1. Grundlage ist die Vorgabe «Skills webpage redesign» (README des Design-Handoffs). In navigator.py, nur in VORLAGE: Farben, Radien und Schatten als CSS-Variablen, gerundete Karten, Chips als Pillen, Knöpfe und Eingabefelder neu, Tabellen mit braunem Kopf und runden Ecken, Phasen- und Stufenfarben an Chips und Phasenkarten, Statuspunkte; neuer Kopf mit Logo-Kachel und Navigation mit Icons; das Icon-Sprite der Vorgabe ist eingebettet, ohne seinen Herkunftsblock (C2PA-Metadaten mit Herstellerangabe, E-072); Icons an Einstiegskacheln, rotem Faden, Bereichen, Steckbrief und den Köpfen der vier Werkzeuge; Hauptknopf je Bereich in Braun. Nicht umgesetzt: alle neuen Funktionen und Grafiken aus Option 2. Adressen, Texte, Werkzeugabläufe, Druckansicht und die Regeln E-072 und E-075 bleiben.

**Entschieden von:** David, 17.10.2026 (Umfang mit dem Auftrag; Aussehen nach der privaten Vorschau freigegeben: «ja, das Aussehen ist freigegeben, mach die Abnahme und veröffentliche»)

**Betroffen:** navigator.py; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV

**Rückgängig:** VORLAGE in navigator.py auf den Stand von Version 11 zurücksetzen, Seite neu erzeugen und veröffentlichen

**Stand:** umgesetzt; als Version 12 am 17.10.2026 veröffentlicht (E-167). Abnahme: Erzeugen Exit 0, JavaScript-Syntax Exit 0, Sichtkontrolle bei 390, 820 und 1280 px (Hauptseite, Artikel, Methodenfinder), Suche nach E-072 und E-075 ohne neue Treffer; die Prüfungen in «00 Start/Prüfungen» unverändert gegenüber dem 16.10.2026. Nicht angesehen: Druckansicht der Werkzeuge, Seite ohne Browserspeicher.

## E-189 Merkmal 9 am Kapitel ausbauen

**Optionen:**
1. Notiz am Kapitel ausbauen, mit allem, was der Vault dazu enthält, und die Spannung zu den Bezugsnormen als eigenen Abschnitt mit gekennzeichneter Lesart
2. Lassen

**Wahl:** Option 1. [[Merkmal 9 Transparente Leistungserwartungen]] neu geschrieben: Leistungsbegriff, Arbeitsdefinition, Leistungsbereitschaft, vier Teilmerkmale, die vierzehn Indikatoren nach dem Buch, Forschungsergebnisse, sechs Ratschläge, Fazit, Leseempfehlungen, Bezüge in den Vault und zur EHB, Lücken; Abschnitt «Spannung zu den Bezugsnormen» mit der Lesart als Vorschlag (B-146). Die Indikatoren laut Skill sind durch den Wortlaut des Buchs ersetzt. Geprüft am Kapitelauszug S. 145–154, den David am 19.10.2026 hochgeladen hat (Impressumszeile «© 2025 Cornelsen»); das PDF aus [[Quelle Was ist guter Unterricht]] wurde nicht geöffnet.

**Entschieden von:** David, 19.10.2026 («1. ja baue es bitte aus mit allem was du finden konntest. 2. ja.»)

**Betroffen:** [[Merkmal 9 Transparente Leistungserwartungen]], [[Befundliste]]

**Rückgängig:** Notiz auf die frühere Fassung zurücksetzen: kurz und Abschnitt «Kurz» «Klar kommuniziert wird, was erwartet und wie beurteilt wird und wo jemand steht, auf Basis der drei Bezugsnormen. Lernphasen, in denen Fehler produktiv sind, werden von notenrelevanten Überprüfungen getrennt.», dann «**Funktion:** Stärkung der Leistungsbereitschaft.», Abschnitt «Indikatoren (Auswahl, Prüfsteine laut Skill nach Meyer)» mit «Leistungserwartungen werden an den Aufgaben besprochen; Schwierigkeitsgrad und Pensum sind bekannt; auch Schwächere verstehen, was verlangt ist; verschiedene Formen der Leistungsüberprüfung; zügige, differenzierte formative Rückmeldungen; realistische Selbsteinschätzung der Lernenden.» und dem Satz zum hermeneutischen Dreischritt; quelle nur Meyer S. 145–154 und Skill guter-unterricht; entscheide nur E-088; verwandt nur Guter Unterricht nach Meyer, Sicht- und Tiefenstruktur, Bezugsnormen, Lehrprobe 07 Zielbezug der Aufgaben, Feedback und Kritik; ohne auslegung. B-146 entfernen.

**Stand:** umgesetzt

## E-190 B-147, B-148, B-158 Kontrollnotizen und Basic Skills nachführen

**Optionen:**
1. Kontrollnotizen nachführen, Befunde ab B-147 eintragen, Basic Skills neu veröffentlichen
2. Lassen

**Wahl:** Option 1. [[Stand]], [[Übergabe]] und der Archivhinweis der [[Befundliste]] sind nachgeführt; Basic Skills wird nach allen Änderungen dieses Tages neu erzeugt und an dieselbe Adresse veröffentlicht (E-167). Die Frage, ob Version 11 und 12 am 16. oder 17.10.2026 veröffentlicht wurden (B-158), bleibt ungeklärt, weil die Neuveröffentlichung den Punkt erledigt.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** [[Stand]], [[Übergabe]], [[Befundliste]]; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV

**Rückgängig:** Kontrollnotizen auf den Stand vom 17.10.2026 zurücksetzen; frühere Version der Seite wiederherstellen

**Stand:** umgesetzt. Die Veröffentlichung war wegen «laut Auslegung qub-lehrprobe» aus [[Merkmal 9 Transparente Leistungserwartungen]] angehalten (B-148); nach E-203 am 22.10.2026 als Version 13 veröffentlicht. Suche in der erzeugten Seite nach Skill-Namen, Claude, Pfaden und Dateiendungen ohne Treffer; «Skill» steht nur im Namen «Basic Skills» und einmal als gewöhnliches Wort («welche Skills weiterentwickeln»).

## E-191 B-146 Meyers Bezugsnormen

**Optionen:**
1. Erste Lesart: Meyers Abwechseln gilt für formative Rückmeldungen, summativ bleibt es kriterial
2. Zweite Lesart: hohe Erwartungen an das Lernen, keine Erwartungen in der Bewertung
3. Beide
4. Keine

**Wahl:** Option 1, dazu Meyer als Gegenposition in [[Bezugsnormen]], wie Strohmeier bei B-142. In [[Merkmal 9 Transparente Leistungserwartungen]] ist der Vorschlag durch die entschiedene Lesart ersetzt; die zweite Lesart (Pygmalion-Effekt) gilt nicht und ist entfernt. In [[Bezugsnormen]] neu: Abschnitt «Gegenposition Meyer» mit den Zitaten S. 150 und 153–154 aus Merkmal 9, quelle Meyer, verwandt Merkmal 9.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** [[Bezugsnormen]], [[Merkmal 9 Transparente Leistungserwartungen]], [[Befundliste]]

**Rückgängig:** In Merkmal 9 den Absatz zur Lesart zurücksetzen auf: «**Vorschlag zur Lesart, nicht aus den Quellen, Entscheid offen (B-146):** Meyers Abwechseln der Bezugsnormen gilt für formative Rückmeldungen; summative Beurteilungen bleiben kriterial nach E-183. Ebenso beim Pygmalion-Effekt: Meyer will hohe Erwartungen an das Lernen nutzen, [[Beurteilungsfehler]] führt denselben Mechanismus als Erwartungseffekt, also als Verzerrung der Bewertung. Gelesen als zwei Seiten heisst das: hohe Erwartungen an das Lernen, keine Erwartungen in der Bewertung.» und die Überschrift auf «Spannung zu den Bezugsnormen (E-183, B-146)»; in Bezugsnormen den Abschnitt «Gegenposition Meyer», die Quellenzeile Meyer und den Verweis auf Merkmal 9 entfernen; E-191 aus beiden Notizen entfernen.

**Stand:** umgesetzt

## E-192 B-149 Sandwich-Methode und Sandwich-Modell

**Optionen:**
1. Beide behalten, gegenseitig verweisen, in der Sammlungsnotiz ein Satz zur anderen Gewichtung
2. Sammlungsnotiz an das Modell angleichen
3. Lassen

**Wahl:** Option 1. Beide Notizen verweisen im Feld verwandt aufeinander; [[Sandwich-Methode]] hat nach den Grenzen den Absatz «Abweichung (E-192)».

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** [[Sandwich-Methode]], [[Sandwich-Modell]]

**Rückgängig:** Verweise, Absatz und E-192 entfernen

**Stand:** umgesetzt

## E-193 B-150 Doppelungen in der Methodensammlung

**Optionen:**
1. Gegenseitig verweisen
2. Zusammenlegen
3. Lassen

**Wahl:** Option 1, wie bei Nr. 236 und 285 nach E-100. Gegenseitige Verweise im Feld verwandt: Pro-Contra Debatte (272) und Pro- und Contra-Debatte oder Streiten lernen (246), Projektunterricht und Projektarbeit, Karika-Tour und Karika-Tour, Frage-Leitfaden, Kopfstand und Elfchen und Kopfstand, Streitlinie und Von der Positionslinie zur Streitlinie, Kugellager und Karussellgespräch, Vier-Ecken-Methode und In der Ecke stehen. Zusammengelegt wird nichts, weil das einen Vergleich am Original verlangen würde.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** die vierzehn Notizen mit E-193 im Feld entscheide

**Rückgängig:** Verweise und E-193 entfernen

**Stand:** umgesetzt; im Skill nichts geändert

## E-194 B-151 Verweise von der Sammlung auf belegte Notizen

**Optionen:**
1. Gegenseitig verweisen
2. Nur von der Sammlung auf die belegte Notiz verweisen
3. Lassen

**Wahl:** Option 2. Verweise im Feld verwandt: [[Visualisierung]] auf [[Visualisieren]], [[Differenzierung]] auf [[Differenzierung planen]], [[Portfolio]] auf [[Portfolio als Prüfungsform]], [[Lerntagebuch]] auf [[Lernjournal (AVIVA)]]. Die belegten Notizen bleiben unverändert.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** die vier Sammlungsnotizen mit E-194 im Feld entscheide

**Rückgängig:** Verweise und E-194 entfernen

**Stand:** umgesetzt

## E-195 B-152 Dateinamen korrigieren

**Optionen:**
1. Lehrerperson-Vortrag wird «Lehrpersonenvortrag»
2. wird «Vortrag der Lehrperson»
3. Lassen

**Wahl:** Option 1; dazu werden die doppelten Leerzeichen in «Pro- und Contra-Debatte  oder  Streiten lernen» und «Pro- und Contra-Debatte  oder  Streiten lernen Spielregeln» durch einfache ersetzt. David benennt die drei Dateien selbst in Obsidian um, damit die Links nachgeführt werden. Ob der Skill unterrichtsmethoden denselben Tippfehler hat, ist nicht geprüft; falls ja, gehört er in den Skillumbau.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** drei Methodennotizen

**Rückgängig:** in Obsidian zurückbenennen

**Stand:** umgesetzt. David hat die drei Dateien am 22.10.2026 in Obsidian umbenannt; die Links sind nachgeführt, die Linkprüfung über den ganzen Vault fand keinen kaputten Link.

## E-196 B-153 Redestabrunde und Unterricht löschen

**Optionen:**
1. Löschen, Nummern bleiben frei
2. Neu schreiben
3. Lassen

**Wahl:** Option 1 für beide. Die Notizen Redestabrunde (Nr. 72) und Unterricht (Nr. 107) sind am 22.10.2026 gelöscht. In [[Unterrichtsmethoden Übersicht]] stehen 325 Methoden, die freien Nummern 9, 49, 72 und 107 und die Gruppen «16 bis 96 (ohne 49 und 72)» und «108 bis 112»; in [[CLAUDE]] 325 Methoden. Im Skill unterrichtsmethoden stehen beide Einträge weiter; das gehört in den Skillumbau (Etappe 8).

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** Methodensammlung, [[Unterrichtsmethoden Übersicht]], [[CLAUDE]]

**Rückgängig:** Die beiden Notizen aus dem Skill unterrichtsmethoden (references/weitere.md, Nr. 72 und Nr. 107) neu erzeugen; Übersicht und CLAUDE.md auf 327 zurücksetzen

**Stand:** umgesetzt

## E-197 B-154 Felder der AVIVA-Grossformen

**Optionen:**
1. Ausnahme in der CLAUDE.md
2. Felder ergänzen

**Wahl:** Option 1. In [[CLAUDE]] steht beim Typ methode: Die fünf Grossformen mit gruppe «Grossform AVIVA» tragen nur gruppe und aviva_phase. Nummer, Herkunft und Eignung gehören zur Sammlung und müssten sonst erfunden werden.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** [[CLAUDE]]

**Rückgängig:** Zusatz in der Tabelle der CLAUDE.md entfernen

**Stand:** umgesetzt

## E-198 B-155 Zwischenstufen der Eignungsskala

**Optionen:**
1. Lassen
2. Einer Grundstufe zuordnen

**Wahl:** Option 1. «mittel bis hoch» und «gering bis mittel» folgen dem Wortlaut der Notizen (E-040).

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** keine

**Rückgängig:** entfällt

**Stand:** umgesetzt, nichts geändert

## E-199 B-156 Regel «kurz gleich Abschnitt Kurz»

**Optionen:**
1. In der CLAUDE.md präzisieren: gemeint ist der erste Absatz, weiterer Inhalt darf folgen
2. In 47 Notizen den Rest unter eine eigene Überschrift setzen

**Wahl:** Option 1. Die Pflichtfelder in [[CLAUDE]] sagen jetzt: kurz ist gleich dem ersten Absatz im Abschnitt «Kurz».

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** [[CLAUDE]]

**Rückgängig:** alten Wortlaut «gleich wie der Abschnitt «Kurz»» zurücksetzen

**Stand:** umgesetzt

## E-200 B-157 Studienskript 8 als Beleg

**Optionen:**
1. E-039 bleibt
2. E-039 neu ansehen

**Wahl:** Option 1.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** keine

**Rückgängig:** entfällt

**Stand:** umgesetzt, nichts geändert

## E-201 Nächste Etappe

**Optionen:**
1. Etappe 3 für die Ordner 40 und 20 als nächste Etappe, Ordner 40 zuerst
2. Später

**Wahl:** Option 1. Ordner 40 zuerst, weil dort die meisten Zahlen und Operatorenregeln stehen. [[Arbeitsplan]], [[Stand]] und [[Übergabe]] sind nachgeführt.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** [[Arbeitsplan]], [[Stand]], [[Übergabe]]

**Rückgängig:** Reihenfolge im Arbeitsplan zurücksetzen

**Stand:** umgesetzt

## E-202 Gegenprobe mit den Prüfskripten

**Optionen:**
1. Ordner BFS für die Sitzung anfragen und die Prüfskripte nach den Änderungen laufen lassen
2. Lassen

**Wahl:** Option 1.

**Entschieden von:** David, 22.10.2026 («nehme alle deine empfehlungen an», auf die Fragenrunde vom selben Tag)

**Betroffen:** «00 Start/Prüfungen» (nur Lauf, keine Änderung)

**Rückgängig:** entfällt

**Stand:** gelaufen am 22.10.2026 mit verbundenem Ordner BFS: lk1_abgleich.py Exit 0, raster_proben.py Exit 0 (16 Proben, 0 Fehlurteile); operatoren_check.py, methoden_pruefung.py, slp_check.py und quellen.py Exit 2, weil der Pluginordner unter ~/.claude in der Sitzung nicht erreichbar ist; abschrift_check.py Exit 2, weil die Palette auf dem Schreibtisch nicht verbunden ist; fragecheck.py nicht gelaufen (prüft Dossiers, von den Änderungen nicht betroffen). Die Methodenprüfung nach dem Löschen steht damit aus.

## E-203 B-148 Ersatzeintrag für qub-lehrprobe in navigator.py

**Optionen:**
1. In navigator.py einen Ersatzeintrag anlegen, der «laut Auslegung des Skills qub-lehrprobe» auf der Seite zu «laut Auslegung» macht, danach Seite erzeugen, durchsuchen, veröffentlichen
2. Seite so veröffentlichen
3. Warten

**Wahl:** Option 1, nach dem Muster von E-187. In ERSATZ steht vor dem allgemeinen Eintrag «laut Auslegung des Skills» der Eintrag («laut Auslegung des Skills qub-lehrprobe », «laut Auslegung »). Der Wortlaut in [[Merkmal 9 Transparente Leistungserwartungen]] bleibt (E-072).

**Entschieden von:** David, 22.10.2026 («2. ja»)

**Betroffen:** navigator.py; Seite https://claude.ai/artifact/5muAj83BjbbNTZoNRvCbKV

**Rückgängig:** den Eintrag mit E-203 aus navigator.py entfernen, Seite neu erzeugen und veröffentlichen

**Stand:** umgesetzt; als Version 13 am 22.10.2026 veröffentlicht (E-190).

## E-218 Playbook aus den Notizen

**Optionen:**
1. Playbook nach Arbeitssituationen als eine Notiz mit Schrittfolgen aus den Kurzfassungen und Links auf die Notizen
2. Alle Notizen in eine Datei exportieren
3. Einen Playbook-Einstieg auf Basic Skills

**Wahl:** Option 1, als [[Playbook]] in «00 Start», Typ index. Die Schritte geben nur die Kurzfassungen der verlinkten Notizen wieder (alle mit status belegt); Markierungen «laut Skill» bleiben stehen. Die Notiz ist so geschrieben, dass sie auch ohne Links lesbar ist, damit sie über das Plugin Star NotebookLM als Quelle gesendet werden kann.

**Entschieden von:** David, 22.10.2026 («dann mach», auf die Empfehlung von Option 1)

**Betroffen:** neue Notiz «00 Start/Playbook.md»; Seite Basic Skills (neu erzeugt nach E-167)

**Rückgängig:** Notiz in Obsidian löschen, Seite neu erzeugen und veröffentlichen

**Stand:** Notiz angelegt am 22.10.2026; nicht in [[Start]] verlinkt; Senden an NotebookLM durch David.

## E-219 B-102 Planungskette: Bedingungsanalyse nach der Themenwahl

**Optionen:**
1. Bedingungsanalyse nach der Themenwahl (Meyers Grundraster, Notiz Thema festlegen)
2. Bedingungsanalyse in der Makroplanung, einmal pro Klasse (Skill fertigen-unterricht-planen)
3. Beide Fassungen nebeneinander lassen (Stand nach E-136)

**Wahl:** Option 1. In der Planungskette steht die Bedingungsanalyse neu in Ebene B Klären, direkt nach «Thema festlegen» und vor Sach- und didaktischer Analyse. Der Absatz zur Stellung nennt den Entscheid und die Abweichung des Skills. Ersetzt die Wahl von E-136.

**Entschieden von:** David, 23.10.2026 («nach der Themenwahl»)

**Betroffen:** [[Planungskette fertigen Unterricht]]; [[Befundliste]] B-102; navigator.py (Ersatzeintrag Zeile 208 auf den neuen Satz umgestellt, E-169); Seite Basic Skills

**Rückgängig:** Bedingungsanalyse in Ebene A zurückstellen, Absatz zur Stellung auf die Fassung von E-136 zurücksetzen, E-219 aus `entscheide` entfernen

**Stand:** in der Notiz umgesetzt am 23.10.2026. Der Skill fertigen-unterricht-planen (references/kette.md) führt die Bedingungsanalyse weiterhin in der Makroplanung; nicht geändert. Basic Skills am 23.10.2026 neu erzeugt, aber nicht veröffentlicht: In dieser Sitzung stand kein Werkzeug zum Veröffentlichen zur Verfügung.
