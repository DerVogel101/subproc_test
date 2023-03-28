# teiler_suche.py
# Importiere die Module
import json
import sys


def teiler_finden(limit_start, limit_ende):
    teiler_liste = []  # Erstellt eine leere Liste, um die Teiler zu speichern
    schritt = 0  # Erstellt eine Variable, um die Schritte zu zählen
    for zahl_auswahl in range(limit_start, limit_ende + 1):  # Wählt einen Zahlenbereich aus, über den iteriert wird
        teiler_liste.append([])  # Fügt eine leere Liste in die Liste der Teiler ein
        for teiler_test in range(1, int(zahl_auswahl ** 0.5) + 1):  # Testet alle Zahlen von 1 bis zur Wurzel der Zahl
            if zahl_auswahl % teiler_test == 0:  # Wenn die Zahl durch den Teiler teilbar ist
                teiler_liste[schritt].append(teiler_test)  # Füge den Teiler zur Liste der Teiler hinzu
                # Wenn der Teiler nicht gleich der Zahl ist und die Zahl durch den Teiler teilbar ist
                if teiler_test != zahl_auswahl // teiler_test and zahl_auswahl != zahl_auswahl // teiler_test:
                    # Füge den Teiler zur Liste der Teiler hinzu
                    teiler_liste[schritt].append(zahl_auswahl // teiler_test)
        schritt += 1  # Erhöhe die Schrittvariable um 1
    print(json.dumps(teiler_liste))  # Gebe die Liste der Teiler aus, an den Hauptprozess


if __name__ == '__main__':
    limit_bereich = str(sys.argv[1])  # Lese den Zahlenbereich aus den Argumenten aus
    limit_bereich = limit_bereich[1:-1].split(', ')  # Formatiere den Zahlenbereich
    limit_start = int(limit_bereich[0])  # Setzte den Startwert des Zahlenbereichs
    limit_end = int(limit_bereich[1])  # Setzte den Endwert des Zahlenbereichs
    # Führe die Funktion teiler_finden aus mit den Argumenten limit_start und limit_end als Start- und Endwert
    teiler_finden(limit_start, limit_end)
