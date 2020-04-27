Play:
    YveltalEX = 2 - 0.75 * x
    Tepig = bound(exp_decay(1.1, -1, 1, x))
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
        YveltalEX = bump(10, 1.76, -1, -0.95, 2, 0.93, x)
        DarkraiEX = bump(10, 0.74, -0.43, -2, 1.43, 0.93, x)
        Tepig = sigmoid(15, -1, 0, 0.6, x)
        Pignite = sigmoid(15, -1.2, 0.2, 0.7, x)
        Emboar = -1
        Baltoy = sigmoid(15, -1.08, 0.08, 0.6, x)
        Claydol = sigmoid(15, -1.08, 0.08, 0.6, x)
        Sentret = sigmoid(15, -1.03, 0.03, 1.23, x)
        Furret = -1
        Deino = sigmoid(3.9, -1.4, 0.4, 1.23, x)
        Zweilous = sigmoid(15, -0.8, -0.2, 1.5, x)
        Hydreigon = -1
        Landorus = -1
    Fire:
        YveltalEX = exp_decay(0.2, 0, 3.25, x)
        DarkraiEX = sigmoid(15, -2, 1, 0.6, x)
        Tepig = sigmoid(8.2, -2, 1, 1.2, x)
        Pignite = bump(7.8, 1.56, 0.95, -2.6, 0.65, 1.07, x)
        Emboar = bump(10, 2.55, 1.6, -3, 0.4, 1, x)
        Baltoy = sigmoid(15, -1.18, 0.18, 0.6, x)
        Claydol = sigmoid(15, -1.18, 0.18, 0.6, x)
        Sentret = sigmoid(15, -1.18, 0.18, 1.23, x)
        Furret = sigmoid(15, -1.09, 0.09, 0.6, x)
        Deino = sigmoid(4.4, -2, 1, 1.1, x)
        Zweilous = bump(15, 1.05, 0.98, -2.4, 0.42, 0.5, x)
        Hydreigon = -1
        Landorus = sigmoid(15, -1.2, 0.2, 0.54, x)
    Fighting:
        YveltalEX = math.exp(-0.36 * (x-2))
        DarkraiEX = sigmoid(15, -1.18, 0.18, 0.6, x)
        Tepig = sigmoid(15, -1.03, 0.03, 1.23, x)
        Pignite = sigmoid(15, -1.03, 0.03, 1.23, x)
        Emboar = -1
        Baltoy = sigmoid(15, -1.08, 0.08, 0.6, x)
        Claydol = sigmoid(15, -1.08, 0.08, 0.6, x)
        Sentret = sigmoid(15, -1.03, 0.03, 1.23, x)
        Furret = -1
        Deino = -1
        Zweilous = -1
        Hydreigon = -1
        Landorus = bump(10, 2, -0.55, -2, 1.55, 0, x)
Trainer:
    Cynthia = bump(15, 3.03, -1.5, -1.5, 2, 2.4, total_value(p.ai))
    Muscle Band:
        YveltalEX = 2
        DarkraiEX = 1.7
        Tepig = -1
        Pignite = -1
        Emboar = -1
        Baltoy = -1
        Claydol = -1
        Sentret = -1
        Furret = -1
        Deino = -1
        Zweilous = -1
        Hydreigon = -1
        Landorus = -1
    Ultra Ball = -1
    Roseanne's Research = 2
    Pokemon Catcher = -1
    Rare Candy = -1
    Darkness Energy:
        YveltalEX = 2
        DarkraiEX = 1.7
        Tepig = -1
        Pignite = -1
        Emboar = -1
        Baltoy = -1
        Claydol = -1
        Sentret = -1
        Furret = -1
        Deino = -1
        Zweilous = -1
        Hydreigon = -1
        Landorus = -1
    Celio's Network = 1.9
    Hypnotoxic Laser = 2
    Double Colorless Energy:
        YveltalEX = 2
        DarkraiEX = -1
        Tepig = -1
        Pignite = -1
        Emboar = -1
        Baltoy = -1
        Claydol = -1
        Sentret = -1
        Furret = -1
        Deino = -1
        Zweilous = -1
        Hydreigon = -1
        Landorus = -1
    Colress = bound(1.5 * (len(p.bench) + len(p.opponent.bench)) - total_value(p.ai))
    Virbank City Gym = 2
    Switch = -1
Attacks:
    YveltalEX:
        0 = sigmoid(3.5, 3, -1, 2.1, t)
        1 = 0.2
    DarkraiEX:
        0 = 2
    Tepig:
        0 = sigmoid(15, -3, 2, 1.54, t)
        1 = 1.9
    Pignite:
        0 = sigmoid(15, -3, 2, 2.54, t)
        1 = 1.9
    Emboar:
        0 = 2
    Baltoy:
        0 = bound(len(p.opponent.hand) - len(p.hand))
        1 = 1
    Claydol:
        0 = 2
    Sentret:
        0 = sigmoid(15, -3, 2, 1.54, t)
        1 = 1.9
    Furret:
        0 = 2
        1 = -1
    Deino:
        0 = sigmoid(15, -3, 2, 2.54, t)
        1 = 1.9
    Zweilous:
        0 = 2
        1 = -1
    Hydreigon:
        0 = -1
    Landorus:
        0 = sigmoid(15, -3, 2, 2.54, t)
        1 = 1.9
ActiveValue:
    YveltalEX = two_slope_bump(15, 1, 1, 2, 1, -1, 1.5, t)
    DarkraiEX = sigmoid(15, 2.5, -1, 2.5, t)
    Tepig = sigmoid(15, 1.2, -0.8, 0.5, t)
    Pignite = sigmoid(15, 1.6, -1, 2.4, t)
    Emboar = sigmoid(15, 1.6, -1, 3.34, t)
    Baltoy = sigmoid(15, 1.15, -0.87, 0.56, t)
    Claydol = -1
    Sentret = bump(15, 1.07, 0.45, 0.2, -0.1, 0.56, t)
    Furret = 1
    Deino = bump(15, 1.07, 1.3, 0.2, -0.83, 1.4, t)
    Zweilous = sigmoid(15, 1.3, -1, 1.4, t)
    Hydreigon = -1
    Landorus = sigmoid(15, 1.15, -0.55, 0.56, t)