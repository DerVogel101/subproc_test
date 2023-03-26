# calculate.py
import sys
import json
def calculate(limit_start, limit_end):
    teiler_liste = []
    schritt = 0
    for zahl_auswahl in range(limit_start, limit_end + 1):
        teiler_liste.append([])
        for teiler_test in range(1, int(zahl_auswahl ** 0.5) + 1):

            if zahl_auswahl % teiler_test == 0:
                teiler_liste[schritt].append(teiler_test)
                if teiler_test != zahl_auswahl // teiler_test and zahl_auswahl != zahl_auswahl // teiler_test:
                    teiler_liste[schritt].append(zahl_auswahl // teiler_test)
        schritt += 1
    print(json.dumps(teiler_liste))


if __name__ == '__main__':
    limit_bereich = str(sys.argv[1])
    # wandle den string in eine liste um
    limit_bereich = limit_bereich[1:-1].split(', ')
    limit_start = int(limit_bereich[0])
    limit_end = int(limit_bereich[1])
    calculate(limit_start, limit_end)

