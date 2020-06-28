""" main.py: well basically I have no friends and no moneys so I'm just gonna
make this to hopefully fill up some of my bored hours
"""

import pygame
import random
import traceback
import time
import ui
from ai import Algorithmic
from player import Player

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
    with open("data/crash_logs/{}.log".format(round(time.time())), "x") as f:
        f.write(text)


if __name__ == "__main__":
    playable = ["yvelboar", "rayeels", "steelgears", "speedyzard", "lapras", "mimewall", "ultranecro"]
    try:
        pygame.display.set_icon(pygame.image.load("data/res/icon.png"))
        deck = input("deck (one of the presets or random): ")
        while deck.lower() not in playable and deck.lower() != "random":
            deck = input("deck: ")
        if deck.lower() == "random":
            deck = random.choice(playable)
        screen = pygame.display.set_mode(ui.SCREENSIZE)  # set_mode((0, 0), pygame.FULLSCREEN)
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
        wrlog = input("Type 'log' to save a log. Press enter to close.").lower() == 'log'
        if wrlog:
            log(track)

    # pygame.quit()
    # quit()
