# teiler_suche.py
# Importiere die Module
import json
import sys

def teiler_finden(limit_start, limit_ende):
    teiler_liste = []
    for zahl_auswahl in range(limit_start, limit_ende + 1):
        teiler = [teiler_test for teiler_test in range(1, int(zahl_auswahl ** 0.5) + 1) if zahl_auswahl % teiler_test == 0]
        teiler += [zahl_auswahl // x for x in teiler if x != zahl_auswahl // x and zahl_auswahl != zahl_auswahl // x]
        teiler_liste.append(teiler)
    print(json.dumps(teiler_liste))


if __name__ == '__main__':
    limit_bereich = str(sys.argv[1])  # Lese den Zahlenbereich aus den Argumenten aus
    limit_bereich = limit_bereich[1:-1].split(', ')  # Formatiere den Zahlenbereich
    limit_start = int(limit_bereich[0])  # Setzte den Startwert des Zahlenbereichs
    limit_end = int(limit_bereich[1])  # Setzte den Endwert des Zahlenbereichs
    # Führe die Funktion teiler_finden aus mit den Argumenten limit_start und limit_end als Start- und Endwert
    teiler_finden(limit_start, limit_end)
