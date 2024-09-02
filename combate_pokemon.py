import os
import random
from pokeload import get_all_pokemons


def get_player_profile(pokemon_list):
    return {
        "player_name": input("Cual es tu nombre? "),
        "pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "pokeballs": 3,
        "health_potion": 2
    }


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def choose_pokemon(player_profile):
    choosen = None
    while not choosen:
        print("Elige con que pokemon lucharas\n")
        for index in range(len(player_profile["pokemon_inventory"])):
            print("{} - {}".format(index, get_pokemon_info(player_profile["pokemon_inventory"][index])))
        try:
            return player_profile["pokemon_inventory"][int(input("\nCual eliges? "))]
        except (ValueError, IndexError):
            print("Opcion invalida")


def test_pokemon(player_pokemon, player_profile):
    # Comprobamos si el pokemon seleccionado no esta fuera de combate con esta funcion
    if player_pokemon["current_health"] == 0:
        print("No puedes elegir a un Pokemon fuera de combate, escoge otro")
        choose_pokemon(player_profile)
    else:
        return player_pokemon


def choose_attack(player_pokemon):
    choosen = None
    while not choosen:
        print("Elige que ataque usaras\n")
        ataques = player_pokemon["attacks"]
        index = 0
        for ataque in ataques:
            if player_pokemon["level"] >= ataque["min_level"]:
                print("{} - {} [{}] - Nivel {}".format(index, ataque["name"], ataque["damage"], ataque["min_level"]))
            index += 1
        try:
            return player_pokemon["attacks"][int(input("\nQue habilidad quieres usar? "))]
        except (ValueError, IndexError):
            print("Opcion invalida")


def get_pokemon_info(pokemon):
    return "{} | lvl {} | hp {}/{}".format(pokemon["name"],
                                           pokemon["level"],
                                           pokemon["current_health"],
                                           pokemon["base_health"])


def player_attack(player_pokemon, enemy_pokemon):
    os.system("cls")
    habilidad_usada = choose_attack(player_pokemon)
    critical_damage = habilidad_usada["damage"] * 2
    print("\nHas usado la habilidad {} en {}".format(habilidad_usada["name"], enemy_pokemon["name"]))

    # Daño agregando un poco de los tipos de ataque y pokemon
    if habilidad_usada["type"] == "fuego" and enemy_pokemon["type"] == "planta":
        enemy_pokemon["current_health"] -= critical_damage
        print("El {} enemigo ha sufrido {} de daño, ha sido un golpe critico!".format(enemy_pokemon["name"], critical_damage))
    elif habilidad_usada["type"] == "planta" and enemy_pokemon["type"] == "agua":
        enemy_pokemon["current_health"] -= critical_damage
        print("El {} enemigo ha sufrido {} de daño, ha sido un golpe critico!".format(enemy_pokemon["name"], critical_damage))
    elif habilidad_usada["type"] == "agua" and enemy_pokemon["type"] == "fuego":
        enemy_pokemon["current_health"] -= critical_damage
        print("El {} enemigo ha sufrido {} de daño, ha sido un golpe critico!".format(enemy_pokemon["name"], critical_damage))
    elif habilidad_usada["type"] == "hielo" and enemy_pokemon["type"] == "planta" or enemy_pokemon["type"] == "agua":
        enemy_pokemon["current_health"] -= critical_damage
        print("El {} enemigo ha sufrido {} de daño, ha sido un golpe critico!".format(enemy_pokemon["name"], critical_damage))
    else:
        enemy_pokemon["current_health"] -= int(habilidad_usada["damage"])
        print("El {} enemigo ha sufrido {} de daño".format(enemy_pokemon["name"], habilidad_usada["damage"]))

    input("\nPulsa ENTER para continuar...")
    show_life(player_pokemon, enemy_pokemon)


def enemy_attack(enemy_pokemon, player_pokemon):
    os.system("cls")
    player_pokemon["current_health"] = 1
    enemy_attacks = enemy_pokemon["attacks"]
    random_attack = random.randint(0, len(enemy_attacks) - 1)
    attack = enemy_pokemon["attacks"][random_attack]
    """total_damage = int(attack["damage"]) / 2 # Dividimos el daño del enemigo para que no sea demasiado

    if total_damage < 1:
        total_damage = 1
    """
    print("El {} enemigo ha usado {}".format(enemy_pokemon["name"], attack["name"]))
    print("Tu {} ha sufrido {} de daño".format(player_pokemon["name"], attack["damage"]))
    player_pokemon["current_health"] -= attack["damage"]
    input("\nPulsa ENTER para continuar...")
    show_life(player_pokemon, enemy_pokemon)


def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1,  8)
        pokemon["current_exp"] += points
        # Le resto la experiencia de subir nivel y le subo la vida maxima 15 puntos
        while pokemon["current_exp"] >= 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["current_health"] = pokemon["base_health"] + 15
            print("Tu pokemon ha subido de nivel {}".format(get_pokemon_info(pokemon)))


def show_life(player_pokemon, enemy_pokemon):
    os.system("cls")
    # Miramos que la vida de los pokemons no baje de 0
    if player_pokemon["current_health"] < 0:
        player_pokemon["current_health"] = 0

    if enemy_pokemon["current_health"] < 0:
        enemy_pokemon["current_health"] = 0

    # Mostramos la vida de los pokemon
    grafic_player_pok = int((player_pokemon["current_health"] / player_pokemon["base_health"]) * 20)
    grafic_enemy_pok = int((enemy_pokemon["current_health"] / enemy_pokemon["base_health"]) * 20)
    print("\nLa vida de nuestro {} ({})".format(player_pokemon["name"], player_pokemon["current_health"]))
    print("♡" * grafic_player_pok)
    print("Vida {} ({})".format(enemy_pokemon["name"], enemy_pokemon["current_health"]))
    print("♡" * grafic_enemy_pok)
    # En caso de que nuestro pokemon haya perdido
    if player_pokemon["current_health"] <= 0:
        print("\nOh..., tu {} esta fuera de combate".format(player_pokemon["name"]))

    input("\nPulsa ENTER para continuar...")


def probability_calc(enemy_pokemon):
    # Calculamos el porcentaje de vida que le falta al pokmon enemigo
    health_percentage = (enemy_pokemon["base_health"] - enemy_pokemon["current_health"]) / enemy_pokemon[
        "base_health"] * 100

    # Aumentamos la probabilidad de captura segun la vida que le falta
    capture_probability = min(health_percentage, 75)  # Limitamos la probabilidad maxima al 75%

    # Generamos un numero aleatorio entre 1 y 100
    roll = random.randint(1, 100)

    # Si el numero aleatorio es menor o igual a la probabilidad de captura, se captura al pokemon
    return roll <= capture_probability


def capture_with_pokeball(player_profile, enemy_pokemon):
    os.system("cls")
    probability = probability_calc(enemy_pokemon)
    if player_profile["pokeballs"] > 0:
        if probability:
            print("{} ha sido capturado!!".format(enemy_pokemon["name"]))
        else:
            print("Ohhh... has fallado la captura, te quedan {} Pokeballs".format(player_profile["pokeballs"]))
    else:
        print("Que pena, no tienes Pokeballs!!")


def cure_pokemon(player_profile, player_pokemon):
    os.system("cls")
    if player_profile["health_potion"] > 0:
        player_pokemon["current_health"] += 50
        print("Tu {} ha sido curado! Ha recuperado 50 de salud".format(player_pokemon["name"]))
        if player_pokemon["current_health"] > 50:
            player_pokemon["current_health"] = 100
    else:
        print("No tienes pociones")


def player_info(player_profile):
    # Mostramos la informacion del jugador
    os.system("cls")
    print("Nombre del jugador: {}\nCombates: {}\nPokeballs: {}\nPociones: {}\n".format(player_profile["player_name"],
                                                                                     player_profile["combats"],
                                                                                     player_profile["pokeballs"],
                                                                                     player_profile["health_potion"]))


def fight(player_profile, enemy_pokemon):
    print("\n--- NUEVO COMBATE ---")

    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    test_pokemon(player_pokemon, player_profile)
    print("\nContrincantes: {} VS {}\n".format(get_pokemon_info(player_pokemon),
                                               get_pokemon_info(enemy_pokemon)))

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = None
        while action not in ["A", "P", "V", "C", "I"]:
            action = (input("Que deseas hacer: [A}tacar, [P]okeball, "
                            "Pocion de [V]ida, [C]ambiar, [I]nformacion ")).upper()

        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            # En caso de que ganemos, salimos del bucle
            if enemy_pokemon["current_health"] == 0:
                break

            attack_history.append(player_pokemon)
            enemy_attack(enemy_pokemon, player_pokemon)
        elif action == "P":
            # Si el usuario tiene pokeballs en el inventario se tira 1, hay una probabilidad de capturarlo relativa
            # a la salud restante del pokemon, cuando se captura, pasa a estar en el inventario con la misma salud que
            # tenia antes de capturarlo
            capture_with_pokeball(player_profile, enemy_pokemon )
        elif action == "V":
            # Si el usuario tiene curas en el inventario se aplica, cura 50 de vida hasta llegar a 100
            cure_pokemon(player_profile, player_pokemon)
        elif action == "C":
            player_pokemon = choose_pokemon(player_profile)
            test_pokemon(player_pokemon, player_profile)
            # Al cambiar de pokemon gastamos nuestro turno y el pokemon enemigo atacara
            enemy_attack(enemy_pokemon, player_pokemon)
        elif action == "I":
            player_info(player_profile)

        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
            player_pokemon = choose_pokemon(player_profile)
            test_pokemon(player_pokemon, player_profile)

    if enemy_pokemon["current_health"] == 0:
        print("HAS GANADO EL COMBATE!\n")
        player_profile["combats"] += 1
        assign_experience(attack_history)

    print("--- FIN DEL COMBATE ---\n")
    input("Presiona ENTER para continuar")


def item_lottery(player_profile):
    # Segun un factor aleatorio, al jugador le puede tocar una pokeball o una cura
    lottery = random.randint(1, 2)
    if lottery == 1:
        player_profile["pokeballs"] += 1
        print("El jugador ha recibido una POKEBALL por ganar el combate!")
    else:
        player_profile["health_potion"] += 1
        print("El jugador ha recibido una POCION por ganar el combate!")


def main():
    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)
    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        item_lottery(player_profile)

    print("Has perdido en el combate n{}".format(player_profile["combats"]))


if __name__ == "__main__":
    main()