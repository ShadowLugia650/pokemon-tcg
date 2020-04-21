""" NOTE: This still does not work atm.

"""
from data.scripts.ai_math import *
import random


def gen_vals(func, slopes):
    v = random.uniform(-1, 2)
    h = random.uniform(-3, 3)
    g = random.uniform(0, 10)
    w = random.uniform(0, 5)
    t = random.uniform(-3, 3)
    if func == "exp_decay":
        return {"g": g, "v": v, "h": h}
    elif func == "sigmoid":
        return {"g": g, "t": t, "v": v, "h": h}
    elif func == "bump":
        return {"g": g, "w": w, "t": t, "v": v, "h": h}


def choose_func(labeled_data, slopes=None):
    slopes = get_slopes(labeled_data) if slopes is None else slopes


def get_slopes(labeled_data):
    sorted_keys = sorted(labeled_data.keys())
    prev = None
    slopes = {}
    for key in sorted_keys:
        ybar = sum(sorted_keys[key]) / 2
        if prev is not None:
            slopes[key, prev[0]] = ybar - prev[1]
        prev = key, ybar
    return slopes


def find_curve(labeled_data, func=None):
    """ Used for developing a .alg file for the ai. Finds a curve that fits
    the given labeled_data.

    :param labeled_data: a dict of items in the form
        {x : (ymin, ymax)}. ex. {1:(-1, 0), 2:(0, 1)}
    :param func: None
        Uses the specified func if it is given. Otherwise selects a function
        based on the dataset
    :return: the constants and type of function to use.
    """
    func = choose_func(labeled_data) if func is None else func
    slopes = get_slopes(labeled_data)
    consts = gen_vals(func, slopes)
    mismatched = [-1, -1]  # (above, below)
    while mismatched != [0, 0]:
        for key in labeled_data:
            yhat = eval("{}(**consts, x=key)".format(func))
            if yhat > labeled_data[key][1]:
                mismatched[0] += 1
            elif yhat < labeled_data[key][0]:
                mismatched[1] += 1
        print(mismatched)
    return func, consts
