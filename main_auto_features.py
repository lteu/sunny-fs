import os
import csv
import json

lists = [1,2,3,4,5,6,7,8,16,32,64,128]
# lists = [3,5]

for x in lists:
    with open('directories.txt') as ff:
        for line in ff:
    
            line = line.rstrip()

            print "Run feature selection, scenario: ", line

            command = 'python fs_auto_ranker_featurefile.py ' + line + ' '+ str(x)
            os.system(command)