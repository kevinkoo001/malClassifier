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
    AK = db.AssemKeys
    CI = db.CallInfo
    CA = db.CallArg

    Files = CI.find(timeout=False)
    for f in Files:
        for k in f.keys():
            if k == '_id' or k == 'Id':
                continue
            if CA.find_one({"arg":k}):
                continue
            CA.insert({"arg": k})

    arg = CA.find(timeout=False)
    arg_id = 0
    for c in arg:
        AK.update({"_id":c['_id']}, {"$set": {"arg_id": arg_id}})
        arg_id += 1
    sys.exit()

