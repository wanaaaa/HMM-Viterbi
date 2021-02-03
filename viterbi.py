import numpy as np
from numba import jit

@jit(nopython=True)
def viterbi(A, C, B, O):
    """Viterbi algorithm for solving the uncovering problem

    Notebook: C5/C5S3_Viterbi.ipynb

    Args:
        A: State transition probability matrix of dimension I x I
        C: Initial state distribution  of dimension I
        B: Output probability matrix of dimension I x K
        O: Observation sequence of length N

    Returns:
        S_opt: Optimal state sequence of length N
        D: Accumulated probability matrix
        E: Backtracking matrix
    """
    I = A.shape[0]    # Number of states
    N = len(O)  # Length of observation sequence

    # Initialize D and E matrices
    D = np.zeros((I, N))
    E = np.zeros((I, N-1)).astype(np.int32)
    D[:, 0] = np.multiply(C, B[:, 0])

    # Compute D and E in a nested loop
    for n in range(1, N):
        print("n===============>", n)
        for i in range(I):
            temp_product = np.multiply(A[:, i], D[:, n-1])

            D[i, n] = np.max(temp_product) * B[i, O[n]]
            E[i, n-1] = np.argmax(temp_product)

            print("tempProdcut->", temp_product, "E->", E[i, n-1])
            print("i->", i, '=============')
        if n == 2:
            break
    # Backtracking
    S_opt = np.zeros(N).astype(np.int32)
    S_opt[-1] = np.argmax(D[:, -1])
    for n in range(N-2, 0, -1):
        S_opt[n] = E[int(S_opt[n+1]), n]

    return S_opt, D, E

# Define model parameters
A = np.array([[0.8, 0.1, 0.1],
              [0.2, 0.7, 0.1],
              [0.1, 0.3, 0.6]])

C = np.array([0.6, 0.2, 0.2])

B = np.array([[0.7, 0.0, 0.3],
              [0.1, 0.9, 0.0],
              [0.0, 0.2, 0.8]])


O = np.array([0, 2, 0, 2, 2, 1]).astype(np.int32)

# Apply Viterbi algorithm
S_opt, D, E = viterbi(A, C, B, O)
#
# print('Observation sequence:   O = ', O)
# print('Optimal state sequence: S = ', S_opt)
# np.set_printoptions(formatter={'float': "{: 7.4f}".format})
# print('D =', D, sep='\n')
# np.set_printoptions(formatter={'float': "{: 7.0f}".format})
# print('E =', E, sep='\n')