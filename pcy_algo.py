import re
import itertools
import sys
import csv
import time

#Reference: Nandan Nayak's github post on Finding Frequent Itemsets:
#Url: https://github.com/NandanNayak/Finding-Frequent-Item-Sets


# Define all macros
fileName = sys.argv[1]  # arg 1 filename
hashTable = {}
bitVector = {}
singletonIdx = 0
pair = 2
items = {}
freqItems = []
freqItemsCurItr = []
support = int(sys.argv[2])  # arg 2 support threshold
bucketSize = int(sys.argv[3])  # arg 3 bucket size
weight = 0
my_dict = {}
bitVector = []
isPrint = False
isPrint2 = False
bitMapSize = 0

frequent_items = []  # list of the frequent items


# Define all functions
def getVal(item, my_d):
    if item in my_d:
        return my_d[item]


def addWeights(d, basket):
    global weight
    for item in basket:
        if item not in d:
            d[item] = weight
            weight += 1


def updateHashTable(line, my_dict, size):
    global hashTable
    v1 = v2 = total = 0
    items = [list(x) for x in itertools.combinations(line, size)]
    if isPrint == True:
        print("UpdateHashTable")
        print(items)

    ####################################### HASH function
    for key in items:
        total = 0
        for item in key:
            v1 = getVal(item, my_dict)
            total += v1
        total = total % bucketSize  # actual hash function total % bucket size
        if isPrint == True:
            print("%s - %d" % (key, total))
        hashTable[total] += 1
    ####################################### HASH function
    # if I understand corrctly what is happening here the two values are added
    # then % bucket size. Doesn't this limit destination to the sum?
    # TODO How can we get a better hash?


def printMemSize(items, _pass):
    if _pass == 0:
        print("memory for item counts: %d" % ((8 + _pass * 4) * len(items)))
    else:
        print("memory for candidates counts of size %d : %d" % (_pass + 1, (8 + _pass * 4) * (len(items))))


def printMemSizeHashTable(candidateType):
    print("memory for hash table counts for size %d itemsets: %d" % (candidateType, 4 * len(hashTable)))


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
        temp.append(list(tuples))
    freqItemsCurItr = temp

    return freqItemsCurItr


def updateFreqItems(items):
    global freqItems
    freqItems.append(items)
    if isPrint == True:
        print("FreqItems:")
        print(freqItems)


def printFreqItems(Idx):
    global freqItems
    print(freqItems[Idx])


def generateHashTable(size):
    global hashTable
    for i in range(size):
        hashTable[i] = 0


def generateCandidates(candidates, _pass):
    candidateItems = list(itertools.combinations(candidates, _pass + 1))
    return candidateItems


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
        if (_pass == 0):
            addWeights(my_dict, basket)
        # else:
        # print freqItems
        # candidateItems=generateCandidates(freqItems[0],_pass)
        itemsInBasket = list(itertools.combinations(basket, _pass + 1))
        if isPrint == True:
            print(itemsInBasket)
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


def countCandidatesAndFillHashTable2(_pass, dataset):
    global items
    global my_dict  # Has weights for each item in the basket
    global freqItems
    flag = False
    weight = -1

    # ***Counting Candidates***#

    for basket in dataset:
        if (_pass == 0):
            addWeights(my_dict, basket)
        itemsInBasket = list(itertools.combinations(basket, _pass + 1))
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
        # my_file.close()


def generateBitVector():
    global bitVector
    global bitMapSize
    bitVector = []
    flag = False
    for i in range(bucketSize):
        if hashTable[i] >= support:
            bitVector.append(1)
            flag = True
        else:
            bitVector.append(0)
    if isPrint == True:
        print("BitVector:%d" % (flag))
        print(bitVector)
    # print "bitmap size : %d"%(len(bitVector))
    bitMapSize = len(bitVector)
    return flag


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


# Generating items-singletons
# def __main__():
if __name__ == '__main__':
    # global my_dict
    # global hash
    # cls()

    # data_lines = open(fileName).readlines()

    chunk_percent = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    thresholds = [0.01, 0.05, 0.1]

    # basket count
    data_lines = open(fileName).readlines()
    basket_count = len(data_lines)

    print("%d Baskets" % (basket_count))
    print("%d Buckets" % (bucketSize))
    print("%Thr Supp Chunk  Fre      Time")

    for threshold in thresholds:
        for percent in chunk_percent:

            # get line count for chunk
            chunk_size = int(basket_count * percent)

            # for entry in data_lines[: (chunk_size + 1)]:
            #     cells = []
            #     cells = entry.split(",")
            #     dataset.append(cells[:-1])

            # create chunked dataset
            dataset = []
            with open(fileName) as csvfile:
                reader = csv.reader(csvfile)
                for row in itertools.islice(reader, chunk_size + 1):
                    dataset.append(row)

            # override arg for support
            support = int(threshold * chunk_size)

            start = time.time()  # Timer stop

            _pass = 0
            size = 0
            while (_pass == 0 or isNextPassPossible(_pass) == True):
                # print "\nPASS : %d"%(_pass+1)
                items = {}
                generateHashTable(bucketSize)
                # countCandidatesAndFillHashTable(_pass)
                countCandidatesAndFillHashTable2(_pass, dataset)
                # fillHashTable()
                if _pass != 0:
                    size = _pass - 1

                # if len(items)!=0:
                #     print
                _pass += 1

            end = time.time()  # Timer stop

            print(
                "%.2f %4d %5d %4d %9.3f" % (threshold, support, chunk_size, len(frequent_items), (end - start) * 1000))

    
    
