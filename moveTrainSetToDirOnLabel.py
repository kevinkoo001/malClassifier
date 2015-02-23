# -*- coding: utf-8 -*-
__author__ = 'Kevin Koo'

import commonLib
import os

def moveTrainSetToDirOnLabel(targetDir):
    # Get all labels
    # allData = [['"kGITL4OJxYMWEQ1bKBiP"', '1'], ..., , ['"KGorN9J6XAC4bOEkmyup"', '9']]
    csvFile = "trainLabels.csv"
    allData = commonLib.csvImport(csvFile, ',', True)
    trainSet = []
    
    # Data Sanitization
    for data in allData:
        malwareHash = data[0].replace("\"","")
        label = int(data[1])
        trainSet.append((label, malwareHash))
    
    for (label, malwareHash) in trainSet:
        commonLib.createDir(targetDir, label)
        malware1 = targetDir + '\\' + malwareHash + '.asm'
        malware2 = targetDir + '\\' + malwareHash + '.bytes'
        #malwareBin = targetDir + '\\' + malwareHash + '.bytes_raw'
        try:
            commonLib.moveFile(malware1, targetDir + '\\' + str(label), malwareHash + '.asm')
            commonLib.moveFile(malware2, targetDir + '\\' + str(label), malwareHash + '.bytes')
            #commonLib.moveFile(malwareBin, targetDir + '\\' + str(label), malwareHash + '.bytes_raw')
        except:
            print "'%s' is not found.. (failed to move it)" % (malwareHash)
            
def getDllsImports(targetDir):
    pass

if __name__ == '__main__':
    targetDir = 'F:\\MS_Malware_Classification_Challenge\\trainBin'
    moveTrainSetToDirOnLabel(targetDir)
    #target = '~/gomal/train/5'