# calculate.py
import sys
import json

def calculate(limit_start, limit_end, limit):
    teiler_liste = [[]] * (limit + 1)
    for zahl_auswahl in range(limit_start, limit_end + 1):
        teiler_liste[zahl_auswahl] = []
        for teiler_test in range(1, int(zahl_auswahl ** 0.5) + 1):
            if zahl_auswahl % teiler_test == 0:
                teiler_liste[zahl_auswahl].append(teiler_test)
                if teiler_test != zahl_auswahl // teiler_test and zahl_auswahl != zahl_auswahl // teiler_test:
                    teiler_liste[zahl_auswahl].append(zahl_auswahl // teiler_test)
    print(json.dumps(teiler_liste))


if __name__ == '__main__':
    limit_bereich = str(sys.argv[1])
    limit = int(sys.argv[2])
    # wandle den string in eine liste um
    limit_bereich = limit_bereich[1:-1].split(', ')
    limit_start = int(limit_bereich[0])
    limit_end = int(limit_bereich[1])
    calculate(limit_start, limit_end, limit)