from data.scripts._util import check_energy_cost


def luringflame(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    target = attacker.player.prompt_select_opp("notactive")
    defender.player.bench.append(defender)
    defender.player.bench.remove(target)
    defender.active = target
    target.tokens.append("burned")


def fierylicks(attacker, defender):
    check_energy_cost(attacker, 3, Fire=3)
    damage = 0
    for _ in range(4):
        card = attacker.player.deck.draw()
        if card.id == "fire":
            damage += 50
        attacker.player.discard.append(card.id)
    defender.take_damage(damage, attacker)


def heavybullet(attacker, defender):
    check_energy_cost(attacker, 3, Metal=2)
    defender.take_damage(70, attacker)
    if attacker.player.flip_coin():
        attacker.player.prompt_select_opp("notactive").take_damage(20, attacker, "noweak")


def plasmasteel(user):
    user.player.global_abilities.append("plasmasteel")


def colress(item):
    item.player.deck.stack.extend([i.id for i in item.player.hand])
    item.player.hand = []
    item.player.deck.shuffle_curr()
    for _ in range(len(item.player.bench)+len(item.player.opponent.bench)):
        item.player.hand.append(item.player.deck.draw())


def escaperope(item):
    oppswitch = item.player.opponent.prompt_select_ally("notactive", "remove")
    item.player.opponent.bench.append(item.player.opponent.active)
    item.player.opponent.active = oppswitch
    switch = item.player.prompt_select_ally("notactive", "remove")
    item.player.bench.append(item.player.active)
    item.player.active = switch


def hypnotox(item):
    item.player.opponent.active.tokens.append("poison")
    if item.player.flip_coin():
        item.player.opponent.active.rotation = "sleep"


def hydropump(attacker, defender):
    check_energy_cost(attacker, 4)
    damage = 60 + 10*attacker.energy["Water"]
    defender.take_damage(damage, attacker)


def deluge(user):
    user.player.global_abilities.append("deluge")
