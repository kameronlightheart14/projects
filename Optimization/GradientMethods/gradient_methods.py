# solutions.py
"""Volume 2: Gradient Descent Methods.
Kameron Lightheart
Math 323
2/21/19
"""

import numpy as np
from scipy import optimize as opt
from autograd import grad
from scipy import linalg as la
from autograd import numpy as anp
from matplotlib import pyplot as plt

# Problem 1
def steepest_descent(f, Df, x0, tol=1e-5, maxiter=100):
    """Compute the minimizer of f using the exact method of steepest descent.

    Parameters:
        f (function): The objective function. Accepts a NumPy array of shape
            (n,) and returns a float.
        Df (function): The first derivative of f. Accepts and returns a NumPy
            array of shape (n,).
        x0 ((n,) ndarray): The initial guess.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        ((n,) ndarray): The approximate minimum of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    iters = 0
    converged = False
    for i in range(maxiter):
        iters += 1
        # Minimize alpha
        f_alpha = lambda alpha : f(x0 - alpha*Df(x0).T)
        min_alpha = opt.minimize_scalar(f_alpha).x
        # Calculate the next value x1
        x1 = x0 - min_alpha * Df(x0).T
        if (la.norm(Df(x1)) < tol):
            converged = True
            break
        # Update x0 and repeat
        x0 = x1
    # Return minimizer guess, if it converged and in how many iters
    return x1, converged, iters


def test_steepest_descent():
    f = lambda x : x[0]**4 + x[1]**4 + x[2]**4
    print(steepest_descent(f, grad(f), anp.array([10.,10.,10.])))
    x0 = anp.array([10., 10.])
    epsilon = 1e-5
    M = 1000
    print(steepest_descent(opt.rosen, grad(opt.rosen), x0, epsilon, M))

# Problem 2
def conjugate_gradient(Q, b, x0, tol=1e-4):
    """Solve the linear system Qx = b with the conjugate gradient algorithm.

    Parameters:
        Q ((n,n) ndarray): A positive-definite square matrix.
        b ((n, ) ndarray): The right-hand side of the linear system.
        x0 ((n,) ndarray): An initial guess for the solution to Qx = b.
        tol (float): The convergence tolerance.

    Returns:
        ((n,) ndarray): The solution to the linear system Qx = b.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    # Initialize variables
    r0 = Q @ x0 - b
    d0 = -r0
    iters = 0
    n = len(x0)
    converged = False
    for i in range(n+1):
        # Calculate variables
        alpha = (r0.T @ r0) / (d0.T @ (Q @ d0))
        x1 = x0 + alpha * d0
        r1 = r0 + alpha * (Q @ d0)
        beta = (r1.T @ r1) / (r0.T @ r0)
        d1 = -r1 + beta * d0
        iters += 1

        if (la.norm(r0) < tol):
            converged = True
            iters += 1
            break
        # Update the variables
        x0 = x1
        r0 = r1
        d0 = d1
    # Return minimizer guess, if it converged and in how many iters
    return x1, converged, iters

def test_conjugate_gradient():
    Q = np.array([[2,0], [0,4]])
    b = np.array([1, 8])
    x0 = np.array([-2.,2.])
    f = lambda x : x[0]**2 + 2*x[1]**2 - x[0] - 8*x[1]
    print(conjugate_gradient(Q, b, x0))
    print(steepest_descent(f, grad(f), x0))
    n = 10
    A = np.random.random((n,n))
    Q = A.T @ A
    b, x0 = np.random.random((2,n))
    x = conjugate_gradient(Q, b, x0)[0]
    print(np.allclose(Q @ x, b))


# Problem 3
def nonlinear_conjugate_gradient(f, df, x0, tol=1e-5, maxiter=100):
    """Compute the minimizer of f using the nonlinear conjugate gradient
    algorithm.

    Parameters:
        f (function): The objective function. Accepts a NumPy array of shape
            (n,) and returns a float.
        Df (function): The first derivative of f. Accepts and returns a NumPy
            array of shape (n,).
        x0 ((n,) ndarray): The initial guess.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        ((n,) ndarray): The approximate minimum of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    # Initialize variables
    r0 = -df(x0).T
    d0 = r0
    f_alpha = lambda alpha : f(x0 - alpha*d0)
    min_alpha = opt.minimize_scalar(f_alpha).x
    x1 = x0 + min_alpha * d0
    iters = 1
    converged = False
    for i in range(1, maxiter):
        # Calculate next iteration of values
        r1 = -df(x1).T
        beta = (r1.T @ r1) / (r0.T @ r0)
        d1 = r1 + beta * d0
        f_alpha = lambda alpha : f(x1 - alpha*d1)
        min_alpha = opt.minimize_scalar(f_alpha).x
        x2 = x1 + min_alpha * d1
        iters += 1
        # Check if norm is within tolerance
        if (la.norm(r1) < tol):
            converged = True
            break
        # Update values
        r0 = r1
        d0 = d1
        x1 = x2
    return x2, converged, iters

def test_nonlinear_congugate_descent():
    print("Mine:", nonlinear_conjugate_gradient(opt.rosen, opt.rosen_der, np.array([10.,10.]), maxiter=1000))
    print("Scipy:", opt.fmin_cg(opt.rosen, np.array([10., 10.]), fprime=opt.rosen_der))
    Q = np.array([[2,0], [0,4]])
    b = np.array([1, 8])
    x0 = np.array([-2.,2.])
    f = lambda x : x[0]**2 + 2*x[1]**2 - x[0] - 8*x[1]
    print(conjugate_gradient(Q, b, x0))
    print(steepest_descent(f, grad(f), x0))
    n = 10
    A = np.random.random((n,n))
    Q = A.T @ A
    b, x0 = np.random.random((2,n))
    x = conjugate_gradient(Q, b, x0)[0]
    print(np.allclose(Q @ x, b))

# Problem 4
def prob4(filename="linregression.txt",
          x0=np.array([-3482258, 15, 0, -2, -1, 0, 1829])):
    """Use conjugate_gradient() to solve the linear regression problem with
    the data from the given file, the given initial guess, and the default
    tolerance. Return the solution to the corresponding Normal Equations.
    """
    # Load in data
    data = np.loadtxt(filename)
    # First column are y values
    b = data[:,0].copy()
    A = data
    # Replace y values with 1's
    A[:, 0] = np.full_like(b, 1)
    # Set up the normal equation and return solution
    Q = A.T @ A 
    b = A.T @ b
    return conjugate_gradient(Q, b, x0)[0]

# Problem 5
class LogisticRegression1D:
    """Binary logistic regression classifier for one-dimensional data."""

    def fit(self, x, y, guess):
        """Choose the optimal beta values by minimizing the negative log
        likelihood function, given data and outcome labels.

        Parameters:
            x ((n,) ndarray): An array of n predictor variables.
            y ((n,) ndarray): An array of n outcome variables.
            guess (array): Initial guess for beta.
        """
        # Negative log of Likelihood function
        L = lambda B : np.sum([np.log(1+np.e**(-1*(B[0] + B[1]*x[i])))\
                 + (1-y[i])*(B[0] + B[1]*x[i]) for i in range(len(x))])
        # Find the beta that minimizes L
        minimizer = opt.fmin_cg(L, guess)
        # Store the minimizer values as attributes
        self.B0 = minimizer[0]
        self.B1 = minimizer[1]

    def predict(self, x):
        """Calculate the probability of an unlabeled predictor variable
        having an outcome of 1.

        Parameters:
            x (float): a predictor variable with an unknown label.
        """
        # Use calculated parameters B0 and B1 to predict probability
        return 1 / (1 + np.exp(-(self.B0 + self.B1*x)))


# Problem 6
def prob6(filename="challenger.npy", guess=np.array([20., -1.])):
    """Return the probability of O-ring damage at 31 degrees Farenheit.
    Additionally, plot the logistic curve through the challenger data
    on the interval [30, 100].

    Parameters:
        filename (str): The file to perform logistic regression on.
                        Defaults to "challenger.npy"
        guess (array): The initial guess for beta.
                        Defaults to [20., -1.]
    """
    # Load data
    data = np.load(filename)
    # Instantiate class
    Regression = LogisticRegression1D()
    # Fit data
    Regression.fit(data[:,0], data[:,1], np.array([20,-1]))
    # Make predictions of O-Ring Damage at a given temperature in [30, 100]
    domain = np.linspace(30, 101, 70)
    predictions = []
    for x in domain:
        predictions.append(Regression.predict(x))
    # Plot the data
    plt.scatter(data[:, 0], data[:, 1], label="Previous Damage")
    # Plot the predictions
    plt.plot(domain, predictions, label="Pi(Damage at Launch", color="yellow")
    plt.legend()
    plt.title("Probability of O-Ring Damage")
    plt.xlabel("Temperature")
    plt.ylabel("O-Ring Damage")
    plt.show()
    # Return the probability of O-Ring Damage at 31 degrees F
    return Regression.predict(31)
