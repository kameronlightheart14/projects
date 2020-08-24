# solutions.py
"""Volume 2: Gaussian Quadrature.
Kameron Lightheart
MATH 323
1/24/2019
"""

import numpy as np
from scipy.sparse import diags
from scipy import linalg as la
from scipy.integrate import quad
from scipy.integrate import nquad
from scipy.stats import norm
from matplotlib import pyplot as plt

class GaussianQuadrature:
    """Class for integrating functions on arbitrary intervals using Gaussian
    quadrature with the Legendre polynomials or the Chebyshev polynomials.
    """
    # Problems 1 and 3
    def __init__(self, n, polytype="legendre"):
        """Calculate and store the n points and weights corresponding to the
        specified class of orthogonal polynomial (Problem 3). Also store the
        inverse weight function w(x)^{-1} = 1 / w(x).

        Parameters:
            n (int): Number of points and weights to use in the quadrature.
            polytype (string): The class of orthogonal polynomials to use in
                the quadrature. Must be either 'legendre' or 'chebyshev'.

        Raises:
            ValueError: if polytype is not 'legendre' or 'chebyshev'.
        """
        # Raise error if invalid polytype
        if (polytype != "legendre" and polytype != "chebyshev"):
            raise ValueError("Please enter legendre or chebyshev for polytype parameter")
        # Save all the needed attributes
        self.polytype = polytype
        self.n = n
        if (polytype == "legendre"):
            self.weights_func = lambda x : 1
        else:
            self.weights_func = lambda x : 1 / np.sqrt(1-x**2)
        self.reciprocal_func = lambda x : 1 / self.weights_func(x)
        self.points, self.weights = self.points_weights(self.n)
        #print(self.points, self.weights)

    # Problem 2
    def points_weights(self, n):
        """Calculate the n points and weights for Gaussian quadrature.

        Parameters:
            n (int): The number of desired points and weights.

        Returns:
            points ((n,) ndarray): The sampling points for the quadrature.
            weights ((n,) ndarray): The weights corresponding to the points.
        """
        # Define alpha and beta
        if (self.polytype == "legendre"):
            alpha = 0
            beta = lambda k : k**2/(4*k**2-1)
        else:
            alpha = 0
            beta = lambda k : 1/2 if k == 1 else 1/4
        # Create Jacobi Matrix
        diagonals = np.array([np.zeros((n)), [np.sqrt(beta(k)) for k in range(1, self.n)], [np.sqrt(beta(k)) for k in range(1, self.n)]])
        self.Jacobi = diags(diagonals, [0, 1, -1]).toarray()
        #print(self.Jacobi)
        # Get the eigenvalues
        data = la.eig(self.Jacobi)
        points = np.real(data[0])
        #print(points)
        evecs = data[1]
        mew = 2 if self.polytype == "legendre" else np.pi
        weights = [mew * np.real(evecs[0,i]**2) for i in range(self.n)]
        return points, weights

    # Problem 3
    def basic(self, f):
        """Approximate the integral of a f on the interval [-1,1]."""
        # Define g(x) = f(x) / w(x)
        g = lambda x : f(x) * self.reciprocal_func(x)
        # Return inner product of weights and g(points)
        return np.array(self.weights).T @ np.array(g(self.points)) 


    # Problem 4
    def integrate(self, f, a, b):
        """Approximate the integral of a function on the interval [a,b].

        Parameters:
            f (function): Callable function to integrate.
            a (float): Lower bound of integration.
            b (float): Upper bound of integration.

        Returns:
            (float): Approximate value of the integral.
        """
        # Define h(x)
        h = lambda x : f((b-a)/2*x + (a+b)/2)
        # Use problem 3 to integrate
        return (b-a)/2 * self.basic(h)

    # Problem 6.
    def integrate2d(self, f, a1, b1, a2, b2):
        """Approximate the integral of the two-dimensional function f on
        the interval [a1,b1]x[a2,b2].

        Parameters:
            f (function): A function to integrate that takes two parameters.
            a1 (float): Lower bound of integration in the x-dimension.
            b1 (float): Upper bound of integration in the x-dimension.
            a2 (float): Lower bound of integration in the y-dimension.
            b2 (float): Upper bound of integration in the y-dimension.

        Returns:
            (float): Approximate value of the integral.
        """
        # Define h and g
        h = lambda x, y: f((b1-a1)/2*x + (a1+b1)/2, (b2-a2)/2*y + (a2+b2)/2)
        g = lambda x, y: h(x, y) * self.reciprocal_func(x) * self.reciprocal_func(y)
        # Double sum equation 10.5
        doubleSum = np.sum([np.sum([self.weights[i]*self.weights[j]*g(self.points[i], self.points[j])\
                         for j in range(self.n)]) for i in range(self.n)])
        return (b1 - a1)*(b2 - a2)/4 * doubleSum

def test_prob2():
    G = GaussianQuadrature(5, polytype="legendre")
    G = GaussianQuadrature(5, polytype="chebyshev")

def test_prob3():
    G = GaussianQuadrature(100, polytype="legendre")
    f = lambda x : 1 / np.sqrt(1 - x**2)
    print("Legendre:", quad(f, -1, 1)[0], G.basic(f))

    G = GaussianQuadrature(5, polytype="chebyshev")
    print("Chebyshev:", quad(f, -1, 1)[0], G.basic(f))

def test_prob4():
    G = GaussianQuadrature(100, polytype="legendre")
    f = lambda x : 1 / np.sqrt(1 - x**2)
    print("Legendre:", quad(f, 0, 1)[0], G.integrate(f, 0, 1))

    G = GaussianQuadrature(5, polytype="chebyshev")
    print("Chebyshev:", quad(f, 0, 1)[0], G.integrate(f, 0, 1))

def test_prob6():
    G = GaussianQuadrature(200, polytype="legendre")
    f = lambda x, y: np.sin(x) + np.cos(y)
    print("Legendre:", nquad(f, [[-10,10], [-1,1]])[0], G.integrate2d(f, -10, 10, -1, 1))

    G = GaussianQuadrature(200, polytype="chebyshev")
    print("Chebyshev:", nquad(f, [[-10,10], [-1,1]])[0], G.integrate2d(f, -10, 10, -1, 1))

# Problem 5
def prob5():
    """Use scipy.stats to calculate the "exact" value F of the integral of
    f(x) = (1/sqrt(2 pi))e^((-x^2)/2) from -3 to 2. Then repeat the following
    experiment for n = 5, 10, 15, ..., 50.
        1. Use the GaussianQuadrature class with the Legendre polynomials to
           approximate F using n points and weights. Calculate and record the
           error of the approximation.
        2. Use the GaussianQuadrature class with the Chebyshev polynomials to
           approximate F using n points and weights. Calculate and record the
           error of the approximation.
    Plot the errors against the number of points and weights n, using a log
    scale for the y-axis. Finally, plot a horizontal line showing the error of
    scipy.integrate.quad() (which doesn’t depend on n).
    """
    # Define f(x) function
    f = lambda x : 1/np.sqrt(2*np.pi)*np.e**(-x**2/2)
    # Get excact integral value using scipy.stats.norm
    exact = norm.cdf(2) - norm.cdf(-3)
    leg_error = []
    cheb_error = []
    for n in range(5, 55, 5):
        # Use GaussianQuadrature to approximate
        G_legendre = GaussianQuadrature(n)
        G_cheb = GaussianQuadrature(n, polytype="chebyshev")
        leg_approx = G_legendre.integrate(f, -3, 2)
        cheb_approx = G_cheb.integrate(f, -3, 2)
        leg_error.append(np.abs(leg_approx - exact))
        cheb_error.append(np.abs(cheb_approx - exact))

    # Plot the errrors
    plt.yscale('log')
    plt.plot(range(5, 55, 5), leg_error, label="Legendre error")
    plt.plot(range(5, 55, 5), cheb_error, label="Chebyshev error")
    plt.plot(range(5, 55, 5), [np.abs(quad(f, -3, 2)[0] - exact) for i in range(10)], label="Scipy error")
    plt.title("Error of approximation of 1/sqrt(2*pi) * e^-x^2/2")
    plt.ylabel("Error")
    plt.ylabel("n=5,10,15,...,50")
    plt.legend()
    plt.show()





