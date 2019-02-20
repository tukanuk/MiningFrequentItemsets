import re
import itertools
import sys
import csv
import time
import os
import pandas as pd
import numpy as np
from shutil import copyfile

fileName='data/data.txt'
hashTable={}
bitVector={}
freqItems=[]
freqItemsCurItr=[]
my_dict={}
bitVector=[]
frequent_items=[]             # list of the frequent items
weight=0


def addWeights(d, basket):
    global weight
    for item in basket:
        if item not in d:
            d[item] = weight
            weight += 1

def updateHashTable(line, my_dict, size, max_val):
    global hashTable
    items = [list(x) for x in itertools.combinations(line, size)]

    for pair in items:
        total = pair[0] + pair[1] * max_val
        if total in hashTable:
            hashTable[total] += 1
        else:
            hashTable[total] = 1

def generateFreqCandidates(items):
    global freqItemsCurItr
    temp = []
    freqItemsCurItr = []
    for key in items:
        if items[key] >= support:
            freqItemsCurItr.append(key)
            freqItems.append(key)
    freqItems.sort()
    freqItemsCurItr.sort()
    for tuples in freqItemsCurItr:
        # temp.append(list(tuples))
        temp.append(list(tuples)[0])
    freqItemsCurItr = temp

    return freqItemsCurItr


def countCandidatesAndFillHashTable2(_pass, dataset, max_val):
    global items
    global my_dict  # Has weights for each item in the basket
    global freqItems
    flag = False
    weight = -1

    # ***Counting Candidates***#

    for basket in dataset:
        if (_pass == 0):
            addWeights(my_dict, basket)

        # logTimerStart = time.time()
        itemsInBasket = list(itertools.combinations(basket, _pass + 1))
        # logTimerEnd = time.time()
        # if ((logTimerEnd - logTimerStart) > 0.1): log.debug("Line 171: %f", (logTimerEnd-logTimerStart) )

        for item in itemsInBasket:
            if (_pass != 0):

                # logTimerStart = time.time()
                item_1 = list(itertools.combinations(item, _pass))
                # logTimerEnd = time.time()
                # if ((logTimerEnd - logTimerStart) > 0.1): log.info("Line 181: %f", (logTimerEnd-logTimerStart) )

                for key in item_1:
                    if key in freqItems:
                        flag = True
                    else:
                        flag = False
                        break
                if flag == True:
                    if item in items:
                        items[item] += 1
                    else:
                        items[item] = 1
            else:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1
        updateHashTable(basket, my_dict, _pass + 2, max_val)
        # my_file.close()


# @logTimer
def generateBitVector(min_val, max_val):
    global bitVector
    bitVector = []

    diff = (max_val - min_val)
    bitVector = np.zeros(diff, dtype=int)

    for val in hashTable:
        if hashTable[val] >= support:
            bitVector[val - min_val] = 1


# Outputting to a CSV
# @logTimer
def OutputCSV(data_result):
    """ Takes a list as input and output as as CSV
        A check is made to see if if a file exists and a
        numerical increment is added until a unique file name is made
    """
    inc = 0
    ffname = "data/pcy_result_t" + str(totalTestCount) + "_b" + str(bucketSize) + "_" + str(inc) + ".csv"

    # turn on and off auto file incrementer
    if (1):
        while os.path.isfile(ffname):
            inc += 1
            ffname = "data/pcy_result_t" + str(totalTestCount) + "_b" + str(bucketSize) + "_" + str(inc) + ".csv"

    with open(ffname, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for line in data_result:
            writer.writerow(line)

    # makes a copy with the _0 suffix so you can have an
    # auto refresing csv of results open and retain past runs
    copyfile(ffname, "data/pcy_result_0.csv")




# Generating items-singletons
if __name__ == '__main__':

    # Testing sets
    chunk_percent = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # chunk_percent = [0.05]
    thresholds = [0.01]  # 0.01, 0.05, 0.1]

    # basket count
    data_lines = open(fileName).readlines()
    basket_count = len(data_lines)

    # calculate total number of tests
    totalTestCount = len(chunk_percent) * len(thresholds)
    testCount = 0

    print (" # %Thr Supp Chunk  Fre      Time")

    # Setup for CSV
    data_result = []
    data_result_line = ["#", "threshold", "support", "chunk_size", "c_%", "f_items", "time"]
    data_result.append(data_result_line)

    # Nested loops for test sets
    for threshold in thresholds:
        for percent in chunk_percent:

            # get line count for chunk
            chunk_size = int(basket_count * percent)

            # finding max value for bucket size
            max_val = 0

            # create chunked dataset
            dataset = []
            with open(fileName) as csvfile:
                reader = csv.reader(csvfile)
                for row in itertools.islice(reader, chunk_size + 1):
                    cells = [ int(i) for i in row[0].split(" ")[:-1] ]
                    dataset.append(cells)
                    if max_val < max(cells):
                        max_val = max(cells)

            # support threshold
            support = int(threshold * chunk_size)

            # bucket size is set to 2 times the sum of max in current chunk
            # bucketSize = int(str(max_val) + str(max_val))
            # da = len(my_dict)
            # bucketSize = int(pow(len(my_dict),2)/2)
            bucketSize = (max_val * 1000)
            # log.info("SET: %d (%.2f) support, %d (%.2f) chunk ", support, threshold, chunk_size, percent)

            start = time.time()  # Timer start

            _pass = 0
            size = 0

            items = {}
            # generateHashTable(bucketSize)
            countCandidatesAndFillHashTable2(_pass, dataset, max_val)
            _pass += 1

            frequent_items = generateFreqCandidates(items)  # list of frequent items
            min_hval = min(int(x) for x in hashTable)
            max_hval = max(int(x) for x in hashTable)
            generateBitVector(min_hval, max_hval)

            current_frequent_pairs = [list(x) for x in itertools.combinations(frequent_items, 2)]

            frequent_pairs = []
            temp_frequent_pairs_print = {}

            for pair in current_frequent_pairs:

                # hashIndex = int(((pair[0] + pair[1]) * (pair[0] + pair[1] + 1)) / 2) + pair[1]
                # if hashTable[hashIndex] >= support:
                hashIndex = pair[0] + pair[1] * max_val
                if bitVector[hashIndex - min_hval] == 1:
                    frequent_pairs.append(pair)
                    # temp_frequent_pairs_print[tuple(pair)] = hashTable[hashIndex]

            testCount += 1
            end = time.time() # Timer stop

            # Build a list for use in CSV output
            # data_result_line = [testCount, threshold, support, chunk_size, percent, len(frequent_items), (end-start)*1000]
            data_result_line = [testCount, threshold, support, chunk_size, percent, len(frequent_pairs), (end -start ) *1000]
            data_result.append(data_result_line)

            print ("%2d %.2f %4d %5d %4d %9.3f" %
            (testCount, threshold, support, chunk_size, len(frequent_pairs), (end - start) * 1000))

            # print(max_val)

            # values = []
            # temp_df = pd.DataFrame( columns=['Keys', 'Support'])
            # for key in temp_frequent_pairs_print:
            #     values = [key, temp_frequent_pairs_print[key]]
            #     temp_df.loc[len(temp_df)] = values
            #
            # temp_df.to_csv('data/pcy_test.csv',index=False)

    # print (data_result)
    # OutputCSV(data_result)
