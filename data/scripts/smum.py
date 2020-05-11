from data.scripts._util import check_energy_cost
from card import Type, EnergyCard


def gnaw(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1, Metal=1)
    defender.take_damage(20, attacker)


def unnerve(user):
    user.player.global_abilities.append("unnerve")


def powerfulaxe(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1, Metal=1)
    damage = 10
    for key in attacker.energy.keys():
        if key.upper() in Type.__members__:
            damage += 40 * attacker.energy[key]
    defender.take_damage(damage, attacker)


def grindup(user):
    if user.player.field.stadcard is not None:
        user.player.field.stadium = ""
        user.player.field.stadcard.player.discard.append(user.player.field.stadcard.id)
        user.player.field.stadcard = None
        for _ in range(3):
            c = user.player.prompt_card_from_deck("isenergy", _type=["fire", "metal"])
            if type(c) == EnergyCard:
                c.override_cap = True
                c.use(user)
            else:
                c.data["overridecap"] = True
                c.data["target"] = user
                c.use()
