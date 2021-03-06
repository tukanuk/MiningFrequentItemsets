import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import time
import numpy as np

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

    result_df = pd.DataFrame(columns=['#','Threshold','Support','Chunk Size','Frequent Set Count','Run Time'])

    #Dataframe used only when frequent item sets have to be displayed/printed
    # frequent_sets = pd.DataFrame(columns=['Threshold','Chunk Size','Frequent Set'])

    print(" # Thr Support Chunk Count(F.Set) RunTime")

    for threshold in thresholds:
        for iteration,percent in enumerate(chunk_percent):
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

            #Additional measures to ensure that all itemsets and above are considered
            #Note: Previous version was ignoring min support and only considering above support values
            #Note: Round to 1 decimal because round to 0 seems to be skipping some values again.
            min_support = threshold * chunk_size
            if round( min_support, 1) != int(min_support):  #If there is a round-off error it will be caught here
                #Try lowering the threshold to accomodate the require threshold as well
                min_support = (int(min_support) - 1)/chunk_size
            else:
                min_support = threshold

            #Max len implemented to improve performance and runtime
            frequent_items = apriori(df, min_support=min_support, use_colnames=True, max_len=2)        #threshold

            #Pick sets with only two items in them
            frequent_items['length'] = frequent_items['itemsets'].apply(lambda iset : len(iset))
            frequent_items = frequent_items[(frequent_items['length']) == 2]

            end = time.time()  # Timer stopped

            print("%2d %3d %7d %5d %12d %.3f" % (iteration + 1, int(threshold * 100), int(threshold * chunk_size),
                                                 chunk_size, len(frequent_items.index), ((end - start) * 1000)))

            #This section is for printing the frequent item sets generated per iteration

            #Convert and sort frozensets to tuples for the final records
            # frequent_items['itemsets'] = [tuple((int(tuple(x)[0]), int(tuple(x)[1])))
            #                                                for x in frequent_items['itemsets']]
            # frequent_items['itemsets'] = [tuple(sorted(x)) for x in frequent_items['itemsets']]
            # frequent_items = frequent_items.sort_values(by=['itemsets'])
            #
            # frequent_set_stack = np.column_stack ([ [int(threshold * 100)] * len(frequent_items['itemsets']),
            #                                         [chunk_size] * len(frequent_items['itemsets']),
            #                                         frequent_items['itemsets'] ])

            #Experimentation for comparison with PCY
            # frequent_set_stack = np.column_stack ([ frequent_items['supqport'],
            #                                         [chunk_size] * len(frequent_items['itemsets']),
            #                                         frequent_items['itemsets'] ])

            # frequent_sets_temp = pd.DataFrame(frequent_set_stack,columns=['Threshold','Chunk Size','Frequent Set'])
            # frequent_sets = pd.concat([frequent_sets,frequent_sets_temp])

            #Creating the final result table
            result_list = [iteration + 1, int(threshold * 100), int(threshold * chunk_size), chunk_size,
                           len(frequent_items.index), (end - start) * 1000]
            result_df.loc[len(result_df)] = result_list

    result_df.to_csv('data/apriori_result.csv', index=False)

    #Uncomment to see the sets for a particualr threshold and chunck
    # writer = pd.ExcelWriter('data/apriori_result.xlsx',engine='xlsxwriter')
    # result_df.to_excel(writer,sheet_name='Result', index=False)
    # frequent_sets.to_excel(writer,sheet_name='Sets', index=False)
    # writer.save()

if __name__ == "__main__":
    alg()
