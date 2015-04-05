import csv
import json
from math import sqrt
from combinations import *

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
PORTFOLIO = ['abscon', 
'choco', 
'claspcnf_direct',
'claspcnf_directorder',
'claspcnf_support',
'cryptominisat_direct',
'cryptominisat_directorder',
'cryptominisat_support',
'gecode',
'glucose_direct',
'glucose_directorder',
'glucose_support',
'lingeling_direct',
'lingeling_directorder',
'lingeling_support',
'minisat22_direct',
'minisat22_directorder',
'minisat22_support',
'mistral_nj',
'riss3g_direct',
'riss3g_directorder',
'riss3g_support',
]
BACKUP = None
INSTANCES = 4021
# Neighborhood size.
K = int(round(sqrt(INSTANCES * (FOLDS - 1) / FOLDS)))

def normalize(feat_vector, lims):
  norm_vector = []
  i = 0
  for f in feat_vector:
    lb = lims[str(i)][0]
    ub = lims[str(i)][1]
    i += 1
    if lb == ub:
      continue
    if f == '?':
      f = DEF_FEAT_VALUE
    else:
      f = float(f)
      if f < lb:
        f = LB
      elif f > ub:
        f = UB
      else:
        x = (f - lb) / (ub - lb)
        f = LB + (UB - LB) * x
        assert LB <= f <= UB
    norm_vector.append(f)
  return norm_vector

def get_neighbours(feat_vector, kb):
  """
  Returns a dictionary (inst_name, inst_info) of the k instances closer to the 
  feat_vector in the knowledge base kb.
  """
  reader = csv.reader(open(kb, 'r'), delimiter = '|')
  infos = {}
  feat_vectors = {}
  distances = []
  solved = dict((s, [0, 0.0]) for s in PORTFOLIO)
  for row in reader:
    inst = row[0]
    for (s, it) in eval(row[2]).items():
      if it['info'] == 'ok':
        solved[s][0] += 1
        solved[s][1] += float(it['time'])
      else:
	solved[s][1] += TIMEOUT
    d = euclidean_distance(feat_vector, map(float, row[1][1 : -1].split(',')))
    distances.append((d, inst))
    infos[inst] = row[2]
  best = min((INSTANCES - solved[s][0], solved[s][1], s) for s in solved.keys())
  global BACKUP
  BACKUP = best[2]
  sorted_dist = distances.sort(key = lambda x : x[0])
  return dict((inst, infos[inst]) for (d, inst) in distances[0 : K])

def euclidean_distance(fv1, fv2):
  """
  Computes the Euclidean distance between two feature vectors fv1 and fv2.
  """
  assert len(fv1) == len(fv2)
  distance = 0.0
  for i in range(0, len(fv1)):
    d = fv1[i] - fv2[i]
    distance += d * d
  return sqrt(distance)

def get_schedule(neighbours, timeout):
  """
  Given the neighborhood of a given problem and the backup solver, returns the 
  corresponding SUNNY schedule.
  """
 
  # Dictionaries for keeping track of the instances solved and the runtimes. 
  solved = {}
  times  = {}
  for solver in PORTFOLIO:
    solved[solver] = set([])
    times[solver]  = 0.0
  for inst, item in neighbours.items():
    item = eval(item)
    for solver in PORTFOLIO:
      time = item[solver]['time']
      if time < timeout:
        solved[solver].add(inst)
      times[solver] += time
  # Select the best sub-portfolio, i.e., the one that allows to solve more 
  # instances in the neighborhood.
  max_solved = 0
  min_time = float('+inf')
  best_pfolio = []
  m = len(PORTFOLIO)
  for i in range(1, m + 1):
    old_pfolio = best_pfolio
    
    for j in range(0, binom(m, i)):
      solved_instances = set([])
      solving_time = 0
      # get the (j + 1)-th subset of cardinality i
      sub_pfolio = get_subset(j, i, PORTFOLIO)
      for solver in sub_pfolio:
        solved_instances.update(solved[solver])
        solving_time += times[solver]
      num_solved = len(solved_instances)
      
      if num_solved >  max_solved or \
        (num_solved == max_solved and solving_time < min_time):
          min_time = solving_time
          max_solved = num_solved
          best_pfolio = sub_pfolio
          
    if old_pfolio == best_pfolio:
      break
    
  # n is the number of instances solved by each solver plus the instances 
  # that no solver can solver.
  n = sum([len(solved[s]) for s in best_pfolio]) + (K - max_solved)
  schedule = {}
  # Compute the schedule and sort it by number of solved instances.
  for solver in best_pfolio:
    ns = len(solved[solver])
    if ns == 0 or round(timeout / n * ns) == 0:
      continue
    schedule[solver] = timeout / n * ns
  
  tot_time = sum(schedule.values())
  # Allocate to the backup solver the (eventual) remaining time.
  if round(tot_time) < timeout:
    if BACKUP in schedule.keys():
      schedule[BACKUP] += timeout - tot_time
    else:
      schedule[BACKUP]  = timeout - tot_time
  sorted_schedule = sorted(schedule.items(), key = lambda x: times[x[0]])
  assert sum(t for (s, t) in sorted_schedule) - timeout < 0.001
  return sorted_schedule

reader = csv.reader(open('aslib_data/feature_costs.arff'), delimiter = ',')
for row in reader:
  if row and row[0].strip().upper() == '@DATA':
    # Iterates until preamble ends.
    break
feature_cost = {}
for row in reader:
  feature_cost[row[0]] = sum(float(f) for f in row[2:] if f != '?')
with open('feature_cost', 'w') as outfile:
  json.dump(feature_cost, outfile)
  
for i in range(1, REPS + 1):
  for j in range(1, FOLDS + 1):
    path = 'cv/rep_' + str(i) + '_fold_' + str(j) + '/'
    reader = csv.reader(
      open(path + 'test_feature_values.arff' , 'r'), delimiter = ','
    )
    writer = csv.writer(open(path + 'predictions.csv', 'w'), delimiter = ',')
    with open(path + 'kb_' + SCENARIO + '/' + SCENARIO + '_lims') as infile:
      lims = json.load(infile)
    for row in reader:
      inst = row[0]
      feats = normalize(row[2:], lims)
      kb = path + 'kb_' + SCENARIO + '/' + SCENARIO + '_infos'
      neighbours = get_neighbours(feats, kb)
      if TIMEOUT > feature_cost[inst]: 
        schedule = get_schedule(neighbours, TIMEOUT - feature_cost[inst])
      else:
	schedule = []
      writer.writerow([inst, i, j, schedule])