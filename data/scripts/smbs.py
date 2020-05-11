from data.scripts._util import check_energy_cost
from card import Flair, TrainerType


def scratch(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(10, attacker)


def flametail(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1)
    defender.take_damage(20, attacker)


def wingattack(attacker, defender):
    check_energy_cost(attacker, 3)
    defender.take_damage(70, attacker)


def crimsonstorm(attacker, defender):
    check_energy_cost(attacker, 5, Fire=3)
    defender.take_damage(300, attacker)
    for _ in range(3):
        energy = attacker.player.prompt_select_other(attacker.energy.as_card_list(), _type="fire")
        attacker.energy["Fire"] -= 1
        attacker.other_attached.remove(energy.id)
        attacker.player.discard.append(energy.id)


def ragingout(attacker, defender):
    if attacker.player.gx_used:
        return
    check_energy_cost(attacker, 3, Fire=1)
    for _ in range(10):
        defender.player.discard.append(defender.player.deck.stack.pop(0))
    attacker.player.gx_used = True


def aquaring(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(20, attacker)
    switch = attacker.player.prompt_select_ally()
    if switch in attacker.player.bench:
        attacker.player.bench.remove(switch)
        attacker.player.bench.append(attacker)
        attacker.player.active = switch


def hydroshot(attacker, defender):
    check_energy_cost(attacker, 3, Water=2)
    for _ in range(2):
        energy = attacker.player.prompt_select_other(attacker.energy.as_card_list(), _type="fire")
        attacker.energy["Fire"] -= 1
        attacker.other_attached.remove(energy.id)
        attacker.player.discard.append(energy.id)
    target = attacker.player.prompt_select_opp()
    if target == defender:
        defender.take_damage(120, attacker)
    else:
        target.take_damage(120, attacker, "noweak", "nores")


def tapustorm(attacker, defender):
    if attacker.player.gx_used:
        return
    if len(defender.player.bench) == 0:
        return
    if defender.item is not None:
        if defender.item.trainertype == TrainerType.FLRE:
            attacker.player.discard.append(defender.item.id)
        else:
            defender.player.deck.stack.append(defender.item.id)
        defender.item = None
    defender.player.deck.stack.extend(defender.special_energy)
    defender.player.deck.stack.extend(defender.other_attached)
    defender.special_energy = []
    defender.other_attached = []
    defender.energy.clear()
    defender.player.deck.stack.append(defender.id)
    defender.player.active = defender.player.prompt_select_ally("notactive", "remove")
    attacker.player.gx_used = True


def constrict(attacker, defender):
    check_energy_cost(attacker, 1, Dark=1)
    if attacker.player.flip_coin():
        defender.player.rotation = "paralyzed"


def tackle(attacker, defender):
    check_energy_cost(attacker, 2)
    defender.take_damage(20, attacker)


def prismaticburst(attacker, defender):
    check_energy_cost(attacker, 3)
    damage = 10
    if "Psychic" in attacker.energy.keys():
        damage += 60 * attacker.energy["Psychic"]
        attacker.energy.pop("Psychic")
    if "Prism" in attacker.energy.keys():
        damage += 60 * attacker.energy["Prism"]
        attacker.energy.pop("Prism")
    attacker.other_attached = [i for i in attacker.other_attached if i not in ["psychic", "bwnd-93/99"]]


def blackray(attacker, defender):
    if attacker.player.gx_used:
        return
    check_energy_cost(attacker, 3)
    for i in defender.player.bench + [defender]:
        if i.flair in [Flair.EX, Flair.GX]:
            i.take_damage(100, "noweak")
    attacker.player.gx_used = True


def lightsend(user):
    user.extra_effects["lightsend"] = True
