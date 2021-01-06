# -*- coding: utf-8 -*-
# coding=utf-8

from vacances import *
from TwitterAPI import TwitterAPI
from datetime import datetime
import random, time

api = TwitterAPI(consumer_key='vubLt29IblZTniw1rXOw0zVVG', consumer_secret='ZQvrqzpypnh9opttZRFt1H9yWAQxLUHGsNWSyXyACwnNPRxTu5', access_token_key='1205808613874393088-MMHsXvRZkuKcKa4bAFg0Lms6An3czn', access_token_secret='pF71QMMoK5FXpr8UPTH7geDaszopVjHDZo9h8z86MeV38')

equal, vacances = vacances_create_image()

if equal:
    # STEP 1 - upload image A, B et C
    file = open('/home/bots/Electryon_Bot_Py_2/vacances/data/export_A, B et C.png', 'rb')
    data = file.read()
    r = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')
else:
    # STEP 1 - upload image A
    file = open('/home/bots/Electryon_Bot_Py_2/vacances/data/export_A.png', 'rb')
    data = file.read()
    r = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

    # STEP 2 - upload image B
    file = open('/home/bots/Electryon_Bot_Py_2/vacances/data/export_B.png', 'rb')
    data = file.read()
    r2 = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

    # STEP 3 - upload image C
    file = open('/home/bots/Electryon_Bot_Py_2/vacances/data/export_C.png', 'rb')
    data = file.read()
    r3 = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

confinement = is_confinement()
# STEP 4 - upload image confinement
if confinement:
    file = open('/home/bots/Electryon_Bot_Py_2/vacances/data/export_confinement.png', 'rb')
    data = file.read()
    r4 = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

noel = noel_draw(date.today())
# STEP 5 - upload image noel
if noel:
    file = open('/home/bots/Electryon_Bot_Py_2/vacances/data/export_noel.png', 'rb')
    data = file.read()
    r5 = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

# STEP 6 - post tweet with a reference to uploaded image
if equal:
    if r.status_code == 200: media_id = r.json()['media_id']
else:
    if r.status_code == 200 and r2.status_code == 200 and r3.status_code == 200:
        media_id = r.json()['media_id']
        media_id2 = r2.json()['media_id']
        media_id3 = r3.json()['media_id']
if confinement and r4.status_code == 200: media_id4 = r4.json()['media_id']
if noel and r5.status_code == 200: media_id5 = r5.json()['media_id']

if vacances:
    tweet = "Le retour des vacances c'est pour bientôt ! 🏫\nAlors profitez bien de votre repos ! 🏝"
else:
    lines = open('/home/bots/Electryon_Bot_Py_2/vacances/tweets.txt').read().splitlines()
    tweet = random.choice(lines)
message = tweet + "\n\n#Vacances #Holidays #AQuandLesVacances #BientotLesVacances"

media_ids = [str(media_id)]

if not equal:
    media_ids.append(str(media_id2))
    media_ids.append(str(media_id3))
if confinement: media_ids.append(str(media_id4))
if noel: media_ids.append(str(media_id5))

r = api.request('statuses/update', {'status':message, 'media_ids':",".join(media_ids)})
print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')