
from random import random, randint, seed, choice

seed(7)
B = set(range(0, 10))
P = set(range(0, 1000))
T = set(range(0, 12))


# presupuesto maximo
M = { t: 100_000_000 for t in T }

cap = { b: randint(0, 1000) for b in B }
exp = { p: randint(6, 24) for p in P}

stock_init = { (p, b, e): randint(0, 3000) 
    for p in P  
    for b in B
    for e in range(0, exp[p])
}

guarda = { (p, b): randint()
    for p in P
    for b in B
}
vol = { p: random()*10 for p in P }
unit = {p: choice(12, 24, 50, 100) for p in P}
costo = { p: randint(10_000, 400_000) for p in P}

d = { (p, t): random() * 1000 
    for p in P
    for t in T 
}

stock_crit = { (p, b): random(0, 1000)
    for p in P
    for b in B
}
tmv = 1