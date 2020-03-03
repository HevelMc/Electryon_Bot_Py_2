from vacances import *

today_input = input("Entrer la date : ")
if today_input:
    vacances_create_image(today_input)
else:
    vacances_create_image(None)