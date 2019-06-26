#encoding: utf8
from termcolor import colored
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode
from .rsabuilder import *
import importlib.util
import os
import glob
import sympy
import binascii
import gmpy
import random
import pprint
import signal
import fractions
import pprint
import traceback
import logging

logger = logging.getLogger('Rsolver')
class TimeOutException(Exception):
    def __init__(self, message):
        super(TimeOutException, self).__init__(message)


class Rsolver:
    datas={"n":[], "e":[], "c":[], "phi":[], "dp":[],"dq":[],"qinv":[],"pem":[], "pemfile":[], "p":[],"q":[], "d":[], "chex":[], "cfile":[],"priv":[],"c64":[], "chinese_m":0, "multin_primes":None,"multin_count_of_primes":None, "blind": False, "ucp": None}
    outputfolder=""

    def __init__(self, timeout):
        self.decrypted=False
        self.pubCreated=False
        self.privCreated=False
        self.solvedC=False
        self.solvedF=False
        self.stopInFirstFound=True
        if timeout:
            self.timeout=int(timeout)
        else:
            self.timeout=120
        tiempo="1"
        creo=False
        while not creo:
            try:
                os.mkdir("output_"+str(tiempo).zfill(2))
                tiempo="output_"+str(tiempo).zfill(2)
                creo=True
            except:
                tiempo=int(tiempo)+1


        self.outputfolder=str(tiempo)
        # LOGGER
        script_path = os.path.dirname(os.path.abspath(__file__))
        log_format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        logging.basicConfig(filename=self.outputfolder+'/output.log', level=logging.DEBUG, format=log_format)
        logger.info('Iniciando Rsolver en carpeta {}'.format(self.outputfolder))
        print (colored("OUTPUT FOLDER: " +self.outputfolder,"red")) #Cambiar por colores


    def printflag(self):
        C=self.datas["c"][-1]
        d=self.datas["d"][-1]
        N=self.datas["n"][-1]
        p = pow(C, d, N)
        size = len("{:02x}".format(p)) // 2
        output= ("".join([chr((p >> j) & 0xff) for j in reversed(range(0, size << 3, 8))]))
        #print (output)

        filename=self.outputfolder+"/plaintext_cdn"
        out=open(filename,"wb")
        plaintext=hex(pow(C,d,N))[2:]
        if plaintext == "0":
            return
        # print ("!!!!!!!!!!!!!!!!!! ",plaintext, "...", type(plaintext))
        if len(plaintext) % 2 ==1 :
            plaintext="0"+plaintext
        plaintext=binascii.unhexlify(plaintext)
        print(colored('===FLAG FOUND IN {}==='.format(filename), 'green'))
        logger.info("FLAG FOUND from c,d and n:\n{}".format(plaintext))
        logger.info("FLAG save in {}".format(filename))
        self.solvedC=True
        out.write(plaintext)
        out.close()
        if self.stopInFirstFound:
            exit()


    def inv(self,x, m):
        return sympy.invert(x, m)

    def crt_speedup_decrypt(self,cipher_text, private_key, primes, count_of_primes, n):
        plain_text = 0

        for p, count in zip(primes, count_of_primes):
            m = p ** count
            phi_m = (p ** (count - 1)) * (p - 1)
            c = cipher_text % m
            remainder = pow(c, private_key % phi_m, m)
            M = n // m
            M_inv = self.inv(M, m)
            plain_text = (plain_text + remainder * M * M_inv) % n

        text= hex(plain_text)[2:]
        if len(text)%2==1:
            text="0"+text
        filename=self.outputfolder+"/PLAINTEXTE"
        print(colored('===FLAG FOUND IN {}==='.format(filename), 'green'))
        out=open(filename, "wb")
        text=binascii.unhexlify(text)
        logger.info("FLAG FOUND SAVE IN FILE:\n{}".format(filename))
        out.write(text)




    def pandq(self):
        if (not self.datas["n"]):
            self.addn(self.datas["p"][-1]*self.datas["q"][-1])

        f=(self.datas["p"][-1]-1)*(self.datas["q"][-1]-1)
        if f not in self.datas["phi"]:
            self.addphi(f)

        if (self.datas["c"]):
            aux=0
            for e in self.datas["e"]:
                d = int(gmpy.invert(e, self.datas["phi"][-1]))
                self.addd(int(d))
                filename=self.outputfolder+"/PLAINTEXTB"+str(aux)
                out=open(filename,"wb")
                logger.info("FLAG FOUND save in :\n{}".format(filename))
                print(colored('===FLAG FOUND IN {}==='.format(filename), 'green'), colored("(Somethimes this decrypt file, if do, try with base64 crypt file)","blue"))
                aux=aux+1
                plaintext=hex((pow(self.datas["c"][-1], d, self.datas["n"][-1])))[2:]
                if len(plaintext) % 2 ==1 :
                   plaintext="0"+plaintext
                plaintext=binascii.unhexlify(plaintext)
                out.write(plaintext)
                out.close()
        self.datas["privatekey"]=crearPrivateKey(self.datas["p"],self.datas["q"],self.datas["e"],self.outputfolder,logger)
        if (self.datas["c64"]):
            try:
                plaintext=self.decrypt_withc64(self.datas["c64"][-1])
                filename=self.outputfolder+"/PLAINTEXTA"
                out=open(filename,"wb")
                logger.info("FLAG FOUND save in :\n{}".format(filename))
                print(colored('===FLAG FOUND IN {}==='.format(filename), 'green'))
                out.write(plaintext)
                out.close()
            except Exception as e:
                print (e)


    def flagchinese(self):
        m=self.datas["chinese_m"]
        filename=self.outputfolder+"/PLAINTEXTF"
        out=open(filename,"w")
        plaintext=bytes.fromhex(hex(m)[2:]).decode()
        out.write(plaintext)
        out.close()
        logger.info("FLAG FOUND save in :\n{}".format(filename))
        print(colored('===FLAG FOUND IN {}==='.format(filename), 'green'))
        self.solvedF=True



    def factor_modulus(self,n, d, e):
        """
        Efficiently recover non-trivial factors of n
        See: Handbook of Applied Cryptography
        8.2.2 Security of RSA -> (i) Relation to factoring (p.287)
        http://www.cacr.math.uwaterloo.ca/hac/
        """
        t = (e * d - 1)
        s = 0

        while True:
            quotient, remainder = divmod(t, 2)

            if remainder != 0:
                break

            s += 1
            t = quotient

        found = False

        while not found:
            i = 1
            a = random.randint(1,n-1)

            while i <= s and not found:
                c1 = pow(a, pow(2, i-1, n) * t, n)
                c2 = pow(a, pow(2, i, n) * t, n)

                found = c1 != 1 and c1 != (-1 % n) and c2 == 1

                i += 1

        p = fractions.gcd(c1-1, n)
        q = n // p

        return p, q



    def decrypt_withc64(self,message):

        key = open(self.outputfolder+"/privateKey.pem", "r").read()
        rsakey = RSA.importKey(key)
        rsakey = PKCS1_OAEP.new(rsakey)
        decrypted = rsakey.decrypt(b64decode(message))
        return decrypted

    def canCreatePub(self):
        if not self.pubCreated:
            if (len(self.datas["n"])==1 and len(self.datas["e"]) == 1 and len(self.datas["pem"])==0):
                filename=self.outputfolder+"/publicKey.pem"
                out=open(filename,"w")
                plaintext=RSA.construct((self.datas["n"][-1], self.datas["e"][-1])).publickey().exportKey().decode("utf8")
                out.write(plaintext)
                out.close()
                print(colored('Public Key created in {}'.format(filename), 'blue'))
                logger.info('Public Key created in {}'.format(filename))
                self.pubCreated=True

    def canCreatePriv(self):
        if not self.privCreated:
            if (len(self.datas["n"])>0 and len(self.datas["p"])>0 and len(self.datas["q"])>0 and len(self.datas["e"])>0):
                self.addpriv(self.datas["p"][-1], self.datas["q"][-1],
                             self.datas["e"][-1], self.datas["n"][-1])
                filename=self.outputfolder+"/privateKey.pem"
                out=open(filename,"w")
                out.write(str(self.datas["priv"][-1]))
                out.close()
                print(colored("PEM Private key create in {} !".format(filename),"green"))
                logger.info("PEM Private key create in {} !".format(filename))

    def decrypt(self):
        # if (self.datas["c64"]):
        #     try:
        #         plaintext=self.decrypt_withc64(self.datas["c64"][-1])
        #         filename=self.outputfolder+"/plaintext_64"
        #         out=open(filename,"wb")
        #         logger.info("FLAG FOUND save in :\n{}".format(filename))
        #         print(colored('===FLAG FOUND IN {}==='.format(filename), 'green'))
        #         out.write(plaintext)
        #         out.close()
        #         self.decrypted=True
        #         print (self.datas)
        #     except Exception as e:
        #         print (e)

        if not self.decrypted:
            g=self.datas["priv"][-1].decrypt(self.datas["chex"][-1])
            filename=self.outputfolder+"/plaintext"
            out=open(filename,"wb")
            out.write(g)
            out.close()
            print(colored("FLAG FOUND IN {} !".format(filename),"green"))
            logger.info("FLAG FOUND IN {} !".format(filename))

            try:
                g=self.datas["priv"][-1].decryptOAEP(self.datas["chex"][-1])
                filename=self.outputfolder+"/plaintext_oaep"
                out=open(filename,"wb")
                out.write(g)
                out.close()
                self.decrypted=True
                print(colored("Experimental FLAG FOUND (maybe false positive) IN {} !".format(filename),"green"))
                logger.info("Experimental FLAG FOUND (maybe false positive) IN {} !".format(filename))
            except:
                None

            self.decrypted=True
            if (self.stopInFirstFound):
                exit()
            # exit()



    def halfn(self):
        if(len(self.datas["p"])>0 and len(self.datas["q"])>0 and len(self.datas["e"])>0):
            if (not self.datas["n"]):
                self.addn(self.datas["p"][-1]*self.datas["q"][-1])
        if (len(self.datas["p"])>0 and len(self.datas["n"])>0 and len(self.datas["e"])>0 and len(self.datas["q"])==0):
            self.addq(self.datas["n"][0]//self.datas["p"][0])
        elif (len(self.datas["q"])>0 and len(self.datas["n"])>0 and len(self.datas["e"])>0 and len(self.datas["p"])==0):
            self.addp(self.datas["n"][0]//self.datas["q"][0])

    #Después de cada script ejecutado, chequea si se puede resolver
    def iscracked(self):
        #print (self.datas)
        #if p y q -> add N
        self.halfn()
        self.canCreatePub()
        self.canCreatePriv()
        if self.privCreated and len(self.datas["chex"])>0:
            self.decrypt()
        elif (self.datas["c"] and self.datas["d"] and self.datas["n"]):
            if not self.solvedC:
                self.printflag()
                return True

        if self.datas["multin_primes"] and self.datas["multin_count_of_primes"]:
            self.crt_speedup_decrypt(self.datas["c"][-1], self.datas["d"][-1], self.datas["multin_primes"], self.datas["multin_count_of_primes"], self.datas["n"][-1])
        else:
            if self.datas["chinese_m"]!=0:
                if not self.solvedF:
                    self.flagchinese()



            elif (len(self.datas["n"])>0 and len(self.datas["d"])>0 and len(self.datas["e"])>0 and len(self.datas["p"])==0):
               p,q=self.factor_modulus(self.datas["n"][-1], self.datas["d"][-1], self.datas["e"][-1])
               self.addp(p)
               self.addq(q)



    def finish(self):
        self.writeFindings()
        if not self.solvedC:
            print(colored("Note: If the script doesnt work, try with --timeout 0 or read the logs in {}".format(self.outputfolder+"/output.log"), 'blue'))
        exit()






    def handler(self,signum, frame):
       #print ("Timeout")
       raise TimeOutException("Timeoutddd")

    def crack(self):
        self.writeQuery()
        import rsolver
        path = os.path.dirname(rsolver.__file__)
        print(path+"/scripts/*")
        scripts= (glob.glob(path + '/scripts/[!_]*'))
        self.iscracked()
        for script in scripts:
            try:
                spec = importlib.util.spec_from_file_location("module.name", script)
                sc = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(sc)
                #print (script,sc.check(self.datas))
                logger.debug ("Checking condition for script {}".format(script))
                if sc.check(self):
                    logger.info("TRYING script:"+ script)
                    signal.signal(signal.SIGALRM, self.handler)
                    signal.alarm(self.timeout)
                    sc.crack(self)
                    signal.alarm(0)
                else:
                    logger.debug ("script {} does not meet the conditions".format(script))
            except TimeOutException:
                logger.error ("Timeout for script:" + script)
            except Exception as e:
                logging.error("script {} get the exception: \n{}".format(script,str(e)), exc_info=True)
            self.iscracked()

#            print (self.datas)

        self.finish()

    def writeQuery(self):
        logger.info("The variables received from inputs are:\n\n"+pprint.pformat(self.datas) +"\n\n")



    def writeFindings(self):
        logger.info("After execution the variables are:\n\n"+pprint.pformat(self.datas) +"\n\n\n")


#        print (pprint.pprint(self.datas))

    def adddp(self, dp):
        logger.info("dp FOUND!: {}".format(dp))
        self.datas["dp"].append(dp)
    def adddq(self, dq):
        logger.info("dq FOUND!: {}".format(dq))
        self.datas["dq"].append(dq)

    def addqinv(self, qinv):
        logger.info("qinv FOUND!: {}".format(qinv))
        self.datas["qinv"].append(qinv)

    def addd(self, d):
        if d not in self.datas["d"]:
            logger.info("d FOUND!: {}".format (d))
            self.datas["d"].append(d)

    def addn(self, n):
        logger.info("n FOUND!: {}".format(n))
        self.datas["n"].append(n)

    def addc(self, c):
        logger.info("c FOUND {}".format(c))
        self.datas["c"].append(c)
        d=hex(c)[2:]
        if len(d)%2==0:
            d=binascii.unhexlify(d)
        else:
            d=binascii.unhexlify("0"+d)
        self.addchex(d)

    def addchex(self, chex):
        self.datas["chex"].append(chex)
        # print (self.datas)

    def addp(self, p):
        logger.info("p FOUND!: {}".format(p))
        self.datas["p"].append(p)

    def addq(self, q):
        logger.info("q FOUND!: {}".format(q))
        self.datas["q"].append(q)

    def adde(self, e):
        logger.info("e FOUND!: {}".format(e))
        self.datas["e"].append(e)

    def addphi(self, phi):
        logger.info("phi FOUND!: {}".format(phi))
        self.datas["phi"].append(phi)

    def addpem(self, pem):
        self.datas["pem"].append(pem)

    def addpriv(self, p,q,e,n):
        self.privCreated=True
        self.datas["priv"].append(PrivateKey(p,q,e,n))

    def addc64(self, c64):
        self.datas["c64"].append(c64)

    def adducp(self, ucp):
        self.datas["ucp"] = ucp

    def blindTrue(self):
        self.datas["blind"]=True

    def setucp(self, ucp):
        self.datas["ucp"] = int(ucp)


    def start(self):
        pass
#        print (self.datas)



class PrivateKey(object):
    def __init__(self, p, q, e, n):
        """Create private key from base components
           :param p: extracted from n
           :param q: extracted from n
           :param e: exponent
           :param n: n from public key
        """
        t = (p-1)*(q-1)
        d = modinv(e,t)
        self.key = RSA.construct((n, e, d, p, q))

    def decrypt(self, cipher):
        """Uncipher data with private key
           :param cipher: input cipher
           :type cipher: string
        """
        return self.key.decrypt(cipher)


    def decryptOAEP(self,cipher):
        rsakey = PKCS1_OAEP.new(self.key)
        decrypted = rsakey.decrypt(cipher)
        return decrypted

    def __str__(self):
        # Print armored private key
        return self.key.exportKey().decode("utf8")