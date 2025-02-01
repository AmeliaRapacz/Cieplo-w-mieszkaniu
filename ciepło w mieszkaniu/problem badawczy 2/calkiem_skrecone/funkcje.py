import numpy as np

def f(P, ro, Ri, cw):
    return(P/(ro*Ri*cw))

def matrix(n):
    matrix = np.zeros((n, n))
    matrix[0, 0] = -2
    matrix[0, 1] = 1
    matrix[n - 1, n - 1] = -2
    matrix[n - 1, n - 2] = 1
    for i in range(1, n - 1):
        matrix[i, i - 1] = 1
        matrix[i, i] = -2
        matrix[i, i + 1] = 1
    return matrix

def diff_matrix(N, M):
    dX = matrix(N)
    dY = matrix(M)
    L = np.kron(np.eye(M), dX)
    R = np.kron(dY, np.eye(N))
    return L + R
