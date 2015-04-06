import os
import csv
import json



print "Run feature selection"
command = 'python fs.py'
os.system(command)

os.chdir("sunny")

print "Run data2cv"
command = 'python data2cv.py'
os.system(command)

print "Run cv2csv"
command = 'python cv2csv.py'
os.system(command)

print "Run csv2kb"
command = 'python csv2kb.py'
os.system(command)

print "Run predict"
command = 'python predict.py'
os.system(command)

print "Run evaluate"
command = 'python evaluate.py'
os.system(command)