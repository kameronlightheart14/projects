# interior_point_quadratic.py
"""Volume 2: Interior Point for Quadratic Programs.
Kameron Lightheart
MATH 323
3/28/19
"""

import numpy as np
from scipy import linalg as la
from scipy.sparse import spdiags
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from cvxopt import matrix, solvers

def startingPoint(G, c, A, b, guess):
    """
    Obtain an appropriate initial point for solving the QP
    .5 x^T Gx + x^T c s.t. Ax >= b.
    Parameters:
        G -- symmetric positive semidefinite matrix shape (n,n)
        c -- array of length n
        A -- constraint matrix shape (m,n)
        b -- array of length m
        guess -- a tuple of arrays (x, y, mu) of lengths n, m, and m, resp.
    Returns:
        a tuple of arrays (x0, y0, l0) of lengths n, m, and m, resp.
    """
    m,n = A.shape
    x0, y0, l0 = guess

    # Initialize linear system
    N = np.zeros((n+m+m, n+m+m))
    N[:n,:n] = G
    N[:n, n+m:] = -A.T
    N[n:n+m, :n] = A
    N[n:n+m, n:n+m] = -np.eye(m)
    N[n+m:, n:n+m] = np.diag(l0)
    N[n+m:, n+m:] = np.diag(y0)
    rhs = np.empty(n+m+m)
    rhs[:n] = -(G.dot(x0) - A.T.dot(l0)+c)
    rhs[n:n+m] = -(A.dot(x0) - y0 - b)
    rhs[n+m:] = -(y0*l0)

    sol = la.solve(N, rhs)
    dx = sol[:n]
    dy = sol[n:n+m]
    dl = sol[n+m:]

    y0 = np.maximum(1, np.abs(y0 + dy))
    l0 = np.maximum(1, np.abs(l0+dl))

    return x0, y0, l0


# Problems 1-2
def qInteriorPoint(Q, c, A, b, guess, niter=20, tol=1e-16, verbose=False):
    """Solve the Quadratic program min .5 x^T Q x +  c^T x, Ax >= b
    using an Interior Point method.

    Parameters:
        Q ((n,n) ndarray): Positive semidefinite objective matrix.
        c ((n, ) ndarray): linear objective vector.
        A ((m,n) ndarray): Inequality constraint matrix.
        b ((m, ) ndarray): Inequality constraint vector.
        guess (3-tuple of arrays of lengths n, m, and m): Initial guesses for
            the solution x and lagrange multipliers y and eta, respectively.
        niter (int > 0): The maximum number of iterations to execute.
        tol (float > 0): The convergence tolerance.

    Returns:
        x ((n, ) ndarray): The optimal point.
        val (float): The minimum value of the objective function.
    """
    def make_F(x, y, mew):
        """ 
        Paramters:
            x ((n, ) ndarray)
            lamb ((n, ) ndarray)
            mew ((m, ) ndarray)
        """
        top = Q @ x - A.T @ mew + c
        mid = A @ x - y - b
        bottom = np.diag(y) @ (np.diag(mew) @ np.ones_like(y))
        return np.hstack((top, mid, bottom))
    def get_DF(x, y, mew):
        """ 
        Paramters:
            x ((n, ) ndarray)
            y ((m, ) ndarray)
            mew ((m, ) ndarray)
        """
        # Create empty shell for DF
        m,n = A.shape
        DF = np.zeros((n+2*m,n+2*m))
        I = np.eye(m)
        Y = np.diag(y)
        M = np.diag(mew)
        # Start to populate DF
        DF[0:n,0:n] = Q
        DF[0:n,n+m:] = -A.T
        DF[n:n+m,0:n] = A
        DF[n:n+m,n:n+m] = -I
        DF[n+m:,n:n+m] = M
        DF[n+m:, n+m:] = Y
        return DF
    def compute_search_direction(x, y, mew, sigma=0.1):
        """ 
        Paramters:
            x ((n, ) ndarray)
            y ((m, ) ndarray)
            mew ((m, ) ndarray)
        """
        m, n = A.shape
        # Get F and DF 
        F = make_F(x,y,mew)
        DF = get_DF(x,y,mew)
        # Get LU decomposition
        L, piv = la.lu_factor(DF)
        
        # Construct b vector
        vec = np.zeros_like(F)
        vec[n+m:] = sigma * (y @ mew / m) * np.ones_like(y)
        b = -F + vec

        # Solve using LU_Solve from scipy.linalg.lu_solve()
        sol = la.lu_solve((L, piv), b)
        return sol

    def compute_step_size(direction, x, y, mew):
        """ 
        Paramters:
            direction ((n+m+m, ) ndarray): step direction vector
            x ((n, ) ndarray)
            y ((m, ) ndarray)
            mew ((m, ) ndarray)
        """
        m,n = A.shape
        delta_mew = direction[-m:]
        delta_y = direction[n:n+m]

        # Calculate alpha_max and delta_max
        beta_max = min(1, min(-mew[delta_mew < 0] / delta_mew[delta_mew < 0]))
        delta_max = min(1, min(-y[delta_y < 0] / delta_y[delta_y < 0]))

        # Back off final step lengths
        if (np.alltrue(delta_mew > 0)):
            beta_max = min(1, 0.95*1)
            delta_max = min(1, 0.95*1)
        beta = min(1, 0.95 * beta_max)
        delta = min(1, 0.95 * delta_max)
        alpha = min(beta, delta)

        return alpha

    # Get starting values
    m,n = A.shape
    x0, y0, mew0 = startingPoint(Q, c, A, b, guess)

    for i in range(niter):
        # Get step direction vector [delta_x, delta_lamb, delta_mew]
        direction = compute_search_direction(x0, y0, mew0)
        # Parse out the delta's
        delta_mew = direction[-m:]
        delta_y = direction[n:n+m]
        delta_x = direction[:n]

        # Compute the next step size
        alpha = compute_step_size(direction, x0, y0, mew0)

        # Update variables
        x0 = x0 + alpha * delta_x
        y0 = y0 + alpha * delta_y
        mew0 = mew0 + alpha * delta_mew

        # Compute nu and check if less than tol, if so exit iteration
        nu = (y0 @ mew0) / m
        if (abs(nu) < tol):
            break

    return x0, 0.5 * x0 @ (Q @ x0) + c @ x0 # Minimizer, optimal value

def test_qInteriorPoint():
    Q = np.array([[1, -1], [-1, 2]])
    c = np.array([-2, -6])
    A = np.array([[-1,-1], [1,-2], [-2,-1], [1,0], [0,1]])
    b = np.array([-2,-2,-3,0,0])
    guess = np.array([0.5,0.5])
    m,n = A.shape
    guess_vec = (guess, np.ones(m), np.ones(m))
    print(qInteriorPoint(Q,c,A,b,guess_vec))


def laplacian(n):
    """Construct the discrete Dirichlet energy matrix H for an n x n grid."""
    data = -1*np.ones((5, n**2))
    data[2,:] = 4
    data[1, n-1::n] = 0
    data[3, ::n] = 0
    diags = np.array([-n, -1, 0, 1, n])
    return spdiags(data, diags, n**2, n**2).toarray()


# Problem 3
def circus(n=15):
    """Solve the circus tent problem for grid size length 'n'.
    Display the resulting figure.
    """
    # Create the tent pole configuration.
    L = np.zeros((n,n)) 
    L[n//2-1:n//2+1,n//2-1:n//2+1] = .5 
    m = [n//6-1, n//6, int(5*(n/6.))-1, int(5*(n/6.))] 
    mask1, mask2 = np.meshgrid(m, m) 
    L[mask1, mask2] = .3 
    L = L.ravel()
    # Set initial guesses. 
    x = np.ones((n,n)).ravel() 
    y = np.ones(n**2) 
    mu = np.ones(n**2)
    
    # Use laplacian function to construct H
    H = laplacian(n)

    # Construct A
    A = np.eye(n*n)

    # Construct c
    c = np.full(n*n, -(n-1)**(-2))
    
    # Calculate the solution. 
    z = qInteriorPoint(H, c, A, L, (x,y,mu))[0].reshape((n,n))

    print(z)

    # Plot the solution. 
    domain = np.arange(n)
    X, Y = np.meshgrid(domain, domain)
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d') 
    ax1.plot_surface(X, Y, z, rstride=1, cstride=1, color='r') 
    plt.xlabel("x axis (ft)")
    plt.ylabel("y axis(ft)")
    plt.title("Tent Optimization")
    plt.show()

# Problem 4
def portfolio(filename="portfolio.txt"):
    """Markowitz Portfolio Optimization

    Parameters:
        filename (str): The name of the portfolio data file.

    Returns:
        (ndarray) The optimal portfolio with short selling.
        (ndarray) The optimal portfolio without short selling.
    """
    # Load the data
    data = np.loadtxt(filename)

    # Compute the covariance matrix   
    Q = matrix(np.cov(data[:,1:].T))
    n = 8

    # Compute mew, averages of data vectors
    mew = np.average(data[:,1:], axis=0)
    #print(mew)
    R = 1.13

    # Set up the constraints
    A = matrix(np.vstack((np.ones(n), mew)))
    G = matrix(-np.eye(n))
    h = matrix(np.zeros(n))
    c = matrix(np.zeros(n))
    b = matrix(np.array([1, R]))
    noselling_solver = solvers.qp(Q, c, A=A, b=b, G=G, h=h)
    noselling_sol = np.ravel(noselling_solver['x'])
    shortselling_solver = solvers.qp(Q, c, A=A, b=b)
    shortselling_sol = np.ravel(shortselling_solver['x'])
    return shortselling_sol, noselling_sol
