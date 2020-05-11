from data.scripts._util import check_energy_cost


def razorfin(attacker, defender):
    check_energy_cost(attacker, 1, Electric=1)
    defender.take_damage(20, attacker)


def dragonaxe(attacker, defender):
    check_energy_cost(attacker, 1, Metal=1)
    damage = 40*(attacker.energy["Metal"]+attacker.energy["Prism"]+attacker.energy["WEFM"])
    defender.take_damage(damage, attacker)


def champstrike(attacker, defender):
    check_energy_cost(attacker, 2, Metal=1, Fighting=1)
    defender.take_damage(9999, attacker)


def pokemoncatcher(item):
    target = item.player.prompt_select_opp("notactive", "remove")
    item.player.opponent.bench.append(item.player.opponent.active)
    item.player.opponent.active = target


def ultraball(item):
    d1 = item.player.prompt_card_from_hand()
    d2 = item.player.prompt_card_from_hand()
    item.player.discard.append(d1.id)
    item.player.discard.append(d2.id)
    c = item.player.prompt_card_from_deck("ispokemon")
    item.player.hand.append(c)


def masterball(item):
    item.player.hand.append(item.player.prompt_card_from_deck("ispokemon"))
