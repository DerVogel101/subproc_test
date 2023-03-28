# main.py
import subprocess
import json
import os
import time
from colorama import Style
from datetime import datetime

# Variablen initialisieren
kern_anzahl = os.cpu_count()  # Anzahl der Prozessorkerne einlesen
teiler_liste = []
summe_teiler_liste = []
teiler_liste_abschnitte = []
stellen_summe_liste = []
wert_summe_liste = []
stellen_summe_liste_abschnitte = []
befreundete_volkkommende_zahlen = []

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
        proz_anzahl_input = input(f"Bitte die Anzahl der Prozesse angeben "
                                  f"(Standart = hälfte der verfügbaren Kerne: {kern_anzahl // 2}): ")
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
        print(f"Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein, "
              f"die kleiner oder gleich der max. Zahl: {limit} ist")
        print(f"und kleiner als die Kernanzahl ist, "
              f"weil es sonst die Leistung beinträchtigen könnte. Die Anzahl der Prozessorkerne ist: {kern_anzahl}")
    except TypeError:
        print("Ungültige Eingabe. Bitte geben Sie eine positive Ganzzahl ein.")

gesamt_start = time.time()

# Pfad, Dateiendung und Ordnernamen definieren
tmp_ordner = "tmp"  # Ordner für die Zwischenergebnisse
erg_ordner = "ergebnisse"  # Ordner für die Ergebnisse
datei_endung = ".tmp_data"  # Dateiendung für die Zwischenergebnisse
os.makedirs(erg_ordner, exist_ok=True)  # Erstelle den Ordner für die Ergebnisse, falls er noch nicht existiert
os.makedirs(tmp_ordner, exist_ok=True)  # Erstelle den Ordner für die Zwischenergebnisse, falls er noch nicht existiert
pfad_erg = os.path.join(os.path.dirname(os.path.abspath(__file__)), erg_ordner)  # Pfad für die Ergebnisse
pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), tmp_ordner)  # Pfad für die Zwischenergebnisse
pfad = pfad.replace("\\", "/")  # Ersetze die Backslashes durch Slashes, damit es mit Python keine Probleme gibt funktioniert

# Funktionen definieren
def zeit_format(start, ende):
    global stunden, minuten, sekunden  # Globale Variablen definieren: Stunden, Minuten und Sekunden
    dauer = round(ende - start, 4)  # Diff. zwischen Start und Ende in Sekunden mit 4 Nachkommastellen
    minuten, sekunden = divmod(dauer, 60)  # Teile die Sekunden durch 60 und speichere den Rest in Minuten
    stunden, minuten = divmod(minuten, 60)  # Teile die Minuten durch 60 und speichere den Rest in Stunden
    # Formatiere die Stunden, Minuten und Sekunden in dem die Zahlen fett sind
    sekunden = Style.BRIGHT + str(sekunden) + Style.RESET_ALL
    minuten = Style.BRIGHT + str(minuten) + Style.RESET_ALL
    stunden = Style.BRIGHT + str(stunden) + Style.RESET_ALL


def tmp_dateien_loeschen():
    for filename in os.listdir(pfad):  # Durchlaufe alle Dateien im Verzeichnis
        if filename.endswith(datei_endung):  # Überprüfe, ob die Datei die gewünschte Endung hat
            losch_datei = os.path.join(pfad, filename)  # Erstelle den Pfad zur Datei
            os.remove(losch_datei)  # Lösche die Datei


# Temporäre Dateien löschen
tmp_dateien_loeschen()

# teile limit auf die Anzahl der Prozesse auf so,
# dass sie in einer liste sind z.b. [[0, 100], [101, 200], [201, 300]] für ein limit von 300 und 3 Prozessen
prozesse = [[0, (0 + 1) * limit // proz_anzahl]] # Füge die Zahlen hinzu die auf die Prozesse aufgeteilt werden sollen für den 0. Prozess

for i in range(1, proz_anzahl):  # Für jeden Prozess
    # Füge die Zahlen hinzu, die auf die Prozesse aufgeteilt werden sollen ab dem 1. Prozess
    prozesse.append([(i * limit // proz_anzahl) + 1, (i + 1) * limit // proz_anzahl])

print("\nDie Zahlen die auf die Prozesse aufgeteielt werden sind wie folgt: ")
for proz_num in range(proz_anzahl):  # Für jeden Prozess
    # Gib die Zahlen aus die auf die Prozesse aufgeteilt werden sollen
    print(f"Prozess {proz_num}: {prozesse[proz_num][0]:>{len(str(limit))}} - {prozesse[proz_num][1]:<{len(str(limit))}}")

start_teiler = time.time()  # Startzeit für die Teilerberechnung
for proz_num in range(proz_anzahl): # Für jeden Prozess
    # Führe den Befehl aus, der die Prozesse startet, die die Teiler berechnen
    exec(f'p{proz_num} = subprocess.Popen(["python", "teiler_suche.py", str(prozesse[proz_num])], stdout=subprocess.PIPE)')

for proz_num in range(proz_anzahl): # Für jeden Prozess
    # Empfange die Daten von den Prozessen und speichere sie in einer Liste ab
    exec(f'teiler_erg_{proz_num} = json.loads(p{proz_num}.communicate()[0])')
    exec(f'teiler_liste_abschnitte.append(teiler_erg_{proz_num})')

end_teiler = time.time()  # Endzeit für die Teilerberechnung
zeit_format(start_teiler, end_teiler)  # Berechne die Stunden, Minuten und Sekunden
# Gib aus, wie lange die Teilerberechnung gedauert hat
print(f"\nTeiler berechnen ist fertig, es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.")


start_summe = time.time()  # Startzeit für die Summenberechnung
for proz_num in range(proz_anzahl): # Für jeden Prozess
    # Führe den Befehl aus, der die Eregbnisse der Teilerberechnung in Dateien für die Summenberechnung zwischenspeichert
    exec(f'with open("{pfad}/p_sum_{proz_num}{datei_endung}", "w") as'
         f' f{proz_num}: f{proz_num}.write(str(teiler_liste_abschnitte[proz_num]))')

for proz_num in range(proz_anzahl):  # Für jeden Prozess
    # Führe den Befehl aus, der die Prozesse startet, die die Summen berechnen
    exec(f'p_sum_{proz_num} = subprocess.Popen(["python", "teiler_summierer.py", str(proz_num),'
         f' str(pfad), str(datei_endung)], stdout=subprocess.PIPE)')

for proz_num in range(proz_anzahl):  # Für jeden Prozess
    # Empfange die Daten von den Prozessen und speichere sie in einer Liste ab
    exec(f'teiler_sum_erg_{proz_num} = json.loads(p_sum_{proz_num}.communicate()[0])')
    exec(f'summe_teiler_liste += teiler_sum_erg_{proz_num}')

end_summe = time.time()  # Endzeit für die Summenberechnung
zeit_format(start_summe, end_summe)  # Berechne die Stunden, Minuten und Sekunden
# Gib aus, wie lange die Summenberechnung gedauert hat
print(f"Summe der Teiler berechnen ist fertig, es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.")


start_vollfreu = time.time()  # Startzeit für die Vollkommen und Freundschafts berechnung
for stelle_liste_summe, wert_summe in enumerate(summe_teiler_liste):  # Für jeden Wert in der Summenliste
    stellen_summe_liste.append(stelle_liste_summe)  # Füge die Stelle in die Liste der Stellen ein
    wert_summe_liste.append(wert_summe)  # Füge den Wert in die Liste der Werte ein

for i in range(proz_anzahl):  # Für jeden Prozess
    stellen_summe_liste_abschnitte.append([])  # Füge eine leere Liste hinzu
    # Für jeden Wert in der Summenliste von der variable prozzesse[i][0] bis prozesse[i][1] + 1
    for j in range(prozesse[i][0], prozesse[i][1] + 1):
        stellen_summe_liste_abschnitte[i].append(stellen_summe_liste[j])  # Füge die Stelle in die Liste der Stellen ein

for proz_num in range(proz_anzahl):  # Für jeden Prozess
    # Führe den Befehl aus, der die zu bearbeitenden Stellen in Dateien für die Vollkommen und Freundschafts berechnung zwischenspeichert
    exec(f'with open("{pfad}/p_vollfreu_abschnitt_{proz_num}{datei_endung}", "w") as'
         f' f{proz_num}: f{proz_num}.write(str(stellen_summe_liste_abschnitte[proz_num]))')
    # Führe den Befehl aus, der die Eregbnisse der Summenberechnung in Dateien für die Vollkommen und Freundschafts berechnung zwischenspeichert
    exec(f'with open("{pfad}/p_vollfreu_wert_{proz_num}{datei_endung}", "w") as'
         f' f{proz_num}: f{proz_num}.write(str(wert_summe_liste))')

for proz_num in range(proz_anzahl):  # Für jeden Prozess
    # Führe den Befehl aus, der die Prozesse startet, die die Vollkommenden und Befreundeten sucht
    exec(f'p_vollfreu_{proz_num} = subprocess.Popen(["python", "vollfreu.py", str(proz_num),'
         f' str(pfad), str(datei_endung)], stdout=subprocess.PIPE)')
for proz_num in range(proz_anzahl):  # Für jeden Prozess
    # Empfange die Daten von den Prozessen und speichere sie in einer Liste ab
    exec(f'vollfreu_erg_{proz_num} = json.loads(p_vollfreu_{proz_num}.communicate()[0])')
    exec(f'befreundete_volkkommende_zahlen += vollfreu_erg_{proz_num}')


end_vollfreu = time.time()  # Endzeit für die Vollkommen und Freundschafts berechnung
zeit_format(start_vollfreu, end_vollfreu)  # Berechne die Stunden, Minuten und Sekunden
# Gib aus, wie lange die Vollkommen und Freundschafts berechnung gedauert hat
print(f"Das berechnen der Vollkommenden und Befreundeten ist fertig,"
      f" es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.\n")


while [] in befreundete_volkkommende_zahlen:  # Solange [] in der Liste sind
    befreundete_volkkommende_zahlen.remove([])  # Entferne []

zeitstempel = datetime.now().strftime("%d.%m.%Y_%H-%M-%S")  # Erstelle einen Zeitstempel
with open(f"{pfad_erg}/ergebnis_{zeitstempel}.txt", "w") as f:  # Öffne eine Datei zum Schreiben der Ergebnisse
    for paare in befreundete_volkkommende_zahlen:  # Für jedes Paar in der Liste der befreundeten und vollkommenen Zahlen
        ausgabe_paare_z1 = paare[0]  # speichere die erste Zahl des Paares in der Variable ausgabe_paare_z1
        ausgabe_paare_z2 = paare[1]  # speichere die zweite Zahl des Paares in der Variable ausgabe_paare_z2
        # formatiere die beiden Zahlen, damit sie hervorgehoben werden
        format_paar_z1 = Style.BRIGHT + str(ausgabe_paare_z1) + Style.RESET_ALL
        format_paar_z2 = Style.BRIGHT + str(ausgabe_paare_z2) + Style.RESET_ALL

        # wenn die beiden Zahlen gleich sind und das Paar nicht [0, 0] oder [1, 1] ist
        if ausgabe_paare_z1 == ausgabe_paare_z2 and paare not in [[0, 0], [1, 1]]:
            print(f"{'Die Zahl: ':<14}{format_paar_z1} ist vollkomen")  # dann gebe aus, dass die Zahl vollkommen ist
            print(f"{'Die Zahl: ':<14}{ausgabe_paare_z1} ist vollkomen", file=f)  # und schreibe es in die Datei
        elif paare not in [[0, 0], [1, 1]]:  # sonst wenn das Paar nicht [0, 0] oder [1, 1] ist
            # dann gebe aus, dass die beiden Zahlen befreundet sind
            print(f"{'Die Zahlen: ':<13} {format_paar_z1} und {format_paar_z2} sind befreundet")
            # und schreibe es in die Datei
            print(f"{'Die Zahlen: ':<13} {ausgabe_paare_z1} und {ausgabe_paare_z2} sind befreundet", file=f)

tmp_dateien_loeschen()  # Lösche alle temporären Dateien

gesamt_ende = time.time()  # Endzeit für das gesamte Programm
zeit_format(gesamt_start, gesamt_ende)  # Berechne die Stunden, Minuten und Sekunden
# Gib aus, wie viele Prozesse es gab
print(f"\n\n{'Die Anzahl der Prozesse war: ':<30}{Style.BRIGHT + str(proz_anzahl) + Style.RESET_ALL}")
# Gib aus, welches Limit es gab
print(f"{'Die Anzahl der Zahlen war: ':<30}{Style.BRIGHT + str(limit) + Style.RESET_ALL}")
# Gib aus, wie viele Paare es gab
print(f"{'Die Anzahl der Paare war: ':<30}{Style.BRIGHT + str(len(befreundete_volkkommende_zahlen)) + Style.RESET_ALL}")
# Gib aus, wie lange das gesamte Programm gedauert hat
print(f"\nDas Programm ist fertig, es hat {stunden} Stunden, {minuten} Minuten und {sekunden} Sekunden gedauert.")
# Gib aus, wo die Ergebnisse gespeichert sind und dass alle temporären Dateien gelöscht wurden
print(f"Alle Temporären Dateien wurden gelöscht und"
      f" das ergbnis ist in der Datei 'befreundete_volkkommende_zahlen_{zeitstempel}.txt' gespeichert.")
