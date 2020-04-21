from data.scripts._util import InvalidPlay


def rowan(item):
    if len(item.player.hand) < 2:
        raise InvalidPlay
    c = item.player.prompt_card_from_hand()
    item.player.deck.stack.extend([i.id for i in item.player.hand])
    item.player.hand = [c]
    for _ in range(4):
        item.player.hand.append(item.player.deck.draw())
