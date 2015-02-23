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
import string
from pymongo import MongoClient

#client = MongoClient('localhost', 27017)
#db = client.Malware

BASEDIR = "H:/Malware_Data/"

def CV_RanFor(data, L, y):

    datal = data[0:L,:]

    model = RandomForestClassifier()
    param_grid = {"n_estimators": [7, 10, 11, 13, 15], "max_depth": range(datal.shape[1]/2,datal.shape[1]), "min_samples_split": [1, 3, 7, 9]}
    grid_search = GridSearchCV(model, param_grid=param_grid, cv=10)
    grid_search.fit(datal, y)

    print "CV score:", grid_search.best_score_

    return grid_search.best_params_

if __name__ == '__main__':

    train = np.loadtxt('../TrFeat(Comm+Length).csv', delimiter=',', dtype=float)

    for i in range(train.shape[1]):
        S = np.sum(train[:, i])
        if S == 0:
            #print i
            continue
        train[:, i] = train[:, i]/S

    training_instances = train

    training_label = np.loadtxt('../TrLabel(Comm+Length).csv', delimiter=',')

    L = len(training_instances)

    print "Training Random Forest with 10-fold Cross-validation"
    param = CV_RanFor(training_instances, L, training_label)
    model = RandomForestClassifier(min_samples_split=param['min_samples_split'], max_depth=param['max_depth'])
    model.fit(training_instances, training_label)

    np.savetxt('../Feat_importances(Comm+Length).csv', model.feature_importances_, delimiter = ',')

    print "Read Test features and normalize..."

    test = np.loadtxt('../TtFeat(Comm+Length).csv', delimiter=',', dtype=float)

    for i in range(test.shape[1]):
        S = np.sum(test[:, i])
        if S == 0:
            #print i
            continue
        test[:, i] = test[:, i]/S

    res = model.predict_proba(test)

    TestList = []
    with open('../TtID(Comm+Length).csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            TestList.append(row[0])

    fout = open('../Result(Comm+Length).csv', 'wb')
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

