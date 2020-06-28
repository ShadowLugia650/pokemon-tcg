from data.scripts._util import check_energy_cost
from card import get, Type


def slash(attacker, defender):
    check_energy_cost(attacker, 2)
    defender.take_damage(30, attacker)


def midairstrike(attacker, defender):
    check_energy_cost(attacker, 3, Fire=1)
    damage = 70 if attacker.player.flip_coin() else 50
    defender.take_damage(damage, attacker)


def shoutofpower(attacker, defender):
    check_energy_cost(attacker, 1, Fighting=1)
    defender.take_damage(20, attacker)
    energy = attacker.player.prompt_select_other(
        [get(i) for i in attacker.player.discard],
        "isenergy",
        "remove"
    )
    to = attacker.player.prompt_select_ally("notactive")
    if energy.upper() in Type.__members__:
        c = get(energy, attacker.player)
        c.override_cap = True
        c.use(to)
    else:
        for id in attacker.special_energy:
            c = get(id, attacker.player)
            if energy in c.name:
                c.data["overridecap"] = True
                c.data["target"] = to
                c.use()
                break


def skylariat(attacker, defender):
    check_energy_cost(attacker, 3, Fighting=2)
    defender.take_damage(90, attacker)


def korrina(item):
    item.player.hand.append(item.player.prompt_card_from_deck("ispokemon", _type="fighting"))
    # prompt item card from deck
