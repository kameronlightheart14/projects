# solutions.py
"""Volume 2: One-Dimensional Optimization.
Kameron Lightheart
MATH 323
1/31/19
"""

import numpy as np
import math
from scipy import optimize as opt
from scipy.optimize import linesearch 
from autograd import numpy as anp 
from autograd import grad

# Problem 1
def golden_section(f, a, b, tol=1e-5, maxiter=15):
    """Use the golden section search to minimize the unimodal function f.

    Parameters:
        f (function): A unimodal, scalar-valued function on [a,b].
        a (float): Left bound of the domain.
        b (float): Right bound of the domain.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        (float): The approximate minimizer of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    # Compute initial values
    x0 = (a+b)/2
    p = (1+math.sqrt(5))/2
    n = range(1, maxiter+1)
    # Initialize variables
    iterations = maxiter
    boole = False
    # Compute the next a-hat or a-hat and if within tol, end
    for i in n:
        c = (b-a)/p
        a_hat = b-c
        b_hat = a+c
        if (f(a_hat) <= f(b_hat)):
            b = b_hat
        else:
            a = a_hat
        x1 = (a+b)/2
        if (abs(x0-x1) < tol):
            iterations = i
            boole = True
            break
        x0 = x1
    # Returns approximation, if it finished before maxiters, and iterations
    return x1, boole, iterations

def test_golden_section():
    f = lambda x : np.e**x-4*x
    min, boole, iters = golden_section(f, 0, 3)
    print(boole, min, iters)



# Problem 2
def newton1d(df, d2f, x0, tol=1e-5, maxiter=15):
    """Use Newton's method to minimize a function f:R->R.

    Parameters:
        df (function): The first derivative of f.
        d2f (function): The second derivative of f.
        x0 (float): An initial guess for the minimizer of f.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        (float): The approximate minimizer of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    # Initialize variables
    iterations = maxiter
    boole = False
    n = range(1, maxiter)
    for i in n:
        # Newton's method
        x1 = x0 - df(x0)/d2f(x0)
        # If within tolerance, break out of loop
        if (abs(x1 - x0) < tol):
            iterations = i
            boole = True
            break
        x0 = x1
    # Returns approximation, if it finished before maxiters, and iterations
    return x1, boole, iterations

def test_newton1d():
    df = lambda x : 2*x + 5*np.cos(5*x)
    d2f = lambda x : 2 - 25*np.sin(5*x) 
    sci_apprx = opt.newton(df, x0=0, fprime=d2f, tol=1e-10, maxiter=500)
    apprx = newton1d(df, d2f, 0, maxiter=200)
    print("My Apprx:", apprx)
    print("Scipy Apprx", sci_apprx)


# Problem 3
def secant1d(df, x0, x1, tol=1e-5, maxiter=15):
    """Use the secant method to minimize a function f:R->R.

    Parameters:
        df (function): The first derivative of f.
        x0 (float): An initial guess for the minimizer of f.
        x1 (float): Another guess for the minimizer of f.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        (float): The approximate minimizer of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    # Initialize variables
    boole = False
    iterations = maxiter
    n = range(1, maxiter+1)
    for i in n:
        dfx0 = df(x0)
        dfx1 = df(x1)
        # Compute next using secant formula
        x2 = (x0*dfx1 - x1*dfx0)/(dfx1 - dfx0)
        if (abs(x2 - x1) < tol):
            boole = True
            iterations = i
            break
        x0 = x1
        x1 = x2
    # Returns approximation, if it finished before maxiters, and iterations
    return x2, boole, iterations

def test_secant1d():
    df = lambda x : 2*x + np.cos(x) + 10*np.cos(10*x)
    sci_apprx = opt.newton(df, x0=0, tol=1e-10, maxiter=500)
    my_apprx = secant1d(df, 0, -1, maxiter=1000)
    print("My Apprx:", my_apprx)
    print("Scipy Apprx", sci_apprx)

# Problem 4
def backtracking(f, Df, x, p, alpha=1, rho=.9, c=1e-4):
    """Implement the backtracking line search to find a step size that
    satisfies the Armijo condition.

    Parameters:
        f (function): A function f:R^n->R.
        Df (function): The first derivative (gradient) of f.
        x (float): The current approximation to the minimizer.
        p (float): The current search direction.
        alpha (float): A large initial step length.
        rho (float): Parameter in (0, 1).
        c (float): Parameter in (0, 1).

    Returns:
        alpha (float): Optimal step size.
    """
    # Follow algorithm
    Dfp = Df(x).T@p
    fx = f(x)
    while (f(x+alpha*p) > fx + c*alpha*Dfp):
        # Set new alpha
        alpha = rho*alpha
    # Return step approximation
    return alpha

def test_backtracking():
    f = lambda x: x[0]**2 + x[1]**2 + x[2]**2
    Df = lambda x: np.array([2*x[0], 2*x[1], 2*x[2]])
    f = lambda x: x[0]**2 + x[1]**2 + x[2]**2 
    x = anp.array([150., .03, 40.]) # Current minimizer guesss. 
    p = anp.array([-.5, -100., -4.5]) # Current search direction.  
    phi = lambda alpha: f(x + alpha*p) # Define phi(alpha). 
    dphi = grad(phi) 
    alpha, _ = linesearch.scalar_search_armijo(phi, phi(0.), dphi(0.))
    my_alpha = backtracking(f, Df, x, p)
    print("Their alpha:", alpha)
    print("My alpha:", my_alpha)

