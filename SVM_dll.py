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
    suffix = '(SVM)'
    train = np.loadtxt('../TrFeat.csv', delimiter=',', dtype=int)

    training_instances = train

    print "Read training labels"
    training_label = np.loadtxt('../TrLabel.csv', delimiter=',')

    print "Read features of test instances"
    test = np.loadtxt('../TtFeat.csv', delimiter=',', dtype=int)

    print "Training Sequence"
    #res, feat_importances = commonLib.RandomForest(training_instances, training_label, test)
    res, feat_importances = commonLib.KernelSVM(training_instances, training_label, test)
    np.savetxt('../Feat_importances'+suffix+'.csv', feat_importances, delimiter = ',')

    TestList = []
    with open('../TtID.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            TestList.append(row[0])

    commonLib.Export_TestResult('../Result'+suffix+'.csv', TestList, res)

    sys.exit()

