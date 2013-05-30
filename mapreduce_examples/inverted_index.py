# Create an Inverted index. 
# Given a set of documents, an inverted index is a dictionary where each word is associated with a list of the 
# document identifiers in which that word appears.  


import MapReduce
import sys


# Part 1
mr = MapReduce.MapReduce()

# Part 2
# map (in_key, in_value) -> list(out_key, intermediate_value)
#   Input is a 2 element list: [document_id, text]
#    document_id: document identifier formatted as a string
#    text: text of the document formatted as a string
#   
def mapper(record):
    # key: document identifier
    # value: document contents
    
    used  = []  # make sure not to emit dupes
    docid = record[0]
    text  = record[1]
    words = text.split()


    for w in words:
      if w not in used:
        mr.emit_intermediate(w, docid)
        used.append(w)

# 
# reduce (out_key, list(intermediate_value)) -> list(out_value)
#  Output is(word, document ID list) tuple where word is a String and document ID list is a list of Strings.
#


def reducer(key, list_of_values):
    mr.emit((key, list_of_values))

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)