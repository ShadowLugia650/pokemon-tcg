import math


def argmax(dataset, return_val=False):
    """ returns the key of the maximum value in the dict dataset

    :param dataset: dict or list
    :param return_val: whether or not to return the value in addition to the key
    :return: the key of the largest value in dataset or (value, key)
    """
    amax = (None, None)
    dataset = {i: dataset[i] for i in range(len(dataset))} if type(dataset) == list else dataset
    for key in dataset.keys():
        if amax == (None, None):
            amax = (dataset[key], key)
        else:
            if dataset[key] > amax[0]:
                amax = (dataset[key], key)
    if return_val:
        return amax
    return amax[1]


def exp_decay(g, v, h, x):
    """ Calculates the value of f with the given variables for the exponential decay function
            f(x) = v + e^(-g * (x-h))

    :param g: the gradient (how steep the graph should be) (on a side note why isn't stepth a word)
    :param v: the vertical shift of the graph
    :param h: the horizontal shift of the graph
    :param x: variable
    :return: the calculated value of f given a, g, h, and x
    """
    return v + math.exp(-g * (x-h))


def sigmoid(g, t, v, h, x):
    """ Calculates the value of f with the given variables for the sigmoid
            f(x) = v + t / (1 + e^(-g * (x-h)))

    :param g: how steep the sigmoid is
    :param t: the height of the sigmoid curve
    :param v: vertical shift
    :param h: horizontal shift
    :param x: x variable
    :return: the calculated value of f
    """
    return v + t / exp_decay(g, 1, h, x)  # (1 + math.exp(-g * (x-h)))


def bump(g, w, l, r, v, h, x):
    """ Calculates the value of f with the given variables for the bump function:
            f(x) = (t / (1 + e^(-g * (x-h)))) + (-t / (1 + e^(-g * (x - (h+w))))) + v
        as the composition of two sigmoid functions

    :param g: the steepness of the bump
    :param w: the width of the bump
    :param l: the height of the left side
    :param r: the height of the right side
    :param v: vertical shift
    :param h: horizontal shift
    :param x: x variable
    :return: the calculated value of f
    """
    return sigmoid(g, l, 0, h, x) + sigmoid(g, r, 0, h+w, x) + v


def bound(x):
    """ Limits the x value to being bounded by [-1, 2]

    :param x: value
    :return: the x value bounded by [-1, 2]
    """
    return bump(15, 1.43, 2, 1, -1, 0, x)


def total_value(ai):
    """ Calculates the total value of a given ai's hand based on the weights of all cards in it.

    :param ai: the ai with the hand of cards to calculate the value of
    :return: the total value of the hand
    """
    handweights = ai.gen_hand_weights(ai.player.bench+[ai.player.active], avoid_recursion=True)
