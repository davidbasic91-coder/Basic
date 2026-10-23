#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft die Zeilen "Meyer/Stocker, Lehren kompakt 1, S. 70" in den sechs
K-Stufen-Notizen des Vaults gegen das Original auf S. 70.
Exit 0 = jeder dort genannte Operator steht im Original, 1 = Abweichung."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quellen import lehren_kompakt1

V = os.environ.get("KS_ORDNER", os.path.expanduser("~/Desktop/BFS/Werkstatt Didaktik/40 Aufgaben und Operatoren"))
NOTIZEN = {"K1": "K1 Wissen.md", "K2": "K2 Verstehen.md", "K3": "K3 Anwenden.md",
           "K4": "K4 Analysieren.md", "K5": "K5 Synthese oder Entwickeln.md",
           "K6": "K6 Bewerten oder Beurteilen.md"}

orig, zitate = lehren_kompakt1()
# Die Stufenbezeichnung selbst deckt den gleichnamigen Operator: steht im Original
# "Stufe K4: Analyse", so ist "analysieren" am Original belegt.
BEZEICHNUNG = {"K1": {"wiedergeben", "wiedererkennen"}, "K2": {"verstehen"},
               "K3": {"anwenden"}, "K4": {"analysieren"},
               "K5": {"synthetisieren"}, "K6": {"evaluieren"}}
orig_flach = {k: {o.rstrip("*") for o in v} | BEZEICHNUNG.get(k, set())
              for k, v in orig.items()}

befunde = 0
for k, datei in NOTIZEN.items():
    p = os.path.join(V, datei)
    if not os.path.isfile(p):
        print(f"Pruefung nicht lauffaehig: {p} fehlt"); sys.exit(2)
    txt = open(p, encoding="utf-8").read()
    m = re.search(r'^\|\s*Meyer/Stocker[^|]*\|\s*([^|]+)\|', txt, re.M)
    if not m:
        print(f"{k}: keine Zeile 'Meyer/Stocker' in {datei}"); befunde += 1; continue
    behauptet = [" ".join(t.split()).lower() for t in m.group(1).split(",") if t.strip()]
    fehlen = [o for o in behauptet if o not in orig_flach.get(k, set())]
    print(f"{k}  Original S. 70: {zitate.get(k,'')}")
    print(f"    Notiz behauptet: {', '.join(behauptet)}")
    if fehlen:
        print(f"    NICHT IM ORIGINAL: {', '.join(fehlen)}")
        befunde += len(fehlen)
    else:
        print("    alle am Original belegt")
print(f"\nBefunde: {befunde}")
sys.exit(1 if befunde else 0)
