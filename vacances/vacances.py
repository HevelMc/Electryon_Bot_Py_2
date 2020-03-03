# coding=utf-8

# -*- coding: utf-8 -*-

import urllib.request, json, datetime
from PIL import Image, ImageDraw, ImageFont
from datetime import date, time, datetime, timedelta
from instapy_cli import client

# if prochaines_vacances:
#     print("Prochaines vacances dans " + str((prochaines_vacances - today).days) + " Jours.")
# else:
#     print("Retour de vacances dans " + str((actuelles_vacances - today).days) + " Jours.")

def business_days(since, until):
    since_isoweekday = since.isoweekday() + 1
    return len([x for x in range(since_isoweekday, since_isoweekday + (until - since).days) if x % 7 not in [0, 6]])

def vacances_create_image(date=None, folder=None, jour=None):

    with urllib.request.urlopen("https://gitlab.com/pidila/sp-simulateurs-data/raw/master/donnees-de-reference/VacancesScolaires.json") as url:
        data = json.loads(url.read().decode())


    if date:
        today = datetime.strptime(date, "%d/%m/%Y") - timedelta(days=1)
    else:
        today = datetime.today() - timedelta(days=1)

    if today.month >= 8:
        annee_scolaire = str(today.year) + "-" + str(today.year + 1)
    else:
        annee_scolaire = str(today.year - 1) + "-" + str(today.year)

    zones = ["A", "B", "C"]
    for zone in zones:
        for obj in data['Calendrier']:
            if obj['annee_scolaire'] == annee_scolaire:
                if obj['Zone'] == "Zone " + zone:
                    prochaines_vacances = datetime.strptime(str(obj['Debut']), "%Y-%m-%d")
                    actuelles_vacances = datetime.strptime(str(obj['Fin']), "%Y-%m-%d")
                    print(prochaines_vacances - today)
                    if prochaines_vacances - today > timedelta(days=1):
                        print(obj['Description'])
                        actuelles_vacances = None
                        break
                    elif actuelles_vacances - today > timedelta(days=1):
                        print(obj['Description'])
                        prochaines_vacances = None
                        break
        if prochaines_vacances:
            image = Image.open('/home/bots/Electryon_Bot_Py_2/vacances/data/Avant-les-vacances.png')
        else:
            image = Image.open('/home/bots/Electryon_Bot_Py_2/vacances/data/Apres-les-vacances.png')
        
        font = ImageFont.truetype('/home/bots/Electryon_Bot_Py_2/vacances/data/Roboto-Black.ttf', size=59)
        font_45 = ImageFont.truetype('/home/bots/Electryon_Bot_Py_2/vacances/data/Roboto-Black.ttf', size=45)
        fontbold = ImageFont.truetype('/home/bots/Electryon_Bot_Py_2/vacances/data/Roboto-Bold.ttf', size=100)
        draw = ImageDraw.Draw(image)
        color = 'rgb(68, 68, 68)'

        if prochaines_vacances:
            draw.text((668, 260), str("%02d" % ((prochaines_vacances - today).days)) + " JOURS", fill=color, font=font)
            draw.text((190, 742), str(business_days(today, prochaines_vacances)) + " JOURS", fill=color, font=font_45)
            draw.text((163, 819), "DE SEMAINE", fill=color, font=font_45)
            draw.text((633, 420), str(round(((prochaines_vacances - today).days) / 7)) + " SEMAINES", fill=color, font=font)
        else:
            draw.text((668, 260), str("%02d" % ((actuelles_vacances - today).days)) + " JOURS", fill=color, font=font)
            draw.text((640, 420), actuelles_vacances.strftime("%d/%m/%Y"), fill=color, font=font)
        
        draw.text((290, 44), zone, fill=color, font=fontbold)
        draw.text((25, 1010), (today + timedelta(days=1)).strftime("%d/%m/%Y"), fill=color, font=font_45)
        im = Image.open("/home/bots/Electryon_Bot_Py_2/vacances/data/zone " + zone + ".png")
        image.paste(im, (604, 579))

        if folder and jour:
            image.save('/home/bots/Electryon_Bot_Py_2/vacances/data/instagram_export/' + folder + '/' + str(jour) + zone + '.png')
        else:
            image.save('/home/bots/Electryon_Bot_Py_2/vacances/data/export_' + zone + '.png')