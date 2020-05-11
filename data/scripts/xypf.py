from data.scripts._util import check_energy_cost


def slashblast(attacker, defender):
    check_energy_cost(attacker, 3)
    damage = 40 + attacker.energy["Metal"] * 20
    defender.take_damage(damage, attacker)


def mightyshield(user):
    user.extra_effects["mightyshield"] = 1


def dce_added(target):
    if "Double Colorless" in target.energy.keys():
        target.energy["Double Colorless"] += 2
    else:
        target.energy["Double Colorless"] = 2
