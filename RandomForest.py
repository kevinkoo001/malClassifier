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
import commonLib

#client = MongoClient('localhost', 27017)
#db = client.Malware

BASEDIR = "H:/Malware_Data/"



if __name__ == '__main__':

    print "Read features of training instances"
    suffix = '(Sample+RF)'
    train = np.loadtxt('../TrFeat(sample).csv', delimiter=',', dtype=float)
    S = np.sum(train[:,0])
    train[:, 0] = train[:, 0]/S

    training_instances = train

    print "Read training labels"
    training_label = np.loadtxt('../TrLabel(sample).csv', delimiter=',')

    '''
    print "Read features of test instances"
    test = np.loadtxt('../TtFeat.csv', delimiter=',', dtype=int)
    '''
    print "Training Sequence"
    res, feat_importances = commonLib.RandomForest(training_instances, training_label, [])
    np.savetxt('../Feat_importances'+suffix+'.csv', feat_importances, delimiter = ',')

    '''
    result = np.zeros((test.shape[0], 9), dtype=float)
    for i in range(1, 10):
        print "Class", i
        label = np.ones((training_label.shape))*(-1)
        label[training_label[:] == i] = 1
        res = commonLib.KernelSVM(training_instances, label, test)
        print res.shape
        result[:, i-1] = res[:, 1]

    for i in range(result.shape[0]):
        result[i,:] = result[i,:]/np.sum(result[i, :])


    TestList = []
    with open('../TtID.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            TestList.append(row[0])

    commonLib.Export_TestResult('../Result'+suffix+'.csv', TestList, res)
    '''
    sys.exit()

