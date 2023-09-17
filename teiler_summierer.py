# teiler_summierer.py
import sys
import json


def teiler_sum(teiler_liste_abschnitt):
    teiler_liste_summe = list(map(sum, teiler_liste_abschnitt))  # Berechne die Summe der Teiler für jeden Abschnitt
    print(json.dumps(teiler_liste_summe))  # Gebe die Liste aus, an den Hauptprozess


if __name__ == '__main__':
    proz_num = int(json.loads(sys.argv[1]))  # Lese die Prozessnummer aus
    pfad = sys.argv[2]  # Lese den Pfad der Datei mit den Daten aus und dessen Namen
    datei_endung = sys.argv[3]  # Lese die Dateiendung aus
    with open(f"{pfad}/p_sum_{proz_num}{datei_endung}", "r") as f:  # Öffne die Datei mit den Daten
        teiler_liste_abschnitt = json.loads(f.read())  # Lese die Daten aus der Datei und speichere sie in einer Liste
    # Rufe die Funktion teiler_sum auf, um die Summen der Teiler zu berechnen, mit dem Abschnitt der Teilerliste
    teiler_sum(teiler_liste_abschnitt)
