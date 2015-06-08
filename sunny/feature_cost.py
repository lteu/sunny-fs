# this file gets the selected features, chech which feature steps are involve, which features are involved,
# at last, sum up all features costs ...

import os
import sys

def readSelectedFeatures(scenario):
	root = "../data/"+scenario+ "/"
	path_features = root + "selected_feature_values.arff"
	arr = []
	with open(path_features) as ff:
		for line in ff:
			if '@attribute' in line.lower():
			  line = line.strip()
			  splitted = line.split(" ")
			  tmpAttr = splitted[1] + " " + splitted[2].upper()
			  if 'instance_id' not in line.lower() and 'repetition' not in line.lower():
			  	arr.append(splitted[1])
			elif '@data' in line:
			  break
	# print scenario
	return arr


def loadFeatureSteps(scenario):
	arr = {}
	root = "../data/"+scenario+ "/"
	desc_features = root + "description.txt"
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


def createSelectedFeatureCostFile(root,selected_steps):
	feature_positions = []
	# out = []
	out = ""
	dataMode = False
	attributeCount = -1
    # idxAlg = -1
    # idxTime = -1
    # idxScore = -1
    # isFair = True

	feature_costs = root + "/feature_costs.arff"
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



scenario = sys.argv[1]

root = "../data/"+scenario
path_feature_cost = root + '/feature_costs.arff'
path_selected_feature_cost = root + '/selected_feature_costs.arff'
path_out_feature_cost = root + '/select_feature_costs.arff'
desc_features = root + "/description.txt"

if not os.path.exists(path_feature_cost):
	print "Feature cost ZERO for '" + path_feature_cost + "'"
elif not os.path.exists(desc_features):
	command = 'cp ' + path_feature_cost + ' '+ path_selected_feature_cost
	os.system(command)
	print "Feature cost description not found for '" + path_feature_cost + "' so feature_cost copied ..."
else:
	feature_steps = loadFeatureSteps(scenario)
	# print 'steps: ', feature_steps
	selected_features = readSelectedFeatures(scenario)
	# print 'features: ', selected_features
	selected_steps = getInvolvedSteps(feature_steps,selected_features)
	selected_steps = list(set(selected_steps))
	# print selected_steps
	out = createSelectedFeatureCostFile(root,selected_steps)

	print 'step: ',selected_steps
	# print 'out ', out

	with open(path_out_feature_cost, 'w+') as outfile:
		outfile.write(out)
	print "Feature cost filtered for ", scenario ,' ...'

