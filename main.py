# main.py
import subprocess
import json

limit = int(input("Bitte die Maximale Zahl angeben bis zu welcher getestet werden soll: "))

p1 = subprocess.Popen(['python', 'calculate.py', str(limit), '1', '2'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['python', 'calculate.py', str(limit), '2', '2'], stdout=subprocess.PIPE)
result1 = json.loads(p1.communicate()[0])
result2 = json.loads(p2.communicate()[0])

teiler_liste = [None] * (limit + 1)
for i in range(1, limit + 1):
    if i % 2 == 1:
        teiler_liste[i] = result1[i]
    else:
        teiler_liste[i] = result2[i]

print(teiler_liste)

