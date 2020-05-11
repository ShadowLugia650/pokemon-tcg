from data.scripts._util import check_energy_cost


def flarebonus(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    attacker.player.discard.append(attacker.player.prompt_card_from_hand("isenergy", _type="fire").id)
    for _ in range(2):
        attacker.player.hand.append(attacker.player.deck.draw())


def claw(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    if attacker.player.flip_coin():
        defender.take_damage(20, attacker)


def tumblingattack(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1)
    damage = 60 if attacker.player.flip_coin() else 30
    defender.take_damage(damage, attacker)


def explosivejet(attacker, defender):
    check_energy_cost(attacker, 4, Fire=2)
    # figure this out layter


def electricannon(attacker, defender):
    check_energy_cost(attacker, 4, Electric=2)
    damage = 80
    # figure this out later
    defender.take_damage(damage, attacker)


def energyconnect(user):
    to = user.player.active
    _from = user.player.prompt_select_ally("notactive", "hasenergy")
    energy = user.player.prompt_select_other(_from.energy.as_card_list)
    energy.override_cap = True
    energy.use(to)
    _from.energy[energy.id.title()] -= 1
    if _from.energy[energy.id.title()] == 0:
        _from.energy.pop(energy.id.title())
    _from.other_attached.remove(energy.id)
