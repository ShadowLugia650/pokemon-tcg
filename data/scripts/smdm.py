from data.scripts._util import check_energy_cost
from data.scripts.smfl import photongeyser, skyscorchinglight
from card import get


def firestream(attacker, defender):
    check_energy_cost(attacker, 3, Fire=1)
    defender.take_damage(90, attacker)
    energy = attacker.player.prompt_select_other(attacker.energy.as_card_list(), _type="fire")
    attacker.energy["Fire"] -= 1
    attacker.other_attached.remove(energy.id)
    attacker.player.discard.append(energy.id)
    for p in defender.player.bench:
        p.take_damage(20, attacker, "noweak")


def firestarter(user):
    if "firestarter" in user.one_time_used:
        return
    if "fire" not in user.player.discard:
        return
    energy = user.player.prompt_select_other([get(i, user.player) for i in user.player.discard],
                                             "isenergy", _type="fire")
    target = user.player.prompt_select_ally("notactive")
    if "-" in energy.id:
        energy.data["overridecap"] = True
        energy.data["target"] = target
        energy.use()
    else:
        energy.override_cap = True
        energy.use(target)
    user.player.discard.remove(energy.id)
    user.one_time_used.append("firestarter")


def hydropump(attacker, defender):
    check_energy_cost(attacker, 1)
    damage = 10 + 20 * attacker.energy["Water"]
    defender.take_damage(damage, attacker)


def hydropump2(attacker, defender):
    check_energy_cost(attacker, 1)
    damage = 10 + 50 * attacker.energy["Water"]
    defender.take_damage(damage, attacker)


def reversethrust(attacker, defender):
    check_energy_cost(attacker, 1, Water=1)
    defender.take_damage(30, attacker)
    switch = attacker.player.prompt_select_ally("notactive")
    attacker.player.bench.remove(switch)
    attacker.player.bench.append(attacker)
    attacker.player.active = switch


def maelstrom(attacker, defender):
    check_energy_cost(attacker, 1, Water=1)
    defender.take_damage(40, attacker)
    for i in defender.player.bench:
        i.take_damage(40, attacker, "noweak", "nores")
