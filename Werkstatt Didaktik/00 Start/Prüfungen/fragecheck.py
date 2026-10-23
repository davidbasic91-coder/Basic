#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft Einstiegs- und Ergebnissicherungsfragen der Arbeitsdossiers gegen
die hoechste K-Stufe des jeweiligen Teils.

Exit 0 = keine Frage zielt zu hoch, 1 = Befunde, 2 = nicht lauffaehig.
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from raster import urteil
except Exception as e:
    print(f"Pruefung nicht lauffaehig: {e}"); sys.exit(2)

BAEUME = [os.path.expanduser("~/Desktop/BFS/BKU1 Lernsituationen"),
          os.path.expanduser("~/Desktop/BFS/2. Unterrichtseinheiten")]
AUSSCHLUSS = ("/alt/", "/löschen/", " kopie/", "kopie.docx", "_neuaufbau",
              "vorfassung", "(ersetzt)", "/archiv/", "musterl")  # Musterlösungen sind keine Dossiers (E-215)

def bloecke(doc):
    for child in doc.element.body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag == 'p':   yield ('p', Paragraph(child, doc))
        elif tag == 'tbl': yield ('t', Table(child, doc))

def tabellentext(tbl):
    zeilen = []
    for r in tbl.rows:
        z, vorher = [], None
        for c in r.cells:
            t = " ".join(c.text.split())
            if t and t != vorher: z.append(t); vorher = t
        if z: zeilen.append(z)
    return zeilen

def kstufen_aus_tabelle(zeilen):
    out = set()
    for z in zeilen:
        for zelle in z:
            if re.fullmatch(r'K[1-6]', zelle.strip()):
                out.add(zelle.strip())
    return out

# Zeilen, die zwar ein Fragezeichen tragen, aber Ueberschriften der
# Dossiervorlage sind und keine Frage an die Lernenden.
VORLAGEN_ZEILEN = (
    "schneller fertig", "wo stehen sie", "was wissen sie schon",
    "warum ist das thema wichtig", "was ist das thema",
    "gibt es fragen",            # Organisationsfrage, kein Lerninhalt
    "haben sie fragen",
)

def fragen_aus_text(t):
    """Fragesaetze aus einem Textstueck."""
    t = " ".join(t.split())
    tl = t.lower()
    if any(v in tl for v in VORLAGEN_ZEILEN) and len(t) < 60:
        return []
    out = []
    for stueck in re.split(r'(?<=\?)\s+', t):
        if "?" not in stueck: continue
        # Satzanfang suchen: letztes Satzende vor der Frage
        s = re.split(r'(?<=[.!:])\s+', stueck)
        kandidat = s[-1] if s else stueck
        kandidat = kandidat.strip()
        if len(kandidat) > 12 and kandidat.endswith("?"):
            out.append(kandidat)
    return out

def ist_fragment(f):
    """Satzrest ohne eigenen Anfang: beginnt mit Satzzeichen oder klein."""
    f = f.strip(" \u00ab\u00bb\u201e\u201c\u2019'")
    if not f: return True
    return not (f[0].isupper() or f[0].isdigit())

def dossiers():
    """Pro Lernsituation die jungste Datei, die kein Alt- oder Kopiestand ist."""
    best = {}
    for baum in BAEUME:
        if not os.path.isdir(baum): continue
        for wurzel, _, dateien in os.walk(baum):
            for n in dateien:
                if not n.lower().endswith(".docx") or n.startswith("~$"): continue
                p = os.path.join(wurzel, n)
                pl = p.lower()
                if "arbeitsdossier" not in n.lower() and "arbeitsdossier" not in wurzel.lower():
                    continue
                if any(a in pl for a in AUSSCHLUSS): continue
                m = re.search(r'(?:LS[ _]?)(\d\.\d\d?)', n) or re.search(r'(?:LS[ _]?)(\d\.\d\d?)', wurzel)
                if not m: continue
                ls = m.group(1)
                if len(ls) == 3: ls = ls[0] + "." + ls[2].zfill(2)
                mt = os.path.getmtime(p)
                if ls not in best or mt > best[ls][1]: best[ls] = (p, mt)
    return {ls: p for ls, (p, _) in sorted(best.items())}

def pruefe(pfad):
    """-> Liste von Teilen: {teil, kstufen, fragen:[{quelle, frage, urteil, muster, beleg}]}"""
    doc = docx.Document(pfad)
    teile, aktuell, abschnitt = [], None, None
    for art, el in bloecke(doc):
        if art == 'p':
            t = el.text.strip()
            if not t or el.style.name.startswith('toc'): continue
            st = el.style.name
            ist_teil = (st == 'KW Wochentitel') or re.match(r'^Teil\s+\d\s*[|:]', t)
            if ist_teil and not re.search(r'lerncheck', t, re.I):
                aktuell = {"teil": t, "kstufen": set(), "fragen": []}
                teile.append(aktuell); abschnitt = None
                continue
            if ist_teil:
                # Lerncheck beendet den Teil, ohne einen neuen zu beginnen
                abschnitt = None
                continue
            if aktuell is None: continue
            if st.startswith('Heading 3') or st == 'Heading 3':
                low = t.lower()
                if "einstieg" in low:              abschnitt = "Einstieg"
                elif "ergebnissicherung" in low:   abschnitt = "Ergebnissicherung"
                elif "lerncheck" in low:           abschnitt = None
                else:                              abschnitt = None
                continue
            if abschnitt:
                for f in fragen_aus_text(t):
                    aktuell["fragen"].append({"quelle": abschnitt + " (Text)", "frage": f})
        else:
            if aktuell is None: continue
            zeilen = tabellentext(el)
            aktuell["kstufen"] |= kstufen_aus_tabelle(zeilen)
            flach = " ".join(" ".join(z) for z in zeilen)
            # Leitfragen aus der Praxissituation: «Mia fragt sich: …»
            m = re.search(r'(?:fragt sich|fragen sich)\s*:?(.*)$', flach)
            if m:
                for f in fragen_aus_text(m.group(1)):
                    aktuell["fragen"].append({"quelle": "Leitfrage im Fall", "frage": f})
            if abschnitt:
                for z in zeilen:
                    for zelle in z:
                        hinweis = bool(re.search(r'HILFE|Schneller fertig|FERTIG, WENN', zelle))
                        for f in fragen_aus_text(zelle):
                            aktuell["fragen"].append(
                                {"quelle": abschnitt + (" (Hinweiskasten)" if hinweis else ""),
                                 "frage": f})
    # Urteile
    for t in teile:
        ks = sorted(t["kstufen"])
        t["hoechste"] = ks[-1] if ks else None
        t["kstufen"] = ks
        gesehen = set()
        neu = []
        for f in t["fragen"]:
            key = f["frage"]
            if key in gesehen: continue
            gesehen.add(key)
            if ist_fragment(f["frage"]):
                f.update({"urteil": "Satzfragment, nicht beurteilt", "muster": "-", "beleg": "-"})
                neu.append(f); continue
            if t["hoechste"]:
                u, n, b, e = urteil(f["frage"], t["hoechste"])
            else:
                u, n, b, e = ("K-Stufe des Teils nicht gefunden", "-", "-", "")
            # «zu flach» zaehlt nur fuer die Leitfrage der Klammer und die
            # Ergebnissicherung. Der Einstieg (Runde 1) soll laut Skill spontan
            # und aus dem Vorwissen beantwortet werden, Hinweiskaesten sind Hilfen.
            if u.startswith("zu flach"):
                traegt = ("Leitfrage im Fall" in f["quelle"]
                          or f["quelle"].startswith("Ergebnissicherung"))
                if not traegt or "Hinweiskasten" in f["quelle"]:
                    u = "flach, aber Hilfsfrage"
            f.update({"urteil": u, "muster": n, "beleg": b})
            neu.append(f)
        t["fragen"] = neu
    return teile

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nur", help="eine Lernsituation, z. B. 2.04")
    ap.add_argument("--json", help="Ergebnis als JSON ablegen")
    ap.add_argument("--pfad", help="genau diese Datei pruefen, Auswahlregel umgehen")
    a = ap.parse_args()
    if a.pfad:
        if not os.path.isfile(a.pfad):
            print(f"Pruefung nicht lauffaehig: Datei fehlt: {a.pfad}"); return 2
        d = {"(Einzeldatei)": a.pfad}
    else:
        d = dossiers()
    if not d:
        print("Pruefung nicht lauffaehig: keine Arbeitsdossiers gefunden."); return 2
    if a.nur: d = {k: v for k, v in d.items() if k == a.nur}
    if not d:
        print("Pruefung nicht lauffaehig: gewaehlte Lernsituation nicht im Bestand."); return 2

    ergebnis, zu_hoch, ohne_stufe, von_hand, unpruefbar = [], 0, 0, 0, []
    for ls, pfad in d.items():
        try:
            teile = pruefe(pfad)
        except Exception as e:
            print(f"{ls}  FEHLER beim Lesen: {e}"); return 2
        ergebnis.append({"ls": ls, "pfad": pfad, "teile": teile})
        print(f"\n=== LS {ls}  {os.path.basename(pfad)}")
        # Ein Dossier ohne erkennbare Teile oder ohne K-Stufen ist NICHT
        # geprueft. Das muss stehen, sonst zaehlt es stillschweigend als gruen.
        if not teile or not any(t["kstufen"] for t in teile):
            grund = "keine Teilstruktur erkannt" if not teile else "keine K-Stufen in den Teilen"
            print(f"  NICHT PRUEFBAR: {grund}. Die Frage-Tiefe kann nicht beurteilt werden.")
            unpruefbar.append((ls, grund))
            continue
        for t in teile:
            print(f"  {t['teil'][:60]}   K-Stufen: {'/'.join(t['kstufen']) or 'keine gefunden'}")
            if not t["kstufen"]: ohne_stufe += 1
            for f in t["fragen"]:
                mark = "  "
                if f["urteil"].startswith("ZU HOCH"): mark = "!!"; zu_hoch += 1
                elif f["urteil"].startswith("zu flach"): mark = " ~"
                elif "von Hand" in f["urteil"]: von_hand += 1
                print(f"   {mark} [{f['quelle']:28s}] {f['urteil']:28s} {f['frage'][:110]}")
    print(f"\nDossiers gefunden: {len(d)} | davon geprueft: {len(d) - len(unpruefbar)} | "
          f"NICHT PRUEFBAR: {len(unpruefbar)}")
    if unpruefbar:
        print("Nicht pruefbar: " + ", ".join(f"LS {ls} ({g})" for ls, g in unpruefbar))
    print(f"Fragen zu hoch: {zu_hoch} | Teile ohne K-Stufe: {ohne_stufe} | "
          f"von Hand anzusehen: {von_hand}")
    if a.json:
        json.dump(ergebnis, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 1 if (zu_hoch or unpruefbar) else 0

if __name__ == "__main__":
    sys.exit(main())
