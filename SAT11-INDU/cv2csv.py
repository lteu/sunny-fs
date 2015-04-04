import csv

# Name of the scenario.
SCENARIO = 'SAT11-INDU'
# No. of repetitions.
REPS = 1
# No. of folds.
FOLDS = 10
# Default value for missing features.
DEF_FEAT_VALUE = float("nan")
# Solving timeout (seconds)
TIMEOUT = 5000
# No. of features.
FEATURES = 9

for i in range(1, REPS + 1):
  for j in range(1, FOLDS + 1):
    path = 'cv/rep_' + str(i) + '_fold_' + str(j) + '/'
    
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

      #print len(feats)
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
      