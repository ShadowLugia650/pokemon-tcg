from data.scripts.smbs import wingattack, crimsonstorm, ragingout, aquaring, hydroshot, tapustorm
from card import get


def cynthia(item):
    item.player.deck.stack.extend([i.id for i in item.player.hand])
    item.player.deck.shuffle_curr()
    item.player.hand = []
    for _ in range(6):
        item.player.hand.append(item.player.deck.draw())


def fisherman(item):
    for _ in range(4):
        energy = item.player.prompt_select_other([get(i, item.player) for i in item.player.discard],
                                                 "isenergy",
                                                 "basic"
                                                 )
        item.player.deck.append(energy.id)
        item.player.discard.remove(energy.id)


def lady(item):
    for _ in range(4):
        item.player.hand.append(item.player.prompt_card_from_deck("isenergy", "basic"))
