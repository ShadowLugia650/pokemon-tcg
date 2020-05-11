import random
from card import get, Stage, PokemonCard, TrainerCard, TrainerType, EnergyCard
import ui
from data.scripts._util import InvalidPlay, GameWon


class Deck:
    def __init__(self, player, preset=None):
        self.all_cards = []
        self.stack = []
        self.player = player
        if preset is not None:
            self.load_preset(preset)
        self.preset = preset

    def load_preset(self, preset):
        self.preset = preset
        with open("data/presets/{}.deck".format(preset)) as f:
            for line in f:
                self.all_cards.append(line.replace("\n", ""))
        if len(self.all_cards) != 60:
            print("Error: Deck is not 60 cards.")

    def load_deck(self, deck_name):
        with open("data/user/{}.deck".format(deck_name)) as f:
            for line in f:
                self.all_cards.append(line.replace("\n", ""))
        if len(self.all_cards) != 60:
            print("Error: Deck is not 60 cards.")

    def draw(self):
        return get(self.stack.pop(0), self.player)

    def shuffle_all(self):
        cards = [i for i in self.all_cards]
        self.stack = []
        while len(cards) > 0:
            self.stack.insert(0, cards.pop(random.randint(0, len(cards)-1)))

    def shuffle_curr(self):
        cards = [i for i in self.stack]
        self.stack = []
        while len(cards) > 0:
            self.stack.insert(0, cards.pop(random.randint(0, len(cards)-1)))

    def is_empty(self):
        return len(self.stack) == 0


class Player:
    """ Defines a player's side on the board, with the prize card pool, a hand,
    a bench, an active pokemon, and a deck.
    """
    def __init__(self, field=None, preset=None):
        self.deck = Deck(self, preset)
        self.prize = []
        self.bench = []
        self.active = None
        self.discard = []
        self.lostzone = []
        self.hand = []
        self.has_done = []
        self.opponent = None
        self.mulligans = -1
        self.global_abilities = []  # infernofandango, shiftgear, etc.
        self.field = field
        self.ai = None
        self.gx_used = False
        self.cardback = "classic"
        self.coin = "pokeball"
        self.coin_heads = True

    def flip_coin(self):
        return ui.flip_coin(self.ai is None)

    def prompt_select_ally(self, *args, **kwargs):
        id = ""
        if "notactive" not in args:
            id = self.prompt_select_other([self.active]+self.bench, *args, **kwargs)
        else:
            id = self.prompt_select_other(self.bench, *args, **kwargs)
        return id

    def prompt_select_opp(self, *args, **kwargs):
        id = ""
        if "notactive" not in args:
            id = self.prompt_select_other([self.opponent.active]+self.opponent.bench, *args, **kwargs)
        else:
            id = self.prompt_select_other(self.opponent.bench, *args, **kwargs)
        return id

    def prompt_card_from_deck(self, *args, **kwargs):
        card = self.prompt_select_other([get(i, self) for i in self.deck.stack], *args, **kwargs)
        self.deck.stack.remove(card.id)
        self.deck.shuffle_curr()
        return card

    def prompt_card_from_hand(self, *args, **kwargs):
        card = self.prompt_select_other(self.hand, *args, **kwargs)
        index = [i for i in range(len(self.hand)) if self.hand[i].id == card.id]
        return self.hand.pop(index[0])

    # All other prompt selects should call prompt_select_other to make more sense
    def prompt_select_other(self, _from, *args, **kwargs):
        """ Prompts the player to select a card from a given list _from. Takes
        other args and kwargs

        :param _from: the list to select an option from
        :param args: extra arguments, including:
            "isenergy": only lets the player select energy cards
            "remove": removes the card from the list _from
            "ispokemon": only lets the player select pokemon cards
            "issupporter": only lets the player select supporter cards
            "isstadium": only lets the player select stadium cards
            "istrainer": only lets the player select trainer cards
            "basic": only lets the player select basic pokemon or basic energy
                cards
            "hasenergy": has energy attached of any kind
            "skippable": if this selection prompt is skippable
            NOTE: using multiple "is_" args will OR them, not AND them.
        :param kwargs: extra keyword arguments, including:
            _type="typestring": the type of the card (all lowercase)
            _type=["typestring",]: a list of types that can be chosen
            hpmax=int: the maximum hp the pokemon can have
            _not= item: an item the selection cannot be (generally _not=self)
            basic= "pokemon"|"energy" if isenergy and ispokemon are both args,
                but the player can only select basic of one of the two and any
                of the other.
            exclude_flair=[Flair, ] flairs to exclude in selection of pokemon
            evo_of=["pokemon name", ] requires that the pokemon are evolutions
                of one pokemon in evo_of
                NOTE: only works if "ispokemon" is the only specification arg
            has_energy="typestring": if the pokemon has the given energy type
            name_in=["pokemon name", ] requires that the pokemon's name is in
                the provided list
            label="label": a string label to display with the selection
        :return: the element of the list _from that was selected. May be a Card
            or an id. When used with custom lists may return any value in the
            list.
        """
        options = []
        available = [i for i in _from]
        if "_not" in kwargs.keys():
            available = [i for i in options if i != kwargs["_not"]]
        if "isenergy" in args:
            narrow = [i for i in available if "-" not in i.id or (type(i) == TrainerCard and
                      i.trainertype == TrainerType.ENRG)]
            if "_type" in kwargs.keys():
                narrow = [i for i in narrow if i.id in kwargs["_type"] or
                          (type(i) == TrainerCard and "type" in i.data.keys() and
                           not set(i.data["type"]).isdisjoint(set(kwargs["_type"])))]
            if "basic" in args:
                narrow = [i for i in narrow if type(i) == EnergyCard]
            options.extend(narrow)
        if "ispokemon" in args:
            narrow = [i for i in available if type(i) == PokemonCard]
            if "_type" in kwargs.keys():
                narrow = [i for i in narrow if not set(
                    [eval("Type.{}".format(i.upper())) for i in kwargs["_type"]]
                ).isdisjoint(set(i.type))]
            if "basic" in args:
                narrow = [i for i in narrow if i.stage == Stage.BASIC]
            if "evo_of" in kwargs.keys():
                narrow = [i for i in narrow if i.prevo in kwargs["evo_of"]]
            if "exclude_flair" in kwargs.keys():
                narrow = [i for i in narrow if i.flair not in kwargs["exclude_flair"]]
            if "hpmax" in kwargs.keys():
                narrow = [i for i in narrow if i.maxhp <= kwargs["hpmax"]]
            if "has_energy" in kwargs.keys():
                narrow = [i for i in narrow if kwargs["has_energy"].title() in i.energy.keys()]
            elif "hasenergy" in args:
                narrow = [i for i in narrow if i.energy.total() > 0]
            if "name_in" in kwargs.keys():
                narrow = [i for i in narrow if i.name in kwargs["name_in"]]
            options.extend(narrow)
        if "istrainer" in args:
            narrow = [i for i in available if type(i) == TrainerCard]
            options.extend(narrow)
        if "issupporter" in args:
            narrow = [i for i in available if type(i) == TrainerCard and i.trainertype == TrainerType.SUPP]
            options.extend(narrow)
        if "isstadium" in args:
            narrow = [i for i in available if type(i) == TrainerCard and i.trainertype == TrainerType.STAD]
            options.extend(narrow)
        if len(available) == 0:
            return  # this may cause problems.
        if len(options) == 0:
            options = available  # this actually causes problems buddy boy
        sel = (None, None)
        if self.ai is None:
            sel = ui.display_choice(options,
                                    kwargs["label"] if "label" in kwargs.keys() else "",
                                    "skippable" in args)
        else:
            sel = self.ai.choose(options, "skippable" in args)
        if "remove" in args:
            _from.remove(sel[1] if sel[1] is not None else sel[0])
        return sel[1]

    def start_game(self):
        """ Starts the game by dealing out prize cards and hand. Assumes that
        self.deck is initialized
        """
        self.deck.shuffle_all()
        while Stage.BASIC not in [i.stage for i in self.hand if type(i) == PokemonCard]:
            self.mulligans += 1
            self.hand = []
            self.deck.shuffle_all()
            for _ in range(7):
                self.hand.append(self.deck.draw())
        for _ in range(6):
            self.prize.append(self.deck.draw().id)

    def pull_prize(self):
        if len(self.prize) == 0:
            self.win()
            raise GameWon("player wins" if self.ai is None else "ai wins")
        return get(self.prize.pop(), self)

    def evolve(self, _from, to):
        if "cantevolve" in _from.extra_effects.keys() and "bts" != self.field.stadium:
            raise InvalidPlay
        to.other_attached = _from.other_attached
        to.other_attached.append(_from.id)
        damage_taken = _from.maxhp - _from.hp
        to.take_damage(damage_taken, _from, "nomod")
        self.global_abilities.extend(to.global_abilities)
        for ability in to.on_play:
            exec("from data.scripts.{} import {}".format(to.id.split("-")[0], ability))
            exec("{}(to)".format(ability))
        if _from == self.active:
            self.active = to
        else:
            self.bench[self.bench.index(_from)] = to

    def play_pokemon(self, pokemon):
        for ability in pokemon.on_play:
            exec("from data.scripts.{} import {}".format(pokemon.id.split("-")[0], ability))
            exec("{}(to)".format(ability))
        self.global_abilities.extend(pokemon.global_abilities)
        self.bench.append(pokemon)

    def start_turn(self):
        self.hand.append(self.deck.draw())
        if "darkcloak" in self.global_abilities:
            for card in [self.active]+self.bench:
                if "Dark" in card.energy.keys():
                    card.extra_effects["freeretreat"] = True

    def end_turn(self):
        self.has_done = []
        for i in [self.active]+self.bench:
            i.end_turn(True)
        if self.opponent.active is None:
            self.win()
            return
        for i in [self.opponent.active]+self.opponent.bench:
            i.end_turn(False)
        self.field.is_player_turn = False

    def retreat(self):
        if "freeretreat" in self.active.extra_effects.keys() or \
             ("Dark" in self.active.energy.keys() and "darkcloak" in self.global_abilities) or \
             ("Water" in self.active.energy.keys() and "aquatube" in self.global_abilities):
            pass
        elif self.active.energy.total() >= self.active.retreat:
            for _ in range(self.active.retreat):
                energy = self.prompt_select_other(self.active.energy.as_card_list())
                if type(energy) == EnergyCard:
                    self.active.energy[energy.typestring.title()] -= 1
                    if self.active.energy[energy.typestring.title()] == 0:
                        self.active.energy.pop(energy.typestring.title())
                else:
                    pass
                print(self.active.other_attached)
                print("{}: {}".format(energy.id, energy))
                self.active.other_attached.remove(energy.id)
                self.discard.append(energy.id)
        else:
            return
        newactive = self.prompt_select_ally("notactive", "remove")
        self.active.tokens = []
        self.active.rotation = None
        self.bench.append(self.active)
        self.active = newactive

    def win(self):
        import main
        main.hang()
