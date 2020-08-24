# interior_point_linear.py
"""Volume 2: Interior Point for Linear Programs.
Kameron Lightheart
MATH 323
3/21/19
"""

import numpy as np
from scipy import linalg as la
from scipy.stats import linregress
from matplotlib import pyplot as plt

# Auxiliary Functions ---------------------------------------------------------
def startingPoint(A, b, c):
    """Calculate an initial guess to the solution of the linear program
    min c^T x, Ax = b, x>=0.
    Reference: Nocedal and Wright, p. 410.
    """
    # Calculate x, lam, mu of minimal norm satisfying both
    # the primal and dual constraints.
    B = la.inv(A @ A.T)
    x = A.T @ B @ b
    lam = B @ A @ c
    mu = c - (A.T @ lam)

    # Perturb x and s so they are nonnegative.
    dx = max((-3./2)*x.min(), 0)
    dmu = max((-3./2)*mu.min(), 0)
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    # Perturb x and mu so they are not too small and not too dissimilar.
    dx = .5*(x*mu).sum()/mu.sum()
    dmu = .5*(x*mu).sum()/x.sum()
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    return x, lam, mu

# Use this linear program generator to test your interior point method.
def randomLP(m):
    """Generate a 'square' linear program min c^T x s.t. Ax = b, x>=0.
    First generate m feasible constraints, then add slack variables.
    Parameters:
        m -- positive integer: the number of desired constraints
             and the dimension of space in which to optimize.
    Returns:
        A -- array of shape (m,n).
        b -- array of shape (m,).
        c -- array of shape (n,).
        x -- the solution to the LP.
    """
    n = m
    A = np.random.random((m,n))*20 - 10
    A[A[:,-1]<0] *= -1
    x = np.random.random(n)*10
    b = A.dot(x)
    c = A.sum(axis=0)/float(n)
    return A, b, -c, x

# This random linear program generator is more general than the first.
def randomLP2(m,n):
    """Generate a linear program min c^T x s.t. Ax = b, x>=0.
    First generate m feasible constraints, then add
    slack variables to convert it into the above form.
    Parameters:
        m -- positive integer >= n, number of desired constraints
        n -- dimension of space in which to optimize
    Returns:
        A -- array of shape (m,n+m)
        b -- array of shape (m,)
        c -- array of shape (n+m,), with m trailing 0s
        v -- the solution to the LP
    """
    A = np.random.random((m,n))*20 - 10
    A[A[:,-1]<0] *= -1
    v = np.random.random(n)*10
    k = n
    b = np.zeros(m)
    b[:k] = A[:k,:].dot(v)
    b[k:] = A[k:,:].dot(v) + np.random.random(m-k)*10
    c = np.zeros(n+m)
    c[:n] = A[:k,:].sum(axis=0)/k
    A = np.hstack((A, np.eye(m)))
    return A, b, -c, v


# Problems --------------------------------------------------------------------
def interiorPoint(A, b, c, niter=20, tol=1e-16, verbose=False):
    """Solve the linear program min c^T x, Ax = b, x>=0
    using an Interior Point method.

    Parameters:
        A ((m,n) ndarray): Equality constraint matrix with full row rank.
        b ((m, ) ndarray): Equality constraint vector.
        c ((n, ) ndarray): Linear objective function coefficients.
        niter (int > 0): The maximum number of iterations to execute.
        tol (float > 0): The convergence tolerance.

    Returns:
        x ((n, ) ndarray): The optimal point.
        val (float): The minimum value of the objective function.
    """
    # Define fuction to make a function F and return it
    def make_F(x, lamb, mew):
        """ 
        Paramters:
            x ((n, ) ndarray)
            lamb ((n, ) ndarray)
            mew ((m, ) ndarray)
        """
        top = A.T @ lamb + mew - c
        mid = A @ x - b
        bottom = np.diag(mew) @ x
        return np.hstack((top, mid, bottom))
    def get_DF(x, lamb, mew):
        """ 
        Paramters:
            x ((n, ) ndarray)
            lamb ((n, ) ndarray)
            mew ((m, ) ndarray)
        """
        # Create empty shell for DF
        m,n = A.shape
        DF = np.zeros((2*n+m,2*n+m))
        I = np.eye(n)
        X = np.diag(x)
        M = np.diag(mew)
        # Start to populate DF
        DF[0:n,n:n+m] = A.T
        DF[:n,n+m:] = I
        DF[n:n+m,0:n] = A
        DF[n+m:,:n] = M
        DF[n+m:, n+m:] = X
        return DF
    def compute_search_direction(x, lamb, mew, sigma=0.1):
        """ 
        Paramters:
            x ((n, ) ndarray)
            lamb ((n, ) ndarray)
            mew ((m, ) ndarray)
        """
        m, n = A.shape
        # Get F and DF 
        F = make_F(x,lamb,mew)
        DF = get_DF(x,lamb,mew)
        # Get LU decomposition
        L, piv = la.lu_factor(DF)
        
        # Construct b vector
        vec = np.zeros_like(F)
        vec[n+m:] = sigma * (x @ mew / n)
        b = -F + vec

        # Solve using LU_Solve from scipy.linalg.lu_solve()
        sol = la.lu_solve((L, piv), b)
        return sol

    def compute_step_size(direction, x, lambd, mew):
        """ 
        Paramters:
            direction ((n+m+n, ) ndarray): step direction vector
            x ((n, ) ndarray)
            lamb ((n, ) ndarray)
        """
        m,n = A.shape
        delta_mew = direction[-n:]
        delta_x = direction[:n]

        # Calculate alpha_max and delta_max
        alpha_max = min(1, min(-mew[delta_mew < 0] / delta_mew[delta_mew < 0]))
        delta_max = min(1, min(-x[delta_x < 0] / delta_x[delta_x < 0]))

        # Back off final step lengths
        alpha = min(1, 0.95 * alpha_max)
        delta = min(1, 0.95 * delta_max)

        return alpha, delta

    # Get starting values
    x0, lamb0, mew0 = startingPoint(A, b, c)

    for i in range(niter):
        m, n = A.shape

        # Get step direction vector [delta_x, delta_lamb, delta_mew]
        direction = compute_search_direction(x0, lamb0, mew0)
        # Parse out the delta's
        delta_mew = direction[-n:]
        delta_lamd = direction[n:n+m]
        delta_x = direction[:n]

        # Compute the next step size
        alpha, delta = compute_step_size(direction, x0, lamb0, mew0)

        # Update variables
        x0 = x0 + delta * delta_x
        lamb0 = lamb0 + alpha * delta_lamd
        mew0 = mew0 + alpha * delta_mew

        # Compute nu and check if less than tol, if so exit iteration
        nu = (x0 @ mew0) / n
        if (abs(nu) < tol):
            break

    return x0, c @ x0 # Minimizer, optimal value

def test_prob4():
    m,n = 7, 5
    A,b,c,x = randomLP2(m, n)
    point, value = interiorPoint(A, b, c)
    print(np.allclose(x, point[:n]))

def test_F():
    b = np.ones(4)
    c = 2*np.ones(3)
    A = np.random.random((4,3))
    interiorPoint(A, b, c)
    

def leastAbsoluteDeviations(filename='simdata.txt'):
    """Generate and show the plot requested in the lab."""
    data = np.loadtxt(filename)
    m = data.shape[0]
    n = data.shape[1] - 1
    c = np.zeros(3*m + 2*(n + 1))
    c[:m] = 1
    y = np.empty(2*m)
    y[::2] = -data[:, 0]
    y[1::2] = data[:, 0]
    x = data[:, 1:]
    A = np.ones((2*m, 3*m + 2*(n + 1)))
    A[::2, :m] = np.eye(m)
    A[1::2, :m] = np.eye(m)
    A[::2, m:m+n] = -x
    A[1::2, m:m+n] = x
    A[::2, m+n:m+2*n] = x
    A[1::2, m+n:m+2*n] = -x
    A[::2, m+2*n] = -1
    A[1::2, m+2*n+1] = -1
    A[:, m+2*n+2:] = -np.eye(2*m, 2*m)
    sol = interiorPoint(A, y, c, niter=10)[0]
    beta = sol[m:m+n] - sol[m+n:m+2*n]
    b = sol[m+2*n] - sol[m+2*n+1]
    
    # Do linear regression and plot the result
    slope, intercept = linregress(data[:,1], data[:,0])[:2]
    domain = np.linspace(0,10,200)
    plt.plot(domain, domain*slope + intercept, label = "Least Squares Approximation")
    plt.scatter(data[:,1],data[:,0],s = 4,c = "black")
    plt.plot(domain,beta*domain+b, label = "LAD approximation")
    plt.title("SimData Line Fit Regressions")
    plt.legend()
    plt.show()
