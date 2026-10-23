---
typ: verfahren
kurz: Achtpunkt-Prüfliste, mit der eine fertige Einstiegs- oder Ergebnissicherungsfrage gegen die höchste K-Stufe der Lernziele geprüft wird. Die Fragegrammatik entscheidet, nicht der Operator allein.
quelle:
- 'Basic, D.: Verfahren Leitfragen-Klammer (Skill praxis-ergebnissicherung, SKILL.md Abschnitt «DIE zentrale Regel» und references/verfahren.md Schritt 2)'
- Operatorenliste des Skills aufgabentypen (unterrichten 0.16.0), references/k-stufen-operatoren.md; Zusammenstellung des Skills, nicht Teil der Palette
status: belegt
entscheide:
- E-090
- E-128
- E-162
verwandt:
- "[[Leitfragen-Klammer zur Ergebnissicherung]]"
- "[[Operatoren und K-Stufen]]"
- "[[K-Stufen im Überblick]]"
- "[[Aufgabentyp 04 Offene Verständnisfrage]]"
---

## Kurz

Achtpunkt-Prüfliste, mit der eine fertige Einstiegs- oder Ergebnissicherungsfrage gegen die höchste K-Stufe der Lernziele geprüft wird. Die Fragegrammatik entscheidet, nicht der Operator allein.

## Wozu

[[Leitfragen-Klammer zur Ergebnissicherung]] regelt, wie eine Frage gebaut wird. Für eine bestehende Frage fehlte ein Prüfweg. Diese Notiz schliesst die Lücke.

## Prüfliste

1. Welche K-Stufe tragen die Lernziele dieses Teils? Die höchste zählt.
2. Beginnt die Frage mit «Darf», «Soll», «Gilt», «Ist es richtig» oder «Wer hat recht»? Dann ist sie ein Urteil und bei Zielen unter K6 unzulässig.
3. Enthält sie einen Superlativ der Bedeutung, etwa «das Wichtigste», «am schwersten», «wiegt mehr», «das Richtige»? Dann verlangt sie Gewichten, also mindestens K4.
4. Verlangt sie, eine Regel auf den Fall anzuwenden, etwa «welche Informationen darf sie weitergeben»? Dann ist sie K3, nicht K2.
5. Fragt sie nach einem Unterschied? Ohne Gewichtung K2, mit Gewichtung K4.
6. Fragt sie «Warum»? Das Erklären eines bekannten Zusammenhangs ist K2, eine eigene Analyse K4.
7. Beginnt sie mit «Was» oder «Welche» und trägt sie die Klammer? Dann reicht sie bei Zielen ab K3 nicht tief genug.
8. Steht dieselbe Frage in Runde 1 und Runde 2? Ohne das entsteht keine Klammer.

## Fragegrammatik und K-Stufe

| Fragetyp | Stufe | Beleg |
|---|---|---|
| Was, Welche, Wer, Wo, Wann | K1 bis K2 | Skill, references/verfahren.md Schritt 2 |
| Warum, Wie kommt es | K2; mit eigener Analyse K4 | «erklären» K2, «begründen» K2 bis K4 (E-083) |
| Wie würden Sie anwenden | K3 | Aufgabentyp 7, Skill Schritt 2 |
| Welche darf, welche muss (Regel auf den Fall) | K3 | eine Bestimmung anwenden ist K3 |
| Worin unterscheiden sich | K2 ohne Gewichtung, K4 mit Gewichtung | Aufgabentyp 6 trägt K2 bis K4 |
| Superlativ der Bedeutung | K4 bis Bewertung | «gewichten» K4 laut Liste, K6 bei Lehren und Lernen |
| Ist das, Konnte, Wäre (Entscheidungsfrage ohne Fragewort) | K2 bis K4 | «einschätzen» K4 laut Liste |
| Darf, Soll, Gilt, Wer hat recht, Wie soll X handeln | Bewertung, in FaBe gesperrt | Skill: «Häufigste Falle … das ist bewerten und handeln» |

## Zwei Unterscheidungen, die der Skill nicht nennt

**Entscheidungsfrage gegen Ergänzungsfrage.** «Darf das Team darüber reden?» ist ein Urteil. «Welche Informationen darf sie weitergeben?» fragt nach der Rechtslage. Dasselbe Modalverb, drei Stufen Unterschied.

**Leitfrage gegen Hilfsfrage.** Die Tiefe muss die Leitfrage der Klammer erreichen. Flache Fragen im Einstieg sind kein Fehler, denn Runde 1 soll laut Skill spontan und aus dem Vorwissen beantwortet werden.

## Mechanische Prüfung

`00 Start/Prüfungen/fragecheck.py` liest die Arbeitsdossiers, zieht je Teil die K-Stufen aus den Lernzieltabellen und urteilt über jede gefundene Frage. `raster.py` enthält die Fragetypen, `raster_proben.py` prüft das Raster an sechzehn Proben. Dossiers ohne Teilstruktur oder ohne K-Stufen meldet die Prüfung als «nicht prüfbar», statt sie stillschweigend zu überspringen.

## Entscheid David (E-090, 07.10.2026)

Prüfliste und Skripte kommen in den Vault. Der Skill praxis-ergebnissicherung bleibt zunächst unverändert; eine Erweiterung dort folgt, wenn sich das Raster im Gebrauch hält. Befund B-061.
