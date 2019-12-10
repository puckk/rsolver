from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import gmpy2

def check(solver):
    if (len(solver.datas["n"]) > 0 and len(solver.datas["e"]) > 0):
        return True

def crack(solver):
	e = solver.datas["e"][-1]
	n = solver.datas["n"][-1]
	for k in range(1, 1000000):
		if gmpy2.iroot(1+4*e*n*k, 2)[1]:
			q = int((1 + int(gmpy2.iroot(1+4*e*n*k, 2)[0]))//(2*e))
			solver.addq(q)
			if n % q == 0:
				p = n // q
				solver.addp(p)
				phin = (p - 1) * (q - 1)
				d = inverse(e, phin)
				solver.addd(d)
				break
