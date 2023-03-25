# calculate.py
import sys
import json

def calculate(limit, start, step):
    teiler_liste = [0] * (limit + 1)
    for zahl_auswahl in range(start, limit + 1, step):
        teiler_liste[zahl_auswahl] = []
        for teiler_test in range(1, int(zahl_auswahl ** 0.5) + 1):
            if zahl_auswahl % teiler_test == 0:
                teiler_liste[zahl_auswahl].append(teiler_test)
                if teiler_test != zahl_auswahl // teiler_test and zahl_auswahl != zahl_auswahl // teiler_test:
                    teiler_liste[zahl_auswahl].append(zahl_auswahl // teiler_test)
    print(json.dumps(teiler_liste))

if __name__ == '__main__':
    limit = int(sys.argv[1])
    start = int(sys.argv[2])
    step = int(sys.argv[3])
    calculate(limit, start, step)