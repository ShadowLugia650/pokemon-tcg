from enum import Enum
from data.scripts._util import PokemonAlreadyHasItem, TurnEnergyCapReached, TurnSupporterCapReached


class TrainerType(Enum):
    ITEM = 0
    TOOL = 1
    STAD = 2  # stadium
    SUPP = 3  # supporter
    FLRE = 4  # flare tool
    ENRG = 5  # special energy
    # how do we know if something's an ace spec?


class Stage(Enum):
    BASIC = 0
    ONE = 1
    TWO = 2
    MEGA = 3
    BREAK = 4
    VMAX = 5
    LEGEND = 6


class Type(Enum):
    NORMAL = 0
    FIGHTING = 1
    PSYCHIC = 2
    DARK = 3
    FAIRY = 4
    METAL = 5
    FIRE = 6
    WATER = 7
    GRASS = 8
    ELECTRIC = 9
    DRAGON = 10


class Flair(Enum):
    NONE = 0
    EX = 1  # 2 prizes
    X = 2
    BREAK = 3
    GX = 4  # 2 prizes
    TAGTEAM = 5  # 3 prizes
    V = 6  # 2 prizes
    PRISM = 7
    DELTA = 8
    LEGEND = 9  # 2 prizes, 2 types


def get(id, player=None):
    """ Returns the card corresponding to the given id. This function should be
    used instead of constructors for the different card classes.

    :param id: the id of the card to get
    :param player: the pointer to the Player() class that owns this card.
        Defaults to None for card data purposes
    :return: the proper Card object containing all of the data for the given
        card id.
    """
    if "-" in id:
        expansion, num = id.split("-")
        with open("data/cards/{}.cards".format(expansion)) as f:
            lines = {line.split(": ")[0]: line.split(": ")[1].replace("\n", "") for line in f}
            line = lines[num]
            if "REF " in line:
                line = lines[line.split("REF ")[1]]
            c = None
            if line.split("|")[0] in Stage.__members__:
                c = PokemonCard(id, player)
            else:
                c = TrainerCard(id, player)
            c.get_card_data(line)
            return c
    else:  # is an energy card // or should I override load() in EnergyCard?
        return EnergyCard(id, player)


class EnergyBank(dict):
    """ Extends the dict class and adds a few class methods to make energy card
    management easier.
    """
    def __init__(self, pokemon):
        dict.__init__(self)
        self.pokemon = pokemon

    def total(self):
        t = 0
        for key in self.keys():
            t += self[key]
        return t

    def as_id_list(self):
        l = []
        for key in self.keys():
            if key.upper() in Type.__members__:
                for _ in range(self[key]):
                    l.append(key)
            else:
                for id in self.pokemon.special_energy:
                    l.append(id)
        return l

    def as_card_list(self):
        l = []
        for key in self.keys():
            if key.upper() in Type.__members__:
                for _ in range(self[key]):
                    l.append(get(key, self.pokemon.player))
            else:
                for id in self.pokemon.special_energy:
                    l.append(get(id, self.pokemon.player))
        return l

    def lose_energy(self, _type):
        pass


class PokemonCard:
    """ Represents a Pokemon Card that has the data of a specific pokemon.
    This class should not be initialized by the user. Instead, the static
    get(id) function should be used
    """
    def __init__(self, id, player):
        self.id = id
        self.stage = None
        self.name = ""
        self.prevo = ""
        self.hp = 0
        self.maxhp = 0
        self.abilities = []
        self.pokepowers = []
        self.pokebodies = []
        self.attacks = []
        self.weakness = None
        self.resist = None
        self.retreat = 0
        self.type = []
        self.flair = None
        self.energy = EnergyBank(self)
        self.item = None
        self.player = player
        self.rotation = None  # "sleep"/"confused"/"paralyzed"
        self.tokens = []  # "burn", "poison"
        self.extra_effects = {"cantevolve": 1}
        self.one_time_used = []
        self.special_energy = []
        self.other_attached = []

    def get_card_data(self, line):
        data = line.split("|")
        self.stage = eval("Stage.{}".format(data[0]))
        self.name = data[1]
        self.prevo = data[2] if data[2] != "None" else None
        self.flair = eval("Flair.{}".format(data[3]))
        self.hp = int(data[4])
        self.maxhp = int(data[4])
        if self.flair in [Flair.DELTA, Flair.LEGEND]:
            for t in data[5].split(","):
                self.type.append(eval("Type.{}".format(t)))
        else:
            self.type.append(eval("Type.{}".format(data[5])))
        self.weakness = eval("Type.{}".format(data[6])) if data[6] != "None" else None
        self.resist = eval("Type.{}".format(data[7])) if data[7] != "None" else None
        self.retreat = int(data[8])
        extras = data[9]
        if "?" in extras:  # pokebodies
            self.pokebodies = extras.split("?")[1].split(",")
            extras = extras.split("?")[0]
        if "!" in extras:  # pokepowers
            self.pokepowers = extras.split("!")[1].split(",")
            extras = extras.split("!")[0]
        if ";" in extras:  # abilities
            self.abilities = extras.split(";")[1].split(",")
            extras = extras.split(";")[0]
        if "@" in extras:  # scripts
            self.attacks = extras.split("@")[1].split(",")

    def use_attack(self, index, target):
        """ Uses the attack at a given index on the given target

        :param index: the index of the attack to use
        :param target: the opposing player's active pokemon
        :raises NotEnoughEnergy: if this pokemon does not have enough
            energy to use that attack.
        """
        if "cantattack" in self.extra_effects.keys():
            return
        if self.rotation == "confused" and not self.player.flip_coin():
            self.take_damage(30, self, "nomod")
            return
        if self.rotation == "paralyzed":
            return
        # imports = ""
        # for i in self.attacks:
        #     imports += i + ", "
        # imports = imports[:len(imports)-2]
        exec("from data.scripts.{} import {}".format(self.id.split("-")[0], self.attacks[index]))
        exec("{}(self, target)".format(self.attacks[index]))
        self.player.end_turn()

    def use_ability(self, index, target=None):
        if len(self.abilities) > 0:
            exec("from data.scripts.{} import {}".format(self.id.split("-")[0], self.abilities[index]))
            exec("{}(self)".format(self.abilities[index]))
        elif len(self.pokepowers) > 0:
            exec("from data.scripts.{} import {}".format(self.id.split("-")[0], self.pokepowers[index]))
            exec("{}(self)".format(self.pokepowers[index]))

    def take_damage(self, amount, attacker, *args):
        if "nomod" not in args:
            if "damageup" in attacker.extra_effects.keys():
                amount += attacker.extra_effects["damageup"]
            if "damagedown" in attacker.extra_effects.keys():
                amount -= attacker.extra_effects["damagedown"]
            if "damageup" in attacker.player.global_abilities:
                amount += attacker.player.global_abilities.count("damageup") * 10
                if "noweak" not in args:
                    if self.weakness in attacker.type and \
                            ("Dark" not in self.energy.keys() or "shadowcircle" != self.player.field.stadium):
                        amount *= 2
                    elif self.resist in attacker.type:
                        amount -= 20
            if "defenseup" in self.extra_effects.keys():
                amount -= self.extra_effects["defenseup"]
            if "defensedown" in self.extra_effects.keys():
                amount += self.extra_effects["defensedown"]
            if "defenseup" in self.player.global_abilities:
                amount -= self.player.global_abilities.count("defenseup") * 10
            if "plasmasteel" in self.player.global_abilities and self.type == Type.METAL and attacker.flair == Flair.EX:
                return
            if "mightyshield" in self.extra_effects.keys() and len(attacker.special_energy) > 0:
                return
        self.hp -= amount if amount > 0 else 0
        if self.hp <= 0:
            self.discard_attachments()
            if "rescuescarf" in self.extra_effects.keys():
                self.player.hand.append(self)
            else:
                if self.flair != Flair.PRISM:
                    self.player.discard.append(self.id)
                else:
                    self.player.lostzone.append(self.id)
            if self == self.player.active:
                self.player.active = self.player.prompt_select_ally("notactive", "remove")
            if self in self.player.bench:
                self.player.bench.remove(self)
            if self.player != attacker.player:
                attacker.player.hand.append(
                    attacker.player.pull_prize()
                )
                if self.flair in [Flair.EX, Flair.GX, Flair.V, Flair.TAGTEAM]:
                    attacker.player.hand.append(
                        attacker.player.pull_prize()
                    )
                    if self.flair == Flair.TAGTEAM:
                        attacker.player.hand.append(
                            attacker.player.pull_prize()
                        )

    def discard_attachments(self):
        if self.item is not None:
            if self.item.trainertype == TrainerType.FLRE:
                self.player.opponent.discard.append(self.item)
            else:
                self.player.discard.append(self.item)
            self.player.item = None
        for key in self.energy.keys():
            if key.upper() in Type.__members__:
                for _ in range(self.energy[key]):
                    self.player.discard.append(key.lower())
        self.player.discard.extend(self.special_energy)
        self.player.discard.extend(self.other_attached)
        self.special_energy = []
        self.other_attached = []
        self.energy.clear()
        self.item = None

    def end_turn(self, was_my_turn):
        self.one_time_used = []
        if was_my_turn:
            if self.rotation == "paralyzed":
                self.rotation = None
            if "cantattack" in self.extra_effects.keys():
                self.extra_effects.pop("cantattack")
        if "burned" in self.tokens and not self.player.flip_coin():
            self.take_damage(20, self, "nomod")
            if "flamingfighter" in self.player.opponent.global_abilities:
                self.take_damage(40, self, "nomod")
        if "poison" in self.tokens:
            self.take_damage(10, self, "nomod")
            if self.player.field.stadium == "virbank":
                self.take_damage(20, self, "nomod")
        if "cantevolve" in self.extra_effects.keys():
            self.extra_effects.pop("cantevolve")


class EnergyCard:
    """ Represents an Energy Card with a specific type of energy. This class
    should not be initialized by the user. Instead, the static get(id) function
    should be used
    """
    def __init__(self, type, player):
        self.id = type
        self.type = eval("Type.{}".format(type.upper()))
        self.typestring = type.title()
        self.player = player
        self.override_cap = False

    def check_infinite_energy(self):
        if self.typestring == "Fire" and "infernofandango" in self.player.global_abilities\
                or self.typestring == "Water" and "deluge" in self.player.global_abilities\
                or self.typestring == "Electric" and "magneticcircuit" in self.player.global_abilities:
            self.override_cap = True

    def use(self, pokemon):
        self.check_infinite_energy()
        if "energy" in self.player.has_done and not self.override_cap:
            raise TurnEnergyCapReached
        if self.typestring in pokemon.energy.keys():
            pokemon.energy[self.typestring] += 1
        else:
            pokemon.energy[self.typestring] = 1
        pokemon.other_attached.append(self.id)
        if not self.override_cap:
            self.player.has_done.append("energy")


class TrainerCard:
    """ Represents a Trainer Card that has the data of a specific trainer card.
    This class should not be initialized by the user. Instead, the static
    get(id) function should be used
    """
    def __init__(self, id, player):
        self.id = id
        self.trainertype = None
        self.name = None
        self.effect = None
        self.player = player
        self.data = {}  # data to be stored by trainer cards when necessary

    def get_card_data(self, line):
        data = line.split("|")
        self.trainertype = eval("TrainerType.{}".format(data[0]))
        self.name = data[1]
        self.effect = data[2]
        if len(data) > 3:
            for item in data[3].split(";"):
                key, value = item.split("=")
                self.data[key] = eval(value)

    def use(self):
        if self.trainertype == TrainerType.TOOL:  # give to a pokemon
            target = self.player.prompt_select_ally() if "target" not in self.data.keys() else self.data["target"]
            if target.item is not None:
                raise PokemonAlreadyHasItem
            target.item = self
            exec("from data.scripts.{} import {}_added".format(self.id.split("-")[0], self.effect))
            exec("{}_added(target)".format(self.effect))
        elif self.trainertype == TrainerType.ENRG:  # attach to a pokemon
            if "energy" in self.player.has_done and not ("overridecap" in self.data.keys() and self.data["overridecap"]):
                raise TurnEnergyCapReached
            target = self.player.prompt_select_ally() if "target" not in self.data.keys() else self.data["target"]
            target.special_energy.append(self.id)
            target.other_attached.append(self.id)
            exec("from data.scripts.{} import {}_added".format(self.id.split("-")[0], self.effect))
            exec("{}_added(target)".format(self.effect))
            if not ("overridecap" in self.data.keys() and self.data["overridecap"]):
                self.player.has_done.append("energy")
        elif self.trainertype == TrainerType.FLRE:  # give to an enemy pokemon
            target = self.player.prompt_select_opp() if "target" not in self.data.keys() else self.data["target"]
            if target.item is not None:
                raise PokemonAlreadyHasItem
            target.item = self
            exec("from data.scripts.{} import {}_added".format(self.id.split("-")[0], self.effect))
            exec("{}_added(target)".format(self.effect))
        elif self.trainertype == TrainerType.ITEM:  # actually use
            exec("from data.scripts.{} import {}".format(self.id.split("-")[0], self.effect))
            exec("{}(self)".format(self.effect))
            self.player.discard.append(self.id)
        elif self.trainertype == TrainerType.STAD:  # set up stadium
            if self.player.field.stadcard is not None:
                self.player.field.stadcard.player.discard.append(self.player.field.stadcard.id)
            self.player.field.stadium = self.effect
            self.player.field.stadcard = self
        elif self.trainertype == TrainerType.SUPP:  # use
            if "supporter" in self.player.has_done:
                raise TurnSupporterCapReached
            exec("from data.scripts.{} import {}".format(self.id.split("-")[0], self.effect))
            exec("{}(self)".format(self.effect))
            self.player.has_done.append("supporter")
            self.player.discard.append(self.id)
        # self.player.hand.remove(self)
