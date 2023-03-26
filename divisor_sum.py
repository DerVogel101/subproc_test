#divisor_sum.py
import sys
import json


def teiler_sum(teiler_liste_abschnitt):
    teiler_liste_summe = []
    for i in teiler_liste_abschnitt:
        teiler_liste_summe.append(sum(i))
    print(json.dumps(teiler_liste_summe))


if __name__ == '__main__':
    teiler_liste_abschnitt = json.loads(sys.argv[1])
    teiler_sum(teiler_liste_abschnitt)
