# Job Recommendation System
# RecSys Challenge 2016
#
# Description: This imputes the user-item interaction with the mean of values of
# the interactions the user had with other similar items. The notion of similarity
# used here is clustering. The job item falling in the same cluster are considered
# to be similar.
#
# @author: Sonu Mishra

from scipy.cluster.vq import vq, kmeans2
from scipy import *
import datetime
import csv
import numpy as np
import scipy.sparse.linalg

start_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
print(start_time)

num_users = 1500001
num_items = 1358098
num_tests = 150000
num_clusters = 1000

userid_to_index = {}
users_matrix = []
itemid_to_index = {}
items_matrix = []
clust_to_index = {}
test_user_id = []
test_user_index = []
interaction_matrix = scipy.sparse.lil_matrix((num_users, num_items))

print("Reading users_indicators.csv file ...")
users_rows = csv.reader(open('../../data/training/users_indicators.csv'), delimiter='\t')
next(users_rows)

print("Generating userid to index list ...")
user_counter = 0
for row in users_rows:
    userid_to_index[row[1]] = user_counter
    users_matrix.append(row)
    user_counter += 1
    if user_counter == num_users:
        break

print("Reading items_indicators.csv file ...")
items_rows = csv.reader(open('../../data/training/items_indicators.csv'), delimiter='\t')
next(items_rows)

print("Generating itemid to index list ...")
item_counter = 0
for row in items_rows:
    itemid_to_index[row[1]] = item_counter
    items_matrix.append(row)
    item_counter += 1
    if item_counter == num_items:
        break
index_to_items = {v: k for k, v in itemid_to_index.items()}

print("Generating items_matrix ...")
items_matrix_1 = np.array(items_matrix)
items_matrix_1[items_matrix_1 == ''] = '0'

print("Clustering items data ...")
centroids, item_clusts = kmeans2(np.delete(items_matrix_1, [0, 1, 2], 1).astype(float), num_clusters, minit='points')

print("Appending clusters to last column of items_matrix_1 ...")
items_with_clusters = np.concatenate((items_matrix_1, item_clusts.reshape(item_clusts.shape + (1,))), 1)

clust_to_items = scipy.sparse.lil_matrix((num_clusters, num_items))
for clust in range(0, num_clusters):
    items_in_clust = items_with_clusters[items_with_clusters[:, items_with_clusters.shape[1] - 1] == str(clust)][:, 1]
    for itemid in items_in_clust:
        clust_to_items[clust, itemid_to_index[itemid]] = 1
clust_to_items_1 = clust_to_items.tocsr()

item_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
print(item_time)

print("Reading interactions.csv file ...")
interactions_reader = csv.reader(open('../../data/training/interactions.csv'), delimiter='\t')
print("Generating a sparse users X items matrix for interaction ...")
num_lines_skipped = 0
next(interactions_reader)
num_matches = 0
for row in interactions_reader:
    if str(row[0]) in userid_to_index:
        num_matches += 1
        try:
            temp = float(row[2])
            if temp == 4.0:
                temp = -1.0
            interaction_matrix[userid_to_index[str(row[0])], itemid_to_index[str(row[1])]] = temp
        except:
            num_lines_skipped += 1

print(num_matches)
print(num_lines_skipped)
interaction_matrix_1 = interaction_matrix.tocsr()

intr_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
print(intr_time)

print("Reading target_users.csv file ...")
target_users_reader = csv.reader(open('../../data/target_users.csv'), delimiter='\t')
next(target_users_reader)
for row in target_users_reader:
    if str(row[0]) in userid_to_index:
        test_index = userid_to_index[str(row[0])]
        test_user_id.append(str(row[0]))
        test_user_index.append(test_index)

print("Opening similarity output file ...")
fpResult = open('../../data/CF_ItemItemSimilarity.csv', 'w')

print("Generating new interaction vectors ...")
beta = interaction_matrix_1[test_user_index, :]

num_row = 0
for test_userid in test_user_id:
    num_items_written = 0
    test_index = userid_to_index[test_userid]
    beta = interaction_matrix_1[test_index, :]
    num_row += 1
    if num_row % 1000 == 0:
        print(num_row)

    alpha_z = []
    for clust in range (0, num_clusters):
        alpha = clust_to_items_1[clust, :]
        alpha_beta = beta.multiply(alpha)
        sum_row = alpha_beta.sum(1)[0, 0]
        num_nonzero = alpha_beta.nonzero()[1].__len__() + 0.001
        to_impute = sum_row/num_nonzero
        Z = np.repeat(to_impute, beta.shape[1])
        alpha_z = alpha.multiply(Z)
        idx = beta.nonzero()
        alpha_z[idx] = beta.data
    jobs_score = alpha_z.tolist()
    final_vector = np.argsort(jobs_score)[:, ::-1]

    tobeWritten = str(test_userid) + '\t'
    for item_index in final_vector[0]:
        item_id = index_to_items[int(item_index)]
        if items_with_clusters[int(item_index), 5] == str(1) and beta[0, item_index] != -1 and beta[0, item_index] != 3:
            tobeWritten += str(item_id)
            num_items_written += 1
            if num_items_written > 30:
                break
            tobeWritten += ','
    fpResult.write(tobeWritten + '\n')

end2_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
print(end2_time)