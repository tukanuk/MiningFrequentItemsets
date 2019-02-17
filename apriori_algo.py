import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import time

# For enhancement

# def print_timing(func):
#     def wrapper(*arg):
#         t1 = time.time()
#         res = func(*arg)
#         t2 = time.time()
#         print ("%s took %0.3f ms" % (func.__name__ , (t2-t1)*1000.0))
#         return res
#     return wrapper

# @print_timing
def alg():

    data_lines = open('data/data.txt').readlines()

    chunk_percent = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    thresholds = [0.01, 0.05, 0.1]
    # thresholds = [0.05]

    result_df = pd.DataFrame(columns=['Threshold','Frequent Set Count','Execution Time','Chunk Size',
                                                                                    'Chunk Percent'])

    for threshold in thresholds:
        for percent in chunk_percent:
            # format data as a list of list for next step
            dataset = []
            chunk_size = int(len(data_lines) * percent)

            for entry in data_lines[: (chunk_size + 1)]:
                cells = []
                cells = entry.split(" ")
                dataset.append(cells[:-1])

            start = time.time() #Timer started

            #Encode each item in a transaction to True if item exist else false in a transaction
            te = TransactionEncoder()
            te_table = te.fit(dataset).transform(dataset)

            df = pd.DataFrame(te_table, columns=te.columns_)

            frequent_items = apriori(df, min_support=threshold, use_colnames=True, max_len=2)

            #Pick sets with only two items in them
            frequent_items['length'] = frequent_items['itemsets'].apply(lambda iset : len(iset))
            frequent_items = frequent_items[(frequent_items['length']) == 2]

            end = time.time()   #Timer stopped

            result_list = [int(threshold * 100),len(frequent_items.index), (end - start) * 1000,
                                                                    chunk_size, int(percent * 100)]
            result_df.loc[len(result_df)] = result_list

            print("%d %d %.3f %d" % (int(threshold * 100), len(frequent_items.index) , ((end - start) * 1000), chunk_size))


    result_df.to_csv('data/apriori_result_3.csv', index=False)

if __name__ == "__main__":
    alg()