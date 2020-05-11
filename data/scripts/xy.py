from data.scripts._util import check_energy_cost
from card import Type, get


def evilball(attacker, defender):
    check_energy_cost(attacker, 2, Dark=1)
    damage = 20 + 20 * attacker.energy.total() + 20 * defender.energy.total()
    defender.take_damage(damage, attacker)


def ycyclone(attacker, defender):
    check_energy_cost(attacker, 3, Dark=1)
    defender.take_damage(90, attacker)
    to = attacker.player.prompt_select_ally("notactive")
    energy = attacker.player.prompt_select_other(attacker.energy.as_card_list())
    attacker.energy[energy] -= 1
    if attacker.energy[energy] == 0:
        attacker.energy.pop(energy)
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


def stoke(attacker, defender):
    pass


def fireblast(attacker, defender):
    pass


def trevor(item):
    card = item.player.prompt_card_from_deck("ispokemon")
    item.player.hand.append(card)


def oblivionwing(attacker, defender):
    check_energy_cost(attacker, 1, Dark=1)
    defender.take_damage(30, attacker)
    energy = attacker.player.prompt_select_other(
        attacker.player.discard,
        "isenergy",
        "remove",
        _type="Dark"
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


def darknessblade(attacker, defender):
    check_energy_cost(attacker, 3, Dark=2)
    defender.take_damage(100, attacker)
    if not attacker.player.flip_coin():
        attacker.extra_effects["cantattack"] = 1


def evosoda(item):
    evo = item.player.prompt_card_from_deck("ispokemon", evo_of=[i.name for i in item.player.bench+[item.player.active]])
    print([i for i in item.player.bench+[item.player.active] if i.name == evo.prevo])
    of = item.player.prompt_select_other(
        [i for i in item.player.bench+[item.player.active] if i.name == evo.prevo]
    )
    item.player.evolve(of, evo)


def muscleband_added(target):
    if "damageup" in target.extra_effects:
        target.extra_effects["damageup"] += 20
    else:
        target.extra_effects["damageup"] = 20


def profletter(item):
    for _ in range(2):
        item.player.hand.append(
            item.player.prompt_card_from_deck("isenergy", "basic")
        )
