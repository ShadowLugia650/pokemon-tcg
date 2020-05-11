from data.scripts._util import check_energy_cost
from data.scripts.smbs import prismaticburst, blackray, lightsend, wingattack, crimsonstorm, ragingout
from data.scripts.smfl import photongeyser, skyscorchinglight
from card import TrainerCard, TrainerType


def hau(item):
    for _ in range(3):
        item.player.hand.append(item.player.deck.draw())


def nestball(item):
    if len(item.player.bench) == 5:
        return
    c = item.player.prompt_card_from_deck("ispokemon", "basic")
    item.player.bench.append(c)


def ragingdestruction(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    for _ in range(8):
        c = attacker.player.deck.draw()
        if c.id == "fire":
            c.override_cap = True
            c.use(attacker)
        elif type(c) == TrainerCard and c.trainertype == TrainerType.ENRG:
            c.data["overridecap"] = True
            c.data["target"] = attacker
            c.use()
        else:
            attacker.player.discard.append(c.id)


def steamartillery(attacker, defender):
    check_energy_cost(attacker, 5, Fire=2)
    defender.take_damage(200, attacker)


def dreadfulflames(attacker, defender):
    if attacker.player.gx_used:
        return
    check_energy_cost(attacker, 5, Fire=2)
    defender.take_damage(250, attacker)
    for i in defender.player.hand+[defender]:
        if i.energy.total() > 1:
            e = attacker.player.prompt_select_other(i.energy.as_card_list())
            i.other_attached.remove(e.id)
            i.energy[e.id.title()] -= 1
            if i.energy[e.id.title()] == 0:
                i.energy.pop(e.id.title())
        elif i.energy.total() == 1:
            eid = i.energy.keys()[0]
            i.other_attached.remove(eid)
            i.energy.pop(eid.title())


def argentwing(attacker, defender):
    check_energy_cost(attacker, 3)
    damage = 60
    if len(defender.global_abilities) + len(defender.abilities) + len(defender.personal_abilities) > 0:
        damage += 60
    defender.take_damage(damage, attacker)


def aeroforce(attacker, defender):
    check_energy_cost(attacker, 4)
    defender.take_damage(130)
    energy = attacker.player.prompt_select_other(attacker.energy.as_card_list())
    attacker.energy[energy.typestring] -= 1
    attacker.other_attached.remove(energy.id)
    attacker.player.discard.append(energy.id)
