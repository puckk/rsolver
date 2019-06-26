#Robado de http://heartsky.info/2017/08/29/HackCon-2017-RSA-3-writeup/
from Crypto.Util.number import bytes_to_long, long_to_bytes
import gmpy2
import string

def check(solver):
    if (len(solver.datas["c"])> 1 and len(solver.datas["n"])> 1 and len(solver.datas["e"])==0):
        return True

def crack(solver):
    n=solver.datas["n"]
    c=solver.datas["c"]
    le=len(n)
    # calc N
    N = 1
    for num in n:
        N *= num

    # N1,N2...Nn
    # NN1 * t1 = 1 (mod n1)
    NN = [None] * le
    t =  [None] * le
    x = 0
    for i in range(le):
        NN[i] = int(N / n[i])
        t[i] = gmpy2.invert(NN[i],n[i])
        x += c[i]*t[i]*NN[i]

    res = x % N
    for i in range(2, 65535):
        num = 0
        try:
            flag = long_to_bytes(gmpy2.iroot(res,i)[0])
            for j in flag:
                if j not in string.printable:
                    num = 1
                    break
            if num == 0:
                print ('e is ' + str(i))
                print (flag)
        except:
            continue
