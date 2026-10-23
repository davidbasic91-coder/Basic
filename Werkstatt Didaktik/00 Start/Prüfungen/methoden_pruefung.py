#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft die Methodensammlung des Skills unterrichtsmethoden und die
zugehoerigen Vaultnotizen.

Pruefarten:
  duplikate   Fast-Duplikate: sehr aehnliche Titel oder Kurzdefinitionen
  bloomwozu   Zielverb im WOZU-Feld gegen die ausgewiesene Bloom-Passung
  eignung     Eignungsskala: «Tief» und «Gering» nebeneinander
  lsstufe     «Passende BKU1-LS» gegen die hoechste K-Stufe jener LS im SLP
  synchron    Vaultnotiz gegen ihren Skill-Eintrag
  alle        alles, Exit 1 sobald eine Art Befunde hat

Exit 0 keine Befunde, 1 Befunde, 2 Pruefung nicht lauffaehig.
"""
import argparse, difflib, json, os, re, sys

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
SKILL = _plugin_unterrichten() + "/skills"
REF = SKILL + "/unterrichtsmethoden/references"
VAULT = HOME + "/Desktop/BFS/Werkstatt Didaktik/30 Methoden und Medien/Methodensammlung"
DATEIEN = ["prinzipien.md", "techniken.md", "medien.md", "weitere.md",
           "ergaenzungen-1.md", "ergaenzungen-2.md", "ergaenzungen-3.md"]

def fehl(msg):
    print(f"Pruefung nicht lauffaehig: {msg}"); sys.exit(2)

def norm(s):
    s = s.lower()
    for a, b in (("ä","ae"),("ö","oe"),("ü","ue"),("ß","ss")): s = s.replace(a,b)
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)

def eintraege(ref=REF, dateien=DATEIEN):
    """-> Liste {nr, titel, datei, text, felder}"""
    out = []
    for name in dateien:
        p = os.path.join(ref, name)
        if not os.path.isfile(p): fehl(f"Referenzdatei fehlt: {p}")
        text = open(p, encoding="utf-8").read()
        teile = re.split(r"^## (\d+)\.\s*(.+)$", text, flags=re.M)
        for i in range(1, len(teile), 3):
            nr, titel, body = teile[i], teile[i+1].strip(), teile[i+2]
            felder = {}
            for m in re.finditer(r'\*\*([^*]+?):\*\*\s*(.*?)(?=\n\s*[-*]?\s*\*\*|\n\s*---|\Z)',
                                 body, re.S):
                felder[m.group(1).strip()] = " ".join(m.group(2).split())
            out.append({"nr": nr, "titel": titel, "datei": name,
                        "text": body, "felder": felder})
    return out

QUITTIERT = set()

def melde(befunde, marke, art):
    befunde = [b for b in befunde if (art, b) not in QUITTIERT]
    for b in befunde: print(f"BEFUND [{art}] {b}")
    if befunde:
        print(f"{art}: {len(befunde)} Befund(e)"); return 1
    print(f"{marke}"); return 0

# ---------------- 1 Fast-Duplikate ----------------
def praefix(a, b):
    """Laenge des gemeinsamen Anfangs."""
    n = 0
    for x, y in zip(a, b):
        if x != y: break
        n += 1
    return n

# Paare, die die Vorauswahl trifft, die aber am Eintrag geprueft und als
# verschiedene Methoden bestaetigt sind. Je Zeile der Grund.
GEPRUEFT_VERSCHIEDEN = {
 ("116", "117"): "Kette wirft einen Ball im Kreis, Stern sammelt an der "
                 "Wandtafel. Verschiedene Methodenkartei-Eintraege.",
 ("244", "245"): "244 ist das Legebild mit Thesenkarten (Heft Nr. 28), "
                 "245 sind drei Anschlussformate dazu (Heft Nr. 29).",
 ("246", "247"): "246 ist die Debatte (Heft Nr. 30, K4), 247 sind ihre "
                 "sieben Spielregeln (Heft Nr. 31, K3).",
 ("261", "262"): "261 ist Feedback als Rueckmeldeform (Heft Nr. 50), "
                 "262 das Regelwerk mit Satzanfaengen (Heft Nr. 51).",
 ("236", "285"): "Dieselbe Grundidee, zwei Durchfuehrungen: 236 mit vier bis "
                 "fuenf Thesenpostern und Rundgang (40 bis 60 Min.), 285 mit "
                 "A3-Blatt in Kleingruppen (20 bis 35 Min.).",
}

def p_duplikate(E, min_praefix=12, min_teil=12, kurz_hoch=0.55):
    """Die Zeichenaehnlichkeit ganzer Titel taugt nicht: «Deduktive Verfahren»
    und «Induktive Verfahren» erreichen 0.89, sind aber Gegensaetze. Darum
    zaehlt hier nur ein langer gemeinsamer Titelanfang oder ein Titel, der als
    Ganzes im anderen steckt; die Kurzdefinition gibt den Schweregrad."""
    befunde = []
    n = len(E)
    for i in range(n):
        for j in range(i+1, n):
            a, b = E[i], E[j]
            ta, tb = norm(a["titel"]), norm(b["titel"])
            if not ta or not tb: continue
            pf = praefix(ta, tb)
            kurz, lang = sorted((ta, tb), key=len)
            teil = len(kurz) >= min_teil and kurz in lang
            ka = norm(a["felder"].get("Kurzdefinition", ""))
            kb = norm(b["felder"].get("Kurzdefinition", ""))
            kq = difflib.SequenceMatcher(None, ka, kb).ratio() if ka and kb else 0.0
            if not (pf >= min_praefix or teil or kq >= 0.70): continue
            paar = tuple(sorted((a["nr"], b["nr"]), key=int))
            if paar in GEPRUEFT_VERSCHIEDEN: continue
            grad = "HOCH" if (kq >= kurz_hoch or (teil and kq >= 0.40)) else "zu pruefen"
            wie = []
            if pf >= min_praefix: wie.append(f"gemeinsamer Anfang {pf} Zeichen")
            if teil: wie.append("ein Titel steckt im anderen")
            if kq >= 0.70: wie.append("Kurzdefinition fast gleich")
            befunde.append(
                f"{grad}: Nr. {a['nr']} «{a['titel']}» und Nr. {b['nr']} «{b['titel']}» "
                f"({', '.join(wie)}, Kurzdefinition {kq:.2f})")
    befunde.sort()
    if GEPRUEFT_VERSCHIEDEN:
        print(f"({len(GEPRUEFT_VERSCHIEDEN)} Paare am Eintrag geprueft und als "
              f"verschiedene Methoden bestaetigt, nicht gemeldet)")
    return melde(befunde, "DUPLIKATE-OK", "duplikate")

# ---------------- 2 Bloom gegen WOZU ----------------
# Zielverben und ihre Stufe. Quelle: Operatorenliste der Palette (Skill
# aufgabentypen) und SKILL.md unterrichtsmethoden: «bewerten, beurteilen,
# Stellung nehmen, Feedback geben» gehoeren auf K4.
# Nur Operatoren, die die Operatorenliste der Palette fuehrt, dazu die vier,
# die SKILL.md unterrichtsmethoden ausdruecklich auf K4 setzt. «ueben» ist
# bewusst NICHT aufgenommen: kein Operator der Palette, nur Alltagswort.
VERB_STUFE = {
 "nennen":1,"aufzählen":1,"benennen":1,"wiedergeben":1,"zuordnen":1,"definieren":1,
 "erklären":2,"erläutern":2,"zusammenfassen":2,"beschreiben":2,"umschreiben":2,"ordnen":2,
 "anwenden":3,"durchführen":3,"umsetzen":3,"einsetzen":3,"demonstrieren":3,
 "analysieren":4,"untersuchen":4,"gliedern":4,"herausarbeiten":4,"ableiten":4,
 "gegenüberstellen":4,"identifizieren":4,"korrigieren":4,"voraussagen":4,
 "gewichten":4,"einschätzen":4,"bewerten":4,"beurteilen":4,"stellung nehmen":4,"feedback geben":4,
 "konzipieren":5,"planen":5,"ausarbeiten":5,
}
# Operatoren, die nach Davids Entscheid E-083 ueber mehrere Stufen spannen. Sie zaehlen
# nicht als Befund, sondern werden gesondert als Grenzfall gelistet.
MEHRDEUTIG = {"begründen", "einordnen", "entwickeln", "erschliessen", "erarbeiten", "gestalten", "vergleichen"}
def bloom_stufen(roh):
    """K-Stufen einer Bloom-Angabe. Spannen wie «K2 bis K4» oder «K2-K4»
    werden aufgeloest, damit die Schreibweise des Skills und die
    YAML-Aufzaehlung der Vaultnotiz vergleichbar sind."""
    out = set()
    for m in re.finditer(r"K(\d)\s*(?:bis|\u2013|\u2014|-)\s*K(\d)", roh):
        a, b = int(m.group(1)), int(m.group(2))
        out |= set(range(min(a, b), max(a, b) + 1))
    rest = re.sub(r"K\d\s*(?:bis|\u2013|\u2014|-)\s*K\d", " ", roh)
    out |= {int(x) for x in re.findall(r"K(\d)", rest)}
    return sorted(out)

def p_bloomwozu(E):
    befunde = []
    for e in E:
        roh = e["felder"].get("Bloom-Passung", "")
        if not roh:
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: keine Bloom-Passung"); continue
        st = bloom_stufen(roh)
        if not st:
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: Bloom-Passung ohne K-Angabe"); continue
        wozu = e["felder"].get("WOZU – Ziel/Kompetenz", "").lower()
        if not wozu: continue
        gefunden, grenz = {}, []
        for verb, st_v in VERB_STUFE.items():
            if re.search(r'\b' + re.escape(verb), wozu): gefunden[verb] = st_v
        for verb in MEHRDEUTIG:
            if re.search(r'\b' + re.escape(verb), wozu): grenz.append(verb)
        if grenz and not gefunden:
            continue   # nur mehrdeutige Verben: kein Befund, siehe E-083
        if not gefunden: continue
        hoechstes = max(gefunden.values())
        # Nur melden, wenn das hoechste Zielverb ueber der Bloom-Spanne liegt
        # oder die Bloom-Spanne mehr als eine Stufe darueber liegt.
        if hoechstes > max(st):
            vs = ", ".join(f"{v} (K{s})" for v, s in gefunden.items() if s == hoechstes)
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: Bloom {roh[:28]} , "
                           f"WOZU nennt {vs}")
        elif min(st) - hoechstes >= 2:
            vs = ", ".join(f"{v} (K{s})" for v, s in gefunden.items() if s == hoechstes)
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: Bloom K{min(st)}, "
                           f"WOZU nennt hoechstens {vs}")
    return melde(befunde, "BLOOMWOZU-OK", "bloomwozu")

# ---------------- 3 Eignungsskala ----------------
# Reine Stufenwoerter. Zwischenstufen («mittel bis hoch») sind zulaessig und
# werden auf ihre Bestandteile zerlegt.
STUFEN_ERLAUBT = ("sehr hoch", "hoch", "mittel", "gering", "tief", "keine", "bedingt")

def eignungsstufe(roh):
    """Schneidet die Stufenangabe vom Begruendungstext ab.
    «Hoch: passt zu …» -> hoch; «mittel-hoch» -> mittel-hoch."""
    t = roh.strip().lower()
    t = re.split(r'[:.;(,]', t)[0]
    t = re.sub(r'\s+(als|f\u00fcr|im|in|mit|bei|wenn|aber)\b.*$', '', t)
    t = " ".join(t.split()).strip(" ,-")
    return t

def p_eignung(E):
    befunde, nutzt = [], {}
    for e in E:
        roh = e["felder"].get("Eignung FaBe-BKU1", "")
        if not roh:
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: kein Eignungsfeld"); continue
        wort = eignungsstufe(roh)
        teile = [x.strip() for x in re.split(r'\s*(?:bis|\u2013|-|/|oder)\s*', wort) if x.strip()]
        unbekannt = [x for x in teile if x not in STUFEN_ERLAUBT]
        if not teile or unbekannt:
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: Eignung «{wort}» nicht in der Skala")
        for x in teile:
            if x in STUFEN_ERLAUBT: nutzt.setdefault(x, []).append(e["nr"])
    if "tief" in nutzt and "gering" in nutzt:
        befunde.append(f"Skala doppelt besetzt: «Tief» bei Nr. {', '.join(nutzt['tief'])}, "
                       f"«Gering» bei Nr. {', '.join(nutzt['gering'])}")
    return melde(befunde, "EIGNUNG-OK", "eignung")

# ---------------- 4 LS-Empfehlung gegen K-Stufe der LS ----------------
def slp_stufen():
    """-> {LS-Nummer: hoechste K-Stufe} aus beiden Fachrichtungen."""
    out = {}
    for s in ("slp-bku1-kind", "slp-bku1-beh"):
        p = f"{SKILL}/{s}/references/lernsituationen.json"
        if not os.path.isfile(p): fehl(f"SLP-Datei fehlt: {p}")
        for nr, d in json.load(open(p, encoding="utf-8")).items():
            ks = [z.get("k") for z in d.get("bfs_ziele", []) if isinstance(z.get("k"), int)]
            if ks: out[nr] = max(out.get(nr, 0), max(ks))
    if not out: fehl("SLP ergab keine K-Stufen")
    return out

def p_lsstufe(E, min_abstand=2):
    """Gemeldet wird nur, wenn die Methode in ihrer niedrigsten Auspraegung
    mindestens zwei Stufen ueber dem hoechsten Ziel der empfohlenen LS liegt.
    Grund: 13 der 26 BKU1-Lernsituationen haben als hoechstes BFS-Ziel nur K2,
    waehrend 95 der 330 Methoden erst bei K4 oder K5 beginnen. Bei Abstand 1
    waeren es 455 Meldungen, was die Pruefung unbrauchbar machen wuerde."""
    slp = slp_stufen()
    befunde = []
    for e in E:
        roh = e["felder"].get("Passende BKU1-LS", "")
        st = bloom_stufen(e["felder"].get("Bloom-Passung", ""))
        if not roh or not st: continue
        for nr in sorted(set(re.findall(r'LS\s*(\d\.\d\d)', roh))):
            if nr not in slp: 
                befunde.append(f"Nr. {e['nr']} «{e['titel']}»: empfiehlt LS {nr}, "
                               f"die im SLP nicht vorkommt")
                continue
            ziel = slp[nr]
            # Eine Methode, die flacher ist als das hoechste Ziel der LS, ist
            # kein Befund: jede LS braucht Methoden auf mehreren Stufen. Nur
            # eine Methode, die in ihrer NIEDRIGSTEN Ausprägung schon hoeher
            # zielt als die LS ueberhaupt verlangt, passt nicht.
            abstand = min(st) - ziel
            if abstand >= min_abstand:
                grad = "GROB" if abstand >= 3 else "zu pruefen"
                befunde.append(f"{grad} (+{abstand}): Nr. {e['nr']} «{e['titel']}» "
                               f"(Bloom K{min(st)}"
                               + (f" bis K{max(st)}" if max(st) != min(st) else "")
                               + f") empfiehlt sich fuer LS {nr}, deren hoechstes Ziel K{ziel} ist")
    befunde.sort()
    return melde(befunde, "LSSTUFE-OK", "lsstufe")

# ---------------- 5 Synchronitaet Vault gegen Skill ----------------
def vaultnotizen():
    if not os.path.isdir(VAULT): fehl(f"Vaultordner fehlt: {VAULT}")
    out = {}
    for name in sorted(os.listdir(VAULT)):
        if not name.endswith(".md"): continue
        text = open(os.path.join(VAULT, name), encoding="utf-8").read()
        m = re.search(r'^nr:\s*(\d+)\s*$', text, re.M)
        if not m: continue
        fm = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        kurz = re.search(r"^kurz:\s*'?(.*?)'?\s*$", fm.group(1), re.M) if fm else None
        ks = re.findall(r'^- (K[1-6])\s*$', fm.group(1), re.M) if fm else []
        eig = re.search(r'^eignung_fabe:\s*(.+)$', fm.group(1), re.M) if fm else None
        out[m.group(1)] = {"datei": name, "kurz": kurz.group(1) if kurz else "",
                           "kstufen": ks, "eignung": eig.group(1).strip() if eig else ""}
    if not out: fehl("keine Vaultnotiz mit Feld nr gefunden")
    return out

def p_synchron(E):
    V = vaultnotizen()
    skill = {e["nr"]: e for e in E}
    befunde = []
    nur_skill = sorted(set(skill) - set(V), key=int)
    nur_vault = sorted(set(V) - set(skill), key=int)
    if nur_skill: befunde.append(f"Nummern nur im Skill: {', '.join(nur_skill)}")
    if nur_vault: befunde.append(f"Nummern nur im Vault: {', '.join(nur_vault)}")
    for nr in sorted(set(skill) & set(V), key=int):
        e, v = skill[nr], V[nr]
        sk = norm(e["felder"].get("Kurzdefinition", ""))
        vk = norm(v["kurz"])
        if sk and vk and difflib.SequenceMatcher(None, sk, vk).ratio() < 0.9:
            befunde.append(f"Nr. {nr}: Kurzdefinition weicht ab. Skill «"
                           f"{e['felder'].get('Kurzdefinition','')[:70]}» , "
                           f"Vault «{v['kurz'][:70]}»")
        st = {f"K{x}" for x in bloom_stufen(e["felder"].get("Bloom-Passung", ""))}
        if st and v["kstufen"] and st != set(v["kstufen"]):
            befunde.append(f"Nr. {nr} «{e['titel']}»: K-Stufe Skill "
                           f"{'/'.join(sorted(st))}, Vault {'/'.join(v['kstufen'])}")
        def ev(t):
            t = eignungsstufe(t)
            return re.sub(r'\s*(?:bis|\u2013|-|/|oder)\s*', ' bis ', t).strip()
        se, vv = ev(e["felder"].get("Eignung FaBe-BKU1", "")), ev(v["eignung"])
        if se and vv and se != vv:
            befunde.append(f"Nr. {nr} «{e['titel']}»: Eignung Skill «{se}», Vault «{vv}»")
    return melde(befunde, "SYNCHRON-OK", "synchron")

# ---------------- 6 K6 und K5-als-Bewerten ----------------
def p_k6(E):
    """Die Aufgabentypen-Palette fuehrt in FaBe nur K1 bis K5 und schreibt
    ausdruecklich, dass K6 praktisch nie erreicht wird. K5 heisst dort
    Synthese, nicht Bewerten. Dieselbe Pruefung macht Davids
    methoden_check.py bloom; sie ist hier mitgefuehrt, damit eine Gegenprobe
    auf einer Kopie moeglich ist."""
    befunde = []
    for e in E:
        roh = e["felder"].get("Bloom-Passung", "")
        if not roh:
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: keine Bloom-Passung"); continue
        if "K6" in roh:
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: nennt K6, "
                           f"in FaBe laut Palette nicht vorgesehen")
        if re.search(r"K5[^.]{0,18}(Bewerten|Beurteilen)|(Bewerten|Beurteilen)[^.]{0,10}\(K5\)", roh):
            befunde.append(f"Nr. {e['nr']} «{e['titel']}»: K5 als «Bewerten», K5 ist Synthese")
    return melde(befunde, "K6-OK", "k6")

ARTEN = {"duplikate": p_duplikate, "bloomwozu": p_bloomwozu, "eignung": p_eignung,
         "lsstufe": p_lsstufe, "synchron": p_synchron, "k6": p_k6}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("art", nargs="?", default="alle")
    ap.add_argument("--ref", default=REF, help="anderer Referenzordner, fuer Gegenproben")
    ap.add_argument("--ausnahmen", help="JSON-Liste quittierter Befunde [[art, text], ...]")
    a = ap.parse_args()
    if a.ausnahmen:
        if not os.path.isfile(a.ausnahmen): fehl(f"Ausnahmedatei fehlt: {a.ausnahmen}")
        for art, txt in json.load(open(a.ausnahmen, encoding="utf-8")):
            QUITTIERT.add((art, txt))
        print(f"Ausnahmedatei: {a.ausnahmen} ({len(QUITTIERT)} quittierte Befunde)")
    E = eintraege(a.ref)
    print(f"Eintraege gelesen: {len(E)}")
    if len(E) < 300: fehl(f"nur {len(E)} Eintraege gelesen, erwartet rund 330")
    if a.art == "alle":
        return max(f(E) for f in ARTEN.values())
    if a.art not in ARTEN:
        print("unbekannt:", a.art, "erlaubt:", ", ".join(ARTEN), "oder alle"); return 2
    return ARTEN[a.art](E)

if __name__ == "__main__":
    sys.exit(main())
