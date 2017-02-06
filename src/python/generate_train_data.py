# Job Recommendation System
# RecSys Challenge 2016
#
# Description: This generates the training data that can be 
# used to build predictive models in R
#
# @author: Sonu Mishra
# @author: Manoj Reddy

import sys
import csv
#csv.field_size_limit(sys.maxsize)

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
edu_fields = {}

user_reader = csv.reader(open('../../data/training/users.csv'), delimiter='\t')
next(user_reader)
for row in user_reader:
    user_id = row[0]
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
    edu_fields[user_id] = row[11]

items_jobroles = {}
items_career_level = {}
items_discipline_id = {}
items_industry_id = {}
items_region = {}
items_country = {}
items_tags = {}
items_toe = {}

items_reader = csv.reader(open('../../data/training/items.csv'), delimiter='\t')
next(items_reader)
for row in items_reader:
    item_id = row[0]
    items_jobroles[item_id] = row[1]
    items_career_level[item_id] = row[2]
    items_discipline_id[item_id] = row[3]
    items_industry_id[item_id] = row[4]
    items_country[item_id] = row[5]
    items_region[item_id] = row[6]
    items_toe[item_id] = row[9]
    items_tags[item_id] = row[10]

interactions_reader = csv.reader(open('../../data/training/interactions.csv'), delimiter='\t')
next(interactions_reader)
minT = 9444154047
maxT = 0
for row in interactions_reader:
    t = int(row[3])
    if t > maxT:
        maxT = t
    if t < minT:
        minT = t
midT = minT + (maxT - minT) * 0.6

interactions_reader = csv.reader(open('../../data/training/interactions_sorted.csv'), delimiter=',')
next(interactions_reader)
matrix = []
result = []
prev_interact = {}
total = 0
count = 0
error = 0
temp = 0
for row in interactions_reader:
    total += 1
    if total % 10000 == 0:
        print(total)

    user = row[0]
    item = row[1]
    key = (user, item)

    interaction_type = row[2]
    if (key not in prev_interact):
        p_interact = 0
    else:
        p_interact = prev_interact[key]
    prev_interact[key] = interaction_type

    time_stamp = int(row[3])
    if (time_stamp < midT):
        continue
    vec = []
    try:
        # vec.append(time_stamp)
        vec.append(p_interact)
        vec.append(int(career_level[user]))
        vec.append(int(discipline_id[user]))
        vec.append(int(industry_id[user]))
        vec.append(country[user])

        if region[user] == 'NULL':
            region[user] = -1
        vec.append(int(region[user]))

        vec.append(int(exp_entries[user]))
        vec.append(int(exp_years[user]))
        vec.append(int(exp_current[user]))
        vec.append(int(edu_degree[user]))
        
        vec.append(int(items_career_level[item]))
        vec.append(int(items_discipline_id[item]))
        vec.append(int(items_industry_id[item]))
        vec.append(int(items_region[item]))
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

        matrix.append(vec)

        if interaction_type == '4':
            result.append(-1)
        else:
            result.append(int(interaction_type))
        count += 1
        
    except:
        error += 1

print('saving data ...')

with open("../../data/training/trainingXforR.csv", "w") as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(matrix)

with open("../../data/training/trainingYforR.csv", "w") as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(result)
