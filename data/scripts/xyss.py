from data.scripts._util import check_energy_cost
from data.scripts.xy import oblivionwing, darknessblade


def scratch(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(20, attacker)


def flare(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1)
    defender.take_damage(30, attacker)
