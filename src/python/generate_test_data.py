# Job Recommendation System
# RecSys Challenge 2016
#
# Description: This generates the test data descriptions
# that can be used to predict future interactions using
# the already built predictive models
#
# @author: Sonu Mishra
# @author: Manoj Reddy

import sys
import csv
import collections
# csv.field_size_limit(sys.maxsize)

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
for row in target_users_reader:
    target_users.add(row[0])

items_reader = csv.reader(open('../../data/training/items.csv'), delimiter='\t')
items_jobroles = {}
items_career_level = {}
items_discipline_id = {}
items_industry_id = {}
items_region = {}
items_country = {}
items_tags = {}
items_toe = {}

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
    items_toe[item_id] = row[9]
    items_tags[item_id] = row[10]
print('Finished reading the active_items.csv file')

impressions_reader = csv.reader(open('../../data/training/impressions.csv'), delimiter='\t')

user_map = {}  # It maps a user to a list of item impressions
count = 0
for row in impressions_reader:
    count += 1
    if count % 10000 == 0:
        print(count)
    if row[0] in target_users:
        if row[0] in user_map:
            user_map[row[0]] = user_map[row[0]] + ',' + row[3]
        else:
            user_map[row[0]] = row[3]

jobroles = {}
career_level = {}
discipline_id = {}
industry_id = {}
region = {}
country = {}
exp_entries = {}
exp_years = {}
exp_current = {}
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
        exp_entries[user_id] = row[7]
        exp_years[user_id] = row[8]
        exp_current[user_id] = row[9]
        edu_degree[user_id] = row[10]
print("Finished reading users.csv file")


interactions_map = {}  # Map between (user,item) pair and the value of the interaction 1, 2, 3
interactions_map_2 = {}  # Map between user and item
interactions_reader = csv.reader(open('../../data/training/interactions_sorted.csv'), delimiter=',')
next(interactions_reader)

for row in interactions_reader:
    # 0 - user_id, 1 - item_id, 2 - interaction_type, 3 - created_at
    if str(row[0]) in target_users and str(row[1]) in items_jobroles and row[2] != '4':
        if row[2] == '4':
            interactions_map[(row[0], row[1])] = -1
        else:
            interactions_map[(row[0], row[1])] = int(row[2])
            if row[0] in interactions_map_2:
                interactions_map_2[row[0]] = interactions_map_2[row[0]] + ',' + row[1]
            else:
                interactions_map_2[row[0]] = row[1]

num_errors = 0
count1 = 0
count2 = 0
count = 0
for user in user_map:
    item_list = user_map[user].split(',')
    count += 1
    if count % 1000 == 0:
        print(count)
    for item in item_list:
        if item not in items_jobroles:
            continue  # ignore non-active items
        if (user, item) not in interactions_map:
            interactions_map[(user, item)] = 0
            count1 += 1
        else:
            count2 += 1

f = open("../../data/master_test_data_1.csv", "w")
writer = csv.writer(f, lineterminator='\n')

total = 0
count = 0
error = 0
temp = 0
for user_item in interactions_map:
    total += 1
    if total % 10000 == 0:
        print(total)

    user = user_item[0]
    item = user_item[1]
    if item not in items_jobroles:
        continue
    p_interact = interactions_map[user_item]

    vec = []
    try:
        # vec.append(time_stamp)
        vec.append(user)
        vec.append(item)
        vec.append(p_interact)
        if career_level[user] == 'NULL':
            career_level[user] = ''
        vec.append(career_level[user])

        vec.append(discipline_id[user])
        vec.append(industry_id[user])
        vec.append(country[user])

        if region[user] == 'NULL':
            region[user] = ''
        vec.append((region[user]))

        if exp_entries[user] == 'NULL':
            exp_entries[user] = ''
        vec.append((exp_entries[user]))

        if exp_years[user] == 'NULL':
            exp_years[user] = ''
        vec.append((exp_years[user]))

        if exp_current[user] == 'NULL':
            exp_current[user] = ''
        vec.append((exp_current[user]))

        if edu_degree[user] == 'NULL':
            edu_degree[user] = ''
        vec.append((edu_degree[user]))

        vec.append((items_career_level[item]))
        vec.append((items_discipline_id[item]))
        vec.append((items_industry_id[item]))
        vec.append((items_region[item]))
        vec.append(items_country[item])

        vec.append(len(set(jobroles[user].split(',')).intersection(set(items_jobroles[item].split(',')))))
        vec.append(len(set(jobroles[user].split(',')).intersection(set(items_tags[item].split(',')))))

        if career_level[user] == items_career_level[item] and career_level[user] != '0':
            vec.append(1)
        else:
            vec.append(0)

        if discipline_id[user] == items_discipline_id[item]:
            vec.append(1)
        else:
            vec.append(0)

        if industry_id[user] == items_industry_id[item]:
            vec.append(1)
        else:
            vec.append(0)

        if region[user] == items_region[item] and region[user] != '0':
            vec.append(1)
        else:
            vec.append(0)

        if country[user] == items_country[item]:
            vec.append(1)
        else:
            vec.append(0)

        writer.writerow(vec)
        count += 1
    except:
        error += 1
print('Done generating test data.')
