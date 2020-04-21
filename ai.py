from card import Stage, PokemonCard, Flair, EnergyCard, TrainerCard, TrainerType, Type
import random
from data.scripts.ai_math import *
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
        print([i.id for i in self.player.hand])
        inplay = [self.player.active] + self.player.bench
        handweights = self.gen_hand_weights(inplay)
        best = argmax(handweights)
        while handweights[best][0] >= 0:  # fix later to include negatives, but never play -1 or lower
            card = self.player.hand.pop(best)
            if type(card) == PokemonCard:
                if card.stage == Stage.BASIC:
                    if len(self.player.bench) == 5:
                        handweights[best] = (-2, None)
                        return
                    self.player.bench.append(card)
                else:
                    evo_from = [i for i in inplay if i.name == card.prevo and "cantevolve" not in i.extra_effects]
                    if len(evo_from) == 0:
                        handweights[best] = (-2, None)
                        return
                    self.player.evolve(evo_from[0], card)
            elif type(card) == EnergyCard:
                if "energy" in self.player.has_done:
                    handweights[best] = (-2, None)
                    return
                card.use(handweights[best][1])
            handweights.pop(best)
            handweights = self.gen_hand_weights(inplay)
            best = argmax(handweights)
        self.player.end_turn()
        self.player.opponent.start_turn()
        self.player.field.is_player_turn = True

    def gen_hand_weights(self, inplay, avoid_recursion=False):
        handweights = []  # Elements in form (weight, extra_data)
        for card in self.player.hand:
            if type(card) == PokemonCard:
                name = card.name + "{}".format(card.flair).split(".")[1] if card.flair != Flair.NONE else card.name
                x = inplay.count(card)
                weight = eval(self.weights["Play"][name])
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
                            x = pk.energy[card.typestring] if card.typestring in pk.energy else 0
                            # t = pk.energy.total()
                            weight = eval(self.weights["Energy"][card.typestring][name])
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
