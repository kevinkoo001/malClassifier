__author__ = 'HEEYOUNG'

import numpy as np
import csv

if __name__ == '__main__':

    Fname, Labels = np.loadtxt('trainLabels.csv', skiprows=1, delimiter=',', usecols=(0, 1), unpack=True, dtype=[('a', '|S25'), ('b', '<i4')])
    for i in range(0, len(Fname)):
        Fname[i] = Fname[i].replace('"', '') + '.asm'

    f1 = open('SampleTrain.csv', 'wb')
    f2 = open('SampleTest.csv', 'wb')
    writer1 = csv.writer(f1)
    writer2 = csv.writer(f2)
    for i in range(9):
        count = 0
        flag = 0
        for name in Fname[Labels==(i+1)]:
            count += 1
            if not flag:
                writer1.writerow([name, i+1])
            else:
                writer2.writerow([name, i+1])
            if count%20 == 0:
                flag = 1
            if count%40 == 0:
                break