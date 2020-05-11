from data.scripts._util import check_energy_cost


def desperateslap(attacker, defender):
    check_energy_cost(attacker, 2, Psychic=1)
    damage = 60 if attacker.maxhp - attacker.hp >= 50 else 20
    defender.take_damage(damage, attacker)


def cynthguide(item):
    cards = []
    for _ in range(7):
        cards.append(item.player.deck.draw())
    sel = item.player.prompt_select_other(cards, "remove")
    item.player.hand.append(sel)
    item.player.deck.stack.append(cards)
    item.player.deck.shuffle_curr()
