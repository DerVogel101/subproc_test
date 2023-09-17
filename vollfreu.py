# vollfreu.py
import sys
import json

def paar_finden(stellen_liste, summen_werte_liste):
    befreundet_vollkommen_liste = []  # Erstellt eine leere Liste, um die befreundeten oder vollkommenen Zahlen zu speichern
    stellen_set = set(stellen_liste)  # Erstellt ein Set aus der Liste der Stellen
    for zahl1, zahl2 in enumerate(summen_werte_liste):  # Iteriert über die Summen der Teiler
        if zahl1 in stellen_set and zahl2 < len(
                summen_werte_liste):  # Wenn die erste Zahl in der Liste der Stellen ist und die zweite Zahl kleiner als die Länge der Liste ist
            summe_zahl2 = summen_werte_liste[zahl2]  # Nehme die Summe der Teiler der zweiten Zahl aus der Liste
            # Wenn die Summe der Teiler der zweiten Zahl gleich der ersten Zahl ist und das Paar (zahl2, zahl1) noch nicht in der Liste ist
            if summe_zahl2 == zahl1 and (zahl2, zahl1) not in befreundet_vollkommen_liste:
                # dann füge das Paar zur Liste der befreundeten oder vollkommenen Zahlen hinzu
                befreundet_vollkommen_liste.append((zahl1, zahl2))

    # Gebe die Liste der befreundeten oder vollkommenen Zahlen an den Hauptprozess weiter
    print(json.dumps(befreundet_vollkommen_liste))


if __name__ == '__main__':
    proz_num = int(json.loads(sys.argv[1]))  # Lese die Prozessnummer aus den Argumenten aus
    pfad = sys.argv[2]  # Lese den Pfad der Datei mit den Daten aus und dessen Namen
    datei_endung = sys.argv[3]  # Lese die Dateiendung aus
    # Öffne die Datei mit den Summen der Teiler und speichere sie in einer Liste
    with open(f"{pfad}/p_vollfreu_wert_{proz_num}{datei_endung}", "r") as f:
        summen_werte_liste = json.loads(f.read())

    # Öffne die Datei mit den Stellen und speichere sie in einer Liste
    with open(f"{pfad}/p_vollfreu_abschnitt_{proz_num}{datei_endung}", "r") as f:
        stellen_liste = json.loads(f.read())
    # Rufe die Funktion paar_finden auf, um die befreundeten oder vollkommenen Zahlen zu finden
    paar_finden(stellen_liste, summen_werte_liste)
