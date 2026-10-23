#!/usr/bin/env python3
"""Vergleicht die Skill-Abschrift der Aufgabentypen-Palette mit dem Original-PDF.
Exit 0 = deckungsgleich bei Operatoren und K-Stufen je Typ, 1 = Abweichung, 2 = Datei fehlt."""
import re, sys, subprocess, tempfile, os

PDF = os.path.expanduser("~/Desktop/Aufgabentypen-Palette_FaBe.pdf")
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
MD  = _plugin_unterrichten() + "/skills/aufgabentypen/references/aufgabentypen-palette_wortgetreu.md"
PDF = os.environ.get("PALETTE_PDF", PDF)
MD  = os.environ.get("PALETTE_MD", MD)

def norm(s):
    s = s.replace("’","'").replace("‘","'").replace("„",'"').replace("“",'"')
    s = s.replace("–","-").replace("—","-").replace("−","-")
    return " ".join(s.split()).strip(" .")

def kstufe(s):
    """Nur die K-Angabe, Zusaetze in Klammern oder nach Komma weg."""
    s = norm(s)
    s = re.split(r'[,(]', s)[0]
    return s.strip()

def pdftext(p):
    out = subprocess.run(["pdftotext","-layout",p,"-"],capture_output=True,text=True)
    if out.returncode:
        print("Pruefung nicht lauffaehig: pdftotext fehlgeschlagen: "+out.stderr); sys.exit(2)
    t = out.stdout
    # Kopf- und Fusszeilen des PDF entfernen, sie sind kein Inhalt
    t = re.sub(r'^\s*Seite \d+ von \d+\s*$', '', t, flags=re.M)
    t = re.sub(r'^\s*Aufgabentypen-Palette FaBe-Unterricht\s*$', '', t, flags=re.M)
    t = t.replace('\x0c','\n')
    return t

def parse(text, md):
    """-> {nr: (kstufe, operatoren)}"""
    res = {}
    head = r'^#{0,3}\s*Aufgabentyp\s+(\d+):\s*(.+?)\s*\((.+?)\)\s*$'
    lines = text.split("\n")
    idx = [(i,m) for i,l in enumerate(lines) for m in [re.match(head,l.strip())] if m]
    for k,(i,m) in enumerate(idx):
        nr = int(m.group(1)); kst = kstufe(m.group(3))
        end = idx[k+1][0] if k+1 < len(idx) else len(lines)
        body = "\n".join(lines[i:end])
        om = re.search(r'Lernziel-Operatoren:\*{0,2}\s*(.+?)(?=\s*(?:\*\*)?Beispielaufgabe)', body, re.S)
        ops = norm(om.group(1)) if om else "<KEINE OPERATORENZEILE>"
        res[nr] = (kst, ops)
    return res

pdf_roh = pdftext(PDF)
if not os.path.isfile(MD):
    print(f"Pruefung nicht lauffaehig: Abschrift fehlt: {MD}"); sys.exit(2)
md_roh  = open(MD, encoding="utf-8").read()
p = parse(pdf_roh, False)
m = parse(md_roh, True)

befunde = []

# Rahmen der Abschrift: Stufenband der Bloom-Uebersicht und Einschraenkungsabsatz
def band(t):
    mm = re.search(r'Bloom-Taxonomie: Kurz\u00fcbersicht \((K\d\s*[\u2013-]\s*K\d)\)', t)
    return norm(mm.group(1)) if mm else "<fehlt>"
if band(pdf_roh) != band(md_roh):
    befunde.append(f"Bloom-Uebersicht: Stufenband verschieden.\n"
                   f"    Original: {band(pdf_roh)}\n    Abschrift: {band(md_roh)}")
pdf_k6 = bool(re.search(r'^\s*K6\s+Bewerten', pdf_roh, re.M))
md_k6  = bool(re.search(r'^\|\s*K6\s*\|', md_roh, re.M))
if pdf_k6 != md_k6:
    befunde.append(f"Bloom-Uebersicht: K6-Zeile im Original {'vorhanden' if pdf_k6 else 'nicht vorhanden'}, "
                   f"in der Abschrift {'vorhanden' if md_k6 else 'nicht vorhanden'}")
if ("Wichtige Einschr" in pdf_roh) and ("Wichtige Einschr" not in md_roh):
    befunde.append("Absatz 'Wichtige Einschraenkung' (K6 wird in FaBe praktisch nie "
                   "erreicht) steht im Original, fehlt in der Abschrift")
if sorted(p) != sorted(m):
    befunde.append(f"Typennummern verschieden. PDF={sorted(p)} MD={sorted(m)}")
for nr in sorted(set(p) | set(m)):
    a = p.get(nr, ("<fehlt>","<fehlt>")); b = m.get(nr, ("<fehlt>","<fehlt>"))
    if a[1] != b[1]:
        befunde.append(f"Typ {nr} Operatoren:\n    Original: {a[1]}\n    Abschrift: {b[1]}")
    if a[0] != b[0]:
        befunde.append(f"Typ {nr} K-Stufe:\n    Original: {a[0]}\n    Abschrift: {b[0]}")

print(f"Typen im Original: {len(p)} | Typen in der Abschrift: {len(m)}")
for b in befunde: print("BEFUND:", b)
print(f"Befunde: {len(befunde)}")
sys.exit(1 if befunde else 0)
