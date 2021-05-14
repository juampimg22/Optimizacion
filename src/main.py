
from math import e
from params import *
import gurobipy as gb




m = gb.Model()

# VARIABLES
stock = m.addVars((p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
qvend = m.addVars((p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
qexp = m.addVars((p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
qtransf = m.addVars((p, t, b0, b1,  e)
    for p in P
    for t in T
    for b0 in B
    for b1 in B
    for e in range(0, exp[p])
)
qcons = m.addVars((p, t, b, e)
    for p in P
    for t in T
    for b in B
    for e in range(0, exp[p])
)
#1.- No sobrepasar el presupuesto m ́aximo.
m.addConstrs(
    for t in T
    for p in P
    for b in B
    for e in range(0, exp[p])
)

m.addVars(

)




