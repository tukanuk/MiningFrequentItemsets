import re
import itertools
import sys
import csv
import time
import os
import pandas as pd
import numpy as np
from shutil import copyfile
from decorators import timer, debug, logTimer
import simplelogging


#Define all global variables

fileName='data/data.txt'
hashTable={}
bitVector={}
singletonIdx=0
pair=2
items={}
freqItems=[]
freqItemsCurItr=[]
# bucketSize=1000 # arg 3 bucket size
weight=0
itemCountDict={}
bitVector=[]
isPrint=False
isPrint2=False
bitMapSize=0

frequent_items=[]             # list of the frequent items 

candidatePair = {}

#Define all functions
def getVal(item,my_d):
    if item in my_d:
        return my_d[item]

# if not present in itemCountDict add to itemCountDict
def addWeights(itemCountDict, basket):
    global weight
    for item in basket:
        if item not in itemCountDict:
            itemCountDict[item] = weight
            weight += 1

# @logTimer
def updateHashTable(line, itemCountDict, size):
    global hashTable
    v1 = v2 = total = 0
    items = [list(x) for x in itertools.combinations(line, size)]
    # if isPrint==True:
    #     print ("UpdateHashTable")
    #     print (items)

    ####################################### HASH function
    for key in items:
        total = 0
        for item in key:
            v1=getVal(item,itemCountDict)            
            total+=v1
        total=total%bucketSize # actual hash function total % bucket size
        hashTable[total]+=1
    ####################################### HASH function
    # TODO How can we get a better hash?

# @logTimer
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

# @logTimer
def updateFreqItems(items):
    global freqItems
    freqItems.append(items)
    if isPrint==True:
        print ("FreqItems:")
        print (freqItems)

# @logTimer
def generateHashTable(size):
    global hashTable
    for i in range(size):
        hashTable[i] = 0

# @logTimer
def countCandidatesAndFillHashTable2(_pass, dataset):
    global items
    global itemCountDict  # Has weights for each item in the basket
    global freqItems
    # flag = False

    global candidatePair
    # weight = -1 # pretty sure this is unused 

    # ***Counting Candidates***#

    for basket in dataset:
        if (_pass==0):                    
            addWeights(itemCountDict,basket) # if not present in itemCountDict add to itemCountDict
            itemsInBasket = list(itertools.combinations(basket,_pass+1))
        
            for item in itemsInBasket:
                # first pass
                # items[item] += 1
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1
    
            updateHashTable(basket, itemCountDict, _pass + 2) # no hash table on second pass
        else:
            freqItemInBasket = []   # find the frequent items in this basket
            
            for item in basket:
                for s in freqItems: 
                   if item in s: 
                    freqItemInBasket.append(item)
            combination_freqItemInBasket = list(itertools.combinations(freqItemInBasket, _pass +1))
            
            for pair in combination_freqItemInBasket:
                total = 0
                for item in pair:
                    total += item
                hash = total % bucketSize
                if bitVector[hash] == 1:
                    if pair in candidatePair:
                        candidatePair[pair] +=1
                    else:
                        candidatePair[pair] = 1
                
    # print (candidatePair)

# @logTimer
def generateBitVector(min_val, max_val):
    global bitVector
    global bitMapSize
    bitVector = []
    flag = False
    # for i in range(bucketSize):
    #     if hashTable[i] >= support:
    #         bitVector.append(1)
    #         flag = True
    #     else:
    #         bitVector.append(0)
    # if isPrint==True:
    #     print ("BitVector:%d"%(flag))
    #     print (bitVector)
    # #print "bitmap size : %d"%(len(bitVector))
    # bitMapSize=len(bitVector)


    diff = (max_val - min_val)
    bitVector = np.zeros(diff, dtype=int)

    for val in hashTable:
        if hashTable[val] >= support:
            bitVector[val - min_val] = 1

    return flag

# @logTimer
def isNextPassPossible(_pass):
    global items
    global freqItemsCurItr
    global frequent_items
    bitVectorFlag = False
    frequent_items = generateFreqCandidates(items)  # list of frequent items
    bitVectorFlag = generateBitVector()             # TODO no bitvector on second pass
    if (len(freqItemsCurItr) > 0 and bitVectorFlag == True and _pass < 2):
        return True
    else:
        return False
    
# Outputting to a CSV 
# @logTimer
def OutputCSV(data_result):
    """ Takes a list as input and output as as CSV
        A check is made to see if if a file exists and a 
        numerical increment is added until a unique file name is made
    """ 
    inc = 0
    ffname = "data/pcy_results/pcy_result_t" + str(totalTestCount) + "_b" + str(bucketSize) + "_" + str(inc) + ".csv"

    # turn on and off auto file incrementer
    if(1):
        while os.path.isfile(ffname):
            inc += 1
            ffname = "data/pcy_results/pcy_result_t" + str(totalTestCount) + "_b" + str(bucketSize) + "_" + str(inc) + ".csv"

    with open(ffname, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for line in data_result:
            writer.writerow(line)
    
    # makes a copy with the _0 suffix so you can have an 
    # auto refresing csv of results open and retain past runs
    copyfile(ffname, "data/pcy_results/pcy_result_0.csv")


#Generating items-singletons
#def __main__():
if __name__ == '__main__':
    # global itemCountDict
    # global hash
    # cls()

    # data_lines = open(fileName).readlines()
    
    # simplelogger
    log = simplelogging.get_logger(console_level=-simplelogging.DEBUG, file_name="log/pcy_log.log", console=False)

    # Testing sets
    # chunk_percent = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    chunk_percent = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    thresholds = [0.01, 0.05, 0.1]

    log.debug("START debug session")
  

    # basket count
    data_lines = open(fileName).readlines()
    basket_count = len(data_lines)

    # calculate total number of tests
    totalTestCount = len(chunk_percent) * len(thresholds)
    testCount = 0

    # Output Run info to debug
    log.info("START param: %s (%d baskets)", fileName, basket_count)
  
    # Basic file info
    print ("\n%d Baskets" % (basket_count))
    print ("%d Tests\n" % (totalTestCount))
    print (" # %Thr Supp Chunk  Fre      Time   Buckets")

    # Setup for CSV
    data_result = []
    data_result_line = ["#", "threshold", "support", "chunk_size", "c_%", "buckets", "f_items", "time"]
    data_result.append(data_result_line)

    # Nested loops for test sets
    for threshold in thresholds:
        for percent in chunk_percent:

            # get line count for chunk
            chunk_size = int(basket_count * percent)

            #finding max value for bucket size
            max_val = 0

            # create chunked dataset
            dataset = []
            with open(fileName) as csvfile:
                reader = csv.reader(csvfile)
                for row in itertools.islice(reader, chunk_size + 1):
                    cells = [ int(i) for i in row[0].split(" ")[:-1] ]
                    dataset.append(cells)
                    if max_val < max(cells): # corrected ti < instead of !=
                        max_val = max(cells)

            # support threshold
            support = (threshold * chunk_size)
            # support = round(support)
            if round( support, 1) != int(support):  #If there is a round-off error it will be caught here
                #Try lowering the threshold to accomodate the require threshold as well
                support = (int(support) - 1)
            else:
                support = threshold
            # print ("Support %d" % (support))

            #bucket size is set to 2 times the sum of max in current chunk
            bucketSize = 2 * max_val
            # bucketSize = 53103
            
            log.info("SET: %d (%.2f) support, %d (%.2f) chunk ", support, threshold, chunk_size, percent)

            # reset variables for new test
            hashTable.clear()
            bitVector.clear()
            singletonIdx=0
            items.clear()
            freqItems.clear()
            freqItemsCurItr.clear()
            weight = 0
            itemCountDict.clear()
            bitMapSize = 0
            candidatePair.clear()

            start = time.time()  # Timer start

            _pass = 0
            size = 0
            while (_pass == 0 or isNextPassPossible(_pass) == True):
                # print "\nPASS : %d"%(_pass+1)
                items = {}
                generateHashTable(bucketSize) # TODO no point in gnerating table on second pass is there a .destroy?
                
                # countCandidatesAndFillHashTable(_pass)
                countCandidatesAndFillHashTable2(_pass, dataset)

                finalList = {}    
                # fillHashTable()
                if _pass != 0:
                    size = _pass - 1

                    # finalList = {}
                    total = 0

                    for pair in candidatePair:
                        if candidatePair[pair] > support:
                            finalList[pair] = candidatePair[pair]

                    # print ("%d frequent pairs: %s" % (len(finalList), finalList))

                _pass += 1
            
            testCount += 1
            end = time.time() # Timer stop

            # Build a list for use in CSV output
            data_result_line = [testCount, threshold, support, chunk_size, percent, bucketSize, len(finalList), (end-start)*1000]
            data_result.append(data_result_line)
            
            # detailed output with frequent pairs
            # print ("%2d %.2f %4d %5d %4d %9.1f %9d -> %d frequent item sets of size %d: %s" % (testCount, threshold, support, chunk_size, len(finalList), (end-start)*1000, bucketSize, len(finalList), _pass, finalList))
            
            # standard screen output
            print ("%2d %.2f %4d %5d %4d %9.1f %9d -> %d frequent item sets of size %d" % (testCount, threshold, support, chunk_size, len(finalList), (end-start)*1000, bucketSize, len(finalList), _pass))
            
            log.info("RESULT: [%d of %d] %d buckets: %.2f %4d %5d %4d %9.1f" % (testCount, totalTestCount, bucketSize, threshold, support, chunk_size, len(finalList), (end-start)*1000))

    # print (data_result)
    # OutputCSV(data_result)
