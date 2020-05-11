from data.scripts._util import check_energy_cost


def waterarrow(attacker, defender):
    check_energy_cost(attacker, 1, Water=1)
    target = attacker.player.prompt_select_opp()
    if target == defender:
        defender.take_damage(20, attacker)
    else:
        target.take_damage(20, attacker, "noweak", "nores")


def surf(attacker, defender):
    check_energy_cost(attacker, 3, Water=1)
    defender.take_damage(50, attacker)
