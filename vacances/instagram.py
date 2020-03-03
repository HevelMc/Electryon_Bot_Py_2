from vacances import *
import os

max_days = {'janvier': 31, 'février': 29, 'mars': 31, 'avril': 30, 'mai': 31, 'juin': 30, 'juillet': 31, 'aout': 31, 'septembre': 30, 'octobre': 31, 'novembre':30, 'décembre': 31}
mois_nb = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7, 'aout': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12}

# for mois in max_days:



def images_mois(mois, année):
    try:
        os.mkdir("/home/bots/Electryon_Bot_Py_2/vacances/data/instagram_export/" + mois)
        print("Dossier " + mois + " créé !")
    except:
        print("Dossier " + mois + " existant.")
    
    if mois == "février":
        if (année / 4) == round(année / 4):
            max_days["février"] = 29
        else:
            max_days["février"] = 28

    for jour in range(1, max_days[mois] + 1):
        vacances_create_image(str(jour) + "/" + str(mois_nb[mois]) + "/" + str(année), mois, jour)

def load_input():
    mois = input("Mois : ").lower()
    année = int(input("Année : "))
    if mois in max_days:
        print("Génération d'image pour le mois de " + mois)
        images_mois(mois, année)
        load_input()
    else:
        print("Incorrect !")
        load_input()

load_input()