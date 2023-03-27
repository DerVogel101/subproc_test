#divisor_sum.py
import sys
import json


def teiler_sum(teiler_liste_abschnitt):
    teiler_liste_summe = []
    for i in teiler_liste_abschnitt:
        teiler_liste_summe.append(sum(i))
    print(json.dumps(teiler_liste_summe))


if __name__ == '__main__':
    proz_num = int(json.loads(sys.argv[1]))
    pfad = sys.argv[2]
    datei_endung = sys.argv[3]
    with open(f"{pfad}/p_sum_{proz_num}{datei_endung}", "r") as f:
        teiler_liste_abschnitt = json.loads(f.read())
    teiler_sum(teiler_liste_abschnitt)
