# vollfreu.py
import sys
import json

def paar_finden(stellen_liste, summen_werte_liste):
    befreundet_vollkommen_liste = []
    stellen_set = set(stellen_liste)
    for zahl1, zahl2 in enumerate(summen_werte_liste):
        if zahl1 in stellen_set:
         # Wenn die zweite Zahl kleiner als die Länge der Liste ist
            if zahl2 < len(summen_werte_liste):
                # Nehme die Summe der Teiler der zweiten Zahl aus der Liste
                summe_zahl2 = summen_werte_liste[zahl2]
                # Wenn die Summe der Teiler der zweiten Zahl gleich der ersten Zahl ist
                # und das Paar (zahl2, zahl1) noch nicht in der Liste ist
                # und die erste Zahl kleiner oder gleich der zweiten Zahl ist
                if summe_zahl2 == zahl1 and (zahl2, zahl1) and zahl1 <= zahl2:
                    # dann füge das Paar zur Liste der befreundeten oder vollkommenen Zahlen hinzu
                    befreundet_vollkommen_liste.append((zahl1, zahl2))
    print(json.dumps(befreundet_vollkommen_liste))


if __name__ == '__main__':


    proz_num = int(json.loads(sys.argv[1]))
    pfad = sys.argv[2]
    datei_endung = sys.argv[3]
    with open(f"{pfad}/p_vollfreu_wert_{proz_num}{datei_endung}", "r") as f:
        summen_werte_liste = json.loads(f.read())

    with open(f"{pfad}/p_vollfreu_abschnitt_{proz_num}{datei_endung}", "r") as f:
        stellen_liste = json.loads(f.read())
    paar_finden(stellen_liste, summen_werte_liste)