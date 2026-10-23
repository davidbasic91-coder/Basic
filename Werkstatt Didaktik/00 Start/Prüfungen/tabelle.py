#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut aus quellen.py die Vergleichstabelle (1.1), die drei Listen (1.2)
und die Aufarbeitung von B-004 (1.3)."""
import json, re, sys
from quellen import alles, BAUPLAN, BAUPLAN_STATUS

d = alles()

SPALTEN = ["Palette-Liste", "Palette-Typen", "SAVOIRSOCIAL",
           "Lehren kompakt 1", "Lehren und Lernen", "Master-Korpus 03", "Bauplan"]

# ---- Palette-Liste (Aggregat des Skills) ----
pal_liste = {}
for k, ops in d["palette_aggregat"].items():
    for o in ops: pal_liste.setdefault(o, set()).add(k)

# ---- Palette-Typen (Original-PDF): K-Stufe des Typs, in dem der Operator steht ----
pal_typen, pal_typen_wo = {}, {}
for nr, t in d["palette_typen"].items():
    for o in t["ops"]:
        pal_typen.setdefault(o, set()).add(t["kstufe"])
        pal_typen_wo.setdefault(o, []).append(f'Typ {nr} ({t["kstufe"]})')

# ---- Lehren kompakt 1 / Lehren und Lernen / Master-Korpus ----
def invert(dd):
    r = {}
    for k, ops in dd.items():
        for o in ops: r.setdefault(o.rstrip("*"), set()).add(k)
    return r
lk1 = invert(d["lehren_kompakt1"])
lul = invert(d["lehren_und_lernen"])
mk  = invert(d["master_korpus"])
sav = {o: v["fragetyp"] for o, v in d["savoirsocial"].items()}
bau = {o: "?" for o in BAUPLAN}

def z(s):
    return "/".join(sorted(s)) if s else ""

alle_ops = sorted(set(pal_liste) | set(pal_typen) | set(sav) | set(lk1) | set(lul) | set(mk) | set(bau))

zeilen = []
for o in alle_ops:
    zeilen.append({
        "operator": o,
        "Palette-Liste": z(pal_liste.get(o, set())),
        "Palette-Typen": z(pal_typen.get(o, set())),
        "SAVOIRSOCIAL": sav.get(o, ""),
        "Lehren kompakt 1": z(lk1.get(o, set())),
        "Lehren und Lernen": z(lul.get(o, set())),
        "Master-Korpus 03": z(mk.get(o, set())),
        "Bauplan": bau.get(o, ""),
    })

# ---- 1.2 drei Listen ----
# Nur K-Stufen-Quellen vergleichen; SAVOIRSOCIAL nennt Fragetypen, keine K-Stufen,
# und wird ueber die Zuordnung Fragetyp->Stufe NICHT eingerechnet (die Quelle
# macht diese Zuordnung ausdruecklich nicht).
# Nur Quellen, die eine Zuordnung Operator -> K-Stufe BEHAUPTEN.
# "Palette-Typen" bleibt in der Tabelle, geht aber nicht in die Einteilung ein:
# dort ist die Stufe die des Aufgabentyps, nicht die des Operators. Sonst wuerde
# jeder Operator eines Typs mit Spanne (z. B. Typ 17 K2-K5) automatisch als
# abweichend gelten und die Liste mit Rauschen fuellen.
KSTUFEN_SPALTEN = ["Palette-Liste", "Lehren kompakt 1",
                   "Lehren und Lernen", "Master-Korpus 03"]
def kern(v):
    """K-Stufen einer Zelle als Menge; Spannen werden aufgeloest."""
    out = set()
    for teil in v.split("/"):
        teil = teil.strip()
        m = re.match(r'^K(\d)\s*[–-]\s*K(\d)', teil)
        if m:
            out |= {f"K{i}" for i in range(int(m.group(1)), int(m.group(2))+1)}
        else:
            mm = re.match(r'^(K\d)', teil)
            if mm: out.add(mm.group(1))
    return out

gleich, abweichend, einzeln = [], [], []
for zl in zeilen:
    belegt = {s: kern(zl[s]) for s in KSTUFEN_SPALTEN if zl[s]}
    quellen_gesamt = [s for s in SPALTEN if zl[s]]
    if len(quellen_gesamt) == 1:
        einzeln.append((zl["operator"], quellen_gesamt[0], zl[quellen_gesamt[0]]))
    elif len(belegt) >= 2:
        werte = list(belegt.values())
        if all(w == werte[0] for w in werte):
            gleich.append((zl["operator"], z(werte[0]), ", ".join(belegt)))
        else:
            abweichend.append((zl["operator"], belegt))
    else:
        einzeln.append((zl["operator"], ", ".join(quellen_gesamt),
                        " | ".join(f"{s}={zl[s]}" for s in quellen_gesamt)))

# ---- 1.3 B-004: Typen, deren Operatoren die Aggregatliste anders einstuft ----
b004 = []
for nr in sorted(d["palette_typen"]):
    t = d["palette_typen"][nr]
    typ_stufen = kern(t["kstufe"])
    if not typ_stufen: continue
    treffer = []
    for o in t["ops"]:
        listen_stufen = pal_liste.get(o, set())
        if not listen_stufen:
            treffer.append((o, "nicht in der Liste"))
        elif not (listen_stufen & typ_stufen):
            treffer.append((o, "Liste: " + z(listen_stufen)))
    if treffer:
        b004.append({"nr": nr, "titel": t["titel"], "kstufe": t["kstufe"], "treffer": treffer})

# ---- QV-Vergleich: SAVOIRSOCIAL-Fragetyp neben Palette-Stufe ----
# Die Quelle ordnet den Fragetypen ausdruecklich KEINE K-Stufen zu. Hier steht
# darum nur das Nebeneinander, keine Umrechnung.
qv = []
for zl in zeilen:
    if zl["SAVOIRSOCIAL"]:
        qv.append({"operator": zl["operator"], "savoirsocial": zl["SAVOIRSOCIAL"],
                   "punkte": d["savoirsocial"][zl["operator"]]["punkte"],
                   "palette_liste": zl["Palette-Liste"] or "nicht in der Liste",
                   "palette_typen": zl["Palette-Typen"] or "in keinem Typ"})

if __name__ == "__main__":
    out = {"zeilen": zeilen, "qv": qv, "gleich": gleich,
           "abweichend": [(o, {k: sorted(v) for k, v in b.items()}) for o, b in abweichend],
           "einzeln": einzeln, "b004": b004,
           "pal_typen_wo": pal_typen_wo, "bauplan_status": BAUPLAN_STATUS}
    json.dump(out, open("auswertung.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Operatoren insgesamt: {len(zeilen)}")
    print(f"(a) gleich eingestuft: {len(gleich)}")
    print(f"(b) abweichend:        {len(abweichend)}")
    print(f"(c) nur eine Quelle:   {len(einzeln)}")
    print(f"B-004 betroffene Typen: {len(b004)} von 19")
