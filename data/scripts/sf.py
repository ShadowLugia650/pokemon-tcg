# NOTE: THIS FILE CONTAINS DATA FOR FAKE POKEMON CARDS!
from data.scripts._util import check_energy_cost


def creativeburst(attacker, defender):
    if attacker.player.gx_used:
        return
    check_energy_cost(attacker, 4, Psychic=2)
    for _ in range(2):
        attacker.player.play_pokemon(attacker.player.prompt_card_from_deck("ispokemon"))
    attacker.player.gx_used = True


def geneticbaseline(user):
    pass


def abilitycommand(user):
    ally = user.player.prompt_select_ally("notactive", "skippable")
    user.personal_abilities = ally.personal_abilities
    user.abilities = ally.abilities
