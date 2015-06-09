#feature selection with ranker 

import os
import csv
import json
import sys

def filterE16(arr):
  for indx, val in enumerate(arr):
    num = str(val)
    if num.find("e-16") != -1:
      num = float(num)
      num = round(num,15)
    arr[indx] = str(num)

  return arr

def getBestAlg( directory ):
  "This function reads directory"

  path = directory
  ALG_RUN_FILE = path+'/algorithm_runs.arff'

  instToAlg = {}


  with open(ALG_RUN_FILE) as ff:
    dataMode = False
    tmpid = ''
    tmpScore = 0
    tmpTime = 999999999999
    attributeCount = -1
    idxAlg = -1
    idxTime = -1
    idxScore = -1
    isFair = True
    
    for line in ff:
      line = line.rstrip()

      #preambles
      if dataMode == False:
        if '@data' in line or '@DATA' in line:
          dataMode = True
        elif '@attribute' in line.lower():
          attributeCount += 1
          if 'algorithm' in line.lower():
            idxAlg = attributeCount
          if 'runtime' in line.lower():
            idxTime = attributeCount
          if 'score' in line.lower():
            idxScore = attributeCount
      #data
      else:
        splitted = line.split(',');
        instID =  splitted[0]
        instAlg = splitted[idxAlg]
        instTime = float(splitted[idxTime])
        if idxScore != -1:
          instScore = float(splitted[idxScore])

        #new data
        if not (tmpid == instID):

          #if all alg of last istance perfom the same
          if isFair and tmpid != '':
            instToAlg[tmpid] = 'allfair'

          tmpid = instID
          tmpTime = instTime
          instToAlg[instID] = instAlg
          isFair = True

          if idxScore != -1:
            tmpScore = instScore

        #following data of same inst
        else:

          if (instTime < tmpTime) or (instTime == tmpTime and idxScore != -1 and instScore > tmpScore):
            tmpid = instID
            tmpTime = instTime
            instToAlg[instID] = instAlg

          if instTime != tmpTime or (instTime == tmpTime and idxScore != -1 and instScore != tmpScore):
            isFair = False

  return instToAlg

def generateFile( directory,instToAlg,attrnum):

  "This function reads directory"


  #================= Ranker ===================

  # working
  # ranker used evaluation methods:ReliefFAttributeEval InfoGainAttributeEval SymmetricalUncertAttributeEval


  # all the same results
  selection_algorithm = ' -E "weka.attributeSelection.SymmetricalUncertAttributeEval"  -S "weka.attributeSelection.Ranker -N '+attrnum+'" '
  # selection_algorithm = ' -E "weka.attributeSelection.GainRatioAttributeEval"  -S "weka.attributeSelection.Ranker -N 10" '
  # selection_algorithm = ' -E "weka.attributeSelection.OneRAttributeEval"  -S "weka.attributeSelection.Ranker -N 10" ' 
  # selection_algorithm = ' -E "weka.attributeSelection.InfoGainAttributeEval" -S "weka.attributeSelection.Ranker -N 10" '
  # selection_algorithm = ' -E "weka.attributeSelection.ReliefFAttributeEval" -S "weka.attributeSelection.Ranker -N 10" '


  path = directory
  TMPFILE1 = path+'/tmpfile1.arff'
  TMPFILE2 = path+'/tmpfile2.arff'
  FEATURE_FILE = path+'/feature_values.arff'
  SELECT_FEATURE_FILE = path+'/selected_feature_values.arff'
  PROPERTY_FILE = path+'/property.json'


  #Get algorithms of this scenario
  algs = {}
  PROPERTY_FILE_STATIC = path+'/property_static.json'
  with open(PROPERTY_FILE_STATIC) as ff:
    dic = json.load(ff)
    algs = dic['PORTFOLIO']
    algs.append('allfair')
    algsstring = ', '.join(algs)
    #print algsstring

  #filter file content
  dataMode = False
  newlines = []
  attrCount = 0
  with open(FEATURE_FILE) as ff:
      for line in ff:

        if dataMode == False:
          if 'instance_id STRING'.upper() not in line.upper() and 'repetition NUMERIC'.upper() not in line.upper() and '@DATA' not in line.upper():
            newlines.append(line)
          if '@DATA' in line.upper():
            algsstr = ','.join(algs)
            algsstrToAppend = '\n@ATTRIBUTE algorithm {'+algsstr+'}\n'
            
            size = len(newlines)
            lastline = newlines[size-1].rstrip()
            newlines[size-1] = lastline
            newlines.append(algsstrToAppend)
            newlines.append('\n@DATA\n')
            dataMode = True
          if '@ATTRIBUTE' in line.upper():
            attrCount += 1
        else:
          splitted = line.split(",")

          instID = splitted[0]
          alg = instToAlg[instID]
          count = len(splitted)
          subarr = []

          for i in range(2,count):
            num = str(splitted[i])
            #filter e-016 like elements
            if num.find("E-0") != -1 or num.find("e-0") != -1 or  num.find("e-1") != -1 or  num.find("e-07") != -1:
              num = float(num)
              num = round(num,6)
            subarr.append(str(num))


          #subarr = splitted[2:count]
          tmp = ','.join(subarr)
          tmp = tmp.rstrip()
          tmp = tmp + ','+alg+'\n'
          #tmp = tmp + ',g12cpx\n'
          
          newlines.append(tmp)

  #write to filtered file
  with open(TMPFILE1, 'w+') as outfile:
    for idx, val in enumerate(newlines):
      out = val
      outfile.write(out)




  #feature selection
  command = 'java -cp weka.jar weka.filters.supervised.attribute.AttributeSelection '+selection_algorithm+'   -i '+ TMPFILE1+ ' -o '+ TMPFILE2
  #print command
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
      if 'algorithm' not in val.lower():
        outfile.write(attr)

    #write data
    preData = "\n" + "@DATA" + "\n"
    outfile.write(preData)

    for idx, val in enumerate(itemData):
      splitted = val.split(',')
      count = len(splitted)
      validValArr = splitted[0:count-1]
      validVal = ','.join(validValArr)
      data = validVal+"\n"
      outfile.write(data)

  #write property json file
  with open(PROPERTY_FILE, 'w+') as outfile:
    #write relation
    propertyArr = {}
    propertyArr['attributesNumber'] = len(itemAttr) -1
    propertyArr['instancesNumber'] = len(itemData)
    json.dump(propertyArr, outfile)

  #remove tmp files
  # rm = "rm -rf "+TMPFILE1
  # os.system(rm)
  # rm = "rm -rf "+TMPFILE2
  # os.system(rm)

##################
## MAIN
##################


dataDir = 'data/' + sys.argv[1]
attrnum = sys.argv[2]
dic = getBestAlg(dataDir)

# for (key,val) in dic.iteritems():
#   print 'hey:', key,' valore',val

generateFile(dataDir,dic,attrnum)