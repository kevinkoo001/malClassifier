__author__ = 'Heeyoung and Kevin Koo'
# -*- coding: utf-8 -*-

"""
This file contains a common helper class and function
"""
import sys
import csv
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn import svm
import numpy as np
import re
DEBUG = False

class FeatureCollector:

    def __init__(self, targetFile):
        self.targetFile = targetFile
        self.sections = []
        self.rawData = []

    def getSectionName(self, line):
        return line.split(':')[0]
        
    def getSections(self):
        return self.sections
    
    def lineProcessing(self, line):
        l = line.rstrip()

        section = self.getSectionName(l)
        if section not in self.sections:
            self.sections.append(section)

        lineContainer = l.split('\t')        
        validLine = ""
        
        if len(lineContainer) > 1:
            index = 0
            for x in range(0, len(lineContainer)):
                try:
                    validLine += lineContainer[index] + " "
                except:
                    pass
                index += 1
        return validLine

    def readAsm(self):
        with open(self.targetFile) as f:
            for line in f:
                self.rawData.append(self.lineProcessing(line))
    
    def checkFeature(self, technique, sections=[]):
        
        cnt = 0
        for line in range(0, len(self.rawData)):
            section = self.getSectionName(self.rawData[line])
            if len(sections) == 0:
                try:
                    if re.search(technique, self.rawData[line]):
                        if DEBUG == True:
                            print "\t\t\t" + str(line + 1), 
                            print re.findall(technique, self.rawData[line])
                        cnt += 1
                except:
                    pass
                
            elif len(sections) > 0 and (False not in [x in self.sections for x in sections]):
                try:
                    if section in sections and re.search(technique, self.rawData[line]):
                        if DEBUG == True:
                            print "\t\t\t" + str(line + 1), 
                            print re.findall(technique, self.rawData[line])
                        cnt += 1
                except:
                    pass
            else:
                print ".",
                
        return cnt
    
    def readLine(self, start, end):
        for i in range(start, end):
            if len(self.rawData[i]) > 0:
                try:
                    print i, 
                    print self.rawData[i]
                except:
                    pass


# parameters: file, delimeter, and header
def csvImport(csvFile, delim, header=True):
    # Reading a csv file and print it out
    try:
        with open(csvFile, 'r') as f:
            reader = csv.reader(f, delimiter=delim, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if header:
                header = reader.next()
            data = [row for row in reader]

    except csv.Error as e:
        print "Error reading CSV file at line %s: %s" % (reader.linenum, e)
        sys.exit(-1)
        
    return data
    

def createDir(location, name):
    if str(name) in os.listdir(location):
        pass
        #print "The directory %s is already in %s" % (name, location)
    else:
        os.mkdir(location + '\\' + str(name))
        #print "mkdir %s\\%s" % (location, name)
        
def moveFile(old, newDir, newFile):
    filename = os.path.basename(old)
    if filename in newDir:
        pass
        #print "The file %s is already in %s" % (filename, newDir)
    else:
        os.rename(old, newDir + '\\' + newFile)
        #print "%s  ----> %s\\%s" % (old, newDir, newFile)


def CV_RanFor(data, L, y):

    datal = data[0:L,:]

    model = RandomForestClassifier()
    param_grid = {"n_estimators": [9, 11, 13, 15], "min_samples_split": [1, 3, 7, 9]}
    grid_search = GridSearchCV(model, param_grid=param_grid, cv=5)
    grid_search.fit(datal, y)

    print "CV score:", grid_search.best_score_

    return grid_search.best_params_


def RandomForest(train, labels, test):
    L = len(train)

    print "Training Random Forest with 5-fold Cross-validation"
    param = CV_RanFor(train, L, labels)
    model = RandomForestClassifier(n_estimators=param['n_estimators'], min_samples_split=param['min_samples_split'])
    model.fit(train, labels)

    feat_importances = model.feature_importances_
    res = model.predict_proba(test)

    return res, feat_importances


def CV_KernelSVM(data, L, y):

    datal = data[0:L,:]

    C_range = 10.0 ** np.arange(-5, 4)
    gamma_range = 10.0 ** np.arange(-5, 4)
    param_grid = dict(gamma=gamma_range, C=C_range)
    grid_search = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=5)
    grid_search.fit(datal, y)

    print "CV score:", grid_search.best_score_

    return grid_search.best_params_


def KernelSVM(train, labels, test):
    L = len(train)

    print "Training Random Forest with 5-fold Cross-validation"
    param = CV_KernelSVM(train, L, labels)
    model = svm.SVC(C = param['C'], gamma = param['gamma'])
    model.fit(train, labels)

    feat_importances = model.feature_importances_
    res = model.predict_proba(test)

    return res, feat_importances

def Export_TestResult(fname, TestList, res):

    fout = open(fname, 'wb')
    writer = csv.writer(fout)
    header = ['Id']
    for i in range(9):
        header.append('Prediction'+str(i+1))
    writer.writerow(header)
    for i in range(len(TestList)):
        out = [TestList[i]]
        out.extend(res[i,:])
        writer.writerow(out)
