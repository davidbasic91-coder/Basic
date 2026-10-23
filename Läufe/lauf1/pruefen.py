# Schritt 4: prüft einen Themenfeld-Vorschlag gegen liste.json und den Vault.
# Aufruf: python3 pruefen.py liste.json ergebnis.json vaultordner
# Exit-Code 0 = alles eingehalten, 1 = mindestens ein Verstoss.
import os, sys, json, unicodedata, collections
N = lambda s: unicodedata.normalize("NFC", s).strip()
liste = {e["datei"]: e for e in json.load(open(sys.argv[1], encoding="utf-8"))}
erg = json.load(open(sys.argv[2], encoding="utf-8"))
vault = sys.argv[3]
auf_platte = set()
for o in os.listdir(vault):
    if N(o)[:2] in ("10", "20", "30", "40", "50", "60", "70") and N(o)[2:3] == " ":
        for dp, dn, fn in os.walk(os.path.join(vault, o)):
            auf_platte |= {N(f[:-3]) for f in fn if f.endswith(".md")}
verstoss = 0
def melde(text):
    global verstoss; verstoss += 1; print("VERSTOSS:", text)

felder = erg["themenfelder"]; nz = [N(x) for x in erg.get("nicht_zugeordnet", [])]
zaehler = collections.Counter(); genannt = set(nz)
for f in felder:
    for n in f["notizen"]:
        zaehler[N(n)] += 1; genannt.add(N(n))
# 1. Erfundene oder falsch geschriebene Namen
for n in sorted(genannt):
    if n not in liste: melde(f"Notiz nicht in der Liste: «{n}»")
    elif n not in auf_platte: melde(f"Notiz nicht im Vault gefunden: «{n}»")
# 2. Vollständigkeit
fehlt = sorted(set(liste) - genannt)
for n in fehlt: melde(f"Notiz weder in einem Feld noch auf «nicht zugeordnet»: «{n}»")
# 3. Höchstens zwei Felder, nicht zugleich in Feld und «nicht zugeordnet»
for n, c in sorted(zaehler.items()):
    if c > 2: melde(f"Notiz in {c} Feldern: «{n}»")
for n in sorted(set(nz) & set(zaehler)): melde(f"Notiz in einem Feld und auf «nicht zugeordnet»: «{n}»")
for n, c in collections.Counter(nz).items():
    if c > 1: melde(f"Notiz {c}-mal auf «nicht zugeordnet»: «{n}»")
# 4. Grössenregel (ohne Methoden): höchstens 40 Notizen und 20000 Wörter
print("\nFeld | Notizen gesamt | ohne Methoden | Wörter ohne Methoden | belegt | sammlung")
for f in felder:
    ns = [N(n) for n in f["notizen"] if N(n) in liste]
    if len(set(ns)) != len(ns): melde(f"Feld «{f['name']}» nennt eine Notiz mehrfach")
    ohne = [n for n in set(ns) if liste[n]["typ"] != "methode"]
    w = sum(liste[n]["woerter"] for n in ohne)
    b = sum(1 for n in set(ns) if liste[n]["status"] == "belegt"); s = sum(1 for n in set(ns) if liste[n]["status"] == "sammlung")
    print(f"{f['name']} | {len(set(ns))} | {len(ohne)} | {w} | {b} | {s}")
    if len(ohne) > 40: melde(f"Feld «{f['name']}» hat {len(ohne)} Notizen ohne Methoden (höchstens 40)")
    if w > 20000: melde(f"Feld «{f['name']}» hat {w} Wörter ohne Methoden (höchstens 20000)")
    for k, ist in (("anzahl_belegt", b), ("anzahl_sammlung", s), ("woerter_volltext_ohne_methoden", w)):
        if k in f and f[k] != ist: print(f"  Hinweis: {k} angegeben {f[k]}, nachgezählt {ist}")
print(f"\nNotizen in der Liste: {len(liste)} | genannt: {len(genannt & set(liste))} | nicht zugeordnet: {len(set(nz))} | Felder: {len(felder)}")
print(f"Verstösse: {verstoss}")
sys.exit(1 if verstoss else 0)
