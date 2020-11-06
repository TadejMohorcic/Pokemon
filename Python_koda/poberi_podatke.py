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
    r'types:\[(?P<type1>.*?)\],.*?'
    r'baseStats:\{hp:(?P<hp>\d+),atk:(?P<attack>\d+),def:(?P<defense>\d+),spa:(?P<attack_special>\d+),spd:(?P<defense_special>\d+),spe:(?P<speed>\d+)\},.*?'
    r'abilities:\{(?P<ability1>.*?)\},.*?'
    r'heightm:(?P<height>.*?),weightkg:(?P<weight>.*?),.*?',
    flags=re.DOTALL
)

def izloci_podatke_pokemona(blok):
    try:
        pokemon = vzorec_pokemona.search(blok).groupdict()
        #popravimo id in ime pokemona
        pokemon["id"] = int(pokemon["id"])
        pokemon["name"] = pokemon["name"].replace('"', '').replace('\\', '')
        #pogledamo ce ima pokemon vec tipov, ce jih ima jih locimo
        pokemon["type1"] = pokemon["type1"].replace('"', '').replace('\\', '').split(",")
        if len(pokemon["type1"]) > 1:
            pokemon["type2"] = pokemon["type1"][1]
            pokemon["type1"] = pokemon["type1"][0]
        else:
            pokemon["type1"] = pokemon["type1"][0]
        #popravimo ostale podatke, ki morajo biti stevilke
        pokemon["hp"] = int(pokemon["hp"])
        pokemon["attack"] = int(pokemon["attack"])
        pokemon["defense"] = int(pokemon["defense"])
        pokemon["attack_special"] = int(pokemon["attack_special"])
        pokemon["defense_special"] = int(pokemon["defense_special"])
        pokemon["speed"] = int(pokemon["speed"])
        pokemon["height"] = float(pokemon["height"])
        pokemon["weight"] = float(pokemon["weight"])
        #podobno kot pri tipu pokemona pogledamo koliko ima ablilitijev, ce jih je vec to ustrezno popravimo
        #vemo, da imajo pokemoni največ 2 ability-ja, hkrati pa vemo, da sta prva dva znaka stringa abiliti stevilka in :, zato ju odstranimo
        pokemon["ability1"] = pokemon["ability1"].replace('"', '').replace('\\', '').split(",")
        if len(pokemon["ability1"]) > 1:
            pokemon["ability2"] = pokemon["ability1"][1][2:]
            pokemon["ability1"] = pokemon["ability1"][0][2:]
        else:
            pokemon["ability1"] = pokemon["ability1"][0][2:]
        #vrnemo le pokemone z pozitivnim id-jem, na strani so tudi fan-made pokemoni, ki imajo to vrednost negativno
        if pokemon["id"] > 0:
            return pokemon
        else:
            return None
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
funkcije.zapisi_csv(
    pokemoni,
    ["id", "name", "type1", "type2", "hp", "attack", "defense", "speed", "attack_special", "defense_special", "ability1", "ability2", "height", "weight"], "obdelani_podatki/pokemoni.csv"
)

