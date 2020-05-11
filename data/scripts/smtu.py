from data.scripts._util import check_energy_cost
from card import get


def tackle(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(10, attacker)


def rainsplash(attacker, defender):
    check_energy_cost(attacker, 2, Water=1)
    defender.take_damage(20, attacker)


def brockgrit(item):
    for _ in range(6):
        card = item.player.prompt_select_other([get(i) for i in item.player.discard], "ispokemon", "isenergy",
                                               basic="energy")
        item.player.deck.stack.append(card.id)
        item.player.discard.remove(card.id)
        item.player.deck.shuffle_curr()


def supersplash(attacker, defender):
    check_energy_cost(attacker, 5, Water=5)
    defender.take_damage(180, attacker)


def toweringsplash(attacker, defender):
    if attacker.player.gx_used:
        return
    check_energy_cost(attacker, 1, Water=1)
    defender.take_damage(10, attacker)
    if attacker.energy["Water"] >= 8:
        for i in defender.player.bench:
            i.take_damage(100, attacker, "noweak", "nores")
    attacker.player.gx_used = True
