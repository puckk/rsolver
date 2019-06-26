import sympy

def check(solver):
    if (len(solver.datas["dp"]) > 0 and len(solver.datas["dq"]) > 0 and len(solver.datas["qinv"]) > 0):
        return True
    return False

def crack(solver):
    dp=solver.datas["dp"][-1]
    dq=solver.datas["dq"][-1]
    qinv=solver.datas["qinv"][-1]

    #Common, maybe bad
    if len(solver.datas["e"])==0:
        solver.datas["e"].append(65537)

    e =solver.datas["e"][-1]
    results = []
    d1p = dp * e - 1
    for k in range(3, e):
        if d1p % k == 0:
            hp = d1p // k
            p = hp + 1
            if sympy.isprime(p):
                d1q = dq * e - 1
                for m in range(3, e):
                    if d1q % m == 0:
                        hq = d1q // m
                        q = hq + 1
                        if sympy.isprime(q):
                            if (qinv * q) % p == 1 or (qinv * p) % q == 1:
                                solver.addp(p)
                                solver.addq(q)
