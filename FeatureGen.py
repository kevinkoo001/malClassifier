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

if __name__ == '__main__':

    DI = db.dllInfo
    TL = db.TrainLabels


    dll_list = []
    with open('../dll_list.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dll_list.append(row[0])


    Train = DI.find(timeout=False)

    TrainFeat = np.zeros((Train.count(), len(dll_list)))
    TrainLabel = np.zeros((Train.count(), 1))
    idx = 0
    for d in Train:
        for k in d.keys():
            if k == '_id':
                continue
            if k == 'Id':
                Info = TL.find_one({"Id": d[k]})
                TrainLabel[idx] = Info['Class']
            else:
                TrainFeat[idx, dll_list.index(k)-1] = d[k]
        idx += 1

    np.savetxt('../TrFeat.csv', TrainFeat, fmt= '%d', delimiter=',')  # Save features of training data
    np.savetxt('../TrLabel.csv', TrainLabel, delimiter = ',')

    DI = db.dllInfoTest

    Test = DI.find(timeout=False)

    TestFeat = np.zeros((Test.count(), len(dll_list)))
    TestID = np.zeros((Test.count(), 1), dtype='str')
    idx = 0
    fout = open('../TtID.csv', 'wb')
    writer = csv.writer(fout)
    for d in Test:
        for k in d.keys():
            if k == '_id':
                continue
            if k == 'Id':
                writer.writerow([d[k]])
            else:
                TestFeat[idx, dll_list.index(k)-1] = d[k]
        idx += 1

    np.savetxt('../TtFeat.csv', TestFeat, fmt='%d', delimiter=',')

    sys.exit()