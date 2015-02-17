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

client = MongoClient('localhost', 27017)
db = client.Malware

BASEDIR = "H:/Malware_Data/"

def Read_Data(dir, F_List):

    idx = 0
    print "Total: ", len(F_List), "files"
    for fname in F_List:
        idx += 1
        Data = {}
        if AC.find_one({"Id":fname[:-4]}):
            continue
        Data['Id'] = fname[:-4]
        if idx % 100 == 0 and idx != 0:
            print 100*float(idx)/len(F_List), "% is done"
        with open(os.path.join(BASEDIR+dir, fname)) as f:
            for line in f:
                token = line.replace("\n", '')
                token = token.replace("\t", ' ')
                token = token.replace("+", '')
                token = token.split(' ')
                token = filter(None, token) # fastest
                if not (token[0].startswith('.text')):
                    continue
                if len(token) > 1:
                    if not all(c in string.hexdigits for c in token[1]):
                        continue
                    for i in range(1, len(token)):
                        if len(token[i])>5:
                            continue
                        if all(c in string.lowercase for c in token[i]):
                            if token[i] in Data.keys():
                                Data[token[i]] += 1
                            else:
                                Data[token[i]] = 1
                            break
            AC.insert(Data)

def CV_RanFor(data, L, y):

    datal = data[0:L,:]

    model = RandomForestClassifier()
    param_grid = {"n_estimators": [3, 5, 7, 10], "max_depth": range(datal.shape[1]/2,datal.shape[1]), "min_samples_split": [1, 3, 7, 9]}
    grid_search = GridSearchCV(model, param_grid=param_grid)
    grid_search.fit(datal, y)

    return grid_search.best_params_

if __name__ == '__main__':

    AC = db.AssemCntTest

    TrainList = []
    TestList = [ f for f in listdir(BASEDIR+'test') if f.endswith('.asm') ]

    print "Read Test data and Extract features..."
    test = Read_Data("test", TestList)
    sys.exit()

