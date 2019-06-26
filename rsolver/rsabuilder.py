#!/usr/bin/env python
#======================================
#Jeremias Pretto
#Given p, q, e in decimal
#generates RSA private and public keys

import sys
import time
import subprocess
import os
import gmpy
from .asnbuilder import *
from Crypto.Util.number import *
from termcolor import colored

helptext = """
Se creo asn1.conf
openssl asn1parse -genconf asn1.conf  -out key.der
"""


#########################

def build_key(p,q,e):
    print (p,q,e)
    n = p * q
    phi = (p-1) * (q-1)
    d = gmpy.invert(e, phi)
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

def crearPrivateKey(p, q, e,outputfolder,logger):

    # if len(sys.argv) != 4:
    #     sys.stderr.write('Usage: %s p q e\n' % sys.argv[0])
    #     sys.exit(1)

    # p, q, e = [ int(a,10) for a in sys.argv[1:] ]
    p=p[0]
    q=q[0]
    e=e[0]
    print (p,q,e)

    conf = get_asn1conf( build_key(p,q,e) )


    a= open(outputfolder+'/asn1.conf','w').write(conf)

    try:
        # print ('openssl asn1parse -genconf '+outputfolder+'/asn1.conf  -out '+outputfolder + '/privkey.der')

        subprocess.check_output('openssl asn1parse -genconf '+outputfolder+'/asn1.conf  -out '+outputfolder + '/privkey.der', shell=True)
        filename=outputfolder + '/privkey.der'
        print(colored("DER Private key create in {} !".format(filename),"green"))
        logger.info("DER Private key create in {} !".format(filename))
    except:
        subprocess.check_output('rm '+outputfolder+ '/privkey.der', shell=True)

    # try:
    #     subprocess.check_output('openssl rsa -inform DER -in '+ outputfolder + '/privkey.der > '+ outputfolder + '/key.priv', shell=True)
    #     filename=outputfolder + '/key.priv'
    #     print(colored("PEM Private key create in {} !".format(filename),"green"))
    #     logger.info("PEM Private key create in {} !".format(filename))
    # except:
    #     subprocess.check_output('rm '+ outputfolder +'/key.priv', shell=True)


    # try:
    #     subprocess.check_output('openssl rsa -in ' + outputfolder + '/key.priv -pubout > ' + outputfolder + '/key.pub', shell=True)
    #     filename=outputfolder + '/key.pub'
    #     print(colored("PEM Public key create in {}".format(filename),"blue"))
    #     logger.info("PEM public key create in {} !".format(filename))
    #
    # except:
    #     subprocess.check_output('rm ' + outputfolder + '/key.pub', shell=True)


    # print ("\nOutput folder: "+outputfolder+"\n")
    # print ("/asn1.conf:    asn1parse file (for openssl)")
    # print ('/privkey.der:  RSA private key in DER format')
    # print ('/key.priv:     RSA private key in b64')
    # print ('/key.pub:      RSA Public key in b64')



if __name__ == "__main__":
    main()
