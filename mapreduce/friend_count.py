# Consider a simple social network dataset consisting of 
#   key-value pairs where each key is a person and each value is a friend of that person. 
# 
# Describe a MapReduce algorithm to count the number of friends each person has.

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
    print record
    person = record[0]
    friend = record[1]
    # print order_id, record

    mr.emit_intermediate(person, 1)

# 

def reducer(key, list_of_values):   
    
    mr.emit((key, sum(list_of_values)))

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)