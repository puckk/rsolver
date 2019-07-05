#multiprime extract factors with yafu and not e setted
import rsolver
import subprocess
import gmpy2
import binascii
import os

def check(solver):
    if (len(solver.datas["n"])>0):
        if ((len(str(solver.datas["n"][-1]))) < 400):
            return True
def crack(solver):
    path = os.path.dirname(rsolver.__file__)
    a=path + '/scripts/yafu "factor({})"'.format(str(solver.datas["n"][-1]))
    #print (a)
    b= (subprocess.check_output(a,shell=True).decode("utf8"))
    b= (b[b.index("***factors found***"):])
    multiprimefactors=[]
    for i in b.split("\n"):
        if "P" in i and "=" in i:
            multiprimefactors.append(int(i.split(" ")[2]))
    solver.datas["multiprimefactors"]=multiprimefactors
    t = 1

    for line in multiprimefactors:
        temp=line-1
        t*=temp
    if (len(solver.datas["e"])==0):
        e=65537
        solver.adde(e)
    solver.addd(int(gmpy2.invert(solver.datas["e"][-1],t)))
