#! /usr/bin/env python

'''
pre_process [OPTIONS] <SCENARIO_PATH>
Computes the SUNNY pre-solving phase and sets the corresponding arguments.
Note that feature selection is performed by using WEKA tool, and in particular 
the supervised attribute filter:
  weka.filters.supervised.attribute.AttributeSelection
which allows various search and evaluation methods to be combined.
Options
=======
--kb-path <PATH>
  PATH of the SUNNY knowledge base for the specified scenario. By default, it is 
  set to <SCENARIO_PATH>
  
--static-schedule 
  Computes a static schedule. If set, computes a static schedule (B, C) where:
    B: is the backup solver of the given scenario.
    C: is T/(M * 10), where T is the timeout and M the number of algorithms of 
       the given scenario.
  By default, this option is unset.
  TODO: Add more options for static scheduling.
  
-S <SEARCH CLASS>
  Sets the search method and its options for WEKA subset evaluators, e.g.:
    -S "weka.attributeSelection.BestFirst -S 8"
  This option is allowed only in conjunction with -E option.
  (TBD)
  
-E <ALGORITHM>
  Sets the attribute/subset evaluator and its options, e.g.:
    -E "weka.attributeSelection.CfsSubsetEval -L"
  This option is allowed only in conjunction with -S option.
  (TBD)
  
--help
  Prints this message.
'''

import os
import csv
import sys
import json
import getopt
import shutil

def parse_arguments(args):
  '''
  Parse the options specified by the user and returns the corresponding
  arguments properly set.
  '''
  try:
    opts, args = getopt.getopt(
      args, 'S:E:', ['help', 'static-schedule', 'kb-path=']
    )
  except getopt.GetoptError as msg:
    print >> sys.stderr, msg
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  
  if not args:
    if not opts:
      print >> sys.stderr, 'Error! No arguments given.'
      print >> sys.stderr, 'For help use --help'
      sys.exit(2)
    else:
      print __doc__
      sys.exit(0)

  scenario = args[0]
  if scenario[-1] != '/':
    scenario += '/'
  if not os.path.exists(scenario):
    print >> sys.stderr, 'Error: Directory ' + scenario + ' does not exists.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
    
  # Initialize variables with default values.
  feat_algorithm = None
  evaluator = ''
  search = ''
  static_schedule = False
  kb_path = scenario
  kb_name = 'kb_' + scenario.split('/')[-2]

  # Options parsing.
  for o, a in opts:
    if o == '--help':
      print __doc__
      sys.exit(0)
    elif o == '-E':
      evaluator = a
    elif o == '-S':
      search = a
    elif o == '--static-schedule':
      static_schedule = True
    elif o == '--kb-path':
      if not os.path.exists(a):
        print >> sys.stderr, 'Error! Directory ' + a + ' not exists.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      if a[-1] == '/':
        kb_path = a[:-1]
      else:
        kb_path = a
  
  kb_name = kb_path.split('/')[-2]
  args_file = kb_path + '/' + kb_name + '.args'
  info_file = kb_path + '/' + kb_name + '.info'
  return args_file, info_file, scenario, evaluator, search, static_schedule

def select_features(args, info_file, evaluator, search):
  
  # ****************************************************************************
  # TODO: Tong, please implement this function.
  # args = python dict containing the arguments of SUNNY (e.g., selected_features, 
  #  feature_steps,...)
  # info_file = path of csv file containing feature vectors and runtime infos for each instance
  # evaluator = WEKA evaluator command
  # search = WEKA search command
  
  #weka_cmd = 'java -cp weka.jar weka.filters.supervised.attribute.AttributeSelection ' + evaluator + search
  #....

  # for the purpose of creating algorithm classes in order to associate each instance with the best solving algorithm
  scenario = args['scenario']
  dic = getBestAlg('data/'+scenario)

  path = 'data/'+scenario #working directory
  TMPFILE1 = path+'/tmpfile1.arff'
  TMPFILE2 = path+'/tmpfile2.arff'
  FEATURE_FILE = path+'/feature_values.arff'
  SELECT_FEATURE_FILE = path+'/selected_feature_values.arff'
  PROPERTY_FILE = path+'/property.json'


  #Get all solving tools of this scenario
  algs = {}
  PROPERTY_FILE_STATIC = path+'/property_static.json'
  with open(PROPERTY_FILE_STATIC) as ff:
    dic = json.load(ff)
    algs = dic['PORTFOLIO']
    algs.append('allfair')
    algsstring = ', '.join(algs)
    #print algsstring

  #filter file content
  # filters instance_id STRING repetition NUMERIC e-0 e-1 .... 
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
  

  #feature selection, where 'selection_algorithm' stands for 'evaluator + search'
  command = 'java -cp weka.jar weka.filters.supervised.attribute.AttributeSelection -S "'+search+'" -E "'+evaluator+'"  -i '+ TMPFILE1+ ' -o '+ TMPFILE2
  #weka_cmd = 'java -cp weka.jar weka.filters.supervised.attribute.AttributeSelection ' + evaluator + search
  
  #print execute weka feature selection command
  os.system(command)

  newlines = []
  instanceids = []
  repetitions = []

  # load istance_id, repetition from original arff
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
          instanceid = splitted[0]
          repetition = splitted[1]
          instanceids.append(instanceid)
          repetitions.append(repetition)

  # combine istance_id, repetition with selected_features (generated by weka)
  itemRelation = [] #scenario name
  selected_features_raw = [] # selected attributes a.k.a selected features
  selected_features_data = [] # values of intances
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
          selected_features_raw.append(tmpAttr)
        elif '@data' in line:
          dataMode = True
      else:
        line = line.strip()
        if line != "" :
          tmpData =  instanceids[dataCounter]+","+repetitions[dataCounter]+","+line
          dataCounter += 1
          selected_features_data.append(tmpData)     



  #write to final file
  with open(SELECT_FEATURE_FILE, 'w+') as outfile:

    #write relation
    relation = "@RELATION '" + itemRelation[0] + "'\n\n"
    outfile.write(relation)

    #write attribute
    attr = "@ATTRIBUTE instance_id STRING\n" + "@ATTRIBUTE repetition NUMERIC\n"
    outfile.write(attr)
    for idx, val in enumerate(selected_features_raw):
      attr = "@ATTRIBUTE " + val + "\n"
      if 'algorithm' not in val.lower():
        outfile.write(attr)

    #write data
    preData = "\n" + "@DATA" + "\n"
    outfile.write(preData)

    for idx, val in enumerate(selected_features_data):
      splitted = val.split(',')
      count = len(splitted)
      validValArr = splitted[0:count-1]
      validVal = ','.join(validValArr)
      data = validVal+"\n"
      outfile.write(data)

  # write properties json file, the parameters: attributesNumber and instancesNumber would then be
  # read by sunny, if this part has already been treated we can then delete the function.
  with open(PROPERTY_FILE, 'w+') as outfile:
    #write relation
    propertyArr = {}
    propertyArr['attributesNumber'] = len(selected_features_raw) -1
    propertyArr['instancesNumber'] = len(selected_features_data)
    json.dump(propertyArr, outfile)


  # Roberto:
  # new_features will be the list of the selected features. This is a dummy test
  # which selects all the training features.
  # selected_features = args['selected_features']
  

  # new_features = selected_features.keys()
  # #
  # #*****************************************************************************
  # feature_steps = getFeatureSteps(selected_features_raw)
  feature_steps = args['feature_steps']
  new_features = readSelectedFeaturesName(selected_features_raw)
  
  selected_features = dict(
    (feature, index) 
    for (feature, index) in selected_features.items() 
    if feature in new_features
  )
  feature_steps = dict(
    (step, features) 
    for (step, features) in feature_steps.items()
    if set(features).intersection(new_features)
  )

  return selected_features, feature_steps


#====================================#====================================
# func by Tong
#====================================#====================================

def filterE16(arr):
  " convert data format "
  for indx, val in enumerate(arr):
    num = str(val)
    if num.find("e-16") != -1:
      num = float(num)
      num = round(num,15)
    arr[indx] = str(num)

  return arr

def getBestAlg( directory ):
  #"This function reads scenario directory and gets directory of best algorithms"
  # " example of directory: 'data/SAT11-HAND' "

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


#===================  Feature cost Foo ====================================

def readSelectedFeaturesName(selected_features_raw):

  selected_features_names = []
  for indx, feature in enumerate(selected_features_raw):
    splitted = feature.split(" ")
    selected_features_names.append(splitted[0])
  return selected_features_names


def loadFeatureSteps(desc_features):
  arr = {}
  with open(desc_features) as ff:
    for line in ff:
      if 'feature_step ' in line.lower():
        line = line.strip()
        splitted = line.split(":")
        prename = splitted[0].split(" ")
        step_name = prename[1]
        step_features = splitted[1].split(",")

        for feature in step_features:
          feature = feature.strip()
          if feature in arr:
            arr[feature].append(step_name)
            # print "append for ",feature,' the',step_name
          else:
            arr[feature] = [step_name]
            # print "create for ",feature,' the',step_name
  return arr

# def markFeatureSteps():

def getInvolvedSteps(feature_steps,selected_features):
  result = []
  for indx, feature in enumerate(selected_features):
    steps = feature_steps[feature]
    result = result + steps
  return result


def createSelectedFeatureCostFile(feature_costs,selected_steps):
  feature_positions = []
  # out = []
  out = ""
  dataMode = False
  attributeCount = -1
    # idxAlg = -1
    # idxTime = -1
    # idxScore = -1
    # isFair = True

  with open(feature_costs) as ff:
    for line in ff:
      #line = line.rstrip()
      if dataMode == False:
        if '@data' in line.lower():
          dataMode = True
          out = out + "@DATA\n"
        elif '@attribute' in line.lower():
          attributeCount += 1
          splitted = line.split(" ")
          stepname = splitted[1].rstrip()
          if stepname in selected_steps:
            feature_positions.append(attributeCount)
            out = out + line
          if 'instance_id' in line or 'repetition' in line:
            out = out + line
        else:
          out = out + line
      else:
        line = line.rstrip()
        if line != "":
          splitted = line.split(",")
          tmpline = ""
          for pos, val in enumerate(splitted):
            if pos == 0:
              tmpline = val
            if pos == 1:
              tmpline = tmpline + ","+val
            elif pos in feature_positions:
              tmpline = tmpline + ","+val

          out = out+tmpline+"\n"
  return out


def getFeatureSteps(selected_features_raw):
  root = "data/"+scenario
  path_feature_cost = root + '/feature_costs.arff'
  path_selected_feature_cost = root + '/selected_feature_costs.arff'
  desc_features = root + "/description.txt"
  result = None

  if not os.path.exists(path_feature_cost):
    print "No feature cost file  - ok"
  elif not os.path.exists(desc_features):
    command = 'cp ' + path_feature_cost + ' '+ path_selected_feature_cost
    os.system(command)
    print "NO feature cost description  - ok"
  else:
    feature_steps = loadFeatureSteps(desc_features)
    # print 'steps: ', feature_steps
    selected_features_names = readSelectedFeaturesName(selected_features_raw)
    selected_steps = getInvolvedSteps(feature_steps,selected_features_names)
    selected_steps = list(set(selected_steps))
    result = selected_steps

  return result



#====================================#====================================
# end func by Tong
#====================================#====================================  

def compute_schedule(args, max_time = 10):
  # TODO: Fabio, here you can try different static schedules (maybe setting a 
  # corresponding options, e.g. --static-schedule <...>)
  solver = args['backup']
  time = args['timeout'] / (10 * len(args['portfolio']))
  return [(solver, min(time, max_time))]

def main(args):
  args_file, info_file, scenario, evaluator, search, static_schedule = \
    parse_arguments(args)
  with open(args_file) as infile:
    args = json.load(infile)
  infile.close()
  
  # Feature selection.
  if evaluator and search:
    selected_features, feature_steps = select_features(
      args, info_file, evaluator, search
    )
    args['selected_features'] = selected_features
    args['feature_steps'] = feature_steps
  
  # Static schedule.
  if static_schedule:
    static_schedule = compute_schedule(args)
    args['static_schedule'] = static_schedule
    
  with open(args_file, 'w') as outfile:
    json.dump(args, outfile)
    
if __name__ == '__main__':
  main(sys.argv[1:])