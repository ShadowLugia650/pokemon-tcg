def collector(item):
    for _ in range(3):
        item.player.hand.append(item.player.prompt_card_from_deck("ispokemon", "basic"))
