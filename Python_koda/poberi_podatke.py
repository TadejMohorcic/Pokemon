import re
import funkcije


#====================================================================================================
#Vzorci za regex

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

vzorec_bloka_moves = re.compile(
    r':\{num.*?,shortDesc:.*?}',
    flags=re.DOTALL
)

vzorec_moves = re.compile(
    r'num:(?P<ID>\d+),.*?'
    r'accuracy:(?P<Accuracy>.*?),.*?'
    r'basePower:(?P<BasePower>\d+),.*?'
    r'category:(?P<Category>.*?),.*?'
    r'name:(?P<Name>.*?),pp:(?P<PP>\d+),.*?'
    r'type:(?P<Type>.*?),.*?'
    r'desc:(?P<Description>.*?),shortDesc:.*?',
    flags=re.DOTALL
)

#====================================================================================================
#Pomožne funkcije

def izloci_znake(niz):
    return niz.replace('"', '').replace('\\', '')

#====================================================================================================
#Funkcija za pokemone

def izloci_podatke_pokemona(blok):
    try:
        pokemon = vzorec_pokemona.search(blok).groupdict()
        #Popravimo id in ime pokemona
        pokemon["ID"] = int(pokemon["ID"])
        pokemon["Name"] = izloci_znake(pokemon["Name"])
        #Pogledamo, če ima pokemon vec tipov, in če jih ima, ju ločimo
        #Vemo pa, da ima pokemon največ 2 tipa
        pokemon["type1"] = izloci_znake(pokemon["type1"]).split(",")
        if len(pokemon["type1"]) > 1:
            pokemon["Type 2"] = pokemon["type1"][1]
            pokemon["Type 1"] = pokemon["type1"][0]
        else:
            pokemon["Type 1"] = pokemon["type1"][0]
        del pokemon["type1"]
        #Popravimo ostale podatke, tako da nastanejo številke(int ali float)
        pokemon["HP"] = int(pokemon["HP"])
        pokemon["Attack"] = int(pokemon["Attack"])
        pokemon["Defense"] = int(pokemon["Defense"])
        pokemon["Speed"] = int(pokemon["Speed"])
        pokemon["Height"] = float(pokemon["Height"])
        pokemon["Weight"] = float(pokemon["Weight"])
        #Olepšamo ime za special attack and defense, ter izbrišemo nepotrebne
        pokemon["Attack Special"] = int(pokemon["Attack_special"])
        del pokemon["Attack_special"]
        pokemon["Defense Special"] = int(pokemon["Defense_special"])
        del pokemon["Defense_special"]
        #Vemo, da ima pokemon največ 2 ability-je, kjer je zadnji vedno "Hidden", razen v primeru, ko ima pokemon le en ability
        #Hkrati sta prva dva znaka v našem html-ju odveč, zato ju odstranimo
        pokemon["ability1"] = izloci_znake(pokemon["ability1"]).split(",")
        if len(pokemon["ability1"]) == 1:
            pokemon["Ability 1"] = pokemon["ability1"][0][2:]
        else:
            pokemon["Hidden Ability"] = pokemon["ability1"][-1][2:]
            if len(pokemon["ability1"]) == 3:
                pokemon["Ability 1"] = pokemon["ability1"][0][2:]
                pokemon["Ability 2"] = pokemon["ability1"][1][2:]
            else:
                pokemon["Ability 1"] = pokemon["ability1"][0][2:]
        del pokemon["ability1"]
        #pokemonom dodamo generacijo v kateri so se pojavili prvic
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

#====================================================================================================
#Funkcija za poteze

def izloci_podatke_moves(blok):
    try:
        move = vzorec_moves.search(blok).groupdict()
        #Popravimo podatke, ki morajo biti številke v le te, ter nepotrebne izbrišemo(olepšam imena)
        move["Base Power"] = int(move["BasePower"])
        del move["BasePower"]
        move["PP"] = int(move["PP"])
        move["ID"] = int(move["ID"])
        #Izločimo nepotrebne znake iz naših nizov
        move["Category"] = izloci_znake(move["Category"])
        move["Name"] = izloci_znake(move["Name"])
        move["Type"] = izloci_znake(move["Type"])
        move["Description"] = izloci_znake(move["Description"])
        #Uredimo se accuracy, kjer se lahko pojavi številka (procent), ali pa true
        try:
            move["Accuracy"] = int(move["Accuracy"])
        except:
            move["Accuracy"] = move["Accuracy"].capitalize()
        #Vrnemo le poteze s pozitivnim ID-jem, isti razlog kot zgoraj
        if move["ID"] > 0:
            return move
        else:
            return None
    except:
        return None

#====================================================================================================

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
    ["ID", "Name", "Type 1", "Type 2", "HP", "Attack", "Defense", "Speed", "Attack Special", "Defense Special", "Ability 1", "Ability 2", "Hidden Ability", "Generation", "Height", "Weight"], "obdelani_podatki/pokemoni.csv"
)

#====================================================================================================

def st_moves():
    url_moves = "https://play.pokemonshowdown.com/data/moves.js"
    ime_datoteke = "zajeti_podatki/moves.html"
    funkcije.shrani_spletno_stran(url_moves, ime_datoteke)
    vsebina = funkcije.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka_moves.finditer(vsebina):
        yield izloci_podatke_moves(blok.group(0))

moves = []
for move in st_moves():
    if move != None:
        moves.append(move)
moves = sorted(moves, key=lambda x : x["ID"], reverse=False)
funkcije.zapisi_json(moves, "obdelani_podatki/moves.json")
funkcije.zapisi_csv(
    moves,
    ["ID", "Name", "Type", "Category", "Accuracy", "Base Power", "PP", "Description"], "obdelani_podatki/moves.csv"
)
