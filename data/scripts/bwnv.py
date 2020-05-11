from data.scripts._util import check_energy_cost
from data.scripts.bwlt import energypress, ironbreaker
from card import get


def tackle(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(10, attacker)


def lightningball(attacker, defender):
    check_energy_cost(attacker, 3, Electric=2)
    defender.take_damage(50, attacker)


def dynamotor(user):
    if "dynamotor" in user.one_time_used:
        return
    if "electric" not in user.player.discard:  # and somehow check for special electric energy
        return
    energy = user.player.prompt_select_other(
        [get(i, user.player) for i in user.player.discard], "isenergy", _type="electric")
    target = user.player.prompt_select_ally("notactive")
    if "-" in energy.id:
        energy.data["overridecap"] = True
        energy.data["target"] = target
        energy.use()
    else:
        energy.override_cap = True
        energy.use(target)
    user.player.discard.remove(energy.id)
    user.one_time_used.append("dynamotor")


def dualchop(attacker, defender):
    check_energy_cost(attacker, 1)
    for _ in range(2):
        if attacker.player.flip_coin():
            defender.take_damage(10, attacker)


def scratch(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(20, attacker)


def dualchop2(attacker, defender):
    check_energy_cost(attacker, 2)
    for _ in range(2):
        if attacker.player.flip_coin():
            defender.take_damage(30, attacker)
