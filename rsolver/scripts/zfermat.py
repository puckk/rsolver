import gmpy


def check(solver):
    if (len(solver.datas["n"])>0):
        return True
    return False

def crack(solver):
        a = gmpy.sqrt(solver.datas["n"][-1])
        max = a + 999999999
        while a < max:
            b2 = a*a - solver.datas["n"][-1]
            if b2 >= 0:
                b = gmpy.sqrt(b2)
                if b*b == b2:
                    break
            a += 1
        if a < max:
            solver.addq(int(a-b))
            solver.addp(int(a+b))
            return True
        else:
            return False
