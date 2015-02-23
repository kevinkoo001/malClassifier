__author__ = 'HEEYOUNG'
'''
This script is for building the histogram of length of instructions in training files.

'''

import csv
import numpy as np
import sys
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import os
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.grid_search import GridSearchCV

client = MongoClient('localhost', 27017)
db = client.Malware
BASEDIR =  "H:/Malware_Data/"


def CV_RanFor(data, L, y):

    datal = data[0:L,:]

    model = RandomForestClassifier()
    param_grid = {"n_estimators": [7, 9, 11, 13], "max_depth": range(datal.shape[1]/2,datal.shape[1]), "min_samples_split": [1, 3, 7, 9]}
    grid_search = GridSearchCV(model, param_grid=param_grid, cv=10)
    grid_search.fit(datal, y)

    print "CV score:", grid_search.best_score_

    return grid_search.best_params_

if __name__ == '__main__':

    AB = db.AsmBytes
    ABT = db.AsmBytesTest
    TL = db.TrainLabels

    RawData = AB.find(timeout=False)

    train = np.zeros((RawData.count(), 16), dtype=float)
    label = np.zeros((RawData.count(), 1), dtype =int)
    idx = 0
    for d in RawData:
        for k in d.keys():
            if k == '_id' or k == 'Id':
                continue
            train[idx][int(k)-1] = d[k]
        l = TL.find_one({"Id":d['Id']})
        label[idx] = l['Class']
        idx += 1

    for i in range(train.shape[1]):
        S = np.sum(train[:, i])
        if S == 0:
            #print i
            continue
        train[:, i] = train[:, i]/S

    print train.shape, label.shape
    training_instances = train
    training_label = label[:, 0]

    L = len(training_instances)

    print "Training Random Forest with 10-fold Cross-validation"
    param = CV_RanFor(training_instances, L, training_label)
    model = RandomForestClassifier(min_samples_split=param['min_samples_split'], max_depth=param['max_depth'])
    model.fit(training_instances, training_label)

    np.savetxt('../Feat_importances_.csv', model.feature_importances_, delimiter = ',')

    testData = ABT.find(timeout=False)

    test = np.zeros((testData.count(), 16), dtype=float)
    TestList = []
    idx = 0
    for d in testData:
        for k in d.keys():
            if k == '_id':
                continue
            if k == 'Id':
                TestList.append(d[k])
                continue
            test[idx][int(k)-1] = d[k]
        idx += 1

    for i in range(test.shape[1]):
        S = np.sum(test[:, i])
        if S == 0:
            #print i
            continue
        test[:, i] = test[:, i]/S

    res = model.predict_proba(test)


    fout = open('../Result(length).csv', 'wb')
    writer = csv.writer(fout)
    header = ['Id']
    for i in range(9):
        header.append('Prediction'+str(i+1))
    writer.writerow(header)
    for i in range(len(TestList)):
        out = [TestList[i]]
        out.extend(res[i,:])
        writer.writerow(out)
    sys.exit()


