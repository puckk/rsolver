from fractions import gcd
from Crypto.Util.number import long_to_bytes


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist.')
    else:
        return x % m


def attack(c1, c2, e1, e2, N):
    if gcd(e1, e2) != 1:
        raise ValueError("Exponents e1 and e2 must be coprime")
    s1 = modinv(e1, e2)
    s2 = (gcd(e1, e2) - e1 * s1) // e2
    temp = modinv(c2, N)
    m1 = pow(c1, s1, N)
    m2 = pow(temp, -s2, N)
    return (m1 * m2) % N


def check(solver):
    if len(solver.datas["n"]) == 2 \
     and len(solver.datas["e"]) == 2 \
     and len(solver.datas["c"]) == 2:
        if solver.datas["n"][0] == solver.datas["n"][1]:
            return True
    return False


def crack(solver):
    c1 = solver.datas["c"][0]
    c2 = solver.datas["c"][1]
    e1 = solver.datas["e"][0]
    e2 = solver.datas["e"][1]
    n = solver.datas["n"][0]
    plain = attack(c1, c2, e1, e2, n)
    solver.datas["plaintext"] = long_to_bytes(plain)
