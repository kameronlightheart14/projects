from mpi4py import MPI
import numpy as np
# Problem 1
"""Print 'Hello from process n' from processes with an even rank and
print 'Goodbye from process n' from processes with an odd rank (where
n is the rank).

Usage:
    $ mpiexec -n 4 python problem1.py
    Goodbye from process 3                  # Order of outputs will vary.
    Hello from process 0
    Goodbye from process 1
    Hello from process 2

    # python problem1.py
    Hello from process 0
"""
# Get communicator
COMM = MPI.COMM_WORLD

# Get id of engine
RANK = COMM.Get_rank()

# Evan rank print hello, odd print goodbye
if RANK % 2 == 0:
    print("Hello")
else:
    print("Goodbye")
