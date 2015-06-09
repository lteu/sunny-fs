#feature selection experiment

import os
import csv
import json
import sys


def generateFile( directory ):
  "This function reads directory"

  #================= Evaluation Methods ===================
  # cannot call: AttributeSetEvaluator, CorrelationAttributeEval, HoldOutSubsetEvaluator,  UnsupervisedAttributeEvaluator,  UnsupervisedSubsetEvaluator
  # Need special class: GainRatioAttributeEval, InfoGainAttributeEval, OneRAttributeEval, SymmetricalUncertAttributeEval, ReliefFAttributeEval
  # Returns only one feature, WrapperSubsetEval

  #================= BestFirst ===================

  # Searches the space of attribute subsets by greedy hillclimbing augmented 
  # with a backtracking facility. Setting the number of consecutive non-improving nodes 
  # allowed controls the level of backtracking done. Best first may start with the empty set of 
  # attributes and search forward, or start with the full set of attributes and search backward, 
  # or start at any point and search in both directions (by considering all possible single attribute 
  # additions and deletions at a given point).

  # Forward search - ok
  # selection_algorithm = ' -E "weka.attributeSelection.CfsSubsetEval -M" -S "weka.attributeSelection.BestFirst -D 1 -N 5" '

  # backward search - ok
  # selection_algorithm = ' -E "weka.attributeSelection.CfsSubsetEval -M" -S "weka.attributeSelection.BestFirst -D 0 -N 5" '
  
  # Returns only one feature - ok
  # selection_algorithm = ' -E "weka.attributeSelection.WrapperSubsetEval" -S "weka.attributeSelection.BestFirst -D 1 -S 5" '

  # not working
  
  # NOT FOUND - no
  # selection_algorithm = ' -E "weka.attributeSelection.AttributeSetEvaluator" -S "weka.attributeSelection.BestFirst -D 1 -N 5" '
  # selection_algorithm = ' -E "weka.attributeSelection.CorrelationAttributeEval" -S "weka.attributeSelection.BestFirst -D 1 -N 5" '
  # selection_algorithm = ' -E "weka.attributeSelection.HoldOutSubsetEvaluator" -S "weka.attributeSelection.BestFirst -D 1 -N 5" '
  # selection_algorithm = ' -E "weka.attributeSelection.UnsupervisedAttributeEvaluator" -S "weka.attributeSelection.BestFirst -D 1 -N 5" '
  selection_algorithm = ' -E "weka.attributeSelection.UnsupervisedSubsetEvaluator" -S "weka.attributeSelection.BestFirst -D 1 -N 5" '

  
  
  #================= GreedyStepwise ===================

  # "Performs a greedy forward or backward search through the space of attribute subsets. \
  #   May start with no/all attributes or from an arbitrary point in the space. \
  #   Stops when the addition/deletion of any remaining attributes results in a decrease in evaluation. \
  #   Can also produce a ranked list of attributes by traversing the space from one side to the other and \
  #   recording the order that attributes are selected."

  #selection_algorithm = ' -E "weka.attributeSelection.CfsSubsetEval" -S "weka.attributeSelection.GreedyStepwise -N 15 -B" '

  #================= Ranker ===================

  # see file fs_ranker.py

  path = directory
  TMPFILE1 = path+'/tmpfile1.arff'
  TMPFILE2 = path+'/tmpfile2.arff'
  FEATURE_FILE = path+'/feature_values.arff'
  SELECT_FEATURE_FILE = path+'/selected_feature_values.arff'
  PROPERTY_FILE = path+'/property.json'

  #filter file content
  dataMode = False
  newlines = []
  with open(FEATURE_FILE) as ff:
      for line in ff:
        if dataMode == False:
          if 'instance_id STRING'.upper() not in line.upper() and 'repetition NUMERIC'.upper() not in line.upper():
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
  command = 'java -cp weka.jar weka.filters.supervised.attribute.AttributeSelection '+selection_algorithm+'   -i '+ TMPFILE1+ ' -o '+ TMPFILE2
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

  with open(PROPERTY_FILE, 'w+') as outfile:
    #write relation
    propertyArr = {}
    propertyArr['attributesNumber'] = len(itemAttr)
    propertyArr['instancesNumber'] = len(itemData)
    json.dump(propertyArr, outfile)

  #remove tmp files
  rm = "rm -rf "+TMPFILE1
  os.system(rm)
  rm = "rm -rf "+TMPFILE2
  os.system(rm)

##################
## MAIN
##################


dataDir = 'data/' + sys.argv[1]
generateFile(dataDir)