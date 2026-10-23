#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liest die Operatorenzuordnungen aller Quellen aus den Originaldateien.
Nichts ist aus dem Gedaechtnis ergaenzt. Jede Quelle wird geparst; wo eine
Quelle keine Liste fuehrt, wird das wortgetreue Zitat mitgegeben."""
import os, re, subprocess, sys, json

HOME = os.path.expanduser("~")

def _plugin_unterrichten():
    """Neuster installierter Stand des Plugins unterrichten. Der Ordnername
    (unterrichten, unterrichten~g3, ...) wechselt bei jedem Sync (E-166)."""
    import glob as _g, json as _j
    best = None
    for d in _g.glob(os.path.expanduser("~/.claude/plugins/synced/*/unterrichten*/")):
        try:
            v = _j.load(open(os.path.join(d, ".claude-plugin", "plugin.json"), encoding="utf-8"))["version"]
            k = tuple(int(x) for x in v.split("."))
        except Exception:
            continue
        if best is None or k > best[0]:
            best = (k, d.rstrip("/"))
    return best[1] if best else os.path.expanduser("~/.claude/plugins/synced/unterrichten-nicht-gefunden")
SKILL = _plugin_unterrichten() + "/skills/aufgabentypen"
TRESOR = HOME + "/Desktop/BFS/BFS"
KORPUS = HOME + "/Desktop/BFS/Master-Korpus"
PDF_PALETTE = HOME + "/Desktop/Aufgabentypen-Palette_FaBe.pdf"
PDF_LUL = KORPUS + "/Mentor/Lehren und Lernen _E-Book_4 Unterrichtsplanung.pdf"
PDF_LK1 = HOME + "/Desktop/BFS/EHB/Lehren kompakt I (Print inkl. E-Book Edubase) - Ruth Meyer.pdf"

SOFT = "­"      # weiches Trennzeichen
HYPH = "‐"      # Bindestrich-Variante

def pdftext(p, first=None, last=None):
    cmd = ["pdftotext", "-layout"]
    if first: cmd += ["-f", str(first)]
    if last:  cmd += ["-l", str(last)]
    cmd += [p, "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(f"Pruefung nicht lauffaehig: pdftotext fehlgeschlagen fuer {p}: {r.stderr}"); sys.exit(2)
    return r.stdout

# Woerter, die pdftotext im Satzspiegel mit eingeschobenem Leerzeichen rendert.
# Jede Zeile ist am Original nachgelesen, keine Vermutung.
PDF_RISSE = {
    "umsch reiben": "umschreiben",      # Lehren kompakt 1, S. 70, Stufe K2
    "er läutern": "erläutern",          # Lehren kompakt 1, S. 70, Stufe K5
    "über prüfen": "überprüfen",          # Lehren kompakt 1, S. 70, Stufe K6
    "ih re": "ihre",
}

def entsilben(t):
    """Weiche Trennzeichen, Trennstriche am Zeilenende und Satzspiegel-Risse zusammenziehen."""
    # Reihenfolge wichtig: weiches Trennzeichen AM ZEILENENDE samt Umbruch
    # zusammenziehen, erst danach die restlichen weichen Trennzeichen loeschen.
    t = re.sub(SOFT + r'\s*\n\s*', '', t)
    t = t.replace(SOFT, "").replace(HYPH, "-")
    for falsch, richtig in PDF_RISSE.items():
        t = t.replace(falsch, richtig)
    t = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', t)   # Trennung ueber Zeilenumbruch
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)        # Trennung nach Layout-Glaettung
    return t

# Mehrwortige Aufzaehlungsglieder, die nicht an Kommas zerlegt werden duerfen.
GANZ = {"Kennen von Zusammenhängen, Gesetzmässigkeiten und Anwendungen": "kennen"}

def split_ops(s):
    s = re.sub(r'\(.*?\)', ' ', s.replace(SOFT, ""))
    fest = []
    for phrase, ersatz in GANZ.items():
        if phrase.lower() in s.lower():
            s = re.sub(re.escape(phrase), " ", s, flags=re.I)
            fest.append(ersatz)
    out = []
    for t in re.split(r'[,;/]| und | bzw\. ', s):
        t = " ".join(t.split()).strip(" .:»«’'")
        if t and len(t) >= 3:
            out.append(t.lower())
    return fest + out

# ---------- A  Palette: Aggregattabelle des Skills ----------
def palette_aggregat():
    p = SKILL + "/references/k-stufen-operatoren.md"
    if not os.path.isfile(p):
        print(f"Pruefung nicht lauffaehig: Skilldatei fehlt: {p}"); sys.exit(2)
    txt = open(p, encoding="utf-8").read()
    return {m.group(1): split_ops(m.group(2))
            for m in re.finditer(r'^\|\s*\*\*(K[1-6])\s*[–-][^|]*\*\*\s*\|\s*([^|]+)\|', txt, re.M)}

# ---------- A2 Palette: Operatoren je Aufgabentyp, Original-PDF ----------
def palette_typen():
    t = pdftext(PDF_PALETTE)
    t = re.sub(r'^\s*Seite \d+ von \d+\s*$', '', t, flags=re.M)
    t = re.sub(r'^\s*Aufgabentypen-Palette FaBe-Unterricht\s*$', '', t, flags=re.M)
    lines = entsilben(t).split("\n")
    idx = [(i, m) for i, l in enumerate(lines)
           for m in [re.match(r'^Aufgabentyp\s+(\d+):\s*(.+?)\s*\((.+?)\)\s*$', l.strip())] if m]
    res = {}
    for k, (i, m) in enumerate(idx):
        end = idx[k+1][0] if k+1 < len(idx) else len(lines)
        body = "\n".join(lines[i:end])
        om = re.search(r'Lernziel-Operatoren:\s*(.+?)(?=\s*Beispielaufgabe)', body, re.S)
        roh = " ".join(om.group(1).split()) if om else ""
        ops = [] if roh.startswith("(") else split_ops(roh)
        res[int(m.group(1))] = {"titel": m.group(2).strip(), "kstufe": m.group(3).strip(),
                                "ops": ops, "roh": roh}
    return res

# ---------- B  SAVOIRSOCIAL, Tresornotiz ----------
def savoirsocial():
    txt = open(TRESOR + "/70 Rahmenvorgaben/Operatoren und Punkte BK-Prüfung.md",
               encoding="utf-8").read()
    res = {}
    for m in re.finditer(r'^\|\s*(Wissensfrage|Verständnisfrage|Anwendungsfrage|Analysefrage)'
                         r'\s*\|\s*([^|]+)\|\s*([^|]*)\|\s*([^|]*)\|', txt, re.M):
        for op in split_ops(m.group(2)):
            res[op] = {"fragetyp": m.group(1), "punkte": m.group(4).strip()}
    return res

# ---------- C  Lehren kompakt 1, S. 70, Original ----------
# Das Buch fuehrt auf S. 70 KEINE Operatorenliste, sondern je Stufe eine Klammer-
# Umschreibung. Die darin genannten Taetigkeitswoerter werden ausgelesen;
# Nominalisierungen tragen ein * und werden nicht stillschweigend gebeugt.
LK1_NOMEN = {"anwendung": "anwenden*", "lösung": "lösen*", "analyse": "analysieren*",
             "kenntnis": None, "wissen": None, "synthese": None, "evaluation": None,
             "verstehen": "verstehen"}
LK1_STOPP = {"eigenen", "worten", "kriterien", "formeln", "einsichten", "begriffen",
             "tatsachen", "erlebnissen", "elementen", "modellen", "problems",
             "sachverhalte", "begriffe", "modelle", "situation", "elemente",
             "praktischen", "verschiedenen", "neue", "reale", "anhand",
             "kenntnissen", "kenntnis"}
def lehren_kompakt1():
    t = re.sub(r'\s+', ' ', entsilben(pdftext(PDF_LK1, 70, 70)))
    res, zitate = {}, {}
    for m in re.finditer(r'Stufe (K[1-6]):\s*([^(]+)\(([^)]*)\)', t):
        k, inner = m.group(1), m.group(3)
        zitate[k] = f"Stufe {k}: {' '.join(m.group(2).split())} ({' '.join(inner.split())})"
        ops = []
        for w in re.findall(r'[A-Za-zÄÖÜäöüß]{4,}', inner):
            wl = w.lower()
            if wl in LK1_NOMEN:
                if LK1_NOMEN[wl]: ops.append(LK1_NOMEN[wl])
            elif wl.endswith(("en", "ern")) and wl not in LK1_STOPP:
                ops.append(wl)
        res[k] = sorted(set(ops))
    return res, zitate

# ---------- D  Lehren und Lernen, Kap. 4, Original ----------
def lehren_und_lernen():
    t = pdftext(PDF_LUL)
    t = re.sub(r'©[^\n]*\n', '\n', t)                                     # Urheberrechtszeile
    t = re.sub(r'^\s*\d{1,3}\s+Lehren und Lernen\s*$', '', t, flags=re.M)      # Kopfzeile links
    t = re.sub(r'^\s*4 Unterrichtsplanung\s+\d{1,3}\s*$', '', t, flags=re.M)   # Kopfzeile rechts
    t = re.sub(r'\s+', ' ', entsilben(t))
    res, zitate = {}, {}
    for m in re.finditer(r'K([1-6])\s*:.*?Beschreibungen des Endverhaltens sind zum Beispiel\s*:\s*'
                         r'(.*?)(?=\s*K[1-6]\s*:|\s*Vieles spricht daf|$)', t):
        liste = " ".join(m.group(2).split())
        zitate["K"+m.group(1)] = liste
        res["K"+m.group(1)] = split_ops(liste)
    return res, zitate

# ---------- E  Master-Korpus Referenz 03 ----------
KORPUS_FLEX = {  # 3. Person -> Infinitiv; nur Formen, die die Quelle selbst eindeutig macht
 "nennt": "nennen", "zählt auf": "aufzählen", "gibt wieder": "wiedergeben",
 "bezeichnet": "benennen", "ordnet zu": "zuordnen", "definiert": "definieren",
 "erklärt": "erklären", "erläutert": "erläutern", "beschreibt": "beschreiben",
 "fasst zusammen": "zusammenfassen", "grenzt ab": "abgrenzen", "wendet an": "anwenden",
 "setzt um": "umsetzen", "plant nach vorgabe": "planen", "formuliert": "formulieren",
 "gestaltet nach kriterien": "gestalten", "führt aus": "ausführen",
 "analysiert": "analysieren", "vergleicht kriteriengeleitet": "vergleichen",
 "untersucht": "untersuchen", "deckt beziehungen auf": "beziehungen aufdecken",
 "diagnostiziert": "diagnostizieren", "gliedert": "gliedern", "entwickelt": "entwickeln",
 "entwirft": "entwerfen", "kombiniert zu einem ganzen": "kombinieren",
 "konzipiert": "konzipieren", "konstruiert": "konstruieren",
}
def master_korpus():
    txt = open(KORPUS + "/03_taxonomie-operatoren.md", encoding="utf-8").read()
    res, roh = {}, {}
    for m in re.finditer(r'^- \*\*(K[1-6])\*\*:\s*(.+)$', txt, re.M):
        k = m.group(1); roh[k] = m.group(2).strip()
        ops = []
        for t in m.group(2).split(","):
            t = " ".join(re.sub(r'\(.*?\)', '', t).split()).strip(" .").lower()
            if t: ops.append(KORPUS_FLEX.get(t, t))
        res[k] = ops
    return res, roh

# ---------- F  Davids 4-Schritt-Bauplan ----------
# Als Datei nicht auffindbar (Vault, Tresor, Master-Korpus, Skills, Desktop durchsucht).
# Gefuehrt werden nur die drei Operatoren, die David im Auftrag vom 07.10.2026 nennt.
BAUPLAN = ["übertragen", "berechnen", "charakterisieren"]
BAUPLAN_STATUS = ("nicht geprüft: keine Quelldatei gefunden; Angabe stammt aus Davids "
                  "Auftrag vom 07.10.2026, ohne K-Stufen-Zuordnung")

def alles():
    lk1, lk1z = lehren_kompakt1()
    lul, lulz = lehren_und_lernen()
    mk, mkroh = master_korpus()
    return {"palette_aggregat": palette_aggregat(),
            "palette_typen": palette_typen(),
            "savoirsocial": savoirsocial(),
            "lehren_kompakt1": lk1, "lehren_kompakt1_zitate": lk1z,
            "lehren_und_lernen": lul, "lehren_und_lernen_zitate": lulz,
            "master_korpus": mk, "master_korpus_roh": mkroh,
            "bauplan": BAUPLAN, "bauplan_status": BAUPLAN_STATUS}

if __name__ == "__main__":
    print(json.dumps(alles(), ensure_ascii=False, indent=1))
