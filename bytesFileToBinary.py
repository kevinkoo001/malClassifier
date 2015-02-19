__author__ = 'HEEYOUNG'


import os
import struct 

def writeRawBinary(fileName):
    newFile = open(fileName + "_raw", "wb")
    
    # Take all single-bytes in a list
    # Eventually rawData = ['5e', '3e', '11', '8f', ...]
    rawData = []
    with open(fileName) as f:
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
    
    for b in rawData:
        allBytes += struct.pack('<B', b)
    newFile.write(allBytes)

if __name__ == '__main__':
    files = os.listdir('.')
    
    # Converting "byte" file into binary
    index = 1
    for f in files:
        if f.endswith('bytes'):
            print "[%5d] Processing %s..." % (index, f)
            index += 1
            
    print "Done!"