import os
import csv
import json

TMPFILE1 = 'data/tmpfile1.arff'
TMPFILE2 = 'data/tmpfile2.arff'
FEATURE_FILE = 'data/feature_values.arff'
SELECT_FEATURE_FILE = 'data/new_feature_values.arff'
#INPUT_FILES = ['feature_values.arff', 'algorithm_runs.arff']

#filter file content
dataMode = False
newlines = []
with open(FEATURE_FILE) as ff:
    for line in ff:
      if dataMode == False:
        if 'instance_id STRING' not in line and 'repetition NUMERIC' not in line:
          newlines.append(line)
        if '@DATA' in line:
          dataMode = True
      else:
        splitted = line.split(",")
        count = len(splitted)
        subarr = splitted[2:count]
        tmp = ','.join(subarr)
        newlines.append(tmp)

#write to filtered file
with open(TMPFILE1, 'w+') as outfile:
  for idx, val in enumerate(newlines):
    out = val
    outfile.write(out)

#feature selection
command = 'java -cp weka.jar weka.filters.supervised.attribute.AttributeSelection -E "weka.attributeSelection.CfsSubsetEval -M" -S "weka.attributeSelection.BestFirst -D 1 -N 5"   -i '+ TMPFILE1+ ' -o '+ TMPFILE2
os.system(command)

newlines = []
headStrings = []
repetitions = []

# load original file head strings
with open(FEATURE_FILE) as ff:
  dataMode = False
  for line in ff:
    if dataMode == False:
      if '@DATA' in line:
        dataMode = True
    else:
      line = line.strip()
      if line != "" :
        splitted = line.split(",")
        headstring = splitted[0]
        repetition = splitted[1]
        headStrings.append(headstring)
        repetitions.append(repetition)

# load generated file contents
itemRelation = []
itemAttr = []
itemData = []
with open(TMPFILE2) as ff:
  dataCounter = 0
  dataMode = False
  for line in ff:
    if dataMode == False:
      if '@relation' in line:
        splitted = line.split("'")
        itemRelation.append(splitted[1])
      elif '@attribute' in line:
        line = line.strip()
        splitted = line.split(" ")
        tmpAttr = splitted[1] + " " + splitted[2].upper()
        itemAttr.append(tmpAttr)
      elif '@data' in line:
        dataMode = True
    else:
      line = line.strip()
      if line != "" :
        tmpData =  headStrings[dataCounter]+","+repetitions[dataCounter]+","+line
        dataCounter += 1
        itemData.append(tmpData)

#write to final file
with open(SELECT_FEATURE_FILE, 'w+') as outfile:

  #write relation
  relation = "@RELATION '" + itemRelation[0] + "'\n\n"
  outfile.write(relation)

  #write attribute
  attr = "@ATTRIBUTE instance_id STRING\n" + "@ATTRIBUTE repetition NUMERIC\n"
  outfile.write(attr)
  for idx, val in enumerate(itemAttr):
    attr = "@ATTRIBUTE " + val + "\n"
    outfile.write(attr)

  #write data
  preData = "\n" + "@DATA" + "\n"
  outfile.write(preData)

  for idx, val in enumerate(itemData):
    data = val+"\n"
    outfile.write(data)