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

    TL = db.TrainLabels
    with open('../trainLabels.csv', 'rb') as csvfile:  # Read Sample file, which has list of files and class
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            TL.insert({"Id":row[0], "Class":int(row[1])})

    sys.exit()
