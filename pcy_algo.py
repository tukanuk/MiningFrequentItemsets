import re
import itertools
import sys
import csv
import time
import os
import pandas as pd
import numpy as np
from shutil import copyfile
# from decorators import timer, debug, logTimer
# import simplelogging


#Define all macros
# fileName=sys.argv[1]        # arg 1 filename
fileName='data/data.txt'
hashTable={}
bitVector={}
singletonIdx=0
pair=2
items={}
freqItems=[]
freqItemsCurItr=[]
#support=int(sys.argv[2])    # arg 2 support threshold
# bucketSize=int(sys.argv[2]) # arg 3 bucket size
bucketSize=1000 # arg 3 bucket size
weight=0
my_dict={}
bitVector=[]
isPrint=False
isPrint2=False
bitMapSize=0

frequent_items=[]             # list of the frequent items 


#Define all functions
def getVal(item,my_d):
    if item in my_d:
        return my_d[item]


def addWeights(d, basket):
    global weight
    for item in basket:
        if item not in d:
            d[item] = weight
            weight += 1

# @logTimer
def updateHashTable(line, my_dict, size, max_val):
    global hashTable
    v1 = v2 = total = 0
    items = [list(x) for x in itertools.combinations(line, size)]
    # if isPrint==True:
    #     print ("UpdateHashTable")
    #     print (items)

    ####################################### HASH function
    # for key in items:
    #     total = 0
    #     for item in key:
    #         v1 = getVal(item,my_dict)
    #         total += v1
    #
    #     total = total % bucketSize # actual hash function total % bucket size
    #
    #     if isPrint==True:
    #         print ("%s - %d"%(key,total) )
    #     hashTable[total]+=1

    for pair in items:
        # total = ((pair[0]) + pair[1]) % bucketSize
        # if total == 19:
        #     print()
        # total = int(str(pair[0]) + str(pair[1]))

        total = pair[0] + pair[1] * max_val
        if total in hashTable:
            hashTable[total] += 1
        else:
            hashTable[total] = 1

        # hashIndex = int(((pair[0] + pair[1]) * (pair[0] + pair[1] + 1)) / 2) + pair[1]
        # if hashIndex in hashTable:
        #     hashTable[hashIndex] += 1
        # else:
        #     hashTable[hashIndex] = 1


    ####################################### HASH function
    # if I understand corrctly what is happening here the two values are added
    # then % bucket size. Doesn't this limit destination to the sum?
    # TODO How can we get a better hash?

# @logTimer
# def printMemSize(items,_pass):
#     if _pass==0:
#         print ("memory for item counts: %d"%((8+_pass*4)*len(items)))
#     else:
#         print ("memory for candidates counts of size %d : %d"%(_pass+1,(8+_pass*4)*(len(items))))

# @logTimer
# def printMemSizeHashTable(candidateType):
#     print ("memory for hash table counts for size %d itemsets: %d"%(candidateType,4*len(hashTable)))

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
# def printFreqItems(Idx):
#     global freqItems
#     print (freqItems[Idx])

# @logTimer
def generateHashTable(size):
    global hashTable
    for i in range(size):
        hashTable[i] = 0

# @logTimer
# def generateCandidates(candidates, _pass):
#     candidateItems = list(itertools.combinations(candidates, _pass + 1))
#     return candidateItems

# @logTimer
def countCandidatesAndFillHashTable(_pass):
    global items
    global my_dict  # Has weights for each item in the basket
    global freqItems
    flag = False
    weight = -1

    my_file = open(fileName, "r+")
    # ***Counting Candidates***#
    for line in my_file:
        line = re.sub(r'\n', "", line)
        basket = line.split(',')
        basket.sort()
        if (_pass==0):                    
            addWeights(my_dict,basket)
        #else:
            #print freqItems
            #candidateItems=generateCandidates(freqItems[0],_pass)
        itemsInBasket = list(itertools.combinations(basket,_pass+1))
        if isPrint==True:
            print (itemsInBasket)                    
        for item in itemsInBasket:
            if (_pass != 0):
                item_1 = list(itertools.combinations(item, _pass))
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
        updateHashTable(basket, my_dict, _pass + 2)
    my_file.close()

# @logTimer
def countCandidatesAndFillHashTable2(_pass, dataset, max_val):
    global items
    global my_dict  # Has weights for each item in the basket
    global freqItems
    flag = False
    weight = -1

    # ***Counting Candidates***#

    for basket in dataset:
        if (_pass==0):
            addWeights(my_dict,basket)
        
        # logTimerStart = time.time()
        itemsInBasket = list(itertools.combinations(basket,_pass+1))
        # logTimerEnd = time.time()
        # if ((logTimerEnd - logTimerStart) > 0.1): log.debug("Line 171: %f", (logTimerEnd-logTimerStart) )

        for item in itemsInBasket:
            if (_pass!=0):

                # logTimerStart = time.time()
                item_1=list(itertools.combinations(item,_pass))
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
    # if _pass > 1:
    #     print "frequent item sets of size %d : "%(_pass), "%d " % (len(frequent_items)), frequent_items
    bitVectorFlag = generateBitVector()
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
    ffname = "data/pcy_result_t" + str(totalTestCount) + "_b" + str(bucketSize) + "_" + str(inc) + ".csv"

    # turn on and off auto file incrementer
    if(1):
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


#Generating items-singletons
#def __main__():
if __name__ == '__main__':
    # global my_dict
    # global hash
    # cls()

    # data_lines = open(fileName).readlines()
    
    # simplelogger
    # log = simplelogging.get_logger(console_level=-simplelogging.DEBUG, file_name="log/pcy_log.log", console=False)

    # Testing sets
    # chunk_percent = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    chunk_percent = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    thresholds = [0.01] #0.01, 0.05, 0.1]

    # log.debug("START debug session")
    # log.info("some debug")
    # log.warning("some debug")
    # log.error("some debug")
    # log.critical("some debug")

    # basket count
    data_lines = open(fileName).readlines()
    basket_count = len(data_lines)

    # calculate total number of tests
    totalTestCount = len(chunk_percent) * len(thresholds)
    testCount = 0

    # Output Run info to debug
    # log.info("START param: %s (%d baskets) %d buckets", fileName, basket_count, bucketSize)
    # log.info("some debug")
    # log.warning("some debug")
    # log.error("some debug")
    # log.critical("some debug")

    # Basic file info
    # print ("\n%d Baskets" % (basket_count))
    # print ("%d Buckets" % (bucketSize))
    # print ("%d Tests\n" % (totalTestCount))
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


            #finding max value for bucket size
            max_val = 0

            # create chunked dataset
            dataset = []
            with open(fileName) as csvfile:
                reader = csv.reader(csvfile)
                for row in itertools.islice(reader, chunk_size + 1):
                    cells = [ int(i) for i in row[0].split(" ")[:-1] ]
                    dataset.append(cells)
                    if max_val != max(cells):
                        max_val = max(cells)

            # support threshold
            support = int(threshold * chunk_size)

            #bucket size is set to 2 times the sum of max in current chunk
            # bucketSize = int(str(max_val) + str(max_val))
            # da = len(my_dict)
            # bucketSize = int(pow(len(my_dict),2)/2)
            bucketSize = (max_val * 1000)
            # log.info("SET: %d (%.2f) support, %d (%.2f) chunk ", support, threshold, chunk_size, percent)

            start = time.time()  # Timer start

            _pass = 0
            size = 0
            # while (_pass == 0 or isNextPassPossible(_pass) == True):
            #     # print "\nPASS : %d"%(_pass+1)
            #     items = {}
            #     generateHashTable(bucketSize)
            #
            #     # countCandidatesAndFillHashTable(_pass)
            #     countCandidatesAndFillHashTable2(_pass, dataset)
            #
            #     # fillHashTable()
            #     if _pass != 0:
            #         size = _pass - 1
            #
            #     # if len(items)!=0:
            #     #     print
            #     _pass += 1

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
            data_result_line = [testCount, threshold, support, chunk_size, percent, len(frequent_pairs), (end-start)*1000]
            data_result.append(data_result_line)

            # print ("%2d %.2f %4d %5d %4d %9.3f" % (testCount, threshold, support, chunk_size, len(frequent_items), (end-start)*1000))
            print ("%2d %.2f %4d %5d %4d %9.3f" % (testCount, threshold, support, chunk_size, len(frequent_pairs), (end-start)*1000))
            #log.info("RESULT: [%d of %d] %.2f %4d %5d %4d %9.3f" % (testCount, totalTestCount, threshold, support, chunk_size, len(frequent_items), (end-start)*1000))

            # values = []
            # temp_df = pd.DataFrame( columns=['Keys', 'Support'])
            # for key in temp_frequent_pairs_print:
            #     values = [key, temp_frequent_pairs_print[key]]
            #     temp_df.loc[len(temp_df)] = values
            #
            # temp_df.to_csv('data/pcy_test.csv',index=False)

    # print (data_result)
    # OutputCSV(data_result)
