import os
import pickle
from requests_html import HTMLSession
import random

# Diccionario base de todos los pokemons
pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0
}

URL_BASE = "https://pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_pokemon&pk="


def get_pokemon(index):
    url = "{}{}".format(URL_BASE, index)
    session = HTMLSession()

    try:
        new_pokemon = pokemon_base.copy()
        pokemon_page = session.get(url)

        new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text.split("\n")[0]
        new_pokemon["type"] = []

        for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
            new_pokemon["type"].append(img.attrs["alt"])

        new_pokemon["attacks"] = []

        for index, attack_item in enumerate(pokemon_page.html.find(".pkmain")[-1].find("tr .check3")):
            attack = {
                "name": attack_item.find("td", first=True).find("a", first=True).text,
                "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
                "damage": int(attack_item.find("td")[2].text.replace("--", "0")),
            }

            if index < 3:
                # Las tres primeras habilidades tienen nivel 1
                attack["min_level"] = 1
            else:
                # Para el resto de ataques, se asigna un nivel aleatorio entre 1 y 50
                attack["min_level"] = random.randint(1, 50)
            new_pokemon["attacks"].append(attack)

        return new_pokemon
    except Exception as e:
        return f"Error al obtener el tipo: {str(e)}"


def barr_progres(index):
    os.system("cls")

    porcen = int(index*100/150)
    n_diferencia = 10
    n_porcen = int(porcen/10)
    n_diferencia -= n_porcen

    barra = ("""Cargando los pokemons en la base de datos: \n|{}{}|""".format("*" * n_porcen, " " * n_diferencia,))
    print("{}  {}%, {} de 150 pokemos completado".format(barra, porcen, index))


def get_all_pokemons():
    try:
        print("Cargando el archivo de pokemons...")
        with open("pokefile.pkl", "rb") as pokefile:
            all_pokemons = pickle.load(pokefile)
    except FileNotFoundError:
        print("Archivo no encontrado! Cargando de internet...")
        all_pokemons = []
        for index in range(151):
            all_pokemons.append(get_pokemon(index + 1))
            barr_progres(index)

        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)
        print("\nTodos los pokemons han sido descargados!")

    print("Lista de pokemons cargada!")
    return all_pokemons


