def check(solver):
    if (len(solver.datas["e"])>0):
        if (solver.datas["e"][-1]==1):
            return True

def crack(solver):
    solver.addd(1)
