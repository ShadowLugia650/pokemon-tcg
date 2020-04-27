""" main.py: well basically I have no friends and no moneys so I'm just gonna
make this to hopefully fill up some of my bored hours
"""

from player import Player
import pygame
import random
import traceback
import ui
from ai import Algorithmic

pygame.init()


class Field:
    def __init__(self):
        self.stadium = ""
        self.stadcard = None
        self.is_player_turn = False
        self.user = None
        self.cpu = None


def init_match(deck):
    field = Field()
    field.user = Player(field, deck)
    field.cpu = Player(field, "yvelboar")  # random.choice(["rayeels", "yvelboar"]))
    field.user.opponent = field.cpu
    field.cpu.opponent = field.user
    field.cpu.ai = Algorithmic(field.cpu)  # remove later
    field.cpu.cardback = "yveltal"
    field.cpu.ai.load_alg()
    if field.user.flip_coin():
        field.is_player_turn = True
    if field.is_player_turn:
        field.user.start_game()
        field.cpu.start_game()
        ui.setup_screen(screen, "game", field)
        ui.blit_hands_prizes()
        field.user.active = field.user.prompt_card_from_hand("ispokemon", "basic", label="Select an Active Pokemon:")
        field.cpu.ai.first_turn()
    else:
        field.cpu.start_game()
        field.user.start_game()
        field.cpu.ai.first_turn()  # remove later
        ui.setup_screen(screen, "game", field)
        ui.blit_hands_prizes()
        field.user.active = field.user.prompt_card_from_hand("ispokemon", "basic", label="Select an Active Pokemon:")
    return field


def hang():
    global running
    running = False


def log(text):
    f = open("1.log", "x")


if __name__ == "__main__":
    try:
        pygame.display.set_icon(pygame.image.load("data/res/icon.png"))
        deck = input("deck (yvelboar/rayeels/steelgears/speedyzard/lapras): ")
        while deck.lower() not in ["yvelboar", "rayeels", "steelgears", "speedyzard", "lapras"]:
            deck = input("deck: ")
        screen = pygame.display.set_mode((800, 600))  # set_mode((0, 0), pygame.FULLSCREEN)
        screen_id = "game"  # "mainmenu"
        field = init_match(deck.lower())
        running = True
        while running:
            if not field.is_player_turn:
                field.cpu.ai.my_turn()
            ui.setup_screen(screen, screen_id, field)
            ui.blit_cards(screen, field)
            ui.blit_hands_prizes()
            ui.user_input(screen, field)
            pygame.display.flip()
    except Exception as e:
        print("Exception caught:")
        track = traceback.format_exc()
        print(track)
        log = input("Type 'log' to save a log. Press enter to close.").lower() == 'log'
        if log:
            pass

    # pygame.quit()
    # quit()
