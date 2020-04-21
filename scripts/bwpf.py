from data.scripts._util import check_energy_cost


def pushdown(attacker, defender):
    check_energy_cost(attacker, 2, Dark=1)
    defender.take_damage(20, attacker)
    p = defender.player.prompt_select_ally("notactive", "remove")
    defender.player.bench.append(defender)
    defender.player.active = p


def bite(attacker, defender):
    check_energy_cost(attacker, 3, Dark=1)
    defender.take_damage(30, attacker)
