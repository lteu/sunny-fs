import csv
import json
import sys

def cv2csv(scenario,numberOfAttributes,timeout,reps,folds,rootDir):
  # Name of the scenario.
  SCENARIO = scenario
  # No. of repetitions.
  REPS = reps
  # No. of folds.
  FOLDS = folds
  # Default value for missing features.
  DEF_FEAT_VALUE = float("nan")
  # Solving timeout (seconds)
  TIMEOUT = timeout
  # No. of features.
  FEATURES = numberOfAttributes

  for i in range(1, REPS + 1):
    for j in range(1, FOLDS + 1):
      path = rootDir+'/cv/rep_' + str(i) + '_fold_' + str(j) + '/'
      
      # Creating ASP-POTASSCO.feat
      reader = csv.reader(
        open(path + 'train_selected_feature_values.arff'), delimiter = ','
      )
      writer = csv.writer(open(path + SCENARIO + '.feat', 'w'), delimiter = '|')
      for row in reader:
        feats = []
        for f in row[2:]:
          if f == '?':
            f = DEF_FEAT_VALUE
          feats.append(float(f))
          # print str(len(feats)),' vs ',FEATURES
        assert len(feats) == FEATURES
        writer.writerow([row[0], feats])
      
      # Creating ASP-POTASSCO.info
      reader = csv.reader(
        open(path + 'train_algorithm_runs.arff'), delimiter = ','
      )
      writer = csv.writer(open(path + SCENARIO + '.info', 'w'), delimiter = '|')
      for row in reader:
        inst = row[0]
        solver = row[2]

        # here we have a incongruency ... 
        if SCENARIO == "CSP-MZN-2013" or SCENARIO == "COP-MZN-2013":
          info = row[5]
          if info != 'ok':
            time = TIMEOUT
          else:
            time = float(row[4])
        else:
          info = row[4]
          if info != 'ok':
            time = TIMEOUT
          else:
            time = float(row[3])

        assert time != 'ok' or time < TIMEOUT
        writer.writerow([inst, solver, time, info])



###########################
#------- main  ------------
###########################

rootDir = "../data/"+ sys.argv[1]
numberOfInstances = 0
PROPERTY_FILE = rootDir + "/property.json"
PROPERTY_FILE_STATIC = rootDir + "/property_static.json"

with open(PROPERTY_FILE) as data_file:    
  dic = json.load(data_file)
  numberOfAttributes = int(dic['attributesNumber'])
  numberOfInstances = int(dic['instancesNumber'])

with open(PROPERTY_FILE_STATIC) as data_file:    
  dic = json.load(data_file)
  scenario = dic['SCENARIO']
  timeout = dic['timeout']
  reps = dic['reps']
  folds = dic['folds']

cv2csv(scenario,numberOfAttributes,timeout,reps,folds,rootDir)

      