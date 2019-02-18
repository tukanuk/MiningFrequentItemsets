import csv
import os

def OutputCSV():
    inc = 0
    ffname = "data/pcy_result_" + str(inc) + ".csv"
    while os.path.isfile(ffname):
        inc += 1
        ffname = "data/pcy_result_" + str(inc) + ".csv"

    with open(ffname, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for line in data_result:
            writer.writerow(line)
