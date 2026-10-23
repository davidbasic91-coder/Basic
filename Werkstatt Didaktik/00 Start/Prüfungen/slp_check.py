#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft, ob die Lernziele des Schullehrplans hoeher zielen als die
BFS-Leistungsziele des Bildungsplans, die sie bedienen.

Hintergrund: Die Arbeitsdossiers paaren SLP-Lernzieltexte mit den K-Stufen der
BiP-Leistungsziele. Zielt der SLP-Text hoeher, entsteht ein Konflikt, der sich
in den Einstiegsfragen niederschlaegt.

Die Operatorentabelle wird NICHT hier gefuehrt, sondern aus den vier belegten
Quellen (Paket 1, quellen.py) abgeleitet. Ein Verb zaehlt nur, wenn alle
Quellen, die es kennen, es gleich einstufen; sonst gilt es als mehrdeutig und
bleibt aussen vor (siehe Befund B-056).

Exit 0 kein Fall, 1 Faelle gefunden, 2 nicht lauffaehig.
"""
import json, os, re, sys

# quellen.py liegt im selben Ordner; der Pfad nach ~/Desktop/Paket1-Operatoren
# bleibt als Rueckfall, solange dort die Arbeitsfassung steht.
PAKET1 = os.path.dirname(os.path.abspath(__file__))
RUECKFALL = os.path.expanduser("~/Desktop/Paket1-Operatoren")
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
B = os.environ.get("SLP_BASIS", _plugin_unterrichten() + "/skills")

def fehl(m):
    print(f"Pruefung nicht lauffaehig: {m}"); sys.exit(2)

ANZAHL_QUELLEN = {}

def operatoren():
    """-> ({Verb: Stufe} eindeutige, {Verb: [Stufen]} mehrdeutige)"""
    sys.path.insert(0, PAKET1)
    sys.path.insert(1, RUECKFALL)
    try:
        from quellen import alles
    except Exception as e:
        fehl(f"quellen.py nicht ladbar (gesucht in {PAKET1} und {RUECKFALL}): {e}")
    q = alles()
    je = {}
    for key in ("palette_aggregat", "lehren_kompakt1", "lehren_und_lernen", "master_korpus"):
        for k, ops in q[key].items():
            for o in ops:
                je.setdefault(o.rstrip("*"), set()).add(int(k[1]))
    eindeutig = {v: next(iter(s)) for v, s in je.items() if len(s) == 1}
    mehrdeutig = {v: sorted(s) for v, s in je.items() if len(s) > 1}
    # Wie viele der vier Quellen kennen das Verb? Ein Verb, das nur eine Quelle
    # fuehrt, traegt einen schwaecheren Befund als eines, das drei fuehren.
    global ANZAHL_QUELLEN
    ANZAHL_QUELLEN = {}
    for key, name in (("palette_aggregat", "Palette"), ("lehren_kompakt1", "LK1"),
                      ("lehren_und_lernen", "LuL"), ("master_korpus", "MK03")):
        for k, ops in q[key].items():
            for o in ops:
                ANZAHL_QUELLEN.setdefault(o.rstrip("*"), set()).add(name)
    if len(eindeutig) < 30:
        fehl(f"nur {len(eindeutig)} eindeutige Operatoren geparst, erwartet ueber 30")
    return eindeutig, mehrdeutig

def formen(v):
    """Suchmuster fuer ein Verb. Nur Infinitiv und 3.-Person-Form, jeweils mit
    Wortgrenzen. Ein Wortstamm ohne Grenze traf vorher Substantive:
    «Werte» als «werten», «Datenschutzbestimmungen» als «bestimmen»,
    «angemessen» als «messen». Die SLP-Lernziele sind Infinitive, darum genuegt
    das."""
    v = v.strip()
    muster = [re.escape(v)]
    if v.endswith("en") and len(v) > 4:
        muster.append(re.escape(v[:-2]) + "t")      # erklaeren -> erklaert
    if v.endswith("ern") and len(v) > 5:
        muster.append(re.escape(v[:-1]) + "t")      # aeussern -> aeussert
    return re.compile(r"\b(?:" + "|".join(muster) + r")\b")

FORMEN_CACHE = {}
def trifft(v, text):
    if v not in FORMEN_CACHE: FORMEN_CACHE[v] = formen(v)
    return bool(FORMEN_CACHE[v].search(text))

def main():
    eindeutig, mehrdeutig = operatoren()
    befunde, mehr_treffer = [], []
    for fach in ("slp-bku1-kind", "slp-bku1-beh"):
        p = f"{B}/{fach}/references/lernsituationen.json"
        if not os.path.isfile(p): fehl(f"{p} fehlt")
        for nr, ls in sorted(json.load(open(p, encoding="utf-8")).items()):
            ziele = [z for z in ls.get("bfs_ziele", []) if isinstance(z.get("k"), int)]
            if not ziele: continue
            hoechst = max(z["k"] for z in ziele)
            for lz in ls.get("lernziele", []):
                t = lz.lower()
                gef = {v: s for v, s in eindeutig.items() if trifft(v, t)}
                if not gef: continue
                top = max(gef.values())
                if top > hoechst:
                    namen = ", ".join(sorted(v for v, s in gef.items() if s == top))
                    md = sorted(v for v in mehrdeutig if trifft(v, t))
                    qn = sorted(set().union(*(ANZAHL_QUELLEN.get(v, set())
                                for v, sv in gef.items() if sv == top)))
                    befunde.append({"fach": fach[-4:], "ls": nr, "bip": hoechst,
                                    "slp": top, "verben": namen,
                                    "quellen": ", ".join(qn), "stark": len(qn),
                                    "mehrdeutig": ", ".join(md), "lernziel": lz})
    for b in sorted(befunde, key=lambda x: (x["ls"], x["fach"])):
        grad = "STARK" if b["stark"] >= 2 else "einzelquelle"
        print(f"BEFUND [{grad}] LS {b['ls']} ({b['fach']}): BiP hoechstens K{b['bip']}, "
              f"SLP-Lernziel verlangt K{b['slp']} ueber «{b['verben']}» "
              f"(belegt in: {b['quellen']})")
        print(f"       {b['lernziel'][:160]}")
        if b["mehrdeutig"]:
            print(f"       dazu mehrdeutig, nicht gewertet: {b['mehrdeutig']}")
    print(f"\nEindeutige Operatoren aus den belegten Quellen: {len(eindeutig)}, "
          f"mehrdeutige ausgenommen: {len(mehrdeutig)}")
    stark = sum(1 for b in befunde if b["stark"] >= 2)
    print(f"Faelle: {len(befunde)}, davon mit mindestens zwei Quellen belegt: {stark}")
    return 1 if befunde else 0

if __name__ == "__main__":
    sys.exit(main())
