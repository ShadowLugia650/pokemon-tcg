from data.scripts._util import check_energy_cost


def pierce(attacker, defender):
    check_energy_cost(attacker, 2, Metal=2)
    defender.take_damage(2, attacker)


def steelfeelers(attacker, defender):
    check_energy_cost(attacker, 1, Metal=1)
    for _ in range(3):
        if attacker.player.flip_coin():
            defender.take_damage(30, attacker)


def gyroball(attacker, defender):
    check_energy_cost(attacker, 3, Metal=1)
    defender.take_damage(60, attacker)
    switch = attacker.player.prompt_select_ally("notactive", "remove")
    attacker.player.bench.append(attacker)
    attacker.player.active = switch
    switch = defender.player.prompt_select_ally("notactive", "remove")
    defender.player.bench.append(defender)
    defender.player.active = switch


def spinningattack(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.take_damage(10, attacker)


def geargrind(attacker, defender):
    check_energy_cost(attacker, 3, Metal=1)
    for _ in range(2):
        if attacker.player.flip_coin():
            defender.take_damage(30, attacker)


def metalsound(attacker, defender):
    check_energy_cost(attacker, 1)
    defender.rotation = "confused"


def guardpress(attacker, defender):
    check_energy_cost(attacker, 3, Metal=2)
    defender.take_damage(60, attacker)
    # reduce damage dealt from defender to attacker


def recycle(item):
    if item.player.flip_coin():
        card = item.player.prompt_select_other(item.player.discard, "remove")
        item.player.deck.stack.insert(0, card)
