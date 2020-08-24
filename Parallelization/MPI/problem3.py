from mpi4py import MPI
import numpy as np

# Problem 3
"""In each process, generate a random number, then send that number to the
process with the next highest rank (the last process should send to the root).
Print what each process starts with and what each process receives.

Usage:
    $ mpiexec -n 2 python problem3.py
    Process 1 started with [ 0.79711384]        # Values and order will vary.
    Process 1 received [ 0.54029085]
    Process 0 started with [ 0.54029085]
    Process 0 received [ 0.79711384]

    $ mpiexec -n 3 python problem3.py
    Process 2 started with [ 0.99893055]
    Process 0 started with [ 0.6304739]
    Process 1 started with [ 0.28834079]
    Process 1 received [ 0.6304739]
    Process 2 received [ 0.28834079]
    Process 0 received [ 0.99893055]
"""
num_engines = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
x = np.random.randn(1)

if RANK == num_engines-1:
    MPI.COMM_WORLD.Recv(x, source=RANK-1)
    print("Engine ", RANK, " recieved ", x)

    # Send random variable to root engine
    x = np.random.randn(1)
    print("Engine ", RANK, "Sending ", x, " to engine ", RANK+1)
    MPI.COMM_WORLD.Send(x, dest=0)
elif RANK == 0:
    x = np.random.randn(1)
    print("Engine ", RANK, "Sending ", x, " to engine ", RANK+1)
    MPI.COMM_WORLD.Send(x, dest=RANK+1)

    MPI.COMM_WORLD.Recv(x, source=num_engines-1)
    print("Engine ", RANK, " recieved ", x)
else:
    MPI.COMM_WORLD.Recv(x, source=RANK-1)
    print("Engine ", RANK, " recieved ", x)

    x = np.random.randn(1)
    print("Engine ", RANK, "Sending ", x, " to engine ", RANK+1)
    MPI.COMM_WORLD.Send(x, dest=RANK+1)
