# main.py
import subprocess
import json
import os

# Anzahl der Prozessorkerne einlesen
kern_anzahl = os.cpu_count()

# Eingabe der max. Zahl und der Anzahl der Prozesse
while True:
    try:
        limit = int(input("Bitte die maximale Zahl angeben bis zu welcher getestet werden soll: "))
        if limit <= 0:
            raise ValueError
        break
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein.")

while True:
    try:
        proz_anzahl = int(input("Bitte die Anzahl der Prozesse angeben: "))
        if proz_anzahl > limit:
            raise ValueError
        elif proz_anzahl > kern_anzahl:
            raise ValueError
        break
    except ValueError:
        if proz_anzahl > kern_anzahl:
            print(f"Die Anzahl der Prozesse darf nicht größer als die Anzahl der Prozessorkerne sein, "
                  f"weil es sonst die Leistung beinträchtigen könnte. Die Anzahl der Prozessorkerne ist: {kern_anzahl}")
        else:
            print(f"Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein, die kleiner oder gleich der max. Zahl: {limit} ist.")

teiler_liste = []
# teile limit auf die Anzahl der Prozesse auf so,
# dass sie in einer liste sind z.b. [[0, 100], [101, 200], [201, 300]] für ein limit von 300 und 3 Prozessen

prozesse = [[0, (0 + 1) * limit // proz_anzahl]]

for i in range(1, proz_anzahl):
    prozesse.append([(i * limit // proz_anzahl) + 1, (i + 1) * limit // proz_anzahl])
print(prozesse)

for proz_num in range(proz_anzahl):
    exec(f'p{proz_num} = subprocess.Popen(["python", "calculate.py", str(prozesse[proz_num]), str(limit)], stdout=subprocess.PIPE)')

for proz_num in range(proz_anzahl):
    exec(f'teiler_erg_{proz_num} = json.loads(p{proz_num}.communicate()[0])')
    exec(f'teiler_liste += teiler_erg_{proz_num}')
print("teiler berechnen fertig")


print(teiler_liste)
print("fertig")

