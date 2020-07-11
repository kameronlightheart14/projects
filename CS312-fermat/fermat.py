import random
import numpy as np


def prime_test(N, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N):
    # You will need to implement this function and change the return value.   
    if y == 0:
        return 1
    z = modexp(x, np.floor(y / 2), N)
    if y % 2 == 0:
        return z**2 % N
    else:
        return x * z**2 % N
    

def fprobability(k):
    # You will need to implement this function and change the return value.   
    return 1 - 2**(-k)


def mprobability(k):
    # You will need to implement this function and change the return value.   
    return 1 - 4**(-k)


def run_fermat(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    a_array = np.random.randint(0, k, N)
    a_array = a_array**(N-1)
    
    if np.array_equal(a_array % N, np.ones_like(a_array)):
        return 'prime'

    return 'composite'


def run_miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    if N % 2 == 0:
        return 'composite'
    n = N - 1
    r = 0
    while n % 2 == 0:
        n = n/2
        r += 1
    d = int(n)

    for _ in range(k):
        a = random.randint(0, N)
        x = pow(a, d, N)
        if x == 1 or x == N - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, N)
            if x == N - 1:
                break
        else:
            return 'composite'

    return 'prime'
