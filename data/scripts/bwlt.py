from data.scripts._util import check_energy_cost


def secretsword(attacker, defender):
    check_energy_cost(attacker, 3)
    damage = 50 + attacker.energy["Water"]*20
    defender.take_damage(damage, attacker)


def rushin(user):
    if "rushin" not in user.one_time_used and user != user.player.active:
        user.player.bench.append(user.player.active)
        user.player.bench.remove(user)
        user.player.active = user
        user.one_time_used.append("rushin")


def nightspear(attacker, defender):
    check_energy_cost(attacker, 3, Dark=2)
    defender.take_damage(90, attacker)
    target = attacker.player.prompt_select_opp("notactive")
    target.take_damage(30, attacker, "noweak")


def darkcloak(user):
    user.player.global_abilities.append("darkcloak")


def energypress(attacker, defender):
    check_energy_cost(attacker, 2, Metal=1)
    damage = 20 + 20*defender.energy.total()
    defender.take_damage(damage, attacker)


def ironbreaker(attacker, defender):
    check_energy_cost(attacker, 3, Metal=2)
    defender.take_damage(80, attacker)
    defender.extra_effects["noattack"] = 1


def dragonblast(attacker, defender):
    check_energy_cost(attacker, 4, Psychic=1, Dark=2)
    defender.take_damage(140, attacker)
    attacker.energy["Dark"] -= 2
    if attacker.energy["Dark"] == 0:
        attacker.energy.pop("Dark")


def darktrance(user):
    user.player.global_abilities.append("darktrance")
