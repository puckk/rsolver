from factordb.factordb import FactorDB


def check(solver):
	if (len(solver.datas["n"]) > 0 and len(solver.datas["e"]) == 1):
			return True


def crack(solver):
	a = FactorDB(solver.datas["n"][-1])
	a.connect()
	b = a.get_factor_list()
	if (len(b) == 2):
		solver.addp(b[0])
		solver.addq(b[1])
