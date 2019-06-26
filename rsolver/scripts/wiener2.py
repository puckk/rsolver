import owiener
from functools import reduce

def check(solver):
    if (solver.datas["e"] and solver.datas["n"]):
        return True



def crack(solver):

    e= (reduce(lambda x, y: x*y, solver.datas["e"]))
    d = owiener.attack(e, solver.datas["n"][-1])

    if d is None:
        pass
    else:
        solver.addd(d)
        solver.adde(e)
