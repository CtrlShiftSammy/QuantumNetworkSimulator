import numpy as np

A = np.zeros((2, 2))

for i in range(2):
    for j in range(2):
        str = 'A[i][j] = 1'
        exec(str)
print(A)