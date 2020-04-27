from card import Stage, PokemonCard, Flair, EnergyCard, TrainerCard, TrainerType, Type
import random
from data.scripts.ai_math import *
from data.scripts._util import NotEnoughEnergy
import math  # remove later


class Algorithmic:
    def __init__(self, player):
        self.player = player
        self.weights = {}  # dict of dicts

    def load_alg(self):
        with open("data/algs/{}.alg".format(self.player.deck.preset)) as f:
            header = None
            subheader = None
            for line in f:
                line = line.replace("\n", "")
                if line == "":
                    continue
                indent = line.count("    ")
                line = line.strip()
                if indent == 0:
                    header = line.replace(":", "")
                    self.weights[header] = {}
                elif indent == 1:
                    if ":" not in line:
                        key, value = line.split(" = ")
                        self.weights[header][key] = value
                    else:
                        subheader = line.replace(":", "")
                        self.weights[header][subheader] = {}
                elif indent == 2:  # should only occur when a subheader exists
                    key, value = line.split(" = ")
                    self.weights[header][subheader][key] = value

    def choose(self, options, skippable=False):
        sel = random.choice(options)  # fix later
        return sel.id, sel

    def my_turn(self):
        self.player.start_turn()
        inplay = [self.player.active] + self.player.bench
        handweights = self.gen_hand_weights(inplay)
        print(handweights)
        best = argmax([i[0] for i in handweights])
        while best is not None and handweights[best][0] >= 0:  # fix later to include negatives, but never play -1 or lower
            card = self.player.hand.pop(best)
            if type(card) == PokemonCard:
                if card.stage == Stage.BASIC:
                    self.player.bench.append(card)
                else:
                    evo_from = [i for i in inplay if i.name == card.prevo and "cantevolve" not in i.extra_effects]
                    self.player.evolve(evo_from[0], card)
            elif type(card) == EnergyCard:
                card.use(handweights[best][1])
            elif type(card) == TrainerCard:
                if card.trainertype == TrainerType.ENRG:
                    card.data["target"] = handweights[best][1]
                    card.use()
                elif card.trainertype == TrainerType.SUPP:
                    card.use()
                elif card.trainertype == TrainerType.TOOL:
                    card.data["target"] = handweights[best][1]
                    card.use()
                elif card.trainertype == TrainerType.ITEM:
                    card.use()
            handweights.pop(best)
            handweights = self.gen_hand_weights(inplay)
            best = argmax([i[0] for i in handweights])
        self.use_attack()
        # self.player.end_turn()
        self.player.opponent.start_turn()
        self.player.field.is_player_turn = True

    def use_attack(self):
        name = self.player.active.name + "{}".format(self.player.active.flair).split(".")[1] \
            if self.player.active.flair != Flair.NONE else self.player.active.name
        attacks = {}
        t = self.player.active.energy.total()
        p = self.player
        for key in self.weights["Attacks"][name].keys():
            attacks[int(key)] = eval(self.weights["Attacks"][name][key])
        index = argmax(attacks)
        try:
            self.player.active.use_attack(index, self.player.opponent.active)
        except NotEnoughEnergy:
            print("Not enough energy to use attack {}: {}".format(index, self.player.active.attacks[index]))
            for i in attacks.keys():
                try:
                    self.player.active.use_attack(i, self.player.opponent.active)
                    break
                except NotEnoughEnergy:
                    print("Not enough energy to use attack {}: {}".format(i, self.player.active.attacks[i]))
                    self.player.end_turn()

    def gen_hand_weights(self, inplay, avoid_recursion=False):
        handweights = []  # Elements in form (weight, extra_data)
        for card in self.player.hand:
            if type(card) == PokemonCard:
                name = card.name + "{}".format(card.flair).split(".")[1] if card.flair != Flair.NONE else card.name
                x = inplay.count(card)
                weight = eval(self.weights["Play"][name])
                if card.stage == Stage.BASIC:
                    if len(self.player.bench) == 5:
                        weight = -2
                else:
                    evo_from = [i for i in inplay if i.name == card.prevo and "cantevolve" not in i.extra_effects]
                    if len(evo_from) == 0:
                        weight = -2
                handweights.append((weight, None))
            elif type(card) == EnergyCard:
                if "energy" in self.player.has_done:
                    handweights.append((-2, None))
                    continue
                energyweights = {}
                for pk in inplay:
                    name = pk.name + "{}".format(pk.flair).split(".")[1] if pk.flair != Flair.NONE else pk.name
                    x = pk.energy[card.typestring] if card.typestring in pk.energy else 0
                    # t = pk.energy.total()
                    weight = eval(self.weights["Energy"][card.typestring][name])
                    energyweights[pk] = weight
                weight, data = argmax(energyweights, return_val=True)
                if weight is None:
                    weight = -2
                handweights.append((weight, data))
            elif type(card) == TrainerCard:
                if card.trainertype == TrainerType.ENRG:
                    if "energy" in self.player.has_done:
                        handweights.append((-2, None))
                    else:
                        energyweights = {}
                        for pk in inplay:
                            name = pk.name + "{}".format(pk.flair).split(".")[1] if pk.flair != Flair.NONE else pk.name
                            # x = pk.energy[card.typestring] if card.typestring in pk.energy else 0
                            # t = pk.energy.total()
                            weight = eval(self.weights["Trainer"][card.name][name])
                            energyweights[pk] = weight
                        weight, data = argmax(energyweights, return_val=True)
                        if weight is None:
                            weight = -2
                        handweights.append((weight, data))
                elif card.trainertype == TrainerType.TOOL:
                    toolweights = {}
                    for pk in inplay:
                        name = pk.name + "{}".format(pk.flair).split(".")[1] if pk.flair != Flair.NONE else pk.name
                        p = self.player
                        weight = eval(self.weights["Trainer"][card.name][name])
                        toolweights[pk] = weight
                    weight, data = argmax(toolweights, return_val=True)
                    if weight is None:
                        weight = -2
                    handweights.append((weight, data))
                elif card.trainertype == TrainerType.SUPP:
                    if "supporter" in self.player.has_done:
                        handweights.append((-2, None))
                    else:
                        p = self.player
                        weight = 0
                        if not ("total_value" in self.weights["Trainer"][card.name] and avoid_recursion):
                            weight = eval(self.weights["Trainer"][card.name])
                        handweights.append((weight, None))
                else:
                    weight = eval(self.weights["Trainer"][card.name])
                    handweights.append((weight, None))
        print(handweights)
        print(self.player.hand)
        return handweights

    def first_turn(self):
        basic_index = [i for i in range(len(self.player.hand)) if type(self.player.hand[i]) == PokemonCard
                       and self.player.hand[i].stage == Stage.BASIC]
        handweights = self.gen_hand_weights([])
        best_basic = argmax({i: handweights[i] for i in basic_index})
        self.player.active = self.player.hand.pop(best_basic)
        while Stage.BASIC in [i.stage for i in self.player.hand if type(i) == PokemonCard]:
            basic_index = [i for i in range(len(self.player.hand)) if type(self.player.hand[i]) == PokemonCard
                           and self.player.hand[i].stage == Stage.BASIC]
            handweights = self.gen_hand_weights([self.player.active]+self.player.bench)
            best_basic = argmax({i: handweights[i] for i in basic_index})
            if handweights[best_basic][0] > 0:
                self.player.bench.append(self.player.hand.pop(best_basic))
        # self.my_turn()

    def check_switch(self):
        pass
