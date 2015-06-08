import os
import csv
import json
import time

start = 0
elapse_fs = 0
elapse = 0

#list denotes number of features that will be extracted ... 
# lists = [3,5,7,9,11,13,15,17,19]
lists = [8]

text = ""

for x in lists:
      with open('directories.txt') as ff:
            for line in ff:
                  start = time.time()

                  line = line.rstrip()

                  print "Run feature selection, scenario: ", line

                  command = 'python fs_auto_ranker.py ' + line + ' '+ str(x)
                  os.system(command)

                  elapse_fs = time.time() - start

                  os.chdir("sunny")

                  print "Filter features costs"
                  command = "python feature_cost.py " + line
                  os.system(command)

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
                  if line == "COP-MZN-2013":
                        command = 'python evaluate_auto_cop.py ' + line  + ' '+ str(x)
                        os.system(command)
                  else:
                        command = 'python evaluate_auto.py ' + line  + ' '+ str(x)
                        os.system(command)

                  elapse = time.time() - start
                  text = text + str(elapse) + " " + line + " ranker "+str(x)+" features "+str(elapse_fs)+" \n"

                  os.chdir("../")
            
            outfile = 'time/time_ranker_'+str(x)+".txt"
            with open(outfile, 'a+') as file:
                  file.write(text)