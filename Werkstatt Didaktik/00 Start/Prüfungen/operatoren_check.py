#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft die Notizen in "40 Aufgaben und Operatoren" gegen die Aufgabentypen-Palette.

Meldet:
  LUECKE    Die Notiz nennt einen Operator, den die Operatorenliste der Palette nicht kennt.
  KONFLIKT  Die Liste kennt den Operator, ordnet ihn aber einer anderen K-Stufe zu
            als die K-Stufe der Notiz.
  ABSCHRIFT Das Frontmatter weicht vom Original-PDF der Palette ab
            (Operatoren, K-Stufe oder Nummer).
  TEXT      Die Zeile "Operatoren laut Palette:" im Fliesstext weicht vom
            Frontmatter-Feld "operatoren" ab.

Aufruf:  python3 operatoren_check.py [--ordner PFAD] [--ausnahmen DATEI]
Exit  0  keine Befunde (ausser den in der Ausnahmedatei quittierten)
Exit  1  Befunde vorhanden
Exit  2  Pruefung selbst nicht lauffaehig (Datei fehlt, Parsen gescheitert)

Die Ausnahmedatei ist eine JSON-Liste von Objekten
{"notiz": "...", "art": "...", "operator": "...", "entscheid": "E-0xx"}.
Ohne sie meldet die Pruefung den Istzustand, also auch die offenen Punkte von B-004.
"""
import argparse, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
try:
    from quellen import alles
except Exception as e:                                    # pragma: no cover
    print(f"Pruefung nicht lauffaehig: quellen.py fehlt oder bricht ab: {e}")
    sys.exit(2)

VAULT_STD = os.path.expanduser("~/Desktop/BFS/Werkstatt Didaktik/40 Aufgaben und Operatoren")

def frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m: return {}
    fm, feld = {}, None
    for line in m.group(1).split("\n"):
        if re.match(r'^\s*-\s', line) and feld:
            fm[feld].append(line.strip()[1:].strip().strip('"\''))
        else:
            mm = re.match(r'^([a-z_]+):\s*(.*)$', line)
            if mm:
                feld, wert = mm.group(1), mm.group(2).strip()
                if wert in ("[]", "{}", "~", "null"):
                    fm[feld] = []                       # leere YAML-Liste, kein Wert "[]"
                else:
                    fm[feld] = [wert.strip('"\'')] if wert else []
    return fm

def kstufen(werte):
    """K-Stufen einer Angabe als Menge. Spannen wie "K2-K4" werden aufgeloest,
    damit die Schreibweise des Originals und die YAML-Aufzaehlung der Notiz
    vergleichbar sind."""
    out = set()
    for w in werte:
        t = str(w)
        for m in re.finditer(r'K([1-6])\s*[\u2013\u2014-]\s*K([1-6])', t):
            out |= {f"K{i}" for i in range(int(m.group(1)), int(m.group(2))+1)}
        t = re.sub(r'K[1-6]\s*[\u2013\u2014-]\s*K[1-6]', ' ', t)
        for m in re.finditer(r'K([1-6])', t):
            out.add("K"+m.group(1))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ordner", default=VAULT_STD)
    ap.add_argument("--ausnahmen", default=None)
    a = ap.parse_args()

    if not os.path.isdir(a.ordner):
        print(f"Pruefung nicht lauffaehig: Ordner fehlt: {a.ordner}")
        return 2

    quellen = alles()
    liste = {}                               # Operator -> {K-Stufen} laut Palette-Liste
    for k, ops in quellen["palette_aggregat"].items():
        for o in ops: liste.setdefault(o, set()).add(k)
    if not liste:
        print("Pruefung nicht lauffaehig: Operatorenliste der Palette leer geparst.")
        return 2
    original = quellen["palette_typen"]      # Nr -> {titel, kstufe, ops}
    if len(original) != 19:
        print(f"Pruefung nicht lauffaehig: Original-PDF ergab {len(original)} Typen, erwartet 19.")
        return 2

    quittiert = set()
    if a.ausnahmen:
        if not os.path.isfile(a.ausnahmen):
            print(f"Pruefung nicht lauffaehig: Ausnahmedatei fehlt: {a.ausnahmen}")
            return 2
        for e in json.load(open(a.ausnahmen, encoding="utf-8")):
            quittiert.add((e.get("notiz",""), e.get("art",""), e.get("operator","")))

    befunde, geprueft = [], 0
    def melde(notiz, art, operator, text):
        if (notiz, art, operator) in quittiert: return
        befunde.append((art, notiz, operator, text))

    for name in sorted(os.listdir(a.ordner)):
        if not name.endswith(".md"): continue
        text = open(os.path.join(a.ordner, name), encoding="utf-8").read()
        fm = frontmatter(text)
        ops = [o.lower() for o in fm.get("operatoren", []) if o]
        if not ops: continue
        geprueft += 1
        stufen = kstufen(fm.get("k_stufe", []))

        for o in ops:
            if o not in liste:
                melde(name, "LUECKE", o,
                      "Operatorenliste der Palette kennt diesen Operator nicht")
            elif stufen and not (liste[o] & stufen):
                melde(name, "KONFLIKT", o,
                      f'Notiz {"/".join(sorted(stufen))}, Liste {"/".join(sorted(liste[o]))}')

        # Frontmatter gegen Original-PDF
        nr = fm.get("nr", [None])[0]
        if nr and str(nr).isdigit() and int(nr) in original:
            orig = original[int(nr)]
            if orig["ops"] and ops != [o.lower() for o in orig["ops"]]:
                melde(name, "ABSCHRIFT", "operatoren",
                      f'Original {", ".join(orig["ops"])} | Notiz {", ".join(ops)}')
            ostufen = kstufen([orig["kstufe"]])
            if ostufen and stufen and ostufen != stufen:
                melde(name, "ABSCHRIFT", "k_stufe",
                      f'Original {orig["kstufe"]} | Notiz {"/".join(sorted(stufen))}')
        elif nr:
            melde(name, "ABSCHRIFT", "nr", f"Nummer {nr} kommt im Original-PDF nicht vor")

        # Fliesstext gegen Frontmatter
        tm = re.search(r'\*\*Operatoren laut Palette:\*\*\s*(.+)', text)
        if tm and not tm.group(1).strip().startswith("("):
            # Ein Klammerhinweis wie "(je nach Posten unterschiedlich)" steht so
            # im Original und ist kein Operator; dann gibt es nichts zu vergleichen.
            im_text = [" ".join(t.split()).lower()
                       for t in tm.group(1).split(",") if t.strip()]
            if im_text != ops:
                melde(name, "TEXT", "operatoren",
                      f'Fliesstext {", ".join(im_text)} | Frontmatter {", ".join(ops)}')

    print(f"Geprueft: {geprueft} Notizen mit Feld 'operatoren' in {a.ordner}")
    if a.ausnahmen: print(f"Ausnahmedatei: {a.ausnahmen} ({len(quittiert)} quittierte Faelle)")
    for art, notiz, op, txt in sorted(befunde):
        print(f"{art:9s} {notiz:52s} {op:18s} {txt}")
    print(f"Befunde: {len(befunde)}")
    return 1 if befunde else 0

if __name__ == "__main__":
    sys.exit(main())
