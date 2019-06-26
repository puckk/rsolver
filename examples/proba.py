from Crypto.Util.number import bytes_to_long, long_to_bytes
import gmpy2
import string

# get all n and c
s = open('14.test').read().split('\n')
num = 0
n = []
c = []
for i in range(len(s)):
    if num % 3 == 0:
        n.append(int(s[i].split(' ')[2]))
    elif num % 3 == 1:
        c.append(int(s[i].split(' ')[2]))
    num += 1
le = len(n)

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
    NN[i] = N / n[i]
    t[i] = gmpy2.invert(NN[i],n[i])
    x += c[i]*t[i]*NN[i]

res = x % N
for i in range(2, 65537):
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
