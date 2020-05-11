from data.scripts._util import check_energy_cost


def scratch(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(10, attacker)


def tailsmack(attacker, defender):
    check_energy_cost(attacker, 2)
    defender.take_damage(20, attacker)
