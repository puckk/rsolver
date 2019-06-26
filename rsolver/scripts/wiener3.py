# The big Wiener attack
# Claude Jaspart - June 14th, 2016
# claude_jaspart at hotmail.com
# elmacfish / root-me.org
#
# python wiener.py
#
# Enjoy !

import math
from fractions import gcd
import gmpy2


#checking if d is odd
def verif_odd_den(den) :
        if den%2 == 1:
                return True
        else:
                return False



#checking if the roots are whole numbers
def verif_quadra(phi, N) :
        # coefficients are initialized
        a=1
        b=phi - N - 1
        c=N

        #calculation of the determinant
        delta = b*b-4*a*c
        if delta < 0 :
                return  False

        #processing the roots
        n=gmpy2.mpz(delta)
        gmpy2.get_context().precision=2048
        det=gmpy2.sqrt(n)

        num1 = (-b + det)
        num2 = (-b - det)
        den  = 2*a

        k1 = int(num1//den)
        r1 = num1 - k1 * den

        k2 = int(num2//den)
        r2 = num2 - k2 * den

        if  r1 == 0.0 and r2 == 0.0 :
                return True
        else:
                return False


#calculates the phi(N)
def calc_phi(e,k,d) :
        num = ( e * d - 1)
        den = k

        r = int(num//den)

        if num - r * den == 0:
                return num//den
        else :
                return 0


def check(solver):
    if (solver.datas["n"] and solver.datas["e"]):
        return True
    return False

def crack (solver):

    e=solver.datas["e"][-1]
    N=solver.datas["n"][-1]


    # continued fraction coefficient processing part
    eprime = e
    nprime = N
    coeff = []
    profondeur = 0        # defines how many coefficients there are

    coeff.append(0)
    while (eprime >= 1):
            profondeur = profondeur + 1
            k = int(nprime//eprime)
            r = nprime - k * eprime
            coeff.append(k)
            nprime = eprime
            eprime = r



    # prints the continued fractions coefficients
    '''
    for i in coeff:
            print i,

    print ''
    '''

    # calcul du (num/den) de la fraction pour chaque profondeur
    found = False                #for the end message
    for n in range (1,profondeur) :

            # counter init
            cptr = n

            # starting values
            num = coeff[cptr]        # start from right to left in the coeff array
            den = 1

            while ( cptr > 0 ) :

                    # swap denominator and numerator
                    tmpnum = num
                    num = den
                    den = tmpnum

                    # processing the new value of the numerator,
                    # denominator doesnt change
                    num = coeff[cptr-1] * den + num

                    # preparing to retrieve previous coefficient
                    cptr = cptr - 1

            # some debug prints
            #print 'k/d = ' , num, '/', den

            #calculates phi
            phi = calc_phi(e,num,den)

            # tests all 3 criteria and exits at first valid value
            if ( (phi > 0) and verif_odd_den(den) and verif_quadra(phi, N)):
                    solver.addd(den)
                    return True
                    found = True
                    break
