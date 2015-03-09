__author__ = 'Kevin Koo'

import os
import struct 
import commonLib
from progressBar import *

def writeRawBinary(saveToDir, target):
    newFile = open(saveToDir + target.split(os.sep)[-1] + "_raw", "wb")

    # Take all single-bytes in a list
    # Eventually rawData = ['5e', '3e', '11', '8f', ...]
    rawData = []
    with open(target) as f:
        for line in f:
            l = line.split('\n')
            raws = l[0].split(' ')
            for raw in raws:
                if len(raw) == 2:
                    if raw == '??':
                        raw = raw.replace('??','00')
                    rawData.append(raw)
                    
    # Create a new raw binary based on the given file
    rawData = [int(x, 16) for x in rawData]
    allBytes = struct.pack('<B', rawData[0])
    del rawData[0]
    
    # Write all bytes to the target file
    for b in rawData:
        allBytes += struct.pack('<B', b)
    newFile.write(allBytes)

if __name__ == '__main__':
    #files = os.listdir('.')

    dataBase = commonLib.getBase(os.name)
    trainDir = dataBase + 'train' + os.sep
    trainBinDir = dataBase + 'trainBin' + os.sep
    trainLabels = range(1,10)
    
    files = []
    
    # Find all binaries to which have not been converted from 'bytes'
    index = 0
    progress = progressBar(0, 1407, 50)
    for trainLabel in trainLabels:
        srcDir = trainDir + str(trainLabel) + os.sep
        for tr in os.listdir(srcDir):
            if tr.endswith('bytes'):
                dstDir = trainBinDir + str(trainLabel) + os.sep
                if tr+'_raw' not in os.listdir(dstDir):
                    files.append(srcDir + tr)
                    writeRawBinary(dstDir, srcDir + tr)
                    index += 1
                    progress(index)
    
    '''
    # Converting "byte" file into binary
    index = 0
    for f in files:
        if f.endswith('bytes'):
            #print "[%5d] Processing %s..." % (index, f)
            writeRawBinary(trainBinDir, f)
            index += 1
    '''
    
    print str(len(files)) + " files done!"