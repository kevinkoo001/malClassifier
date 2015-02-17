__author__ = 'HEEYOUNG'

import sys
from os import listdir
from os.path import isfile, join
import numpy as np
import pylzma

if __name__ == '__main__':

    F_list = [ f for f in listdir('./') if isfile(join('./',f)) ]
    nfeature = 16**2 + 1 # For two_byte_codes, no_que_marks
    train = np.zeros((2, nfeature), dtype = int)
    idx = -1
    for fname in F_list:
        if fname.endswith('.asm'):
            print fname
            idx += 1
            with open(fname) as f:
                for line in f:
                    token = line.split(' ')
                    if not token[0].startswith('.text'):
                        continue
                    if len(token) > 1:
                        if len(token[1]) == 2:
                            if token[1] == '??':
                                train[idx, -1] += 1
                            else:
                                train[idx, int(token[1], 16)] += 1
    print train
    sys.exit()