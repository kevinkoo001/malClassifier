__author__ = 'HEEYOUNG'


import csv
import numpy as np
import sys
from os import listdir
import mmap
import copy
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
db = client.Malware

BASEDIR = "H:/Malware_Data/"

def Read_Data(dir, F_List):

    idx = 0
    print "Total: ", len(F_List), "files"
    Data_bulk = []
    for fname in F_List:
        idx += 1
        Data = {}
        Data['Id'] = fname[:-4]
        if idx % 100 == 0 and idx != 0:
            print 100*float(idx)/len(F_List), "% is done"
        dll_pool = copy.deepcopy(dll_list)
        with open(BASEDIR+dir+'/'+fname) as f:
            for line in f:
                if not (line.startswith('.idata')):      # we care only .text area
                    continue
                for dll in dll_pool:
                    if line.find(dll) != -1:
                        Data[dll] = 1
                        dll_pool.remove(dll)
            '''
            s = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ)
            for dll in dll_list:
                if s.find(dll) != -1:                           # Check whether a specific dll is in a file
                    Data[dll] = 1
            '''
        Data_bulk.append(Data)

        if len(Data_bulk) % 100 == 0:
            DI.insert(Data_bulk)
            Data_bulk = []

    if len(Data_bulk):
        DI.insert(Data_bulk)


if __name__ == '__main__':

    DI = db.dllInfo

    TrainList = []
    TestList = [ f for f in listdir(BASEDIR+'test') if f.endswith('.asm') ]

    dll_list = []
    with open('../dll_list.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dll_list.append(row[0])

    with open('../trainLabels.csv', 'rb') as csvfile:  # Read training file list
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            row[0] = row[0] + '.asm'
            TrainList.append(row)

    TrainList = np.array(TrainList)

    print "Read Train data and Extract features..."
    Read_Data("train", TrainList[:, 0])

    DI = db.dllInfoTest

    print "Read Test data and Extract features..."
    Read_Data("test", TestList)
    sys.exit()

