#!/usr/bin/env python
import sys

helptext = """
Redirect output to asn1.conf and then create and check the key with:
openssl asn1parse -genconf asn1.conf  -out key.der
openssl rsa -in key.der -inform der -text -check
https://gist.github.com/gnpar/89224485386acf83ec01daf7503b2c3b
"""

#### Extended Euclidean Algorithm and Modular Inverse
#### Copied from wikibooks:
#### https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
       q, r = b//a, b%a
       m, n = x-u*q, y-v*q
       b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
       return None  # modular inverse does not exist
    else:
       return x % m
#########################

def build_key(p,q,e):
    n = p * q
    phi = (p-1) * (q-1)
    d = modinv(e, phi)

    e1 = d % (p-1)
    e2 = d % (q-1)
    c = modinv(q,p)

    return (n,e,d,p,q,e1,e2,c)

def get_asn1conf(key):
# Sample config from openssl.org's ASN1_generate_nconf
    return """
asn1=SEQUENCE:private_key

[private_key]
version=INTEGER:0
n=INTEGER:%s
e=INTEGER:%s
d=INTEGER:%s
p=INTEGER:%s
q=INTEGER:%s
exp1=INTEGER:%s
exp2=INTEGER:%s
coeff=INTEGER:%s
""" % key

def main():
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: %s p q e\n' % sys.argv[0])
        sys.exit(1)

    p, q, e = [ int(a,16) for a in sys.argv[1:] ]

    conf = get_asn1conf( build_key(p,q,e) )

    sys.stderr.write(helptext)
    #print conf

if __name__ == "__main__":
    main()
