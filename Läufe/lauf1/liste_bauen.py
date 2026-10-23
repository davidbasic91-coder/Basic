# Schritt 1: ein Eintrag je Notiz aus den Ordnern 10 bis 70 -> liste.json
import os, re, sys, json, unicodedata, yaml
vault = sys.argv[1]; ziel = sys.argv[2]
N = lambda s: unicodedata.normalize("NFC", s)
ordner = sorted(d for d in os.listdir(vault) if re.match(r"^[1-7]0 ", N(d)))
liste = []
for o in ordner:
    for dp, dn, fn in os.walk(os.path.join(vault, o)):
        dn.sort()
        for f in sorted(fn):
            if not f.endswith(".md"): continue
            txt = open(os.path.join(dp, f), encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, re.S)
            fm = yaml.safe_load(m.group(1)) if m else {}
            body = m.group(2) if m else txt
            e = {"datei": N(f[:-3]), "ordner": N(os.path.relpath(dp, vault))}
            for k in ["typ", "kurz", "status", "verwandt", "gruppe", "aviva_phase", "k_stufe"]:
                v = fm.get(k)
                if isinstance(v, str): v = N(v)
                if isinstance(v, list): v = [N(x) if isinstance(x, str) else x for x in v]
                if k == "verwandt" and v: v = [re.sub(r"^\[\[|\]\]$", "", x).split("|")[0] if isinstance(x, str) else x for x in v]
                e[k] = v
            e["woerter"] = len(re.findall(r"\S+", body))
            liste.append(e)
namen = [e["datei"] for e in liste]
doppelt = sorted({n for n in namen if namen.count(n) > 1})
json.dump(liste, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Anzahl Einträge:", len(liste))
print("doppelte Dateinamen:", doppelt or "keine")
print("ohne Frontmatter-typ:", [e["datei"] for e in liste if not e["typ"]] or "keine")
