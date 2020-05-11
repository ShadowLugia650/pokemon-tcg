from data.scripts._util import check_energy_cost


def wavesplash(attacker, defender):
    check_energy_cost(attacker, 2, Water=1)
    defender.take_damage(30, attacker)


def blessingsofthedeep(user):
    if "blessingdeep" in user.one_time_used:
        return
    sel = user.player.prompt_select_ally(has_energy="water")
    sel.hp += 20
    if sel.hp > sel.maxhp:
        if "hpboost" in sel.extra_effects.keys():
            if sel.hp > sel.maxhp + sel.extra_effects["hpboost"]:
                sel.hp = sel.maxhp + sel.extra_effects["hpboost"]
        else:
            sel.hp = sel.maxhp
    user.one_time_used.append("blessingdeep")


def dragonpulse(attacker, defender):
    check_energy_cost(attacker, 1, Electric=1)
    defender.take_damage(40, attacker)
    for _ in range(2):
        attacker.player.discard.append(attacker.player.deck.draw().id)


def skyjudgment(attacker, defender):
    check_energy_cost(attacker, 4, Fire=1, Electric=2)
    defender.take_damage(190, attacker)
    for _ in range(3):
        energy = attacker.player.prompt_select_other(attacker.energy.as_card_list())
        attacker.energy[energy.typestring] -= 1
        attacker.other_attached.remove(energy.id)
        attacker.player.discard.append(energy.id)
