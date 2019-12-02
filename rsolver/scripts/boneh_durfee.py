import subprocess
import rsolver
import os

def check(solver):
    return len(solver.datas["n"]) == 1 and len(solver.datas["e"])== 1
# para Rsolver
def crack(solver):
    path = os.path.dirname(rsolver.__file__)
    n = solver.datas["n"][-1]
    e = solver.datas["e"][-1]
    python3_command = path + "/scripts/boneh_durfee {} {}".format(str(n),str(e))
    process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode()
    if "DFOUND:" in (output):
        d = int(output[output.index("DFOUND:")+8:output.index("#")-1])
        solver.addd(d)
        solver.addpriv_d(n, e, d)
