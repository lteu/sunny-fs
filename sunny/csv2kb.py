import os
import csv
import json
from math import sqrt, isnan

# Name of the scenario.
SCENARIO = 'PROTEUS-2014'
# No. of repetitions.
REPS = 1
# No. of folds.
FOLDS = 10
# Default value for missing features.
DEF_FEAT_VALUE = -1
# Solving timeout (seconds)
TIMEOUT = 3600
# No. of features.
FEATURES = 198
# Lower bound for feature scaling.
LB = -1
# Upper bound for feature scaling.
UB =  1
# No. of algorithms.
ALGORITHMS = 22
# Default value for missing features.
DEF_FEAT_VALUE = -1

for i in range(1, REPS + 1):
  for j in range(1, FOLDS + 1):
    path = 'cv/rep_' + str(i) + '_fold_' + str(j) + '/'
    # Processing runtime information.
    reader = csv.reader(open(path + SCENARIO + '.info'), delimiter = '|')
    kb = {}
    n = 0
    for row in reader:
      n += 1
      inst = row[0]
      solv = row[1]
      time = float(row[2])
      info = row[3]
      assert info != 'ok' or time < TIMEOUT    
      if inst not in kb.keys():
        kb[inst] = {}
      kb[inst][solv] = {'info': info, 'time': time}
        
    # Processing features.
    reader = csv.reader(open(path + SCENARIO + '.feat'), delimiter = '|')
    kb_path = path + 'kb_' + SCENARIO 
    if not os.path.exists(kb_path):
      os.makedirs(kb_path)
    writer = csv.writer(
      open(kb_path + '/' + SCENARIO + '_infos', 'w'), delimiter = '|'
    )
    features = {}
    lims = {}
    for row in reader:
      inst = row[0]
      nan = float("nan")
      feat_vector = eval(row[1])
      if not lims:
        for k in range(0, len(feat_vector)):
          lims[k] = [float('+inf'), float('-inf')]
      # Computing min/max value for each feature.
      for k in range(0, len(feat_vector)):
	if not isnan(feat_vector[k]):
	  if feat_vector[k] < lims[k][0]:
	    lims[k][0] = feat_vector[k]
	  if feat_vector[k] > lims[k][1]:
	    lims[k][1] = feat_vector[k]
      features[inst] = feat_vector
      assert len(feat_vector) == FEATURES
      
    for (inst, feat_vector) in features.items():
      if not [s for s, it in kb[inst].items() if it['info'] == 'ok']:
        continue
      new_feat_vector = []
      for k in range(0, len(feat_vector)):
        if lims[k][0] == lims[k][1]:
           # Ignore constant features.
           continue
	if isnan(feat_vector[k]):
	  new_val = DEF_FEAT_VALUE
	else:
	  min_val = lims[k][0]
	  max_val = lims[k][1]
	  # Scale feature value in [LB, UB].
	  x = (feat_vector[k] - min_val) / (max_val - min_val)
	  new_val = LB + (UB - LB) * x
        assert LB <= new_val <= UB
        new_feat_vector.append(new_val)
      assert nan not in new_feat_vector
      kb_row = [inst, new_feat_vector, kb[inst]]
      writer.writerow(kb_row)
  
    lim_file = kb_path + '/' + SCENARIO + '_lims'
    with open(lim_file, 'w') as outfile:
      json.dump(lims, outfile)