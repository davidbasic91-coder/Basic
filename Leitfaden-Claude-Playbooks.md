# Claude-Playbooks verstehen und selber bauen

**Ein Leitfaden in einfacher Sprache**

Stand: 23. Oktober 2026. Grundlage ist eine Internetrecherche vom selben Tag. Die zentralen Zitate sind im Originaltext nachgeprüft.

---

## So liest du diesen Leitfaden

- **Zitate** stehen im Original, meist auf Englisch, in «Anführungszeichen». Dahinter steht eine Quellennummer wie [Q8]. Alle Quellen findest du in Kapitel 15.
- **✔ bei einer Quelle** heisst: Die zitierten Stellen wurden im heruntergeladenen Originaltext Wort für Wort gefunden.
- **○ bei einer Quelle** heisst: Ein Recherche-Subagent hat die Quelle gelesen. Ich habe sie nicht selbst nachgeprüft.
- **Meine Schlussfolgerung:** Das leite ich aus den Quellen ab. So steht es in keiner Quelle.
- **Nicht geprüft:** Diese Angabe konnte ich nicht bestätigen.
- **Allgemeinwissen:** Das stammt nicht aus der Recherche, sondern aus meinem allgemeinen Wissen.

### Deine Fragen und wo die Antworten stehen

| Deine Frage | Kapitel |
|---|---|
| Was ist ein Playbook überhaupt? | 2 und 3 |
| Wie funktioniert es? | 4 |
| Wo lege ich es ab? | 5 |
| Was muss drinstehen? | 6 und 8 |
| Wie schreibe ich es gut? | 7 |
| Wie erstelle ich eines, Schritt für Schritt? | 8, 9 und 10 |
| Was bringt es, was ist der Nutzen? | 11 |
| Wofür setze ich es am besten ein? | 12 |
| Fragen, die du so nicht gestellt hast | 13 |

### Inhalt

1. Das Wichtigste in zehn Sätzen
2. Was ist ein Playbook?
3. Die Begriffe auseinanderhalten
4. Wie ein Playbook technisch funktioniert
5. Wo lege ich mein Playbook ab?
6. Was in ein Playbook gehört
7. Schreibregeln
8. Vorlage zum Ausfüllen
9. Durchgearbeitetes Beispiel: Lernkontrolle
10. Testen und pflegen
11. Nutzen, Grenzen, Risiken
12. Wofür sich ein Playbook lohnt
13. Fragen, die du vielleicht nicht gestellt hast
14. Widersprüche und offene Punkte
15. Quellen

---

## 1. Das Wichtigste in zehn Sätzen

1. Ein Playbook ist eine Arbeitsanleitung, die du einmal für Claude aufschreibst. Claude erledigt damit eine wiederkehrende Aufgabe immer nach deinen Regeln.
2. Eine Funktion namens «Playbooks» gibt es bei Anthropic nicht. «Playbook» ist ein gewöhnliches Wort, kein Knopf im Programm.
3. Technisch steckt ein Playbook fast immer in einem **Skill**: einem Ordner mit einer Datei `SKILL.md`.
4. Claude sieht von jedem Skill zuerst nur das Etikett, also Name und Beschreibung. Erst wenn das Etikett zur Aufgabe passt, liest Claude die eigentliche Anleitung.
5. Darum entscheidet das Etikett, ob dein Playbook überhaupt zum Einsatz kommt.
6. Ein Playbook ist eine Bitte, kein Gesetz. Claude hält sich meistens daran, aber nicht garantiert.
7. Am meisten bringt, was Claude nicht schon weiss: deine Regeln, deine Vorlagen, deine Vorgaben.
8. Kurz und klar wirkt besser als lang und vollständig. Anthropic nennt als Obergrenze 500 Zeilen.
9. Eine Studie zeigt: Mit sorgfältig geschriebenen Skills lösen KI-Modelle deutlich mehr Aufgaben richtig. Allgemeine Überblickstexte bringen dagegen nichts.
10. Ein Playbook muss man testen und pflegen, besonders wenn ein neues Claude-Modell erscheint.

---

## 2. Was ist ein Playbook?

### 2.1 Ein Bild: die Anleitung für die Stellvertretung

Stell dir vor, eine sehr fähige Stellvertretung übernimmt deine Klasse. Sie kann viel, aber sie kennt deine Gewohnheiten nicht. Also legst du ihr einen Zettel hin: was zu tun ist, in welcher Reihenfolge, worauf sie achten soll und wie das Ergebnis aussehen muss.

Genau so beschreibt Anthropic Claude: «Think of Claude as a brilliant but new employee who lacks context on your norms and workflows.» [Q23]

Das Playbook ist dieser Zettel. Der Unterschied zur Stellvertretung: Claude vergisst nach jedem Gespräch alles. Ohne Playbook müsstest du den Zettel jedes Mal neu schreiben.

### 2.2 Gibt es «Claude Playbooks» als eigene Funktion? Nein.

Ein deutscher Artikel auf borncity.com behauptet das Gegenteil. Er heisst «Claude Playbooks: Anthropic startet KI-Planungs-Plattform heute» und erschien am 13. Juni 2026 [Q41]. Er schreibt: «Die kostenlose Version erlaubt zwei Playbooks pro Monat, das Professional-Abo kostet neun Euro monatlich.»

Die Prüfung ergibt:

- Anthropic führt die Abos Free, Pro, Max, Team und Enterprise [Q18]. Ein «Professional-Abo» für neun Euro gibt es nicht.
- Der Artikel trägt selbst den Hinweis, dass er mit künstlicher Intelligenz erstellt wurde («Art. 50 KI-VO»), und enthält Anzeigen [Q41].
- Ein Recherche-Subagent hat Anthropics Preisseite, die Release Notes, die Seitenverzeichnisse und die vollständigen Textfassungen der Dokumentation durchsucht. Ein Feature namens «Playbooks» fand er nirgends (○).
- Ich habe nachgeprüft, dass das Wort in der Claude-Code-Dokumentation nur als gewöhnliches Wort vorkommt [Q1, Q2].

Fazit: Der Artikel ist unzuverlässig. **Meine Schlussfolgerung:** Vermutlich beschreibt er ein Produkt eines anderen Anbieters, das auf Claude aufbaut. Belegt ist das nicht.

Daneben gibt es Bücher und Sammlungen anderer Anbieter mit «Playbook» im Namen, zum Beispiel ein E-Book «The Claude Playbook» mit dem Vermerk «Independent publication, not affiliated with Anthropic» [Q44, ○]. Auch diese sind keine Anthropic-Funktion.

### 2.3 Wie Anthropic das Wort «Playbook» tatsächlich braucht

Bei Anthropic hat das Wort drei Bedeutungen.

**a) Playbook = eine Anleitung, die man als Skill speichert.**
Die Claude-Code-Dokumentation sagt in einer Tabelle: Wenn du «the same playbook or multi-step procedure into chat for the third time» einfügst, dann: «Capture it as a skill» [Q1]. Das Glossar nennt die eingebauten Skills «Prompt-based playbooks included with Claude Code» [Q2]. Und ein Kurs der Anthropic Academy sagt: «Where a skill is one playbook, a plugin is several» [Q6].

**b) Playbook = ein Regelwerk, das ein Skill als Massstab liest.**
Das beste Beispiel ist das Legal-Plugin (siehe 2.4).

**c) Playbook = Titel von Leitfäden.**
Anthropic veröffentlicht Leitfäden wie «The founder's playbook» (14. Mai 2026) oder «The AI-native SDLC playbook» (21. August 2026) [Q33, ○]. Das ist Lesestoff, keine Funktion.

Für dich sind die Bedeutungen a und b wichtig.

### 2.4 Das Musterbeispiel: das Legal-Plugin

Anthropic bietet ein Plugin für Rechtsabteilungen an. Es läuft in Cowork, Anthropics Desktop-Anwendung, und in Claude Code [Q3]. Das Herzstück ist eine Datei namens `legal.local.md`, die die Rechtsabteilung selbst schreibt. Anthropic sagt dazu: «Your playbook is the heart of the contract review system.» [Q3]

**Wo die Datei liegt:** In Cowork «Save it in any folder you've shared with Cowork», in Claude Code «Save it in your project's .claude/ directory» [Q3].

**Was drinsteht:** Für jede Vertragsklausel drei Angaben: die eigene Standardposition, den akzeptablen Spielraum und die Auslöser für eine Eskalation an höhere Stellen («Standard positions», «Acceptable ranges», «Escalation triggers») [Q3].

**Wie es wirkt:** Der Skill zur Vertragsprüfung hat einen Schritt «Load the Playbook». Dort steht: «Look for the organization's contract review playbook in local settings (e.g., `legal.local.md` or similar configuration files).» [Q4] Findet Claude keine Datei, soll es das melden («Inform the user that no playbook was found») und anbieten, ein Playbook einzurichten oder mit allgemeinen Standards zu prüfen [Q4]. Jede Abweichung wird grün, gelb oder rot eingestuft. Im Ergebnis steht ausdrücklich, ob nach dem Playbook oder nach allgemeinen Standards geprüft wurde («Review Basis: [Playbook / Generic Standards]») [Q4].

**Die neueren Legal-Plugins** gehen weiter: Ein Einrichtungsgespräch fragt die Regeln der Abteilung ab und schreibt sie in eine Profildatei. Ein eigener Helfer namens «playbook-monitor» schlägt Änderungen am Playbook vor, wenn dieselbe Abweichung immer wieder vorkommt [Q5, ○].

**Was du daraus lernst:** Hier besteht ein Playbook aus zwei Teilen.

1. Der **Skill** beschreibt das Vorgehen: wie geprüft wird.
2. Die **Playbook-Datei** enthält den Massstab: woran geprüft wird.

Den Massstab kannst du ändern, ohne den Skill anzufassen.

**Meine Schlussfolgerung:** Dieses Muster passt gut zur Schule, zum Beispiel ein Skill «Lernkontrolle prüfen» zusammen mit einer Datei, in der deine Gütekriterien stehen.

---

## 3. Die Begriffe auseinanderhalten

Rund um Claude gibt es viele ähnliche Begriffe. Diese Tabelle ordnet sie.

| Begriff | Was es ist | Wann es wirkt | Wo es das gibt |
|---|---|---|---|
| **Prompt** | Eine einzelne Nachricht an Claude | Nur in diesem Moment | Überall |
| **Anweisungen für Claude** (deine Präferenzen) | Dauerregeln für alle deine Gespräche. Anthropic: «Instructions are account-wide settings» [Q22] | In jedem Gespräch | claude.ai, Desktop-App, Cowork |
| **Projekt** | Arbeitsraum mit eigenen Anweisungen und eigenen Dateien (Projektwissen) | In jedem Chat dieses Projekts | claude.ai |
| **Skill** | Ordner mit einer Datei `SKILL.md` und allenfalls Zusatzdateien. «Unlike prompts (conversation-level instructions for one-off tasks), Skills load on demand» [Q7] | Wenn das Etikett zur Aufgabe passt oder du ihn ausdrücklich aufrufst | claude.ai, Cowork, Claude Code |
| **Plugin** | Paket aus mehreren Skills, dazu Connectoren, Befehle und Helfer. Alles besteht aus «markdown and JSON, no code» [Q27] | Wie seine Teile | Cowork, Claude Code, teils claude.ai |
| **CLAUDE.md** | Datei mit Dauerregeln für Claude Code | Bei jedem Start einer Sitzung | Claude Code |
| **Hook** | Kleines Programm, das bei einem Ereignis automatisch läuft und etwas erzwingen kann | Immer, ohne dass Claude entscheidet | Claude Code, Cowork |
| **Connector (MCP)** | Verbindung zu anderen Diensten. «MCP connections give Claude access to tools, while skills teach Claude how to use those tools effectively.» [Q17] | Wenn Claude den Dienst braucht | Überall |
| **Subagent** | Helfer mit eigenem Arbeitsgedächtnis, der eine Teilaufgabe erledigt und nur das Ergebnis zurückgibt | Wenn Claude eine Aufgabe abgibt | Claude Code, Cowork (○) |
| **Memory** | Notizen, die Claude sich selbst über dich macht | Automatisch | claude.ai, Claude Code |

**Merksatz:** Ein Playbook ist kein eigener Begriff in dieser Tabelle. Es ist ein *Inhalt*, und dieser Inhalt braucht einen *Behälter*. Der übliche Behälter ist der Skill.

---

## 4. Wie ein Playbook technisch funktioniert

### 4.1 Der Skill: ein Ordner mit Etikett

Ein Skill ist ein Ordner. Darin liegt mindestens die Datei `SKILL.md`. Weitere Dateien sind freiwillig.

```
lernkontrolle-fabe/
├── SKILL.md         ← oben das Etikett, darunter die Anleitung
├── vorlage.md       ← Zusatzdatei, wird nur bei Bedarf gelesen
└── kriterien.md     ← Zusatzdatei, wird nur bei Bedarf gelesen
```

Die Datei `SKILL.md` beginnt mit dem Etikett zwischen zwei Strichlinien:

```
---
name: lernkontrolle-fabe
description: Baut eine schriftliche Lernkontrolle ... Verwenden, wenn ...
---
```

Darunter folgt die Anleitung als normaler Text.

Claude liest einen Skill in **drei Stufen** [Q7]:

| Stufe | Was Claude liest | Wann | Umfang laut Anthropic |
|---|---|---|---|
| 1 | Name und Beschreibung (das Etikett) | Immer, bei jedem Gespräch | «~100 tokens» pro Skill |
| 2 | Die Anleitung in `SKILL.md` | Wenn die Aufgabe zum Etikett passt oder du den Skill aufrufst | «Under 5k tokens» |
| 3 | Zusatzdateien und Skripte | Nur wenn die Anleitung darauf verweist und Claude sie braucht | Nichts, solange sie ungeöffnet bleiben |

Ein Token ist ein Wortstück, die Masseinheit, in der KI-Modelle Text zählen (Allgemeinwissen).

Der Vorteil dieser Stufen: Du kannst viele Skills haben, ohne Claude zu überladen. Solange ein Skill nicht gebraucht wird, kostet er nur sein Etikett.

### 4.2 Warum das Etikett entscheidet

Anthropic sagt über die Beschreibung: «it's the only part Claude sees before deciding to use the skill» [Q10]. Ist das Etikett unklar, öffnet Claude den Ordner nie.

Die Claude-Code-Dokumentation warnt: «If descriptions are vague or overlap, Claude may load the wrong skill or miss one that would help.» [Q1] Eine Studie von 2026 nennt das Auslösen sogar den Hauptengpass: «skill triggering is a key bottleneck» [Q40]. Anthropics eigene Hilfsanleitung zum Skill-Schreiben stellt fest: «Claude has a tendency to "undertrigger" skills» [Q26]. Claude greift also eher zu selten als zu oft zu einem Skill.

Du kannst einen Skill auch direkt aufrufen. In Claude Code geht das mit `/name`: «To tell Claude to use a specific skill, invoke it with `/<name>`» [Q1]. Dann spielt das Etikett keine Rolle.

### 4.3 Was nach dem Laden passiert

In Claude Code bleibt die Anleitung im Gespräch, sobald sie geladen ist. Claude liest die Datei danach nicht nochmals: «Claude Code does not re-read the skill file on later turns» [Q11]. Änderst du die Datei mitten im Gespräch, merkt Claude das also nicht.

Wird ein Gespräch sehr lang, fasst Claude Code es zusammen. Danach hängt es die benutzten Skills wieder an, aber nur die ersten 5'000 Tokens pro Skill und insgesamt höchstens 25'000 Tokens [Q11]. Anthropic folgert daraus: «Truncation keeps the start of the file, so put the most important instructions near the top» [Q14]. Das Wichtigste gehört also nach oben.

**Nicht dokumentiert:** Ob claude.ai und Cowork genau gleich vorgehen, steht in keiner gelesenen Quelle.

### 4.4 Der Arbeitstisch: das Kontextfenster

Alles, was Claude in einem Moment «vor sich hat», liegt im sogenannten Kontextfenster: das Gespräch, deine Anweisungen, die Etiketten aller Skills, geladene Anleitungen und geöffnete Dateien. Stell es dir als Arbeitstisch vor. Er ist gross, aber nicht unendlich.

Anthropic schreibt: «The context window is a public good.» [Q8] Was auf dem Tisch liegt, teilt sich den Platz. Ein voller Tisch schadet: «Bloated CLAUDE.md files cause Claude to ignore your actual instructions» [Q13]. Auch zu viele Skills schaden: «With too many Skills active, Claude might fail to select the right Skill or miss relevant ones entirely» [Q9].

In Claude Code bekommt die Liste aller Skill-Etiketten einen festen Anteil: «The budget scales at 1% of the model's context window» [Q11]. Wird es eng, lässt Claude Code zuerst die Beschreibungen der selten benutzten Skills weg [Q11].

### 4.5 Wo Skills laufen und wie man sie teilt

- **claude.ai und Desktop-App:** Skills findest du unter «Customize > Skills» [Q10]. Dafür muss die Code-Ausführung eingeschaltet sein: «This feature requires code execution» [Q17].
- **Cowork:** Cowork lädt die Skills deines claude.ai-Kontos. Cowork-Sitzungen «load the skills enabled for your claude.ai account» [Q11].
- **Claude Code:** Persönliche Skills liegen im Ordner `~/.claude/skills/`, Skills für ein Projekt in `.claude/skills/` [Q11]. Skills aus claude.ai werden heruntergeladen, aber nie zurückgeschrieben: «Claude Code downloads synced skills and never uploads them» [Q11]. In dieser Arbeitssitzung sind deine claude.ai-Skills tatsächlich so heruntergeladen, im Ordner `~/.claude/skills/synced/`.
- **In einer Organisation (Team und Enterprise):** Die Besitzer können Skills für alle bereitstellen: «When you upload a skill through organization settings, it becomes available to everyone in your organization» [Q19]. Einzelne Personen können Skills weitergeben: «Users can share a skill or plugin with specific colleagues» [Q19]. Wer einen geteilten Skill erhält, «can't edit its contents» [Q19].

**Achtung, Widerspruch:** Eine ältere Entwicklerseite sagt noch: «Custom Skills are individual to each user» [Q7]. Die neuere Hilfe-Seite beschreibt das Teilen ausführlich [Q19]. Die ältere Seite ist an dieser Stelle vermutlich veraltet.

### 4.6 Die Dauerregeln: Anweisungen, Projekte, CLAUDE.md

Neben Skills gibt es Orte für Regeln, die *immer* gelten:

- **Anweisungen für Claude:** «Any instructions you add here will be applied to all of your conversations with Claude.» [Q22]
- **Projektanweisungen:** Sie gelten in allen Chats eines Projekts (○). Das Projektwissen sind die Dateien, die du im Projekt ablegst. Wird es sehr gross, sucht Claude darin automatisch nach den passenden Stellen. So lässt sich laut Anthropic bis zu zehnmal mehr ablegen: «Store up to 10x more content» [Q21].
- **Organisationsanweisungen** (Team und Enterprise): Sie gehen vor: «organization instructions take precedence» [Q20]. «The maximum length is 3,000 characters» [Q20].
- **CLAUDE.md** (nur Claude Code): «Put it in CLAUDE.md if Claude should always know it» [Q1]. Empfohlene Länge: «target under 200 lines per CLAUDE.md file» [Q12].

Anthropic unterscheidet Projekt und Skill so: Skills sind «Task-specific procedures that Claude loads when a request matches», Projekte «Background knowledge that's always loaded» [Q10].

### 4.7 Bitte oder Schloss?

Das ist der wichtigste technische Punkt. Alles, was du aufschreibst, ist für Claude eine Bitte. Anthropic sagt es klar:

- «An instruction like "never edit `.env`" in CLAUDE.md or a skill is a request, not a guarantee.» [Q1]
- «Claude treats them as context, not enforced configuration.» [Q12]

Anthropic zeigt selbst ein Beispiel, wie eine Regel verloren geht: «it wrote the query but forgot to filter out test accounts, even though the Skill mentions this rule» [Q8].

Erzwingen lässt sich etwas nur mit einem **Hook**, einem kleinen Programm, das bei einem bestimmten Ereignis automatisch läuft. Hooks geben laut Anthropic «deterministic control» [Q15], und: «hooks are deterministic and guarantee the action happens» [Q13]. Hooks gibt es in Claude Code und Cowork. Im normalen Chat auf claude.ai werden sie laut Anthropic ignoriert [Q31, ○].

**Meine Schlussfolgerung:** Im Chat bist du selbst das Schloss. Alles, was wirklich stimmen muss, etwa Noten oder Punkte, prüfst du von Hand.

### 4.8 Was gilt, wenn sich Regeln widersprechen?

- «if two instructions contradict each other, Claude may pick one arbitrarily» [Q12]
- Zu persönlichen und projektbezogenen Regeln in Claude Code: «Neither set overrides the other» [Q12]
- Einzige klare Rangfolge auf claude.ai: Organisationsanweisungen gehen vor [Q20].
- Für claude.ai gibt es keine dokumentierte Rangfolge zwischen deinen Anweisungen, Projektanweisungen, Skills und Memory (○, Ergebnis der Recherche).

**Meine Schlussfolgerung:** Verlass dich nicht auf eine Rangfolge. Jede Regel steht an genau einem Ort. Wenn du etwas änderst, suchst du alte, widersprechende Regeln und löschst sie.

---

## 5. Wo lege ich mein Playbook ab?

Diese Tabelle ist meine Zusammenstellung aus mehreren Anthropic-Quellen [Q1, Q10, Q12, Q45]. Die Academy fasst den Kern so zusammen: «General rules go in Instructions; a repeatable process goes in a Skill.» [Q45, ○]

| Was willst du festhalten? | Beispiel aus deinem Alltag | Bester Ort in claude.ai und Cowork | Bester Ort in Claude Code |
|---|---|---|---|
| Regeln, die immer gelten | Du-Form, Schweizer «ss», Anführungszeichen «so» | Anweisungen für Claude | CLAUDE.md (persönlich) |
| Regeln für ein Fach oder eine Klasse | Fachrichtung MmB, Profil der Klasse | Projektanweisungen | CLAUDE.md im Projektordner |
| Ein wiederkehrender Ablauf | Lernkontrolle bauen, Dossier prüfen | Skill | Skill |
| Nachschlagewissen | Bildungsplan, Schullehrplan | Projektwissen oder Zusatzdatei im Skill | Zusatzdatei im Skill |
| Ein Massstab zum Prüfen | Deine Gütekriterien | Zusatzdatei im Skill (wie `legal.local.md`) | Zusatzdatei im Skill |
| Eine Regel, die nie gebrochen werden darf | «Nie eine Datei löschen» | Gibt es im Chat nicht: Kontrolle durch dich | Hook oder Berechtigung |
| Weitergabe an Kolleginnen und Kollegen | Gemeinsame Vorlagen | Skill teilen, Organisation, Plugin | Plugin oder Projektordner |

---

## 6. Was in ein Playbook gehört

Anthropic veröffentlicht keine fertige Pflichtliste. Die offizielle Spezifikation für Skills nennt unter «Recommended sections» nur drei Teile: «Step-by-step instructions», «Examples of inputs and outputs» und «Common edge cases» [Q34]. Die übrigen Bausteine empfiehlt Anthropic auf verschiedenen Seiten. Die folgende Liste ist meine Zusammenstellung daraus.

| Nr. | Baustein | Was hineingehört | Beleg |
|---|---|---|---|
| 1 | **Das Etikett** | Ein bis drei Sätze: was das Playbook macht, wann Claude es nehmen soll und wofür nicht | «should include both what the Skill does and when to use it» [Q8]; «clarify the boundary between this skill and adjacent capabilities» [Q36] |
| 2 | **Die Rolle** | Ein Satz, wer Claude hier ist | «Even a single sentence makes a difference» [Q23] |
| 3 | **Ziel und Grund** | Wozu das Ergebnis dient und warum deine Regeln wichtig sind | «Providing context or motivation behind your instructions … can give Claude more information about your goals» [Q23] |
| 4 | **Was Claude braucht** | Welche Angaben Claude vor dem Start von dir braucht | Meine Ergänzung, keine Anthropic-Quelle |
| 5 | **Die Schritte** | Der Ablauf in Reihenfolge, bei langen Aufgaben als Checkliste zum Abhaken | «Break complex operations into clear, sequential steps» [Q8] |
| 6 | **Die Weggabelungen** | «Wenn A, dann so; wenn B, dann anders» | «Guide Claude through decision points» [Q8] |
| 7 | **Die Vorlage** | Wie das fertige Ergebnis aussieht | «Provide templates for output format» [Q8] |
| 8 | **Beispiele** | Ein bis drei konkrete, gute Beispiele | «Examples are concrete, not abstract» [Q8]; für Prompts: «Include 3–5 examples for best results» [Q23] |
| 9 | **Stolperstellen** | Wo es oft schiefgeht und was dann zu tun ist | «Common edge cases» [Q34] |
| 10 | **Die Schlusskontrolle** | Prüfen, verbessern, nochmals prüfen | «Run validator → fix errors → repeat» [Q8] |
| 11 | **Wann anhalten und fragen** | Wann Claude stoppen und dich fragen muss | «Pause for the user only when the work genuinely requires them» [Q24] |
| 12 | **Verweise auf Zusatzdateien** | Welche Datei es gibt und wann Claude sie lesen soll | «"Read `references/api-errors.md` if the API returns a non-200 status code" is more useful than a generic "see references/ for details."» [Q35] |

Zwei Regeln gelten für das ganze Playbook:

- **Feste Wörter:** «Choose one term and use it throughout the Skill» [Q8]. Also nicht einmal «Auftrag» und einmal «Aufgabe».
- **Eine Standardwahl statt vieler Möglichkeiten:** «Don't present multiple approaches unless necessary» [Q8].

**Was nicht hineingehört:**

- Was Claude ohnehin weiss (Kapitel 7.1).
- Angaben, die bald veralten: «Don't include information that will become outdated» [Q8].
- Lange Verbotslisten ohne Alternative: «Tell Claude what to do instead of what not to do» [Q23].
- Personendaten von Lernenden (Kapitel 11.5).
- Alles, was über etwa 500 Zeilen hinausgeht: Das lagerst du in Zusatzdateien aus [Q8].

---

## 7. Schreibregeln

### 7.1 Nur, was Claude nicht weiss

Anthropics Grundannahme: «Default assumption: Claude is already very smart» [Q8], und daraus folgt: «Only add context Claude doesn't already have.» [Q8]

Die Prüffrage für jeden Satz: «Would the agent get this wrong without this instruction? If the answer is no, cut it.» [Q35]

Lass Claude ein Playbook nicht aus dem Nichts schreiben. Ohne dein Fachwissen entstehen laut Anthropic-naher Spezifikation nur allgemeine Floskeln: «The result is vague, generic procedures» [Q35]. Gib Claude deine Vorlagen, Kriterien und ein gelungenes Beispiel mit.

### 7.2 Schmale Brücke oder offenes Feld

Anthropic unterscheidet, wie eng eine Anleitung sein soll [Q8]:

- «Narrow bridge with cliffs on both sides: There's only one safe way forward.» Hier gibst du genaue Anweisungen.
- «Open field with no hazards: Many paths lead to success.» Hier gibst du nur die Richtung vor und vertraust Claude.

**Meine Schlussfolgerung für die Schule:** Die Notenberechnung ist eine schmale Brücke: genaue Formel, genaue Rundung. Eine Einstiegsidee für eine Lektion ist ein offenes Feld. Die meisten Playbooks haben beides. Für jeden Teil entscheidest du einzeln, wie eng er sein muss.

### 7.3 Das Etikett schreiben

1. **Was und wann:** Das Etikett sagt, was das Playbook macht und wann es gebraucht wird [Q8].
2. **In der dritten Person:** «Always write in third person» [Q8]. Auf Deutsch also «Baut …», «Prüft …», nicht «Ich helfe dir …».
3. **Konkrete Stichwörter:** Schreib die Wörter hinein, die du selbst verwenden würdest, etwa «Lernkontrolle», «Test», «Prüfung». Anthropic nennt als schlechtes Beispiel: «Helps with documents» [Q8].
4. **Abgrenzung:** Wofür das Playbook nicht gedacht ist und welches andere stattdessen passt [Q36].
5. **Lieber etwas zu deutlich:** Weil Claude Skills eher zu selten nutzt, rät Anthropics Hilfsanleitung, Beschreibungen «a little bit "pushy"» zu formulieren [Q26].
6. **Länge:** höchstens 1'024 Zeichen [Q7].

Deine bestehenden Skills machen das bereits so. Sie haben «Gilt, wenn …», «Abgrenzung: …» und «Trigger: «…»».

### 7.4 Sagen, was zu tun ist, und warum

- **Positiv formulieren:** «Tell Claude what to do instead of what not to do» [Q23].
- **Den Grund nennen:** Anthropic zeigt dazu ein Beispiel. «NEVER use ellipses» wirkt schlechter als die Begründung, dass die Antwort von einer Vorlesesoftware («text-to-speech engine») gelesen wird, die Auslassungspunkte nicht aussprechen kann [Q23]. Wer den Grund kennt, wendet die Regel auch in Fällen richtig an, an die du nicht gedacht hast.
- **Nicht schreien:** Grossbuchstaben und «UNBEDINGT» schaden bei neueren Modellen eher. Anthropic rät: «soften any aggressive language» [Q23]. Die Hilfsanleitung nennt ALWAYS und NEVER in Grossbuchstaben ein Warnsignal, eine «yellow flag» [Q26].

**Widerspruch in Anthropics Quellen:** Die Skill-Anleitung nennt stärkere Wörter wie «MUST» an einer Stelle als mögliche Korrektur [Q8]. **Meine Schlussfolgerung:** Betonung nur als letztes Mittel für eine einzelne Regel, die nachweislich übergangen wird, und am besten mit Begründung.

### 7.5 Länge und Aufbau

| Was | Richtwert | Quelle |
|---|---|---|
| Anleitung in `SKILL.md` | unter 500 Zeilen | «Keep the SKILL.md body under 500 lines for optimal performance» [Q8] |
| Etikett (Beschreibung) | höchstens 1'024 Zeichen | [Q7] |
| CLAUDE.md | unter 200 Zeilen pro Datei | [Q12] |
| Zusatzdateien | direkt aus `SKILL.md` verlinkt, nicht verschachtelt | «Keep references one level deep from SKILL.md» [Q8] |
| Lange Zusatzdateien | ab 100 Zeilen ein Inhaltsverzeichnis oben | «longer than 100 lines» [Q8] |
| Format | Überschriften, nummerierte Schritte, kurze Listen | [Q8, Q12] |

Die Zahlen sind Obergrenzen, keine Ziele. **Meine Schlussfolgerung:** Das beste Playbook ist das kürzeste, das im Test noch funktioniert.

### 7.6 Was die neueren Modelle anders machen

Anthropics Anleitungen zu den neuesten Modellen nennen vier Punkte, die Playbooks betreffen. Jeder gilt laut Anthropic für bestimmte Modelle. Ob er auch für das Modell gilt, das du gerade nutzt, zeigt nur ein Test.

1. **Wörtlicher:** Claude Sonnet 5 überträgt eine Regel nicht von selbst auf andere Fälle: Es «does not silently generalize an instruction from one item to another» [Q25]. Daher: «If you need Claude to apply an instruction broadly, state the scope explicitly» [Q25]. Also: «Gilt für alle Aufträge im Dossier, nicht nur für den ersten.»
2. **Alte Playbooks können schaden:** «Skills developed for prior models are often too prescriptive» [Q24]. Nach einem Modellwechsel lohnt es sich, Regeln zu streichen und zu testen, ob es ohne besser geht.
3. **Kein «Denken ausschreiben»:** Anweisungen, Claude solle sein inneres Nachdenken in die Antwort schreiben, können bei neueren Modellen zur Verweigerung führen. Anthropic nennt dafür eine eigene Kategorie, `reasoning_extraction` [Q24]. Eine kurze Begründung oder Zusammenfassung zu verlangen, ist erlaubt [Q24].
4. **Konkrete Schwellen:** Statt «nur wichtige Fehler melden» sagst du genau, was als Fehler zählt. Anthropic rät, eine Schwelle konkret zu benennen, «rather than using qualitative terms such as "important"» [Q25].

### 7.7 Die häufigsten Fehler

1. **Zu lang:** Die wichtigen Regeln gehen im Rauschen unter [Q13].
2. **Zu allgemein:** «Arbeite sorgfältig» hilft niemandem.
3. **Unklares Etikett:** Das Playbook wird nie geladen [Q1, Q40].
4. **Widersprüche:** zwischen zwei Playbooks oder zwischen Playbook und Anweisungen [Q12].
5. **Was Claude schon weiss:** kostet Platz und bringt nichts [Q8].
6. **Zu viele Wahlmöglichkeiten** statt einer klaren Standardwahl [Q8].
7. **Verschachtelte Verweise:** Datei A verweist auf B, B auf C. Claude liest dann womöglich nur Teile [Q8].
8. **Veraltete Angaben:** Termine, Jahrgänge, alte Versionen [Q8].
9. **Grossbuchstaben statt Gründe** [Q23, Q26].
10. **Keine Schlusskontrolle:** Claude meldet «fertig», ohne geprüft zu haben.
11. **Vertrauen auf Regeln, die halten müssen:** Was immer stimmen muss, prüfst du selbst oder sicherst es technisch ab [Q1].

---

## 8. Vorlage zum Ausfüllen

Diese Vorlage setzt die Bausteine aus Kapitel 6 um. Alles in eckigen Klammern ersetzt du. Bausteine, die du nicht brauchst, lässt du weg.

```markdown
---
name: [kurzer-name-mit-bindestrichen]
description: [Was es macht, in der dritten Person: «Baut …», «Prüft …».] Verwenden, wenn [typische Situationen und Stichwörter, die du selbst sagen würdest]. Nicht für [Abgrenzung] (dafür: [anderes Playbook]).
---

# [Titel]

[Ein Satz: Rolle von Claude.]

## Ziel
[Wozu dient das Ergebnis? Für wen ist es?]
[Warum sind die Regeln unten wichtig? Ein bis drei Sätze.]

## Was ich von dir brauche
Bevor du beginnst, kläre:
- [Angabe 1]
- [Angabe 2]
Fehlt etwas, frag nach, bevor du anfängst.

## Ablauf
Kopiere diese Checkliste in deine Antwort und hake ab:
- [ ] Schritt 1: [...]
- [ ] Schritt 2: [...]
- [ ] Schritt 3: [...]
- [ ] Schritt 4: Schlusskontrolle (siehe unten)

## Weggabelungen
- Wenn [Fall A]: [so vorgehen].
- Wenn [Fall B]: [anders vorgehen].
- Sonst: [Standardwahl].

## Vorlage für das Ergebnis
[Aufbau, Überschriften, Format. Sag, wie streng die Vorlage gilt.]

## Beispiel
[Ein kurzes, gutes Beispiel.]

## Stolperstellen
- [Typischer Fehler]: [was stattdessen zu tun ist].

## Schlusskontrolle
Prüfe vor der Abgabe:
- [Kriterium 1]
- [Kriterium 2]
Ist ein Punkt nicht erfüllt: verbessern und nochmals prüfen.

## Wann du anhältst und fragst
- [Situation, in der du entscheiden willst]

## Zusatzdateien
- Lies `[datei].md`, wenn [Situation].

## Feste Begriffe
- [Begriff]: [Bedeutung]. Verwende nur dieses Wort.
```

**So kommt die Vorlage zu Claude:**

- **In claude.ai:** Lege einen Ordner mit dem Namen des Skills an und speichere darin die Datei `SKILL.md`. Den Ordner lädst du als ZIP-Datei unter «Customize > Skills» hoch [Q10, Q18]. Der Ordnername muss mit dem `name` im Etikett übereinstimmen, sonst scheitert das Hochladen: «Skill folder name doesn't match the skill name» [Q18]. Eine ältere Anthropic-Seite nennt dafür noch den Weg über die Einstellungen («Settings > Features») [Q7]. Die Code-Ausführung muss eingeschaltet sein [Q17].
- **Mit Claude zusammen:** Du kannst Claude bitten, aus der Vorlage und deinem Material einen Skill zu bauen. Anthropic: «Claude models handle the Skill format and structure natively» [Q8]. Anthropic stellt dafür auch einen eigenen Hilfs-Skill namens «skill-creator» bereit [Q26].
- **In Claude Code:** Der Ordner kommt nach `~/.claude/skills/` (für dich persönlich) oder nach `.claude/skills/` im Projekt [Q11].

---

## 9. Durchgearbeitetes Beispiel: Lernkontrolle

**Wichtig vorweg:**

- Dieses Beispiel zeigt den **Aufbau**, nicht deine fachlichen Regeln.
- Die Fachbegriffe stammen aus den Beschreibungen deiner bestehenden Skills (zum Beispiel «lk-schriftlich», «lk-grundlagen», «lk-bewerten»). Deren Inhalte habe ich nicht gelesen.
- Wo deine Regeln stehen müssten, steht `[deine Regel]`.
- Du hast bereits einen Skill für diese Aufgabe. Nutze das Beispiel, um ihn mit der Struktur aus Kapitel 6 zu vergleichen.

### Der Ordner

```
lernkontrolle-fabe/
├── SKILL.md
├── kriterien.md      ← dein Massstab, wie das Legal-Playbook
└── beispiel.md       ← eine gelungene Lernkontrolle als Muster
```

### Die Datei SKILL.md

```markdown
---
name: lernkontrolle-fabe
description: Baut eine druckfertige schriftliche Lernkontrolle zu einer Lernsituation des BKU1 FaBe (Kind oder MmB) mit Praxissituation, Aufgaben mit K-Stufen-Progression, Punkteverteilung, Erwartungshorizont und Notenschlüssel. Verwenden, wenn jemand eine Lernkontrolle, einen Test oder eine Prüfung zu einer LS will, auch ohne das Wort «Lernkontrolle». Nicht für einzelne Aufgaben (dafür: aufgabentypen) und nicht für das Prüfen einer fertigen Lernkontrolle (dafür: lk-guetecheck).
---

# Schriftliche Lernkontrolle FaBe

Du bist eine erfahrene Lehrperson für Berufskunde FaBe und baust Lernkontrollen nach den Vorgaben in diesem Playbook.

## Ziel
Die Lernkontrolle prüft, ob die Lernenden die Lernziele der Lernsituation erreicht haben. Sie wird benotet. Deshalb muss jede Aufgabe auf ein Lernziel zurückgehen und die Punkte müssen nachvollziehbar sein: Eine Note muss vor Lernenden und Eltern begründbar sein.

## Was ich von dir brauche
Bevor du beginnst, kläre:
- Lernsituation (Nummer) und Fachrichtung (Kind oder MmB)
- Dauer der Lernkontrolle in Minuten
- Welche Lernziele geprüft werden
Fehlt etwas, frag nach. Erfinde keine Lernziele.

## Ablauf
Kopiere diese Checkliste in deine Antwort und hake ab:
- [ ] 1. Lernziele mit K-Stufe auflisten (aus dem Schullehrplan).
- [ ] 2. Praxissituation schreiben, aus der alle Aufgaben folgen.
- [ ] 3. Aufgaben ableiten: [deine Regel zur K-Stufen-Progression].
- [ ] 4. Punkte verteilen: [deine Regel zur Punkteverteilung].
- [ ] 5. Erwartungshorizont je Aufgabe schreiben.
- [ ] 6. Notenschlüssel nach `kriterien.md` erstellen.
- [ ] 7. Schlusskontrolle (siehe unten).
- [ ] 8. Entwurf zeigen und auf Freigabe warten. Erst danach die Datei bauen.

## Weggabelungen
- Fachrichtung Kind: [deine Regel].
- Fachrichtung MmB: [deine Regel].
- Steht ein Lernziel auf K6: höchstens auf K5 prüfen ([deine Begründung]).

## Vorlage für das Ergebnis
Halte dich genau an diesen Aufbau:
1. Kopf: [Felder]
2. Praxissituation
3. Aufgaben mit Punktzahl
4. Erwartungshorizont (separates Blatt)
5. Notenschlüssel

## Beispiel
Ein gelungenes Muster steht in `beispiel.md`. Lies es vor Schritt 2.

## Stolperstellen
- Aufgaben, die mit der Praxissituation nichts zu tun haben: jede Aufgabe auf die Situation beziehen.
- Operatoren, die nicht zur K-Stufe passen: [deine Operatorenliste].
- Punktsumme stimmt nicht mit dem Notenschlüssel überein: nachrechnen.

## Schlusskontrolle
Prüfe vor der Abgabe jeden Punkt in `kriterien.md`. Ist ein Punkt nicht erfüllt: verbessern und nochmals prüfen. Melde «fertig» erst, wenn alle Punkte erfüllt sind, und nenne die Punkte, die du nicht prüfen konntest.

## Wann du anhältst und fragst
- Wenn Lernziele fehlen oder unklar sind.
- Bevor du eine Datei baust.
- Wenn eine Vorgabe aus `kriterien.md` nicht umsetzbar ist.

## Feste Begriffe
- Lernkontrolle: die benotete schriftliche Prüfung. Nicht «Test», nicht «Prüfung».
- Erwartungshorizont: die erwarteten Antworten mit Punkten.
```

### Die Datei kriterien.md

```markdown
# Kriterien für Lernkontrollen

## Notenschlüssel
[deine Notenformel, Sockelwert, Rundung]

## Gütekriterien
- [ ] Jede Aufgabe geht auf ein Lernziel zurück.
- [ ] Die K-Stufe jeder Aufgabe liegt nicht über der K-Stufe ihres Lernziels.
- [ ] [dein Kriterium]
- [ ] [dein Kriterium]
```

### Was jeder Teil bewirkt

| Teil | Wirkung | Baustein |
|---|---|---|
| Etikett mit Stichwörtern und Abgrenzung | Claude lädt das Playbook bei «Test zu LS 2.08», aber nicht beim Prüfen einer fertigen Lernkontrolle | 1 |
| Ziel mit Begründung | Claude versteht, warum Punkte nachvollziehbar sein müssen, und achtet auch in unerwarteten Fällen darauf | 3 |
| «Erfinde keine Lernziele» | Verhindert, dass Claude Lücken mit Erfundenem füllt | 4 |
| Checkliste | Claude überspringt keinen Schritt und du siehst den Fortschritt | 5 |
| `kriterien.md` als eigene Datei | Du änderst den Massstab, ohne den Ablauf anzufassen, wie beim Legal-Plugin | 7, 10 |
| Schritt 8 und «Wann du anhältst» | Du behältst die Kontrolle über das Ergebnis | 11 |
| Feste Begriffe | Kein Durcheinander von «Test», «Prüfung», «Lernkontrolle» | Querschnitt |

---

## 10. Testen und pflegen

### 10.1 Anthropics Vorgehen in fünf Schritten

Anthropic sagt: «Create evaluations BEFORE writing extensive documentation» [Q8]. Erst testen, dann schreiben. Die Schritte [Q8]:

1. **Lücken finden:** Lass Claude die Aufgabe *ohne* Playbook lösen. Notiere, was fehlt oder falsch ist.
2. **Testfälle bauen:** «Build three scenarios that test these gaps» [Q8].
3. **Ausgangslage messen:** «Measure Claude's performance without the Skill» [Q8].
4. **Knapp schreiben:** Nur so viel, wie nötig ist, um die Lücken zu schliessen.
5. **Wiederholen:** testen, verbessern, nochmals testen.

### 10.2 Zwei Claudes

Anthropic empfiehlt: «Work with one instance of Claude ("Claude A") to create a Skill that is used by other instances ("Claude B")» [Q8]. Mit dem einen Claude schreibst du das Playbook. Ein frisches Gespräch mit einem zweiten Claude testet es an echten Aufgaben: «Give Claude B (with the Skill loaded) actual tasks» [Q8].

### 10.3 Ein einfacher Testplan für dich

**Meine Schlussfolgerung**, zusammengesetzt aus [Q8, Q35, Q36]:

1. Schreib drei echte Aufträge auf: einen salopp formulierten, einen genauen und einen Sonderfall.
2. Lass jeden in einem **neuen** Gespräch laufen.
3. Prüfe das Ergebnis mit drei bis fünf klaren Fragen, zum Beispiel: «Geht jede Aufgabe auf ein Lernziel zurück?»
4. Ändere jeweils nur eine Sache am Playbook und teste nochmals.
5. Teste auch das Etikett: Formuliere Bitten, bei denen das Playbook laden soll, und ähnliche, bei denen es *nicht* laden soll. Anthropic-nahe Quellen empfehlen dafür etwa 20 Anfragen: «Aim for about 20 queries» [Q36].

### 10.4 Der Kollegentest

Ein einfacher Test von Anthropic: «Show your prompt to a colleague with minimal context on the task and ask them to follow it» [Q23]. Würde eine Kollegin oder ein Kollege mit deinem Playbook scheitern, scheitert auch Claude.

### 10.5 Pflege

- **Nach jedem Modellwechsel neu testen:** «Test your Skill with all the models you plan to use it with» [Q8]. Laut Anthropic kann es bei neuen Modellen sogar besser sein, alte Regeln zu streichen [Q24].
- **Es gibt kein eingebautes Testwerkzeug:** «There is not currently a built-in way to run these evaluations» [Q8].
- **In Claude Code** gibt es einen Prüfbefehl, `/doctor prompt-audit`. Er sucht nach veralteten oder widersprüchlichen Anweisungen [Q11, Q12].
- **Meine Schlussfolgerung:** Schreib oben ins Playbook, wem es gehört und wann es zuletzt geprüft wurde. Wenn Claude eine Regel zweimal falsch macht, verbesserst du das Playbook, statt dieselbe Korrektur immer wieder im Chat zu tippen.

---

## 11. Nutzen, Grenzen, Risiken

### 11.1 Was belegt ist

**Studie 1: SkillsBench** [Q38, Studie von Forschenden, nicht von Anthropic]. Getestet wurden 87 Aufgaben aus 8 Fachgebieten, jeweils mit und ohne Skill.

- «Curated Skills raise the average pass rate from 33.9% to 50.5%» [Q38]. Mit sorgfältig geschriebenen Skills stieg die Erfolgsquote also im Schnitt von rund einem Drittel auf rund die Hälfte.
- «Focused Skills with at most three modules outperform larger or exhaustive bundles» [Q38]. Kleine, fokussierte Skills waren besser als grosse, vollständige.
- «smaller models with Skills can match larger models without them» [Q38]. Ein kleineres Modell mit Skill kann ein grösseres ohne Skill einholen.
- Laut Subagent fand die Studie zudem: Skills, die ein Modell selbst geschrieben hatte, brachten im Schnitt nichts (○, nicht in der Zusammenfassung, nicht von mir nachgeprüft).

**Studie 2: Kontextdateien für Programmier-Agenten** [Q37, Studie von Forschenden]. Hier ging es um allgemeine Dateien mit Projektbeschreibungen, ähnlich einer CLAUDE.md.

- «providing context files does not generally improve task success rates, while increasing inference cost by over 20% on average» [Q37]. Solche Dateien brachten im Schnitt keinen Erfolg, kosteten aber über 20 Prozent mehr Rechenleistung.
- Aber: «instructions in the context files are well followed by coding agents» [Q37]. Die Anweisungen wurden befolgt.
- Und: «repository overviews, although popular and recommended by model providers, are not helpful» [Q37]. Allgemeine Überblicke halfen nicht. Nützlich waren die Dateien dort, wo sie Abweichungen vom Üblichen festhielten («non-standard coding practices») [Q37].

**Was die beiden Studien zusammen sagen** (Meine Schlussfolgerung): Ein Playbook lohnt sich, wenn es Wissen enthält, das Claude nicht hat: deine eigenen Regeln und Abläufe. Es lohnt sich nicht, wenn es Allgemeines wiederholt. Beides deckt sich mit Anthropics Regel «Only add context Claude doesn't already have» [Q8].

### 11.2 Was nicht belegt ist

- Anthropic veröffentlicht keine eigenen Messungen, wie viel Zeit oder Qualität Skills bringen (○, Ergebnis der Recherche).
- Für Bildung gibt es keine veröffentlichte Messung mit und ohne Playbook (○).
- Versprechen von Büchern und Kursen («in einem Bruchteil der Zeit») sind nicht belegt (○).
- Beide Studien testeten Programmier- und Fachaufgaben, nicht Unterrichtsmaterial. Ob die Ergebnisse auf Lernkontrollen übertragbar sind, ist offen.

### 11.3 Grenzen

- **Keine Garantie:** Ein Playbook ist eine Bitte (Kapitel 4.7).
- **Auslösen ist unsicher:** Das Etikett muss passen [Q1, Q40].
- **Zu viele Skills:** Claude wählt dann womöglich falsch [Q9].
- **Zu lang:** Regeln gehen unter [Q13].
- **Widersprüche:** Claude wählt willkürlich [Q12].
- **Lange Gespräche:** Was nur im Chat gesagt wurde, kann bei der Zusammenfassung verloren gehen. Geladene Skills werden in Claude Code nur gekürzt wieder angehängt [Q11].
- **Modelle sind verschieden:** «What works perfectly for Opus might need more detail for Haiku» [Q8]. Opus und Haiku sind zwei Claude-Modellreihen, Opus die grösste, Haiku die kleinste (Allgemeinwissen).

### 11.4 Sicherheit

- Anthropic nennt das Hauptrisiko: «The most significant risks are prompt injection» [Q18]. Gemeint ist, dass versteckte Anweisungen Claude zu ungewollten Handlungen bringen.
- Darum: «Only install skills only from trusted sources» [Q18], so im Original. Und auch bei Skills von Kolleginnen und Kollegen: «review it before enabling» [Q18].
- Anthropic prüft hochgeladene Skills auf schädliche Inhalte («checked for malicious content») [Q18]. Wie gründlich, steht nicht dabei.
- Plugins für Claude Code können Programme ausführen: «can execute arbitrary code on your machine with your user privileges» [Q16].
- Auch reiner Text ist ein Risiko: «Skills, commands, and agents: these enter Claude's context as instructions» [Q16].
- Eine Untersuchung von über 31'000 Skills aus öffentlichen Sammlungen fand: «26.1% of skills contain at least one vulnerability» [Q39]. Skills mit Programmen waren riskanter: «skills bundling executable scripts are 2.12x more likely to contain vulnerabilities» [Q39]. Die Stichprobe stammt aus fremden Sammlungen, nicht aus Anthropics eigenem Angebot.

**Meine Schlussfolgerung:** Eigene Skills und solche von Anthropic sind unbedenklich. Fremde Skills liest du vor dem Einschalten durch, besonders wenn sie Programme enthalten.

### 11.5 Datenschutz

Nicht recherchiert: Schweizer Datenschutzregeln und die Vorgaben deiner Schule. Die Recherche fand auch keine Angabe, wie lange Anthropic hochgeladene Skills speichert (○).

**Meine Schlussfolgerung:** Schreib keine Namen, Noten oder Daten von Lernenden in ein Playbook. Ein Playbook enthält Regeln und Vorlagen, keine Personen. Was mit Daten von Lernenden erlaubt ist, klärst du mit deiner Schule.

---

## 12. Wofür sich ein Playbook lohnt

### 12.1 Zwei Faustregeln von Anthropic

Die Claude-Code-Dokumentation nennt zwei Auslöser [Q1]:

- «Claude gets a convention or command wrong twice»: Dann gehört die Regel in die Dauerregeln.
- «You paste the same playbook or multi-step procedure into chat for the third time»: Dann wird ein Skill daraus.

**Meine Schlussfolgerung:** Beim zweiten Fehler eine Dauerregel, bei der dritten Wiederholung ein Playbook. Für einmalige Aufgaben lohnt es sich nicht.

### 12.2 Vier Muster

Die Recherche fand vier wiederkehrende Muster. Die Einteilung ist eine Synthese des Recherche-Subagenten, Anthropic nennt sie nicht so. Deine bestehenden Skills (aus der Liste in dieser Sitzung) zeigen alle vier.

| Muster | Was es tut | Beispiel von Anthropic | Beispiel aus deinen Skills |
|---|---|---|---|
| **Prüfen gegen einen Massstab** | Vergleicht etwas Fertiges mit festen Kriterien | Legal-Plugin: Vertrag gegen Playbook [Q3] | «lk-guetecheck»: Lernkontrolle gegen vier Raster |
| **Dokument in festem Format** | Baut immer dieselbe Art von Ergebnis | Skills für Word, PowerPoint, Excel, PDF (○) | «powerpoint-basix»: Folien streng aus deiner Vorlage |
| **Ablauf mit Freigaben** | Mehrere Schritte mit Halt vor wichtigen Schritten | Kein Beispiel gefunden | «ad-auftrag»: «ohne Freigabe im Wortlaut wird nicht gebaut» |
| **Nachschlagewissen** | Stellt festes Wissen bereit | Firmenwissen in Plugins [Q27] | «bildungsplan-fabe»: 571 Leistungsziele |

### 12.3 Was Anthropic für andere Berufe anbietet

Anthropic stellt Plugins für Berufsgruppen bereit, darunter Recht, Finanzen, Kundendienst und Produktmanagement [Q27]. Dazu sagt Anthropic: «These plugins are generic starting points» und rät, sie anzupassen: «Modify skill instructions to match how your team actually does things» [Q27].

**Meine Schlussfolgerung:** Ein fertiges Playbook ist ein Anfang. Wertvoll wird es durch deine eigenen Regeln.

### 12.4 Bildung: was Anthropic zeigt und was Lehrpersonen sagen

- **Wie Hochschul-Lehrpersonen Claude nutzen:** Anthropic hat rund 74'000 Gespräche ausgewertet. Am häufigsten ging es um das Entwickeln von Unterricht: «Develop curricula (57% of the conversations in our analysis)» [Q28]. Das Bewerten war seltener: «Assess student performance (7%)» [Q28]. Befragte Lehrpersonen nannten das Bewerten den Bereich, in dem KI am wenigsten taugt («least effective») [Q28].
- **Ein Rat aus dieser Befragung:** «Use it as a thought partner, not a thought substitute» [Q28].
- **Claude for Education** (2025): Ein Lernmodus für Studierende, der Fragen stellt statt Antworten zu geben: «Learning mode, a feature that works within Projects» [Q29]. Lehrpersonen können zum Beispiel «rubrics aligned to specific learning outcomes» erstellen [Q29].
- **Claude for Teachers** (14. Juli 2026): Fertige Skills für Unterrichtsplanung und Differenzierung, aber nur für «verified K-12 educators in the US» [Q30]. Für dich in der Schweiz ist das Angebot nicht zugänglich.
- **Kritik:** Eine US-Lehrperson sagt in Education Week, allgemeine Sprachmodelle seien «mediocre», wenn sie eine allgemeine Lektion zu einem Standard schreiben sollen, und warnt vor einem Verlernen bei jungen Lehrpersonen [Q42, ○].

**Meine Schlussfolgerung:** Die Kritik spricht *für* eigene Playbooks. Ein allgemeines Playbook liefert allgemeine Lektionen. Ein Playbook mit deinem Lehrplan, deiner Klasse und deinen Vorlagen liefert etwas, das zu deinem Unterricht passt.

### 12.5 Gute und schlechte Kandidaten im Unterricht

**Meine Schlussfolgerung**, gestützt auf [Q1, Q8, Q28]:

| Gut geeignet | Weniger geeignet |
|---|---|
| Lernkontrollen und Dossiers in festem Aufbau | Einmalige, kreative Ideen |
| Folien aus deiner Vorlage | Brainstorming ohne feste Form |
| Prüfen eines fertigen Dokuments gegen Kriterien | Die endgültige Note für eine Person |
| Abläufe mit Freigaben | Rückmeldungen, die persönliche Daten brauchen |
| Nachschlagen in Lehrplan und Bildungsplan | Fakten, die sich laufend ändern |
| Gemeinsame Vorlagen im Team | Aufgaben, die Claude ohne Hilfe schon gut löst |

---

## 13. Fragen, die du vielleicht nicht gestellt hast

**Sind meine bestehenden Skills schon Playbooks?**
Ja. Sie folgen sogar dem empfohlenen Etikett-Muster mit «Gilt, wenn …», «Abgrenzung» und «Trigger». Was fehlen kann, zeigt der Vergleich mit Kapitel 6.

**Muss ich programmieren können?**
Nein. Ein Playbook ist Text in einer Markdown-Datei. Anthropic über seine Plugins: «markdown and JSON, no code» [Q27]. Programme (Skripte) sind freiwillig. Sie helfen bei Aufgaben, die immer exakt gleich ablaufen müssen, etwa Berechnungen [Q8].

**Kann Claude mir helfen, ein Playbook zu schreiben?**
Ja [Q8, Q26]. Gib Claude aber dein Material mit: Vorlagen, Kriterien, ein gelungenes Beispiel. Ohne Material entstehen allgemeine Floskeln [Q35].

**Warum ignoriert Claude manchmal mein Playbook?**
Mögliche Gründe: Das Etikett passt nicht zur Bitte. Das Playbook ist zu lang. Eine Regel widerspricht einer anderen. Das Gespräch ist sehr lang geworden. Oder Claude hat eine Regel schlicht übergangen, was laut Anthropic vorkommt [Q8]. Erster Schritt: das Etikett prüfen. Anthropic rät: «Check that the skill's description field clearly explains when it should be used» [Q18].

**Wie viele Skills kann ich haben?**
Für claude.ai ist keine Obergrenze dokumentiert. Viele Skills machen die Auswahl aber unsicherer [Q9]. In Claude Code ist der Platz für die Etiketten begrenzt: Wird er knapp, fallen die Beschreibungen selten benutzter Skills zuerst weg [Q11].

**Was ist der Unterschied zwischen Projekt und Skill?**
Ein Projekt ist ein Arbeitsraum mit Wissen, das dort immer bereitliegt. Ein Skill ist ein Ablauf, der nur bei Bedarf geladen wird [Q10]. Faustregel: Projekt für «worüber», Skill für «wie».

**Gilt mein Playbook auch in Cowork und Claude Code?**
Skills aus deinem claude.ai-Konto lädt Cowork automatisch [Q11]. Claude Code lädt sie herunter, schreibt aber Änderungen nicht zurück [Q11]. Wenn du einen Skill verbessern willst, änderst du ihn deshalb in claude.ai.

**Kann ich Playbooks mit Kolleginnen und Kollegen teilen?**
In Team- und Enterprise-Konten ja [Q19]. Die Empfängerinnen und Empfänger können den Skill nutzen, aber nicht ändern [Q19]. Ohne solches Konto kannst du den Ordner als Datei weitergeben (Meine Schlussfolgerung).

**Reicht das Gratis-Abo?**
Unklar. Die Hilfe-Seiten sagen: «Skills are available for users on Free, Pro, Max, Team, and Enterprise plans» [Q17, Q18]. Die Entwicklerseiten nennen nur Pro, Max, Team und Enterprise [Q7, Q10]. Am sichersten prüfst du es direkt in deinem Konto.

**Muss ich Playbooks nach einem Modellwechsel anpassen?**
Testen ja, anpassen vielleicht. Anthropic warnt, dass ältere Skills für neue Modelle zu eng sein können [Q24]. Gleichzeitig verbessern neue Modelle Skills teils selbst: «Claude Fable 5 also does a good job of updating skills as it works» [Q24].

**Sind fremde Skills sicher?**
Nicht automatisch. Siehe Kapitel 11.4.

**Darf ich Daten von Lernenden in ein Playbook schreiben?**
Siehe Kapitel 11.5. Meine Empfehlung: nein.

**Was ist mit «Stilen» (Styles) auf claude.ai?**
Laut Recherche ersetzt Anthropic die Stile durch Skills. **Nicht geprüft:** Die Hilfe-Seite dazu war nicht erreichbar.

**Ersetzt ein Playbook meine Kontrolle?**
Nein. Anthropic sagt selbst, dass Anweisungen keine Garantie sind [Q1]. Lehrpersonen halten das Bewerten für den Bereich, in dem KI am wenigsten taugt [Q28]. Ein Playbook macht Claude verlässlicher, die Verantwortung bleibt bei dir.

**Wie lang soll mein erstes Playbook sein?**
So kurz wie möglich. Fang mit Etikett, Ziel, Schritten und Schlusskontrolle an. Ergänze nur, was im Test fehlt [Q8].

**Lohnt sich ein gekauftes «Claude Playbook»?**
Nicht bewertet. Die Recherche fand keine unabhängigen Bewertungen solcher Bücher (○). Anthropics eigene Anleitungen sind frei zugänglich (Kapitel 15).

---

## 14. Widersprüche und offene Punkte

**Widersprüche in Anthropics eigenen Quellen**

1. **Gratis-Abo und Skills:** Hilfe-Seite ja [Q17, Q18], Entwicklerseiten nein [Q7, Q10].
2. **Skills in der Organisation teilen:** Die Entwicklerseite sagt nein [Q7], die neuere Hilfe-Seite ja [Q19]. Die Hilfe-Seite ist wahrscheinlich aktueller.
3. **Betonung:** Die Hilfsanleitung nennt Grossbuchstaben eine «yellow flag» [Q26], die Skill-Anleitung schlägt «MUST» als mögliche Korrektur vor [Q8].
4. **Form des Etiketts:** dritte Person laut [Q8], dagegen «Use this skill when …» in der Befehlsform laut [Q26, Q36]. Meine Schlussfolgerung: beides verbinden, wie in der Vorlage («Baut … Verwenden, wenn …»).
5. **Begründen oder nicht:** Die Prompt-Anleitung rät, Gründe zu nennen [Q23]. Die Claude-Code-Skill-Seite rät aus Platzgründen, eher zu sagen, was zu tun ist (○). Meine Schlussfolgerung: kurze Gründe nur bei Regeln, die Claude sonst falsch anwenden würde.

**Offene Punkte**

- Wie Claude genau entscheidet, ob ein Etikett passt, ist nicht dokumentiert.
- Keine Rangfolge auf claude.ai zwischen Anweisungen, Projekt, Skill und Memory.
- Keine Messung mit und ohne Playbook für Unterrichtsmaterial.
- Keine Schweizer Quellen (Berufsbildung, EHB, Datenschutz) in der Recherche.
- Wie lange Anthropic hochgeladene Skills speichert: nicht gefunden.
- Ob claude.ai und Cowork Skills nach einer Gesprächszusammenfassung gleich behandeln wie Claude Code: nicht dokumentiert.

---

## 15. Quellen

✔ = zitierte Stellen am 23.10.2026 im heruntergeladenen Originaltext gefunden. ○ = von einem Recherche-Subagenten gelesen, nicht selbst nachgeprüft.

**Anthropic: Dokumentation zu Claude Code**

- [Q1] ✔ Extend Claude Code (Features overview): https://code.claude.com/docs/en/features-overview
- [Q2] ✔ Glossary: https://code.claude.com/docs/en/glossary
- [Q11] ✔ Skills: https://code.claude.com/docs/en/skills
- [Q12] ✔ How Claude remembers your project (Memory, CLAUDE.md): https://code.claude.com/docs/en/memory
- [Q13] ✔ Best practices: https://code.claude.com/docs/en/best-practices
- [Q14] ✔ Context window: https://code.claude.com/docs/en/context-window
- [Q15] ✔ Hooks guide: https://code.claude.com/docs/en/hooks-guide
- [Q16] ✔ Plugin security: https://code.claude.com/docs/en/plugins/security

**Anthropic: Dokumentation zu Skills und Prompts**

- [Q7] ✔ Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- [Q8] ✔ Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- [Q9] ✔ Skills for enterprise: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise
- [Q10] ✔ Skills overview (claude.com): https://claude.com/docs/skills/overview
- [Q23] ✔ Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- [Q24] ✔ Prompting Claude Fable 5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- [Q25] ✔ Prompting Claude Sonnet 5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
- [Q26] ✔ skill-creator (Anthropics Hilfs-Skill): https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
- [Q31] ○ Plugin platform support: https://claude.com/docs/plugins/platform-support

**Anthropic: Hilfe-Center**

- [Q17] ✔ What are skills?: https://support.claude.com/en/articles/12512176-what-are-skills
- [Q18] ✔ Using skills in Claude: https://support.claude.com/en/articles/12512180-using-skills-in-claude
- [Q19] ✔ Provision and manage skills for your organization: https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization
- [Q20] ✔ Set organization instructions: https://support.claude.com/en/articles/14546867-set-organization-instructions
- [Q21] ✔ Retrieval augmented generation (RAG) for projects: https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects
- [Q22] ✔ Understanding Claude's personalization features: https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features

**Anthropic: Plugins und Academy**

- [Q3] ✔ Legal-Plugin, README: https://github.com/anthropics/knowledge-work-plugins/blob/main/legal/README.md
- [Q4] ✔ Legal-Plugin, Skill «review-contract»: https://github.com/anthropics/knowledge-work-plugins/blob/main/legal/skills/review-contract/SKILL.md
- [Q5] ○ Claude for Legal (neuere Plugins): https://github.com/anthropics/claude-for-legal
- [Q6] ✔ Anthropic Academy, Plugins in Cowork: https://academy.claude.com/courses/introduction-to-claude-cowork/plugins-cowork-as-a-specialist
- [Q27] ✔ Knowledge-work-plugins, README: https://github.com/anthropics/knowledge-work-plugins
- [Q32] ○ claude.com Blog, Steering Claude Code (18.6.2026): https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- [Q33] ○ Leitfäden mit «Playbook» im Titel: https://claude.com/blog/the-founders-playbook und https://claude.com/resources/articles/the-ai-native-sdlc-playbook
- [Q45] ○ Anthropic Academy, Customize Claude Cowork: https://academy.claude.com/tutorials/customize-claude-cowork

**Anthropic: Bildung**

- [Q28] ✔ Anthropic Education Report: How educators use Claude (2025): https://www.anthropic.com/news/anthropic-education-report-how-educators-use-claude
- [Q29] ✔ Introducing Claude for Education (2.4.2025): https://www.anthropic.com/news/introducing-claude-for-education
- [Q30] ✔ Claude for Teachers (14.7.2026): https://www.anthropic.com/news/claude-for-teachers

**Offener Standard für Skills (agentskills.io)**

- [Q34] ✔ Agent Skills Specification: https://agentskills.io/specification
- [Q35] ✔ Best practices for skill creators: https://agentskills.io/skill-creation/best-practices
- [Q36] ✔ Optimizing descriptions: https://agentskills.io/skill-creation/optimizing-descriptions

**Studien**

- [Q37] ✔ Gloaguen et al.: Evaluating AGENTS.md. Are Repository-Level Context Files Helpful for Coding Agents? arXiv 2602.11988: https://arxiv.org/abs/2602.11988
- [Q38] ✔ SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks. arXiv 2602.12670: https://arxiv.org/abs/2602.12670
- [Q39] ✔ Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale. arXiv 2601.10338: https://arxiv.org/abs/2601.10338
- [Q40] ✔ Demystifying Agent Skills for Smart Contract Auditing. arXiv 2609.29454: https://arxiv.org/abs/2609.29454

**Andere Anbieter und Medien**

- [Q41] ✔ borncity.com: Claude Playbooks: Anthropic startet KI-Planungs-Plattform heute (13.6.2026). Als unzuverlässig eingestuft.: https://borncity.com/news/claude-playbooks-anthropic-startet-ki-planungs-plattform-heute/
- [Q42] ○ Education Week via GovTech: Educators share mixed reactions to Claude for Teachers (21.7.2026): https://www.govtech.com/education/k-12/educators-share-mixed-reactions-to-claude-for-teachers
- [Q43] ○ Beispiele aus der Community: playbook-ai (https://github.com/bluemax713/playbook), awesome-claude-md (https://github.com/josix/awesome-claude-md), claudecodehq (https://www.claudecodehq.com/)
- [Q44] ○ E-Book «The Claude Playbook»: https://payhip.com/b/Dk3OB

**Zur Entstehung**

Die Recherche lief am 23. Oktober 2026 mit sechs Recherche-Subagenten zu je einem Teilthema: Begriff und offizielle Quellen, technische Mechanik, Schreibregeln, Praxisbeispiele, Nutzen und Risiken, Einsatzfelder. Ihre Ergebnisse wurden geprüft. Die Zitate der mit ✔ markierten Quellen wurden mit einem Skript im heruntergeladenen Originaltext gesucht und gefunden. Die Arbeitsnotizen der Recherche sind nicht Teil dieses Repositorys.
