# simplex.py
"""Volume 2: Simplex.
Kameron Lightheart
Math 323
2/28/2019

Problems 1-6 give instructions on how to build the SimplexSolver class.
The grader will test your class by solving various linear optimization
problems and will only call the constructor and the solve() methods directly.
Write good docstrings for each of your class methods and comment your code.

prob7() will also be tested directly.
"""

import numpy as np

# Problems 1-6
class SimplexSolver(object):
    """Class for solving the standard linear optimization problem

                        maximize        c^Tx
                        subject to      Ax <= b
                                         x >= 0
    via the Simplex algorithm.
    """
    def __init__(self, c, A, b):
        """Check for feasibility and initialize the tableau.

        Parameters:
            c ((n,) ndarray): The coefficients of the objective function.
            A ((m,n) ndarray): The constraint coefficients matrix.
            b ((m,) ndarray): The constraint vector.

        Raises:
            ValueError: if the given system is infeasible at the origin.
        """
        # Check if feasible at origin
        if np.any(0 > b):
            raise ValueError("The problem is not feasible at the origin")
        # Save attributes
        self.A = A
        self.coeffs = c
        self.b = b
        self.m = len(b)
        self.n = len(c)
        self.vars = np.arange(self.n, self.n+self.m)
        self.vars = np.hstack((self.vars, np.arange(self.n)))
        # Set up the tableau matrix
        self.T = self.set_up_tableau()

    def set_up_tableau(self):
        c_bar = np.hstack((self.coeffs, np.zeros_like(self.b)))
        A_bar = np.hstack((self.A, np.eye(self.m)))
        # First "column" in T with 0 on top of b
        col1 = np.hstack((np.array([0]), self.b))
        col1 = np.reshape(col1, (self.m+1, 1))
        # Second "column" in T with -c_bar.T on top of A_bar
        col2 = np.vstack((-c_bar.T, A_bar))
        # Third "column" in T with 1's on top of 0's
        col3 = np.hstack((np.array([1]), np.zeros_like(self.b)))
        col3 = np.reshape(col3, (self.m+1, 1))
        # Hstack the "columns" together to form the tableau T
        return np.hstack((col1, col2, col3))

    def get_pivot_index(self):
        col_index = -1
        for i in range(1, self.n+self.m+1):
            if (self.T[0, i] < 0):
                col_index = i
                break
        if (col_index == -1):
            # Algorithm has completed since all values are positive
            return (-1, -1)
        ratios = np.full((self.m + 1,), np.inf)
        isvalid = False # This variable helps us know if it is solvable
        for j in range(1, self.m+1):
            if (self.T[j, col_index] <= 0):
                continue
            isvalid = True
            ratios[j] = self.T[j, 0] / self.T[j, col_index]
        #print(ratios)
        if (not isvalid):
            raise ValueError("None of the ratios are positive, no solution")
        row_index = np.argmin(ratios)
        return (row_index, col_index)

    def single_pivot(self):
        pivot_row_index, pivot_col_index = self.get_pivot_index()
        #print(pivot_row_index, pivot_col_index)
        #print(self.vars)
        #print(pivot_row_index, pivot_col_index)
        if (pivot_row_index == -1):
            # True means algorithm is complete!
            return True
        enter_index = (self.m - 1) + pivot_col_index
        leave_index = pivot_row_index - 1
        self.vars[enter_index], self.vars[leave_index] =\
             self.vars[leave_index], self.vars[enter_index]
        pivot_val = self.T[pivot_row_index, pivot_col_index]
        # 1. Divide pivot row by value of pivot entry
        self.T[pivot_row_index, :] /= pivot_val
        # 2. Use the pivot row to zero out all entries in the pivot column
        for row in range(self.m+1):
            # Skip the pivot row
            if (row == pivot_row_index):
                continue
            # Make sure the current entry is not already 0
            if (self.T[row, pivot_col_index] == 0):
                continue
            # Do row operations to zero out the pivot_column except
            self.T[row, :] -= self.T[pivot_row_index, :] * self.T[row, pivot_col_index]
        # False means algorithm not complete
        return False


    def solve(self):
        """Solve the linear optimization problem.

        Returns:
            (float) The maximum value of the objective function.
            (dict): The basic variables and their values.
            (dict): The nonbasic variables and their values.
        """
        finished = False
        # Pivot until algorithm returns that it is finished
        while(not finished):
            finished = self.single_pivot()
        # Get the answers from the tableau T
        optimal_val = self.T[0,0]
        basic_dict = {}
        nonbasic_dict = {}
        # Get basic values
        for i in range(self.m):
            basic_dict[self.vars[i]] = self.T[i+1, 0]
        # Set non-basic variables to 0
        for i in range(self.m, self.m+self.n):
            nonbasic_dict[self.vars[i]] = 0
        #print(self.vars)
        return (optimal_val, basic_dict, nonbasic_dict) 

def test_Simplex_Solver():
    c = np.array([3., 2])
    A = np.array([[1.,-1], [3,1], [4, 3]])
    b = np.array([2., 5, 7])
    simplex = SimplexSolver(c, A, b)
    #simplex.set_up_tableau()
    #print(simplex.get_pivot_index())
    #simplex.single_pivot()
    print(simplex.solve())

# Problem 7
def prob7(filename='productMix.npz'):
    """Solve the product mix problem for the data in 'productMix.npz'.

    Parameters:
        filename (str): the path to the data file.

    Returns:
        The minimizer of the problem (as an array).
    """
    data = np.load(filename)
    A = data['A']
    # 'p' = Coefficients of objective function
    p = data['p']
    #print(len(p))
    # A@x <= m
    m = data['m']
    # xi <= di
    d = data['d']
    I = np.eye(len(d))
    A = np.vstack((A,I))
    b = np.hstack((m, d))
    simplex = SimplexSolver(p, A, b)
    ans = simplex.solve()
    
    return [ans[1][i] for i in range(4)]

    
