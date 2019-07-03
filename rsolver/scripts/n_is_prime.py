from factordb.factordb import FactorDB
import libnum


def check(solver):
    if (len(solver.datas["n"]) > 0 and len(solver.datas["e"]) > 0):
        return True

def crack(solver):
    n = solver.datas["n"][-1]
    e = solver.datas["e"][-1]
    a = FactorDB(n)
    a.connect()
    if (a.get_status() == "P"):
        d = libnum.modular.invmod(e, n-1)
        solver.addd(d)
