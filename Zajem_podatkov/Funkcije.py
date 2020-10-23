import requests
import re
import os
import csv

mapa = "zajeti_podatki"
pokemoni = "pokemoni.html"
poteze = "moves.html"
url_pokemoni = "https://play.pokemonshowdown.com/data/pokedex.js"
url_poteze = "https://dex.pokemonshowdown.com/moves/"

def nalozi_spletno_stran(url):
    try:
        vsebina_strani = requests.get(url)
    except Exception as e:
        print("Prišlo je do napake!")
        print(e)
        return None
    if vsebina_strani.status_code == requests.codes["ok"]:
        return vsebina_strani.text
    else:
        print("Težava pri nalaganju spletne strani.")
        return None

def shrani_spletno_stran(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return None

def shrani_v_datoteko(page, directory, filename):
    html = nalozi_spletno_stran(page)
    if html:
        shrani_spletno_stran(html, directory, filename)
        return True
    return False



