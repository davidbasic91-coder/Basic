#!/usr/bin/env python3
"""Basic Skills: erzeugt aus dem Vault «Werkstatt Didaktik» eine einzige HTML-Seite.

Aufruf:
  python3 navigator.py <Vault-Ordner> <Ausgabe.html> [--fonts <Ordner>]

--fonts: Ordner mit texgyreadventor-regular.otf, -bold.otf, -italic.otf
(aus dem Designsystem Basix Pro). Ohne Fonts greift die Ersatzkette
Century Gothic, URW Gothic.

Nur Python-Standardbibliothek; fonttools ist optional und dient zum Verkleinern
der Schriften. Der Vault wird nur gelesen.
Nicht auf der Seite: 00 Start/Kontrolle, 00 Start/Vorlagen, 00 Start/Navigator,
00 Start/Prüfungen (E-169),
CLAUDE.md (E-071), dazu die Notiz «Quelle Plugins Didaktik» (E-072).
Start.md liefert Bereiche, Einstiege und Statusdefinitionen.
Auf der Seite fallen alle Verweise auf Claude, Skills und KI-Werkzeuge weg (E-072);
der Vault selbst bleibt unverändert und behält die Herkunftsangaben.
Die Knotentexte stehen in 00 Start/Navigator/Verbindungstexte.md.
"""
import sys, os, re, io, json, base64, datetime

AUSSCHLUSS = ('00 Start/Kontrolle/', '00 Start/Vorlagen/', '00 Start/Navigator/', '00 Start/Prüfungen/')
AUSSCHLUSS_DATEI = ('CLAUDE.md', 'Start.md', '80 Quellen/Quelle Plugins Didaktik.md')


# ---------- Frontmatter (Teilmenge von YAML, wie sie der Vault verwendet) ----------

def _unq(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1].replace("''", "'")
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return json.loads(v)
    return v


def parse_fm(text):
    if not text.startswith('---\n'):
        return {}, text
    end = text.find('\n---\n', 4)
    if end < 0:
        return {}, text
    fm, key = {}, None
    for ln in text[4:end].split('\n'):
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', ln)
        if m:
            key, v = m.group(1), m.group(2)
            fm[key] = [] if v in ('', '[]') else _unq(v)
        elif ln.startswith('- ') and key is not None and isinstance(fm.get(key), list):
            fm[key].append(_unq(ln[2:]))
        elif ln.startswith('  ') and key is not None and isinstance(fm.get(key), str):
            fm[key] += ' ' + ln.strip()
    return fm, text[end + 5:]


# ---------- Hilfen ----------

WL = re.compile(r'(!?)\[\[([^\]|#]+?)\\?(#[^\]|]*)?(\\?\|[^\]]*)?\]\]')


def links_in(text):
    out = []
    for m in WL.finditer(text):
        if m.group(1):
            continue
        out.append(m.group(2).strip().rstrip('\\'))
    return out


def abschnitte(body):
    teile, name, buf = {}, None, []
    for ln in body.split('\n'):
        m = re.match(r'^##\s+(.+?)\s*$', ln)
        if m:
            if name is not None:
                teile[name] = '\n'.join(buf).strip()
            name, buf = m.group(1), []
        else:
            buf.append(ln)
    if name is not None:
        teile[name] = '\n'.join(buf).strip()
    return teile


def ohne_kurz(body):
    """Entfernt den Abschnitt «Kurz» (er steht als Einleitung über dem Text)."""
    b = body.strip()
    m = re.match(r'^##\s+Kurz\s*\n(.*?)(?=^##\s|\Z)', b, re.S | re.M)
    return b[m.end():].strip() if m else b


# ---------- Zeitbänder aus dem Feld dauer (E-071) ----------

BAENDER = ['bis 10 Minuten', '10 bis 30 Minuten', '30 bis 60 Minuten', 'über 60 Minuten',
           'Lektionen und länger', 'nicht eindeutig', 'keine Angabe']
_GRENZEN = [(0, 10), (10, 30), (30, 60), (60, 10 ** 6)]
_WORT = {'ein': 1, 'eine': 1, 'einer': 1, 'einem': 1, 'einen': 1, 'zwei': 2, 'drei': 3,
         'vier': 4, 'fünf': 5, 'sechs': 6, 'sieben': 7, 'acht': 8, 'neun': 9, 'zehn': 10,
         'elf': 11, 'zwölf': 12, 'fünfzehn': 15, 'zwanzig': 20, 'dreissig': 30,
         'vierzig': 40, 'fünfzig': 50, 'sechzig': 60, 'neunzig': 90}


def zeitbaender(dauer):
    t = (dauer or '').lower().strip()
    if not t:
        return ['keine Angabe']
    t = re.sub(r'\bein paar\b', 'wenige', t)
    t = re.sub(r'\bhalbe stunde\b', '30 minuten', t)
    t = re.sub(r'\b(' + '|'.join(_WORT) + r')\b', lambda m: str(_WORT[m.group(1)]), t)
    zahlen = [int(x) for x in re.findall(r'\d+', t)]
    hat_min = 'min' in t
    if re.search(r'lektion|\btag|tage|tägig|woche|jahr|semester|halbtag', t) and not hat_min:
        return ['Lektionen und länger']
    if zahlen and not hat_min and 'stunde' in t:
        zahlen = [z * 60 for z in zahlen]
        hat_min = True
    if zahlen and hat_min:
        lo, hi = min(zahlen), max(zahlen)
        if lo == hi:
            return [BAENDER[i] for i, (a, b) in enumerate(_GRENZEN) if a < lo <= b]
        return [BAENDER[i] for i, (a, b) in enumerate(_GRENZEN) if hi > a and lo < b]
    if re.search(r'nicht|kein|nennt nur', t):
        return ['keine Angabe']
    return ['nicht eindeutig']


# ---------- Verweise auf Claude, Skills, KI entfernen (nur auf der Seite, E-072) ----------

_SK = re.compile(r'Skills?\b|SKILL|references/|\bClaude\b|CLAUDE|\bKI\b')


def _klammer(m):
    inner = m.group(1)
    if not _SK.search(inner):
        return m.group(0)
    if re.fullmatch(r'\s*Einschätzung laut Skill\s*', inner):
        return ''
    rest = []
    for t in re.split(r'(?<=[,;])\s*', inner):
        t2 = re.sub(r'\blaut Skills?\b\s*', '', t).strip()
        if _SK.search(t2) or not t2.strip(' ,;'):
            continue
        rest.append(t2)
    s = ' '.join(rest).strip().rstrip(',;').strip()
    return ' (' + s + ')' if s else ''


# Einzelfälle: Inhalt bleibt, Verweis fällt weg; Sätze nur über Skills fallen weg.
ERSATZ = [
    ('## Folge im Skill aviva (Davids Setzung)', '## Planungsregel (Davids Setzung)'),
    ('Der Skill rechnet mit Becker (30 Minuten) und teilt längere Inputs:', 'Gerechnet wird mit Becker (30 Minuten), längere Inputs werden geteilt:'),
    ('Der Skill lk-grundlagen lässt für Lernkontrollen je Aufgabe nur eine K-Stufe zu;', 'Für Lernkontrollen gilt je Aufgabe nur eine K-Stufe;'),
    ('## Regel der Skills (keine Auflösung)', '## Regel für Lernkontrollen (keine Auflösung)'),
    ('Beispiel des Skills:', 'Beispiel:'),
    ('| Aufgabentypen-Palette und Skill aufgabentypen |', '| Aufgabentypen-Palette |'),
    ('Die Skills lernkontrollen legen fest, dass für Lernkontrollen die Liste des Skills aufgabentypen gilt. Das ist eine Regel der Skills, keine Auflösung des Widerspruchs zwischen den Büchern.',
     'Für Lernkontrollen gilt die Liste der Aufgabentypen-Palette. Das ist eine Regel, keine Auflösung des Widerspruchs zwischen den Büchern.'),
    ('Laut Skill lk-grundlagen liegen 181 von 260 BFS-Leistungszielen FaBe auf K2', '181 von 260 BFS-Leistungszielen FaBe liegen auf K2'),
    ('Laut Skill lk-grundlagen trägt keines der 571 Leistungsziele des Bildungsplans FaBe die Stufe K6;', 'Keines der 571 Leistungsziele des Bildungsplans FaBe trägt die Stufe K6;'),
    ('Die Zählung stammt aus dem Skill und ist hier nicht nachgezählt.', 'Nicht nachgezählt.'),
    ('## Liste des Skills aufgabentypen (für Lernkontrollen verbindlich)', '## Liste der Aufgabentypen-Palette (für Lernkontrollen verbindlich)'),
    ('der Skill lk-grundlagen erlaubt für Lernkontrollen je Aufgabe nur eine Stufe', 'für Lernkontrollen gilt je Aufgabe nur eine Stufe'),
    ('## Fassung B: Skill lk-grundlagen', '## Fassung B: Regel für Lernkontrollen'),
    ('## Regel des Skills', '## Regel'),
    ('zu Merkmalen im Skill qub-raster ist Lesehilfe', 'zu Merkmalen ist Lesehilfe'),
    ('Laut Skill nennt Meyer dazu', 'Meyer nennt dazu'),
    ('Laut Skill nennt Meyer:', 'Meyer nennt:'),
    ('Laut Skill: Mehr Vielfalt', 'Mehr Vielfalt'),
    ('Der Skill qub-dossier formuliert die Trennlinie so:', 'Die Trennlinie:'),
    ('- Laut Skill deckt sich die Gliederung', '- Die Gliederung deckt sich'),
    ('- Verbesserungen, die der Skill am Musterdossier festhält:', '- Verbesserungen gegenüber dem Musterdossier:'),
    ('Vorschlag des Skills für 45 Minuten:', 'Vorschlag für 45 Minuten:'),
    ('Der Skill hält Lesart A für plausibler und empfiehlt, in eigenen Rechnungen', 'Lesart A gilt als plausibler. Empfohlen ist, in eigenen Rechnungen'),
    ('Für 90 Minuten nennt der Skill drei Ziele als Obergrenze.', 'Für 90 Minuten gelten drei Ziele als Obergrenze.'),
    ('Der Skill qub-raster hält denselben Widerspruch fest und empfiehlt, bei der Kursleitung nachzufragen.', 'Empfohlen ist, bei der Kursleitung nachzufragen.'),
    ('Davids eigenes Dokument; im Vault gilt die wortgetreue Abschrift im Skill als Primärtext.', 'Davids eigenes Dokument.'),
    ('Grundlage mehrerer lernkontrollen-Skills; im verbundenen Ordner nicht gefunden', 'Im verbundenen Ordner nicht gefunden'),
    ('Vom Skill fertigen-unterricht-planen und qub-dossier zitiert; im Vault nicht selbst ausgewertet', 'Im Vault nicht selbst ausgewertet'),
    ('Der Skill lk-raster nennt den Titel', 'Andere Titelangabe:'),
    (' Wortgetreue Abschrift in Skill lehren-kompakt, references/quellen/.', ''),
    (' Der Skill unterrichtsplanung nennt das Buch «RITA»-Grundlage.', ''),
    (' Aufbereitet im Skill unterrichtsmethoden.', ''),
    ('Aufbereitet im Skill unterrichtsmethoden. ', ''),
    ('; Grundlage der Planungskette im Skill fertigen-unterricht-planen.', '.'),
    # Knotentexte
    ('Als Richtwert nennt der Skill aviva 5 bis 10 Prozent der Zeit;', 'Als Richtwert gelten 5 bis 10 Prozent der Zeit;'),
    ('Laut Skill liegt die grosse Mehrheit der BFS-Leistungsziele FaBe auf dieser Stufe;', 'Die grosse Mehrheit der BFS-Leistungsziele FaBe liegt auf dieser Stufe;'),
    ('Laut Skill trägt keines der Leistungsziele des Bildungsplans FaBe diese Stufe;', 'Keines der Leistungsziele des Bildungsplans FaBe trägt diese Stufe;'),
    ('Laut Skill ist kooperatives Lernen überlegen', 'Kooperatives Lernen gilt als überlegen'),
    # Vault-Wörter nur auf der Seite ersetzen (E-074)
    ('Verbindung zum Tresor BFS mit obsidian://-Links auf', 'Verbindung zum Tresor BFS mit Verweisen auf'),
    ('die Notiz nennt beide Fassungen', 'der Artikel nennt beide Fassungen'),
    ('Gefiltert wird über die Felder der Notizen,', 'Gefiltert wird über die Felder der Artikel,'),
    # Ergänzungen 16.10.2026 (E-169): neuere Formulierungen im Vault
    ('Die Skills lernkontrollen legen fest, dass für Lernkontrollen die Liste des Skills aufgabentypen gilt.', 'Für Lernkontrollen gilt die Operatorenliste der Aufgabentypen.'),
    ('## Beschlossene Ergänzungen, im Skill noch nicht umgesetzt', '## Beschlossene Ergänzungen'),
    ('## Beschlossene Ergänzungen, im Skill noch offen', '## Beschlossene Ergänzungen'),
    ('Die Tabelle oben gibt den Istzustand des Skills wieder.', 'Die Tabelle oben gibt die bisherige Liste wieder.'),
    ('Die Tabelle oben gibt den Stand des Skills wieder.', 'Die Tabelle oben gibt die bisherige Liste wieder.'),
    ('## Folge im Skill aviva (Abweichung nach E-050)', '## Planungsregel (Abweichung nach E-050)'),
    ('| K1 bis K2 | Skill, references/verfahren.md Schritt 2 |', '| K1 bis K2 | Verfahren, Schritt 2 |'),
    ('| K3 | Aufgabentyp 7, Skill Schritt 2 |', '| K3 | Aufgabentyp 7, Verfahren Schritt 2 |'),
    ('| Bewertung, in FaBe gesperrt | Skill: «Häufigste Falle', '| Bewertung, in FaBe gesperrt | «Häufigste Falle'),
    ('## Zwei Unterscheidungen, die der Skill nicht nennt', '## Zwei weitere Unterscheidungen'),
    ('Der Skill praxis-ergebnissicherung bleibt zunächst unverändert; eine Erweiterung dort folgt, wenn sich das Raster im Gebrauch hält.', ''),
    ('Abweichend vom Skill gilt das nach Davids Entscheid E-112;', 'Das gilt nach Davids Entscheid E-112;'),
    (' Der Skill fertigen-unterricht-planen führt sie abweichend davon in der Makroplanung (einmal pro Klasse), also vor dem Thema; die Ebenen oben weichen in diesem Punkt vom Skill ab.', ''),
    ('Die Übersicht gibt den Index von Davids eigenem Skill unterrichtsmethoden wieder.', 'Die Übersicht gibt Davids eigenen Methodenindex wieder.'),
    ('Die Auswahlhilfe des Skills nannte', 'Die frühere Auswahlhilfe nannte'),
    ('## Regel der Skills', '## Regel für Lernkontrollen'),
    ('Der Skill lk-grundlagen verlangt für Prüfungen:', 'Für Prüfungen gilt:'),
    ('; Teile aus dem EHB-Skript 8 liegen nur über die Skills vor.', '.'),
    ('nennt erst die Auslegung des Skills qub-fachgespraech für Stufe 4.', 'stehen nicht im Wortlaut, sondern erst in einer Auslegung für Stufe 4.'),
    ('Stufenbeschreibungen sind Auslegung der qub-Skills.', 'Stufenbeschreibungen sind Auslegung.'),
    ('Von Claude nach Davids Auftrag zusammengestellt', 'Nach Davids Auftrag zusammengestellt'),
    ('Grundlage mehrerer lernkontrollen-Skills. ', ''),
    ('; der Skillumbau steht aus.', '.'),
    (', aber erst nach dem Skillumbau dort\neingetragen; bis dahin meldet die Synchronitätsprüfung sie als Abweichung.', '.'),
    ('Laut Befund B-014 (Nachtrag 29.09.2026) liegt das Skript in iCloud unter «Studienskripte Didaktik» und «EHB Zertifikat/Skripte»; am 16.10.2026 vorhanden geprüft (Datei Skript_8_Pruefen_Beurteilen_Qualitaet.md, zitiert «Pfiffner/Städeli (2018, Kap. 6)»).', 'Am 16.10.2026 vorhanden geprüft; es zitiert «Pfiffner/Städeli (2018, Kap. 6)».'),
    (' (Ordner EHB/Präsenzveranstaltungen)', ''),
    (', EHB/Selbststudium_2026-27)', ')'),
    (' (EHB/Selbststudium_2026-27)', ''),
    ('Operatorenliste des Skills aufgabentypen', 'Operatorenliste der Aufgabentypen'),
    ('Operatorenliste des Skills', 'Operatorenliste der Aufgabentypen'),
    ('die Liste des Skills.', 'die Operatorenliste der Aufgabentypen.'),
    # Etappe 3, 16.10.2026 (E-182 nach E-169): Kennzeichnungen in Ordner 70 und 50
    ('(Zuordnung laut Skill qub-dossier, Auslegung, nicht Wortlaut der Wegleitung)', '(Zuordnung als Auslegung, nicht Wortlaut der Wegleitung)'),
    ('(Zuordnung laut Skill qub-lehrprobe, Auslegung, nicht Wortlaut der Wegleitung)', '(Zuordnung als Auslegung, nicht Wortlaut der Wegleitung)'),
    ('(Zuordnung laut Skill qub-fachgespraech, Auslegung, nicht Wortlaut der Wegleitung)', '(Zuordnung als Auslegung, nicht Wortlaut der Wegleitung)'),
    ('(Angaben laut Skill qub-dossier; ', '(Angaben als Auslegung; '),
    (' Der Skill folgt Lehren und Lernen.', ''),
    ('; dass Erfahrungsnoten im FaBe-Unterricht summativ sind und darum kriterial gesetzt werden, steht laut Skill.', '; Erfahrungsnoten im FaBe-Unterricht sind summativ und werden darum kriterial gesetzt.'),
    ('; dass auch die Rundungsregel festgelegt und auf dem Prüfungsblatt ausgewiesen wird, steht laut Skill.', '; auch die Rundungsregel wird festgelegt und auf dem Prüfungsblatt ausgewiesen.'),
    ('Laut Skill dienen prognostische Lernkontrollen', 'Prognostische Lernkontrollen dienen'),
    ('Laut Skill ist er für mündliche Prüfungen', 'Er ist für mündliche Prüfungen'),
    ('Laut Skill ist es kaum möglich', 'Es ist kaum möglich'),
    ('Laut Skill vier Prüfraster', 'Vier Prüfraster'),
    ('Laut Skill zusätzlich:', 'Zusätzlich:'),
    # B-148, 22.10.2026 (E-203): Skill-Name nach «laut Auslegung des Skills»
    ('laut Auslegung des Skills qub-lehrprobe ', 'laut Auslegung '),
    ('laut Auslegung des Skills ', 'laut Auslegung '),
    # Restverweise, 16.10.2026 (E-187): Skill-Namen ohne das Wort «Skill»
    ('Die Palette beschreibt Typen, lk-grundlagen konkrete Aufgaben.', 'Die Palette beschreibt Typen, die Regel für Lernkontrollen konkrete Aufgaben.'),
    ('**EHB-Kursmaterial (laut Skill fertigen-unterricht-planen, ungeprüft):**', '**EHB-Kursmaterial (ungeprüft):**'),
]
ZEILE_WEG =re.compile(r'CLAUDE\.md des Tresors|^- Für Claude:|Skill aufgabentypen, references|Documents/Claude|\[\[Quelle Plugins Didaktik')
ABSCHNITT_WEG = ('Unstimmigkeiten im Skill',)


def entferne_verweise(t):
    if not t:
        return t
    for a, b in ERSATZ:
        t = t.replace(a, b)
    # «Laut (Auslegung) Skill qub-…» wird zu «Laut Auslegung» (Etappe 3, E-182)
    t = re.sub(r'\b([Ll])aut (?:Auslegung )?Skill (?:qub|lk)-[a-z]+ ', r'\1aut Auslegung ', t)
    zeilen, weg = [], False
    for ln in t.split('\n'):
        h = re.match(r'^##\s+(.+?)\s*$', ln)
        if h:
            weg = h.group(1) in ABSCHNITT_WEG
        if weg or ZEILE_WEG.search(ln):
            continue
        zeilen.append(ln)
    t = '\n'.join(zeilen)
    t = re.sub(r'\s*\(([^()\n]*)\)', _klammer, t)
    t = re.sub(r'Ursprung laut Skill:\s*', 'Ursprung: ', t)
    t = re.sub(r'(?<=\w)\s+laut Skills?\b(?:\s+[a-z][a-z0-9-]*-[a-z0-9-]+|\s+(?:aviva|aufgabentypen|unterrichtsmethoden))?', '', t)
    t = re.sub(r'(?<=\S)  +', ' ', t)
    t = re.sub(r' ([,.;:])', r'\1', t)
    t = re.sub(r'(?<!\.)\.\.(?!\.)', '.', t)
    for a, b in ERSATZ:
        t = t.replace(a, b)
    return t


# ---------- Keine Rückschlüsse auf Schule, Personen und Ablage (nur auf der Seite, E-075) ----------

SEITE_ERSATZ = [
    # Aussagen über die Schule (vor der allgemeinen Tresor-Regel)
    ('Die FaBe-Lernenden der BFS sind Erwachsene', 'Die FaBe-Lernenden sind Erwachsene'),
    ('181 von 260 BFS-Leistungszielen FaBe', '181 von 260 Leistungszielen FaBe im Schullehrplan'),
    ('Die grosse Mehrheit der BFS-Leistungsziele FaBe', 'Die grosse Mehrheit der Leistungsziele FaBe im Schullehrplan'),
    ('Die Notenregelung der BFS steht im Tresor BFS', 'Die Notenregelung der Schule steht im Tresor'),
    ('Notenregelung BFS FaBe', 'Notenregelung FaBe'),
    ('Folien BFS-Tagung', 'Tagungsfolien'),
    (', BFS Basel 2023', ', 2023'),
    (' Eine zweite Tagungspräsentation liegt in 3. BFS Megastarters/7_Wichtige Formulare für LP/Kompetenzorientierung/ (nicht ausgewertet).', ''),
    # Vault-Wörter (Entscheid 30.09.2026, Punkt 1)
    ('Diese Notiz behandelt', 'Dieser Artikel behandelt'),
    ('im Zweifel gilt der Text der Notiz', 'im Zweifel gilt der Text des Artikels'),
    # Name des zweiten Vaults
    ('Tresor BFS', 'Tresor'),
    # Flaig: Verweise auf die entfernten Artikel (Entscheid 30.09.2026)
    (' | [[Deskriptorenraster bauen]] | [[Raster-Bibliothek nach Flaig]] | [[Reflexionszyklus nach Gibbs]]', ''),
    ('Gedacht für mündliche Prüfungen und Feedback, nicht mit den Punkteskalen der Flaig-Raster zu vermischen.', 'Gedacht für mündliche Prüfungen und Feedback.'),
    ('Zählt die Präsentation als eigenständige Note, gilt die Flaig-Vorlage 12 ([[Raster-Bibliothek nach Flaig]]). ', ''),
    ('gedacht und nicht mit den Punkteskalen der Flaig-Raster zu vermischen;', 'gedacht;'),
    # Restverweise, 16.10.2026 (E-187): Datei- und Pfadangaben
    ('Impressum in lk1.pdf, geprüft 16.10.2026:', 'Impressum, geprüft 16.10.2026:'),
    ('`00 Start/Prüfungen/fragecheck.py` liest die Arbeitsdossiers,', 'Ein Prüfskript liest die Arbeitsdossiers,'),
    ('`raster.py` enthält die Fragetypen, `raster_proben.py` prüft das Raster an sechzehn Proben.', 'Die Fragetypen stehen in einem Raster, das ein weiteres Skript an sechzehn Proben prüft.'),
    ('Die Liste führt `00 Start/Prüfungen/slp_check.py`.', 'Die Liste führt ein Prüfskript.'),
    ('Master-Korpus, 03_taxonomie-operatoren.md, Abschnitt 6', 'Master-Korpus, Taxonomie und Operatoren, Abschnitt 6'),
    (', «260303_ppt», PDF-S. 11', ', Präsentation, PDF-S. 11'),
    ('In der Base [[Methoden.base]] nach Phase, K-Stufe, Sozialform und Eignung filtern.', 'Im Methodenfinder nach Phase, K-Stufe, Sozialform und Eignung filtern.'),
]
# Artikel, die nicht auf die Seite kommen (Entscheid 30.09.2026: beruhen auf einer nicht zu nennenden Diplomarbeit)
SEITE_OHNE = ('Raster-Bibliothek nach Flaig', 'Quelle Flaig Beurteilungsraster', 'Deskriptorenraster bauen', 'Reflexionszyklus nach Gibbs',
              # Linkziele ohne Artikel auf der Seite (E-187)
              'Vorschlaege_ausserhalb', 'Methoden.base')
SEITE_ZEILE_WEG = re.compile(r'Die Links setzen voraus, dass der Tresor in Obsidian|Index des Tresors \(greppen|\[\[Vorschlaege_ausserhalb\]\]|^\s*!\[\[[^\]]*\]\]\s*$')
SEITE_ABSCHNITT_WEG = ('Ablage',)
_OBSIDIAN_LINK = re.compile(r'\[([^\]]+)\]\(obsidian:[^)]*\)')


def seite_bereinigen(t):
    """Entfernt Hinweise auf Schule, Personen, Ablagepfade und Obsidian (nur auf der Seite)."""
    if not t:
        return t
    for a, b in SEITE_ERSATZ:
        t = t.replace(a, b)
    t = _OBSIDIAN_LINK.sub(r'\1', t)
    zeilen, weg = [], False
    for ln in t.split('\n'):
        h = re.match(r'^##\s+(.+?)\s*$', ln)
        if h:
            weg = h.group(1) in SEITE_ABSCHNITT_WEG
            if weg:
                continue
        if weg or SEITE_ZEILE_WEG.search(ln):
            continue
        zeilen.append(ln)
    return '\n'.join(zeilen)


def quelle_bereinigen(q):
    """Kürzt Ortsangaben in Quellenzeilen: «PDF in …», «in EHB/…», leere Klammern."""
    q = seite_bereinigen(q)
    q = re.sub(r',?\s*PDF in [^)]*', '', q)
    q = re.sub(r'\s+in (?:EHB|Didaktische Dokumente|Unterrichtsplanung)/[^)]*', '', q)
    q = re.sub(r'\s*\(\s*\)', '', q)
    return q


def quelle_filtern(qs):
    out = []
    for q in qs:
        if not q or re.match(r'\s*Skills?\b', q) or 'SKILL.md' in q:
            continue
        q2 = entferne_verweise(q)
        if q2.strip() and not _SK.search(q2):
            out.append(q2)
    return out


def felder_filtern(felder):
    out = {}
    for k, v in felder.items():
        if k == 'auslegung':
            continue
        if isinstance(v, list):
            v2 = [entferne_verweise(x) for x in v if not _SK.search(entferne_verweise(x))]
            if v2:
                out[k] = v2
        else:
            v2 = entferne_verweise(v)
            if v2 and not _SK.search(v2):
                out[k] = v2
    return out


# ---------- Vault lesen ----------

def lies_vault(root):
    notizen = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith('.')]
        for f in files:
            if not f.endswith('.md'):
                continue
            rel = os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/')
            notizen[rel] = open(os.path.join(d, f), encoding='utf-8').read()
    return notizen


def baue_daten(root):
    roh = lies_vault(root)
    start = roh.get('Start.md', '')
    vt = roh.get('00 Start/Navigator/Verbindungstexte.md', '')
    notes = []
    for rel in sorted(roh):
        if rel.startswith(AUSSCHLUSS) or rel in AUSSCHLUSS_DATEI:
            continue
        fm, body = parse_fm(roh[rel])
        name = os.path.basename(rel)[:-3]
        if name in SEITE_OHNE:
            continue
        teile = rel.split('/')
        bereich = teile[0] if len(teile) > 1 else ''
        felder = {k: v for k, v in fm.items()
                  if k not in ('typ', 'kurz', 'status', 'quelle', 'verwandt', 'entscheide')}
        n = {
            'name': seite_bereinigen(name), 'bereich': bereich,
            'typ': fm.get('typ', ''), 'kurz': entferne_verweise(fm.get('kurz', '')),
            'status': fm.get('status', ''), 'felder': felder_filtern(felder),
            'quelle': quelle_filtern(fm.get('quelle', []) if isinstance(fm.get('quelle'), list) else [fm.get('quelle')]),
            'verwandt': [x.strip('[]') for x in (fm.get('verwandt') or [])],
            'text': entferne_verweise(ohne_kurz(body)),
        }
        n['links'] = sorted(set(links_in(body)) | set(n['verwandt']))
        m = re.search(r'^\*\*Material:\*\*\s*(.+)$', body, re.M)
        if m:
            n['material'] = entferne_verweise(m.group(1).strip())
        if n['typ'] == 'methode':
            n['zeit'] = zeitbaender(fm.get('dauer', ''))
        # Seite: keine Rückschlüsse auf Schule, Personen und Ablage (E-075)
        n['kurz'] = seite_bereinigen(n['kurz'])
        n['text'] = seite_bereinigen(n['text'])
        n['quelle'] = [quelle_bereinigen(q) for q in n['quelle']]
        n['verwandt'] = [seite_bereinigen(x) for x in n['verwandt'] if x not in SEITE_OHNE]
        n['links'] = sorted({seite_bereinigen(x) for x in n['links'] if x not in SEITE_OHNE})
        for k in ('pfad', 'pfad_geprueft'):
            n['felder'].pop(k, None)
        n['felder'] = {k: ([seite_bereinigen(x) for x in v] if isinstance(v, list) else seite_bereinigen(v)) for k, v in n['felder'].items()}
        if 'material' in n:
            n['material'] = seite_bereinigen(n['material'])
        notes.append(n)

    st = abschnitte(parse_fm(start)[1])
    bereiche = []
    for ln in st.get('Bereiche', '').split('\n'):
        m = re.match(r'^\|\s*(\d\d [^|]+?)\s*\|\s*\[\[([^\]]+)\]\]\s*\|', ln)
        if m:
            bereiche.append({'ordner': m.group(1), 'index': m.group(2)})
    einstiege = seite_bereinigen(entferne_verweise(st.get('Häufige Einstiege', '')))
    status_def = seite_bereinigen(entferne_verweise(st.get('Status der Notizen', '')))

    knoten = abschnitte(parse_fm(vt)[1]) if vt else {}
    knoten.pop('Kurz', None)
    knoten = {k: seite_bereinigen(entferne_verweise(v)) for k, v in knoten.items()}

    return {
        'notes': notes, 'bereiche': bereiche, 'einstiege': einstiege,
        'statusDef': status_def, 'knoten': knoten, 'baender': BAENDER,
        'stand': datetime.date.today().strftime('%d.%m.%Y'),
    }


def zeichen_der_daten(x, out=None):
    """Alle Zeichen im dekodierten JSON (Schlüssel und Werte)."""
    if out is None:
        out = set()
    if isinstance(x, dict):
        for k, v in x.items():
            out.update(str(k))
            zeichen_der_daten(v, out)
    elif isinstance(x, list):
        for v in x:
            zeichen_der_daten(v, out)
    elif x is not None:
        out.update(str(x))
    return out


def font_css(ordner, zeichen=None):
    if not ordner:
        return ''
    try:
        from fontTools import subset as ft_subset
        from fontTools.ttLib import TTFont
    except ImportError:
        ft_subset = None
        print('Hinweis: fonttools fehlt, die Schriften werden ganz eingebettet.')
    unicodes = None
    if ft_subset is not None and zeichen is not None:
        unicodes = {ord(c) for c in zeichen} | set(range(0x20, 0x7F)) | set(range(0xA0, 0x180))
    css = []
    for datei, gewicht, stil in (('texgyreadventor-regular.otf', 400, 'normal'),
                                 ('texgyreadventor-bold.otf', 700, 'normal'),
                                 ('texgyreadventor-italic.otf', 400, 'italic')):
        p = os.path.join(ordner, datei)
        if os.path.exists(p):
            roh = open(p, 'rb').read()
            if unicodes is not None:
                opt = ft_subset.Options()
                opt.layout_features = ['*']
                opt.drop_tables = opt.drop_tables + ['FFTM']
                font = TTFont(io.BytesIO(roh))
                sub = ft_subset.Subsetter(opt)
                sub.populate(unicodes=unicodes)
                sub.subset(font)
                buf = io.BytesIO()
                font.save(buf)
                roh = buf.getvalue()
            b64 = base64.b64encode(roh).decode()
            css.append("@font-face{font-family:'TeX Gyre Adventor';src:url(data:font/otf;base64,%s) format('opentype');"
                       "font-weight:%d;font-style:%s;font-display:swap}" % (b64, gewicht, stil))
    return '\n'.join(css)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    root, ziel = argv[1], argv[2]
    fonts = argv[argv.index('--fonts') + 1] if '--fonts' in argv else None
    daten = baue_daten(root)
    js = json.dumps(daten, ensure_ascii=False).replace('</', '<\\/')
    zeichen = zeichen_der_daten(daten) | set(VORLAGE)
    html = VORLAGE.replace('/*FONTS*/', font_css(fonts, zeichen)).replace('/*DATEN*/', js)
    open(ziel, 'w', encoding='utf-8').write(html)
    print('Notizen:', len(daten['notes']), '| Knotentexte:', len(daten['knoten']),
          '| Grösse:', round(len(html) / 1024), 'KB ->', ziel)
    return 0


VORLAGE = r'''<meta charset="utf-8">
<title>Basic Skills</title>
<style>
/*FONTS*/
/* Basix Pro fürs Web (kleine Fassung des neuen Designs, E-188): warmer Grund, weisse Karten mit feiner Linie, Braun gliedert, Gold als Akzent. Nur ein helles Thema. */
:root{
  --dunkelbraun:#241812; --braun:#5B3A29; --mittelbraun:#976B3F; --gold:#C49A6C;
  --graubraun:#8C7B6B; --sand:#DCD0C2; --hell:#F4EEE7; --weiss:#FFFFFF;
  --gold-tint:#EFE2D1; --grund:#F8F4EE; --linie:#E4D9CC; --linie-hell:#EFE6DB;
  --text2:#3B2A20; --grip:#B9A998;
  /* Phasen und Stufen: fünf Farben von hell nach dunkel, die Schriftfarbe gehört fest dazu */
  --phase1:#E6D3BA; --phase2:#C49A6C; --phase3:#976B3F; --phase4:#5B3A29; --phase5:#241812;
  --phase1-text:#241812; --phase2-text:#241812; --phase3-text:#FFFFFF; --phase4-text:#FFFFFF; --phase5-text:#FFFFFF;
  --stufe1:var(--phase1); --stufe2:var(--phase2); --stufe3:var(--phase3); --stufe4:var(--phase4); --stufe5:var(--phase5);
  --stufe1-text:var(--phase1-text); --stufe2-text:var(--phase2-text); --stufe3-text:var(--phase3-text); --stufe4-text:var(--phase4-text); --stufe5-text:var(--phase5-text);
  /* Radien */
  --r-kuerzel:7px; --r-klein:10px; --r-feld:12px; --r-kachel:14px; --r-box:16px; --r-karte-s:18px; --r-karte:20px; --r-gross:22px; --r-pille:999px;
  /* Schatten */
  --schatten-karte:0 12px 28px -20px rgba(36,24,18,.3);
  --schatten-karte-s:0 12px 28px -22px rgba(36,24,18,.35);
  --schatten-suche:0 14px 30px -18px rgba(36,24,18,.4);
  --schatten-liste:0 18px 40px -24px rgba(36,24,18,.45);
  --schatten-segment:0 1px 3px rgba(36,24,18,.2);
  --font:'TeX Gyre Adventor','Century Gothic','URW Gothic',sans-serif;
  --a1:4px; --a2:8px; --a3:16px; --a4:24px; --a5:32px; --a6:48px;
  --rand:32px;
  color-scheme:light;
}
@media (max-width:820px){:root{--rand:16px}}
html,body{background:var(--grund);color:var(--dunkelbraun);margin:0}
body{font-family:var(--font);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;padding-inline:var(--rand);padding-block:0}
a{color:var(--braun);text-decoration-color:var(--gold);text-underline-offset:3px}
a:hover{color:var(--dunkelbraun)}
:focus-visible{outline:2px solid var(--braun);outline-offset:2px}
h1,h2,h3{text-wrap:balance;font-weight:400;margin:0}
.huelle{max-width:1180px;margin:0 auto}

/* Icons aus dem Sprite: Linie = currentColor, Fläche = --ig */
.ic{width:20px;height:20px;flex:none;--ig:var(--gold);vertical-align:middle}

/* Kopf */
.kopf,.kopf *,.kopf *::before,.kopf *::after,.start *,.start *::before,.start *::after{box-sizing:border-box}
.kopf{position:sticky;top:0;z-index:5;background:var(--weiss);border-bottom:1px solid var(--linie);margin-inline:calc(-1 * var(--rand));padding:0 var(--rand)}
.kopf .zeile{display:flex;align-items:center;gap:20px;height:68px;transition:height .18s ease}
.marke{display:flex;align-items:center;gap:11px;text-decoration:none;color:var(--dunkelbraun);flex:none;min-width:0}
.marke:hover{color:var(--dunkelbraun)}
.marke-kachel{width:38px;height:38px;border-radius:11px;background:var(--braun);box-shadow:inset 0 -3px 0 var(--gold);display:flex;align-items:center;justify-content:center;flex:none;color:var(--hell)}
.marke-kachel .ic{width:22px;height:22px;color:var(--hell);--ig:var(--gold)}
.marke-text{display:flex;flex-direction:column;justify-content:center;line-height:1.1;min-width:0}
.marke b{font-weight:400;font-size:22px;white-space:nowrap}
.marke small{color:var(--mittelbraun);font-size:11px;letter-spacing:.3px;margin-top:2px;white-space:nowrap;overflow:hidden;max-height:16px;transition:max-height .18s ease,opacity .18s ease,margin .18s ease}
.hauptnav{display:flex;gap:4px;margin-left:12px;font-size:14px}
.hauptnav a{display:flex;align-items:center;gap:8px;padding:9px 14px;border-radius:var(--r-klein);text-decoration:none;color:var(--braun);white-space:nowrap;transition:background-color .15s ease,color .15s ease}
.hauptnav a>.ic{width:18px;height:18px}
.hauptnav a:hover{background:var(--grund);color:var(--dunkelbraun)}
.hauptnav a.aktiv{background:var(--hell);color:var(--dunkelbraun)}
.suchfeld{position:relative;flex:0 1 340px;min-width:0}
.kopf .zeile>.suchfeld{margin-left:auto}
.suchfeld input{width:100%;height:42px;box-sizing:border-box;font:inherit;font-size:14px;padding:0 14px 0 40px;border:1px solid var(--linie);border-radius:var(--r-feld);background:var(--hell);color:var(--dunkelbraun);-webkit-appearance:none;appearance:none}
.suchfeld input::placeholder{color:var(--graubraun)}
.suchfeld input:hover{border-color:var(--sand)}
.suchfeld input:focus{outline:2px solid var(--braun);outline-offset:0;border-color:var(--braun);background:var(--weiss)}
.suchfeld>svg{position:absolute;left:13px;top:50%;width:18px;height:18px;transform:translateY(-50%);color:var(--braun);pointer-events:none}
.vorschlag{position:absolute;left:0;right:0;top:calc(100% + 6px);background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-kachel);box-shadow:var(--schatten-liste);list-style:none;margin:0;padding:6px;z-index:9;max-height:60vh;overflow:auto}
.vorschlag li a{display:block;padding:9px 12px;border-radius:var(--r-klein);text-decoration:none;color:var(--dunkelbraun)}
.vorschlag li a small{display:block;color:var(--braun);font-size:12px}
.vorschlag li a:hover,.vorschlag li a.aktiv{background:var(--hell)}
.ikon{display:none;width:44px;height:44px;align-items:center;justify-content:center;color:var(--braun);font:inherit;background:var(--weiss);border:1px solid var(--linie);padding:0;cursor:pointer;border-radius:var(--r-feld);flex:none}
.ikon:hover{background:var(--hell)}
.ikon svg{width:22px;height:22px}
.ikon .m-zu{display:none}
.ikon[aria-expanded="true"] .m-auf{display:none}
.ikon[aria-expanded="true"] .m-zu{display:inline}
.klappe{display:none}
.kopf.schmal .zeile{height:56px}
.kopf.schmal .marke small{max-height:0;opacity:0;margin-top:0}
@media (min-width:821px) and (max-width:1020px){
  .kopf .zeile>.hauptnav a{padding:9px 10px}
  .kopf .zeile>.hauptnav a>.ic{display:none}
}
@media (max-width:820px){
  .kopf .zeile{height:58px;gap:8px}
  .kopf.schmal .zeile{height:52px}
  .kopf .zeile>.suchfeld,.kopf .zeile>.hauptnav{display:none}
  .marke{margin-right:auto}
  .ikon{display:inline-flex}
  .klappe{border-top:1px solid var(--linie);padding:12px 0 14px}
  .klappe:not([hidden]){display:block}
  .klappe .suchfeld{flex:none}
  .klappe .suchfeld input{font-size:16px;height:46px;padding:0 14px 0 42px}
  .klappe .hauptnav{flex-direction:column;gap:2px;margin-left:0;font-size:16px}
  .klappe .hauptnav a{padding:12px 14px;border-radius:var(--r-feld)}
  .klappe .hauptnav a>.ic{width:20px;height:20px}
  .klappe .hauptnav a.aktiv{box-shadow:inset 3px 0 0 var(--gold)}
}

/* Gerüst und Seitenleiste */
.geruest{display:grid;grid-template-columns:220px minmax(0,1fr);gap:var(--a6);padding-block:var(--a5) var(--a6)}
.seitenleiste{font-size:14px;line-height:1.45;align-self:start;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-karte);padding:16px 12px;box-shadow:var(--schatten-karte-s)}
.seitenleiste details{margin:0}
.seitenleiste summary{display:none}
.seitenleiste h4{font-size:12px;letter-spacing:.7px;color:var(--braun);font-weight:700;margin:var(--a4) 0 var(--a2);text-transform:uppercase}
.seitenleiste h4:first-child{margin-top:0}
.seitenleiste ul{list-style:none;margin:0;padding:0}
.seitenleiste li{padding:1px 0}
.seitenleiste a{display:block;padding:5px 10px;border-radius:var(--r-klein);text-decoration:none;transition:background-color .15s ease}
.seitenleiste a:hover{background:var(--hell);color:var(--dunkelbraun)}
.seitenleiste .l-kopf{margin:0 0 var(--a2);padding-bottom:var(--a2);border-bottom:1px solid var(--linie-hell)}
.seitenleiste .l-kopf a{font-weight:700;color:var(--braun)}
.seitenleiste .l-finder{margin:0 0 var(--a2)}
.seitenleiste a.aktiv{color:var(--dunkelbraun);font-weight:700;background:var(--gold-tint)}
.geruest.ohne-leiste{grid-template-columns:minmax(0,1fr)}
.geruest.ohne-leiste>.seitenleiste{display:none}
main{min-width:0}
@media (max-width:860px){
  .geruest{grid-template-columns:minmax(0,1fr);gap:var(--a4);padding-block:var(--a4) var(--a5)}
  .seitenleiste{order:2;padding:14px 12px}
  .seitenleiste summary{display:block;cursor:pointer;color:var(--braun);font-weight:700;font-size:14px;padding:2px 10px}
  .seitenleiste details[open] summary{margin-bottom:var(--a2)}
}

/* Typografie */
.kicker{color:var(--braun);font-size:13px;letter-spacing:.8px;text-transform:uppercase;margin:0 0 var(--a2)}
.kicker a{color:var(--braun)}
.titel{font-size:clamp(36px,4.6vw,46px);line-height:1.08;letter-spacing:-.6px}
.titel::after{content:"";display:block;width:44px;height:5px;border-radius:3px;background:var(--gold);margin:20px 0 22px}
.lead{font-size:18px;line-height:1.55;max-width:68ch;margin:0 0 var(--a4);color:var(--text2)}
.inhalt{max-width:72ch;color:var(--text2);line-height:1.65}
.inhalt h2{font-size:22px;font-weight:700;color:var(--braun);margin:var(--a5) 0 var(--a2);line-height:1.3}
.inhalt h3{font-size:17px;font-weight:700;color:var(--dunkelbraun);margin:var(--a4) 0 var(--a2)}
.inhalt p{margin:0 0 var(--a3)}
.inhalt ul{list-style:none;padding:0;margin:0 0 var(--a3)}
.inhalt ul>li{position:relative;padding-left:22px;margin:0 0 6px}
.inhalt ul>li::before{content:"";position:absolute;left:3px;top:.68em;width:7px;height:7px;border-radius:50%;background:var(--gold)}
.inhalt ol{padding-left:0;margin:0 0 var(--a3);list-style:none;counter-reset:n}
.inhalt ol>li{counter-increment:n;position:relative;padding-left:30px;margin:0 0 6px}
.inhalt ol>li::before{content:counter(n) ".";position:absolute;left:0;color:var(--braun);font-weight:700}
.inhalt blockquote{margin:var(--a3) 0;padding:var(--a3) var(--a4);background:var(--gold-tint);border-left:4px solid var(--gold);border-radius:var(--r-kachel);color:var(--dunkelbraun);font-style:italic}
.inhalt blockquote p:last-child{margin-bottom:0}
.inhalt blockquote a{color:var(--braun)}
.inhalt code{background:var(--hell);padding:1px 6px;border-radius:6px;font-size:.92em}
.tabellenrahmen{overflow-x:auto;margin:var(--a3) 0 var(--a4);background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-kachel)}
.inhalt table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.45}
.inhalt th{background:var(--braun);color:var(--weiss);text-align:left;padding:10px 14px;font-weight:700}
.inhalt th a{color:var(--weiss)}
.inhalt td{padding:10px 14px;border-bottom:1px solid var(--linie-hell);vertical-align:top}
.inhalt tbody tr:last-child td{border-bottom:0}
.inhalt tbody tr:nth-child(even) td{background:var(--grund)}

/* Abschnittstitel: klein für Unterabschnitte, gross für die Hauptabschnitte der Hauptseite */
.balken{display:flex;align-items:center;gap:var(--a3);font-size:13px;letter-spacing:.8px;text-transform:uppercase;color:var(--braun);line-height:1.4;margin:var(--a5) 0 var(--a3)}
.balken>span{min-width:0}
.balken::after{content:"";flex:1 0 24px;height:1px;background:var(--linie)}
.abschnitt>.balken{display:block;margin:0 0 var(--a4);font-size:32px;line-height:1.15;letter-spacing:-.4px;text-transform:none;color:var(--dunkelbraun)}
.abschnitt>.balken::before{content:"";display:block;width:36px;height:4px;border-radius:2px;background:var(--gold);margin:0 0 14px}
.abschnitt>.balken::after{display:none}
.zusammenhang{max-width:72ch;font-size:16.5px;color:var(--text2);line-height:1.6}
.zusammenhang p{margin:0 0 var(--a3)}

/* Artikel mit Steckbrief */
.artikel{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:var(--a5);align-items:start}
.artikel>.kopfteil{grid-column:1/-1}
@media (max-width:1020px){.artikel{grid-template-columns:minmax(0,1fr)}.artikel>.kopfteil{order:-2}.infobox{order:-1}}
/* Steckbrief: breit rechts, schmal nach der Kurzfassung als aufklappbarer Block (standardmässig zu) */
.steckbrief-klapp{display:none}
@media (max-width:1020px){.infobox-breit{display:none}.steckbrief-klapp{display:block;margin:0 0 var(--a4)}}
.aufklapp{background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-box)}
.aufklapp>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:12px 16px;color:var(--braun);font-size:15px;border-radius:var(--r-box)}
.aufklapp>summary::-webkit-details-marker{display:none}
.aufklapp>summary::before{content:"";width:8px;height:8px;border-right:1.5px solid var(--braun);border-bottom:1.5px solid var(--braun);transform:rotate(-45deg);transition:transform .15s ease;margin:0 4px 0 2px}
.aufklapp[open]>summary::before{transform:rotate(45deg)}
.aufklapp>summary:hover{color:var(--dunkelbraun)}
.aufklapp[open]{padding-bottom:var(--a3)}
.aufklapp>.spalten{padding:0 16px}
.aufklapp .infobox{margin:0 12px;border-radius:var(--r-kachel);box-shadow:none}
.erwaehnt-klapp{margin:var(--a5) 0 var(--a3)}
.infobox{border:1px solid var(--linie);border-radius:var(--r-karte);overflow:hidden;font-size:14px;line-height:1.4;background:var(--weiss);box-shadow:var(--schatten-karte-s)}
.infobox .ib-kopf{display:flex;align-items:center;gap:8px;background:var(--braun);color:var(--weiss);padding:12px 16px;font-weight:700;letter-spacing:.2px;font-size:13.5px}
.infobox .ib-kopf .ic{width:18px;height:18px;color:var(--hell);--ig:var(--gold)}
.infobox dl{margin:0}
.infobox .zeile{display:grid;grid-template-columns:108px minmax(0,1fr);gap:8px;padding:11px 16px;border-bottom:1px solid var(--linie-hell)}
.infobox .zeile:last-child{border-bottom:0}
.infobox dt{color:var(--braun);font-weight:700;font-size:12.5px}
.infobox dd{margin:0;overflow-wrap:anywhere}
.inhalt,.lead{overflow-wrap:break-word}
.infobox .status{font-size:12.5px}
.infobox .chip{max-width:100%;white-space:normal;border-radius:16px}

/* Chips: Pillen */
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:6px;background:var(--hell);color:var(--braun);border:1px solid var(--sand);border-radius:var(--r-pille);padding:3px 12px;font-size:13px;line-height:1.5;text-decoration:none;white-space:nowrap;transition:border-color .15s ease,background-color .15s ease}
a.chip:hover{border-color:var(--braun);color:var(--dunkelbraun)}
button.chip{font:inherit;font-size:13.5px;line-height:1.4;padding:6px 14px;background:var(--weiss);cursor:pointer}
button.chip:not([aria-pressed="true"]):hover{border-color:var(--braun);color:var(--dunkelbraun)}
button.chip .anz{font-variant-numeric:tabular-nums;opacity:.8;margin-left:2px}
/* Phasen- und Stufenfarben: --ck und --ck-text je Wert, gesetzt über die Attribute */
a.chip[href="#aviva-phase-ankommen-und-einstimmen"],a.chip[href="#k1-wissen"],button.chip[data-f="aviva_phase"][data-w="Ankommen"],button.chip[data-f="k_stufe"][data-w="K1"],button.chip[data-k="K1"]{--ck:var(--phase1);--ck-text:var(--phase1-text)}
a.chip[href="#aviva-phase-vorwissen-aktivieren"],a.chip[href="#k2-verstehen"],button.chip[data-f="aviva_phase"][data-w="Vorwissen aktivieren"],button.chip[data-f="k_stufe"][data-w="K2"],button.chip[data-k="K2"]{--ck:var(--phase2);--ck-text:var(--phase2-text)}
a.chip[href="#aviva-phase-informieren"],a.chip[href="#k3-anwenden"],button.chip[data-f="aviva_phase"][data-w="Informieren"],button.chip[data-f="k_stufe"][data-w="K3"],button.chip[data-k="K3"]{--ck:var(--phase3);--ck-text:var(--phase3-text)}
a.chip[href="#aviva-phase-verarbeiten"],a.chip[href="#k4-analysieren"],button.chip[data-f="aviva_phase"][data-w="Verarbeiten"],button.chip[data-f="k_stufe"][data-w="K4"],button.chip[data-k="K4"]{--ck:var(--phase4);--ck-text:var(--phase4-text)}
a.chip[href="#aviva-phase-auswerten"],a.chip[href="#k5-synthese-oder-entwickeln"],button.chip[data-f="aviva_phase"][data-w="Auswerten"],button.chip[data-f="k_stufe"][data-w="K5"],button.chip[data-k="K5"]{--ck:var(--phase5);--ck-text:var(--phase5-text)}
a.chip[href="#aviva-phase-ankommen-und-einstimmen"]::before,a.chip[href="#aviva-phase-vorwissen-aktivieren"]::before,a.chip[href="#aviva-phase-informieren"]::before,a.chip[href="#aviva-phase-verarbeiten"]::before,a.chip[href="#aviva-phase-auswerten"]::before,
a.chip[href="#k1-wissen"]::before,a.chip[href="#k2-verstehen"]::before,a.chip[href="#k3-anwenden"]::before,a.chip[href="#k4-analysieren"]::before,a.chip[href="#k5-synthese-oder-entwickeln"]::before,
button.chip[data-f="aviva_phase"]::before,button.chip[data-f="k_stufe"][data-w^="K"]::before,button.chip[data-k]::before{content:"";flex:none;width:8px;height:8px;border-radius:50%;background:var(--ck);box-shadow:inset 0 0 0 1px rgba(36,24,18,.22)}
/* K6 ist für FaBe gesperrt: schraffiert, gestrichelter Rand */
a.chip[href="#k6-bewerten-oder-beurteilen"]{border:1.5px dashed var(--graubraun);background:repeating-linear-gradient(135deg,var(--hell) 0 6px,var(--weiss) 6px 12px);padding:2px 11px}
a.chip[href="#k6-bewerten-oder-beurteilen"]::before{content:"";flex:none;width:8px;height:8px;border-radius:50%;border:1.5px dashed var(--graubraun);background:var(--weiss)}
/* Status: belegt, Sammlung, nicht geprüft, Widerspruch */
a.chip[href="#status-belegt"]::before,a.chip[href="#status-sammlung"]::before,a.chip[href="#status-nicht-geprueft"]::before{content:"";flex:none;width:8px;height:8px;border-radius:50%}
a.chip[href="#status-belegt"]::before{background:var(--braun)}
a.chip[href="#status-sammlung"]::before{background:var(--gold)}
a.chip[href="#status-nicht-geprueft"]::before{border:1.5px solid var(--graubraun);background:transparent}
a.chip[href="#status-widerspruch"]{background:var(--gold-tint);border-color:var(--mittelbraun)}
/* Gewählte Filterchips: Phasen- und Stufenfarbe, sonst Braun */
button.chip[aria-pressed="true"]{background:var(--ck,var(--braun));border-color:var(--ck,var(--braun));color:var(--ck-text,var(--weiss))}
button.chip[aria-pressed="true"][data-w]::before,button.chip[aria-pressed="true"][data-k]::before{display:none}

/* Listen von Einträgen */
.eintraege{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.eintraege li{padding:14px 18px;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-box);transition:border-color .15s ease}
.eintraege li:hover{border-color:var(--mittelbraun)}
.eintraege .e-titel{font-size:17px;text-decoration:none;font-weight:700}
.eintraege .e-titel:hover{text-decoration:underline}
.eintraege p{margin:4px 0 6px;max-width:80ch}
.eintraege .meta{color:var(--braun);font-size:13px}
.gruppe-titel{font-size:14px;font-weight:700;color:var(--braun);margin:var(--a4) 0 var(--a2)}
.spalten{columns:2 260px;column-gap:var(--a5);font-size:15px}
.spalten a{display:block;padding:3px 0;break-inside:avoid}

/* Hauptseite */
.start{margin-top:calc(-1 * var(--a5))}
@media (max-width:860px){.start{margin-top:calc(-1 * var(--a4))}}
.oben{position:relative;z-index:2;padding:56px 0 52px;background:var(--hell);box-shadow:0 0 0 100vmax var(--hell);clip-path:inset(0 -100vmax)}
.oben>*{position:relative;z-index:1}
.oben::after{content:"";position:absolute;z-index:0;right:40px;top:50%;width:300px;height:300px;margin-top:-110px;border-radius:50%;background:var(--gold-tint);box-shadow:0 0 0 36px rgba(220,208,194,.4),0 0 0 72px rgba(220,208,194,.22);pointer-events:none}
.oben .kicker{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:var(--r-pille);background:var(--weiss);border:1px solid var(--linie);font-size:13px;letter-spacing:0;text-transform:none;color:var(--braun);margin:0 0 22px}
.oben .titel{font-size:clamp(36px,5.2vw,54px);line-height:1.06;letter-spacing:-.8px;max-width:14em}
.oben .lead{font-size:18px;max-width:520px;margin:0 0 28px}
.grosssuche{max-width:560px;flex:none}
.grosssuche input{height:62px;font-size:17px;padding:0 20px 0 56px;border:1.5px solid var(--mittelbraun);border-radius:var(--r-box);background:var(--weiss);box-shadow:var(--schatten-suche)}
.grosssuche input:hover{border-color:var(--mittelbraun)}
.grosssuche input:focus{border-color:var(--braun)}
.grosssuche>svg{left:20px;width:22px;height:22px;color:var(--braun)}
.abschnitt{padding:56px 0 8px}
.kacheln{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.kachel{background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-karte);padding:22px;box-shadow:var(--schatten-karte);transition:border-color .15s ease}
.kachel:hover{border-color:var(--mittelbraun)}
.k-haupt{display:flex;align-items:center;gap:14px;text-decoration:none;color:var(--braun)}
.k-ikon{width:46px;height:46px;border-radius:13px;background:var(--gold-tint);color:var(--braun);display:flex;align-items:center;justify-content:center;flex:none}
.k-ikon .ic{width:24px;height:24px}
.k-kopf{display:flex;flex-direction:column;min-width:0;flex:1}
.k-titel{font-size:19px;font-weight:700;line-height:1.25;color:var(--braun)}
.k-ziel{font-size:13.5px;line-height:1.45;color:var(--text2);margin-top:4px}
.k-pfeil{flex:none;box-sizing:content-box;width:16px;height:16px;padding:8px;border:1px solid var(--sand);border-radius:50%;color:var(--braun);transition:transform .15s ease,color .15s ease,border-color .15s ease}
.k-haupt:hover .k-pfeil{transform:translateX(3px);color:var(--dunkelbraun);border-color:var(--mittelbraun)}
.k-weitere{margin:14px 0 0;padding-top:12px;border-top:1px solid var(--linie-hell);font-size:12.5px;line-height:1.45;display:flex;flex-wrap:wrap;gap:6px}
.k-weitere a{color:var(--braun);background:var(--hell);border-radius:var(--r-pille);padding:2px 10px;text-decoration:none;transition:background-color .15s ease}
.k-weitere a:hover{background:var(--gold-tint);color:var(--dunkelbraun)}
/* Roter Faden */
.kette{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr))}
.kette li{position:relative}
.kette a,.kette .k-schritt{display:flex;flex-direction:column;align-items:center;text-align:center;padding:0 10px;text-decoration:none;color:var(--dunkelbraun);height:100%}
.kette li::before{content:"";position:absolute;left:0;right:0;top:29px;height:2px;background:repeating-linear-gradient(90deg,var(--gold) 0 6px,transparent 6px 12px)}
.kette li:first-child::before{left:50%}
.kette li:last-child::before{right:50%}
.s-kreis{position:relative;z-index:1;flex:none;width:60px;height:60px;border-radius:50%;background:var(--weiss);border:2px solid var(--mittelbraun);box-shadow:0 0 0 6px var(--grund);display:flex;align-items:center;justify-content:center;color:var(--braun);transition:border-color .15s ease}
.s-kreis .ic{width:28px;height:28px}
.s-nr{display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:var(--braun);color:var(--weiss);border:2px solid var(--grund);font-size:12px;font-weight:700;font-variant-numeric:tabular-nums;transition:background-color .15s ease}
.s-kreis .s-nr{position:absolute;top:-6px;right:-6px}
.s-text{font-size:15.5px;font-weight:700;line-height:1.3;margin-top:14px;padding:0 2px}
.kette a:hover .s-text{text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:3px}
.kette a:hover .s-kreis{border-color:var(--braun)}
.kette a:hover .s-nr{background:var(--dunkelbraun)}
.mehr{margin-top:var(--a4);background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-box)}
.mehr summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:12px 16px;color:var(--braun);font-size:15px;border-radius:var(--r-box)}
.mehr summary::-webkit-details-marker{display:none}
.mehr summary::before{content:"";width:8px;height:8px;border-right:1.5px solid var(--braun);border-bottom:1.5px solid var(--braun);transform:rotate(-45deg);transition:transform .15s ease;margin:0 4px 0 2px}
.mehr[open] summary::before{transform:rotate(45deg)}
.mehr summary:hover{color:var(--dunkelbraun)}
.mehr .zusammenhang{max-width:72ch;font-size:16px;padding:0 16px var(--a3)}
/* Bereiche */
.bereiche{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.bereiche li{display:flex}
.bereich{display:grid;grid-template-columns:auto minmax(0,1fr);grid-template-areas:"ikon anz" "name name" "text text";align-content:start;gap:12px 8px;width:100%;padding:20px;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-karte);box-shadow:var(--schatten-karte);text-decoration:none;color:var(--dunkelbraun);transition:border-color .15s ease}
.bereich:hover{border-color:var(--mittelbraun)}
.b-ikon{grid-area:ikon;width:34px;height:34px;border-radius:var(--r-klein);background:var(--gold-tint);color:var(--braun);display:flex;align-items:center;justify-content:center}
.b-ikon .ic{width:20px;height:20px}
.b-kopf{display:contents}
.b-name{grid-area:name;font-size:16.5px;font-weight:700;color:var(--braun);line-height:1.3}
.bereich:hover .b-name{text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:3px}
.b-anz{grid-area:anz;justify-self:end;align-self:start;font-size:12.5px;color:var(--braun);white-space:nowrap;font-variant-numeric:tabular-nums}
.b-text{grid-area:text;font-size:13.5px;line-height:1.5;color:var(--text2)}
.rasterzeile{display:flex;flex-wrap:wrap;align-items:center;gap:6px var(--a3);margin-top:var(--a4);font-size:13px}
.rasterzeile>span{color:var(--braun);letter-spacing:.7px;text-transform:uppercase;font-size:12px}
@media (max-width:1020px){
  .kacheln{grid-template-columns:repeat(2,minmax(0,1fr))}
  .bereiche{grid-template-columns:repeat(2,minmax(0,1fr))}
  .kette{grid-template-columns:repeat(3,minmax(0,1fr));row-gap:var(--a4)}
  .kette li:nth-child(3)::before{right:50%}
  .kette li:nth-child(4)::before{left:50%}
  .oben::after{display:none}
}
@media (max-width:640px){
  .oben{padding:var(--a5) 0 var(--a4)}
  .oben .titel{font-size:36px}
  .lead{font-size:16px}
  .oben .lead{font-size:16px;margin-bottom:var(--a4)}
  .grosssuche input{font-size:16px;height:56px;padding:0 16px 0 50px}
  .grosssuche>svg{left:17px}
  .abschnitt{padding:var(--a5) 0 var(--a2)}
  .abschnitt>.balken{font-size:26px}
  .kacheln{grid-template-columns:minmax(0,1fr);gap:12px}
  .kachel{padding:16px 18px}
  .k-titel{font-size:17px}
  .kette{grid-template-columns:minmax(0,1fr);row-gap:0}
  .kette li::before,.kette li:nth-child(3)::before,.kette li:nth-child(4)::before{left:29px;right:auto;top:0;bottom:0;width:2px;height:auto;background:repeating-linear-gradient(180deg,var(--gold) 0 6px,transparent 6px 12px)}
  .kette li:first-child::before{left:29px;top:38px}
  .kette li:last-child::before{left:29px;right:auto;bottom:auto;height:38px}
  .kette a,.kette .k-schritt{flex-direction:row;align-items:center;text-align:left;gap:16px;padding:8px 0}
  .s-text{font-size:16px;margin-top:0}
  .bereiche{grid-template-columns:minmax(0,1fr);gap:12px}
  .bereich{padding:16px 18px}
}

/* Methodenfinder */
.filter{display:grid;gap:var(--a3);margin-bottom:var(--a4)}
.filtergruppe{display:grid;grid-template-columns:140px minmax(0,1fr);gap:var(--a3);align-items:start}
.filtergruppe>span{font-weight:700;color:var(--braun);font-size:12px;letter-spacing:.7px;text-transform:uppercase;padding-top:9px}
@media (max-width:560px){.filtergruppe{grid-template-columns:minmax(0,1fr);gap:6px}.filtergruppe>span{padding-top:0}}
.finder-suche input{width:100%;max-width:460px;height:46px;box-sizing:border-box;font:inherit;font-size:15px;padding:0 14px;border:1px solid var(--sand);border-radius:var(--r-feld);background:var(--weiss);color:var(--dunkelbraun);-webkit-appearance:none;appearance:none}
.finder-suche input::placeholder{color:var(--graubraun)}
.finder-suche input:hover{border-color:var(--braun)}
.finder-suche input:focus{outline:2px solid var(--braun);outline-offset:0;border-color:var(--braun)}
.trichter{width:fit-content;max-width:100%;background:var(--gold-tint);border-radius:var(--r-feld);padding:8px 14px;margin:0 0 var(--a3);font-size:14px;line-height:1.45}
.trichter ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 0;align-items:center}
.trichter li{display:flex;align-items:center}
.trichter li+li::before{content:"";width:12px;height:1px;background:var(--braun);margin:0 6px}
.trichter b{font-variant-numeric:tabular-nums;color:var(--braun)}
.mf-filter{gap:14px;margin-bottom:var(--a3);padding:20px;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-karte);box-shadow:var(--schatten-karte)}
.mf-mehrbereich{display:grid;gap:14px}
.mf-mehrbereich[hidden]{display:none}
.mf-mehrknopf{font:inherit;font-size:14px;background:none;border:0;padding:6px 0;cursor:pointer;color:var(--braun);display:inline-flex;align-items:center;gap:10px}
.mf-mehrknopf::before{content:"";width:8px;height:8px;border-right:1.5px solid var(--braun);border-bottom:1.5px solid var(--braun);transform:rotate(-45deg);transition:transform .15s ease;margin:0 2px}
.mf-mehrknopf[aria-expanded="true"]::before{transform:rotate(45deg)}
.mf-mehrknopf:hover{color:var(--dunkelbraun);text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:3px}
.skripthinweis{color:var(--braun);font-size:14px;line-height:1.45;max-width:72ch;margin:0 0 var(--a3)}
.mf-hinweis{font-size:12.5px;margin:0}
.mf-leiste,.mf-fensterkopf,.mf-fensterfuss{display:none}
.mf-aktiv{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px}
button.chip.mf-weg{background:var(--weiss);border-color:var(--mittelbraun);color:var(--braun);display:inline-flex;align-items:center;gap:8px;padding:4px 6px 4px 14px}
button.chip.mf-weg:hover{background:var(--hell);color:var(--dunkelbraun)}
.mf-weg .x{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:var(--gold-tint);font-size:14px;line-height:1}
.mf-aktiv .knopf{min-height:32px;padding:0 12px;font-size:13px}
.mf-karten{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.mf-karte{background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-karte-s);box-shadow:var(--schatten-karte-s);padding:18px;display:flex;flex-direction:column;gap:6px;min-width:0;transition:border-color .15s ease}
.mf-karte:hover{border-color:var(--mittelbraun)}
.mf-name{font-size:17px;font-weight:700;line-height:1.3;text-decoration:none;color:var(--braun)}
.mf-name:hover{text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:3px}
.mf-kurz{margin:0;font-size:14px;line-height:1.5;color:var(--text2);display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;overflow:hidden}
.mf-merkmale{margin-top:auto;padding-top:12px;border-top:1px solid var(--linie-hell);color:var(--braun);font-size:12px;line-height:1.4;display:flex;flex-wrap:wrap;gap:6px}
.mf-merkmale span{background:var(--hell);border-radius:var(--r-pille);padding:2px 10px}
.mf-weiter{margin:var(--a4) 0 0;text-align:center}
@media (max-width:819.98px){
  .mf-leiste{display:flex;margin:0 0 12px}
  .mf-filter{display:none}
  .mf-filter.offen{display:grid;align-content:start;position:fixed;inset:0;z-index:30;background:var(--weiss);overflow-y:auto;overscroll-behavior:contain;padding:0 16px;margin:0;gap:14px;border:0;border-radius:0;box-shadow:none}
  .mf-filter.offen:focus{outline:0}
  .mf-fensterkopf{display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:1;background:var(--weiss);border-bottom:1px solid var(--linie);padding:14px 0 12px;font-weight:700;color:var(--braun);font-size:17px}
  .mf-zu{font:inherit;font-size:24px;line-height:1;background:none;border:0;color:var(--braun);cursor:pointer;width:44px;height:44px;border-radius:50%}
  .mf-zu:hover{background:var(--hell)}
  .mf-fensterfuss{display:block;position:sticky;bottom:0;background:var(--weiss);border-top:1px solid var(--linie);padding:12px 0 calc(12px + env(safe-area-inset-bottom,0px))}
  .mf-anzeigen{width:100%;font:inherit;font-size:16px;font-weight:700;background:var(--braun);color:var(--weiss);border:1px solid var(--braun);border-radius:var(--r-feld);min-height:48px;padding:0 16px;cursor:pointer;transition:background-color .15s ease}
  .mf-anzeigen:hover{background:var(--dunkelbraun)}
  html.mf-gesperrt,html.mf-gesperrt body{overflow:hidden}
  .mf-karten{grid-template-columns:minmax(0,1fr);gap:12px}
}

/* Knöpfe */
.knopf{font:inherit;font-size:14px;line-height:1.2;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:42px;padding:0 18px;border-radius:var(--r-feld);background:var(--weiss);color:var(--braun);border:1px solid var(--mittelbraun);cursor:pointer;text-decoration:none;transition:background-color .15s ease,border-color .15s ease,color .15s ease}
.knopf:hover{background:var(--hell);color:var(--braun)}
.knopf .ic{width:16px;height:16px}
.knopf.primaer{background:var(--braun);color:var(--weiss);border-color:var(--braun)}
.knopf.primaer:hover{background:var(--dunkelbraun);border-color:var(--dunkelbraun);color:var(--weiss)}
.knopf:disabled{opacity:.5;cursor:default}
.leer{color:var(--braun);font-style:italic}
.fuss{border-top:1px solid var(--gold);color:var(--braun);font-size:12.5px;padding:12px 0 var(--a4);display:flex;gap:6px var(--a3);flex-wrap:wrap}
.fuss span+span{border-left:1px solid var(--graubraun);padding-left:var(--a3)}
@media (max-width:640px){.fuss{flex-direction:column}.fuss span+span{border-left:0;padding-left:0;border-top:1px solid var(--linie);padding-top:6px}}
mark{background:var(--sand);color:var(--dunkelbraun);padding:0 2px;border-radius:3px}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}

/* Werkzeuge C */
/* «Lektion planen» (wl-) und «Aufgabe formulieren» (wa-); gemeinsame Bausteine tragen das Präfix wl- und gelten für beide Seiten. */
.wz-kopf{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:16px;row-gap:0;align-items:center;margin:0 0 var(--a3)}
.wz-ikon{grid-row:1 / span 2;width:60px;height:60px;border-radius:18px;background:var(--braun);color:var(--hell);display:flex;align-items:center;justify-content:center;flex:none;--ig:var(--gold);box-shadow:inset 0 -3px 0 var(--gold)}
.wz-ikon .ic{width:34px;height:34px;color:var(--hell);--ig:var(--gold)}
.wz-kopf .kicker{margin:0 0 2px}
.wz-kopf .titel{font-size:clamp(28px,3.8vw,38px);line-height:1.1;letter-spacing:-.5px}
.wz-kopf .titel::after{display:none}
.wl-seite,.wa-seite{max-width:1000px}
.wl-seite *,.wl-seite *::before,.wl-seite *::after,.wa-seite *,.wa-seite *::before,.wa-seite *::after{box-sizing:border-box}
.wl-speicher{display:flex;flex-wrap:wrap;align-items:center;gap:8px var(--a3);font-size:13.5px;color:var(--braun);margin:0 0 var(--a3);padding:8px 14px;width:fit-content;max-width:100%;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-kachel)}
.wl-speicher .knopf{min-height:34px;padding:0 12px;font-size:13px}
.wl-frage{display:inline-flex;flex-wrap:wrap;align-items:center;gap:8px}
.wl-frage[hidden],.wl-speicher [hidden]{display:none}
.wl-feld{display:flex;flex-direction:column;gap:6px;min-width:0}
.wl-feld>label,.wl-etikett{font-weight:700;color:var(--braun);font-size:13.5px;line-height:1.35}
.wl-feld>label small,.wl-etikett small{font-weight:400;color:var(--braun);font-size:12.5px;margin-left:6px}
.wl-seite input[type=number],.wl-seite input[type=search],.wl-seite select,.wl-seite textarea,
.wa-seite input[type=number],.wa-seite input[type=search],.wa-seite select,.wa-seite textarea{width:100%;min-width:0;font:inherit;font-size:15px;line-height:1.4;padding:9px 12px;border:1px solid var(--sand);border-radius:var(--r-feld);background:var(--weiss);color:var(--dunkelbraun);margin:0}
.wl-seite input[type=number],.wl-seite input[type=search],.wl-seite select,
.wa-seite input[type=number],.wa-seite input[type=search],.wa-seite select{height:44px}
.wl-seite input[type=number],.wl-seite input[type=search],.wa-seite input[type=number],.wa-seite input[type=search]{-webkit-appearance:none;appearance:none}
.wl-seite textarea,.wa-seite textarea{resize:vertical;min-height:92px}
.wl-seite input::placeholder,.wa-seite input::placeholder,.wl-seite textarea::placeholder,.wa-seite textarea::placeholder{color:var(--graubraun)}
.wl-seite input:hover,.wl-seite select:hover,.wl-seite textarea:hover,.wa-seite input:hover,.wa-seite select:hover,.wa-seite textarea:hover{border-color:var(--braun)}
.wl-seite input:focus,.wl-seite select:focus,.wl-seite textarea:focus,.wa-seite input:focus,.wa-seite select:focus,.wa-seite textarea:focus{outline:2px solid var(--braun);outline-offset:0;border-color:var(--braun)}
.wl-hinweis{font-size:12.5px;line-height:1.45;color:var(--braun);margin:0}
.wl-hinweis a{color:var(--braun)}
.wl-ungeprueft{display:inline-block;font-size:12px;line-height:1.4;color:var(--braun);border:1px solid var(--sand);border-radius:var(--r-pille);padding:0 8px;margin-left:4px;white-space:nowrap}
.wl-rahmen{display:grid;grid-template-columns:minmax(0,1.8fr) minmax(0,.7fr) minmax(0,1.1fr);gap:var(--a3) var(--a4);align-items:start;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-gross);padding:22px 24px;box-shadow:var(--schatten-karte-s)}
.wl-rahmen .chips button.chip{padding:6px 12px}
.wl-schalter{display:flex;align-items:center;gap:12px;font-size:15px;cursor:pointer;color:var(--dunkelbraun)}
.wl-schalter input{-webkit-appearance:none;appearance:none;position:relative;flex:none;width:44px;height:26px;margin:0;border-radius:13px;background:var(--sand);cursor:pointer;transition:background-color .15s ease}
.wl-schalter input::before{content:"";position:absolute;left:3px;top:3px;width:20px;height:20px;border-radius:50%;background:var(--weiss);box-shadow:0 1px 3px rgba(36,24,18,.3);transition:transform .15s ease}
.wl-schalter input:checked{background:var(--braun)}
.wl-schalter input:checked::before{transform:translateX(18px)}
.wl-bilanz{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:var(--a3) 0 0;padding:0}
.wl-bilanz>div{padding:10px 14px;border-radius:var(--r-kachel);background:var(--hell);min-width:0}
.wl-bilanz>div:last-child{background:var(--braun);color:var(--weiss)}
.wl-bilanz dt{font-size:11.5px;letter-spacing:.5px;text-transform:uppercase;color:var(--braun)}
.wl-bilanz dd{margin:2px 0 0;font-size:22px;font-weight:400;color:var(--dunkelbraun);font-variant-numeric:tabular-nums;line-height:1.2}
.wl-bilanz dd small{display:block;font-weight:400;font-size:12px;color:var(--braun);line-height:1.35}
.wl-bilanz>div:last-child dt,.wl-bilanz>div:last-child dd small{color:var(--phase1)}
.wl-bilanz>div:last-child dd{color:var(--weiss)}
/* Tabellen der Werkzeuge: Kopf Braun, aussen gerundet, Zeilen 10/14, gestreift */
.wl-tab,.wk-tabelle{border-collapse:separate;border-spacing:0;width:100%;font-size:14px;line-height:1.4;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-kachel);overflow:hidden}
.wl-tab th{background:var(--braun);color:var(--weiss);text-align:left;padding:10px 14px;font-weight:700;vertical-align:bottom}
.wl-tab td{padding:10px 14px;border-bottom:1px solid var(--linie-hell);vertical-align:top;overflow-wrap:break-word}
.wl-tab tbody tr:last-child td{border-bottom:0}
.wl-tab tbody tr:nth-child(even) td{background:var(--grund)}
.wl-tab .wl-zahl{font-variant-numeric:tabular-nums;white-space:nowrap}
.wl-geruest{margin:0 0 var(--a2)}
.wl-summe{font-size:15px;color:var(--braun);margin:0 0 8px;font-variant-numeric:tabular-nums}
.wl-summe b{color:var(--dunkelbraun)}
.wl-phasen{list-style:none;margin:var(--a3) 0 0;padding:0}
.wl-karte{position:relative;overflow:hidden;border:1px solid var(--linie);border-radius:var(--r-karte);background:var(--weiss);box-shadow:var(--schatten-karte-s);padding:22px 20px 20px;transition:border-color .15s ease}
.wl-karte::before{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:var(--ph,var(--sand))}
.wl-karte[data-phase="Ankommen"]{--ph:var(--phase1)}
.wl-karte[data-phase="Vorwissen aktivieren"]{--ph:var(--phase2)}
.wl-karte[data-phase="Informieren"]{--ph:var(--phase3)}
.wl-karte[data-phase="Verarbeiten"]{--ph:var(--phase4)}
.wl-karte[data-phase="Auswerten"]{--ph:var(--phase5)}
.wl-karte:focus-within{border-color:var(--mittelbraun)}
.wl-phase-kopf{display:flex;align-items:center;justify-content:space-between;gap:var(--a2);margin:0 0 16px}
.wl-phase-name{display:flex;align-items:center;gap:12px;font-weight:700;font-size:18px;color:var(--braun);min-width:0;line-height:1.3}
.wl-nr{flex:none;width:30px;height:30px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:var(--braun);color:var(--weiss);font-size:14px;font-weight:400;font-variant-numeric:tabular-nums}
.wl-entfernen{font:inherit;font-size:13.5px;background:none;border:0;color:var(--braun);cursor:pointer;padding:4px 0;text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:3px;flex:none}
.wl-entfernen:hover{color:var(--dunkelbraun)}
.wl-reihe{display:grid;gap:12px var(--a3);align-items:start}
.wl-reihe1{grid-template-columns:110px minmax(0,1.6fr) minmax(0,1fr)}
.wl-reihe2{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:12px}
.wl-methlink{font-size:13.5px;margin:0}
.wl-methlink:empty,.wl-sichhinweis:empty{display:none}
.wl-plus{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:12px 0 16px}
.wl-plus>.knopf[data-akt="plus"]{border:1.5px dashed var(--mittelbraun);background:transparent}
.wl-plus>.knopf[data-akt="plus"]:hover{background:var(--gold-tint)}
.wl-wahl{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.wl-wahl[hidden]{display:none}
.wl-warn{margin:0 0 var(--a3);background:var(--gold-tint);border-radius:var(--r-box);padding:14px 18px;font-size:14.5px;line-height:1.5}
.wl-warn[hidden]{display:none}
.wl-warn-titel{font-weight:700;color:var(--braun);margin:0 0 6px}
.wl-warn ul{margin:0;padding:0;list-style:none;display:grid;gap:8px}
.wl-warn li{position:relative;padding-left:18px}
.wl-warn li::before{content:"";position:absolute;left:2px;top:.62em;width:7px;height:7px;border-radius:50%;background:var(--mittelbraun)}
.wl-warn p.wl-hinweis{margin-top:8px;color:var(--braun)}
.wl-ergebnis,.wa-ergebnis{background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-karte);padding:20px 22px;box-shadow:var(--schatten-karte-s)}
.wl-erg-titel{font-size:22px;font-weight:700;color:var(--braun);margin:0 0 12px;line-height:1.25}
.wl-kopfdaten{display:flex;flex-wrap:wrap;gap:4px var(--a4);margin:0 0 var(--a3);font-size:14.5px}
.wl-kopfdaten>div{display:flex;gap:6px}
.wl-kopfdaten dt{font-weight:700;color:var(--braun)}
.wl-kopfdaten dt::after{content:":"}
.wl-kopfdaten dd{margin:0;font-variant-numeric:tabular-nums}
.wl-plan{font-size:13.5px}
.wl-plan .wl-reserve td{font-style:italic;color:var(--braun)}
.wl-leerzeile td{color:var(--braun);font-style:italic}
.wl-knoepfe{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:var(--a3) 0 0}
.wl-meldung{font-size:13.5px;color:var(--braun);margin:8px 0 0;min-height:1.45em}
.wl-nachlesen{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px var(--a4);font-size:15px}
/* Aufgabe formulieren */
.wa-stufen{margin:0 0 8px}
.wa-block{display:grid;gap:var(--a3);margin-top:var(--a3)}
.wa-typen{border:0;padding:0;margin:0;min-width:0}
.wa-typen legend{font-weight:700;color:var(--braun);font-size:13.5px;padding:0;margin:0 0 8px}
.wa-typliste{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.wa-typliste>li{display:flex;align-items:stretch;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-kachel);min-width:0;transition:border-color .15s ease}
.wa-typliste>li:hover{border-color:var(--mittelbraun)}
.wa-typliste>li:has(input:checked){border-color:var(--braun);background:var(--gold-tint);box-shadow:0 0 0 1px var(--braun)}
.wa-typ{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;flex:1;min-width:0;cursor:pointer}
.wa-typ input{accent-color:var(--braun);margin:3px 0 0;flex:none;width:16px;height:16px}
.wa-typ-text{display:flex;flex-direction:column;min-width:0;font-size:14.5px;line-height:1.35}
.wa-typ-text small{color:var(--braun);font-size:12.5px;margin-top:2px}
.wa-typlink{flex:none;align-self:center;font-size:13px;padding:9px 14px 9px 0;white-space:nowrap}
.wa-raster{display:grid;grid-template-columns:140px 180px minmax(0,260px);gap:var(--a3);margin:0 0 var(--a3)}
.wa-texte{display:grid;gap:var(--a3);margin:0 0 var(--a3)}
.wa-auftrag{width:100%}
.wa-auftrag th{width:170px}
.wa-auftrag tbody th{background:none;color:var(--braun);border-bottom:1px solid var(--linie-hell);vertical-align:top;font-size:14px}
.wa-auftrag tbody tr:last-child th{border-bottom:0}
.wa-auftrag td{white-space:pre-wrap}
.wa-auftrag tbody tr:nth-child(even) td{background:none}
@media (max-width:820px){
  .finder-suche input,.wzd-feld input,.wzd-feld select,.wzd-feld textarea,
  .wl-seite input[type=number],.wl-seite input[type=search],.wl-seite select,.wl-seite textarea,
  .wa-seite input[type=number],.wa-seite input[type=search],.wa-seite select,.wa-seite textarea{font-size:16px}
}
@media (max-width:860px){
  .wl-rahmen{grid-template-columns:minmax(0,1fr);padding:18px}
  .wl-reihe1{grid-template-columns:110px minmax(0,1fr)}
  .wl-reihe1 .wl-feld-methode{grid-column:1/-1;order:3}
  .wl-reihe2{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:560px){
  .wl-bilanz{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  .wl-bilanz dd{font-size:20px}
  .wl-karte{padding:20px 14px 16px}
  .wl-ergebnis,.wa-ergebnis{padding:16px 14px}
  .wa-raster{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .wa-raster>.wl-feld:last-child{grid-column:1/-1}
  .wa-typliste{grid-template-columns:minmax(0,1fr)}
  .wa-auftrag th{width:120px}
}
/* Verlaufsplan auf dem Handy: jede Zeile als Block, Spaltenname davor (nur Bildschirm) */
@media screen and (max-width:700px){
  .wl-plan{border:0;border-radius:0;overflow:visible;background:none}
  .wl-plan thead{display:none}
  .wl-plan,.wl-plan tbody,.wl-plan tr,.wl-plan td{display:block;width:100%}
  .wl-plan tr{background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-kachel);overflow:hidden;margin:0 0 10px}
  .wl-plan td{display:grid;grid-template-columns:118px minmax(0,1fr);gap:8px;padding:6px 12px;border-bottom:0}
  .wl-plan td::before{content:attr(data-label);font-weight:700;color:var(--braun);font-size:12.5px;font-style:normal}
  .wl-plan tbody tr:nth-child(even) td{background:none}
  .wl-plan tbody tr td:first-child{background:var(--hell)}
  .wl-plan .wl-leerzeile td::before{content:none}
}
/* Druck: nur das Ergebnis */
@media print{
  html,body{background:var(--weiss)}
  body:has(.wl-seite),body:has(.wa-seite){padding:0}
  body:has(.wl-seite) .kopf,body:has(.wa-seite) .kopf,body:has(.wl-seite) .fuss,body:has(.wa-seite) .fuss,
  body:has(.wl-seite) .seitenleiste,body:has(.wa-seite) .seitenleiste{display:none!important}
  body:has(.wl-seite) .geruest,body:has(.wa-seite) .geruest{display:block;padding:0}
  .wl-seite>*:not(.wl-ergebnis),.wa-seite>*:not(.wa-ergebnis){display:none!important}
  .wl-ergebnis,.wa-ergebnis{border:0;border-radius:0;box-shadow:none;background:none;padding:0}
  .wl-tab{border-collapse:collapse;border:0;border-radius:0;overflow:visible;background:none;font-size:9.5pt}
  .wl-tab th,.wl-tab td{padding:8px}
  .wl-tab td{border-bottom:1px solid var(--sand)}
  .wl-tab th{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .wl-tab tr{break-inside:avoid}
  .wa-auftrag tbody th{color:var(--braun)}
}

/* Werkzeuge D */
.wzd-seite{max-width:880px}
.wzd-seite,.wzd-seite *,.wzd-seite *::before,.wzd-seite *::after{box-sizing:border-box}
.wzd-entwurf{display:flex;flex-wrap:wrap;align-items:center;gap:8px var(--a3);font-size:13.5px;color:var(--braun);margin:0 0 var(--a2)}
.wzd-entwurf p{margin:0}
.wzd-feld{display:flex;flex-direction:column;gap:6px;min-width:0}
.wzd-feld>span,.wzd-feld>label{font-weight:700;color:var(--braun);font-size:13.5px}
.wzd-feld input,.wzd-feld select,.wzd-feld textarea{font:inherit;font-size:15px;width:100%;max-width:100%;padding:9px 12px;border:1px solid var(--sand);border-radius:var(--r-feld);background:var(--weiss);color:var(--dunkelbraun)}
.wzd-feld input,.wzd-feld select{height:44px}
.wzd-feld input[type="text"],.wzd-feld textarea{-webkit-appearance:none;appearance:none}
.wzd-feld input:hover,.wzd-feld select:hover,.wzd-feld textarea:hover{border-color:var(--braun)}
.wzd-feld input:focus,.wzd-feld select:focus,.wzd-feld textarea:focus{outline:2px solid var(--braun);outline-offset:0;border-color:var(--braun)}
.wzd-feld textarea{resize:vertical;line-height:1.5}
.wzd-unter{font-size:15px;font-weight:700;color:var(--braun);margin:var(--a4) 0 var(--a2)}
.wzd-hinweis{font-size:12.5px;line-height:1.45;color:var(--braun);margin:6px 0 var(--a2)}
.wzd-ergebnis{background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-karte);box-shadow:var(--schatten-karte-s);padding:var(--a3) var(--a4);overflow-wrap:break-word}
.wzd-e-titel{font-size:22px;font-weight:700;color:var(--braun);margin:0 0 var(--a2)}
.wzd-e-kopf{margin:0 0 var(--a2);font-size:14px}
.wzd-ergebnis h3{font-size:16px;font-weight:700;color:var(--braun);margin:var(--a3) 0 4px}
.wzd-ergebnis h4{font-size:15px;font-weight:700;margin:var(--a2) 0 2px}
.wzd-ergebnis p{margin:0 0 var(--a2)}
.wzd-text{white-space:pre-wrap;overflow-wrap:anywhere}
.wzd-aktionen{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:var(--a3) 0 0}
.wzd-aktionen .knopf:disabled{opacity:.5;cursor:default}
.wzd-meldung{font-size:13.5px;color:var(--braun)}
.wzd-nachlesen{list-style:none;margin:0;padding:0}
.wzd-nachlesen li{padding:4px 0}
.wk-eingaben{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1.6fr);gap:var(--a3)}
@media (max-width:640px){.wk-eingaben{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.wk-eingaben>:last-child{grid-column:1/-1}}
.wk-einzel{display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr);gap:var(--a3);align-items:end}
.wk-einzelnote{margin:0;font-size:20px;line-height:1.3;padding-bottom:8px;color:var(--dunkelbraun)}
.wk-formel{font-size:14px;margin:0 0 var(--a2)}
.wk-skala{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:var(--a3);align-items:start;margin-top:var(--a3)}
.wk-tabelle{line-height:1.35;font-variant-numeric:tabular-nums}
.wk-tabelle th{background:var(--braun);color:var(--weiss);text-align:right;padding:8px 14px;font-weight:700}
.wk-tabelle td{text-align:right;padding:5px 14px;border-bottom:1px solid var(--linie-hell)}
.wk-tabelle tbody tr:last-child td{border-bottom:0}
.wk-tabelle tbody tr:nth-child(even) td{background:var(--grund)}
.wk-liste{list-style:none;margin:0;padding:4px 16px;background:var(--weiss);border:1px solid var(--linie);border-radius:var(--r-box)}
.wk-liste li{border-bottom:1px solid var(--linie-hell)}
.wk-liste li:last-child{border-bottom:0}
.wk-liste label{display:flex;gap:12px;align-items:flex-start;padding:10px 0;cursor:pointer;line-height:1.45;min-width:0}
.wk-liste input{flex:none;width:18px;height:18px;margin:2px 0 0;accent-color:var(--braun);cursor:pointer}
.wk-liste span{min-width:0;overflow-wrap:break-word}
.wk-liste input:checked+span{color:var(--graubraun)}
.wk-nr{color:var(--braun);font-weight:700}
.wr-kopf{display:grid;grid-template-columns:minmax(0,200px) minmax(0,1fr);gap:var(--a3);margin:var(--a3) 0 0}
.wr-schritt{margin:0 0 var(--a4)}
.wr-schritt-kopf{display:flex;align-items:center;gap:12px;margin:0 0 8px}
.wr-nr{width:30px;height:30px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;background:var(--braun);color:var(--weiss);font-size:14px;font-weight:400}
.wr-schritt-kopf label{font-weight:700;font-size:17px;color:var(--braun)}
.wr-fragen{margin:0 0 8px;font-size:14.5px;line-height:1.5;max-width:72ch;color:var(--text2)}
.wr-merkmal{margin:0 0 10px}
.wr-m-text{display:flex;flex-direction:column;min-width:0}
.wr-m-name{font-weight:700;color:var(--braun)}
.wr-m-funktion{font-size:13px;line-height:1.4;color:var(--braun)}
.wr-m-innen{padding:0 16px 0 38px}
.wr-ind-kopf{font-size:12.5px;letter-spacing:.3px;color:var(--braun);margin:0 0 4px}
.wr-ind{font-size:14.5px;line-height:1.5}
.wr-ind p{margin:0 0 8px}
.wr-leer{font-style:italic;color:var(--braun)}
@media (max-width:560px){
  .wzd-ergebnis{padding:var(--a3)}
  .wk-einzel,.wr-kopf{grid-template-columns:minmax(0,1fr)}
  .wr-m-innen{padding-left:16px}
}
@media print{
  body:has(.wzd-seite){padding:0}
  body:has(.wzd-seite) .kopf,body:has(.wzd-seite) .fuss,body:has(.wzd-seite) .seitenleiste{display:none!important}
  body:has(.wzd-seite) .geruest{display:block;padding:0}
  .wzd-seite{max-width:none}
  .wzd-seite>:not(.wzd-druck){display:none!important}
  .wzd-druck>.balken,.wzd-druck .wzd-aktionen{display:none!important}
  .wzd-ergebnis{border:0;border-radius:0;box-shadow:none;background:none;padding:0}
  .wk-skala{grid-template-columns:repeat(4,minmax(0,1fr))}
  .wk-tabelle{break-inside:avoid;border-collapse:collapse;border:0;border-radius:0;overflow:visible;background:none}
  .wk-tabelle th{padding:5px 8px}
  .wk-tabelle td{padding:3px 8px;border-bottom:1px solid var(--sand)}
  .wk-tabelle th,.wk-tabelle tbody tr:nth-child(even) td{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>

<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><symbol id="i-search" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="10.5" cy="10.5" r="5.6" style="fill:var(--ig,#C49A6C);stroke:none;opacity:.45"></circle><circle cx="10.5" cy="10.5" r="6.5"></circle><path d="M15.5 15.5 21 21"></path></symbol><symbol id="i-home" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M10 19v-5h4v5z" style="fill:var(--ig,#C49A6C);stroke:none"></path><path d="M4 11 12 4l8 7M6 9.5V19h12V9.5"></path></symbol><symbol id="i-plan" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M4 7.5A2.5 2.5 0 0 1 6.5 5h11A2.5 2.5 0 0 1 20 7.5V10H4z" style="fill:var(--ig,#C49A6C);stroke:none"></path><rect x="4" y="5" width="16" height="15" rx="2.5"></rect><path d="M8 3v4M16 3v4M8 14h3M8 17h6"></path></symbol><symbol id="i-cards" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="3" y="7.5" width="13" height="13" rx="2.5" style="fill:var(--ig,#C49A6C);stroke:none"></rect><rect x="8" y="3.5" width="13" height="13" rx="2.5" style="fill:#fff;fill-opacity:.0"></rect><path d="M11.5 8.5h6M11.5 12h4"></path></symbol><symbol id="i-task" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M4 20l1.2-4.2 3 3z" style="fill:var(--ig,#C49A6C);stroke:none"></path><path d="M4 20l1.2-4.2L16.6 4.4a2 2 0 0 1 2.8 0l.2.2a2 2 0 0 1 0 2.8L8.2 18.8zM14.5 6.5l3 3"></path></symbol><symbol id="i-exam" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="9" y="2.5" width="6" height="3.5" rx="1.2" style="fill:var(--ig,#C49A6C);stroke:none"></rect><rect x="5" y="4.5" width="14" height="16.5" rx="2.5"></rect><path d="M9 13.5l2.2 2.2L15.5 11.5"></path></symbol><symbol id="i-loop" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="12" r="3" style="fill:var(--ig,#C49A6C);stroke:none"></circle><path d="M20 12a8 8 0 1 1-2.6-5.9M20 4v4h-4"></path></symbol><symbol id="i-users" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="9" cy="8" r="3.2" style="fill:var(--ig,#C49A6C);stroke:none"></circle><circle cx="9" cy="8" r="3.2"></circle><path d="M3.5 20a5.5 5.5 0 0 1 11 0M16 5.3a3.2 3.2 0 0 1 0 5.4M17.5 14.5A5.5 5.5 0 0 1 20.5 20"></path></symbol><symbol id="i-compass" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M15.5 8.5 13.5 13.5 8.5 15.5 10.5 10.5z" style="fill:var(--ig,#C49A6C);stroke:none"></path><circle cx="12" cy="12" r="9"></circle></symbol><symbol id="i-star" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.9 6.8 19.7l1-5.9L3.5 9.7l5.9-.8z" style="fill:var(--ig,#C49A6C);fill-opacity:.55"></path></symbol><symbol id="i-book" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="9" y="7" width="6" height="3" rx="1" style="fill:var(--ig,#C49A6C);stroke:none"></rect><path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5zM5 19.5A1.5 1.5 0 0 0 6.5 21H19v-3"></path></symbol><symbol id="i-award" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="9" r="3.6" style="fill:var(--ig,#C49A6C);stroke:none"></circle><circle cx="12" cy="9" r="6"></circle><path d="M8.5 14l-1.5 7 5-2.5 5 2.5-1.5-7"></path></symbol><symbol id="i-check" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M5 12.5l4.5 4.5L19 7.5"></path></symbol><symbol id="i-checks" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><g style="fill:var(--ig,#C49A6C);stroke:none;opacity:.55"><circle cx="6" cy="6.3" r="3.2"></circle><circle cx="6" cy="12" r="3.2"></circle><circle cx="6" cy="17.7" r="3.2"></circle></g><path d="M4.3 6.3l1.2 1.2L7.8 5M4.3 12l1.2 1.2L7.8 10.7M4.3 17.7l1.2 1.2 2.3-2.5M12 6.5h8M12 12h8M12 17.5h8"></path></symbol><symbol id="i-bookmark" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M7 4h10a1 1 0 0 1 1 1v15l-6-4-6 4V5a1 1 0 0 1 1-1z" style="fill:var(--ig,#C49A6C);fill-opacity:.5"></path></symbol><symbol id="i-clock" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="12" r="7.6" style="fill:var(--ig,#C49A6C);stroke:none;opacity:.35"></circle><circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path></symbol><symbol id="i-filter" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="15" cy="7" r="2.4" style="fill:var(--ig,#C49A6C);stroke:none"></circle><circle cx="9" cy="17" r="2.4" style="fill:var(--ig,#C49A6C);stroke:none"></circle><path d="M4 7h8.5M17.5 7H20M4 17h2.5M11.5 17H20"></path></symbol><symbol id="i-grid" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="4" y="4" width="6.5" height="6.5" rx="1.6" style="fill:var(--ig,#C49A6C);fill-opacity:.6"></rect><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.6"></rect><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.6"></rect><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.6"></rect></symbol><symbol id="i-list" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><g style="fill:var(--ig,#C49A6C);stroke:none"><circle cx="5" cy="6" r="1.6"></circle><circle cx="5" cy="12" r="1.6"></circle><circle cx="5" cy="18" r="1.6"></circle></g><path d="M9.5 6H20M9.5 12H20M9.5 18H20"></path></symbol><symbol id="i-chev" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M9 6l6 6-6 6"></path></symbol><symbol id="i-down" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M6 9l6 6 6-6"></path></symbol><symbol id="i-arrow" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M4 12h15M13 6l6 6-6 6"></path></symbol><symbol id="i-up-right" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M7 17 17 7M8.5 7H17v8.5"></path></symbol><symbol id="i-plus" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M12 5v14M5 12h14"></path></symbol><symbol id="i-x" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M6 6l12 12M18 6 6 18"></path></symbol><symbol id="i-grip" viewBox="0 0 24 24" style="fill:currentColor;stroke:none"><circle cx="9" cy="6" r="1.5"></circle><circle cx="15" cy="6" r="1.5"></circle><circle cx="9" cy="12" r="1.5"></circle><circle cx="15" cy="12" r="1.5"></circle><circle cx="9" cy="18" r="1.5"></circle><circle cx="15" cy="18" r="1.5"></circle></symbol><symbol id="i-cmd" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="9" y="9" width="6" height="6" style="fill:var(--ig,#C49A6C);stroke:none;opacity:.6"></rect><path d="M9 9V6.5A2.5 2.5 0 1 0 6.5 9H9zM15 9V6.5A2.5 2.5 0 1 1 17.5 9H15zM9 15v2.5A2.5 2.5 0 1 1 6.5 15H9zM15 15v2.5a2.5 2.5 0 1 0 2.5-2.5H15zM9 9h6v6H9z"></path></symbol><symbol id="i-moon" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z" style="fill:var(--ig,#C49A6C);fill-opacity:.55"></path></symbol><symbol id="i-sun" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="12" r="4" style="fill:var(--ig,#C49A6C);fill-opacity:.7"></circle><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"></path></symbol><symbol id="i-link" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"></path></symbol><symbol id="i-net" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><g style="fill:var(--ig,#C49A6C);stroke:none"><circle cx="6" cy="7" r="2.6"></circle><circle cx="18" cy="7" r="2.6"></circle><circle cx="12" cy="18" r="2.6"></circle></g><path d="M8.6 7h6.8M7.3 9.3l3.4 6.4M16.7 9.3l-3.4 6.4"></path></symbol><symbol id="i-layers" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M12 3 3 8l9 5 9-5z" style="fill:var(--ig,#C49A6C);fill-opacity:.6"></path><path d="M3 12.5l9 5 9-5M3 16.5l9 5 9-5"></path></symbol><symbol id="i-stairs" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M3 20h5v-5h5v-5h5V5h3v15z" style="fill:var(--ig,#C49A6C);fill-opacity:.5"></path><path d="M3 20h5v-5h5v-5h5V5h3"></path></symbol><symbol id="i-info" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="12" r="7.6" style="fill:var(--ig,#C49A6C);stroke:none;opacity:.4"></circle><circle cx="12" cy="12" r="9"></circle><path d="M12 11v5M12 8h.01"></path></symbol><symbol id="i-copy" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="9" y="9" width="11" height="11" rx="2.2" style="fill:var(--ig,#C49A6C);fill-opacity:.5"></rect><path d="M15 9V6.2A2.2 2.2 0 0 0 12.8 4H6.2A2.2 2.2 0 0 0 4 6.2v6.6A2.2 2.2 0 0 0 6.2 15H9"></path></symbol><symbol id="i-download" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="5" y="18" width="14" height="2.6" rx="1.3" style="fill:var(--ig,#C49A6C);stroke:none"></rect><path d="M12 4v10.5M7.5 10 12 14.5l4.5-4.5"></path></symbol><symbol id="i-history" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="12" r="2.2" style="fill:var(--ig,#C49A6C);stroke:none"></circle><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4.3h4.3M12 8v4l2.6 1.6"></path></symbol><symbol id="i-target" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="12" r="2.6" style="fill:var(--ig,#C49A6C);stroke:none"></circle><circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="5"></circle></symbol><symbol id="i-menu" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M4 7h16M4 12h16M4 17h16"></path></symbol><symbol id="i-trash" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M7 7l1 13h8l1-13z" style="fill:var(--ig,#C49A6C);fill-opacity:.4"></path><path d="M4.5 7h15M10 7V4.5h4V7"></path></symbol><symbol id="i-warn" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M12 4 3 19.5h18z" style="fill:var(--ig,#C49A6C);fill-opacity:.45"></path><path d="M12 10v4M12 17h.01"></path></symbol><symbol id="i-lock" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="5" y="11" width="14" height="9" rx="2.2" style="fill:var(--ig,#C49A6C);fill-opacity:.5"></rect><path d="M8 11V8a4 4 0 0 1 8 0v3"></path></symbol><symbol id="i-person" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="8" r="3.6" style="fill:var(--ig,#C49A6C);stroke:none"></circle><circle cx="12" cy="8" r="3.6"></circle><path d="M5 20a7 7 0 0 1 14 0"></path></symbol><symbol id="i-toc" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><rect x="4" y="4" width="2.6" height="16" rx="1.3" style="fill:var(--ig,#C49A6C);stroke:none"></rect><path d="M10.5 6.5H20M10.5 12H17M10.5 17.5H20"></path></symbol><symbol id="i-bulb" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M12 3.5a6 6 0 0 0-3.4 10.9c.6.5.9 1.1.9 1.8v.8h5v-.8c0-.7.3-1.3.9-1.8A6 6 0 0 0 12 3.5z" style="fill:var(--ig,#C49A6C);fill-opacity:.5"></path><path d="M9.5 20h5M10.5 22h3"></path></symbol><symbol id="i-flag" viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"><path d="M5 4v17M5 5h12l-2.5 4L17 13H5z" style="fill:none"></path><path d="M5 5h12l-2.5 4L17 13H5z" style="fill:var(--ig,#C49A6C);fill-opacity:.55;stroke:none"></path></symbol></svg>
<header class="kopf" id="kopf">
  <div class="huelle">
    <div class="zeile">
      <a class="marke" href="#h"><span class="marke-kachel"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-layers"/></svg></span><span class="marke-text"><b>Basic Skills</b><small>Werkstatt Didaktik</small></span></a>
      <nav class="hauptnav" aria-label="Hauptnavigation"><a href="#h" data-nav="h"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-home"/></svg>Hauptseite</a><a href="#finder" data-nav="finder"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-cards"/></svg>Methodenfinder</a><a href="#ueber" data-nav="ueber"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-info"/></svg>Über dieses Wiki</a></nav>
      <div class="suchfeld" role="search"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-search"/></svg><input id="suche" type="search" placeholder="Suchen: Methode, Modell, Begriff" autocomplete="off" aria-label="Im Wiki suchen" aria-controls="vorschlag"><ul id="vorschlag" class="vorschlag" hidden></ul></div>
      <button class="ikon" id="k-suche" type="button" aria-expanded="false" aria-controls="klappe-suche" aria-label="Suche öffnen"><svg class="ic m-auf" aria-hidden="true" focusable="false"><use href="#i-search"/></svg><svg class="ic m-zu" aria-hidden="true" focusable="false"><use href="#i-x"/></svg></button>
      <button class="ikon" id="k-menue" type="button" aria-expanded="false" aria-controls="klappe-menue" aria-label="Menü öffnen"><svg class="ic m-auf" aria-hidden="true" focusable="false"><use href="#i-menu"/></svg><svg class="ic m-zu" aria-hidden="true" focusable="false"><use href="#i-x"/></svg></button>
    </div>
    <div class="klappe" id="klappe-suche" hidden><div class="suchfeld" role="search"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-search"/></svg><input id="suche-mobil" type="search" placeholder="Suchen: Methode, Modell, Begriff" autocomplete="off" aria-label="Im Wiki suchen" aria-controls="vorschlag-mobil"><ul id="vorschlag-mobil" class="vorschlag" hidden></ul></div></div>
    <div class="klappe" id="klappe-menue" hidden><nav class="hauptnav" aria-label="Hauptnavigation"><a href="#h" data-nav="h"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-home"/></svg>Hauptseite</a><a href="#finder" data-nav="finder"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-cards"/></svg>Methodenfinder</a><a href="#ueber" data-nav="ueber"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-info"/></svg>Über dieses Wiki</a></nav></div>
  </div>
</header>

<div class="huelle geruest" id="geruest">
  <aside class="seitenleiste" aria-label="Bereich"><details id="leiste" open><summary id="leiste-titel">Bereiche und Schnellwahl</summary><div id="leiste-inhalt"></div></details></aside>
  <main id="seite" tabindex="-1"></main>
</div>
<div class="huelle"><footer class="fuss" id="fuss"></footer></div>

<script id="daten" type="application/json">/*DATEN*/</script>
<script>
(function(){
'use strict';
var D=JSON.parse(document.getElementById('daten').textContent);
var N=D.notes;
/* Feste Adressen aus dem Namen */
function slug(s){s=String(s==null?'':s).toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');}
var RESERVIERT={h:1,finder:1,ueber:1,suche:1,'werkzeug-lektion':1,'werkzeug-aufgabe':1,'werkzeug-lernkontrolle':1,'werkzeug-reflexion':1};
var nachId=Object.create(null);
N.forEach(function(n){var b=slug(n.name),id=b,k=2;while(nachId[id])id=b+'-'+(k++);n.id=id;nachId[id]=n;});
var nachName={},nachKlein={};
N.forEach(function(n){nachName[n.name]=n;nachKlein[n.name.toLowerCase()]=n;});
function finde(name){name=(name||'').trim().replace(/\\$/,'');return nachName[name]||nachKlein[name.toLowerCase()]||null;}

var TYP={konzept:'Konzept',verfahren:'Verfahren',methode:'Methode',aufgabentyp:'Aufgabentyp','k-stufe':'K-Stufe',kriterium:'Kriterium',vorgabe:'Vorgabe',quelle:'Quelle',index:'Übersicht'};
var FELD={nr:'Nummer',gruppe:'Gruppe',aviva_phase:'AVIVA-Phase',k_stufe:'K-Stufe',sozialform:'Sozialform',dauer:'Zeitbedarf',eignung_fabe:'Eignung FaBe',herkunft:'Herkunft',operatoren:'Operatoren',musterloesung:'Musterlösung',stufe:'Stufe',bezeichnung:'Bezeichnung',raster:'Raster',nummer:'Nummer',punkte_max:'Punkte max.',bezugssituation:'Bezugssituation',gilt_fuer:'Gilt für',autor:'Autor',titel:'Titel',jahr:'Jahr',art:'Art',pfad:'Pfad',pfad_geprueft:'Pfad geprüft',auslegung:'Auslegung'};
var KAT=['aviva_phase','k_stufe','sozialform','zeit','eignung_fabe','raster','typ','gruppe','status'];
var KATNAME={aviva_phase:'AVIVA-Phase',k_stufe:'K-Stufe',sozialform:'Sozialform',zeit:'Zeitband',eignung_fabe:'Eignung FaBe',raster:'Raster',typ:'Art',gruppe:'Gruppe',status:'Status'};
var PHASEN=['Ankommen','Vorwissen aktivieren','Informieren','Verarbeiten','Auswerten'];
var EIGNUNG=['sehr hoch','hoch','mittel bis hoch','mittel','gering bis mittel','gering'];
var SOZ=['Einzelarbeit','Partnerarbeit','Gruppenarbeit','Plenum'];
var STATUS=['belegt','sammlung','nicht geprüft','widerspruch'];

function werte(n,f){
  if(f==='zeit')return n.zeit||[];
  if(f==='typ')return n.typ?[n.typ]:[];
  if(f==='status')return n.status?[n.status]:[];
  var v=n.felder[f];if(v===undefined||v==='')return [];return Array.isArray(v)?v:[v];
}
/* Knotenseiten: Feldwert -> Notiz */
function phaseNotiz(w){return finde(w==='Ankommen'?'AVIVA Phase Ankommen und einstimmen':'AVIVA Phase '+w);}
var kNotiz={};N.forEach(function(n){if(n.typ==='k-stufe')kNotiz[n.felder.stufe]=n;});
function hubFuer(n){
  if(/^AVIVA Phase /.test(n.name)){for(var i=0;i<PHASEN.length;i++)if(phaseNotiz(PHASEN[i])===n)return {f:'aviva_phase',w:PHASEN[i]};}
  if(n.typ==='k-stufe')return {f:'k_stufe',w:n.felder.stufe};
  return null;
}
/* Kategorie-IDs: Feldname plus Wert. Kollidiert eine Adresse mit einem Artikel, gehört sie dem Artikel;
   die Sammelseite für diesen Wert gibt es nicht (Davids Entscheid, betrifft vier AVIVA-Phasen).
   Kollisionen mit reservierten Adressen oder zwischen Sammelseiten kommen derzeit nicht vor. */
var KATFELD={aviva_phase:'aviva-phase',k_stufe:'k-stufe',sozialform:'sozialform',zeit:'zeitbedarf',eignung_fabe:'eignung-fabe',raster:'raster',typ:'notiztyp',gruppe:'gruppe',status:'status'};
var katWerte={},katId={},katAus=Object.create(null);
KAT.forEach(function(f){var s={};N.forEach(function(n){werte(n,f).forEach(function(w){s[w]=(s[w]||0)+1;});});katWerte[f]=s;
  Object.keys(s).sort().forEach(function(w){var id=slug(KATFELD[f]+'-'+w);if(nachId[id]||RESERVIERT[id]||katAus[id])return;katId[f+'|'+w]=id;katAus[id]={f:f,w:w};});});
function katLink(f,w,label){
  if(f==='aviva_phase'){var p=phaseNotiz(w);if(p)return '<a class="chip" href="#'+p.id+'">'+esc(label||w)+'</a>';}
  if(f==='k_stufe'&&kNotiz[w])return '<a class="chip" href="#'+kNotiz[w].id+'">'+esc(label||w)+'</a>';
  var id=katId[f+'|'+w];if(!id)return '<span class="chip">'+esc(label||w)+'</span>';
  return '<a class="chip" href="#'+id+'">'+esc(label||(f==='typ'?(TYP[w]||w):w))+'</a>';
}
/* Rückverweise */
var rueck={};N.forEach(function(n){n.links.forEach(function(l){var z=finde(l);if(z&&z!==n){(rueck[z.id]=rueck[z.id]||[]);if(rueck[z.id].indexOf(n)<0)rueck[z.id].push(n);}});});
var bereichIndex={};D.bereiche.forEach(function(b){var x=finde(b.index);if(x)bereichIndex[b.ordner]=x;});
function bereichName(o){return (o||'').replace(/^\d\d\s+/,'');}

function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function anzeige(name){return String(name==null?'':name).replace(/^Index /,'');}

/* ---------- Markdown (nur was der Vault braucht) ---------- */
function inline(s){
  var ph=[];function hold(h){ph.push(h);return '\u0000'+(ph.length-1)+'\u0000';}
  s=s.replace(/`([^`]+)`/g,function(_,c){return hold('<code>'+esc(c)+'</code>');});
  s=s.replace(/(!?)\[\[([^\]|#]+?)\\?(#[^\]|]*)?(?:\\?\|([^\]]*))?\]\]/g,function(_,em,ziel,anker,alias){
    ziel=ziel.trim();
    if(em)return hold('');
    var z=finde(ziel),label=alias?alias.trim():(z?anzeige(ziel):ziel);
    if(z)return hold('<a href="#'+z.id+'">'+esc(label)+'</a>');
    return hold(esc(label));});
  s=s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,function(_,t,u){
    if(/^https?:/i.test(u))return hold('<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(t)+'</a>');
    if(/^obsidian:/i.test(u))return hold(esc(t));
    return hold(esc(t));});
  s=esc(s);
  s=s.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g,'$1<em>$2</em>');
  return s.replace(/\u0000(\d+)\u0000/g,function(_,i){return ph[+i];});
}
function zellen(z){z=z.replace(/\\\|/g,'\u0001').trim().replace(/^\|/,'').replace(/\|$/,'');return z.split('|').map(function(c){return c.replace(/\u0001/g,'\\|').trim();});}
/* Ablauf «1) … 2) … 3) …» auf einer Zeile: getrennt wird nur bei der nächsten erwarteten Nummer am Satzanfang
   (nach Zeilenanfang oder Leerzeichen) und nicht innerhalb einer offenen runden Klammer (Davids Entscheid).
   Stehen auf der Zeile weitere solche «Zahl)» ausserhalb der Folge, bleibt die Zeile ungetrennt. */
function marken(s){
  var out=[],tiefe=0,i=0,x,c;
  while(i<s.length){
    c=s.charAt(i);
    if(tiefe===0&&(i===0||/\s/.test(s.charAt(i-1)))&&(x=/^(\d+)\)/.exec(s.slice(i)))){out.push({nr:+x[1],a:i,e:i+x[0].length});i+=x[0].length;continue;}
    if(c==='(')tiefe++;else if(c===')'&&tiefe>0)tiefe--;
    i++;
  }
  return out;
}
function ablaufTeile(s,nr){
  var mk=marken(s),teile=[],pos=0;if(!mk.length)return [s];
  for(var j=0;j<mk.length;j++)if(mk[j].nr!==nr+1+j)return null;
  mk.forEach(function(k){teile.push(s.slice(pos,k.a).trim());pos=k.e;});
  teile.push(s.slice(pos).trim());
  return teile;
}
function schritte(zeile){
  var m=zeile.match(/^\s*(\d+)([.)])\s+([\s\S]*)$/);if(!m)return [zeile];
  if(m[2]!==')')return [m[3]];
  return ablaufTeile(m[3],+m[1])||[m[3]];
}
/* Text vor «1)» auf derselben Zeile: eigener Absatz, danach die Liste; nur wenn «2)» in aufsteigender Folge kommt (Davids Entscheid). */
function vortextAblauf(zeile){
  var mk=marken(zeile);if(mk.length<2||mk[0].nr!==1||mk[0].a===0)return null;
  var vor=zeile.slice(0,mk[0].a).trim();if(!vor)return null;
  var teile=ablaufTeile(zeile.slice(mk[0].e),1);if(!teile||teile.length<2)return null;
  return {vor:vor,teile:teile};
}
function md(src){
  var L=String(src||'').replace(/\r/g,'').split('\n').filter(function(l){return !/^\s*!\[\[[^\]]*\]\]\s*$/.test(l);}),out=[],i=0;
  while(i<L.length){
    var l=L[i];
    if(!l.trim()){i++;continue;}
    var h=l.match(/^(#{1,6})\s+(.*)$/);
    if(h){var lv=Math.min(3,Math.max(2,h[1].length));out.push('<h'+lv+'>'+inline(h[2])+'</h'+lv+'>');i++;continue;}
    if(/^\s*\|/.test(l)){var rows=[];while(i<L.length&&/^\s*\|/.test(L[i])){rows.push(L[i]);i++;}
      var t='<div class="tabellenrahmen"><table>';var start=0;
      if(rows.length>1&&/^\s*\|?\s*:?-{2,}/.test(rows[1])){t+='<thead><tr>'+zellen(rows[0]).map(function(c){return '<th>'+inline(c)+'</th>';}).join('')+'</tr></thead>';start=2;}
      t+='<tbody>'+rows.slice(start).map(function(r){return '<tr>'+zellen(r).map(function(c){return '<td>'+inline(c)+'</td>';}).join('')+'</tr>';}).join('')+'</tbody></table></div>';
      out.push(t);continue;}
    if(/^>\s?/.test(l)){var q=[];while(i<L.length&&/^>\s?/.test(L[i])){q.push(L[i].replace(/^>\s?/,''));i++;}out.push('<blockquote>'+md(q.join('\n'))+'</blockquote>');continue;}
    if(/^\s*[-*]\s+/.test(l)){var it=[];while(i<L.length&&(/^\s*[-*]\s+/.test(L[i])||(/^\s{2,}\S/.test(L[i])&&it.length))){if(/^\s*[-*]\s+/.test(L[i]))it.push(L[i].replace(/^\s*[-*]\s+/,''));else it[it.length-1]+=' '+L[i].trim();i++;}
      out.push('<ul>'+it.map(function(x){return '<li>'+inline(x)+'</li>';}).join('')+'</ul>');continue;}
    if(/^\s*\d+[.)]\s+/.test(l)){var it2=[];while(i<L.length&&/^\s*\d+[.)]\s+/.test(L[i])){it2=it2.concat(schritte(L[i]));i++;}
      out.push('<ol>'+it2.map(function(x){return '<li>'+inline(x)+'</li>';}).join('')+'</ol>');continue;}
    if(/^-{3,}\s*$/.test(l)){i++;continue;}
    var va=vortextAblauf(l.trim());
    if(va){out.push('<p>'+inline(va.vor)+'</p>');out.push('<ol>'+va.teile.map(function(x){return '<li>'+inline(x)+'</li>';}).join('')+'</ol>');i++;continue;}
    var p=[];while(i<L.length&&L[i].trim()&&!/^(#{1,6}\s|\s*\||>|\s*[-*]\s+|\s*\d+[.)]\s+)/.test(L[i])&&!(p.length&&vortextAblauf(L[i].trim()))){p.push(L[i].trim());i++;}
    if(!p.length){p.push(l.trim());i++;}
    out.push('<p>'+inline(p.join(' '))+'</p>');
  }
  return out.join('\n');
}

/* ---------- Bausteine ---------- */
function balken(t){return '<div class="balken"><span>'+esc(t)+'</span></div>';}
function eintrag(n,mitMeta){
  var meta=[];
  if(n.typ==='methode'){
    if(n.felder.aviva_phase&&n.felder.aviva_phase.length)meta.push(n.felder.aviva_phase.join(', '));
    if(n.felder.k_stufe&&n.felder.k_stufe.length)meta.push(n.felder.k_stufe.join(', '));
    if(n.felder.sozialform&&n.felder.sozialform.length)meta.push(n.felder.sozialform.join(', '));
    if(n.zeit)meta.push(n.zeit.join(', '));
  } else meta.push(TYP[n.typ]||n.typ);
  return '<li><a class="e-titel" href="#'+n.id+'">'+esc(anzeige(n.name))+'</a><p>'+esc(n.kurz)+'</p>'+(mitMeta!==false?'<div class="meta">'+esc(meta.join(' | '))+'</div>':'')+'</li>';
}
function gruppiert(liste){
  var g={};liste.forEach(function(n){(g[n.typ]=g[n.typ]||[]).push(n);});
  var ord=['konzept','verfahren','aufgabentyp','methode','kriterium','vorgabe','k-stufe','index','quelle'];
  return ord.filter(function(t){return g[t];}).map(function(t){
    var arr=g[t].sort(function(a,b){return anzeige(a.name).localeCompare(anzeige(b.name),'de');});
    return '<h3 class="gruppe-titel">'+esc(TYP[t]||t)+' ('+arr.length+')</h3>'+(arr.length>24?'<div class="spalten">'+arr.map(function(n){return '<a href="#'+n.id+'">'+esc(anzeige(n.name))+'</a>';}).join('')+'</div>':'<ul class="eintraege">'+arr.map(function(n){return eintrag(n);}).join('')+'</ul>');
  }).join('');
}
function zusammenhang(key){var t=D.knoten[key];return t?balken('Zusammenhänge')+'<div class="zusammenhang">'+md(t)+'</div>':'';}

function infobox(n,klapp){
  var z=[];
  function zeile(l,h){z.push('<div class="zeile"><dt>'+esc(l)+'</dt><dd>'+h+'</dd></div>');}
  var reihen=['aviva_phase','k_stufe','sozialform','dauer','eignung_fabe','gruppe','nr','raster','nummer','punkte_max','stufe','bezeichnung','operatoren','musterloesung','bezugssituation','gilt_fuer','autor','titel','jahr','art','pfad','pfad_geprueft','herkunft'];
  reihen.forEach(function(f){
    var v=n.felder[f];if(v===undefined||v===''||(Array.isArray(v)&&!v.length))return;
    var arr=Array.isArray(v)?v:[v];
    if(KAT.indexOf(f)>=0)zeile(FELD[f]||f,'<div class="chips">'+arr.map(function(w){return katLink(f,w);}).join('')+'</div>');
    else if(f==='dauer'){zeile('Zeitbedarf',esc(v)+(n.zeit?'<div class="chips" style="margin-top:6px">'+n.zeit.map(function(w){return katLink('zeit',w);}).join('')+'</div>':''));}
    else zeile(FELD[f]||f,esc(arr.join(', ')));
  });
  if(n.material)zeile('Material',inline(n.material));
  zeile('Art',katLink('typ',n.typ,TYP[n.typ]||n.typ));
  if(n.bereich)zeile('Bereich',bereichIndex[n.bereich]?'<a href="#'+bereichIndex[n.bereich].id+'">'+esc(anzeige(bereichName(n.bereich)))+'</a>':esc(anzeige(bereichName(n.bereich))));
  if(n.status)zeile('Status','<span class="status">'+katLink('status',n.status)+'</span>');
  var innen='<div class="ib-kopf">'+ikon(TYP_IKON[n.typ]||'info')+esc(TYP[n.typ]||'Artikel')+'</div><dl>'+z.join('')+'</dl>';
  /* Schmal (unter 1020 px): derselbe Steckbrief nach der Kurzfassung, aufklappbar, standardmässig zu. */
  if(klapp)return '<details class="aufklapp steckbrief-klapp"><summary>Steckbrief</summary><div class="infobox">'+innen+'</div></details>';
  return '<aside class="infobox infobox-breit" aria-label="Steckbrief">'+innen+'</aside>';
}

/* ---------- Seiten ---------- */
var S=document.getElementById('seite');
function setze(html,titel){S.innerHTML=html;document.title=(titel?titel+' | ':'')+'Basic Skills';window.scrollTo(0,0);}

function seiteNotiz(n){
  var hub=hubFuer(n),teile=[];
  teile.push('<div class="kopfteil"><p class="kicker">'+(n.bereich?(bereichIndex[n.bereich]?'<a href="#'+bereichIndex[n.bereich].id+'">'+esc(anzeige(bereichName(n.bereich)))+'</a>':esc(anzeige(bereichName(n.bereich)))):'Werkstatt')+'</p><h1 class="titel">'+esc(anzeige(n.name))+'</h1></div>');
  var haupt='<div class="haupt"><p class="lead">'+inline(n.kurz)+'</p>'+infobox(n,true)+zusammenhang(n.name)+'<div class="inhalt">'+md(n.text)+'</div>';
  if(hub){var liste=N.filter(function(x){return x!==n&&werte(x,hub.f).indexOf(hub.w)>=0;});
    var meth=liste.filter(function(x){return x.typ==='methode';}),andere=liste.filter(function(x){return x.typ!=='methode';});
    if(meth.length){
      haupt+=balken('Methoden für die '+(hub.f==='aviva_phase'?'Phase ':'Stufe ')+hub.w+' ('+meth.length+')')+
        '<p><a class="knopf primaer" href="#finder" data-preset="'+esc(hub.f)+'|'+esc(hub.w)+'">Im Methodenfinder filtern</a></p>';
      if(andere.length)haupt+=balken('Weitere Artikel zur '+(hub.f==='aviva_phase'?'Phase ':'Stufe ')+hub.w+' ('+andere.length+')')+gruppiert(andere);
    } else if(liste.length)haupt+=balken('Weitere Artikel zur '+(hub.f==='aviva_phase'?'Phase ':'Stufe ')+hub.w+' ('+liste.length+')')+gruppiert(liste);
  }
  var r=(rueck[n.id]||[]).slice().sort(function(a,b){return anzeige(a.name).localeCompare(anzeige(b.name),'de');});
  var rListe='<div class="spalten">'+r.map(function(x){return '<a href="#'+x.id+'">'+esc(anzeige(x.name))+'</a>';}).join('')+'</div>';
  if(r.length>12)haupt+='<details class="aufklapp erwaehnt-klapp"><summary>Erwähnt in ('+r.length+')</summary>'+rListe+'</details>';
  else if(r.length)haupt+=balken('Erwähnt in ('+r.length+')')+rListe;
  if(n.quelle&&n.quelle.filter(Boolean).length)haupt+=balken('Einzelnachweise')+'<div class="inhalt"><ol>'+n.quelle.filter(Boolean).map(function(q){return '<li>'+inline(q)+'</li>';}).join('')+'</ol></div>';
  haupt+='</div>';
  setze('<article class="artikel">'+teile.join('')+haupt+infobox(n)+'</article>',anzeige(n.name));
}

function seiteKat(id){
  var k=katAus[id];if(!k)return seiteHaupt();
  var liste=N.filter(function(x){return werte(x,k.f).indexOf(k.w)>=0;});
  var titel=k.f==='typ'?(TYP[k.w]||k.w):k.w;
  var key=k.f==='sozialform'?'Sozialform '+k.w:null;
  var h='<p class="kicker">'+esc(KATNAME[k.f])+'</p><h1 class="titel">'+esc(titel)+'</h1>';
  if(key)h+=zusammenhang(key);
  if(k.f==='zeit')h+='<p class="lead">Methoden, deren Zeitangabe in dieses Band fällt. Das Band liest ein Skript aus dem Feld «Zeitbedarf»; die Originalangabe steht in jedem Artikel.</p>';
  /* Felder, nach denen der Methodenfinder filtert: Methoden nur als Zahl mit Knopf, andere Arten als Liste darunter. */
  var finderFeld=k.f==='sozialform'||k.f==='zeit'||k.f==='eignung_fabe'||k.f==='status'||k.f==='aviva_phase'||k.f==='k_stufe';
  var meth=liste.filter(function(x){return x.typ==='methode';}),andere=liste.filter(function(x){return x.typ!=='methode';});
  if((finderFeld||(k.f==='typ'&&k.w==='methode'))&&meth.length){
    h+=balken(meth.length+' Methoden')+'<p><a class="knopf primaer" href="#finder" data-preset="'+(k.f==='typ'?'':esc(k.f)+'|'+esc(k.w))+'">Im Methodenfinder filtern</a></p>';
    if(andere.length)h+=balken(andere.length+' weitere Artikel')+gruppiert(andere);
  } else h+=balken(liste.length+' Einträge')+gruppiert(liste);
  setze(h,titel);
}

/* ---------- Hauptseite (Etappe 1) ---------- */
/* Symbole aus dem eingebetteten Sprite */
function ikon(n){return '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-'+n+'"/></svg>';}
var LUPE=ikon('search');
var PFEIL='<svg class="ic k-pfeil" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>';
/* Zuordnung der Symbole */
var KACHEL_IKON={'Lektion planen':'plan','Methode suchen':'cards','Aufgabe formulieren':'task','Lernkontrolle bauen':'exam','Lektion reflektieren':'loop','EHB':'award'};
var KETTE_IKON=['target','layers','cards','task','checks','loop'];
var BEREICH_IKON={'10':'users','20':'compass','30':'cards','40':'task','50':'checks','60':'loop','70':'award','80':'book'};
var TYP_IKON={methode:'cards',konzept:'bulb',verfahren:'list',aufgabentyp:'task','k-stufe':'stairs',kriterium:'checks',vorgabe:'flag',quelle:'book',index:'grid'};
var KETTE=[['Ziel und K-Stufe','Operatoren und K-Stufen'],['Lernweg in fünf Phasen','AVIVA-Modell'],['Methode, Sozialform, Medien','Verlaufsplanung'],['Aufgaben','Aufgabentypen Übersicht'],['Auswerten und prüfen','AVIVA Phase Auswerten'],['Reflektieren','Guter Unterricht nach Meyer']];
/* Einstiege der Startseite: «- Beschriftung: [[Ziel]], [[Weitere]]» */
function einstiege(){
  return String(D.einstiege||'').split('\n').map(function(l){
    var m=l.match(/^\s*[-*]\s+([^:]+):\s*(.*)$/);if(!m)return null;
    var ziele=[],re=/\[\[([^\]|#]+?)\\?(?:#[^\]|]*)?(?:\\?\|([^\]]*))?\]\]/g,x;
    while((x=re.exec(m[2])))ziele.push(finde(x[1].trim()));
    return {text:m[1].trim(),ziele:ziele.filter(Boolean)};
  }).filter(Boolean);
}
function seiteHaupt(){
  var h='<div class="start"><section class="oben"><p class="kicker">Werkstatt Didaktik</p><h1 class="titel">Wie Unterricht entsteht</h1>'+
    '<p class="lead">Das Nachschlagewerk zu Planung, Methoden, Aufgaben, Prüfen und Unterrichtsqualität: '+N.length+' Artikel, verknüpft wie ein Wiki.</p>'+
    '<div class="suchfeld grosssuche" role="search">'+LUPE+'<input id="suche-gross" type="search" placeholder="Suchen: Methode, Modell, Begriff" autocomplete="off" aria-label="Im Wiki suchen" aria-controls="vorschlag-gross"><ul id="vorschlag-gross" class="vorschlag" hidden></ul></div></section>';
  h+='<section class="abschnitt">'+balken('Häufige Einstiege')+'<ul class="kacheln">'+einstiege().map(function(e){
    var z=e.ziele[0],rest=e.ziele.slice(1);
    if(e.text==='Methode suchen'){z={id:'finder',name:'Methodenfinder'};rest=[];} /* nur auf der Seite (E-075) */
    var WZ={'Lektion planen':'werkzeug-lektion','Aufgabe formulieren':'werkzeug-aufgabe','Lernkontrolle bauen':'werkzeug-lernkontrolle','Lektion reflektieren':'werkzeug-reflexion'};
    if(WZ[e.text]){rest=e.ziele.slice();z={id:WZ[e.text],name:'Werkzeug'};} /* Kachel öffnet das Werkzeug, Artikel klein darunter (E-076) */
    var kopf='<span class="k-ikon">'+ikon(KACHEL_IKON[e.text]||'book')+'</span><span class="k-kopf"><span class="k-titel">'+esc(e.text)+'</span>'+(z?'<span class="k-ziel">'+esc(anzeige(z.name))+'</span>':'')+'</span>';
    return '<li class="kachel">'+(z?'<a class="k-haupt" href="#'+z.id+'">'+kopf+PFEIL+'</a>':'<div class="k-haupt">'+kopf+'</div>')+
      (rest.length?'<p class="k-weitere">'+rest.map(function(r){return '<a href="#'+r.id+'">'+esc(anzeige(r.name))+'</a>';}).join('')+'</p>':'')+'</li>';}).join('')+'</ul></section>';
  h+='<section class="abschnitt">'+balken('Zusammenhänge')+'<ol class="kette">'+KETTE.map(function(k,i){var z=finde(k[1]);
    var inhalt='<span class="s-kreis">'+ikon(KETTE_IKON[i]||'book')+'<span class="s-nr">'+(i+1)+'</span></span><span class="s-text">'+esc(k[0])+'</span>';
    return '<li>'+(z?'<a href="#'+z.id+'" title="'+esc(anzeige(z.name))+'">'+inhalt+'</a>':'<span class="k-schritt">'+inhalt+'</span>')+'</li>';}).join('')+'</ol>';
  if(D.knoten['Hauptseite'])h+='<details class="mehr"><summary>Den Zusammenhang ausführlich lesen</summary><div class="zusammenhang">'+md(D.knoten['Hauptseite'])+'</div></details>';
  h+='</section>';
  h+='<section class="abschnitt">'+balken('Bereiche')+'<ul class="bereiche">'+D.bereiche.map(function(b){var x=finde(b.index);if(!x)return '';
    var anz=N.filter(function(n){return n.bereich===b.ordner;}).length;
    return '<li><a class="bereich" href="#'+x.id+'"><span class="b-ikon">'+ikon(BEREICH_IKON[(b.ordner.match(/^\d\d/)||[''])[0]]||'book')+'</span><span class="b-kopf"><span class="b-name">'+esc(bereichName(b.ordner))+'</span><span class="b-anz">'+anz+' Artikel</span></span><span class="b-text">'+esc(x.kurz)+'</span></a></li>';}).join('')+'</ul>';
  var raster=Object.keys(katWerte.raster).sort();
  if(raster.length)h+='<div class="rasterzeile"><span>Raster</span><div class="chips">'+raster.map(function(r){return katLink('raster',r);}).join('')+'</div></div>';
  h+='</section></div>';
  setze(h,'');
  bindeSuche(document.getElementById('suche-gross'),document.getElementById('vorschlag-gross'));
}

/* ---------- Methodenfinder ---------- */
var FG=[['aviva_phase','AVIVA-Phase',PHASEN],['k_stufe','K-Stufe',['K1','K2','K3','K4','K5','ohne']],['sozialform','Sozialform',SOZ],['zeit','Zeitbedarf',D.baender],['eignung_fabe','Eignung FaBe',EIGNUNG],['status','Status',STATUS]];
/* Sichtbar: AVIVA-Phase, K-Stufe, Sozialform und Volltext; «Mehr Filter» klappt die übrigen auf. */
var FG_SICHTBAR=['aviva_phase','k_stufe','sozialform'];
var SCHRITT=24;
var wahl={},finderText='',mehrOffen=false,gezeigt=SCHRITT,trefferListe=[];
var METH=N.filter(function(n){return n.typ==='methode';});
function passt(n,f){var s=wahl[f];if(!s||!s.length)return true;var w=werte(n,f);return s.some(function(x){return w.indexOf(x)>=0;});}
function textPasst(n){if(!finderText)return true;var q=finderText.toLowerCase();return (n.name+' '+n.kurz+' '+(n.material||'')+' '+n.text).toLowerCase().indexOf(q)>=0;}
function filterGruppe(g){return '<div class="filtergruppe"><span>'+esc(g[1])+'</span><div class="chips">'+g[2].map(function(w){return '<button type="button" class="chip" data-f="'+g[0]+'" data-w="'+esc(w)+'" aria-pressed="'+((wahl[g[0]]||[]).indexOf(w)>=0)+'">'+esc(w)+'<span class="anz"></span></button>';}).join('')+'</div></div>';}
function karte(n){
  var m=[];['aviva_phase','k_stufe','sozialform'].forEach(function(f){var v=n.felder[f];if(v&&v.length)m.push(Array.isArray(v)?v.join(', '):v);});
  return '<li class="mf-karte"><a class="mf-name" href="#'+n.id+'">'+esc(anzeige(n.name))+'</a><p class="mf-kurz">'+esc(n.kurz)+'</p>'+(m.length?'<div class="mf-merkmale">'+m.map(function(x){return '<span>'+esc(x)+'</span>';}).join('')+'</div>':'')+'</li>';
}
function fensterZu(){var f=document.getElementById('filter'),o=document.getElementById('mf-oeffnen');document.documentElement.classList.remove('mf-gesperrt');if(f)f.classList.remove('offen');if(o)o.setAttribute('aria-expanded','false');}
window.addEventListener('hashchange',function(){document.documentElement.classList.remove('mf-gesperrt');});
function seiteFinder(){
  gezeigt=SCHRITT;
  var h='<p class="kicker">Methoden und Medien</p><h1 class="titel">Methodenfinder</h1><p class="lead">Wähle Merkmale, um die '+METH.length+' Methoden einzugrenzen.</p>';
  h+='<div class="mf-leiste"><button type="button" class="knopf" id="mf-oeffnen" aria-controls="filter" aria-expanded="false">Filter</button></div>';
  h+='<div class="filter mf-filter" id="filter" tabindex="-1" aria-label="Filter">'+
    '<div class="mf-fensterkopf">Filter<button type="button" class="mf-zu" id="mf-zu" aria-label="Filter schliessen">×</button></div>'+
    FG.filter(function(g){return FG_SICHTBAR.indexOf(g[0])>=0;}).map(filterGruppe).join('')+
    '<div class="filtergruppe"><span>Volltext</span><div class="finder-suche"><input id="finder-text" type="search" placeholder="zum Beispiel Rollenspiel, Karten, Fallbeispiel" value="'+esc(finderText)+'" aria-label="Methoden im Volltext filtern"></div></div>'+
    '<div class="filtergruppe"><span></span><div><button type="button" class="mf-mehrknopf" id="mf-mehrknopf" aria-expanded="'+mehrOffen+'" aria-controls="mf-mehrbereich">Mehr Filter</button></div></div>'+
    '<div class="mf-mehrbereich" id="mf-mehrbereich"'+(mehrOffen?'':' hidden')+'>'+FG.filter(function(g){return FG_SICHTBAR.indexOf(g[0])<0;}).map(filterGruppe).join('')+'</div>'+
    '<div class="mf-fensterfuss"><button type="button" class="mf-anzeigen" id="mf-anzeigen"></button></div>'+
    '</div>';
  h+='<div class="mf-aktiv" id="mf-aktiv"></div><div class="trichter" id="trichter" aria-live="polite"></div><div id="treffer"></div>';
  setze(h,'Methodenfinder');
  S.querySelectorAll('#filter button.chip').forEach(function(b){b.addEventListener('click',function(){var f=b.dataset.f,w=b.dataset.w;wahl[f]=wahl[f]||[];var i=wahl[f].indexOf(w);if(i>=0)wahl[f].splice(i,1);else wahl[f].push(w);b.setAttribute('aria-pressed',i<0);aktualisiere();});});
  var ft=document.getElementById('finder-text');ft.addEventListener('input',function(){finderText=ft.value.trim();aktualisiere();});
  var mk=document.getElementById('mf-mehrknopf'),mb=document.getElementById('mf-mehrbereich');
  mk.addEventListener('click',function(){mehrOffen=!mehrOffen;mb.hidden=!mehrOffen;mk.setAttribute('aria-expanded',mehrOffen);});
  var fi=document.getElementById('filter'),oe=document.getElementById('mf-oeffnen');
  oe.addEventListener('click',function(){fi.classList.add('offen');document.documentElement.classList.add('mf-gesperrt');oe.setAttribute('aria-expanded','true');fi.scrollTop=0;fi.focus();});
  document.getElementById('mf-anzeigen').addEventListener('click',function(){fensterZu();oe.focus();});
  document.getElementById('mf-zu').addEventListener('click',function(){fensterZu();oe.focus();});
  fi.addEventListener('keydown',function(e){if(e.key==='Escape'&&fi.classList.contains('offen')){fensterZu();oe.focus();}});
  document.getElementById('mf-aktiv').addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;
    if(b.id==='zuruecksetzen'){wahl={};finderText='';fensterZu();seiteFinder();return;}
    if(b.dataset.text){finderText='';ft.value='';}
    else{var f=b.dataset.f,w=b.dataset.w,i=(wahl[f]||[]).indexOf(w);if(i>=0)wahl[f].splice(i,1);
      S.querySelectorAll('#filter button.chip').forEach(function(c){if(c.dataset.f===f&&c.dataset.w===w)c.setAttribute('aria-pressed','false');});}
    aktualisiere();
    var z=document.querySelector('#mf-aktiv button');if(z)z.focus();
  });
  document.getElementById('treffer').addEventListener('click',function(e){
    if(!e.target.closest('#mf-weitere'))return;
    var alt=gezeigt;gezeigt+=SCHRITT;zeigeTreffer();
    var neu=document.querySelectorAll('#treffer .mf-karte')[alt];if(neu)neu.querySelector('a').focus();
  });
  aktualisiere();
}
function zeigeTreffer(){
  var rest=trefferListe;
  document.getElementById('treffer').innerHTML=rest.length?'<ul class="mf-karten">'+rest.slice(0,gezeigt).map(karte).join('')+'</ul>'+
    (rest.length>gezeigt?'<p class="mf-weiter"><button type="button" class="knopf" id="mf-weitere">Weitere Methoden zeigen</button></p>':''):
    '<p class="leer">Keine Methode erfüllt alle gewählten Merkmale. Lös oben einen Filter.</p>';
}
function aktualisiere(){
  gezeigt=SCHRITT;
  var rest=METH.slice(),stufen=['<li>Alle Methoden <b>&nbsp;'+rest.length+'</b></li>'],aktiv=[];
  FG.forEach(function(g){if(wahl[g[0]]&&wahl[g[0]].length){rest=rest.filter(function(n){return passt(n,g[0]);});stufen.push('<li>'+esc(g[1])+': '+esc(wahl[g[0]].join(' oder '))+' <b>&nbsp;'+rest.length+'</b></li>');
    wahl[g[0]].forEach(function(w){aktiv.push('<button type="button" class="chip mf-weg" data-f="'+g[0]+'" data-w="'+esc(w)+'" aria-label="Filter '+esc(g[1])+' '+esc(w)+' entfernen">'+esc(g[1])+': '+esc(w)+'<span class="x" aria-hidden="true">×</span></button>');});}});
  if(finderText){rest=rest.filter(textPasst);stufen.push('<li>Volltext «'+esc(finderText)+'» <b>&nbsp;'+rest.length+'</b></li>');
    aktiv.push('<button type="button" class="chip mf-weg" data-text="1" aria-label="Filter Volltext entfernen">Volltext «'+esc(finderText)+'»<span class="x" aria-hidden="true">×</span></button>');}
  document.getElementById('trichter').innerHTML='<b>'+rest.length+'</b> von '+METH.length+' Methoden';
  document.getElementById('mf-aktiv').innerHTML=aktiv.join('')+'<button type="button" class="knopf" id="zuruecksetzen">Alle Filter lösen</button>';
  S.querySelectorAll('#filter button.chip').forEach(function(b){var f=b.dataset.f,w=b.dataset.w;
    var basis=METH.filter(function(n){return FG.every(function(g){return g[0]===f||passt(n,g[0]);})&&textPasst(n);});
    b.querySelector('.anz').textContent=basis.filter(function(n){return werte(n,f).indexOf(w)>=0;}).length;});
  rest.sort(function(a,b){return anzeige(a.name).localeCompare(anzeige(b.name),'de');});
  trefferListe=rest;
  document.getElementById('mf-anzeigen').textContent=rest.length+' Treffer anzeigen';
  zeigeTreffer();
}

/* ---------- Werkzeuge C ---------- */
/* «Lektion planen» (#werkzeug-lektion) und «Aufgabe formulieren» (#werkzeug-aufgabe).
   Fachliche Zahlen und Texte liest das Werkzeug zur Laufzeit aus den Artikeln (N); findet es eine Angabe nicht,
   fällt der betroffene Teil weg, statt eine Zahl zu erfinden. Der Entwurf liegt im localStorage des Browsers. */
var WZ_UNGEPRUEFT='Richtwert, nicht am Original geprüft';
function wzLies(k){try{var s=window.localStorage.getItem(k);return s?JSON.parse(s):null;}catch(e){return null;}}
function wzSchreib(k,v){try{window.localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
function wzLoesche(k){try{window.localStorage.removeItem(k);}catch(e){}}
function wzSpeicherGeht(){try{var k='bs-wz-probe';window.localStorage.setItem(k,'1');window.localStorage.removeItem(k);return true;}catch(e){return false;}}
/* Text eines Abschnitts («## …», Anfang des Titels genügt) */
function wzAbschnitt(name,anfang){
  var n=finde(name);if(!n)return '';
  var out=[],drin=false;
  n.text.split('\n').forEach(function(l){var h=l.match(/^##\s+(.+?)\s*$/);if(h){drin=h[1].indexOf(anfang)===0;return;}if(drin)out.push(l);});
  return out.join('\n').trim();
}
function wzZahl(x){return String(Math.round(x*10)/10).replace('.',',');}
function wzMin(x){return x+(x===1?' Minute':' Minuten');}
function wzUngeprueft(name,ohneRichtwert){var n=finde(name);return n&&n.status==='nicht geprüft'?' <span class="wl-ungeprueft">'+esc(ohneRichtwert?'nicht am Original geprüft':WZ_UNGEPRUEFT)+'</span>':'';}
function wzArtikel(name){var n=finde(name);return n?'<a href="#'+n.id+'">'+esc(anzeige(n.name))+'</a>':esc(name);}
function wzNachlesen(namen){return balken('Zum Nachlesen')+'<ul class="wl-nachlesen">'+namen.map(function(x){return '<li>'+wzArtikel(x)+'</li>';}).join('')+'</ul>';}
/* Sozialform-Kürzel aus dem Artikel «Verlaufsplanung» */
function wzSozialformen(){
  var m=/Kürzel für Sozialformen\*\*[^:\n]*:\s*([^\n]+)/.exec((finde('Verlaufsplanung')||{}).text||'');if(!m)return [];
  return m[1].replace(/\.\s*$/,'').split(/,\s*/).map(function(x){var p=/^([A-Z]{2})\s+(.+)$/.exec(x.trim());return p?{k:p[1],name:p[2]}:null;}).filter(Boolean);
}
function wzSozText(liste,k){for(var i=0;i<liste.length;i++)if(liste[i].k===k)return liste[i].k+' '+liste[i].name;return k||'';}
function wzSozOptionen(liste,wert){return '<option value="">(keine)</option>'+liste.map(function(s){return '<option value="'+esc(s.k)+'"'+(s.k===wert?' selected':'')+'>'+esc(s.k+' '+s.name)+'</option>';}).join('');}
/* Zeile «Entwurf gespeichert» mit Rückfrage vor dem Zurücksetzen (ohne Dialogfenster) */
function wzSpeicherZeile(praefix){
  return '<p class="wl-speicher"><span>'+(wzSpeicherGeht()?'Dein Entwurf bleibt in diesem Browser gespeichert.':'Dieser Browser speichert den Entwurf nicht; er geht beim Verlassen der Seite verloren.')+'</span>'+
    '<button type="button" class="knopf" id="'+praefix+'-zurueck">Entwurf zurücksetzen</button>'+
    '<span class="wl-frage" id="'+praefix+'-frage" hidden><span>Alle Eingaben löschen?</span><button type="button" class="knopf" data-antwort="ja">Ja, zurücksetzen</button><button type="button" class="knopf" data-antwort="nein">Abbrechen</button></span></p>';
}
function wzBindeZuruecksetzen(praefix,loesche){
  var b=document.getElementById(praefix+'-zurueck'),f=document.getElementById(praefix+'-frage');
  b.addEventListener('click',function(){b.hidden=true;f.hidden=false;f.querySelector('button').focus();});
  f.addEventListener('click',function(e){var a=e.target.closest('button[data-antwort]');if(!a)return;
    if(a.dataset.antwort==='ja'){loesche();return;}
    f.hidden=true;b.hidden=false;b.focus();});
}
/* Kopieren: als HTML-Tabelle und als Text, sonst nur Text */
function wzKopiere(text,html,meldung){
  function ok(){meldung.textContent='Ergebnis kopiert.';}
  function fehl(){meldung.textContent='Kopieren hat nicht geklappt. Markiere das Ergebnis und kopiere es von Hand.';}
  function notfall(){
    try{var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.left='-9999px';
      document.body.appendChild(ta);ta.select();var r=document.execCommand('copy');document.body.removeChild(ta);if(r)ok();else fehl();}catch(e){fehl();}
  }
  function nurText(){if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(text).then(ok,notfall);else notfall();}
  meldung.textContent='';
  try{
    if(navigator.clipboard&&navigator.clipboard.write&&window.ClipboardItem){
      navigator.clipboard.write([new ClipboardItem({'text/plain':new Blob([text],{type:'text/plain'}),'text/html':new Blob([html],{type:'text/html'})})]).then(ok,nurText);
    } else nurText();
  }catch(e){nurText();}
}
function wzZelle(s){return esc(s).replace(/\r?\n/g,'<br>');}

/* ----- Lektion planen ----- */
var WL_KEY='bs-wz-lektion',WL={},wl=null,wlErg={text:'',html:''};
function wlName(art){var n=phaseNotiz(art);return n?n.name.replace(/^AVIVA Phase /,''):art;}
function wlGrundlagen(){
  /* Richtwerte: Artikel «AVIVA-Modell», Abschnitt «Davids Richtwerte (keine Buchvorgabe)» */
  var t=wzAbschnitt('AVIVA-Modell','Davids Richtwerte'),kurz={Ankommen:'Ankommen',Vorwissen:'Vorwissen aktivieren',Informieren:'Informieren',Verarbeiten:'Verarbeiten',Auswerten:'Auswerten'};
  var rw={},re=/(Ankommen|Vorwissen|Informieren|Verarbeiten|Auswerten)\s+(\d+)(?:\s+bis\s+(\d+))?\s*%/g,m;
  while((m=re.exec(t)))if(!rw[kurz[m[1]]])rw[kurz[m[1]]]={von:+m[2],bis:m[3]?+m[3]:+m[2]};
  /* Reserve: Artikel «Zeitplanung einer Lektion» («rund 20 % Reserve (S. 63)») */
  var z=/rund\s+(\d+)\s*%\s*Reserve(\s*\([^)]*\))?/.exec(wzAbschnitt('Zeitplanung einer Lektion','Aus Lehren kompakt 1'));
  /* Input: Artikel «Dauer von Inputphasen», Entscheid E-050 */
  var inp=/Richtwert für einen Input:\s*(\d+)\s*bis\s*(\d+)\s*Minuten/.exec(wzAbschnitt('Dauer von Inputphasen','Entscheid'));
  WL={rw:PHASEN.every(function(p){return rw[p];})?rw:null,reserve:z?+z[1]:null,reserveBeleg:z&&z[2]?z[2].trim():'',
    input:inp?{von:+inp[1],bis:+inp[2]}:null,soz:wzSozialformen(),meth:{}};
  PHASEN.forEach(function(p){WL.meth[p]=METH.filter(function(n){return werte(n,'aviva_phase').indexOf(p)>=0;}).sort(function(a,b){return anzeige(a.name).localeCompare(anzeige(b.name),'de');});});
}
function wlNeuePhase(art,auto){return {art:art,min:0,auto:!!auto,methode:'',soz:'',inhalt:'',medien:'',sicherung:'',vorlage:{inhalt:'',medien:''}};}
function wlStandard(){return {lek:2,pausen:0,reserve:false,phasen:PHASEN.map(function(p){return wlNeuePhase(p,true);})};}
function wlRechnung(s){
  var unterricht=s.lek*45,nachPausen=Math.max(0,unterricht-s.pausen);
  var res=s.reserve&&WL.reserve?Math.round(nachPausen*WL.reserve/100):0;
  return {unterricht:unterricht,pausen:s.pausen,reserve:res,plan:nachPausen-res,zuViel:s.pausen>unterricht};
}
/* Vorbelegung: Mitte der Spanne, ganze Minuten, Rundungsrest zu Verarbeiten */
function wlMitten(plan){
  if(!WL.rw)return null;var m={},sum=0;
  PHASEN.forEach(function(p){m[p]=Math.round(plan*(WL.rw[p].von+WL.rw[p].bis)/200);sum+=m[p];});
  m.Verarbeiten=Math.max(0,m.Verarbeiten+plan-sum);return m;
}
function wlVorbelegen(s){var m=wlMitten(wlRechnung(s).plan);if(m)s.phasen.forEach(function(p){if(p.auto)p.min=m[p.art];});return s;}
function wlLaden(){
  var s=wzLies(WL_KEY);
  if(!s||typeof s!=='object'||!Array.isArray(s.phasen))return wlVorbelegen(wlStandard());
  var d={lek:[2,3,4,5].indexOf(s.lek)>=0?s.lek:2,pausen:typeof s.pausen==='number'&&s.pausen>=0?Math.round(s.pausen):0,reserve:!!s.reserve,phasen:[]};
  s.phasen.forEach(function(p){if(!p||PHASEN.indexOf(p.art)<0)return;var q=wlNeuePhase(p.art,p.auto);q.min=Math.max(0,Math.round(+p.min||0));
    ['methode','soz','inhalt','medien','sicherung'].forEach(function(f){q[f]=typeof p[f]==='string'?p[f]:'';});
    if(p.vorlage&&typeof p.vorlage==='object')['inhalt','medien'].forEach(function(f){q.vorlage[f]=typeof p.vorlage[f]==='string'?p.vorlage[f]:'';});d.phasen.push(q);});
  return wlVorbelegen(d);
}
function wlOptionen(p,filter){
  var liste=WL.meth[p.art]||[],q=(filter||'').toLowerCase().trim();
  var treffer=q?liste.filter(function(n){return anzeige(n.name).toLowerCase().indexOf(q)>=0;}):liste;
  var o='<option value="">(keine Methode)</option>';
  if(p.methode&&!treffer.some(function(n){return n.name===p.methode;}))o+='<option value="'+esc(p.methode)+'" selected>'+esc(anzeige(p.methode))+'</option>';
  o+=treffer.map(function(n){return '<option value="'+esc(n.name)+'"'+(n.name===p.methode?' selected':'')+'>'+esc(anzeige(n.name))+'</option>';}).join('');
  var anz=(q?treffer.length+' von ':'')+liste.length+(liste.length===1?' Methode':' Methoden')+' mit der AVIVA-Phase «'+p.art+'»';
  return {html:o,anz:anz};
}
function wlMethLink(p){var n=p.methode?finde(p.methode):null;return n?'<a href="#'+n.id+'">Zum Methodenartikel</a>':'';}
/* Vorbelegung aus dem Methodenartikel (E-109): Abschnitt «Ablauf» ohne Material und Zeit ins Feld «Inhalt»,
   Feld «material» in «Medien und Material». Gefüllt werden nur leere Felder oder solche, die noch den
   übernommenen Text der vorher gewählten Methode tragen; eigener Text bleibt stehen. Ergebnissicherung
   steht in keinem Methodenartikel: das Feld bleibt leer, mit Hinweis. Artikel ohne «Ablauf»: alles leer. */
function wlVorlage(name){
  var n=name?finde(name):null,v={inhalt:'',medien:'',hinweis:false};if(!n)return v;
  var ab=[],drin=false;
  n.text.split('\n').forEach(function(l){var h=l.match(/^##\s+(.+?)\s*$/);if(h){drin=h[1].indexOf('Ablauf')===0;return;}if(drin)ab.push(l);});
  var t=ab.join('\n').split(/\*\*(?:Material|Zeit):\*\*/)[0].trim();
  if(!t)return v;
  v.inhalt=t.replace(/\s+(?=\d+\)\s)/g,'\n');
  v.medien=String(n.material||'').trim();
  v.hinweis=true;
  return v;
}
function wlSichHinweis(p){return p.methode&&wlVorlage(p.methode).hinweis?'Im Methodenartikel nicht angegeben.':'';}
function wlUebernehmen(p){
  var v=wlVorlage(p.methode);
  ['inhalt','medien'].forEach(function(f){if(!p[f]||p[f]===p.vorlage[f])p[f]=v[f];p.vorlage[f]=v[f];});
}
function wlFeld(p,i,f,label){return '<div class="wl-feld"><label for="wl-'+f+'-'+i+'">'+esc(label)+'</label><textarea id="wl-'+f+'-'+i+'" data-feld="'+f+'" rows="2">'+esc(p[f])+'</textarea>'+
  (f==='sicherung'?'<p class="wl-hinweis wl-sichhinweis">'+esc(wlSichHinweis(p))+'</p>':'')+'</div>';}
function wlKarte(p,i){
  var nm=wlName(p.art),o=wlOptionen(p,'');
  return '<div class="wl-karte" data-phase="'+esc(p.art)+'"><div class="wl-phase-kopf"><h3 class="wl-phase-name"><span class="wl-nr">'+(i+1)+'</span><span>'+esc(nm)+'</span></h3>'+
    '<button type="button" class="wl-entfernen" data-akt="entfernen" aria-label="Phase '+(i+1)+' '+esc(nm)+' entfernen">Entfernen</button></div>'+
    '<div class="wl-reihe wl-reihe1">'+
      '<div class="wl-feld"><label for="wl-min-'+i+'">Minuten</label><input id="wl-min-'+i+'" type="number" min="0" step="1" inputmode="numeric" data-feld="min" value="'+p.min+'"></div>'+
      '<div class="wl-feld wl-feld-methode"><label for="wl-methode-'+i+'">Methode</label>'+
        '<input type="search" data-akt="msuche" placeholder="Methode suchen" autocomplete="off" aria-label="Methoden der Phase '+esc(nm)+' durchsuchen">'+
        '<select id="wl-methode-'+i+'" data-feld="methode">'+o.html+'</select>'+
        '<p class="wl-hinweis wl-anz">'+esc(o.anz)+'</p><p class="wl-methlink">'+wlMethLink(p)+'</p></div>'+
      '<div class="wl-feld"><label for="wl-soz-'+i+'">Sozialform</label><select id="wl-soz-'+i+'" data-feld="soz">'+wzSozOptionen(WL.soz,p.soz)+'</select></div>'+
    '</div>'+
    '<div class="wl-reihe wl-reihe2">'+wlFeld(p,i,'inhalt','Inhalt')+wlFeld(p,i,'medien','Medien und Material')+wlFeld(p,i,'sicherung','Ergebnissicherung')+'</div></div>';
}
function wlPlus(i){
  return '<div class="wl-plus"><button type="button" class="knopf" data-akt="plus" data-nach="'+i+'" aria-expanded="false">Phase hinzufügen</button>'+
    '<div class="wl-wahl" hidden><span class="wl-hinweis">Art der neuen Phase:</span>'+
    PHASEN.map(function(p){return '<button type="button" class="chip" data-akt="neu" data-nach="'+i+'" data-art="'+esc(p)+'">'+esc(wlName(p))+'</button>';}).join('')+
    '<button type="button" class="knopf" data-akt="abbrechen">Abbrechen</button></div></div>';
}
function wlPhasenZeichnen(fokus){
  var el=document.getElementById('wl-phasen');
  el.innerHTML=wl.phasen.length?wl.phasen.map(function(p,i){return '<li data-i="'+i+'">'+wlKarte(p,i)+wlPlus(i)+'</li>';}).join(''):'<li>'+wlPlus(-1)+'</li>';
  if(fokus){var x=el.querySelector(fokus);if(x)x.focus();}
}
function wlRahmenGeaendert(){
  wlVorbelegen(wl);
  wl.phasen.forEach(function(p,i){if(p.auto){var x=document.getElementById('wl-min-'+i);if(x)x.value=p.min;}});
  wlAktualisiere();
}
function wlErgebnis(r){
  var zeilen=[],t=0;
  wl.phasen.forEach(function(p){zeilen.push({phase:wlName(p.art),zeit:t+'–'+(t+p.min),dauer:p.min+' Min.',inhalt:p.inhalt,methode:p.methode?anzeige(p.methode):'',soz:p.soz,medien:p.medien,sicherung:p.sicherung});t+=p.min;});
  if(r.reserve)zeilen.push({phase:'Reserve',zeit:t+'–'+(t+r.reserve),dauer:r.reserve+' Min.',reserve:true});
  var SP=[['phase','Phase'],['zeit','Zeit'],['dauer','Dauer'],['inhalt','Inhalt'],['methode','Methode'],['soz','Sozialform'],['medien','Medien und Material'],['sicherung','Ergebnissicherung']];
  var kopf=[['Lektionen',wl.lek+' ('+wzMin(r.unterricht)+')'],['Pausen',wzMin(r.pausen)],['Reserve',r.reserve?wzMin(r.reserve)+' ('+WL.reserve+' %)':'keine'],['Planungszeit',wzMin(r.plan)]];
  function wert(z,k){return z[k]==null?'':String(z[k]);}
  var h='<h2 class="wl-erg-titel">Verlaufsplan</h2><dl class="wl-kopfdaten">'+kopf.map(function(k){return '<div><dt>'+esc(k[0])+'</dt><dd>'+esc(k[1])+'</dd></div>';}).join('')+'</dl>'+
    '<table class="wl-tab wl-plan"><thead><tr>'+SP.map(function(s){return '<th scope="col">'+esc(s[1])+'</th>';}).join('')+'</tr></thead><tbody>'+
    (zeilen.length?zeilen.map(function(z){return '<tr'+(z.reserve?' class="wl-reserve"':'')+'>'+SP.map(function(s){return '<td data-label="'+esc(s[1])+'"'+(s[0]==='zeit'||s[0]==='dauer'?' class="wl-zahl"':'')+'>'+wzZelle(wert(z,s[0]))+'</td>';}).join('')+'</tr>';}).join('')
      :'<tr class="wl-leerzeile"><td colspan="8">Noch keine Phase geplant.</td></tr>')+'</tbody></table>';
  var text='Verlaufsplan\n'+kopf.map(function(k){return k[0]+': '+k[1];}).join('\n')+'\n\n'+SP.map(function(s){return s[1];}).join('\t')+'\n'+
    zeilen.map(function(z){return SP.map(function(s){return wert(z,s[0]).replace(/\s*\r?\n\s*/g,' ').replace(/\t/g,' ');}).join('\t');}).join('\n');
  var html='<h2>Verlaufsplan</h2><p>'+kopf.map(function(k){return '<b>'+esc(k[0])+':</b> '+esc(k[1]);}).join('<br>')+'</p>'+
    '<table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse"><thead><tr>'+SP.map(function(s){return '<th style="text-align:left">'+esc(s[1])+'</th>';}).join('')+'</tr></thead><tbody>'+
    zeilen.map(function(z){return '<tr>'+SP.map(function(s){return '<td style="vertical-align:top">'+wzZelle(wert(z,s[0]))+'</td>';}).join('')+'</tr>';}).join('')+'</tbody></table>';
  return {anzeige:h,text:text,html:html,zeilen:zeilen,SP:SP,kopf:kopf};
}
function wlAktualisiere(){
  var r=wlRechnung(wl),sum=wl.phasen.reduce(function(a,p){return a+p.min;},0);
  document.getElementById('wl-bilanz').innerHTML=
    '<div><dt>Unterricht</dt><dd>'+wzMin(r.unterricht)+'<small>'+wl.lek+' Lektionen zu 45 Minuten</small></dd></div>'+
    '<div><dt>Pausen</dt><dd>'+wzMin(r.pausen)+'</dd></div>'+
    '<div><dt>Reserve</dt><dd>'+(r.reserve?wzMin(r.reserve)+'<small>'+WL.reserve+' % der Zeit nach Pausen</small>':'keine')+'</dd></div>'+
    '<div><dt>Planungszeit</dt><dd>'+wzMin(r.plan)+'</dd></div>';
  var g=document.getElementById('wl-geruest');
  if(g)g.innerHTML=PHASEN.map(function(p){var w=WL.rw[p],a=w.von*r.plan/100,b=w.bis*r.plan/100;
    return '<tr><td>'+esc(wlName(p))+'</td><td class="wl-zahl">'+(w.von===w.bis?w.von+' %':w.von+' bis '+w.bis+' %')+'</td><td class="wl-zahl">'+(w.von===w.bis?wzZahl(a):wzZahl(a)+' bis '+wzZahl(b))+'</td></tr>';}).join('');
  document.getElementById('wl-summe').innerHTML='Summe der Phasen: <b>'+sum+'</b> von '+wzMin(r.plan);
  var w=[];
  if(r.zuViel)w.push('Die Pausen sind länger als der Unterricht von '+wzMin(r.unterricht)+'.');
  if(sum!==r.plan){var d=Math.abs(sum-r.plan);
    w.push('Die Phasen ergeben zusammen '+wzMin(sum)+', die Planungszeit beträgt '+wzMin(r.plan)+': '+(sum<r.plan?(d===1?'Es fehlt 1 Minute.':'Es fehlen '+d+' Minuten.'):wzMin(d)+' zu viel.'));}
  if(WL.input)wl.phasen.forEach(function(p,i){if(p.art==='Informieren'&&p.min>WL.input.bis)
    w.push('Phase '+(i+1)+' «'+esc(wlName(p.art))+'» dauert '+wzMin(p.min)+'. Richtwert für einen Input laut Artikel «'+wzArtikel('Dauer von Inputphasen')+'» (Entscheid E-050): '+WL.input.von+' bis '+WL.input.bis+' Minuten.');});
  var box=document.getElementById('wl-warn');
  box.hidden=!w.length;
  box.innerHTML=w.length?'<p class="wl-warn-titel">Hinweise</p><ul>'+w.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>':'';
  wlErg=wlErgebnis(r);
  document.getElementById('wl-ergebnis').innerHTML=wlErg.anzeige;
  wzSchreib(WL_KEY,wl);
}
/* Word-Datei (E-109): .docx ohne Bibliothek, ZIP ohne Kompression; A4 quer, Spalten wie im Verlaufsplan */
var WL_CRC=null;
function wlCrc(b){
  if(!WL_CRC){WL_CRC=[];for(var n=0;n<256;n++){var c=n;for(var k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;WL_CRC[n]=c>>>0;}}
  var x=0xFFFFFFFF;for(var i=0;i<b.length;i++)x=WL_CRC[(x^b[i])&255]^(x>>>8);return (x^0xFFFFFFFF)>>>0;
}
function wlZip(dateien){
  var enc=new TextEncoder(),teile=[],zentral=[],pos=0,zLaenge=0;
  function u16(v){return [v&255,(v>>>8)&255];}
  function u32(v){return [v&255,(v>>>8)&255,(v>>>16)&255,(v>>>24)&255];}
  dateien.forEach(function(d){
    var name=enc.encode(d.name),daten=enc.encode(d.text),crc=wlCrc(daten);
    var lk=[0x50,0x4b,3,4].concat(u16(20),u16(0x0800),u16(0),u16(0),u16(33),u32(crc),u32(daten.length),u32(daten.length),u16(name.length),u16(0));
    var zk=[0x50,0x4b,1,2].concat(u16(20),u16(20),u16(0x0800),u16(0),u16(0),u16(33),u32(crc),u32(daten.length),u32(daten.length),u16(name.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(pos));
    teile.push(new Uint8Array(lk),name,daten);pos+=lk.length+name.length+daten.length;
    zentral.push(new Uint8Array(zk),name);zLaenge+=zk.length+name.length;
  });
  var ende=new Uint8Array([0x50,0x4b,5,6].concat(u16(0),u16(0),u16(dateien.length),u16(dateien.length),u32(zLaenge),u32(pos),u16(0)));
  var alle=teile.concat(zentral,[ende]),gesamt=0;alle.forEach(function(a){gesamt+=a.length;});
  var out=new Uint8Array(gesamt),o=0;alle.forEach(function(a){out.set(a,o);o+=a.length;});return out;
}
function wlXml(s){return esc(String(s==null?'':s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g,''));}
function wlDocx(e){
  var NS='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"',BR=[1500,1000,900,3600,1800,1400,2600,2336];
  function lauf(t,fett,kursiv,weiss,gr){return '<w:r><w:rPr>'+(fett?'<w:b/>':'')+(kursiv?'<w:i/>':'')+(weiss?'<w:color w:val="FFFFFF"/>':'')+'<w:sz w:val="'+(gr||18)+'"/></w:rPr><w:t xml:space="preserve">'+wlXml(t)+'</w:t></w:r>';}
  function absaetze(t,fett,kursiv,weiss){return String(t==null?'':t).split(/\r?\n/).map(function(z){return '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'+(z?lauf(z,fett,kursiv,weiss):'')+'</w:p>';}).join('');}
  function zelle(i,inhalt,kopf){return '<w:tc><w:tcPr><w:tcW w:w="'+BR[i]+'" w:type="dxa"/>'+(kopf?'<w:shd w:val="clear" w:color="auto" w:fill="5B3A29"/>':'')+'</w:tcPr>'+inhalt+'</w:tc>';}
  var rand='<w:tblBorders>'+['top','left','bottom','right','insideH','insideV'].map(function(s){return '<w:'+s+' w:val="single" w:sz="4" w:space="0" w:color="DCD0C2"/>';}).join('')+'</w:tblBorders>';
  var tab='<w:tbl><w:tblPr><w:tblW w:w="15136" w:type="dxa"/>'+rand+'<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>'+
    '<w:tblGrid>'+BR.map(function(b){return '<w:gridCol w:w="'+b+'"/>';}).join('')+'</w:tblGrid>'+
    '<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>'+e.SP.map(function(s,i){return zelle(i,absaetze(s[1],true,false,true),true);}).join('')+'</w:tr>'+
    e.zeilen.map(function(z){return '<w:tr><w:trPr><w:cantSplit/></w:trPr>'+e.SP.map(function(s,i){return zelle(i,absaetze(z[s[0]],false,!!z.reserve,false),false);}).join('')+'</w:tr>';}).join('')+'</w:tbl>';
  var titel='<w:p><w:pPr><w:spacing w:after="120"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="5B3A29"/><w:sz w:val="32"/></w:rPr><w:t>Verlaufsplan</w:t></w:r></w:p>';
  var kopf='<w:p><w:pPr><w:spacing w:after="160"/></w:pPr>'+e.kopf.map(function(k,i){return (i?lauf('   |   ',false,false,false,20):'')+lauf(k[0]+': ',true,false,false,20)+lauf(k[1],false,false,false,20);}).join('')+'</w:p>';
  var dok='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document '+NS+'><w:body>'+titel+kopf+tab+'<w:p/>'+
    '<w:sectPr><w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/><w:pgMar w:top="851" w:right="851" w:bottom="851" w:left="851" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr></w:body></w:document>';
  return wlZip([
    {name:'[Content_Types].xml',text:'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'},
    {name:'_rels/.rels',text:'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'},
    {name:'word/document.xml',text:dok}
  ]);
}
var WL_NICHT='Herunterladen geht in dieser Ansicht nicht. Kopiere das Ergebnis und füge es in Word ein.';
function wlWord(meldung){
  meldung.textContent='';
  var daten,name='Verlaufsplan.docx';
  try{daten=wlDocx(wlErg);}catch(err){meldung.textContent='Die Word-Datei liess sich nicht erstellen.';return;}
  function lokal(){
    try{var url=URL.createObjectURL(new Blob([daten],{type:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}));
      var a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();document.body.removeChild(a);
      setTimeout(function(){URL.revokeObjectURL(url);},4000);meldung.textContent='Word-Datei erstellt.';}catch(err){meldung.textContent=WL_NICHT;}
  }
  var c=window.claude;
  if(!c||typeof c.use!=='function'){lokal();return;}
  c.use('downloads').then(function(dl){
    if(!dl){meldung.textContent=WL_NICHT;return;}
    return dl.save({filename:name,data:daten}).then(function(r){meldung.textContent=r&&r.status==='delivered'?'':'Word-Datei gespeichert.';},
      function(err){var k=err&&err.code;meldung.textContent=k==='declined'?'Herunterladen abgebrochen.':k==='rate_limited'?'Eine Speicheranfrage ist schon offen.':WL_NICHT;});
  },function(){meldung.textContent=WL_NICHT;});
}
function seiteWerkzeugLektion(){
  wlGrundlagen();wl=wlLaden();
  var h='<div class="wl-seite"><div class="wz-kopf"><span class="wz-ikon">'+ikon('plan')+'</span><div><p class="kicker">Werkzeug</p><h1 class="titel">Lektion planen</h1></div></div>'+
    '<p class="lead">Wähle die Dauer, verteile die Planungszeit auf die AVIVA-Phasen und fülle den Verlaufsplan Phase für Phase aus.</p>'+
    wzSpeicherZeile('wl');
  h+='<section class="wl-eingabe" aria-label="Eingaben">'+balken('Rahmen')+'<div class="wl-rahmen">'+
    '<div class="wl-feld" role="group" aria-labelledby="wl-dauer-t"><span class="wl-etikett" id="wl-dauer-t">Dauer</span><div class="chips" id="wl-dauer">'+
      [2,3,4,5].map(function(k){return '<button type="button" class="chip" data-lek="'+k+'" aria-pressed="'+(wl.lek===k)+'">'+k+' Lektionen</button>';}).join('')+
      '</div><p class="wl-hinweis">1 Lektion = 45 Minuten</p></div>'+
    '<div class="wl-feld"><label for="wl-pausen">Pausen in Minuten</label><input id="wl-pausen" type="number" min="0" step="1" inputmode="numeric" value="'+wl.pausen+'"><p class="wl-hinweis">Die Pausen gehen von der Planungszeit ab.</p></div>'+
    (WL.reserve?'<div class="wl-feld"><span class="wl-etikett">Reserve</span><label class="wl-schalter"><input type="checkbox" id="wl-reserve"'+(wl.reserve?' checked':'')+'><span>'+WL.reserve+' % Reserve einplanen</span></label>'+
      '<p class="wl-hinweis">Laut Artikel «'+wzArtikel('Zeitplanung einer Lektion')+'», Abschnitt «Aus Lehren kompakt 1»: rund '+WL.reserve+' % Reserve'+(WL.reserveBeleg?' '+esc(WL.reserveBeleg):'')+'. Die Reserve geht von der Zeit nach den Pausen ab.'+wzUngeprueft('Zeitplanung einer Lektion')+'</p></div>':'')+
    '</div><dl class="wl-bilanz" id="wl-bilanz"></dl>';
  h+=balken('Zeitgerüst nach AVIVA')+(WL.rw?
    '<div class="wl-geruest"><table class="wl-tab"><thead><tr><th scope="col">Phase</th><th scope="col">Richtwert</th><th scope="col">Spanne in Minuten</th></tr></thead><tbody id="wl-geruest"></tbody></table></div>'+
    '<p class="wl-hinweis">Richtwerte laut Artikel «'+wzArtikel('AVIVA-Modell')+'», Abschnitt «Davids Richtwerte (keine Buchvorgabe)». Die Spanne bezieht sich auf die Planungszeit.</p>'
    :'<p class="leer">Die Richtwerte im Artikel «AVIVA-Modell» sind nicht lesbar; die Minuten werden nicht vorbelegt.</p>');
  h+=balken('Phasen')+'<p class="wl-summe" id="wl-summe"></p>'+
    '<p class="wl-hinweis">Die Minuten sind mit der Mitte der Richtwerte vorbelegt, auf ganze Minuten gerundet; der Rundungsrest geht zu «Verarbeiten». Änderst du die Minuten einer Phase, bleibt dein Wert stehen. Phasen dürfen im Block wiederholt werden (Artikel «'+wzArtikel('AVIVA-Modell')+'»).</p>'+
    '<ol class="wl-phasen" id="wl-phasen"></ol><div class="wl-warn" id="wl-warn" role="status" hidden></div></section>';
  h+=balken('Ergebnis')+'<section class="wl-ergebnis" id="wl-ergebnis" aria-label="Verlaufsplan"></section>'+
    '<div class="wl-knoepfe"><button type="button" class="knopf" id="wl-kopieren">Ergebnis kopieren</button><button type="button" class="knopf" id="wl-drucken">Drucken</button><button type="button" class="knopf primaer" id="wl-word">Als Word-Datei herunterladen</button></div>'+
    '<p class="wl-meldung" id="wl-meldung" role="status"></p>';
  h+=wzNachlesen(['AVIVA-Modell','Verlaufsplanung','Zeitplanung einer Lektion','Dauer von Inputphasen','Planungskette fertigen Unterricht'])+'</div>';
  setze(h,'Lektion planen');
  wlPhasenZeichnen();
  wzBindeZuruecksetzen('wl',function(){wzLoesche(WL_KEY);seiteWerkzeugLektion();document.getElementById('wl-zurueck').focus();});
  document.getElementById('wl-dauer').addEventListener('click',function(e){var b=e.target.closest('button[data-lek]');if(!b)return;wl.lek=+b.dataset.lek;
    this.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});wlRahmenGeaendert();});
  document.getElementById('wl-pausen').addEventListener('input',function(){var v=parseInt(this.value,10);wl.pausen=isNaN(v)||v<0?0:v;wlRahmenGeaendert();});
  var rs=document.getElementById('wl-reserve');if(rs)rs.addEventListener('change',function(){wl.reserve=rs.checked;wlRahmenGeaendert();});
  var ph=document.getElementById('wl-phasen');
  function eingabe(e){
    var t=e.target,li=t.closest('li[data-i]');if(!li)return;var p=wl.phasen[+li.dataset.i];if(!p)return;
    if(t.dataset.akt==='msuche'){var o=wlOptionen(p,t.value);li.querySelector('select[data-feld="methode"]').innerHTML=o.html;li.querySelector('.wl-anz').textContent=o.anz;return;}
    var f=t.dataset.feld;if(!f)return;
    if(f==='min'){var v=parseInt(t.value,10);p.min=isNaN(v)||v<0?0:v;p.auto=false;}
    else{p[f]=t.value;if(f==='methode'){li.querySelector('.wl-methlink').innerHTML=wlMethLink(p);wlUebernehmen(p);
      ['inhalt','medien'].forEach(function(g){var x=li.querySelector('textarea[data-feld="'+g+'"]');if(x)x.value=p[g];});
      var sh=li.querySelector('.wl-sichhinweis');if(sh)sh.textContent=wlSichHinweis(p);}}
    wlAktualisiere();
  }
  ph.addEventListener('input',eingabe);ph.addEventListener('change',eingabe);
  ph.addEventListener('click',function(e){
    var b=e.target.closest('button[data-akt]');if(!b)return;var a=b.dataset.akt;
    if(a==='entfernen'){var i=+b.closest('li[data-i]').dataset.i;wl.phasen.splice(i,1);
      wlPhasenZeichnen(i>0?'button[data-akt="plus"][data-nach="'+(i-1)+'"]':'button[data-akt="plus"]');wlAktualisiere();return;}
    if(a==='plus'){var w=b.nextElementSibling,auf=w.hidden;
      ph.querySelectorAll('.wl-wahl').forEach(function(x){x.hidden=true;x.previousElementSibling.setAttribute('aria-expanded','false');});
      w.hidden=!auf;b.setAttribute('aria-expanded',String(auf));if(auf)w.querySelector('button').focus();return;}
    if(a==='abbrechen'){var ww=b.closest('.wl-wahl');ww.hidden=true;ww.previousElementSibling.setAttribute('aria-expanded','false');ww.previousElementSibling.focus();return;}
    if(a==='neu'){var n=+b.dataset.nach+1;wl.phasen.splice(n,0,wlNeuePhase(b.dataset.art,false));wlPhasenZeichnen('#wl-min-'+n);wlAktualisiere();}
  });
  document.getElementById('wl-kopieren').addEventListener('click',function(){wzKopiere(wlErg.text,wlErg.html,document.getElementById('wl-meldung'));});
  document.getElementById('wl-drucken').addEventListener('click',function(){window.print();});
  var wb=document.getElementById('wl-word');wb.addEventListener('click',function(){wlWord(document.getElementById('wl-meldung'));});
  if(window.claude&&typeof window.claude.use==='function')window.claude.use('downloads').then(function(dl){if(!dl)wb.hidden=true;},function(){wb.hidden=true;});
  wlAktualisiere();
}

/* ----- Aufgabe formulieren ----- */
var WA_KEY='bs-wz-aufgabe',WA={},wa=null,waErg={text:'',html:''},waMarke=null;
function waGrundlagen(){
  /* Operatorenliste: Artikel «Operatoren und K-Stufen», Tabelle der Aufgabentypen-Palette (K1 bis K5) */
  var ops=[];
  String((finde('Operatoren und K-Stufen')||{}).text||'').split('\n').forEach(function(l){
    var m=/^\|\s*(K[1-5])\b\s*([^|]*)\|\s*([^|]+?)\s*\|\s*$/.exec(l);if(!m)return;
    ops.push({k:m[1],titel:(m[1]+' '+m[2].trim()).trim(),ops:m[3].split(/,\s*/).map(function(o){o=o.trim();return {label:o,wort:o.replace(/\s*\([^)]*\)\s*$/,'')};})});
  });
  var mehr=wzAbschnitt('Operatoren und K-Stufen','Mehrdeutige Operatoren'),satz=(/^[^.]*\./.exec(mehr)||[''])[0];
  var el=/Aufgabenziel \(([^)]+)\), Aufgabenstellung \(([^)]+)\), Zeitbudget \(([^)]+)\), Sozialform \(([^)]+)\)/.exec((finde('Arbeitsauftrag formulieren')||{}).text||'');
  WA={ops:ops,mehrdeutig:satz,frage:el?{ziel:el[1],stellung:el[2],zeit:el[3],soz:el[4]}:{},
    soz:wzSozialformen().filter(function(s){return ['EA','PA','GA','PL'].indexOf(s.k)>=0;}),
    typen:N.filter(function(n){return n.typ==='aufgabentyp';}).sort(function(a,b){return a.name.localeCompare(b.name,'de');})};
}
function waTypName(n){return anzeige(n.name).replace(/^Aufgabentyp\s+\d+\s+/,'');}
function waTypNr(n){var m=/^Aufgabentyp\s+0*(\d+)/.exec(n.name);return m?m[1]:'';}
function waLaden(){
  var s=wzLies(WA_KEY),d={nr:'1',k:'',typ:'',ziel:'',stellung:'',zeit:'',soz:''};
  if(!s||typeof s!=='object')return d;
  Object.keys(d).forEach(function(f){if(typeof s[f]==='string')d[f]=s[f];});
  if(!WA.ops.some(function(o){return o.k===d.k;}))d.k='';
  if(d.typ&&!waTypPasst(finde(d.typ),d.k))d.typ='';
  return d;
}
function waTypPasst(n,k){return !!(n&&k&&werte(n,'k_stufe').indexOf(k)>=0);}
function waStufe(k){for(var i=0;i<WA.ops.length;i++)if(WA.ops[i].k===k)return WA.ops[i];return null;}
/* Ganzes Wort, Gross- und Kleinschreibung egal; mehrteilige Operatoren als Wortfolge */
function waEnthaelt(text,wort){
  var b='[^A-Za-zÄÖÜäöüß]',w=wort.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/\s+/g,'\\s+');
  return new RegExp('(^|'+b+')'+w+'(?='+b+'|$)','i').test(text||'');
}
function waStufeZeichnen(){
  var el=document.getElementById('wa-stufe'),st=waStufe(wa.k);
  if(!st){el.innerHTML='<p class="leer">Wähle zuerst eine K-Stufe. Dann erscheinen die Operatoren und die Aufgabentypen dieser Stufe.</p>';return;}
  var typen=WA.typen.filter(function(n){return waTypPasst(n,st.k);});
  el.innerHTML='<div class="wa-block"><div class="wl-feld"><span class="wl-etikett">Operatoren für '+esc(st.k)+'</span><div class="chips" id="wa-ops">'+
    st.ops.map(function(o){return '<button type="button" class="chip" data-wort="'+esc(o.wort)+'">'+esc(o.label)+'</button>';}).join('')+'</div>'+
    '<p class="wl-hinweis">Ein Klick setzt den Operator in die Aufgabenstellung, an die Stelle der Schreibmarke; ohne Schreibmarke an den Anfang.</p></div>'+
    '<fieldset class="wa-typen"><legend>Aufgabentypen mit '+esc(st.k)+' ('+typen.length+')</legend><ul class="wa-typliste">'+
    '<li><label class="wa-typ"><input type="radio" name="wa-typ" value=""'+(wa.typ?'':' checked')+'><span class="wa-typ-text">Kein Typ<small>Der Typ entfällt im Titel.</small></span></label></li>'+
    typen.map(function(n){return '<li><label class="wa-typ"><input type="radio" name="wa-typ" value="'+esc(n.name)+'"'+(wa.typ===n.name?' checked':'')+'><span class="wa-typ-text">'+esc(waTypName(n))+
      '<small>Typ '+esc(waTypNr(n))+' | '+esc(werte(n,'k_stufe').join(', '))+'</small></span></label><a class="wa-typlink" href="#'+n.id+'" aria-label="Artikel '+esc(anzeige(n.name))+'">Zum Artikel</a></li>';}).join('')+
    '</ul></fieldset></div>';
}
function waTitel(){
  var n=wa.typ?finde(wa.typ):null,t='Aufgabe'+(wa.nr.trim()?' '+wa.nr.trim():'');
  if(wa.k)t+=' ('+(n?waTypName(n)+', ':'')+wa.k+')';
  return t;
}
function waAktualisiere(){
  var w=[];
  if(wa.k)WA.ops.forEach(function(st){if(st.k===wa.k)return;st.ops.forEach(function(o){if(waEnthaelt(wa.stellung,o.wort))
    w.push('Die Aufgabenstellung enthält «'+esc(o.wort)+'». Laut Operatorenliste gehört dieser Operator zu '+esc(st.k)+', gewählt ist '+esc(wa.k)+'.');});});
  var box=document.getElementById('wa-warn');box.hidden=!w.length;
  box.innerHTML=w.length?'<p class="wl-warn-titel">Hinweis</p><ul>'+w.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>'+
    (WA.mehrdeutig?'<p class="wl-hinweis">Laut Artikel «'+wzArtikel('Operatoren und K-Stufen')+'»: «'+esc(WA.mehrdeutig)+'»</p>':''):'';
  var z=[['Aufgabenziel',wa.ziel],['Aufgabenstellung',wa.stellung],['Zeitbudget',wa.zeit.trim()?wa.zeit.trim()+(wa.zeit.trim()==='1'?' Minute':' Minuten'):''],['Sozialform',wzSozText(WA.soz,wa.soz)]];
  var titel=waTitel();
  document.getElementById('wa-ergebnis').innerHTML='<h2 class="wl-erg-titel">'+esc(titel)+'</h2><table class="wl-tab wa-auftrag"><tbody>'+
    z.map(function(r){return '<tr><th scope="row">'+esc(r[0])+'</th><td>'+esc(r[1])+'</td></tr>';}).join('')+'</tbody></table>';
  waErg={text:titel+'\n'+z.map(function(r){return r[0]+': '+r[1];}).join('\n'),
    html:'<h3>'+esc(titel)+'</h3><table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse"><tbody>'+
      z.map(function(r){return '<tr><th style="text-align:left;vertical-align:top">'+esc(r[0])+'</th><td style="vertical-align:top">'+wzZelle(r[1])+'</td></tr>';}).join('')+'</tbody></table>'};
  wzSchreib(WA_KEY,wa);
}
function seiteWerkzeugAufgabe(){
  waGrundlagen();wa=waLaden();waMarke=null;
  var f=WA.frage;
  function etikett(t,k){return esc(t)+(f[k]?'<small>'+esc(f[k])+'</small>':'');}
  var h='<div class="wa-seite"><div class="wz-kopf"><span class="wz-ikon">'+ikon('task')+'</span><div><p class="kicker">Werkzeug</p><h1 class="titel">Aufgabe formulieren</h1></div></div>'+
    '<p class="lead">Wähle die K-Stufe, dann Operator und Aufgabentyp, und formuliere den Arbeitsauftrag mit seinen vier Elementen.</p>'+
    wzSpeicherZeile('wa');
  h+=balken('K-Stufe und Aufgabentyp')+'<div class="chips wa-stufen" id="wa-stufen" role="group" aria-label="K-Stufe">'+
    WA.ops.map(function(o){return '<button type="button" class="chip" data-k="'+esc(o.k)+'" aria-pressed="'+(wa.k===o.k)+'">'+esc(o.titel)+'</button>';}).join('')+'</div>'+
    '<p class="wl-hinweis">Stufen und Operatoren laut Artikel «'+wzArtikel('Operatoren und K-Stufen')+'» (Liste der Aufgabentypen-Palette).</p><div id="wa-stufe"></div>';
  h+=balken('Arbeitsauftrag')+'<p class="wl-hinweis" style="margin-bottom:12px">Die vier Elemente laut Artikel «'+wzArtikel('Arbeitsauftrag formulieren')+'».'+wzUngeprueft('Arbeitsauftrag formulieren',true)+'</p>'+
    '<div class="wa-raster">'+
      '<div class="wl-feld"><label for="wa-nr">Aufgabennummer</label><input id="wa-nr" type="number" min="1" step="1" inputmode="numeric" data-feld="nr" value="'+esc(wa.nr)+'"></div>'+
      '<div class="wl-feld"><label for="wa-zeit">'+etikett('Zeitbudget','zeit')+'</label><input id="wa-zeit" type="number" min="0" step="1" inputmode="numeric" data-feld="zeit" value="'+esc(wa.zeit)+'" aria-describedby="wa-zeit-e"><span class="wl-hinweis" id="wa-zeit-e">in Minuten</span></div>'+
      '<div class="wl-feld"><label for="wa-soz">'+etikett('Sozialform','soz')+'</label><select id="wa-soz" data-feld="soz">'+wzSozOptionen(WA.soz,wa.soz)+'</select></div>'+
    '</div><div class="wa-texte">'+
      '<div class="wl-feld"><label for="wa-ziel">'+etikett('Aufgabenziel','ziel')+'</label><textarea id="wa-ziel" data-feld="ziel" rows="2">'+esc(wa.ziel)+'</textarea></div>'+
      '<div class="wl-feld"><label for="wa-stellung">'+etikett('Aufgabenstellung','stellung')+'</label><textarea id="wa-stellung" data-feld="stellung" rows="4">'+esc(wa.stellung)+'</textarea></div>'+
    '</div><div class="wl-warn" id="wa-warn" role="status" hidden></div>';
  h+=balken('Ergebnis')+'<section class="wa-ergebnis" id="wa-ergebnis" aria-label="Fertiger Auftrag"></section>'+
    '<div class="wl-knoepfe"><button type="button" class="knopf primaer" id="wa-kopieren">Ergebnis kopieren</button><button type="button" class="knopf" id="wa-drucken">Drucken</button></div>'+
    '<p class="wl-meldung" id="wa-meldung" role="status"></p>';
  h+=wzNachlesen(['Arbeitsauftrag formulieren','Operatoren und K-Stufen','Aufgabentypen Übersicht'])+'</div>';
  setze(h,'Aufgabe formulieren');
  waStufeZeichnen();
  wzBindeZuruecksetzen('wa',function(){wzLoesche(WA_KEY);seiteWerkzeugAufgabe();document.getElementById('wa-zurueck').focus();});
  document.getElementById('wa-stufen').addEventListener('click',function(e){var b=e.target.closest('button[data-k]');if(!b)return;
    wa.k=b.dataset.k;if(wa.typ&&!waTypPasst(finde(wa.typ),wa.k))wa.typ='';
    this.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});waStufeZeichnen();waAktualisiere();});
  var seite=S.querySelector('.wa-seite');
  function eingabe(e){var t=e.target;
    if(t.name==='wa-typ'){wa.typ=t.value;waAktualisiere();return;}
    var f=t.dataset.feld;if(!f)return;wa[f]=t.value;waAktualisiere();}
  seite.addEventListener('input',eingabe);seite.addEventListener('change',eingabe);
  var ta=document.getElementById('wa-stellung');
  function merke(){waMarke={s:ta.selectionStart,e:ta.selectionEnd};}
  ['keyup','mouseup','select','blur'].forEach(function(ev){ta.addEventListener(ev,merke);});
  document.getElementById('wa-stufe').addEventListener('click',function(e){
    var b=e.target.closest('button[data-wort]');if(!b)return;
    var v=ta.value,s=waMarke?waMarke.s:0,en=waMarke?waMarke.e:0,vor=v.slice(0,s),nach=v.slice(en),w=b.dataset.wort;
    if(!vor.trim()||/[.!?:]\s*$/.test(vor))w=w.charAt(0).toUpperCase()+w.slice(1); /* Satzanfang gross (E-076) */
    var ein=(vor&&!/\s$/.test(vor)?' ':'')+w+(/^\s/.test(nach)?'':' ');
    ta.value=vor+ein+nach;var pos=(vor+ein).length;ta.focus();ta.setSelectionRange(pos,pos);waMarke={s:pos,e:pos};
    wa.stellung=ta.value;waAktualisiere();
  });
  document.getElementById('wa-kopieren').addEventListener('click',function(){wzKopiere(waErg.text,waErg.html,document.getElementById('wa-meldung'));});
  document.getElementById('wa-drucken').addEventListener('click',function(){window.print();});
  waAktualisiere();
}

/* ---------- Werkzeuge D ---------- */
/* Lernkontrolle bauen und Lektion reflektieren. Fachliche Texte werden zur Laufzeit aus den Artikeln gelesen. */
function wzdLies(k){try{var s=window.localStorage.getItem(k);return s?JSON.parse(s):null;}catch(e){return null;}}
function wzdSchreibe(k,v){try{window.localStorage.setItem(k,JSON.stringify(v));return true;}catch(e){return false;}}
function wzdLoesche(k){try{window.localStorage.removeItem(k);}catch(e){}}
function wzdSpeicherbar(){try{var t='bs-wz-probe';window.localStorage.setItem(t,'1');window.localStorage.removeItem(t);return true;}catch(e){return false;}}
/* Abschnitt eines Artikels, dessen Überschrift mit «anfang» beginnt */
function wzdAbschnitt(n,anfang){
  if(!n)return null;
  var teile=('\n'+n.text).split(/\n## /);
  for(var i=1;i<teile.length;i++){var z=teile[i].indexOf('\n'),kopf=(z<0?teile[i]:teile[i].slice(0,z)).trim();
    if(kopf.indexOf(anfang)===0)return {kopf:kopf,text:(z<0?'':teile[i].slice(z+1)).trim()};}
  return null;
}
function wzdOhneKlammer(k){return String(k).replace(/\s*\([^)]*\)\s*$/,'');}
function wzdHinweis(n){return n&&n.status==='nicht geprüft'?'<p class="wzd-hinweis">nicht am Original geprüft</p>':'';}
function wzdFehlt(was,name){return '<p class="wzd-hinweis">'+esc(was)+' im Artikel «'+esc(name)+'» nicht gefunden.</p>';}
function wzdZahl(s){s=String(s==null?'':s).trim().replace(',','.');if(!/^\d+(\.\d+)?$/.test(s))return NaN;return parseFloat(s);}
function wzdPunkte(x){return String(Math.round(x*100)/100);}
function wzdNachlesen(namen){
  var l=namen.map(finde).filter(Boolean);
  return '<section class="wzd-nachlesen-block">'+balken('Zum Nachlesen')+'<ul class="wzd-nachlesen">'+l.map(function(n){return '<li><a href="#'+n.id+'">'+esc(anzeige(n.name))+'</a></li>';}).join('')+'</ul></section>';
}
function wzdEntwurf(id){return wzSpeicherZeile(id);} /* einheitlich mit Lektion planen (E-076) */
function wzdAktionen(p){
  return '<div class="wzd-aktionen"><button type="button" class="knopf primaer" id="'+p+'-kopieren">Ergebnis kopieren</button><button type="button" class="knopf" id="'+p+'-drucken">Drucken</button><span class="wzd-meldung" id="'+p+'-meldung" role="status" aria-live="polite"></span></div>';
}
function wzdKopiere(text,html,meldung){
  function ok(){meldung.textContent='Ergebnis kopiert.';}
  function fehl(){meldung.textContent='Kopieren hat nicht geklappt. Markiere das Ergebnis und kopiere es von Hand.';}
  function ersatz(){try{var t=document.createElement('textarea');t.value=text;t.setAttribute('readonly','');t.style.position='fixed';t.style.left='-9999px';document.body.appendChild(t);t.select();var r=document.execCommand('copy');document.body.removeChild(t);if(r)ok();else fehl();}catch(e){fehl();}}
  function nurText(){try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(ok,ersatz);return;}}catch(e){}ersatz();}
  meldung.textContent='';
  try{
    if(html&&navigator.clipboard&&navigator.clipboard.write&&window.ClipboardItem){
      navigator.clipboard.write([new window.ClipboardItem({'text/plain':new Blob([text],{type:'text/plain'}),'text/html':new Blob([html],{type:'text/html'})})]).then(ok,nurText);return;}
  }catch(e){}
  nurText();
}
function wzdAbsatz(t){return esc(t).replace(/\n/g,'<br>');}

/* Werkzeug: Lernkontrolle bauen */
var WK_KEY='bs-wz-lernkontrolle';
var WK_RUNDUNG=[['zehntel','Zehntel'],['halbe','halbe Noten'],['keine','keine Rundung (zwei Nachkommastellen)']];
/* Grundformel bei Sockel 60 %, sonst geknickte Skala (Artikel «Notenformel und Sockelwert») */
function wkNote(p,pmax,s){
  if(Math.abs(s-0.6)<1e-12)return p*5/pmax+1;
  if(p<=s*pmax)return 1+3*p/(s*pmax);
  return 4+2*(p-s*pmax)/((1-s)*pmax);
}
function wkRunde(x,r){if(r==='halbe')return Math.round(x*2+1e-9)/2;if(r==='keine')return Math.round(x*100+1e-9)/100;return Math.round(x*10+1e-9)/10;}
function wkZeige(x,r){return wkRunde(x,r).toFixed(r==='keine'?2:1);}
function wkListen(){
  var sp=finde('Schriftliche Lernkontrolle planen'),gc=finde('Checklisten Gütecheck einer Lernkontrolle'),out=[];
  function liste(key,n,name,anfang,zerlege,nummeriert){
    var a=wzdAbschnitt(n,anfang);
    if(!a){out.push({key:key,titel:anfang,fehlt:wzdFehlt('Abschnitt «'+anfang+'»',name),items:[]});return;}
    out.push({key:key,titel:wzdOhneKlammer(a.kopf),n:n,items:zerlege(a.text).filter(Boolean),nummeriert:nummeriert});
  }
  function absatz(t){return t.split(/\n\s*\n/)[0].replace(/\s+/g,' ').trim().replace(/\.$/,'');}
  liste('schritte',sp,'Schriftliche Lernkontrolle planen','Sieben Schritte',function(t){return t.split('\n').map(function(l){var m=l.match(/^\s*\d+\.\s+(.*)$/);return m?m[1].trim():'';});},true);
  liste('pflicht',sp,'Schriftliche Lernkontrolle planen','Pflichtangaben auf dem Dokument',function(t){return absatz(t).split(/,\s+/);},false);
  liste('allgemein',gc,'Checklisten Gütecheck einer Lernkontrolle','C Allgemein',function(t){return absatz(t).split(/;\s*/);},false);
  liste('selbst',gc,'Checklisten Gütecheck einer Lernkontrolle','D Selbstbeurteilung',function(t){return absatz(t).split(/;\s*/);},false);
  return out;
}
function seiteWerkzeugLernkontrolle(){
  var nf=finde('Notenformel und Sockelwert');
  var mS=nf&&String(nf.kurz).match(/Genügendgrenze auf genau (\d+(?:[.,]\d+)?)\s*%/);
  var sockelVor=mS?mS[1].replace(',','.'):'60';
  var grund=nf&&String(nf.kurz).match(/Note = [^;]+/);grund=grund?grund[0].trim():'';
  var knick=wzdAbschnitt(nf,'Anderer Sockel');
  var knickZeilen=knick?knick.text.split('\n').map(function(l){var m=l.match(/^\s*[-*]\s+(.*)$/);return m?m[1].trim():'';}).filter(Boolean):[];
  var alt=wzdLies(WK_KEY)||{};
  var st={pmax:typeof alt.pmax==='string'?alt.pmax:'',sockel:typeof alt.sockel==='string'?alt.sockel:sockelVor,
    rundung:WK_RUNDUNG.some(function(r){return r[0]===alt.rundung;})?alt.rundung:'zehntel',
    punkte:typeof alt.punkte==='string'?alt.punkte:'',haken:(alt.haken&&typeof alt.haken==='object')?alt.haken:{}};
  function sichere(){wzdSchreibe(WK_KEY,st);}
  var listen=wkListen();
  var h='<div class="wzd-seite wk-seite"><div class="wz-kopf"><span class="wz-ikon">'+ikon('exam')+'</span><div><p class="kicker">Werkzeug</p><h1 class="titel">Lernkontrolle bauen</h1></div></div>'+
    '<p class="lead">Rechne die Notenskala für deine Lernkontrolle und hake Schritte, Pflichtangaben und Gütecheck ab.</p>'+wzdEntwurf('wk-reset');
  h+='<section class="wk-rechner">'+balken('Notenrechner')+
    '<div class="wk-eingaben">'+
    '<label class="wzd-feld"><span>Maximale Punkte</span><input id="wk-pmax" type="text" inputmode="decimal" autocomplete="off" value="'+esc(st.pmax)+'"></label>'+
    '<label class="wzd-feld"><span>Sockel in Prozent</span><input id="wk-sockel" type="text" inputmode="decimal" autocomplete="off" value="'+esc(st.sockel)+'"></label>'+
    '<label class="wzd-feld"><span>Rundung</span><select id="wk-rundung">'+WK_RUNDUNG.map(function(r){return '<option value="'+r[0]+'"'+(r[0]===st.rundung?' selected':'')+'>'+esc(r[1])+'</option>';}).join('')+'</select></label>'+
    '</div>'+
    '<h2 class="wzd-unter">Einzelumrechnung</h2>'+
    '<div class="wk-einzel"><label class="wzd-feld"><span>Erreichte Punkte</span><input id="wk-punkte" type="text" inputmode="decimal" autocomplete="off" value="'+esc(st.punkte)+'"></label><p class="wk-einzelnote" id="wk-einzelnote" aria-live="polite"></p></div>'+
    '</section>';
  h+='<section class="wzd-druck">'+balken('Notenskala')+'<div class="wzd-ergebnis" id="wk-ergebnis"></div>'+wzdAktionen('wk')+'</section>';
  listen.forEach(function(l){
    h+='<section class="wk-block">'+balken(l.titel)+(l.fehlt||'')+wzdHinweis(l.n)+
      (l.items.length?'<ul class="wk-liste">'+l.items.map(function(t,i){var k=l.key+'|'+t;
        return '<li><label><input type="checkbox" data-haken="'+esc(k)+'"'+(st.haken[k]?' checked':'')+'><span>'+(l.nummeriert?'<b class="wk-nr">'+(i+1)+'.</b> ':'')+esc(t)+'</span></label></li>';}).join('')+'</ul>':'')+'</section>';
  });
  h+=wzdNachlesen(['Notenformel und Sockelwert','Schriftliche Lernkontrolle planen','Checklisten Gütecheck einer Lernkontrolle','Erwartungshorizont und Punkte','Benotungsregeln und Sechserbremse']);
  h+='</div>';
  setze(h,'Lernkontrolle bauen');

  var ePmax=document.getElementById('wk-pmax'),eSockel=document.getElementById('wk-sockel'),eRund=document.getElementById('wk-rundung'),ePunkte=document.getElementById('wk-punkte');
  var erg=document.getElementById('wk-ergebnis'),einzel=document.getElementById('wk-einzelnote'),kopierKnopf=document.getElementById('wk-kopieren');
  var kopie={text:'',html:''};
  function rundName(){for(var i=0;i<WK_RUNDUNG.length;i++)if(WK_RUNDUNG[i][0]===st.rundung)return WK_RUNDUNG[i][1];return '';}
  function rechne(){
    var pmax=wzdZahl(st.pmax),sp=wzdZahl(st.sockel),r=st.rundung;
    var okP=pmax>0&&pmax<=1000,okS=sp>=1&&sp<=99;
    kopie={text:'',html:''};
    if(!okP||!okS){
      erg.innerHTML='<p class="leer">'+(!okP?'Gib die maximalen Punkte als Zahl über 0 ein (höchstens 1000).':'Der Sockel muss zwischen 1 und 99 Prozent liegen.')+'</p>';
      einzel.textContent='';kopierKnopf.disabled=true;return;
    }
    kopierKnopf.disabled=false;
    var s=sp/100,schritt=pmax<=60?0.5:1,zeilen=[];
    for(var k=0;k*schritt<=pmax+1e-9;k++)zeilen.push(k*schritt);
    if(zeilen[zeilen.length-1]<pmax-1e-9)zeilen.push(pmax);
    var paare=zeilen.map(function(p){return [wzdPunkte(p),wkZeige(wkNote(p,pmax,s),r)];});
    var kopfText='Maximale Punkte '+wzdPunkte(pmax)+' | Sockel '+wzdPunkte(sp)+' % | Rundung: '+rundName();
    var formeln=Math.abs(s-0.6)<1e-12?(grund?['Grundformel: '+grund]:[]):knickZeilen.map(function(z){return 'Geknickte Skala, '+z;});
    var hinweis=nf&&nf.status==='nicht geprüft'?'Richtwert, nicht am Original geprüft':'';
    var h2='<h2 class="wzd-e-titel">Notenskala</h2><p class="wzd-e-kopf">'+esc(kopfText)+'</p>'+
      (formeln.length?'<p class="wk-formel">'+formeln.map(esc).join('<br>')+'</p>':wzdFehlt('Formel','Notenformel und Sockelwert'))+
      (hinweis?'<p class="wzd-hinweis">'+esc(hinweis)+'</p>':'')+'<div class="wk-skala">';
    /* Spalten zu höchstens 21 Zeilen, gleichmässig verteilt */
    var spalten=Math.ceil(paare.length/21),proSpalte=Math.ceil(paare.length/spalten);
    for(var a=0;a<paare.length;a+=proSpalte){
      h2+='<table class="wk-tabelle"><thead><tr><th scope="col">Punkte</th><th scope="col">Note</th></tr></thead><tbody>'+
        paare.slice(a,a+proSpalte).map(function(x){return '<tr><td>'+esc(x[0])+'</td><td>'+esc(x[1])+'</td></tr>';}).join('')+'</tbody></table>';
    }
    erg.innerHTML=h2+'</div>';
    kopie.text='Notenskala\n'+kopfText+'\n'+formeln.join('\n')+(hinweis?'\n'+hinweis:'')+'\n\nPunkte\tNote\n'+paare.map(function(x){return x[0]+'\t'+x[1];}).join('\n');
    kopie.html='<p><b>Notenskala</b></p><p>'+esc(kopfText)+(formeln.length?'<br>'+formeln.map(esc).join('<br>'):'')+(hinweis?'<br>'+esc(hinweis):'')+'</p>'+
      '<table border="1" cellpadding="4" style="border-collapse:collapse"><thead><tr><th>Punkte</th><th>Note</th></tr></thead><tbody>'+
      paare.map(function(x){return '<tr><td>'+esc(x[0])+'</td><td>'+esc(x[1])+'</td></tr>';}).join('')+'</tbody></table>';
    var p=wzdZahl(st.punkte);
    if(String(st.punkte).trim()==='')einzel.textContent='';
    else if(isNaN(p)||p>pmax+1e-9)einzel.textContent='Die erreichten Punkte liegen zwischen 0 und '+wzdPunkte(pmax)+'.';
    else einzel.textContent='Note '+wkZeige(wkNote(p,pmax,s),r);
  }
  function feld(el,name){el.addEventListener('input',function(){st[name]=el.value;sichere();rechne();});}
  feld(ePmax,'pmax');feld(eSockel,'sockel');feld(ePunkte,'punkte');
  eRund.addEventListener('change',function(){st.rundung=eRund.value;sichere();rechne();});
  S.querySelectorAll('input[data-haken]').forEach(function(c){c.addEventListener('change',function(){if(c.checked)st.haken[c.dataset.haken]=true;else delete st.haken[c.dataset.haken];sichere();});});
  kopierKnopf.addEventListener('click',function(){if(kopie.text)wzdKopiere(kopie.text,kopie.html,document.getElementById('wk-meldung'));});
  document.getElementById('wk-drucken').addEventListener('click',function(){window.print();});
  wzBindeZuruecksetzen('wk-reset',function(){wzdLoesche(WK_KEY);seiteWerkzeugLernkontrolle();});
  rechne();
}

/* Werkzeug: Lektion reflektieren */
var WR_KEY='bs-wz-reflexion';
function wrDatum(d){var m=String(d||'').match(/^(\d{4})-(\d{2})-(\d{2})$/);return m?m[3]+'.'+m[2]+'.'+m[1]:String(d||'');}
function seiteWerkzeugReflexion(){
  var hd=finde('Hermeneutischer Dreischritt'),gu=finde('Guter Unterricht nach Meyer');
  var sec=wzdAbschnitt(hd,'Schritte'),schritte=[],hinweise=[];
  if(sec)sec.text.split(/\n\s*\n|\n(?=\s*\d+\.\s)/).forEach(function(b){b=b.trim();if(!b)return;
    var m=b.match(/^\d+\.\s+\*\*([^*:]+):\*\*\s*([\s\S]*)$/);
    if(m)schritte.push({name:m[1].trim(),fragen:m[2].replace(/\s+/g,' ').trim()});else hinweise.push(b.replace(/\s+/g,' '));});
  var warn=wzdAbschnitt(hd,'Warnungen');if(warn&&warn.text)hinweise.push(warn.text.replace(/\s+/g,' '));
  var kat=wzdAbschnitt(gu,'Der Zehnerkatalog'),merkmale=[];
  if(kat)kat.text.split('\n').forEach(function(l){var m=l.match(/^\|\s*(\d+)\s*\|\s*\[\[([^\]|]+)(?:\|[^\]]*)?\]\]\s*\|\s*([^|]+?)\s*\|\s*$/);
    if(m)merkmale.push({nr:+m[1],name:m[2].trim(),funktion:m[3].trim(),n:finde(m[2].trim())});});
  var alt=wzdLies(WR_KEY)||{};
  function obj(x){return x&&typeof x==='object'?x:{};}
  var st={datum:typeof alt.datum==='string'?alt.datum:'',thema:typeof alt.thema==='string'?alt.thema:'',schritte:obj(alt.schritte),merkmale:obj(alt.merkmale)};
  function sichere(){wzdSchreibe(WR_KEY,st);}
  var h='<div class="wzd-seite wr-seite"><div class="wz-kopf"><span class="wz-ikon">'+ikon('loop')+'</span><div><p class="kicker">Werkzeug</p><h1 class="titel">Lektion reflektieren</h1></div></div>'+
    '<p class="lead">Reflektiere eine Lektion im hermeneutischen Dreischritt und halte zu den zehn Merkmalen nach Meyer Stichworte fest.</p>'+wzdEntwurf('wr-reset');
  h+='<div class="wr-kopf"><label class="wzd-feld"><span>Datum</span><input id="wr-datum" type="date" value="'+esc(st.datum)+'"></label>'+
    '<label class="wzd-feld"><span>Lektion oder Thema</span><input id="wr-thema" type="text" autocomplete="off" value="'+esc(st.thema)+'"></label></div>';
  h+='<section class="wr-dreischritt">'+balken('Hermeneutischer Dreischritt')+(hd?wzdHinweis(hd):'')+
    (schritte.length?schritte.map(function(x,i){var id='wr-s-'+i;
      return '<div class="wr-schritt"><div class="wr-schritt-kopf"><span class="wr-nr">'+(i+1)+'</span><label for="'+id+'">'+esc(x.name)+'</label></div>'+
        '<p class="wr-fragen" id="'+id+'-f">'+inline(x.fragen)+'</p><div class="wzd-feld"><textarea id="'+id+'" rows="5" data-schritt="'+esc(x.name)+'" aria-describedby="'+id+'-f">'+esc(st.schritte[x.name]||'')+'</textarea></div></div>';}).join(''):wzdFehlt('Abschnitt «Schritte»','Hermeneutischer Dreischritt'))+
    hinweise.map(function(t){return '<p class="wzd-hinweis">'+inline(t)+'</p>';}).join('')+'</section>';
  var WR_WEG=/^(Die Indikatoren sind|Meyer nennt|Mehr Vielfalt)/,wrSchluss='';
  function wrNurIndikatoren(txt){return String(txt||'').split(/\n\s*\n/).filter(function(p){p=p.trim();if(/^Die Indikatoren sind/.test(p)&&!wrSchluss)wrSchluss=p;return p&&!WR_WEG.test(p);}).join('\n\n');}
  merkmale.forEach(function(m){var x=wzdAbschnitt(m.n,'Indikatoren');if(x)x.text=wrNurIndikatoren(x.text);m.ind=x;});
  h+='<section class="wr-katalog">'+balken('Zehnerkatalog nach Meyer')+(gu?wzdHinweis(gu):'')+(wrSchluss?'<div class="inhalt wr-ind">'+md(wrSchluss)+'</div>':'')+
    (merkmale.length?merkmale.map(function(m,i){var id='wr-m-'+i,ind=m.ind;
      return '<details class="aufklapp wr-merkmal"><summary><span class="wr-m-text"><span class="wr-m-name">'+esc(anzeige(m.name))+'</span><span class="wr-m-funktion">Funktion: '+esc(m.funktion)+'</span></span></summary>'+
        '<div class="wr-m-innen">'+wzdHinweis(m.n)+(ind?'<p class="wr-ind-kopf">'+esc(ind.kopf)+'</p><div class="inhalt wr-ind">'+md(ind.text)+'</div>':wzdFehlt('Abschnitt «Indikatoren»',m.name))+
        '<div class="wzd-feld"><label for="'+id+'">Stichworte</label><textarea id="'+id+'" rows="3" data-merkmal="'+esc(m.name)+'">'+esc(st.merkmale[m.name]||'')+'</textarea></div></div></details>';}).join(''):wzdFehlt('Tabelle «Der Zehnerkatalog»','Guter Unterricht nach Meyer'))+'</section>';
  h+='<section class="wzd-druck">'+balken('Ergebnis')+'<div class="wzd-ergebnis" id="wr-ergebnis"></div>'+wzdAktionen('wr')+'</section>';
  h+=wzdNachlesen(['Hermeneutischer Dreischritt','Guter Unterricht nach Meyer','Sicht- und Tiefenstruktur','Unterricht mit den Lernenden auswerten']);
  h+='</div>';
  setze(h,'Lektion reflektieren');

  var erg=document.getElementById('wr-ergebnis'),kopie={text:'',html:''};
  function zeige(){
    var kopf=[];if(st.datum)kopf.push('Datum: '+wrDatum(st.datum));if(st.thema.trim())kopf.push('Lektion oder Thema: '+st.thema.trim());
    var t=['Lektion reflektieren'],hh='<h2 class="wzd-e-titel">Lektion reflektieren</h2>',ch='<p><b>Lektion reflektieren</b></p>';
    if(kopf.length){t.push(kopf.join(' | '));hh+='<p class="wzd-e-kopf">'+esc(kopf.join(' | '))+'</p>';ch+='<p>'+esc(kopf.join(' | '))+'</p>';}
    schritte.forEach(function(x){var v=(st.schritte[x.name]||'').trim();
      t.push('',x.name,v||'Kein Eintrag.');
      hh+='<h3>'+esc(x.name)+'</h3>'+(v?'<p class="wzd-text">'+esc(v)+'</p>':'<p class="wr-leer">Kein Eintrag.</p>');
      ch+='<h3>'+esc(x.name)+'</h3><p>'+(v?wzdAbsatz(v):'<i>Kein Eintrag.</i>')+'</p>';});
    var voll=merkmale.filter(function(m){return (st.merkmale[m.name]||'').trim();});
    if(voll.length){t.push('','Zehnerkatalog nach Meyer');hh+='<h3>Zehnerkatalog nach Meyer</h3>';ch+='<h3>Zehnerkatalog nach Meyer</h3>';
      voll.forEach(function(m){var v=st.merkmale[m.name].trim();t.push('',anzeige(m.name),v);
        hh+='<h4>'+esc(anzeige(m.name))+'</h4><p class="wzd-text">'+esc(v)+'</p>';ch+='<h4>'+esc(anzeige(m.name))+'</h4><p>'+wzdAbsatz(v)+'</p>';});}
    erg.innerHTML=hh;kopie={text:t.join('\n'),html:ch};
  }
  var eD=document.getElementById('wr-datum'),eT=document.getElementById('wr-thema');
  eD.addEventListener('input',function(){st.datum=eD.value;sichere();zeige();});
  eD.addEventListener('change',function(){st.datum=eD.value;sichere();zeige();});
  eT.addEventListener('input',function(){st.thema=eT.value;sichere();zeige();});
  S.querySelectorAll('textarea[data-schritt]').forEach(function(a){a.addEventListener('input',function(){st.schritte[a.dataset.schritt]=a.value;sichere();zeige();});});
  S.querySelectorAll('textarea[data-merkmal]').forEach(function(a){a.addEventListener('input',function(){st.merkmale[a.dataset.merkmal]=a.value;sichere();zeige();});});
  document.getElementById('wr-kopieren').addEventListener('click',function(){wzdKopiere(kopie.text,kopie.html,document.getElementById('wr-meldung'));});
  document.getElementById('wr-drucken').addEventListener('click',function(){window.print();});
  wzBindeZuruecksetzen('wr-reset',function(){wzdLoesche(WR_KEY);seiteWerkzeugReflexion();});
  zeige();
}

/* ---------- Suche ---------- */
var SUCH=N.map(function(n){return {n:n,t:n.name.toLowerCase(),k:(n.kurz||'').toLowerCase(),b:(n.text||'').toLowerCase()};});
function sucheIn(q){q=q.toLowerCase().trim();if(!q)return [];var w=q.split(/\s+/);
  return SUCH.map(function(s){var sc=0;for(var i=0;i<w.length;i++){var x=w[i],p=0;if(s.t.indexOf(x)>=0)p+=s.t.indexOf(x)===0?14:10;if(s.k.indexOf(x)>=0)p+=4;if(s.b.indexOf(x)>=0)p+=1;if(!p)return null;sc+=p;}return {n:s.n,sc:sc};})
   .filter(Boolean).sort(function(a,b){return b.sc-a.sc||anzeige(a.n.name).localeCompare(anzeige(b.n.name),'de');});}
var letzteSuche='';
function markiere(t,q){var h=esc(t);q.split(/\s+/).filter(Boolean).forEach(function(w){h=h.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi'),'<mark>$1</mark>');});return h;}
function ausschnitt(n,q){var b=n.text.replace(/[#*|>\[\]]/g,' ').replace(/\s+/g,' ');var i=b.toLowerCase().indexOf(q.split(/\s+/)[0].toLowerCase());if(i<0)return '';var a=Math.max(0,i-70);return (a?'… ':'')+b.slice(a,i+130)+' …';}
function seiteSuche(){
  var q=letzteSuche,r=sucheIn(q);
  var h='<p class="kicker">Suche</p><h1 class="titel">«'+esc(q)+'»</h1><p class="lead">'+r.length+' Treffer in Titel, Kurzfassung und Text.</p>';
  h+=r.length?'<ul class="eintraege">'+r.slice(0,150).map(function(x){var n=x.n,a=ausschnitt(n,q);return '<li><a class="e-titel" href="#'+n.id+'">'+markiere(anzeige(n.name),q)+'</a><p>'+markiere(n.kurz,q)+'</p>'+(a?'<div class="meta">'+markiere(a,q)+'</div>':'')+'</li>';}).join('')+'</ul>':'<p class="leer">Nichts gefunden. Versuch ein kürzeres Wort oder den Methodenfinder.</p>';
  setze(h,'Suche');
}

/* ---------- Über dieses Wiki ---------- */
function seiteUeber(){
  var z={};N.forEach(function(n){z[n.status]=(z[n.status]||0)+1;});
  var h='<p class="kicker">Werkstatt Didaktik</p><h1 class="titel">Über dieses Wiki</h1>';
  h+='<p class="lead">Basic Skills ist ein privates didaktisches Nachschlagewerk für den Unterricht in der beruflichen Grundbildung; es entsteht nicht im Auftrag einer Schule. Die Artikel stammen aus der Sammlung «Werkstatt Didaktik»; geändert wird dort, danach wird die Seite neu erzeugt.</p>';
  h+=balken('Was der Status bedeutet')+'<div class="inhalt">'+md(D.statusDef)+'<p>Stand '+esc(D.stand)+': '+STATUS.map(function(s){return esc(s)+' '+(z[s]||0);}).join(' | ')+'.</p><p>Der Status steht in jedem Artikel im Steckbrief rechts.</p></div>';
  h+=balken('Woher die Verbindungen kommen')+'<div class="inhalt"><p>Links, Steckbrief und «Erwähnt in» stammen aus den Artikeln selbst: aus den Feldern, aus «verwandt» und aus den Links im Text. Die Abschnitte «Zusammenhänge» auf der Hauptseite, bei den AVIVA-Phasen, den K-Stufen, den Sozialformen, den Aufgabentypen und beim Prüfen sind aus den verlinkten Artikeln zusammengestellt; jede Aussage nennt den Artikel, aus dem sie stammt.</p>'+
    '<p>Die Felder der Methoden (AVIVA-Phase, K-Stufe, Sozialform) hat ein Skript aus dem Freitext gelesen; im Zweifel gilt der Text des Artikels.</p>'+
    '<p>Das Zeitband liest ein Skript aus dem Feld «Zeitbedarf»: Minutenangaben kommen in die Bänder bis 10, 10 bis 30, 30 bis 60 und über 60 Minuten, eine Spanne in jedes Band, das sie berührt. Angaben in Lektionen, Tagen oder Wochen stehen unter «Lektionen und länger», fehlende unter «keine Angabe», unklare unter «nicht eindeutig».</p></div>';
  h+=balken('Was fehlt')+'<div class="inhalt"><p>Nicht auf der Seite sind interne Arbeitsunterlagen wie Kontrolllisten, Vorlagen und das Archiv.</p></div>';
  setze(h,'Über dieses Wiki');
}

/* ---------- Seitenleiste, Kopfsuche, Router ---------- */
/* Seitenleiste (Etappe 1): nur auf Artikelseiten mit Bereich, nur der eigene Bereich; wird bei jedem Seitenwechsel neu gebaut. */
var GERUEST=document.getElementById('geruest'),LEISTE=document.getElementById('leiste');
function leiste(n){
  if(!n||!n.bereich){GERUEST.classList.add('ohne-leiste');document.getElementById('leiste-inhalt').innerHTML='';return;}
  GERUEST.classList.remove('ohne-leiste');
  var name=bereichName(n.bereich),idx=bereichIndex[n.bereich];
  var liste=N.filter(function(x){return x.bereich===n.bereich&&x!==idx;}).sort(function(a,b){return anzeige(a.name).localeCompare(anzeige(b.name),'de');});
  function li(x){return '<li><a href="#'+x.id+'"'+(x===n?' class="aktiv" aria-current="page"':'')+'>'+esc(anzeige(x.name))+'</a></li>';}
  var h='<p class="l-kopf">'+(idx?'<a href="#'+idx.id+'"'+(idx===n?' class="aktiv" aria-current="page"':'')+'>'+esc(name)+'</a>':esc(name))+'</p>';
  if(liste.length>60){
    var i=liste.indexOf(n);
    h+='<p class="l-finder"><a href="#finder">Methodenfinder</a></p>';
    h+='<ul>'+liste.slice(Math.max(0,i-5),i+6).map(li).join('')+'</ul>';
  } else h+='<ul>'+liste.map(li).join('')+'</ul>';
  document.getElementById('leiste-titel').textContent=name;
  document.getElementById('leiste-inhalt').innerHTML=h;
  LEISTE.open=window.innerWidth>860;
}
window.addEventListener('resize',function(){if(window.innerWidth>860)LEISTE.open=true;});
/* Suchfeld mit Vorschlagsliste: Kopfzeile, aufgeklapptes Handy-Suchfeld und grosses Suchfeld der Hauptseite */
function bindeSuche(inp,ul){
  if(!inp||!ul)return;var akt=-1;
  function zeige(){var q=inp.value.trim();if(q.length<2){ul.hidden=true;return;}var r=sucheIn(q).slice(0,8);akt=-1;
    ul.innerHTML=r.map(function(x){return '<li><a href="#'+x.n.id+'">'+markiere(anzeige(x.n.name),q)+'<small>'+esc(TYP[x.n.typ]||'')+(x.n.bereich?' | '+esc(bereichName(x.n.bereich)):'')+'</small></a></li>';}).join('')+'<li><a href="#suche" data-alle="1">Alle Treffer für «'+esc(q)+'» anzeigen</a></li>';ul.hidden=false;}
  inp.addEventListener('input',zeige);
  inp.addEventListener('keydown',function(e){var a=ul.querySelectorAll('a');
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){if(ul.hidden)return;e.preventDefault();akt=(akt+(e.key==='ArrowDown'?1:-1)+a.length)%a.length;a.forEach(function(x,i){x.classList.toggle('aktiv',i===akt);});}
    else if(e.key==='Enter'){e.preventDefault();if(akt>=0&&a[akt]){a[akt].click();}else{letzteSuche=inp.value.trim();if(letzteSuche){ul.hidden=true;if(location.hash==='#suche')route();else location.hash='suche';}}}
    else if(e.key==='Escape'){ul.hidden=true;}});
  ul.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;if(a.dataset.alle){letzteSuche=inp.value.trim();if(location.hash==='#suche'){e.preventDefault();route();}}ul.hidden=true;});
}
function kopfsuche(){
  bindeSuche(document.getElementById('suche'),document.getElementById('vorschlag'));
  bindeSuche(document.getElementById('suche-mobil'),document.getElementById('vorschlag-mobil'));
  document.addEventListener('click',function(e){var f=e.target.closest('.suchfeld');document.querySelectorAll('.vorschlag').forEach(function(u){if(!f||!f.contains(u))u.hidden=true;});});
}
/* Kopfzeile: beim Scrollen niedriger; unter 820 px Suche und Menü aufklappbar, nur eines offen */
var KOPF=document.getElementById('kopf');
var KLAPPEN=[['k-suche','klappe-suche','Suche'],['k-menue','klappe-menue','Menü']];
function schliesseKlappen(ausser){KLAPPEN.forEach(function(p){if(p[0]===ausser)return;var b=document.getElementById(p[0]);b.setAttribute('aria-expanded','false');b.setAttribute('aria-label',p[2]+' öffnen');document.getElementById(p[1]).hidden=true;});}
function kopfzeile(){
  function schrumpfe(){KOPF.classList.toggle('schmal',window.scrollY>8);}
  window.addEventListener('scroll',schrumpfe,{passive:true});schrumpfe();
  KLAPPEN.forEach(function(p){
    var b=document.getElementById(p[0]),k=document.getElementById(p[1]);
    b.addEventListener('click',function(){
      var auf=b.getAttribute('aria-expanded')!=='true';schliesseKlappen(p[0]);
      b.setAttribute('aria-expanded',String(auf));b.setAttribute('aria-label',p[2]+(auf?' schliessen':' öffnen'));k.hidden=!auf;
      if(auf&&p[0]==='k-suche')document.getElementById('suche-mobil').focus();
    });
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape')schliesseKlappen();});
  window.matchMedia('(min-width:821px)').addEventListener('change',function(m){if(m.matches)schliesseKlappen();});
}
document.addEventListener('click',function(e){var a=e.target.closest('a[data-preset]');if(!a)return;var p=a.dataset.preset.split('|');wahl={};if(p[0])wahl[p[0]]=[p[1]];finderText='';if(p[0]&&FG_SICHTBAR.indexOf(p[0])<0)mehrOffen=true;});
function route(){
  var h=(location.hash||'#h').slice(1);
  document.querySelectorAll('.hauptnav a').forEach(function(a){var an=a.dataset.nav===h;a.classList.toggle('aktiv',an);if(an)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  schliesseKlappen();
  leiste(h&&h!=='h'&&!RESERVIERT[h]&&nachId[h]?nachId[h]:null);
  if(h==='h'||!h)return seiteHaupt();
  if(h==='finder')return seiteFinder();
  if(h==='werkzeug-lektion'){leiste(null);return seiteWerkzeugLektion();}
  if(h==='werkzeug-aufgabe'){leiste(null);return seiteWerkzeugAufgabe();}
  if(h==='werkzeug-lernkontrolle'){leiste(null);return seiteWerkzeugLernkontrolle();}
  if(h==='werkzeug-reflexion'){leiste(null);return seiteWerkzeugReflexion();}
  if(h==='ueber')return seiteUeber();
  if(h==='suche'){if(!letzteSuche)return seiteHaupt();return seiteSuche();}
  if(nachId[h])return seiteNotiz(nachId[h]);
  if(katAus[h])return seiteKat(h);
  seiteHaupt();
}
document.getElementById('fuss').innerHTML='<span>Basic Skills</span><span>Stand '+esc(D.stand)+'</span><span>'+N.length+' Artikel</span>';
kopfzeile();kopfsuche();
window.addEventListener('hashchange',route);route();
})();
</script>
'''

if __name__ == '__main__':
    sys.exit(main(sys.argv))
