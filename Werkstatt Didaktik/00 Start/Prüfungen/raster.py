#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zuordnung Fragegrammatik -> K-Stufe.

Jede Zeile traegt ihren Beleg. Belegquellen:
  SK  = Skill praxis-ergebnissicherung, SKILL.md, Abschnitt «DIE zentrale Regel»
  SKV = Skill praxis-ergebnissicherung, references/verfahren.md, Schritt 2 (Tabelle)
  PAL = Operatorenliste der Palette (Skill aufgabentypen, k-stufen-operatoren.md)
  KN  = K-Stufen-Notizen des Vaults, «40 Aufgaben und Operatoren»
  P6  = Aufgabentypen-Palette, Original-PDF, Abschnitt «Wichtige Einschraenkung»

Die Stufe steht als Menge zulaessiger K-Stufen. "BEW" heisst Bewertung oder
Handlungsentscheid; das ist in FaBe K6 und laut Palette gesperrt.
"""
import re

# (Name, Regex auf die Frage, zulaessige Stufen, Beleg, Erlaeuterung)
MUSTER = [
 ("Bewertungsfrage: Erlaubnis",
  # Nur die Entscheidungsfrage: der Satz beginnt mit dem Modalverb und verlangt
  # ein Ja oder Nein. «Welche Informationen darf sie weitergeben?» ist dagegen
  # eine Ergaenzungsfrage nach der Rechtslage und wird weiter unten erfasst.
  r'^\s*(und\s+)?(darf|dürfen|durfte|durften)\b',
  {"BEW"}, "SK",
  "«Darf X?» als Ja-Nein-Frage verlangt ein Urteil ueber Zulaessigkeit."),

 ("Bewertungsfrage: Sollen",
  r'^\s*(und\s+)?(soll|sollen|sollte|sollten)\b',
  {"BEW"}, "SK",
  "Der Skill nennt «Soll X eingreifen?» ausdruecklich als K4-K6-Falle."),

 ("Bewertungsfrage: Wer hat recht",
  r'\bwer\s+hat\s+recht\b|\brecht\s+hat\b|\bwer\s+von\s+(ihnen|beiden)\b',
  {"BEW"}, "SK",
  "Der Skill nennt «Wer hat recht?» ausdruecklich als Falle."),

 ("Bewertungsfrage: Handlungsentscheid",
  r'\bwie\s+(soll|sollte|muss|müsste|würde)\b.*\b(handeln|vorgehen|reagieren|entscheiden)\b'
  r'|\bwas\s+(sage|sagen|tue|tun|mache|machen)\s+(ich|sie|wir)\s+jetzt\b',
  {"BEW"}, "SK",
  "«Wie soll X handeln?» ist laut Skill bewerten und handeln, nicht K1-K2."),

 ("Bewertungsfrage: Geltung einer Zustimmung",
  # Nur die Guetigkeit einer Aussage oder Entscheidung, nicht der Geltungsbereich
  # einer Norm. «Fuer wen gelten die Artikel?» ist eine Wissensfrage.
  r'^\s*gilt\b(?!\s+(für|fuer)\b)|\bgilt\s+(das|dies|sein|ihr|pierres|ihre)\b'
  r'|\bist\s+das\s+(in\s+ordnung|zulässig)\b',
  {"BEW"}, "SK",
  "«Gilt X?» verlangt ein Urteil nach Kriterien, das ist K6."),

 ("Bewertungsfrage: Rechtfertigung",
  r'\bist\s+es\s+(richtig|falsch|vertretbar|zulässig|in\s+ordnung)\b'
  r'|\bwar\s+das\s+(richtig|falsch)\b',
  {"BEW"}, "KN",
  "K6 laut Notiz: «nach Kriterien werten und ein begruendetes Urteil faellen»."),

 ("Wertfrage: Gewichtung per Superlativ",
  r'\b(das\s+wichtigste|am\s+wichtigsten|am\s+schwersten|am\s+stärksten|das\s+beste'
  r'|am\s+besten|wiegt\s+(für\s+\w+\s+)?\w*\s*(schwerer|mehr)|das\s+entscheidende|am\s+meisten|das\s+richtige|das\s+falsche)\b',
  {"K4", "BEW"}, "PAL",
  "Eine Rangfolge nach Bedeutung verlangt Gewichten; «gewichten» ist K4 "
  "laut Liste und K6 laut Lehren und Lernen. Bei K1-K2-Zielen unzulaessig."),

 ("Analysefrage: Unterschied mit Gewichtung",
  r'\b(worin|was)\b.*\b(unterscheid\w+|abgrenz\w+|gegenüber)\b.*\b(wichtig|schwerer|stärker|gewicht\w+|grenzen)\b',
  {"K4"}, "PAL",
  "Vergleichen mit Gewichtung und Grenzen ist K4 (Hinweis im Skill aufgabentypen)."),

 ("Verstehensfrage: Unterschied ohne Gewichtung",
  r'\b(worin|was|wie)\b.*\b(unterscheid\w+|abgrenz\w+|verschieden)\b',
  {"K2", "K3", "K4"}, "SKV",
  "«unterscheiden» fuehrt der Skill bei K1-K2; mit Kriterienraster K2, "
  "mit Gewichtung K4. Ohne Zusatzmerkmal nicht eindeutig."),

 ("Analysefrage: Zusammenhang und Folge",
  r'\b(welche\s+folge|was\s+folgt\s+daraus|wie\s+hängen|wie\s+wirkt\s+sich|warum\s+hat)\b',
  {"K4"}, "PAL",
  "Beziehungen aufdecken und ableiten ist K4."),

 ("Anwendungsfrage: Norm auf den Fall",
  # W-Frage mit Modalverb und Fallbezug: die Regel muss auf die Situation
  # angewendet werden, das ist K3 (Aufgabentyp 7).
  # Nur Erlaubnis: «welche … darf …». «muss» und «soll» stehen oft in
  # Nebensaetzen ohne Normbezug («ohne dass er es verdienen muss») und sind
  # darum hier nicht aufgenommen.
  r'\b(welche[rsn]?|wen|wem)\b.{0,80}\b(darf|dürfen)\b',
  {"K3", "K4", "K5"}, "SKV",
  "Eine Bestimmung auf eine konkrete Situation anwenden ist K3, nicht K2."),

 ("Anwendungsfrage",
  r'\bwie\s+(würden|wenden|setzen|gehen)\s+sie\b|\bwie\s+lässt\s+sich\b.*\banwenden\b'
  r'|\bwas\s+bedeutet\s+das\s+für\s+(ihre|ihren|ihr)\b',
  {"K3", "K4", "K5"}, "SKV",
  "Anwenden auf eine Situation ist K3 (Aufgabentyp 7)."),

 ("Verstehensfrage: Begruendung eines Zusammenhangs",
  r'^\s*(warum|weshalb|wieso)\b|\bwie\s+kommt\s+es\b|\bwarum\s+(ist|gilt|braucht|muss)\b',
  {"K2", "K3", "K4", "K5"}, "KN",
  "«erklaeren» ist K2; verlangt die Frage eine Analyse, ist sie K4. "
  "Der Operator allein entscheidet nicht."),

 ("Einschaetzungsfrage: ja oder nein",
  # Entscheidungsfrage ohne Fragewort: «Ist das eine Gefaehrdung?»,
  # «Konnte die Person partizipieren?». Sie verlangt, einen Fall einem Begriff
  # zuzuordnen und das zu vertreten; das ist Einschaetzen.
  r'^\s*(ist|sind|war|waren|hat|haben|hatte|kann|konnte|könnte|wäre|würde|gibt|liegt|handelt)\b'
  r'(?!\s+es\s+fragen\b)',
  {"K2", "K3", "K4"}, "PAL",
  "«einschaetzen» fuehrt die Liste der Palette auf K4; ohne Kriterienbezug "
  "ist es ein Zuordnen auf K2. Nicht eindeutig, darum von Hand pruefen."),

 ("Wissens- oder Verstehensfrage",
  # Fragewort auch nach einer Praeposition: «Auf welche Texte …», «An woran …»
  # «wie» steht hier zuletzt: «wie soll», «wie wuerden», «wie kommt es» sind
  # von den Mustern darueber bereits erfasst.
  r'\b(was|welche[rsn]?|wer|wo|wann|woher|woran|womit|wofür|wozu|inwiefern|wie)\b',
  {"K1", "K2", "K3", "K4", "K5"}, "SKV",
  "«Was/Welche» verlangt Nennen oder Beschreiben, also K1 bis K2; "
  "bei hoeheren Zielen ist sie zulaessig, aber zu flach."),
]

ZU_FLACH = {  # Fragetypen, die bei hoeheren Zielen die Tiefe nicht erreichen
 "Wissens- oder Verstehensfrage": {"K1", "K2"},
}

def einstufen(frage):
    """-> Liste von (Mustername, zulaessige Stufen, Beleg, Erlaeuterung).
    Das erste Muster gewinnt; Bewertungsmuster werden immer zuerst geprueft."""
    f = " ".join(frage.split())
    fl = f.lower()
    for name, rx, stufen, beleg, erl in MUSTER:
        if re.search(rx, fl):
            return (name, stufen, beleg, erl)
    return ("nicht eingestuft", set(), "-", "Kein Muster getroffen, von Hand ansehen.")

def urteil(frage, hoechste):
    """hoechste = z. B. 'K2'. -> (urteil, name, beleg, erl)"""
    name, stufen, beleg, erl = einstufen(frage)
    if not stufen:
        return ("von Hand ansehen", name, beleg, erl)
    if "BEW" in stufen:
        andere = {x for x in stufen if x != "BEW"}
        if not andere:
            return ("ZU HOCH: Bewertung", name, beleg, erl)
        if hoechste in andere:
            return ("Grenzfall: Gewichtung", name, beleg, erl)
        return ("ZU HOCH: Bewertung", name, beleg, erl)
    if hoechste in stufen:
        flach = ZU_FLACH.get(name)
        if flach and hoechste not in flach:
            return (f"zu flach fuer {hoechste}", name, beleg, erl)
        return ("passt", name, beleg, erl)
    nmin = min(int(s[1]) for s in stufen)
    if int(hoechste[1]) < nmin:
        return (f"ZU HOCH: verlangt mindestens K{nmin}", name, beleg, erl)
    return (f"zu flach fuer {hoechste}", name, beleg, erl)
