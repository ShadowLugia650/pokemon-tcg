from card import Type


def darknessenergy_added(target):
    if "Dark" in target.energy.keys():
        target.energy["Dark"] += 1
    else:
        target.energy["Dark"] = 1
    if Type.DARK in target.type:
        if "damageup" in target.extra_effects.keys():
            target.extra_effects["damageup"] += 10
        else:
            target.extra_effects["damageup"] = 10
