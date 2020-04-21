def computersearch(item):
    d1 = item.player.prompt_card_from_hand()
    d2 = item.player.prompt_card_from_hand()
    item.player.discard.append(d1.id)
    item.player.discard.append(d2.id)
    c = item.player.prompt_card_from_deck()
    item.player.hand.append(c)


def oak(item):
    item.player.discard.extend([i.id for i in item.player.hand])
    item.player.hand = []
    for _ in range(7):
        item.player.hand.append(item.player.deck.draw())
