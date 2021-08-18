# solutions.py
"""Volume 1: The Page Rank Algorithm.
Kameron Lightheart
MATH 347
3/5/19
"""

import numpy as np
from scipy import linalg as la
import csv
import networkx as nx
from itertools import combinations as comb

# Problems 1-2
class DiGraph:
    """A class for representing directed graphs via their adjacency matrices.

    Attributes:
        (fill this out after completing DiGraph.__init__().)
    """
    # Problem 1
    def __init__(self, A, labels=None):
        """Modify A so that there are no sinks in the corresponding graph,
        then calculate Ahat. Save Ahat and the labels as attributes.

        Parameters:
            A ((n,n) ndarray): the adjacency matrix of a directed graph.
                A[i,j] is the weight of the edge from node j to node i.
            labels (list(str)): labels for the n nodes in the graph.
                If None, defaults to [0, 1, ..., n-1].
        """
        A = np.copy(A)
        self.n = A.shape[0]

        # Set the labels
        if (type(labels) == type(None)):
            self.labels = np.arange(self.n)
        elif len(labels) != self.n:
            raise ValueError("Number of labels doesn't match size of A")
        else:
            self.labels = labels

        # Fix any sinks (0 columns) by adding paths to all other nodes
        # (make it a column of 1's instead)
        for j in range(self.n):
            if np.all(A[:, j] == 0):
                A[:, j] = 1

        # Normalize the columns
        self.A_hat = A / A.sum(axis=0)

    # Problem 2
    def linsolve(self, epsilon=0.85):
        """Compute the PageRank vector using the linear system method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Returns:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        # Make empty dictionary of labels to values
        labels_dict = {}
        I = np.identity(self.n)
        ones = np.ones(self.n)
        p = la.solve((I - epsilon*self.A_hat), (1-epsilon)/self.n*ones)
        for i in range(self.n):
            labels_dict[self.labels[i]] = p[i]
        return labels_dict

    # Problem 2
    def eigensolve(self, epsilon=0.85):
        """Compute the PageRank vector using the eigenvalue method.
        Normalize the resulting eigenvector so its entries sum to 1.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        # Make empty dictionary of labels to values
        labels_dict = {}
        # Solve for PageRank values using eigenvalues/vectors
        E = np.ones_like(self.A_hat)
        B = (epsilon*self.A_hat + (1-epsilon)/self.n*E)
        evals, evecs = la.eig(B)
        # By Perron's theorem lambda = 1 is the largest eval
        p = evecs[:, 0]
        p = p / la.norm(p, ord=1)
        for i in range(self.n):
            labels_dict[self.labels[i]] = p[i]
        return labels_dict

    # Problem 2
    def itersolve(self, epsilon=0.85, maxiter=100, tol=1e-12):
        """Compute the PageRank vector using the iterative method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.
            maxiter (int): the maximum number of iterations to compute.
            tol (float): the convergence tolerance.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        # Make empty dictionary of labels to values
        labels_dict = {}
        # Start with initial guess p0
        p0 = np.full(self.n, 1/self.n)
        pk = p0
        ones = np.ones(self.n)
        # Run algorithm
        for i in range(1, maxiter):
            pk1 = epsilon*self.A_hat @ pk + (1-epsilon)/self.n*ones
            if (la.norm(pk1 - pk) < tol):
                break
            pk = pk1
        for i in range(self.n):
            labels_dict[self.labels[i]] = pk1[i]
        return labels_dict
        
def test_prob1():
    A = np.array([[0,0,0,0], [1,0,1,0], [1,0,0,1], [1,0,1,0]])
    digraph = DiGraph(A) 
    A = np.array([[0,0,0,0,0],[0,1,1,0,1],[0,1,1,0,1],[0,1,0,1,0],[0,0,1,0,1]])
    digraph = DiGraph(A)

def test():
    A = np.array([[0,0,0,0],
                  [1,0,1,0],
                  [1,0,0,1],
                  [1,0,1,0]])
    labels = ['a','b','c','d']
    DG = DiGraph(A,labels)
    print(get_ranks(DG.itersolve()))
    print(get_ranks(DG.eigensolve()))
    print(get_ranks(DG.linsolve()))

def test_prob2():
    A = np.array([[0,0,0,0], [1,0,1,0], [1,0,0,1], [1,0,1,0]])
    digraph = DiGraph(A) 
    print(digraph.linsolve())
    print(digraph.eigensolve())
    print(digraph.itersolve())
    A = np.array([[0,0,0,0,0],[0,1,1,0,1],[0,1,1,0,1],[0,1,0,1,0],[0,0,1,0,1]])
    digraph = DiGraph(A)
    print(digraph.eigensolve())

# Problem 3
def get_ranks(d):
    """Construct a sorted list of labels based on the PageRank vector.

    Parameters:
        d (dict(str -> float)): a dictionary mapping labels to PageRank values.

    Returns:
        (list) the keys of d, sorted by PageRank value from greatest to least.
    """
    # Return the sorted values of the given dictionary
    return sorted(d, key=d.get, reverse=True)

def test_prob3():
    A = np.array([[0,0,0,0], [1,0,1,0], [1,0,0,1], [1,0,1,0]])
    digraph = DiGraph(A) 
    labels_dict = digraph.itersolve()
    print(get_ranks(labels_dict))


# Problem 4
def rank_websites(filename="web_stanford.txt", epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i if webpage j has a hyperlink to webpage i. Use the DiGraph class
    and its itersolve() method to compute the PageRank values of the webpages,
    then rank them with get_ranks().

    Each line of the file has the format
        a/b/c/d/e/f...
    meaning the webpage with ID 'a' has hyperlinks to the webpages with IDs
    'b', 'c', 'd', and so on.

    Parameters:
        filename (str): the file to read from.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of webpage IDs.
    """
    labels = set()
    labels_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            node = line.strip().split("/")
            labels.update(node)
    # Make dictionary of labels to a counting index
    labels = sorted(list(labels))
    labels_dict = dict(zip(labels, np.arange(len(labels))))

    # Create and populate wieght graph matrix
    n = len(labels)
    A = np.zeros((n, n))
    with open(filename, 'r') as file:
        for line in file:
            node = line.strip().split("/")
            col_index = labels_dict[node[0]]
            for i in range(1, len(node)):
                row_index = labels_dict[node[i]]
                A[row_index, col_index] = 1
    # Use DiGraph's itersolve to get pagerank results
    digraph = DiGraph(A, list(labels))
    solve_dict = digraph.itersolve()
    order = get_ranks(solve_dict)
    return order

# Problem 5
def rank_ncaa_teams(filename, epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i with weight w if team j was defeated by team i in w games. Use the
    DiGraph class and its itersolve() method to compute the PageRank values of
    the teams, then rank them with get_ranks().

    Each line of the file has the format
        A,B
    meaning team A defeated team B.

    Parameters:
        filename (str): the name of the data file to read.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of team names.
    """
    teams_set = set()
    # Open file to read
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # Ignore the headers
        next(reader)
        # Get the rest of the data and add each team to the set
        data = list(reader)
        for game in data:
            teams_set.add(game[0])
            teams_set.add(game[1])
    # Make dictionary of teams
    teams_dict = dict(zip(teams_set, np.arange(len(teams_set))))
    # Populate graph array where losing team maps to winning team
    n = len(teams_set)
    A = np.zeros((n,n))
    for game in data:
        win_team = game[0]
        lose_team = game[1]
        win_index = teams_dict[win_team]
        lose_index = teams_dict[lose_team]
        A[win_index, lose_index] += 1
    digraph = DiGraph(A, list(teams_set))
    solve_dict = digraph.itersolve(epsilon=epsilon)
    order = get_ranks(solve_dict)
    return order

def test_prob5():
    print(rank_ncaa_teams("ncaa2010.csv"))


# Problem 6
def rank_actors(filename="top250movies.txt", epsilon=0.85):
    """Read the specified file and construct a graph where node a points to
    node b with weight w if actor a and actor b were in w movies together but
    actor b was listed first. Use NetworkX to compute the PageRank values of
    the actors, then rank them with get_ranks().

    Each line of the file has the format
        title/actor1/actor2/actor3/...
    meaning actor2 and actor3 should each have an edge pointing to actor1,
    and actor3 should have an edge pointing to actor2.
    """
    # Initialize DiGraph uising networkx (nx)
    DG = nx.DiGraph()
    with open(filename, 'r', encoding="utf-8") as file:
        for line in file:
            # Raw contains movie then actors in movie
            raw = line.strip().split("/")
            actors = raw[1:]
            # Add edges or increment if already exists
            combinations = comb(actors, 2)
            for actor_pair in combinations:
                if (DG.has_edge(actor_pair[1], actor_pair[0])):
                    DG[actor_pair[1]][actor_pair[0]]["weight"] += 1
                else:
                    DG.add_edge(actor_pair[1], actor_pair[0], weight=1)
    # Use networkx to get the dictionary
    actors_dict = nx.pagerank(DG, alpha=epsilon)
    # Get the order of ranking
    order = get_ranks(actors_dict)
    return order

