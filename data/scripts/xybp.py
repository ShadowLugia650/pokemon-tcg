from data.scripts._util import check_energy_cost


def smack(attacker, defender):
    check_energy_cost(attacker, 1, Water=1)
    defender.take_damage(20, attacker)


def mineralpump(attacker, defender):
    check_energy_cost(attacker, 2, Water=2)
    defender.take_damage(60, attacker)
    for i in attacker.player.bench:
        i.take_damage(-30, attacker, "nomod")


def aquatube(user):
    user.player.global_abilities.append("aquatube")


def darkpulse(attacker, defender):
    check_energy_cost(attacker, 2)
    damage = 20 + 20 * attacker.energy["Dark"]
    for i in attacker.player.bench:
        damage += 20 * i.energy["Dark"]
    defender.take_damage(damage, attacker)


def darkhead(attacker, defender):
    check_energy_cost(attacker, 3, Dark=1)
    damage = 160 if "sleep" == defender.rotation else 80
    defender.take_damage(damage, attacker)


def skyla(item):
    item.player.hand.append(item.player.prompt_card_from_deck("istrainer"))
