__author__ = 'HEEYOUNG'

import csv
import numpy as np
import sklearn
import sys
from os import listdir
from os.path import isfile, join
import os
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.Malware
BASEDIR = "H:/Malware_Data/"

def Read_Data(dir, F_List):

    idx = -1
    #TokenList = []        # For opcodes
    print "Total: ", len(F_List), "files"
    for fname in F_List:
        Data = {}
        Data['Id'] = fname[:-6]
        idx += 1
        if idx % 100 == 0 and idx != 0:
            print 100*float(idx)/len(F_List), "% is done"
        with open(os.path.join(BASEDIR+dir, fname)) as f:
            for line in f:
                token = line[:-1].split(' ')
                if len(token) > 1:
                    for i in range(1, len(token)-1):
                        if token[i]+token[i+1] not in Data.keys():
                            Data[token[i]+token[i+1]] = 1
                        else:
                            Data[token[i]+token[i+1]] += 1
            Tr.insert(Data)


if __name__ == '__main__':

    TrainList = []

    Tr = db.TrainingData

    with open('trainLabels.csv', 'rb') as csvfile:  # Read Sample file, which has list of files and class
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            row[0] = row[0] + '.bytes'
            TrainList.append(row)

    TrainList = np.array(TrainList)


    print "Read Training Data and Extract features..."
    Read_Data("train", TrainList[:, 0])        # Read and get features of training data

    sys.exit()

