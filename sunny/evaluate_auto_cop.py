import os
import csv
import json
import sys


def evaluate(scenario,timeout,numberOfInstances,reps,folds,rootDir,attrnum):
  # Name of the scenario.
  SCENARIO = scenario
  # No. of repetitions.
  REPS = reps
  # No. of folds.
  FOLDS = folds
  # Solving timeout (seconds).
  TIMEOUT = timeout
  # PAR10 score.
  PAR10 = TIMEOUT * 10
  # Single Best Solver.
  SBS = sbs
  # No. of instances.
  INSTANCES = numberOfInstances

  #result file path, added by Tong
  result_path = '../data/results/ranker'+attrnum+'/' +scenario+ '.txt'
  result_dir_path = '../data/results/ranker'+attrnum+'/'

  runtimes = {}
  for i in range(1, REPS + 1):
    for j in range(1, FOLDS + 1):
      path = rootDir+'/cv/rep_' + str(i) + '_fold_' + str(j) + '/'
      reader = csv.reader(
        open(path + 'test_algorithm_runs.arff' , 'r'), delimiter = ','
      )
      for row in reader:
        inst = row[0]
        solv = row[2]
        if SCENARIO == "CSP-MZN-2013" or SCENARIO == "COP-MZN-2013":
          time = float(row[4])
          info = row[5]
        else:
          time = float(row[3])
          info = row[4]
        if inst not in runtimes.keys():
          runtimes[inst] = {}
        runtimes[inst][solv] = [time, info]
        
  #changed by Tong
  FEAT_COST = -1
  path_fcp = rootDir + '/feature_cost_process_generated'
  if os.path.exists(path_fcp):
    with open(path_fcp, 'r') as infile:
      feature_cost = json.load(infile)
    path_sunny_process_generated = rootDir + '/sunny_process_generated.csv'
    writer = csv.writer(open(path_sunny_process_generated, 'w'), delimiter = ',')
  else:
    FEAT_COST = 0
    writer = csv.writer(open('sunny.csv', 'w'), delimiter = ',')

  writer.writerow(['instances', 'SUNNY'])  
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
  for i in range(1, REPS + 1):
    for j in range(1, FOLDS + 1):
      path = rootDir+'/cv/rep_' + str(i) + '_fold_' + str(j) + '/'
      reader = csv.reader(open(path + 'predictions.csv' , 'r'), delimiter = ',')
      for row in reader:
        inst = row[0]
        best = [
        	(runtimes[inst][s][0], s) 
        	for s in runtimes[inst].keys()
          if runtimes[inst][s][1] == 'ok'
          and runtimes[inst][s][0] < TIMEOUT
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
        if FEAT_COST == -1:
          time = feature_cost[inst]
        elif FEAT_COST == 0:
          time = FEAT_COST
        solved = False
        rem_time = 0
        for (s, t) in schedule:
          t = float(t)
          t += rem_time
          rem_time = 0
          if runtimes[inst][s][0] <= t and runtimes[inst][s][1] == 'ok':
            time += runtimes[inst][s][0]
            if time < TIMEOUT:
              solved = True
            break
          elif runtimes[inst][s][0] < t and runtimes[inst][s][1] != 'ok':
            rem_time = t - runtimes[inst][s][0]
            time += runtimes[inst][s][0]
          else:
            time += t
          if time >= TIMEOUT:
            break
  	  
        if solved:
          sunny_solved += 1
          sunny_time += time
          writer.writerow([inst, time])
          sunny_mcp += time - min_time
        else:
        	sunny_time += PAR10
        	writer.writerow([inst, PAR10])
        	sunny_mcp += TIMEOUT - min_time
        if runtimes[inst][SBS][1] == 'ok' and runtimes[inst][SBS][0] < TIMEOUT:
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

  if not os.path.exists(result_dir_path):
    os.makedirs(result_dir_path,mode=0777)

  #write results
  with open(result_path, 'w+') as outfile:
    res = ('*** ' + SCENARIO + ' ***' + 
          '\nNo. of instances: '+str(n)+
          '\nSolvable instances: '+str(m)+
          '\n----------'+
          '\nSUNNY PAR10: '+ str(sunny_time / n)+
          '\nSUNNY FSI: '+str(sunny_solved / n) +
          '\nSUNNY MCP: '+str(sunny_mcp / n)+
          '\n----------'+
          '\nSBS PAR10: '+str(sbs_time / n) +
          '\nSBS FSI: '+ str(sbs_solved / n) +
          '\nSBS MCP: '+str(sbs_mcp / n)+
          '\n----------'+
          '\nVBS PAR10: '+ str(vbs_time / n)+
          '\nVBS FSI: '+ str(vbs_solved / n) +
          '\nVBS MCP: 0\n==========')
    outfile.write(res)

# Main

rootDir = "../data/"+ sys.argv[1]
attrnum = sys.argv[2]
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
  portfolio = dic['PORTFOLIO']
  sbs = dic['sbs']
  reps = dic['reps']
  folds = dic['folds']

evaluate(scenario,timeout,numberOfInstances,reps,folds,rootDir,attrnum)