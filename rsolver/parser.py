#encoding: utf-8
from Crypto.PublicKey import RSA
import glob
import binascii
import subprocess
from base64 import b64decode


def firstprivkey(key64):
    result = []
    while True:
        try:
            dec=b64decode(key64)
            break
        except:
            key64=key64+"="

    key_tab = list(dec)
    key_tab=key_tab[key_tab.index(0x2)+1:]
    i=0
    while i < len(key_tab):
        x = key_tab[i]
        if x == 0x2:  # integer start
            # print (i,"!!")
            length = key_tab[i + 1]
            octets = key_tab[i + 2: i + 2 + length]
            value = int.from_bytes(octets, byteorder="big")
            result.append(value)
            #print(value)
            i += 2 + length
        else:
            i += 1
    return (result)

def get_dp_dq_qinv(key64):
    result = []
    key_tab = list(b64decode(key64))
    #print(key_tab)
    i = 0
    while i < len(key_tab):
        x = key_tab[i]
        if x == 0x2:  # integer start
            length = key_tab[i + 1]
            octets = key_tab[i + 2: i + 2 + length]
            value = int.from_bytes(octets, byteorder="big")
            result.append(value)
            #print(value)
            i += 2 + length
        else:
            i += 1
    return (result)


#Parseo partial key
def parsepartialkey(b64,solv):
    if (b64[-1]=="*"):
        res=firstprivkey(b64)
        try:
            solv.addn(res[0])
            solv.adde(res[1])
            solv.addd(res[2])
            solv.addp(res[3])
        except:
            None
        for i in (solv.datas):
            try:
                print (i, hex(solv.datas[i]))
            except:
                None
    elif (b64[0]=="*"):
        res=get_dp_dq_qinv(b64)
        solv.adddp(res[0])
        solv.adddq(res[1])
        solv.addqinv(res[2])
        #print (solv.datas)
    else:
        print ("The string must start or finish with *")
        exit()



#Parsea input de hex/decimales
def parseNum(num):
    #print (num,"..s")
    if num:
        if num[:2]=="0x":
            if num[-1]=="L":
                num=num[:-1]
            num=int(num[2:],16)
    #print (num)
    return int(num)


#Parse File
def parseFile(args,solv):
    file= args["file"].read()
    for line in file.split("\n"):
        line=line.strip()
#        print (line)
        if line!="":
                sp=line.split("=")
                key=sp[0].strip()
                value=parseNum(sp[1].strip())
                if key[0]=="n" or key[0]=="N":
                    solv.addn(value)
                elif key[0]=="e":
                    solv.adde(value)
                elif key[0]=="c":
                    solv.addc(value)
                elif key=="phi":
                    solv.addphi(value)
                elif key[0]=="p":
                    solv.addp(value)
                elif key[0]=="q":
                    solv.addq(value)
                elif key[0:2]=="dp":
                    solv.adddp(value)
                elif key[0]=="d":
                    solv.addd(value)
#Parseo de todo
def parse(args,solv):
    cfile=None
    ns=[]
    cs=None
    es=[]
    e=None


    if args["file"]:
        parseFile(args,solv)
    if args["n"]:
        ns=args["n"].split(",")
        for i in range(len(ns)):
            ns[i]=parseNum(ns[i])
            solv.addn(ns[i])
    if (args["c"]):
        cs=args["c"].split(",")
        for i in range(len(cs)):
            cs[i]=parseNum(cs[i])
            solv.addc(cs[i])

    if (args["c64"]):
        a=args["c64"]
        solv.addc64(a)
        a=(b64decode(a))
        b=""
        for i in a:
            b=b+ (hex(int(i))[2:].zfill(2))
        solv.addc (int(b,16))



    if (args["c64file"]):
        for f in args["c64file"]:
            a= f.read().replace("\n","").strip()
            solv.addc64(a)
            a=(b64decode(a))
            b=""
            for i in a:
                b=b+ (hex(int(i))[2:].zfill(2))
            solv.addc (int(b,16))

    if (args["cryptfile"]):
        for f in args["cryptfile"]:
                a=f.read()
                solv.addc(int(a.hex(),16))



    if args["d"]:
        ds=args["d"].split(",")
        for i in range(len(ds)):
            ds[i]=parseNum(ds[i])
            solv.addd(ds[i])

    if args["e"]:
        es=args["e"].split(",")
        for i in range(len(es)):
            es[i]=parseNum(es[i])
            solv.adde(es[i])

    if args["blind"]:
        solv.blindTrue()

    if args["ucp"]:
        solv.setucp(args["ucp"])

    if (args["pem"]):
        for f in args["pem"]:
                load=f.read()
                pub = RSA.importKey(load)
                solv.addpem(pub)
                solv.adde(pub.e)
                solv.addn(pub.n)
    if args["p"]:
        ps=args["p"].split(",")
        for i in range(len(ps)):
            ps[i]=parseNum(ps[i])
            solv.addp(ps[i])
    if args["q"]:
        ps=args["q"].split(",")
        for i in range(len(ps)):
            ps[i]=parseNum(ps[i])
            solv.addq(ps[i])

    if (args["phi"]):
        phis=args["phi"].split(",")
        for i in range(len(phis)):
            phis[i]=parseNum(phis[i])
            solv.addphi(phis[i])


    if (args["partialkey"]):
        parsepartialkey(args["partialkey"],solv)

    if (args["partialkeyfile"]):
        a=args["partialkeyfile"].read().replace("\n","").replace("-----BEGIN RSA PRIVATE KEY-----","").replace("-----END RSA PRIVATE KEY-----","").strip()
        parsepartialkey(a,solv)


    if (len(es)==len(ns) and len(es)>0):
        for i in range(len(es)):
            solv.addpem(RSA.construct((int(ns[i]),int(es[i]))))
