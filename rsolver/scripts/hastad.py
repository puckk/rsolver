#!/usr/bin/env python3
import functools
import itertools


def chinese_remainder(n, a): # https://rosettacode.org/wiki/Chinese_remainder_theorem
    sum = 0
    prod = functools.reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b): # https://rosettacode.org/wiki/Chinese_remainder_theorem
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def inv_pow(c, e):
    low = -1
    high = c+1
    while low + 1 < high:
        m = (low + high) // 2
        p = pow(m, e)
        if p < c:
            low = m
        else:
            high = m
    m = high
    assert pow(m, e) == c
    return m



def check(solver):
    if (len(solver.datas["n"])> 1):
        if (len(solver.datas["n"])==len(solver.datas["c"])):
            return True

def crack(solver):
    N = solver.datas["n"]
    C = solver.datas["c"]

    e = len(N)
    a = chinese_remainder(N, C)
    #solver.datas["d"].append(a)
    solver.adde(e)

    # for n, c in zip(N, C):
    #      assert a % n == c
    m = inv_pow(a, e)
    solver.datas["chinese_m"]=m
    
