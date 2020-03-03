# coding=utf-8

# -*- coding: utf-8 -*-

from vacances import *
from TwitterAPI import TwitterAPI
import random

api = TwitterAPI(consumer_key='vubLt29IblZTniw1rXOw0zVVG', consumer_secret='ZQvrqzpypnh9opttZRFt1H9yWAQxLUHGsNWSyXyACwnNPRxTu5', access_token_key='1205808613874393088-MMHsXvRZkuKcKa4bAFg0Lms6An3czn', access_token_secret='pF71QMMoK5FXpr8UPTH7geDaszopVjHDZo9h8z86MeV38')

vacances_create_image()

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

# STEP 4 - post tweet with a reference to uploaded image
if r.status_code == 200 and r2.status_code == 200 and r3.status_code == 200:
    media_id = r.json()['media_id']
    media_id2 = r2.json()['media_id']
    media_id3 = r3.json()['media_id']
    
    lines = open('/home/bots/Electryon_Bot_Py_2/vacances/tweets.txt').read().splitlines()
    tweet = random.choice(lines)
    message = tweet + "\n\n#Vacances #Holidays #AQuandLesVacances #BientotLesVacances"

    r = api.request('statuses/update', {'status':message, 'media_ids':str(media_id) + ',' + str(media_id2) + ',' + str(media_id3)})

    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')