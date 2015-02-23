__author__ = 'Heeyoung and Kevin Koo'
# -*- coding: utf-8 -*-

"""
This file contains a common helper class and function
"""
import sys
import csv
import os

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