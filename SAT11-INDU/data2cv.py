import os
import csv
import json

CV_FILE = 'aslib_data/cv.arff'
INPUT_FILES = ['feature_values.arff', 'algorithm_runs.arff']

# No. of repetitions.
REPS = 1
# No. of folds.
FOLDS = 10
# No. of algorithms.
ALGORITHMS = 18
# No. of instances.
INSTANCES = 300

# Dictionaries that associate to each repetition/fold the corresponding set of 
# test instances.
test_insts = {}
# Dictionaries that associate to each repetition/fold the corresponding .csv
# writer for creating training/test files.
test_writers = {}
train_writers = {}
# Initializes test_insts, creates rep_I_fold_J directories and files.
for i in range(1, REPS + 1):
  test_insts[i] = {}
  test_writers[i] = {}
  train_writers[i] = {}
  for j in range(1, FOLDS + 1):
    test_insts[i][j] = set([])
    path = 'cv/rep_' + str(i) + '_fold_' + str(j)
    if not os.path.exists(path):
      os.makedirs(path)
    test_writers[i][j] = {}
    train_writers[i][j] = {}
    for infile in INPUT_FILES:
      test_writers[i][j][infile] = csv.writer(
        open(path + '/test_' + infile, 'w'), delimiter = ','
      )
      train_writers[i][j][infile] = csv.writer(
        open(path + '/train_' + infile, 'w'), delimiter = ','
      )
  
# Splits instances into training and test sets.
reader = csv.reader(open(CV_FILE, 'r'), delimiter = ',')  
for row in reader:
  if row and row[0].strip().upper() == '@DATA':
    # Iterates until preamble ends.
    break
for row in reader:
  inst = row[0]
  i = int(row[1])
  j = int(row[2])
  test_insts[i][j].add(inst)
   
# Creates train/test files in the corresponding folders.
for infile in INPUT_FILES:
  tr = 0
  ts = 0
  in_path = 'aslib_data/' + infile
  reader = csv.reader(open(in_path, 'r'), delimiter = ',')
  for row in reader:
    if row and row[0].strip().upper() == '@DATA':
      # Iterates until preamble ends.
      break
  for row in reader:
    inst = row[0]
    i = int(row[1])
    for j in range(1, FOLDS + 1):
     # print i,' ',j
      if inst in test_insts[i][j]:
        test_writers[i][j][infile].writerow(row)
        ts += 1
      else:
        train_writers[i][j][infile].writerow(row)
        tr += 1
  
  # Consistency checks.
  if infile == 'feature_values.arff':
    assert ts == INSTANCES
  else:
    assert ts == INSTANCES * ALGORITHMS
  if infile == 'feature_values.arff':
    assert tr == (FOLDS - 1) * INSTANCES
  else:
    assert tr == (FOLDS - 1) * INSTANCES * ALGORITHMS
    