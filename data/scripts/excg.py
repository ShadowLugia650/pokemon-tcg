from card import Flair


def celios(item):
    item.player.hand.append(
        item.player.prompt_card_from_deck("ispokemon", exclude_flair=[Flair.EX])
    )
