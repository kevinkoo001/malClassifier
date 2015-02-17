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

    TrainList = []

    AC = db.AssemCnt
    AT = db.AssemCntTest
    AK = db.AssemKeys
    TL = db.TrainLabelds

    Com = AK.find().distinct("Com")
    Com_info = {}
    idx = 0
    for c in Com:
        Com_info[c] = idx
        idx += 1

    '''
    Train = AC.find(timeout=False)

    TrainFeat = np.zeros((Train.count(), len(Com_info)))
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
                TrainFeat[idx, Com_info[k]] = d[k]
        idx += 1

    np.savetxt('TrFeat.csv', TrainFeat, delimiter=',')  # Save features of training data
    np.savetxt('TrLabel.csv', TrainLabel, delimiter = ',')
    '''
    Test = AT.find(timeout=False)

    TestFeat = np.zeros((Test.count(), len(Com_info)))
    TestID = np.zeros((Test.count(), 1), dtype='str')
    idx = 0
    fout = open('TtID.csv', 'wb')
    writer = csv.writer(fout)
    for d in Test:
        for k in d.keys():
            if k == '_id':
                continue
            if k == 'Id':
                writer.writerow([d[k]])
            else:
                if k not in Com_info.keys():
                    continue
                TestFeat[idx, Com_info[k]] = d[k]
        idx += 1

    np.savetxt('TtFeat.csv', TestFeat, delimiter=',')

    sys.exit()