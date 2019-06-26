from Crypto.Util.number import *
from termcolor import colored
def check(solver):
    if (len(solver.datas["n"])==1 and len(solver.datas["e"])==1 and len(solver.datas["c"])==1 and solver.datas["blind"]):
        return True
    return False

def crack(solver):
    s=2
    print ("MODE BLIND RSA ACTIVATED")
    if not solver.datas["ucp"]:
        cp = (pow(s, solver.datas["e"][-1]) * solver.datas["c"][-1]) % solver.datas["n"][-1]
        print ("Please undecrypt (or sign) this: {}\n And after relaunch with -ucp ".format(cp))
        exit()
    else:
        m = solver.datas["ucp"] * 1//s % solver.datas["n"][-1]
        m=long_to_bytes(m).decode("utf8")

        print ("FLAG FOUND!!!")
        filename=solver.outputfolder+"/plaintext_blind"
        out=open(filename,"w")
        out.write(m)
        out.close()
        print(colored('===FLAG FOUND IN {}==='.format(filename), 'green'))
        logger.info("FLAG FOUND from c,d and n:\n{}".format(plaintext))
        logger.info("FLAG save in {}".format(filename))
