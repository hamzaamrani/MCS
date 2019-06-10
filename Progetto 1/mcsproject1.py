import os
import numpy as np
import scipy as scipy
import scipy.sparse
import scipy.sparse.linalg
from scipy.io import mmread
from datetime import datetime
from scipy.linalg import norm


def sortedList():
    list = os.listdir("collection")

    pairs = []
    for file in list:
        # Use join to get full file path.
        location = os.path.join("collection", file)

        # Get size and add to list of tuples.
        size = os.path.getsize(location)
        pairs.append((size, file))
    # Sort list of tuples by the first element, size.
    pairs.sort(key=lambda s: s[0])
    return pairs

# Display pairs.
list = sortedList()
for matrix in list:
    #A = mmread("collection/"+matrix[1] ).tocsc()
    mat = scipy.io.loadmat("collection/"+matrix[1])
    A = mat['Problem']['A'][0][0]

    print("\nMatrix: "+matrix[1])
    print("Matrix dimension: " + str(A.shape[0]) + "x" + str(A.shape[1]))

    xe = scipy.ones(A.shape[0])
    b = A*xe

    x = scipy.empty(A.shape[0])

    begin = datetime.now()
    x = scipy.sparse.linalg.spsolve(A, b)
    end = datetime.now() - begin

    err = norm(x-xe)/norm(xe)

    print("Execution time: " + str(end) )
    print("Approximation error: " + str(err) )
