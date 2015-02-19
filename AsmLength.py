__author__ = 'HEEYOUNG'
'''
This script is for building the histogram of length of instructions in training files.

'''

import csv
import numpy as np
import sys
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import os
from pymongo import MongoClient
import string

client = MongoClient('localhost', 27017)
db = client.Malware
BASEDIR =  "H:/Malware_Data/"


if __name__ == '__main__':

    AB = db.AsmBytes
    TL = db.TrainLabels

    for ClassInfo in range(1,10):
        Label_Info = TL.find({"Class": ClassInfo})   # Get the Label info


        Hist = np.zeros((Label_Info.count(), 16))

        idx = 0
        for f_info in Label_Info:
            f = AB.find_one({"Id": f_info['Id']})
            for k in f.keys():
                if k == '_id' or k =='Id':
                    continue
                Hist[idx][int(k)-1] += f[k]
            idx += 1

        with open('../AsmLength/Class' + str(ClassInfo) + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            #plt.figure(ClassInfo+1)
            for H in Hist:
                writer.writerow(H)
                #plt.scatter(range(1,17), H)
        #plt.title('Class %d' %(ClassInfo))
        #plt.show()

    sys.exit()


