from data.scripts._util import check_energy_cost
from card import get


def brilliantflare(attacker, defender):
    check_energy_cost(attacker, 4, Fire=3)
    defender.take_damage(180, attacker)
    for _ in range(3):
        attacker.player.hand.append(attacker.player.prompt_card_from_deck("skippable"))


def crimsonflamepillar(attacker, defender):
    if attacker.player.gx_used:
        return
    check_energy_cost(attacker, 1, Fire=1)
    for _ in range(5):
        energy = attacker.player.prompt_select_other([get(i) for i in attacker.player.discard], "isenergy", "basic")
        target = attacker.player.prompt_select_ally()
        energy.override_cap = True
        energy.use(target)
    if attacker.energy.total() >= 2:
        defender.rotation = "confused"
        defender.tokens.append("burned")
