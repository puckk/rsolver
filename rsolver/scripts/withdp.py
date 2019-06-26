def check(solver):
    if (len(solver.datas["e"]) == 1 and len(solver.datas["n"]) == 1 and len(solver.datas["dp"]) == 1 and len(solver.datas["c"]) == 1):
        return True

def crack(solver):
    e=solver.datas["e"][-1]
    n=solver.datas["n"][-1]
    l = solver.datas["dp"][-1] * e - 1
    p = 0
    for k in range(1, e):
        if l%k == 0:
            p = (l//k + 1)
            if n%p == 0:
                solver.addp(p)
                solver.addq( n//p)
