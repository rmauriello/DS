# Simulate a SQL join
#  SELECT * FROM Orders, LineItem 
#   WHERE Order.order_id = LineItem.order_id

import MapReduce
import sys


# Part 1
mr = MapReduce.MapReduce()

# Part 2
# map (in_key, in_value) -> list(out_key, intermediate_value)
#
#   Input will be database records formatted as lists of Strings.
# 
# Every list element corresponds to a different field in its corresponding record.
#   First element (table_id): either "line_item" or "order"
#   Second element: order_id
# 
#   LineItem records have 17 elements including the identifier string.
#   Order records have 10 elements including the identifier string. 
#
def mapper(record):
    order_id = record[1]
    # print order_id, record

    mr.emit_intermediate(order_id, record)

# 
# reduce (out_key, list(intermediate_value)) -> list(out_value)
#   Output is a single list of length 27 that contains 
#    the fields from the order record followed by the fields from the line item record. 
#    Each list element should be a string.

def reducer(key, list_of_values):   
    for t in list_of_values:
        for u in list_of_values:
            if (t[0] == "order" and u[0] == "line_item"): 
                result =  ", ".join(str(x) for x in t[1:len(t)]) +  ", ".join(str(x) for x in u[1:len(u)])
                
                mr.emit((t + u))

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)