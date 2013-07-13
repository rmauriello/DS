# 
# Remove the last 10 characters from each string of nucleotides and remove any duplicates generated.
#
# Given a set of key-value pairs where each key is sequence id and each value is a string of nucleotides, 
#  e.g., GCTTCCGAAATGCTCGAA....
#

import MapReduce
import sys


# Part 1
mr = MapReduce.MapReduce()

# Part 2
# map (in_key, in_value) -> list(out_key, intermediate_value)
#
# The input is a 2 element list: [sequence id, nucleotides]
#        sequence id: Unique identifier formatted as a string
#        nucleotides: Sequence of nucleotides formatted as a string
def mapper(record):
    dupes = []
    seq_id = record[0]
    nucleo = record[1]
    
    key = nucleo[:-10]
    if key not in dupes:
        mr.emit_intermediate(key, 1)
        dupes.append(key)

def reducer(key, list_of_values):
    mr.emit(key)    

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)