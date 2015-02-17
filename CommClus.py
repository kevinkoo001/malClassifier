__author__ = 'HEEYOUNG'

import csv
import numpy as np
import sklearn
import sys
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
import math

BASEDIR = "H:/Malware_Data/train"

def CV_RanFor(data, L, y):

    datal = data[0:L,:]

    model = RandomForestClassifier()
    param_grid = {"n_estimators": [3, 5, 7, 10], "max_depth": range(datal.shape[1]/2,datal.shape[1]), "min_samples_split": [1, 3, 7, 9]}
    grid_search = GridSearchCV(model, param_grid=param_grid)
    grid_search.fit(datal, y)

    return grid_search.best_params_


if __name__ == '__main__':

    TrainList = []
    with open('SampleTrain.csv', 'rb') as csvfile:  # Read Sample file, which has list of files and class
        reader = csv.reader(csvfile)
        for row in reader:
            TrainList.append(row)

    TestList = []
    with open('SampleTest.csv', 'rb') as csvfile:  # Read Sample file, which has list of files and class
        reader = csv.reader(csvfile)
        for row in reader:
            TestList.append(row)

    TrainList = np.array(TrainList)
    TestList = np.array(TestList)

    F_list = TrainList[:, 0]        # Get the list of file name
    #F_list = TestList[:, 0]
    nfeatures = 16**2 + 1        # For opcodes
    train = np.zeros((TrainList.shape[0], nfeatures), dtype = int)
    #train = np.zeros((TestList.shape[0], nfeatures), dtype = int)
    '''
    idx = -1
    for fname in F_list:
        idx += 1
        print fname
        with open(os.path.join(BASEDIR, fname)) as f:
            for line in f:
                token = line.split(' ')
                if not (token[0].startswith('.text') or token[0].startswith('.code') ):
                    continue
                if len(token) > 1:
                    if len(token[1]) == 2:
                        if token[1] == '??':
                            train[idx, -1] += 1
                        else:
                            train[idx, int(token[1], 16)] += 1
    print train

    np.savetxt('SampleTrainFeat.csv', train, delimiter=',')
    '''

    train = np.loadtxt('SampleTrainFeat.csv', delimiter=',')
    for i in range(train.shape[0]):
        S = np.sum(train[i, :])
        if S == 0:
            #print i
            continue
        train[i,:] = train[i,:]/S


    training_instances = train
    training_label = TrainList[:,1]

    L = len(training_instances)


    param = CV_RanFor(training_instances, L, training_label)
    model = RandomForestClassifier(min_samples_split=param['min_samples_split'], max_depth=param['max_depth'])
    model.fit(training_instances, training_label)

    test = np.loadtxt('SampleTestFeat.csv', delimiter=',')
    for i in range(test.shape[0]):
        S = np.sum(test[i, :])
        if S == 0:
            #print i
            continue
        test[i,:] = test[i,:]/S

    res = model.predict_proba(test)
    loss = 0
    for i in range(9):
        for j in range(i*20, (i+1)*20):
            if res[j,i] == 0:
                loss += math.log10(10**-15)
            else:
                loss += math.log10(res[j, i])
    print loss
    loss = -1*loss/180
    print loss
    '''
    kmeans = KMeans(init='k-means++', n_clusters=10, n_init=10)
    kmeans.fit(train)

    Dist = np.zeros((train.shape[0], len(kmeans.cluster_centers_)))
    for i in range(train.shape[0]):
        for j in range(len(kmeans.cluster_centers_)):
            Dist[i,j] = np.linalg.norm(kmeans.cluster_centers_[j] - train[i,:])


    for i in range(9):   # 0: 0~19, 1: 20~39, 2: 40~59
        for k in range(i*20, (i+1)*20):
            plt.figure(i+1)
            for j in range(Dist.shape[1]):
                plt.scatter(j+1, Dist[k,j])
            plt.title('Class: %d' %(i+1))

    plt.show()
    '''
    sys.exit()
