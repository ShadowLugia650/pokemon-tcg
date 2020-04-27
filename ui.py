import pygame
import math
import random
from card import Stage, PokemonCard, EnergyCard, TurnEnergyCapReached, TrainerType, TrainerCard, \
    TurnSupporterCapReached, PokemonAlreadyHasItem
from data.scripts._util import NotEnoughEnergy, InvalidPlay, GameWon


all_images = []
selection = None
selscreen = [0, 0]
selecting = False
screen = None
field = None
cur_play = None
using_attack = False


class InterfaceObj:
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs: Keyword Arguments, including
            id: str: id of the object
            loc: (int, int): If loc is included, size must be included too.
                size: (int, int)
            on_hover: func: a function to run when this is hovered over
            on_click: func: a function to run when this is clicked on
        """
        self.id = "-1"
        self.rect = None
        if "id" in kwargs.keys():
            self.id = kwargs["id"]
        if "loc" in kwargs.keys():
            self.rect = pygame.Rect(kwargs["loc"], kwargs["size"])
        self.card = kwargs["card"] if "card" in kwargs.keys() else None


def key_pressed(event):
    global using_attack
    attackeys = [pygame.K_q, pygame.K_w, pygame.K_e]
    if event.key in range(48, 58):
        pass
    elif event.key == pygame.K_SPACE:
        using_attack = False
        field.user.end_turn()
    elif event.key == pygame.K_ESCAPE:
        using_attack = False
    elif event.key in attackeys:
        index = attackeys.index(event.key) % len(field.user.active.attacks)
        try:
            field.user.active.use_attack(index, field.cpu.active)
        except NotEnoughEnergy as e:
            print("Player not enough energy")
        using_attack = False
    elif event.key == pygame.K_r:
        field.user.retreat()
    elif event.key == pygame.K_LEFT:
        if selscreen[1] > 1:
            selscreen[0] = (selscreen[0] - 1) % selscreen[1]
    elif event.key == pygame.K_RIGHT:
        if selscreen[1] > 1:
            selscreen[0] = (selscreen[0] + 1) % selscreen[1]


def mouse_click(event):
    global selection, cur_play, using_attack
    if selecting:
        for img in all_images:
            if img.rect.collidepoint(pygame.mouse.get_pos()):
                selection = img
                return
    if field.is_player_turn:
        if cur_play is not None:
            # hand
            if pygame.mouse.get_pos()[1] >= screen.get_height() - 114:
                field.user.hand.append(cur_play.card)
                cur_play = None
            # trainer cards that do not attach
            elif type(cur_play.card) == TrainerCard:
                if cur_play.card.trainertype == TrainerType.SUPP:
                    hold = cur_play
                    try:
                        c = cur_play.card
                        cur_play = None
                        c.use()
                    except TurnSupporterCapReached as e:
                        cur_play = hold
                        print(e)
                elif cur_play.card.trainertype == TrainerType.STAD:
                    cur_play.card.use()
                    cur_play = None
                elif cur_play.card.trainertype == TrainerType.ITEM:
                    c = cur_play.card
                    cur_play = None
                    c.use()
            # bench
            elif pygame.mouse.get_pos()[0] in range(
                    round(screen.get_width() / 2 - 215),
                    round(screen.get_width() / 2 + 220)) \
                    and pygame.mouse.get_pos()[1] >= round(screen.get_height() / 2 + 124):
                if type(cur_play.card) == PokemonCard and cur_play.card.stage == Stage.BASIC:
                    if len(field.user.bench) < 5:
                        field.user.bench.append(cur_play.card)
                        cur_play = None
            # active ?
        for img in all_images:
            if img.rect.collidepoint(pygame.mouse.get_pos()):
                if cur_play is None:
                    if img.card in field.user.hand:  # and not selecting:
                        if selection is not None and img.card == selection.card:
                            selection = None
                        else:
                            cur_play = img
                            field.user.hand.remove(img.card)
                    elif img.card == field.user.active:
                        using_attack = True
                    elif img.card in field.user.bench and pygame.mouse.get_pos()[1] < screen.get_height() - 114:
                        try:
                            img.card.use_ability(0)
                        except Exception as e:
                            print(e)
                else:
                    if img.card in field.user.bench or img.card == field.user.active:
                        if type(cur_play.card) == EnergyCard:
                            try:
                                cur_play.card.use(img.card)
                                cur_play = None
                            except TurnEnergyCapReached as e:
                                print(e)
                        elif type(cur_play.card) == TrainerCard:
                            if cur_play.card.trainertype == TrainerType.TOOL or cur_play.card.trainertype == TrainerType.ENRG:
                                try:
                                    cur_play.card.data["target"] = img.card
                                    cur_play.card.use()  # handle InvalidPlay from evosoda
                                    cur_play = None
                                except (TurnEnergyCapReached, PokemonAlreadyHasItem) as e:
                                    print(e)
                        elif type(cur_play.card) == PokemonCard:
                            if img.card.name == cur_play.card.prevo:
                                try:
                                    field.user.evolve(img.card, cur_play.card)
                                    cur_play = None
                                except InvalidPlay as e:
                                    print(e)
                    if img.card in field.user.hand:
                        field.user.hand.append(cur_play.card)
                        cur_play = None


def flip_coin(is_player):
    heads = True
    for _ in range(random.randint(5, 8)):
        heads = random.choice([True, False])

    return heads


def user_input(screen, field):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and field.is_player_turn:
            key_pressed(event)
        elif event.type == pygame.MOUSEBUTTONUP and field.is_player_turn:
            mouse_click(event)
    for img in all_images:
        if img.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(pygame.image.load("data/res/cards/{}.png".format(img.id.replace("/", "-"))),
                        (screen.get_width() / 2 + 50, screen.get_height() / 2 - 171))
            if img.card is not None and type(img.card) == PokemonCard:
                dmg = img.card.maxhp - img.card.hp
                n100 = math.floor(dmg / 100)
                n50 = math.floor(dmg % 100 / 50)
                n10 = math.floor(dmg % 50 / 10)
                cur_y = screen.get_height() / 2 - 141
                for n in ["100", "50", "10"]:
                    for i in range(eval("n{}".format(n))):
                        screen.blit(pygame.image.load("data/res/damage/{}.png".format(n)),
                                    (screen.get_width() / 2 + 265, cur_y))
                        cur_y += 33
                if img.card.rotation is not None:
                    screen.blit(pygame.image.load("data/res/damage/{}.png".format(img.card.rotation)),
                                (screen.get_width() / 2 + 69, screen.get_height() / 2 - 138))
                if "poison" in img.card.tokens:
                    screen.blit(pygame.image.load("data/res/damage/poison.png"),
                                (screen.get_width() / 2 + 216, screen.get_height() / 2 - 65))
                if "burned" in img.card.tokens:
                    screen.blit(pygame.image.load("data/res/damage/burned.png"),
                                (screen.get_width() / 2 + 69, screen.get_height() / 2 - 65))
    if cur_play is not None:
        screen.blit(get_img(cur_play.id),
                    (pygame.mouse.get_pos()[0] - 41,
                     pygame.mouse.get_pos()[1] - 59))


def setup_screen(screen_in, screen_id, field_in):
    global all_images, screen, field
    if screen is None: screen = screen_in
    if field is None: field = field_in
    all_images = []
    if screen_id == "mainmenu":
        pass
    elif screen_id == "game":
        screen_in.blit(
            pygame.transform.scale(
                pygame.image.load("data/res/bg.png"),
                (screen_in.get_width(), screen_in.get_height())
            ), (0, 0)
        )
        screen_in.blit(
            pygame.transform.scale(
                pygame.image.load("data/res/backs/{}back.png".format(field_in.user.cardback)),
                (82, 114)
            ), (screen_in.get_width() / 2 + 253, screen_in.get_height() / 2 + 10)
        )
        screen_in.blit(
            pygame.transform.flip(pygame.transform.scale(
                pygame.image.load("data/res/backs/{}back.png".format(field_in.cpu.cardback)),
                (82, 114)
            ), False, True),
            (screen_in.get_width() / 2 - 82 - 253, screen_in.get_height() / 2 - 114 - 10)
        )
        # screen_in.blit(
        #
        # )
    elif screen_id == "deckbuild":
        pass


def blit_hands_prizes():
    for i in range(len(field.user.prize)):
        screen.blit(
            pygame.transform.scale(
                pygame.image.load("data/res/backs/{}back.png".format(field.user.cardback)),
                (82, 114)
            ),
            (30, screen.get_height() - 264 + 25 * i)
        )
    for i in range(len(field.cpu.prize)):
        screen.blit(
            pygame.transform.flip(pygame.transform.scale(
                pygame.image.load("data/res/backs/{}back.png".format(field.cpu.cardback)),
                (82, 114)
            ), False, True),
            (screen.get_width() - 112, 150 - 25 * i)
        )
    for i in range(len(field.user.hand)):
        blit_interfaceobj(
            screen,
            field.user.hand[i].id,
            (screen.get_width() / 2 - 82 * len(field.user.hand) / 2
             - math.floor(len(field.user.hand) / 2) * 5 + i * 87,
             screen.get_height() - 114),
            card=field.user.hand[i]
        )
    for i in range(len(field.cpu.hand)):
        screen.blit(
            pygame.transform.flip(pygame.transform.scale(
                pygame.image.load("data/res/backs/{}back.png".format(field.cpu.cardback)),
                (82, 114)
            ), False, True),
            (screen.get_width() / 2 + 82 * (len(field.cpu.hand) / 2 - 1)
             + math.floor(len(field.user.hand) / 2) * 5 - i * 87,
             0)
        )
    if using_attack:
        screen.blit(pygame.image.load("data/res/cards/{}.png".format(field.user.active.id.replace("/", "-"))),
                    (screen.get_width() / 2 + 50, screen.get_height() / 2 - 171))
        screen.blit(pygame.image.load("data/res/cards/{}.png".format(field.cpu.active.id.replace("/", "-"))),
                    (screen.get_width() / 2 - 295, screen.get_height() / 2 - 171))


def get_img(id, cpu=False):
    sprite = pygame.transform.scale(
        pygame.image.load("data/res/cards/{}.png".format(id.replace("/", "-"))),
        (82, 114)
    )
    if cpu:
        sprite = pygame.transform.flip(sprite, False, True)
    return sprite


def blit_interfaceobj(screen, id, location, cpu=False, **kwargs):
    img = get_img(id, cpu)
    screen.blit(img, location)
    all_images.append(InterfaceObj(id=id, loc=location, size=img.get_size(), **kwargs))


def blit_cards(screen, field):
    if field.user.active is None:
        raise GameWon("ai wins")
    if field.cpu.active is None:
        raise GameWon("player wins")
    if field.user.active.item is not None:
        blit_interfaceobj(
            screen,
            field.user.active.item.id,
            (screen.get_width() / 2 - 61, screen.get_height() / 2 + 25),
            card=field.user.active.item
        )
    if field.cpu.active.item is not None:
        blit_interfaceobj(
            screen,
            field.cpu.active.item.id,
            (screen.get_width() / 2 - 21, screen.get_height() / 2 - 139),
            cpu=True,
            card=field.cpu.active.item
        )
    for i in range(len(field.user.active.other_attached))[::-1]:
        blit_interfaceobj(
            screen,
            field.user.active.other_attached[i],
            (screen.get_width() / 2 - 31 + 10 * i, screen.get_height() / 2 + 15)
        )
    for i in range(len(field.cpu.active.other_attached))[::-1]:
        blit_interfaceobj(
            screen,
            field.cpu.active.other_attached[i],
            (screen.get_width() / 2 - 51 - 10 * i, screen.get_height() / 2 - 134),
            cpu=True
        )
    blit_interfaceobj(
        screen,
        field.user.active.id,
        (screen.get_width() / 2 - 41, screen.get_height() / 2 + 5),
        card=field.user.active
    )
    blit_interfaceobj(
        screen,
        field.cpu.active.id,
        (screen.get_width() / 2 - 41, screen.get_height() / 2 - 119),
        cpu=True,
        card=field.cpu.active
    )
    for i in range(len(field.user.bench)):
        blit_interfaceobj(
            screen,
            field.user.bench[i].id,
            (screen.get_width() / 2 - 215 + i * 87, screen.get_height() / 2 + 124),
            card=field.user.bench[i]
        )
    for i in range(len(field.cpu.bench)):
        blit_interfaceobj(
            screen,
            field.cpu.bench[i].id,
            (screen.get_width() / 2 + 123 - i * 87, screen.get_height() / 2 - 238),
            cpu=True,
            card=field.cpu.bench[i]
        )
    if len(field.user.discard) > 0:
        blit_interfaceobj(
            screen,
            field.user.discard[len(field.user.discard)-1],
            (screen.get_width() / 2 + 253, screen.get_height() / 2 + 134)
        )
    if len(field.cpu.discard) > 0:
        blit_interfaceobj(
            screen,
            field.cpu.discard[len(field.cpu.discard)-1],
            (screen.get_width() / 2 - 82 - 253, screen.get_height() / 2 - 248),
            cpu=True
        )
    if field.stadcard is not None:
        blit_interfaceobj(
            screen,
            field.stadcard.id,
            (screen.get_width() / 2 - 164, screen.get_height() / 2 - 57)
        )


def display_choice(options, label, skippable=False):
    global selection, all_images, screen, field, selscreen, selecting
    selection = None
    selecting = True
    selscreen = [0, math.ceil(len(options) / 21)]
    wasmyturn = field.is_player_turn
    field.is_player_turn = True
    while selection is None:
        setup_screen(screen, "game", field)
        try:
            blit_cards(screen, field)
        except Exception:
            pass
        blit_hands_prizes()
        all_images = []
        screen.blit(
            pygame.transform.scale(pygame.image.load("data/res/select_tint.png"),
                                   (screen.get_width(), screen.get_height())),
            (0, 0)
        )
        g = lambda x: 2*math.ceil(x/2)*(x-(math.ceil(x/2)*4-1)/2)
        if len(options) < 21:
            for i in range(len(options)):
                item = options[i]
                loc = (screen.get_width() / 2 - 41 + 92*g(i-7*math.floor(i/7)),
                       screen.get_height() / 2 - 57 + 124*g(math.floor(i/7)))
                if type(item) == str:  # then i is an id
                    blit_interfaceobj(screen, item, loc)
                else:  # i is an object that hopefully has an id attribute...
                    blit_interfaceobj(screen, item.id, loc, card=item)
        else:
            rmin = round(21*selscreen[0])
            rmax = min(round(21*(selscreen[0]+1)), len(options))
            for i in range(rmin, rmax):
                item = options[i]
                n = i - rmin
                loc = (screen.get_width() / 2 - 41 + 92*g(n-7*math.floor(n/7)),
                       screen.get_height() / 2 - 57 + 124*g(math.floor(n/7)))
                if type(item) == str:  # then i is an id
                    blit_interfaceobj(screen, item, loc)
                else:  # i is an object that hopefully has an id attribute...
                    blit_interfaceobj(screen, item.id, loc, card=item)
        user_input(screen, field)
        pygame.display.update()
    field.is_player_turn = wasmyturn
    selecting = False
    return selection.id, selection.card
