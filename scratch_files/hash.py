import math
import csv
import itertools

x = 56
y = 164
b = 53180
r = ( (x+y)*(x+y-1) /2 + max(x,y) )
print (b)
print (r)
h = r % b
print (h)

max_val = 0

 # create chunked dataset
dataset = []
with open("data/data.txt") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader: # itertools.islice(reader, chunk_size + 1):
        cells = [ int(i) for i in row[0].split(" ")[:-1] ]
        dataset.append(cells)
        if max_val < max(cells): # corrected ti < instead of !=
            max_val = max(cells)

print(max_val)