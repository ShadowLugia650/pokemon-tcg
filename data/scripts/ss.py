from data.scripts._util import check_energy_cost
from card import get


def spreadingflames(attacker, defender):
    check_energy_cost(attacker, 1)
    for _ in range(3):
        if "fire" not in attacker.player.discard:
            return
        energy = attacker.player.prompt_select_other([get(i, attacker.player) for i in attacker.player.discard],
                                                     "isenergy", _type="fire")
        target = attacker.player.prompt_select_ally()
        if "-" in energy.id:
            energy.data["overridecap"] = True
            energy.data["target"] = target
            energy.use()
        else:
            energy.override_cap = True
            energy.use(target)
        attacker.player.discard.remove(energy.id)


def energyburst(attacker, defender):
    check_energy_cost(attacker, 2, Fire=2)
    damage = 30 * (attacker.energy.total() + defender.energy.total())
    defender.take_damage(damage, attacker)


def bodysurf(attacker, defender):
    check_energy_cost(attacker, 1)
    if "water" not in [i.id for i in attacker.player.hand]:
        return
    energy = attacker.player.prompt_card_from_hand("isenergy", _type="water")
    target = attacker.player.prompt_select_ally("notactive")
    if "-" in energy.id:
        energy.data["overridecap"] = True
        energy.data["target"] = attacker
        energy.use()
    else:
        energy.override_cap = True
        energy.use(attacker)
    attacker.player.bench.append(attacker)
    attacker.player.active = target
    attacker.player.bench.remove(target)


def oceanloop(attacker, defender):
    check_energy_cost(attacker, 4, Water=3)
    defender.take_damage(210, attacker)
    for _ in range(2):
        energy = attacker.player.prompt_select_other(attacker.energy.as_card_list(), _type="water")
        attacker.player.hand.append(energy)
        attacker.energy["Water"] -= 1
        if attacker.energy["Water"] == 0:
            attacker.energy.pop("Water")
        attacker.other_attached.remove("water")


def gmaxpump(attacker, defender):
    check_energy_cost(attacker, 3)
    damage = 90 + 30 * attacker.energy["Water"]
    defender.take_damage(damage, attacker)


def ram(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(10, attacker)


def aurorabeam(attacker, defender):
    check_energy_cost(attacker, 2, Water=1)
    defender.take_damage(30, attacker)


def icedance(user):
    user.player.global_abilities.append("icedance")


def palpad(item):
    for _ in range(2):
        supp = item.player.prompt_select_other([get(i, item.player) for i in item.player.discard], "issupporter")
        item.player.discard.remove(supp.id)
        item.player.deck.stack.append(supp.id)
        item.player.deck.shuffle_curr()


def ordrod(item):
    pass
