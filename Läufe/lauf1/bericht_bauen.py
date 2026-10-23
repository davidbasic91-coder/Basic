# Schritt 5: themenfelder.md aus themenfelder.json, liste.json und den Prüfausgaben
import json, sys, collections
L = sys.argv[1]
liste = {e["datei"]: e for e in json.load(open(f"{L}/liste.json", encoding="utf-8"))}
v = json.load(open(f"{L}/themenfelder.json", encoding="utf-8"))
pruef = open(f"{L}/pruefung_ausgabe.txt", encoding="utf-8").read().strip()
gegen = open(f"{L}/gegenprobe_ausgabe.txt", encoding="utf-8").read().strip()
c = collections.Counter(n for f in v["themenfelder"] for n in f["notizen"])
o = []
o.append("# Lauf 1: Themenfelder für Playbooks\n")
o.append("## Kurz\n")
o.append(f"Vorschlag mit {len(v['themenfelder'])} Themenfeldern aus den {len(liste)} Notizen der Ordner 10 bis 70 der Werkstatt Didaktik, zusammengeführt aus drei Entwürfen (A Arbeitssituationen, B Inhalte, C verwandt-Links). Alle {len(liste)} Notizen sind zugeordnet, {sum(1 for n in c if c[n]==1)} in einem Feld und {sum(1 for n in c if c[n]==2)} in zwei Feldern; «nicht zugeordnet» ist leer. Im Vault wurde nichts geändert. David wählt die Themenfelder für Lauf 2.\n")
o.append("## Themenfelder\n")
o.append("Notizen: gesamt / ohne Methoden. Wörter: Volltext ohne Frontmatter, ohne Methoden. Grenze je Feld: höchstens 40 Notizen und 20 000 Wörter, Methoden nicht mitgezählt.\n")
o.append("| Nr. | Themenfeld | Notizen | belegt | sammlung | Wörter | Entwürfe | bestehender Skill |")
o.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
for i, f in enumerate(v["themenfelder"], 1):
    ns = f["notizen"]; ohne = [n for n in ns if liste[n]["typ"] != "methode"]
    b = sum(1 for n in ns if liste[n]["status"] == "belegt"); s = sum(1 for n in ns if liste[n]["status"] == "sammlung")
    w = sum(liste[n]["woerter"] for n in ohne)
    o.append(f"| {i} | {f['name']} | {len(ns)} / {len(ohne)} | {b} | {s} | {w} | {', '.join(f['entwuerfe'])} | {f['skill']} |")
o.append("")
o.append("## Beschreibungen und Notizen\n")
for i, f in enumerate(v["themenfelder"], 1):
    o.append(f"### {i}. {f['name']}\n")
    o.append(f"{f['beschreibung']}\n")
    o.append(f"**Skill:** {f['skill']}. {f['skill_begruendung']}\n")
    ohne = [n for n in f["notizen"] if liste[n]["typ"] != "methode"]
    meth = [n for n in f["notizen"] if liste[n]["typ"] == "methode"]
    o.append(f"**Notizen ({len(ohne)}):** " + ", ".join(f"[[{n}]]" for n in ohne) + "\n")
    if meth: o.append(f"**Methoden für die Tabelle ({len(meth)}):** " + ", ".join(meth) + "\n")
o.append("## Bemerkungen des Zusammenführ-Agenten\n")
o.append("Wörtlich übernommen. Nachgeprüft an liste.json: Aufgabentyp 15 und 16 tragen aviva_phase «Auswerten» bei K4 und K5; Göttinger Katalog und Paderborner Methode haben keine aviva_phase. Die Einstufung «fachfremd für FaBe» ist nicht geprüft.\n")
for p in v["bemerkungen"].split("\n\n"): o.append(f"> {p}\n>")
o[-1] = o[-1].rstrip(">").rstrip()
o.append("\n## Prüfung (Schritt 4)\n")
o.append("**Gegenprobe zuerst:** In einer Kopie (gegenprobe.json) wurde «Erwachsene lernen anders» gestrichen und «Erfundene Notiz Gegenprobe» hinzugefügt.\n")
o.append("```\n$ python3 -I pruefen.py liste.json gegenprobe.json \"Werkstatt Didaktik\"\n" + "\n".join(l for l in gegen.splitlines() if l.startswith(("VERSTOSS", "Verstösse"))) + "\nExit-Code: 1\n```\n")
o.append("**Echtes Ergebnis:**\n")
o.append("```\n$ python3 -I pruefen.py liste.json themenfelder.json \"Werkstatt Didaktik\"\n" + pruef + "\n```\n")
o.append("Geprüft: jede der 542 Notizen steht in einem Feld oder auf «nicht zugeordnet»; jede genannte Notiz gibt es in liste.json und als Datei im Vault; keine Notiz steht in mehr als zwei Feldern; Grössenregel eingehalten. Die Angaben des Agenten zu belegt, sammlung und Wörtern stimmen mit der Nachzählung überein (keine Hinweiszeile). Die drei Entwürfe A, B und C bestehen dieselbe Prüfung ebenfalls mit 0 Verstössen.\n")
o.append("## Kosten\n")
o.append("Laut Abschlussmeldung des Workflows: 4 Agenten (Sonnet), 0 Fehler, 1 191 068 Tokens der Agenten, 50 Werkzeugaufrufe, 1 725 Sekunden (rund 29 Minuten). Geschätzt waren 0,5 bis 1 Mio. Tokens und 10 bis 20 Minuten; beides wurde überschritten. Die Tokens der Hauptsitzung sind darin nicht enthalten.\n")
o.append("## Für Lauf 2\n")
o.append("- E-219 ist schon vergeben (B-102 Planungskette, 23.10.2026); der Entscheid zur Ablage der Playbooks wäre E-220.\n- Die Notiz [[Playbook]] aus E-218 fehlt im Vault.\n- Dateien dieses Laufs: liste_bauen.py, liste.json, liste_agenten.jsonl, entwurf_A.json, entwurf_B.json, entwurf_C.json, themenfelder.json, themenfelder.md, pruefen.py, gegenprobe.json und die Prüfausgaben.\n")
open(f"{L}/themenfelder.md", "w", encoding="utf-8").write("\n".join(o))
print("geschrieben:", len("\n".join(o)), "Zeichen")
