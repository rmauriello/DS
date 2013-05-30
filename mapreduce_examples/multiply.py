#
# Mapreduce implementation of matrix multiplication A x B
#
#   Given matrices A and B in a sparse matrix format, where each record is of the form i, j, value.  
#         A has dimensions L x M
#         B has dimensions M x N
#
#   Note that this code hard-codes M. Apparently a two-pass map-reduce job can be used to find size of matrices. 

import MapReduce
import sys
import re

# Part 1
mr = MapReduce.MapReduce()

# Part 2
# map (in_key, in_value) -> list(out_key, intermediate_value)
#
# Every list element corresponds to a different field in its corresponding record.
#   First element (matrix_id): either "a" or "b"
#   Second element: i, j, value corresponding to row, column, element value
# 
def mapper(record):   
    matrix_id = record[0]                             # matrix, either A or B
    row = record[1]
    column = record[2]
    value = record[3]          
        

    if matrix_id == "a":
        for k in range(5):   
                    # emit ((i,k), A[i,j]) for k in 1..N
            mr.emit_intermediate ((row,k), record)
    else:
        for k in range(5):
                # emit ((i,k), B[j,k]) for i in 1..L
            mr.emit_intermediate( (k,column), record)

# 
# reduce (out_key, list(intermediate_value)) -> list(out_value)
#  Output is matrix row records formatted as tuples. 
#    Each tuple will have the format (i, j, value) where each element is an integer.


# List example  [[u'a', 1, 0, 33], [u'a', 1, 3, 26], [u'a', 1, 4, 95], 
#                [u'b', 0, 3, 28], [u'b', 1, 3, 12], [u'b', 2, 3, 3], [u'b', 4, 3, 69]]

def reducer(key, list_of_values):
    i = key[0]        # row of result matrix
    k = key[1]        # column of result matrix
    
    ai = {}           # initialize dictionaries to hold matrix A, B
    bj = {}          

    for v in list_of_values:
        if v[0] == "a":
            ai[v[2]] = v[3]   # only row values
        elif v[0] == "b":
            bj[v[1]] = v[3]     # only column values

# Lazy dot product. Multiply only if k is found in both row and column  
# c[i][j] = a[i][0]*b[0][j] + a[i][1]*b[1][j] + a[i][2]*b[2][j] + a[i][3]*b[3][j] + a[i][4]*b[4][j] 

    sum = 0
    for k in range(5):
        if k in ai and k in bj:
            sum += ai[k] * bj[k]
    
    n=[]
    n.append(key[0])
    n.append(key[1])
    n.append(sum)
    mr.emit(tuple(n))

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)