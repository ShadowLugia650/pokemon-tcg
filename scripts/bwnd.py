from data.scripts._util import check_energy_cost


def levelball(item):
    item.player.hand.append(item.player.prompt_card_from_deck("ispokemon", hpmax=90))


def prismenergy_added(target):
    if "Prism" in target.energy.keys():
        target.energy["Prism"] += 1
    else:
        target.energy["Prism"] = 1


def heatcrash(attacker, defender):
    check_energy_cost(attacker, 4, Fire=2)
    defender.take_damage(80, attacker)


def infernofandango(user):
    user.player.global_abilities.append("infernofandango")
