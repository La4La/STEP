import time
import numpy as np
import matplotlib.pyplot as plt
from step2 import ijk_matrix_product
from step2 import strassen

x = []
ijk_time = []
ikj_time = []
str_time = []
for n in range(16, 514, 16):
    print('--n:', str(n))
    x.append(n)

    a = np.zeros((n, n)) # Matrix A
    b = np.zeros((n, n)) # Matrix B

    # Initialize the matrices to some values.
    for i in range(n):
        for j in range(n):
            a[i, j] = i * n + j
            b[i, j] = j * n + i

    # Calculating time of ijk algorithm
    begin = time.time()
    c = ijk_matrix_product(a,b)
    end = time.time()
    print('ijk:',str(end - begin))
    ijk_time.append(end - begin)

    # Calculating time of strassen algorithm
    begin = time.time()
    c = strassen(a, b)
    end = time.time()
    print('str:',str(end - begin))
    str_time.append(end - begin)

plt.plot(x, ijk_time, label='ijk')
plt.plot(x, str_time, label='strassen')
plt.title('matrix product calculating time')
plt.legend(loc='upper left')
plt.savefig('figure.png')

# Print C for debugging. Comment out the print before measuring the execution time.
#c= np.array(c)
#total = 0
#for i in range(n):
#    for j in range(n):
        # print c[i, j]
#        total += c[i, j]
# Print out the sum of all values in C.
# This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
#print ("sum: %.1f" % total)