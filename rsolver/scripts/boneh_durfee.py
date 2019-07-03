from sage.all_cmdline import *
def crack(solver):
    sage_present = True
    try:
        _sage_const_2 = Integer(2)
        _sage_const_1 = Integer(1)
        _sage_const_0 = Integer(0)
        _sage_const_60 = Integer(60)

        # Currently this exploit is set to work if the private
        # exponent is <= N ^ 0.27. Theoretical it could be set
        # to work as long as d < N ^ 0.292 but that takes a lot
        # longer to run
        _sage_m_value = Integer(6)
        _sage_delta_value = RealNumber('0.27')
    except ImportError:
        sage_present = False

    debug = False
    global sage_present

    if not sage_present:
        print "Boneh Durfee: Sage required, skipping exploit"
        return

    print "Boneh Durfee: Running Attack..."
    success = False
    solx, soly = boneh_durfee_wrapper(solver.datas["n"][-1], solver.datas["e"][-1])

    A = int((rsadata.get_n()+_sage_const_1 )/_sage_const_2 )
    d = (solx * (A + soly) + _sage_const_1) / rsadata.get_e()
    success = True
    rsadata.set_d(long(d))

    if success:
        print "Boneh Durfee: Success, at least one private exponent recovered"
    else:
        print "Boneh Durfee: Failure, no private exponents recovered"
    return sucess


def boneh_durfee_wrapper(n, e):
    """ Wrapper for the boneh durfee exploit """
    P = PolynomialRing(Zmod(e), names=('x', 'y',)); (x, y,) = P._first_ngens(2)
    A = int((n+_sage_const_1 )/_sage_const_2 )
    pol = _sage_const_1  + x * (A + y)

    delta = _sage_delta_value
    m = _sage_m_value
    t = int((_sage_const_1 - _sage_const_2*delta)*m)

    X = _sage_const_2*floor(n**delta)
    Y = floor(n**(_sage_const_1 / _sage_const_2))

    return Boneh_Durfee.boneh_durfee(pol, e, m, t, X, Y)


def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May

    finds a solution if:
    * d < N^delta
    * |x| < e^delta
    * |y| < e^0.5
    whenever delta < 1 - sqrt(2)/2 ~ 0.292
    """

    # substitution (Herrman and May)
    PR = PolynomialRing(ZZ, names=('u', 'x', 'y',)); (u, x, y,) = PR._first_ngens(3)
    Q = PR.quotient(x*y + _sage_const_1  - u) # u = x*y + 1
    polZ = Q(pol).lift()

    UU = XX*YY + _sage_const_1

    # x-shifts
    gg = []

    for kk in range(mm + _sage_const_1 ):
        for ii in range(mm - kk + _sage_const_1 ):
            xshift = x**ii * modulus**(mm - kk) * polZ(u, x, y)**kk
            gg.append(xshift)

    gg.sort()

    # x-shifts monomials
    monomials = []

    for polynomial in gg:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)

    monomials.sort()

    # y-shifts (selected by Herrman and May)
    for jj in range(_sage_const_1 , tt + _sage_const_1 ):
        for kk in range(floor(mm/tt) * jj, mm + _sage_const_1 ):
            yshift = y**jj * polZ(u, x, y)**kk * modulus**(mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift) # substitution

    # y-shifts monomials
    for jj in range(_sage_const_1 , tt + _sage_const_1 ):
        for kk in range(floor(mm/tt) * jj, mm + _sage_const_1 ):
            monomials.append(u**kk * y**jj)

    # construct lattice B
    nn = len(monomials)

    BB = Matrix(ZZ, nn)

    for ii in range(nn):

        BB[ii, _sage_const_0 ] = gg[ii](_sage_const_0 , _sage_const_0 , _sage_const_0 )

        for jj in range(_sage_const_1 , ii + _sage_const_1 ):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)

    # check if vectors are helpful
    if debug:
        helpful_vectors(BB, modulus**mm)

    # check if determinant is correctly bounded
    if debug:
        det = BB.det()
        bound = modulus**(mm*nn)
        if det >= bound:
            print "We do not have det < bound. Solutions might not be found."
            diff = (log(det) - log(bound)) / log(_sage_const_2 )
            print "size det(L) - size e^(m*n) = ", floor(diff)
        else:
            print "det(L) < e^(m*n)"

    # debug: display matrix
    if debug:
        matrix_overview(BB, modulus**mm)

    # LLL
    BB = BB.LLL()

    # vector 1 & 2 -> polynomials 1 & 2
    PR = PolynomialRing(ZZ, names=('w', 'z',)); (w, z,) = PR._first_ngens(2)

    pol1 = pol2 = _sage_const_0
    for jj in range(nn):
        pol1 += monomials[jj](w*z+_sage_const_1 ,w,z) * BB[_sage_const_0 , jj] / monomials[jj](UU,XX,YY)
        pol2 += monomials[jj](w*z+_sage_const_1 ,w,z) * BB[_sage_const_1 , jj] / monomials[jj](UU,XX,YY)

    # resultant
    PR = PolynomialRing(ZZ, names=('q',)); (q,) = PR._first_ngens(1)
    rr = pol1.resultant(pol2)

    if rr.is_zero() or rr.monomials() == [_sage_const_1 ]:
        if debug:
            print "failure"
        return None, None

    rr = rr(q, q)
    # solutions
    try:
        soly = rr.roots()[_sage_const_0 ][_sage_const_0 ]
        if debug:
            print "found for y_0:", soly

        ss = pol1(q, soly)
        solx = ss.roots()[_sage_const_0 ][_sage_const_0 ]
        if debug:
            print "found for x_0:", solx
    except IndexError:
        return None, None
    return solx, soly



# display stats on helpful vectors
def helpful_vectors(BB, modulus):
    nothelpful = _sage_const_0
    for ii in range(BB.dimensions()[_sage_const_0 ]):
        if BB[ii,ii] >= modulus:
            nothelpful += _sage_const_1

    print nothelpful, "/", BB.dimensions()[_sage_const_0 ], " vectors are not helpful"

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[_sage_const_0 ]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[_sage_const_1 ]):
            a += '0' if BB[ii,jj] == _sage_const_0  else 'X'
            if BB.dimensions()[_sage_const_0 ] < _sage_const_60 :
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print a
