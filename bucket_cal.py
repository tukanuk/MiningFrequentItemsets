
lineCount = 0
highestNumber = 0
bucket = 50000
frequency_threshold = [0.01, 0.05, 0.10]
s_frequency_threshold = []
b_hash_buckets = []

f = open(r'Data-Mining-PCY/data.txt') #.readlines()
data = f.read()        
f.close()

item_count = len(data.split(" "))           # words in file (item count)
t_basket_count = len(data.split("\n"))      # lines in file (basket count)
avg_item_count = item_count / t_basket_count  # avg basket size   

# approximate number of possible pairs
possible_pairs = (t_basket_count * (avg_item_count * (avg_item_count -1))) / 2

# for bucket the avg size of the bucket
avg_bucket_count = (t_basket_count * avg_item_count ** 2) / (2 * bucket)

print ("Lines: %d Items: %d Avg: %.2f" % (t_basket_count, item_count, avg_item_count))
print ("Possible pairs: %d" % (possible_pairs))
print ("Avg Bucket Count: %d with %d buckets" % (avg_bucket_count, bucket))
print ("Largest value: %d\n" % (highestNumber))

# optimize the number of buckets

for threshold in frequency_threshold:
    s_frequency_threshold.append(threshold * t_basket_count )
    b_hash_buckets.append( 10 * (t_basket_count * avg_item_count ** 2) / (2 * s_frequency_threshold[-1]) )
    print ("At %.2f support threshold is %d baskets, try at least %d buckets" % (threshold, s_frequency_threshold[-1], b_hash_buckets[-1]))
    
print()
