import re
import funkcije


url_poteze = "https://play.pokemonshowdown.com/data/moves.js"
url_abilities = "https://play.pokemonshowdown.com/data/abilities.js"

vzorec_bloka_pokemon = re.compile(
    r'.:{num:.*?,tier:.*?},',
    flags=re.DOTALL
)

vzorec_pokemona = re.compile(
    r'num:(?P<ID>\d+),.*?'
    r'name:(?P<Name>.*?),.*?'
    r'types:\[(?P<type1>.*?)\],.*?'
    r'baseStats:\{hp:(?P<HP>\d+),atk:(?P<Attack>\d+),def:(?P<Defense>\d+),spa:(?P<Attack_special>\d+),spd:(?P<Defense_special>\d+),spe:(?P<Speed>\d+)\},.*?'
    r'abilities:\{(?P<ability1>.*?)\},.*?'
    r'heightm:(?P<Height>.*?),weightkg:(?P<Weight>.*?),.*?',
    flags=re.DOTALL
)

def izloci_podatke_pokemona(blok):
    try:
        pokemon = vzorec_pokemona.search(blok).groupdict()
        #popravimo id in ime pokemona
        pokemon["ID"] = int(pokemon["ID"])
        pokemon["Name"] = pokemon["Name"].replace('"', '').replace('\\', '')
        #pogledamo ce ima pokemon vec tipov, ce jih ima jih locimo
        pokemon["type1"] = pokemon["type1"].replace('"', '').replace('\\', '').split(",")
        if len(pokemon["type1"]) > 1:
            pokemon["type2"] = pokemon["type1"][1]
            pokemon["type1"] = pokemon["type1"][0]
        else:
            pokemon["type1"] = pokemon["type1"][0]
        #popravimo ostale podatke, ki morajo biti stevilke
        pokemon["HP"] = int(pokemon["HP"])
        pokemon["Attack"] = int(pokemon["Attack"])
        pokemon["Defense"] = int(pokemon["Defense"])
        pokemon["Attack_special"] = int(pokemon["Attack_special"])
        pokemon["Defense_special"] = int(pokemon["Defense_special"])
        pokemon["Speed"] = int(pokemon["Speed"])
        pokemon["Height"] = float(pokemon["Height"])
        pokemon["Weight"] = float(pokemon["Weight"])
        #podobno kot pri tipu pokemona pogledamo koliko ima ablilitijev, ce jih je vec to ustrezno popravimo
        #vemo, da imajo pokemoni največ 2 ability-ja, hkrati pa vemo, da sta prva dva znaka stringa abiliti stevilka in :, zato ju odstranimo
        pokemon["ability1"] = pokemon["ability1"].replace('"', '').replace('\\', '').split(",")
        if len(pokemon["ability1"]) > 1:
            pokemon["ability2"] = pokemon["ability1"][1][2:]
            pokemon["ability1"] = pokemon["ability1"][0][2:]
        else:
            pokemon["ability1"] = pokemon["ability1"][0][2:]
        #pokemonom dodamo generacijo v kateri so se pojavili
        if pokemon["ID"] < 152:
            pokemon["Generation"] = 1
        elif pokemon["ID"] < 252:
            pokemon["Generation"] = 2
        elif pokemon["ID"] < 387:
            pokemon["Generation"] = 3
        elif pokemon["ID"] < 494:
            pokemon["Generation"] = 4
        elif pokemon["ID"] < 650:
            pokemon["Generation"] = 5
        elif pokemon["ID"] < 722:
            pokemon["Generation"] = 6
        elif pokemon["ID"] < 810:
            pokemon["Generation"] = 7
        else:
            pokemon["Generation"] = 8
        #vrnemo le pokemone z pozitivnim id-jem, na strani so tudi fan-made pokemoni, ki imajo to vrednost negativno
        if pokemon["ID"] > 0:
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
    ["ID", "Name", "type1", "type2", "HP", "Attack", "Defense", "Speed", "Attack_special", "Defense_special", "ability1", "ability2", "Generation", "Height", "Weight"], "obdelani_podatki/pokemoni.csv"
)

