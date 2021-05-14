

from params import *
import gurobipy as gb


m = gb.Model()

# VARIABLES
stock = m.addVars(
    (p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
qvend = m.addVars(
    (p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
qcomp = m.addVars(
    (p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
qexp = m.addVars(
    (p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
qtransf = m.addVars(
    (p, t, b0, b1,  e)
    for p in P
    for t in T
    for b0 in B
    for b1 in B
    for e in range(0, exp[p])
)
qcons = m.addVars(
    (p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)

# SET OBJECTIVE
m.setObjective(
    sum(costo[p]*qcomp[p, t, b, e] - 0.9*qvend[p, t, b, e]
        for p in P
        for t in T
        for b in B
        for e in range(0, exp[p]+1)
        ),
    gb.GRB.MAXIMIZE
)

# CONSTRAINTS

# 1.- No sobrepasar el presupuesto máximo.
m.addConstrs(
    sum(costo[p] * qcomp[p, t, b, e]
        for p in P
        for b in B
        for e in range(1, exp[p]+1)) <= M[t]
    for t in T
)

# 2.- Solo se pueden comprar productos nuevospque les quedeexppperiodos para expirar
m.addConstrs(
    qcomp[p, t, b, e] == 0
    for t in T
    for p in P
    for b in B
    for e in range(0, exp[p])
)

# 3.  No se pueden comprar productos para bodegas periféricas, sino que lo que se compra se dirigea los kardex.
m.addConstrs(
    qcomp[p, t, b, e] == 0
    for t in T
    for p in P
    for b in B
    for e in range(0, exp[p]+1)
)

# 4.- No se sobrepasa la capacidad de la bodegab
m.addConstrs(
    sum(stock[p, t, b, e] * vol[p] <= cap[b]
        for p in P
        for e in range(1, exp[p]+1))
    for t in T
    for b in B
)

# 5.-
m.addConstrs(
    qexp[p, t, b, 0] == stock[p, t, b, 0]
    for t in T
    for b in B
    for p in P
)

m.addConstrs(
    qexp[p, t, b, e] == 0
    for t in T
    for b in B
    for p in P
    for e in range(1, exp[p]+1)
)
# 6.  No hay productospguardados en una bodega que no está habilitada para `p`.
m.addConstrs(
    stock[p, t, b, e] * vol[p] <= cap[b] * guarda[p, b]
    for t in T
    for b in B
    for p in P
    for e in range(0, exp[p]+1)
)
# 7.  No bajar del stock crítico
m.addConstrs(
    sum(stock[p, t, b, e] >= stock_crit[p, b]
        for e in range(1, exp[p]+1))
    for t in T
    for b in B
    for p in P
)
# 8.  El stock en el periodo `t = 0` es igual al stock inicial
m.addConstrs(
    stock[p, 0, b, e] == stock_init[p, b, e]
    for b in B
    for p in P
    for e in range(0, exp[p]+1)
)
# 9.  Balance
m.addConstrs(
    stock[p, t+1, b, e-1] == stock[p, t, b, e] + qcomp[p, t, b, e] -
    qvend[p, t, b, e] - qcons[p, t, b, e] - qexp[p, t, b, e] +
    sum(qtransf[p, t, b1, b, e]
        for b1 in B) -
    sum(qtransf[p, t, b, b1, e]
        for b1 in B)
    for b in B
    for p in P
    for t in range(0, len(T)-1)
    for e in range(1, exp[p]+1)
)
