from data.scripts._util import check_energy_cost


def finsmack(attacker, defender):
    check_energy_cost(attacker, 1, Water=1)
    for _ in range(2):
        if attacker.player.flip_coin():
            defender.take_damage(10, attacker)


def pushdown(attacker, defender):
    check_energy_cost(attacker, 2, Dark=1)
    defender.take_damage(20, attacker)
    p = defender.player.prompt_select_ally("notactive", "remove")
    defender.player.bench.append(defender)
    defender.player.active = p


def bite(attacker, defender):
    check_energy_cost(attacker, 3, Dark=1)
    defender.take_damage(30, attacker)
