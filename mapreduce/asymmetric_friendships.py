# 
# Describe a MapReduce algorithm to count asymmetric friendships 
# 
# Consider a simple social network dataset consisting of 
#   key-value pairs where each key is a person and each value is a friend of that person. 
# 
# This one took a while and I need to get help from the forums.
#
# Suppose, the given data is 
# A, B
# B, A
# A, C

# In mapper, emit once the same as 
# (A,B),1
# (B,A), 1
# (A,C), 1
#and second time emit as 
# (B, A), 1
# (A, B), 1
# (C, A), 1

#The reduce phase gets all 6 tuples as given above, now just find the total for each key and emit only those whose total is less than 2. As you can see the totals are following:
# (A, B), 2
# (B,A), 2,
# (A,C) 1,
# (C,A), 1

# In reducer phase, we emit only keys having  total < 2 that is only [A,C] and [C, A] are emitted. 


import MapReduce
import sys

# Part 1
mr = MapReduce.MapReduce()

# Part 2
# map (in_key, in_value) -> list(out_key, intermediate_value)
#
#   Input will be two strings, personA, personB
#
def mapper(record):

    person = record[0]
    friend = record[1]
    
    mr.emit_intermediate( (person , friend), 1)
    mr.emit_intermediate( (friend , person), 1)

def reducer(key, list_of_values):  
    if sum(list_of_values) < 2:
        mr.emit((key))

# Part 4

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)