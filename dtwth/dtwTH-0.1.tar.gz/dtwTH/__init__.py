import numpy as np

def dtwDistance(s, t):
    DTW = {}

    for i in range(len(s)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(t)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s)):
        for j in range(len(t)):
            dist = (s[i] - t[j]) ** 2
            DTW[i, j] = dist + min(DTW[(i - 1), j], DTW[(i, j-1)], DTW[(i - 1, j - 1)])

    return(np.sqrt(DTW[len(s) - 1, len(t) - 1]))
