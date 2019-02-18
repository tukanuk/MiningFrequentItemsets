import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import time
from decorators import debug, timer, repeat

@debug
@timer
def ap():
    data_lines = open('data/data.txt').readlines()
    # data_lines = open('retail.txt').readlines()

    dataset = []
    for entry in data_lines:
        cells = []
        cells = entry.split(" ")
        dataset.append(cells[:-1])

    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)

    df = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_items = apriori(df, min_support=0.01, use_colnames=True, max_len=2 )

    print(frequent_items)

if __name__ == "__main__":
    ap()