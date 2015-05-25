import os
import csv
import json

lists = [3,5,7,9,11,13,15,17,19]
# lists = [3,5]

for x in lists:
    with open('directories.txt') as ff:
        for line in ff:
    
            line = line.rstrip()

            print "Run feature selection, scenario: ", line

            command = 'python fs_auto_ranker2.py ' + line + ' '+ str(x)
            os.system(command)