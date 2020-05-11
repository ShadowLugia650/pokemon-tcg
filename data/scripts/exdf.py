def copycat(item):
    item.player.deck.stack.extend([i.id for i in item.player.hand])
    item.player.hand = []
    for _ in range(len(item.player.opponent.hand)):
        item.player.hand.append(item.player.deck.draw())
