import requests
import json
import webbrowser
postal = input("Entrez le code postal: ")
r = requests.get('http://api.zippopotam.us/fr/' + postal)
r_json = r.json()

time = 0
list_loc = []

for i in r_json["places"]:
    print("Ville : " + r_json["places"][time]['place name'])
    loc = r_json["places"][time]['latitude'] + "," + r_json["places"][time]['longitude']
    list_loc.append(loc)
    time += 1

webbrowser.open_new_tab("https://www.google.com/maps/dir/" + "/".join(list_loc))

print("région : " + r_json["places"][0]['state'])