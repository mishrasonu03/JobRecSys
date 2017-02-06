# Job Recommendation System
# RecSys Challenge 2016
#
# Description: This recommends the jobs to the new 18K test
# users who are not present in interactions and impressions data
#
# @author: Sonu Mishra
# @author: Manoj Reddy

import sys
import csv

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

target_users = set()
target_users_reader = csv.reader(open('../../data/target_users.csv'), delimiter='\t')
next(target_users_reader)
for row in target_users_reader:
    target_users.add(row[0])

output_reader = csv.reader(open('../../data/gbm_132K.txt'), delimiter='\t')
next(output_reader)
already_processed = set()
for row in output_reader:
    already_processed.add(row[0])

users_to_recommend = target_users.difference(already_processed)

jobroles = {}
career_level = {}
discipline_id = {}
industry_id = {}
country = {}
region = {}
experience_n_entries = {}
total_experience = {}
current_experience = {}
edu_degree = {}

users_reader = csv.reader(open('../../data/training/users.csv'), delimiter='\t')
next(users_reader)
for row in users_reader:
    user_id = row[0]
    if user_id in target_users:
        jobroles[user_id] = row[1]
        career_level[user_id] = row[2]
        discipline_id[user_id] = row[3]
        industry_id[user_id] = row[4]
        country[user_id] = row[5]
        region[user_id] = row[6]
        experience_n_entries[user_id] = row[7]
        total_experience[user_id] = row[8]
        current_experience[user_id] = row[9]
        edu_degree[user_id] = row[10]
print("Finished reading users.csv file")

items_reader = csv.reader(open('../../data/training/items.csv'), delimiter='\t')
items_jobroles = {}
items_career_level = {}
items_discipline_id = {}
items_industry_id = {}
items_region = {}
items_country = {}
items_employment = {}
items_tags = {}

for row in items_reader:
    if row[12] != '1':
        continue
    item_id = row[0]
    items_jobroles[item_id] = row[1]
    items_career_level[item_id] = row[2]
    items_discipline_id[item_id] = row[3]
    items_industry_id[item_id] = row[4]
    items_country[item_id] = row[5]
    items_region[item_id] = row[6]
    items_employment[item_id] = row[9]
    items_tags[item_id] = row[10]
print('Finished reading the items.csv file')

interactions_reader = csv.reader(open('../../data/training/interactions_sorted.csv'), delimiter=',')
next(interactions_reader)
item_map = {}
for row in interactions_reader:
    # 0 - user_id, 1 - item_id, 2 - interaction_type, 3 - created_at
    item_id = row[1]
    interaction = int(row[2])
    if interaction == 4:
        interaction = -1
    if item_id in item_map:
        item_map[item_id] += interaction
    else:
        item_map[item_id] = interaction

_132K_reader = csv.reader(open('../../data/op_gbM.csv'), delimiter=',')
next(_132K_reader)
for row in interactions_reader:
    # 0 - user_id, 1 - item_id, 2 - interaction_type
    item_id = row[1]
    interaction = int(row[2])
    if interaction == 4:
        interaction = -1
    if item_id in item_map:
        item_map[item_id] += interaction
    else:
        item_map[item_id] = interaction

sorted_items = sorted(item_map.keys(), key=lambda x: item_map[x], reverse=True)

output_write = open('../data/heuristic_18K.txt', 'w')
still_remaining = set()
count = 0
for user in users_to_recommend:
    added_so_far = 0
    count += 1
    if count % 100 == 0:
        print(count)
    store = ""
    for item in sorted_items:
        if item in items_jobroles:
            if added_so_far > 30:
                break
            temp1 = set(items_jobroles[item].split(','))
            temp2 = set(jobroles[user].split(','))
            if (len(temp1.intersection(temp2)) > 0 or
                    (discipline_id[user] == items_discipline_id[item] and
                        (career_level[user] == 'NULL' or items_career_level[item] == '' or
                            -1 < (int(career_level[user]) - int(items_career_level[item]))) < 1)) and \
                    (country[user] == items_country[item]):
                added_so_far += 1
                store += item + ','
    if added_so_far > 0:
        output_write.write(user + '\t' + store + '\n')
    else:
        still_remaining.add(user)

output_write.close()
