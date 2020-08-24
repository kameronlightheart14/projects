from mpi4py import MPI
from sys import argv
import numpy as np

# Problem 2
"""Pass a random NumPy array of shape (n,) from the root process to process 1,
where n is a command-line argument. Print the array and process number from
each process.

Usage:
    # This script must be run with 2 processes.
    $ mpiexec -n 2 python problem2.py 4
    Process 1: Before checking mailbox: vec=[ 0.  0.  0.  0.]
    Process 0: Sent: vec=[ 0.03162613  0.38340242  0.27480538  0.56390755]
    Process 1: Recieved: vec=[ 0.03162613  0.38340242  0.27480538  0.56390755]
"""
# Get id of engine
RANK = MPI.COMM_WORLD.Get_rank()
# Get command line argument for length of vector
n = int(argv[1])

if RANK == 0:
    # Initialize random array
    vec = np.random.randn(n)

    # Send array to engine 1
    print("Sending ", vec, " to 1")
    MPI.COMM_WORLD.Send(vec, dest=1)
elif RANK == 1:
    # Initialize vector variable to be recieved
    vec = np.zeros(n)

    # Get vector from engine 0
    MPI.COMM_WORLD.Recv(vec, source=0)
    print("Recieved ", vec, " from 0")
