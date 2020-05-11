from data.scripts._util import check_energy_cost
from card import Type, get, EnergyCard


def collect(attacker, defender):
    check_energy_cost(attacker, 1, Water=1)
    for _ in range(3):
        attacker.player.hand.append(attacker.player.deck.draw())


def energyloop(attacker, defender):
    check_energy_cost(attacker, 1, Metal=1)
    defender.take_damage(30, attacker)
    energy = attacker.player.prompt_select_other(attacker.energy)
    attacker.energy[energy] -= 1
    if attacker.energy[energy] == 0:
        attacker.energy.pop(energy)
    if energy.upper() in Type.__members__:
        attacker.player.hand.append(get(energy.lower(), attacker.player))
    else:
        for id in attacker.special_energy:
            c = get(id)
            if energy in c.name:
                attacker.player.hand.append(c)
                break


def metalnavigation(user):
    c = user.player.prompt_card_from_deck("isenergy", _type="metal")
    if type(c) == EnergyCard:
        c.override_cap = True
        c.use(user)
    else:
        c.data["target"] = user
        c.data["overridecap"] = True
        c.use()
