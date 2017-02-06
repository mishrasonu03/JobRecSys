# Job Recommendation System
# RecSys Challenge 2016
#
# Description: This recommends the jobs to the old 132K test
# users who are present in interactions or impressions data
#
# @author: Sonu Mishra
# @author: Manoj Reddy

import sys
import csv
import collections

maxInt = sys.maxsize
decrement = True
while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True
csv.field_size_limit(maxInt)

est_interact_reader = csv.reader(open('../../data/op_gbM.csv'), delimiter=',')
est_interact__map_1 = {}  # Map between (user,item) pair and the value of the estimated action 1, 2, 3
est_interact__map_2 = {}  # Map between user and item

next(est_interact_reader)
for row in est_interact_reader:
    # 0 - user_id, 1 - item_id, 2 - interaction_type
    est_interact__map_1[(row[0], row[1])] = float(row[2])
    if row[0] in est_interact__map_2:
        est_interact__map_2[row[0]] = est_interact__map_2[row[0]] + ',' + row[1]
    else:
        est_interact__map_2[row[0]] = row[1]

def score(user, counter):
    new_map = {}
    for item in counter:
        int_score = est_interact__map_1[(user, item)]
        new_map[item] = int_score
    return sorted(new_map.keys(), key=lambda x: new_map[x], reverse=True)[:50]

output_file = open('../../data/gbm_132K.txt', 'w')
output_file.write('user_id\titems\n')
num_errors = 0
for user in est_interact__map_2:
    temp = est_interact__map_2[user].split(',')
    counter = collections.Counter(temp)
    result = score(user, counter)
    output_file.write(user + '\t' + ','.join(result) + '\n')

output_file.close()