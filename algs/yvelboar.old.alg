Play:
    YveltalEX = 2 - 0.75 * x
    Tepig = -1 + math.exp(-1.1 * (x-1))
    Pignite = 2
    Emboar = 2
    DarkraiEX = 1 - 2 * math.ceil(x/4)
    Baltoy = 2 - x
    Claydol = 2
    Sentret = 0.75 - 1.75 * math.ceil(x/4)
    Furret = 2
    Deino = 0.5 - 1.5 * math.ceil(x/4)
    Zweilous = 2
    Hydreigon = 2
    Landorus = 0.5 - 1.5 * math.ceil(x/4)
Energy:
    Dark:
        YveltalEX = math.exp(-0.36 * (x-2))
        DarkraiEX = -0.7 + math.exp(-0.68 * (x-1))
        Tepig = -1 + math.exp(-0.27 * x)
        Pignite = -1 + math.exp(-0.49 * (x-0.45))
        Emboar = -1
        Baltoy = -1 + math.exp(-0.63 * (x-0.65))
        Claydol = -1 + math.exp(-0.7 * (x+1))
        Sentret = -1 + math.exp(-0.36 * (x+2))
        Furret = -1
        Deino = -1 + math.exp(-2 * (x-0.35))
        Zweilous = -1 + math.exp(-2 * (x-0.2))
        Hydreigon = -1
        Landorus = -1
    Fire:
        YveltalEX = math.exp(-0.14 * (x-5))
        DarkraiEX = -1 + math.exp(-10 * (x-0.07))
        Tepig = 1 - 2 / (1 + math.exp(-8.2 * (x-1.2)))
        Pignite = 1 - 2 / (1 + math.exp(-1.4 * (x-1.1)))
        Emboar = bump(10, 1.65, 1.6, -3, 0.4, 1.9, x)
        Baltoy = -1 + math.exp(-0.63 * (x-0.65))
        Claydol = -1 + math.exp(-0.7 * (x+1))
        Sentret = -1 + math.exp(-0.36 * (x+2))
        Furret = -1
        Deino = -1 + math.exp(-2 * (x-0.35))
        Zweilous = -1 + math.exp(-2 * (x-0.2))
        Hydreigon = -1
        Landorus = -1
    Fighting:
        YveltalEX = math.exp(-0.36 * (x-2))
        DarkraiEX = -1 + math.exp(-10 * (x-0.07))
        Tepig = -1 + math.exp(-0.27 * x)
        Pignite = -1 + math.exp(-0.49 * (x-0.45))
        Emboar = -1
        Baltoy = -1 + math.exp(-0.63 * (x-0.65))
        Claydol = -1 + math.exp(-0.7 * (x+1))
        Sentret = -1 + math.exp(-0.36 * (x+2))
        Furret = -1
        Deino = -1
        Zweilous = -1
        Hydreigon = -1
        Landorus = bump(10, 2.06, -0.55, -2, 1.55, 0, x)