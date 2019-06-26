
import gmpy2
import binascii
import sys
import sympy
import os


def check(solver):

    if (len(solver.datas["n"])>0):
        if (len(str(solver.datas["n"][-1])) > 150000):
            return True
    return False


def inv(x, m):
    return sympy.invert(x, m)



def get_prime_under(n):
    primes = [2]
    for i in range(3, n):
        sqrt = i ** (0.5)
        for p in primes:
            if p <= sqrt:
                if i % p == 0:
                    break
            else:
                primes.append(i)
                break
    return primes

def prime_factorize(n):
    primes = get_prime_under(65538)
    count = [0] * len(primes)
    for idx in range(len(primes)):
        while n % primes[idx] == 0 and n != 1:
            count[idx] += 1
            n = n // primes[idx]
    return primes, count, n

def phi_function(primes, count_of_primes):
    phi = 1
    for (p, c) in zip(primes, count_of_primes):
        phi = phi * ((p ** (c - 1)) * (p - 1))
    return phi


def crack(solver):

    e = int(solver.datas["e"][-1])
    n = int(solver.datas["n"][-1])
    cipher_text = int(solver.datas["c"][-1])

    print('calculate prime factors')
    primes, count_of_primes, rest = prime_factorize(n)
    new_primes, new_count = [], []
    # output prime factors
    print('prime factors')
    for p, c in zip(primes, count_of_primes):
        if c > 0:
            print(p, ':', c)
            new_primes.append(p)
            new_count.append(c)
    print('rest: ', rest)
    primes, count_of_primes = new_primes, new_count

    print('calculate private key')
    solver.addphi(phi_function(primes, count_of_primes))
    solver.addd(int(inv(e, solver.datas["phi"][-1])))

    solver.datas["multin_primes"]=primes
    solver.datas["multin_count_of_primes"]=count_of_primes
    # plain_text = crt_speedup_decrypt(cipher_text, solver.datas["d"][-1], primes, count_of_primes, n)
