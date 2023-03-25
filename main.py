# main.py
import subprocess
import json

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
        break
    except ValueError:
        print(f"Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein, die kleiner oder gleich der max. Zahl: {limit} ist.")

# teile limit auf die Anzahl der Prozesse auf so,
# dass sie in einer liste sind z.b. [[0, 100], [101, 200], [201, 300]] für ein limit von 300 und 3 Prozessen

prozesse = [[0, (0 + 1) * limit // proz_anzahl]]

for i in range(1, proz_anzahl):
    prozesse.append([(i * limit // proz_anzahl) + 1, (i + 1) * limit // proz_anzahl])
print(prozesse)

for proz_num in range(proz_anzahl):
    exec(f'p{proz_num} = subprocess.Popen(["python", "calculate.py", str(prozesse[proz_num]), str(proz_num), "2"], stdout=subprocess.PIPE)')

for proz_num in range(proz_anzahl):
    exec(f'result{proz_num} = json.loads(p{proz_num}.communicate()[0])')


teiler_liste = [None] * (limit + 1)
for i in range(1, limit + 1):
    if i % 2 == 1:
        teiler_liste[i] = result1[i]
    else:
        teiler_liste[i] = result2[i]

print(teiler_liste)

