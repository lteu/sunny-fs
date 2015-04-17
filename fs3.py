#feature selection with ranker 

import os
import csv
import json
import sys


def generateFile( directory ):
  "This function reads directory"


  path = directory
  TMPFILE1 = path+'/tmpfile1.arff'
  TMPFILE2 = path+'/tmpfile2.arff'
  FEATURE_FILE = path+'/feature_values.arff'
  SELECT_FEATURE_FILE = path+'/selected_feature_values.arff'
  PROPERTY_FILE = path+'/property.json'


  #feature selection
  command = 'cp '+FEATURE_FILE+' '+SELECT_FEATURE_FILE
  os.system(command)

  # load generated file contents
  itemAttr = []
  itemData = []
  with open(SELECT_FEATURE_FILE) as ff:
    dataMode = False
    for line in ff:
      if dataMode == False:
        if '@relation' in line or '@RELATION' in line:
          splitted = line.split("'")
        elif '@attribute' in line or '@ATTRIBUTE' in line:
          line = line.strip()
          itemAttr.append(line)
        elif '@data' in line or '@DATA' in line:
          dataMode = True
      else:
        line = line.strip()
        if line != "" :
          tmpData =  line
          itemData.append(tmpData)

  with open(PROPERTY_FILE, 'w+') as outfile:
    #write relation
    propertyArr = {}
    propertyArr['attributesNumber'] = len(itemAttr) -2
    propertyArr['instancesNumber'] = len(itemData)
    json.dump(propertyArr, outfile)


##################
## MAIN
##################


dataDir = 'data/' + sys.argv[1]
generateFile(dataDir)