#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kalibrierproben fuer raster.py. Exit 0 = alle Urteile wie erwartet."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster import urteil

PROBEN = [
 # (Frage, hoechste K-Stufe des Teils, erwartetes Urteil, Herkunft)
 ('Darf Laura Cosi verlangen, dass Gabriella nicht mehr gärtnert?', 'K2', 'ZU HOCH', 'Davids Anlassfall'),
 ('Sollen die beiden an der Weihnachtsrunde teilnehmen, und warum?', 'K2', 'ZU HOCH', 'LS 2.04 alte Fassung'),
 ('Wer hat recht, ihre Mutter Svetlana mit dem Schutz oder Alois mit der Selbstständigkeit?', 'K2', 'ZU HOCH', 'LS 2.04 alte Fassung'),
 ('Gilt Pierres «Ja, klar», und was sage ich jetzt?', 'K5', 'ZU HOCH', 'LS 2.04 neue Fassung Teil 2'),
 ('Welches Recht wiegt in der Situation von Azra und Deniz am schwersten?', 'K2', 'ZU HOCH', 'LS 2.04 alte Fassung'),
 ('Was ist das Wichtigste an einem Menschen?', 'K2', 'ZU HOCH', 'LS 2.04 alte Fassung'),
 ('Wie soll Mia in der Teamsitzung vorgehen?', 'K2', 'ZU HOCH', 'konstruiert'),
 ('Auf welche Texte könnte sich Mia stützen, wenn sie ihr antwortet, und für wen gelten sie?', 'K2', 'passt', 'LS 2.04 neue Fassung Teil 1'),
 ('Was steht Pierre zu, ohne dass er es verdienen muss?', 'K2', 'passt', 'LS 2.04 neue Fassung Teil 1'),
 ('Warum ist die Würde eines Menschen nicht verdienbar?', 'K2', 'passt', 'konstruiert'),
 ('Wie würden Sie das humanistische Menschenbild in Ihrem Betrieb anwenden?', 'K3', 'passt', 'konstruiert'),
 ('Worin unterscheiden sich inhärente und kontingente Würde?', 'K2', 'passt', 'konstruiert'),
 ('Worin unterscheiden sich die Menschenbilder, und welches wiegt in der Betreuung schwerer?', 'K4', 'passt', 'konstruiert'),
 ('Wie sehen der Arzt damals, Ruth, Emma, Leonard und Claudia Pierre, und wie sehe ich ihn?', 'K5', 'zu flach', 'LS 2.04 neue Fassung Teil 2'),
 ('Was hat Pierre gebraucht, als ich in seinem Zimmer sass, und was brauchen die Menschen, die ich betreue?', 'K5', 'zu flach', 'LS 2.04 neue Fassung Teil 2'),
 ('Nennen Sie drei Rechte, die Ihnen wichtig sind.', 'K2', 'von Hand', 'LS 2.04 alte Fassung, keine Frage'),
]

def lauf():
    fehler = []
    for f, h, soll, herkunft in PROBEN:
        u, n, b, e = urteil(f, h)
        if soll not in u:
            fehler.append((f, h, soll, u, n))
        print(f"{'OK ' if soll in u else 'XX '} {h}  {u:30s} erwartet «{soll}»  [{n}]")
        print(f"       {f[:100]}   ({herkunft})")
    print(f"\nProben: {len(PROBEN)}, Fehlurteile: {len(fehler)}")
    return 1 if fehler else 0

if __name__ == "__main__":
    sys.exit(lauf())
