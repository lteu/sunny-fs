#original results tests

import os
import csv
import json
import sys


def loadData( directory,attrsn):
  "This function reads directory"


  path = directory
  TMPFILE1 = path+'/tmpfile1.arff'
  TMPFILE2 = path+'/tmpfile2.arff'
  FEATURE_FILE = path+'/feature_values.arff'
  SELECT_FEATURE_FILE = path+'/selected_feature_values.arff'
  PROPERTY_FILE = path+'/property.json'

  attributes = {}
  data = []

  # with open(FEATURE_FILE) as ff:

  # #feature selection
  # command = 'cp '+FEATURE_FILE+' '+SELECT_FEATURE_FILE
  # os.system(command)

  # # load generated file contents
  itemAttr = []
  itemData = []
  title = ""

  with open(FEATURE_FILE) as ff:
    dataMode = False
    i = 0
    for line in ff:
      if dataMode == False:
        if '@relation' in line or '@RELATION' in line:
          title = line.strip()
          # splitted = line.split("'")
        elif '@attribute' in line or '@ATTRIBUTE' in line:
          line = line.strip()
          # itemAttr.append(line)
          attributes[line] = i
          i = i + 1
        elif '@data' in line or '@DATA' in line:
          dataMode = True
      else:
        line = line.strip()
        if line != "" :
          data.append(line)
          # tmpData =  line
          # itemData.append(tmpData)
  # print attributes 
  # print data

  return title,attributes,data

  # with open(PROPERTY_FILE, 'w+') as outfile:
  #   #write relation
  #   propertyArr = {}
  #   propertyArr['attributesNumber'] = len(itemAttr) -2
  #   propertyArr['instancesNumber'] = len(itemData)
  #   json.dump(propertyArr, outfile)

def cumulativeEvaluation(selAttrs):
  global title,attributes,data
  # print attributes
  for (attr,pos) in attributes.iteritems():
    # print 'text id:', idx, ' val:',val
    if attr not in selAttrs:

      # print 1
      selAttrs.append(attr)

      # title
      outtext = title + "\n\n"

      # attrs
      outtext = outtext + "@ATTRIBUTE instance_id STRING\n"+ "@ATTRIBUTE repetition NUMERIC\n" +"\n".join(selAttrs)+"\n\n@DATA\n"

      # data
      for d in data: #each data line
        ds = d.split(',')
        dLine = ds[0]+","+ds[1] #initials: id, rep
        
        for tmpAttr in selAttrs:
          tmpPos = attributes[tmpAttr]
          dLine = dLine +","+ ds[tmpPos]

        outtext = outtext + dLine + "\n"

      print outtext

      break



# def featureSeletionWith(selAttrs):


##################
## MAIN
##################


# dataDir = 'data/' + sys.argv[1]
dataDir = 'data/PREMARSHALLING-ASTAR-2013'
title,attributes,data = loadData(dataDir,1)

# attrsn =  len(attributes)
# print attrsn
# for i in xrange(1,attrsn-1):
#   print i

testAttrs = ['@ATTRIBUTE group-same-max NUMERIC','@ATTRIBUTE container-density NUMERIC','@ATTRIBUTE bflb NUMERIC']
cumulativeEvaluation(testAttrs)










