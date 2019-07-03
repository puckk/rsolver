from fractions import gcd


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
    s2 = (gcd(e1, e2) - e1 * s1) / e2
    temp = modinv(c2, N)
    m1 = pow(c1, s1, N)
    m2 = pow(temp, -s2, N)
    return (m1 * m2) % N
