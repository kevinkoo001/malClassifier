__author__ = 'HEEYOUNG'

import csv
import numpy as np
import sklearn
import sys
from os import listdir
from os.path import isfile, join
import os
from pymongo import MongoClient
import string

client = MongoClient('localhost', 27017)
db = client.Malware
BASEDIR = "F:/MS_Malware_Classification_Challenge/"


def Read_Data(dir, F_List):

    idx = 0
    print "Total: ", len(F_List), "files"
    for fname in F_List:
        idx += 1
        Data = {}
        if AB.find_one({"Id":fname[:-4]}):
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
                if len(token) < 2:                      # no instruction is contained
                    continue
                L = 0
                print token
                for i in range(1, len(token)):
                    if len(token[i]) != 2:
                        break
                    if not all(c in string.hexdigits for c in token[i]):
                        break
                    if all(c in string.lowercase for c in token[i]):
                        break
                    L += 1
                if L == 0:
                    continue
                if all(item == 'CC' for item in token[1:L+1]):
                    continue
                if all(item == '00' for item in token[1:L+1]):
                    continue
                if str(L) in Data.keys():
                    Data[str(L)] += 1
                else:
                    Data[str(L)] = 1
            sys.exit()
            AB.insert(Data)
if __name__ == '__main__':

    TrainList = []

    AB = db.AsmBytes


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

