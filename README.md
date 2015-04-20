# sunny-fs
In this project branch, we applicate the feature selection algorithms to a dataset which is then used in the sunny experiment.

- To change feature selection algorithm, please change the value of 'selection_algorithm' in the fs.py file.
- Sequential execution: Add scenario names to directories.txt file and run main.py, you will test all selected scenarios in one time.
- Parallel execution: create run_(scenario_name).py files(follow the example of run_PREMARSHALLING-ASTAR-2013.py) and then call each file from a different machine.
- Results are generated in data/results/(scenario_name).txt


***Par10***
![Par10](https://github.com/lteu/sunny-fs/blob/master/overview/PAR10-20.04.2015.png)

***FSI***
![FSI](https://github.com/lteu/sunny-fs/blob/master/overview/FSI-20.04.2015.png)