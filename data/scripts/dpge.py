from data.scripts._util import check_energy_cost, PokemonAlreadyHasItem
from card import PokemonCard


def spinningattack(attacker, defender):
    check_energy_cost(attacker, 2, Fighting=1)
    defender.take_damage(40, attacker)


def cosmicpower(user):
    if "cosmicpower" in user.one_time_used:
        return
    for _ in range(2):
        c = user.player.prompt_card_from_hand("skippable")
        user.player.deck.stack.append(c.id)
    while len(user.player.hand) < 6:
        user.player.hand.append(user.player.deck.draw())
    user.one_time_used.append("cosmicpower")


def hiddenpower(attacker, defender):
    check_energy_cost(attacker, 2, Psychic=1)
    damage = 10 if attacker.hp != attacker.maxhp else 50
    defender.take_damage(damage, attacker)


def guard(user):
    user.discard_attachments()
    target = user.player.prompt_select_ally(_not=user)
    if target.item is not None:
        raise PokemonAlreadyHasItem
    target.item = user
    user.player.bench.remove(user)


def psychicbalance(attacker, defender):
    check_energy_cost(attacker, 1)
    while len(attacker.player.hand) < len(defender.player.hand):
        attacker.player.hand.append(attacker.player.deck.draw())


def spinturn(attacker, defender):
    check_energy_cost(attacker, 2, Fighting=1)
    defender.take_damage(20, attacker)
    switch = attacker.player.prompt_select_ally("notactive", "remove")
    attacker.player.bench.append(attacker)
    attacker.player.active = switch


def rarecandy(item):
    skips = {"Tepig": "Emboar",
             "Klink": "Klinklang",
             "Deino": "Hydreigon",
             "Tynamo": "Eelektross",
             "Axew": "Haxorus",
             "Beldum": "Metagross",
             "Charmander": "Charizard",
             "Torchic": "Blaziken",
             "Fennekin": "Delphox",
             "Chimchar": "Infernape",
             "Squirtle": "Blastoise",
             "Horsea": "Kingdra"}
    if skips.keys().isdisjoint(set([i.name for i in item.player.bench+[item.player.active]])) or \
    set(skips.values()).isdisjoint(set([i.name for i in
                                        [j for j in item.player.hand if type(j) == PokemonCard]])):
        return
    target = item.player.prompt_select_ally("basic", name_in=skips.keys())
    evo = item.player.prompt_card_from_hand(name_in=[skips[target.name]])
    item.player.evolve(target, evo)
