#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, io
d = json.load(open("auswertung.json", encoding="utf-8"))
SP = ["Palette-Liste", "Palette-Typen", "SAVOIRSOCIAL", "Lehren kompakt 1",
      "Lehren und Lernen", "Master-Korpus 03", "Bauplan"]
o = io.StringIO()
o.write("| Operator | " + " | ".join(SP) + " |\n")
o.write("|---" * (len(SP)+1) + "|\n")
for z in d["zeilen"]:
    o.write("| " + z["operator"] + " | " + " | ".join(z[s] for s in SP) + " |\n")
open("vergleichstabelle.md", "w", encoding="utf-8").write(o.getvalue())
print(f"Zeilen: {len(d['zeilen'])}")
