import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

data_lines = open('data/data.txt').readlines()

dataset = []
for entry in data_lines:
    cells = []
    cells = entry.split(" ")
    dataset.append(cells[:-1])

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)

df = pd.DataFrame(te_ary, columns=te.columns_)

frequent_items = apriori(df, min_support=0.05, use_colnames=True)

print(frequent_items)



