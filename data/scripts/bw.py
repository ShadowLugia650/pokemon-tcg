from data.scripts._util import check_energy_cost
from card import EnergyCard, TrainerCard, TrainerType, get
from data.scripts.bwlt import nightspear, darkcloak, secretsword, rushin


def tackle(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    defender.take_damage(10, attacker)


def rollout(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1)
    defender.take_damage(20, attacker)


def flamecharge(attacker, defender):
    check_energy_cost(attacker, 1)
    c = attacker.player.prompt_card_from_deck("isenergy", _type="fire")
    c.override_cap = True
    c.use(attacker)


def heatcrash(attacker, defender):
    check_energy_cost(attacker, 3, Fire=2)
    defender.take_damage(50, attacker)


def celestialroar(attacker, defender):
    check_energy_cost(attacker, 1)
    cards = [attacker.player.deck.draw() for _ in range(3)]
    for i in cards:
        if type(i) == EnergyCard:
            i.override_cap = True
            i.use(attacker)
        elif type(i) == TrainerCard and i.trainertype == TrainerType.ENRG:
            i.data["overridecap"] = True
            i.data["target"] = attacker
            i.use()
        else:
            attacker.player.discard.append(i.id)


def dragonburst(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1, Electric=1)
    energy_type = attacker.player.prompt_select_other([get("fire"), get("electric")]).id
    damage = attacker.energy[energy_type.title()]*60
    for _ in range(attacker.energy[energy_type.title()]):
        attacker.player.discard.append(energy_type.lower())
    attacker.energy.pop(energy_type.title())
    attacker.other_attached = [i for i in attacker.other_attached if i != energy_type]
    defender.take_damage(damage, attacker)


def geargrind(attacker, defender):
    check_energy_cost(attacker, 3, Metal=1)
    for _ in range(2):
        if attacker.player.flip_coin():
            defender.take_damage(80, attacker)


def shiftgear(user):
    # user.player.global_abilities.append("shiftgear")
    _from = user.player.prompt_select_ally(has_energy="metal")
    energy = user.player.prompt_select_other(_from.energy.as_card_list(), _type="metal")
    to = user.player.prompt_select_ally()
    _from.energy[energy] -= 1
    if _from.energy[energy] == 0:
        _from.energy.pop(energy)
    if energy.lower() == "metal":
        c = get(energy, user.player)
        c.override_cap = True
        c.use(to)
    else:
        for id in _from.special_energy:
            c = get(id, user.player)
            if energy in c.name:
                c.data["overridecap"] = True
                c.data["target"] = to
                c.use()
                break


def energyretrieval(item):
    for _ in range(2):
        card = item.player.prompt_select_other(
                [get(i, item.player) for i in item.player.discard],
                "isenergy", "basic"
            )
        item.player.hand.append(
            card
        )
        item.player.discard.remove(card.id)


def pokecom(item):
    p1 = item.player.prompt_card_from_hand("ispokemon")
    item.player.deck.stack.insert(0, p1.id)
    p2 = item.player.prompt_card_from_deck("ispokemon")
    item.player.hand.append(p2)


def switch(item):
    p1 = item.player.prompt_select_ally("notactive", "remove")
    item.player.bench.append(item.player.active)
    item.player.active = p1
