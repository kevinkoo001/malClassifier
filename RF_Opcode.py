__author__ = 'HEEYOUNG'

import csv
import numpy as np
import sys
from os import listdir
from os.path import isfile, join
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
import math
from sklearn.externals import joblib

BASEDIR = "H:/Malware_Data/"

def Read_Data(dir, F_List):

    idx = -1
    nFeatures = 16**2 + 1        # For opcodes
    buf = np.zeros((len(F_List), nFeatures), dtype = float)
    print "Total: ", len(F_List), "files"
    for fname in F_List:
        idx += 1
        if idx % 100 == 0 and idx != 0:
            print 100*float(idx)/len(F_List), "% is done"
        with open(os.path.join(BASEDIR+dir, fname)) as f:
            for line in f:
                token = line.replace("\n", '')
                token = token.replace("\t", ' ')
                token = token.split(' ')
                token = filter(None, token) # fastest
                if not (token[0].startswith('.text') or token[0].startswith('.rdata')):
                    continue
                print token
                if len(token) > 1:
                    if len(token[1]) != 2:
                        continue
                    if token[1] == '??':
                        buf[idx, -1] += 1
                    else:
                        try:
                            buf[idx, int(token[1], 16)] += 1
                        except:
                            print fname
                            print token
                            sys.exit()
    return buf

def CV_RanFor(data, L, y):

    datal = data[0:L,:]

    model = RandomForestClassifier()
    param_grid = {"n_estimators": [3, 5, 7, 10], "max_depth": range(datal.shape[1]/2,datal.shape[1]), "min_samples_split": [1, 3, 7, 9]}
    grid_search = GridSearchCV(model, param_grid=param_grid)
    grid_search.fit(datal, y)

    print grid_search.best_score_
    return grid_search.best_params_

if __name__ == '__main__':

    TrainList = []
    TestList = [ f for f in listdir(BASEDIR+'test') if f.endswith('.asm') ]

    with open('trainLabels.csv', 'rb') as csvfile:  # Read Sample file, which has list of files and class
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            row[0] = row[0] + '.asm'
            TrainList.append(row)

    TrainList = np.array(TrainList)

    '''
    print "Read Training Data and Extract features..."
    train = Read_Data("train", TrainList[:, 0])        # Read and get features of training data
    for i in range(train.shape[0]):
        S = np.sum(train[i, :])
        if S == 0:
            continue
        train[i,:] = train[i,:]/S

    np.savetxt('SampleTrainFeat(text+rdata).csv', train, delimiter=',')  # Save features of training data
    '''

    train = np.loadtxt('SampleTrainFeat.csv', delimiter=',')
    print train
    training_instances = train
    training_label = TrainList[:,1]

    L = len(training_instances)

    print "Training Random Forest with 5-fold Cross-validation"
    param = CV_RanFor(training_instances, L, training_label)
    model = RandomForestClassifier(min_samples_split=param['min_samples_split'], max_depth=param['max_depth'])
    model.fit(training_instances, training_label)
    sys.exit()
    '''
    print "Read Test data and Extract features..."
    test = Read_Data("test", TestList)

    for i in range(test.shape[0]):
        S = np.sum(test[i, :])
        if S == 0:
            #print i
            continue
        test[i,:] = test[i,:]/S

    np.savetxt('SampleTestFeat.csv', test, delimiter=',')  # Save features of training data
    '''

    test = np.loadtxt('SampleTestFeat.csv', delimiter=',')
    res = model.predict_proba(test)

    fout = open('Result.csv', 'wb')
    writer = csv.writer(fout)
    header = ['Id']
    for i in range(9):
        header.append('Prediction'+str(i+1))
    writer.writerow(header)
    for i in range(len(TestList)):
        out = [TestList[i][:-4]]
        out.extend(res[i,:])
        writer.writerow(out)


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

