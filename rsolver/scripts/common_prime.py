from secrets import randbits
from sympy import nextprime, gcd
from timeit import default_timer as timer
import gmpy2

def check(solver):
    if len(solver.datas["n"]) == 2 > 0:
        return True
    return False


def crack(solver):
    n1 = solver.datas["n"][0]
    n2 = solver.datas["n"][1]
    e = solver.datas["e"][0]
    g = gcd(n1, n2)

    if g == 1:
        pass
    elif (n1/g) == int(n1/g):
        
        if gmpy2.is_prime(int(g)):
            print("here",g)
            p = g
            q1 = n1/p
            q2 = n2/p
            solver.addpriv(int(p), int(q1), e, n1)
            solver.addpriv(int(p), int(q2), e, n2)
