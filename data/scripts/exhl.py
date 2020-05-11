from data.scripts._util import check_energy_cost


def metalcharge(attacker, defender):
    check_energy_cost(attacker, 2, Metal=1)
    defender.take_damage(30, attacker)
    attacker.take_damage(10, attacker, "noweak")


def magneticcall(user):
    if user.player.flip_coin():
        user.player.prompt_card_from_deck("ispokemon", "basic", _type="metal")
