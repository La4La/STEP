#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import time
import math
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix

def input(pageName, pages_path, links_path):

    # read pages
    print('Read pages')
    start = time.clock()

    f = open(pages_path, encoding='utf-8')
    line = f.readline()
    while line:
        items = line[:-1].split('\t')
        pageName.append(items[1])
        line = f.readline()
    f.close()

    dummyNode = len(pageName) # add a dummy node at the end
    pageSize = dummyNode + 1
    pageName.append('dummyNode')

    end = time.clock()
    print('time = ', end - start, '[s]')
    print('page size:', dummyNode)
    print('')


    # read links
    print('Read links')
    start = time.clock()

    origin, destination= [], []
    sum = np.zeros([pageSize], dtype = np.uint32)
    f = open(links_path)
    line = f.readline()
    while line:
        items = line.split('\t')
        destination.append(int(items[1]))
        origin.append(int(items[0]))
        sum[int(items[0])] += 1
        line = f.readline()
    f.close()

    end = time.clock()
    print('time = ', end - start, '[s]')
    print('number of links:', len(origin))
    print('')


    # make a weight matrix
    print('Make the weight matrix start')
    start = time.clock()

    matrix = lil_matrix((pageSize, pageSize), dtype = np.float16)
    for k in range(len(origin)):
        if k % 5000000 == 0:
            print('link', k)
        matrix[destination[k], origin[k]] = 1 / sum[origin[k]]

    # if there was NO link from i-th page,
    # add a link from i-th page to dummy
    print('adding dummy')
    for i in range(len(sum)):
        if sum[i] == 0:
            matrix[dummyNode, i] = 1

    matrix = matrix.tocsr()

    end = time.clock()
    print('time = ', end - start, '[s]')

    return matrix, pageSize


# Output result
def output(point, pageName, wfile_name):
    pageSize = len(point)
    pw = []

    for i in range(pageSize - 1):  # except dummy node
        pw.append([point[i], i, pageName[i]])

    wfile = csv.writer(open(wfile_name + '.csv', 'w', encoding = 'utf-8'))
    wfile.writerows(pw)
    
    pw.sort(key = lambda x:x[0], reverse = True)
    print('top 10:')
    print(pw[:10])
    wfile = csv.writer(open(wfile_name + '_sorted.csv', 'w', encoding = 'utf-8'))
    wfile.writerows(pw)


# Computation of PageRank
def computeRank(aMat, pageSize):
    # Initialize all pages' score to 1
    pVec = np.mat([1.0] * pageSize).reshape(pageSize, 1)

    for loop in range(200):
        print('loop', loop)
        # for loop in range(int(10 * (math.log2(pageSize)))):
        pVec = 0.85 * aMat * pVec + 0.15 / pageSize

    pVec = np.array(pVec).reshape(1, pageSize)[0]
    return pVec


# ----Main-----

pageName = []

# Get information of pages and links
pages_path = 'pages.txt'
links_path = 'links.txt'
aMat, pageSize = input(pageName, pages_path, links_path)
print('')

# Computation of PageRank
print('Compute PageRank starts!!')
start = time.clock()
point = computeRank(aMat, pageSize)
print('Compute PageRank finished!!')
end = time.clock()
print('Computing time = ', end - start, '[s]')

# Output csv file
wfile_name = 'ranking'
output(point, pageName, wfile_name)
