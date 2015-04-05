import csv
import json

def cv2csv(scenario,features,timeout,rootDir):
  # Name of the scenario.
  SCENARIO = scenario
  # No. of repetitions.
  REPS = 1
  # No. of folds.
  FOLDS = 10
  # Default value for missing features.
  DEF_FEAT_VALUE = float("nan")
  # Solving timeout (seconds)
  TIMEOUT = timeout
  # No. of features.
  FEATURES = features

  for i in range(1, REPS + 1):
    for j in range(1, FOLDS + 1):
      path = rootDir+'/cv/rep_' + str(i) + '_fold_' + str(j) + '/'
      
      # Creating ASP-POTASSCO.feat
      reader = csv.reader(
        open(path + 'train_feature_values.arff'), delimiter = ','
      )
      writer = csv.writer(open(path + SCENARIO + '.feat', 'w'), delimiter = '|')
      for row in reader:
        feats = []
        for f in row[2:]:
          if f == '?':
            f = DEF_FEAT_VALUE
          feats.append(float(f))
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

DIRECTORIES_FILE = '../directories.txt'
rootDir = ''
numberOfInstances = 0
with open(DIRECTORIES_FILE) as ff:

  for directory in ff:
    rootDir = "../"+directory
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

    cv2csv(scenario,numberOfAttributes,timeout,rootDir)

      