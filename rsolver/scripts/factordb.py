import requests
import re
def check(solver):
	if (solver.datas["n"] and len(solver.datas["e"])==1):
	 	return True

def solveforp(equation):
    try:
        if '^' in equation: k,j = equation.split('^')
        if '-' in j: j,sub = j.split('-')
        eq = map(int, [k,j,sub])
        return pow(eq[0],eq[1])-eq[2]
    except Exception as e:
        print ("[*] FactorDB gave something we couldn't parse sorry (%s). Got error: %s" % (equation,e))
        raise FactorizationError()


def crack(solver):
    url_1 = 'http://www.factordb.com/index.php?query=%i'
    url_2 = 'http://www.factordb.com/index.php?id=%s'
    s = requests.Session()
    r = s.get(url_1 % solver.datas["n"][0])
    regex = re.compile("index\.php\?id\=([0-9]+)", re.IGNORECASE)
    ids = regex.findall(r.text)
    p_id = ids[1]
    q_id = ids[2]
    # bugfix: See https://github.com/sourcekris/RsaCtfTool/commit/16d4bb258ebb4579aba2bfc185b3f717d2d91330#commitcomment-21878835
    regex = re.compile("value=\"([0-9\^\-]+)\"", re.IGNORECASE)
    r_1 = s.get(url_2 % p_id)
    r_2 = s.get(url_2 % q_id)
    key_p = regex.findall(r_1.text)[0]
    key_q = regex.findall(r_2.text)[0]

    p = int(key_p) if key_p.isdigit() else solveforp(key_p)
    q = int(key_q) if key_q.isdigit() else solveforp(key_q)
    if p == q == solver.datas["n"][-1]:
        raise Exception("Not Found in FactorDB")
    solver.addp(p)
    solver.addq(q)
