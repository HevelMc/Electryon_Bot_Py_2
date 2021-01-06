# coding=utf-8

import json, requests
from datetime import date, datetime, time, timedelta
from instapy_cli import client
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

confinement = datetime(2020, 5, 11)
folder = '/home/bots/Electryon_Bot_Py_2/vacances/data/'

URL = "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-calendrier-scolaire&rows=200&sort=-start_date&facet=description&facet=start_date&facet=end_date&facet=zones&facet=annee_scolaire&refine.annee_scolaire={0}&timezone=Europe%2FParis"

def business_days(since, until):
    since_isoweekday = since.isoweekday() + 1
    return len([x for x in range(since_isoweekday, since_isoweekday + (until - since).days) if x % 7 not in [0, 6]])


def get_date(date=None):
    if date:
        today = datetime.strptime(date, "%d/%m/%Y")
    else:
        today = datetime.today()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    print(today)
    if today.month >= 8:
        return today, str(today.year) + "-" + str(today.year + 1)
    else:
        return today, str(today.year - 1) + "-" + str(today.year)


def is_confinement():
    today, _ = get_date()
    return True if confinement - today > timedelta(days=0) else False

def vacances_create_image(date=None):
    equal = False
    today, year = get_date(date)
    r = requests.get(URL.format(year))
    data = r.json()

    type, date = {}, {}

    for area in ["A", "B", "C"]:
        type[area], date[area] = get_per_zone(data, year, today, area)
    
    for area in ["A", "B", "C"]:
        if date["A"] == date["B"] == date["C"]:
            draw_image(type[area], today, date[area], "A, B et C")
            equal = True
            break
        else:
            draw_image(type[area], today, date[area], area)
    if is_confinement():
        past_days = today - datetime(2020, 3, 17)
        remaining_days = confinement - today
        draw_image_confinement(past_days.days + 1, remaining_days.days)
    return equal, type["A"] == "end" and equal

def get_per_zone(data, year, today, area):
    for holiday in data['records']:
        fields = holiday['fields']
        if holiday['fields']['zones'] == "Zone " + area:
            holiday_start = datetime.strptime(str(holiday['fields']['start_date']), "%Y-%m-%d")
            holiday_end = datetime.strptime(str(holiday['fields']['end_date']), "%Y-%m-%d")
            
            if holiday_end - holiday_start > timedelta(days=5):
                if holiday_start - today > timedelta(days=0):
                    return "start", holiday_start
                elif holiday_end - today > timedelta(days=0):
                    return "end", holiday_end
    return "error", "error"


def draw_image(type, today, date, area):
    font = ImageFont.truetype(folder + 'Roboto-Black.ttf', size=59)
    font_45 = ImageFont.truetype(folder + 'Roboto-Black.ttf', size=45)
    fontbold = ImageFont.truetype(folder + 'Roboto-Bold.ttf', size=100)
    color = 'rgb(68, 68, 68)'
    
    if type == "start":
        image = Image.open(folder + 'Avant-les-vacances.png')
        draw = ImageDraw.Draw(image)
        draw.text((668, 260), str("%02d" % ((date - today).days)) + " JOURS", fill=color, font=font)
        draw.text((190, 742), str(business_days(today, date)) + " JOURS", fill=color, font=font_45)
        draw.text((186, 819), "DE COURS", fill=color, font=font_45)
        draw.text((633, 420), str(round( ((date - today).days) / 7)) + " SEMAINES", fill=color, font=font)
    elif type == "end":
        image = Image.open(folder + 'Apres-les-vacances.png')
        draw = ImageDraw.Draw(image)
        draw.text((668, 260), str("%02d" % ((date - today).days)) + " JOURS", fill=color, font=font)
        draw.text((640, 420), date.strftime("%d/%m/%Y"), fill=color, font=font)
    else:
        return

    draw.text((290, 44), area, fill=color, font=fontbold)
    draw.text((25, 1010), today.strftime("%d/%m/%Y"), fill=color, font=font_45)
    im = Image.open(folder + "zone " + area + ".png")
    image.paste(im, (604, 579))
    image.save(folder + 'export_' + area + '.png')

def draw_image_confinement(past_days, remaining_days):
    font = ImageFont.truetype(folder + 'Roboto-Black.ttf', size=80)
    color = 'rgb(68, 68, 68)'
    image = Image.open(folder + 'Confinement.png')
    draw = ImageDraw.Draw(image)
    past_days = str(past_days) + "ème Jour"
    _w, _h = draw.textsize(past_days, font=font)
    draw.text(((image.width-_w)/2, 425), past_days, fill=color, font=font)
    remaining_days = str(remaining_days) + " Jours" if remaining_days > 1 else str(remaining_days) + " Jour"
    _w, _h = draw.textsize(remaining_days, font=font)
    draw.text(((image.width-_w)/2, 771), remaining_days, fill=color, font=font)
    image.save(folder + 'export_confinement.png')

def noel_draw(today):

    if today.month != 12 or today.day > 25: return False 
    delta = date(today.year, 12, 24) - today
    days = delta.days + 1

    image = Image.open(f'{folder}christmas-backgrounds/{str(days % 5 + 1)}.jpg')
    font = ImageFont.truetype(folder + 'Castoro-Regular.ttf', size=230)
    fontsmall = ImageFont.truetype(folder + 'Castoro-Regular.ttf', size=100)
    draw = ImageDraw.Draw(image, "RGBA")
    iw, ih = image.size

    snow = Image.open(folder + 'snow.png')
    snow = snow.resize((iw, ih))
    image.paste(snow, (0, 0), snow)
    
    draw.rectangle(((0, 0), (iw, ih)), fill=(0,0,0, 150))

    deco = Image.open(folder + 'decorative.png')
    deco = ImageOps.mirror(deco)
    deco = deco.resize((deco.size[0]*2, deco.size[1]*2))
    dw, dh = deco.size
    yo = 250
    decodown = ImageOps.flip(deco)
    image.paste(deco, ((round(iw/2 - dw/2), yo)), deco)
    image.paste(decodown, ((round(iw/2 - dw/2), ih - yo - dh)), decodown)

    if days < 2:
        line = "Joyeux" if days == 0 else "Bon"
        tw, th = draw.textsize(line, font=font)
        draw.text((iw/2 - tw/2, ih/2 - th), line, fill=(255, 255, 255), font=font)
        line = "Noël !" if days == 0 else "Réveillon !"
        tw, th = draw.textsize(line, font=font)
        draw.text((iw/2 - tw/2, ih/2), line, fill=(255, 255, 255), font=font)
    else:
        sample = str(days) + " JOUR" + ('S' if days > 1 else '')
        tw, th = draw.textsize(sample, font=font)
        draw.text((iw/2 - tw/2, ih/2 - th/2), sample, fill=(255, 255, 255), font=font)

    sample = str(today.day) + " décembre"
    tw, th = draw.textsize(sample, font=fontsmall)
    draw.text((iw/2 - tw/2, 100), sample, fill=(255, 255, 255), font=fontsmall)

    image.save(folder + 'export_noel.png')
    return True

if __name__ == "__main__":
    today_input = input("Entrer la date : ")
    if today_input:
        vacances_create_image(today_input)
    else:
        vacances_create_image(None)