
import csv
import json

# Name of the scenario.
SCENARIO = 'PROTEUS-2014'
# No. of repetitions.
REPS = 1
# No. of folds.
FOLDS = 10
# Solving timeout (seconds)
TIMEOUT = 3600
# No. of algorithms.
ALGORITHMS = 22
# Single best solver.
SBS = 'choco'
# PAR10 score.
PAR10 = TIMEOUT * 10
# No. of instances.
INSTANCES = 4021

runtimes = {}
for i in range(1, REPS + 1):
  for j in range(1, FOLDS + 1):
    path = 'cv/rep_' + str(i) + '_fold_' + str(j) + '/'
    reader = csv.reader(
      open(path + 'test_algorithm_runs.arff' , 'r'), delimiter = ','
    )
    for row in reader:
      inst = row[0]
      solv = row[2]
      time = float(row[3])
      info = row[4]
      if inst not in runtimes.keys():
        runtimes[inst] = {}
      runtimes[inst][solv] = [time, info]
      
with open('feature_cost', 'r') as infile:
  feature_cost = json.load(infile)
  
vbs_time = 0.0
vbs_solved = 0.0
sbs_time = 0.0
sbs_solved = 0
sbs_mcp = 0.0
sunny_time = 0.0
sunny_solved = 0
sunny_mcp = 0.0
n = 0.0
m = 0.0

#no_sat_list = set([])
#reader = csv.reader(open('PROTEUS_NO_SAT/inst_list', 'r'))
#for row in reader:
  #no_sat_list.add(row[0])
writer = csv.writer(open('sunny.csv', 'w'), delimiter = ',')
writer.writerow(['instances', 'SUNNY'])
for i in range(1, REPS + 1):
  for j in range(1, FOLDS + 1):
    path = 'cv/rep_' + str(i) + '_fold_' + str(j) + '/'
    reader = csv.reader(open(path + 'predictions.csv' , 'r'), delimiter = ',')
    for row in reader:
      inst = row[0]
      #if inst not in no_sat_list:
	#continue
      best = [
	(runtimes[inst][s][0], s) 
	for s in runtimes[inst].keys() 
	if runtimes[inst][s][1] == 'ok'
      ]
      if not best:
	vbs_time += PAR10
	sbs_time += PAR10
	sunny_time += PAR10
	n += 1
	continue
      min_time = min(best)[0]
      n += 1
      m += 1
      vbs_time += min_time
      vbs_solved += 1
      schedule = eval(row[3])
      time = feature_cost[inst]
      solved = False
      rem_time = 0
      for (s, t) in schedule:
	t = float(t)
	t += rem_time
	rem_time = 0
	if runtimes[inst][s][0] <= t and runtimes[inst][s][1] == 'ok':
	  time += runtimes[inst][s][0]
	  solved = True
	  break
	elif runtimes[inst][s][0] < t and runtimes[inst][s][1] != 'ok':
	  rem_time = t - runtimes[inst][s][0]
	  time += runtimes[inst][s][0]
	else:
	  time += t
	  
      if solved:
        sunny_solved += 1
        sunny_time += time
        writer.writerow([inst, time])
        sunny_mcp += time - min_time
      else:
	sunny_time += PAR10
	writer.writerow([inst, PAR10])
	sunny_mcp += TIMEOUT - min_time
      if runtimes[inst][SBS][1] == 'ok':
	sbs_time += runtimes[inst][SBS][0]
	sbs_solved += 1
	sbs_mcp += runtimes[inst][SBS][0] - min_time
      else:
	sbs_time += PAR10
	sbs_mcp += TIMEOUT - min_time

assert n == INSTANCES
print '*** ' + SCENARIO + ' ***'
print 'No. of instances:',n
print 'Solvable instances',m
print '----------'
print 'SUNNY PAR10:',sunny_time / n
print 'SUNNY FSI:',sunny_solved / n
print 'SUNNY MCP:',sunny_mcp / n
print '----------'
print 'SBS PAR10:',sbs_time / n 
print 'SBS FSI:',sbs_solved / n
print 'SBS MCP:',sbs_mcp / n
print '----------'
print 'VBS PAR10:',vbs_time / n
print 'VBS FSI:',vbs_solved / n
print 'VBS MCP: 0'
print '=========='