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
        if CI.find_one({"Id":fname[:-4]}):
            continue
        Data['Id'] = fname[:-4]
        if idx % 100 == 0 and idx != 0:
            print 100*float(idx)/len(F_List), "% is done"
        with open(os.path.join(BASEDIR+dir, fname)) as f:
            for line in f:
                token = line.replace("\n", '')          # delete unnecessary characters
                token = token.replace("\t", ' ')
                token = token.replace("+", '')
                token = token.split(' ')
                token = filter(None, token)             # delete empty items in the token list
                if not (token[0].startswith('.text')):      # we care only .text area
                    continue
                if 'call' in token and (token[1] == 'E8' or token[1] == 'FF' or token[1] == '9A') :     # whether the line has 'call' asm command
                    ix = token.index('call')
                    if token[ix+1] == 'dword':                  # dword
                        k = token[ix+1]+'_'+token[ix+2] + '_' + token[ix+3]
                    elif token[ix+1].startswith('e'):           # call eax type
                        if len(token) == ix+2:
                            k = token[ix+1]
                        else:
                            k = token[ix+3]
                    else:                                        # default
                        k = token[ix+1]
                    k = k.replace('$', 'Dollor_')               # handle values that are not accepted as key
                    k = k.replace('.', '_')
                    if k in Data.keys():
                        Data[k] += 1
                    else:
                        Data[k] = 1
            CI.insert(Data)


if __name__ == '__main__':

    CI = db.CallInfo

    TrainList = []
    TestList = [ f for f in listdir(BASEDIR+'test') if f.endswith('.asm') ]

    with open('trainLabels.csv', 'rb') as csvfile:  # Read training file list
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            row[0] = row[0] + '.asm'
            TrainList.append(row)

    TrainList = np.array(TrainList)

    print "Read Test data and Extract features..."
    test = Read_Data("train", TrainList[:,0])
    sys.exit()

