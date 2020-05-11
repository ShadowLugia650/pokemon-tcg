def check_energy_cost(user, total, **spec):
    """ Checks if the give user has enough energy to use the attack based on
    the given total energy cost and specific energy requirements.

    :param user: the pokemon using the move
    :param total: the total amount of required energy to use the move
    :param spec: kwargs of required amounts of specific energy types to use the
        move
    :raises NotEnoughEnergy: if the pokemon does not meet the given
        requirements
    """
    used_prism = 0
    for key in spec.keys():
        if key not in user.energy.keys():
            raise NotEnoughEnergy
        if user.energy[key] < spec[key]:
            if "Prism" not in user.energy.keys():
                raise NotEnoughEnergy
            if user.energy["Prism"] - used_prism < spec[key]:
                raise NotEnoughEnergy
            used_prism += 1
    if user.energy.total() < total:
        raise NotEnoughEnergy


class NotEnoughEnergy(Exception):
    pass


class PokemonAlreadyHasItem(Exception):
    pass


class TurnEnergyCapReached(Exception):
    pass


class TurnSupporterCapReached(Exception):
    pass


class PrizeAlreadyPicked(Exception):
    pass


class InvalidPlay(Exception):
    pass


class GameWon(Exception):
    def __init__(self, winner):
        self.message = "Game Ended. Winner:{}".format(winner)
