from data.scripts._util import check_energy_cost
from card import get


def livecoal(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    defender.take_damage(10, attacker)


def rearkick(attacker, defender):
    check_energy_cost(attacker, 2, Fire=1)
    defender.take_damage(20, attacker)


def flare(attacker, defender):
    check_energy_cost(attacker, 1, Fire=1)
    defender.take_damage(20, attacker)


def flamethrower(attacker, defender):
    check_energy_cost(attacker, 3, Fire=2)
    defender.take_damage(80, attacker)
    energy = attacker.player.prompt_select_other(attacker.energy.as_card_list())
    attacker.energy[energy.typestring] -= 1
    attacker.other_attached.remove(energy.id)
    attacker.player.discard.append(energy.id)


def firespin(attacker, defender):
    check_energy_cost(attacker, 4, Fire=2)
    defender.take_damage(150, attacker)
    for _ in range(2):
        energy = attacker.player.prompt_select_other(attacker.energy.as_card_list())
        attacker.energy[energy.typestring] -= 1
        attacker.other_attached.remove(energy.id)
        attacker.player.discard.append(energy.id)


def mysticaltorch(user):
    if "mysticaltorch" in user.one_time_used:
        return
    user.player.opponent.active.tokens.append("burned")
    user.one_time_used.append("mysticaltorch")


def psychicsphere(attacker, defender):
    check_energy_cost(attacker, 3, Psychic=2)
    defender.take_damage(60, attacker)


def psychicrecharge(user):
    if "psychicrecharge" in user.one_time_used:
        return
    if "psychic" not in user.player.discard:  # and somehow check for special electric energy
        return
    energy = user.player.prompt_select_other(
        [get(i, user.player) for i in user.player.discard], "isenergy", _type="psychic")
    target = user.player.prompt_select_ally("notactive")
    if "-" in energy.id:
        energy.data["overridecap"] = True
        energy.data["target"] = target
        energy.use()
    else:
        energy.override_cap = True
        energy.use(target)
    user.player.discard.remove(energy.id)
    user.one_time_used.append("psychicrecharge")


def photongeyser(attacker, defender):
    check_energy_cost(attacker, 2, Metal=1, Psychic=1)
    damage = 20 + 80 * attacker.energy["Psychic"]
    for _ in range(attacker.energy["Psychic"]):
        attacker.other_attached.remove("psychic")
        attacker.player.discard.append("psychic")
    attacker.energy.pop("Psychic")
    defender.take_damage(damage, attacker)


def skyscorchinglight(attacker, defender):
    check_energy_cost(attacker, 2, Metal=1, Psychic=1)
    if attacker.player.gx_used:
        return
    if len(attacker.player.prize) + len(defender.player.prize) > 6:
        return
    for i in [defender]+defender.player.bench:
        i.take_damage(60, "nomod")
    attacker.player.gx_used = True


def crasherwake(item):
    pass
