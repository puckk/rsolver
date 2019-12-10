def rwh_primes1(n):
    # https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Returns  a list of primes < n """
    sieve = [True] * (n//2)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
            return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]

def check(solver):
    if (len(solver.datas["n"])>0):
        return True
    return False

def crack (solver):
    n=solver.datas["n"][-1]
    for prime in (rwh_primes1(57970028)):			      
        if n % prime == 0:
            p=prime
            q=n//prime
            solver.addq(q)
            solver.addp(p)
            return True

    #Ahora se queda con el último, podría quedarse con todos y bruteforcear las keys y desencripts
