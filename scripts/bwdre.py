from data.scripts._util import check_energy_cost
from data.scripts.bw import celestialroar, dragonburst
from data.scripts.bwlt import dragonblast, darktrance


def crunch(attacker, defender):
    check_energy_cost(attacker, 2)
    defender.take_damage(30, attacker)
    if attacker.player.flip_coin():
        _type = defender.player.prompt_select_other(defender.energy.keys())
        defender.energy[_type] -= 1
        if defender.energy[_type] == 0:
            defender.energy.pop(_type)
        defender.player.discard.append(_type)


def dragonclaw(attacker, defender):
    check_energy_cost(attacker, 3, Psychic=1, Dark=2)
    defender.take_damage(80, attacker)


def rescuescarf_added(target):
    target.extra_effects["rescuescarf"] = True
