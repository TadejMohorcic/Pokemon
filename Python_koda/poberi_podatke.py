import re
import funkcije

url_poteze = "https://play.pokemonshowdown.com/data/moves.js"
url_abilities = "https://play.pokemonshowdown.com/data/abilities.js"

vzorec_bloka_pokemon = re.compile(
    r'.:{num:.*?,tier:.*?},',
    flags=re.DOTALL
)

vzorec_pokemona = re.compile(
    r'num:(?P<id>\d+),.*?'
    r'name:(?P<name>.*?),.*?'
    r'types:\[(?P<type>.*?)\],.*?'
    r'baseStats:\{hp:(?P<hp>\d+),atk:(?P<attack>\d+),def:(?P<defense>\d+),spa:(?P<attack_special>\d+),spd:(?P<defense_special>\d+),spe:(?P<speed>\d+)\},.*?'
    r'abilities:\{(?P<abilities>.*?)\},.*?'
    r'heightm:(?P<height>.*?),weightkg:(?P<weight>.*?),.*?',
    flags=re.DOTALL
)

def izloci_podatke_pokemona(blok):
    try:
        pokemon = vzorec_pokemona.search(blok).groupdict()
        pokemon["id"] = int(pokemon["id"])
        pokemon["name"] = pokemon["name"].replace('"', '').replace('\\', '')
        pokemon["type"] = pokemon["type"].replace('"', '').replace('\\', '').split(",")
        pokemon["hp"] = int(pokemon["hp"])
        pokemon["attack"] = int(pokemon["attack"])
        pokemon["defense"] = int(pokemon["defense"])
        pokemon["attack_special"] = int(pokemon["attack_special"])
        pokemon["defense_special"] = int(pokemon["defense_special"])
        pokemon["speed"] = int(pokemon["speed"])
        pokemon["height"] = float(pokemon["height"])
        pokemon["weight"] = float(pokemon["weight"])
        pokemon["abilities"] = pokemon["abilities"].replace('"', '').replace('\\', '').split(",")
        return pokemon
    except:
        return None



def st_pokemonov():
    url_pokemoni = "https://play.pokemonshowdown.com/data/pokedex.js"
    ime_datoteke = "zajeti_podatki/pokemoni.html"
    funkcije.shrani_spletno_stran(url_pokemoni, ime_datoteke)
    vsebina = funkcije.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka_pokemon.finditer(vsebina):
        yield izloci_podatke_pokemona(blok.group(0))

pokemoni = []
for pokemon in st_pokemonov():
    if pokemon != None:
        pokemoni.append(pokemon)
funkcije.zapisi_json(pokemoni, "obdelani_podatki/pokemoni.json")

