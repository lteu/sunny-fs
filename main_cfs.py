import os
import csv
import json





with open('directories.txt') as ff:
  for line in ff:
    
    line = line.rstrip()

    print "Run feature selection, scenario: ", line

    command = 'python fs_cfs.py ' + line
    os.system(command)

    os.chdir("sunny")

    print "Run data2cv"
    command = 'python data2cv.py ' + line
    os.system(command)

    print "Run cv2csv"
    command = 'python cv2csv.py ' + line
    os.system(command)

    print "Run csv2kb"
    command = 'python csv2kb.py ' + line
    os.system(command)

    print "Run predict"
    command = 'python predict.py ' + line
    os.system(command)

    print "Run evaluate"
    command = 'python evaluate.py ' + line
    os.system(command)

    os.chdir("../")