from data.scripts._util import check_energy_cost, InvalidPlay


def keeneye(attacker, defender):
    attacker.player.hand.append(attacker.player.prompt_card_from_deck())
    attacker.player.hand.append(attacker.player.prompt_card_from_deck())


def batonpass(attacker, defender):
    check_energy_cost(attacker, 2)
    defender.take_damage(40, attacker)
    switch = attacker.player.prompt_select_ally()
    if switch != attacker:
        attacker.player.active = switch
        attacker.player.bench.append(attacker)
    # add energy movement if you really want to later


def bebes(item):
    if len(item.player.hand) < 2:
        raise InvalidPlay
    put = item.player.prompt_card_from_hand()
    item.player.deck.stack.insert(0, put.id)
    get = item.player.prompt_card_from_deck("ispokemon")
    item.player.hand.append(get)


def nightmaintenance(item):
    for _ in range(3):
        item.player.deck.append(
            item.player.prompt_select_other(
                item.player.discard,
                "remove",
                "ispokemon",
                "isenergy",
                basic="energy"
            )
        )
    item.player.deck.shuffle_curr()


def roseannes(item):
    for _ in range(2):
        item.player.hand.append(item.player.prompt_card_from_deck(
            "ispokemon",
            "isenergy",
            "basic"
        ))
