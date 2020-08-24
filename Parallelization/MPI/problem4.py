from mpi4py import MPI
from sys import argv
from scipy import linalg as la
import numpy as np

# Problem 4
"""The n-dimensional open unit ball is the set U_n = {x in R^n : ||x|| < 1}.
Estimate the volume of U_n by making N draws on each available process except
for the root process. Have the root process print the volume estimate.

Command line arguments:
    n (int): the dimension of the unit ball.
    N (int): the number of random draws to make on each process but the root.

Usage:
    # Estimate the volume of U_2 (the unit circle) with 2000 draws per process.
    $ mpiexec -n 4 python problem4.py 2 2000
    Volume of 2-D unit ball: 3.13266666667      # Results will vary slightly.
"""
# Get rank and size
RANK = MPI.COMM_WORLD.Get_rank()
SIZE = MPI.COMM_WORLD.Get_size()

# Grab command line arguments
n, N = int(argv[1]), int(argv[2])

if RANK != 0:
    # Approximate percentage within unit ball
    points = np.random.uniform(-1, 1, (n, N))

    lengths = la.norm(points, axis=0) < 1
    perc_within = lengths.mean()

    # Send to root engine
    MPI.COMM_WORLD.Send(perc_within, dest=0)
else:
    perc_withins = np.zeros(1)
    # Grab all the percentages
    for i in range(1, SIZE):
        perc_within = np.zeros(1)
        MPI.COMM_WORLD.Recv(perc_within, source=i)
        perc_withins += perc_within

    # Average the percentages
    avg = perc_withins / (SIZE - 1)
    
    # Estimate the area
    est_area = (2**n) * avg
    print("Estimated Area is ", est_area)
