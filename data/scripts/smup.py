from data.scripts._util import check_energy_cost
from card import get
import random


def flare(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    defender.take_damage(20, attacker)


def burstpunch(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1)
    defender.take_damage(50, attacker)
    defender.tokens.append("burned")


def lusamine(item):
    for _ in range(2):
        card = item.player.prompt_select_other([get(i, item.player) for i in item.player.discard], "issupporter",
                                               "isstadium")
        item.player.hand.append(card)
        item.player.discard.remove(card.id)


def mars(item):
    for _ in range(2):
        item.player.hand.append(item.player.deck.draw())
    card = item.player.opponent.hand.pop(random.randint(0, len(item.player.opponent.hand)-1))
    item.player.opponent.discard.append(card.id)
