import requests
import re
import os
import csv

mapa_podatki = "Zajeti_podatki"
pokemoni = "pokemoni.html"
poteze = "moves.html"
abilities = "abilities.html"
url_pokemoni = "https://play.pokemonshowdown.com/data/pokedex.js"
url_poteze = "https://play.pokemonshowdown.com/data/moves.js"
url_abilities = "https://play.pokemonshowdown.com/data/abilities.js"

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

def main(redownload=True, reparse=True):
    shrani_v_datoteko(url_pokemoni, mapa_podatki, pokemoni)
    shrani_v_datoteko(url_poteze, mapa_podatki, poteze)
    shrani_v_datoteko(url_abilities, mapa_podatki, abilities)

if __name__ == "__main__":
    main()