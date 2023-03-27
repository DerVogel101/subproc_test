# main.py
import subprocess
import json
import os
import time
from colorama import Fore, Style
from datetime import datetime

# Anzahl der Prozessorkerne einlesen
kern_anzahl = os.cpu_count()
# Eingabe der max. Zahl und der Anzahl der Prozesse
while True:
    try:
        limit_input = input("Bitte die maximale Zahl angeben bis zu welcher getestet werden soll (Standart = 100000): ")
        if not limit_input:
            limit = 100000
        else:
            limit = int(limit_input)
            if limit <= 0:
                raise ValueError
        break
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein.")

while True:
    try:
        proz_anzahl_input = input(f"Bitte die Anzahl der Prozesse angeben (Standart = hälfte der verfügbaren Kerne: {kern_anzahl // 2}): ")
        if not proz_anzahl_input:
            proz_anzahl = kern_anzahl // 2
        else:
            proz_anzahl = int(proz_anzahl_input)
            if proz_anzahl > limit:
                raise ValueError
            elif proz_anzahl > kern_anzahl:
                raise ValueError

        break
    except ValueError:
        print(f"Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein, die kleiner oder gleich der max. Zahl: {limit} ist")
        print(f"und kleiner als die Kernanzahl ist, weil es sonst die Leistung beinträchtigen könnte. Die Anzahl der Prozessorkerne ist: {kern_anzahl}")
    except TypeError:
        print("Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein.")

gesamt_start = time.time()

teiler_liste = []
summe_teiler_liste = []
teiler_liste_abschnitte = []
stellen_summe_liste = []
wert_summe_liste = []
stellen_summe_liste_abschnitte = []
befreundete_volkkommende_zahlen = []


def zeit_format(start, ende):
    global stunden, minuten, sekunden
    dauer = round(ende - start, 4)
    minuten, sekunden = divmod(dauer, 60)
    stunden, minuten = divmod(minuten, 60)
    sekunden = Style.BRIGHT + str(sekunden) + Style.RESET_ALL
    minuten = Style.BRIGHT + str(minuten) + Style.RESET_ALL
    stunden = Style.BRIGHT + str(stunden) + Style.RESET_ALL

os.makedirs("ergebnisse", exist_ok=True)
os.makedirs("tmp", exist_ok=True)
tmp_ordner = "tmp"
erg_ordner = "ergebnisse"
pfad_erg = os.path.join(os.path.dirname(os.path.abspath(__file__)), erg_ordner)
pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), tmp_ordner)
pfad = pfad.replace("\\", "/")
datei_endung = ".tmp_data"


def tmp_dateien_loeschen():
    # Durchlaufe alle Dateien im Verzeichnis
    for filename in os.listdir(pfad):
        # Überprüfe, ob die Datei die gewünschte Endung hat
        if filename.endswith(datei_endung):
            # Lösche die Datei
            file_path = os.path.join(pfad, filename)
            os.remove(file_path)


tmp_dateien_loeschen()
# teile limit auf die Anzahl der Prozesse auf so,
# dass sie in einer liste sind z.b. [[0, 100], [101, 200], [201, 300]] für ein limit von 300 und 3 Prozessen

prozesse = [[0, (0 + 1) * limit // proz_anzahl]]

for i in range(1, proz_anzahl):
    prozesse.append([(i * limit // proz_anzahl) + 1, (i + 1) * limit // proz_anzahl])
print("Die Zahlen die auf die Prozesse aufgeteielt werden sind wie folgt: ")
for proz_num in range(proz_anzahl):
    print(f"Prozess {proz_num}: {prozesse[proz_num][0]:>{len(str(limit))}} - {prozesse[proz_num][1]:<{len(str(limit))}}")

start_teiler = time.time()
# starte die Prozesse
for proz_num in range(proz_anzahl):
    exec(f'p{proz_num} = subprocess.Popen(["python", "calculate.py", str(prozesse[proz_num])], stdout=subprocess.PIPE)')

for proz_num in range(proz_anzahl):
    exec(f'teiler_erg_{proz_num} = json.loads(p{proz_num}.communicate()[0])')
    exec(f'teiler_liste_abschnitte.append(teiler_erg_{proz_num})')

end_teiler = time.time()
zeit_format(start_teiler, end_teiler)
print(f"\nTeiler berechnen ist fertig, es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.")

# teile die liste teiler_liste in proz_anzahl Teile auf

start_summe = time.time()
# starte die Prozesse
for proz_num in range(proz_anzahl):
    exec(f'with open("{pfad}/p_sum_{proz_num}{datei_endung}", "w") as f{proz_num}: f{proz_num}.write(str(teiler_liste_abschnitte[proz_num]))')
for proz_num in range(proz_anzahl):
    exec(f'p_sum_{proz_num} = subprocess.Popen(["python", "divisor_sum.py", str(proz_num), str(pfad), str(datei_endung)], stdout=subprocess.PIPE)')

for proz_num in range(proz_anzahl):
    exec(f'teiler_sum_erg_{proz_num} = json.loads(p_sum_{proz_num}.communicate()[0])')
    exec(f'summe_teiler_liste += teiler_sum_erg_{proz_num}')

end_summe = time.time()
zeit_format(start_summe, end_summe)
print(f"Summe der Teiler berechnen ist fertig, es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.")

start_vollfreu = time.time()
for stelle_liste_summe, wert_summe in enumerate(summe_teiler_liste):
    stellen_summe_liste.append(stelle_liste_summe)
    wert_summe_liste.append(wert_summe)

for i in range(proz_anzahl):
    stellen_summe_liste_abschnitte.append([])
    for j in range(prozesse[i][0], prozesse[i][1] + 1):
        stellen_summe_liste_abschnitte[i].append(stellen_summe_liste[j])

for proz_num in range(proz_anzahl):
    exec(f'with open("{pfad}/p_vollfreu_abschnitt_{proz_num}{datei_endung}", "w") as f{proz_num}: f{proz_num}.write(str(stellen_summe_liste_abschnitte[proz_num]))')
    exec(f'with open("{pfad}/p_vollfreu_wert_{proz_num}{datei_endung}", "w") as f{proz_num}: f{proz_num}.write(str(wert_summe_liste))')

for proz_num in range(proz_anzahl):
    #exec(f'p_vollfreu_{proz_num} = subprocess.Popen(["python", "vollfreu.py", str(stellen_summe_liste_abschnitte[proz_num]), str(wert_summe_liste)], stdout=subprocess.PIPE)')
    exec(f'p_vollfreu_{proz_num} = subprocess.Popen(["python", "vollfreu.py", str(proz_num), str(pfad), str(datei_endung)], stdout=subprocess.PIPE)')
for proz_num in range(proz_anzahl):
    exec(f'vollfreu_erg_{proz_num} = json.loads(p_vollfreu_{proz_num}.communicate()[0])')
    exec(f'befreundete_volkkommende_zahlen += vollfreu_erg_{proz_num}')

end_vollfreu = time.time()
zeit_format(start_vollfreu, end_vollfreu)
print(f"Das berechnen der Vollkommenden und Befreundeten ist fertig, es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.\n")

while [] in befreundete_volkkommende_zahlen:
    befreundete_volkkommende_zahlen.remove([])

zeitstempel = datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
with open(f"{pfad_erg}/ergebnis_{zeitstempel}.txt", "w") as f:
    for paare in befreundete_volkkommende_zahlen:
        ausgabe_paare_z1 = paare[0]  # speichere die erste Zahl des Paares in einer Variablen
        ausgabe_paare_z2 = paare[1]  # speichere die zweite Zahl des Paares in einer anderen Variablen
        format_paar_z1 = Style.BRIGHT + str(ausgabe_paare_z1) + Style.RESET_ALL
        format_paar_z2 = Style.BRIGHT + str(ausgabe_paare_z2) + Style.RESET_ALL

        # wenn die beiden Zahlen gleich sind und das Paar nicht (0,0) oder (1,1) ist
        if ausgabe_paare_z1 == ausgabe_paare_z2 and paare not in [[0, 0], [1, 1]]:
            print(f"{'Die Zahl: ':<14}{format_paar_z1} ist vollkomen") # dann gebe aus, dass die Zahl vollkommen ist
            print(f"{'Die Zahl: ':<14}{ausgabe_paare_z1} ist vollkomen", file=f)
        elif paare not in [[0, 0], [1, 1]]:  # sonst wenn das Paar nicht (0,0) oder (1,1) ist
            # dann gebe aus, dass die beiden Zahlen befreundet sind
            print(f"{'Die Zahlen: ':<13} {format_paar_z1} und {format_paar_z2} sind befreundet")
            print(f"{'Die Zahlen: ':<13} {ausgabe_paare_z1} und {ausgabe_paare_z2} sind befreundet", file=f)

tmp_dateien_loeschen()

gesamt_ende = time.time()
zeit_format(gesamt_start, gesamt_ende)
print(f"\n\n{'Die Anzahl der Prozesse war: ':<30}{Style.BRIGHT + str(proz_anzahl) + Style.RESET_ALL}")
print(f"{'Die Anzahl der Zahlen war: ':<30}{Style.BRIGHT + str(limit) + Style.RESET_ALL}")
print(f"{'Die Anzahl der Paare war: ':<30}{Style.BRIGHT + str(len(befreundete_volkkommende_zahlen)) + Style.RESET_ALL}")
print(f"\nDas Programm ist fertig, es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.")
print("Alle Temporären Dateien wurden gelöscht und das ergbnis ist in der Datei 'befreundete_volkkommende_zahlen.txt' gespeichert.")


