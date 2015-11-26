# sunny-fs

Feature selection for SUNNY (closed).


This project has generated the results for the work:


> Roberto Amadini, Fabio Biselli, Maurizio Gabbrielli, Tong Liu, Jacopo Mauro. Feature Selection for SUNNY: a Study on the Algorithm Selection Library. ICTAI, Nov 2015, Vietri sul Mare, Italy.


This is the first time that we executed a systematic study for the impact of FS techniques on SUNNY performance.


Technical notes:


- To change feature selection algorithm, please change the value of 'selection_algorithm' in the fs.py file.
- Sequential execution: Add scenario names to directories.txt file and run main.py, you will test all selected scenarios in one time.
- Parallel execution: create run_(scenario_name).py files(follow the example of run_PREMARSHALLING-ASTAR-2013.py) and then call each file from a different machine.
- Results are generated in data/results/(scenario_name).txt

# NEW results

![Par10](https://github.com/lteu/sunny-fs/blob/master/overview/par10-su.png)

![FSI](https://github.com/lteu/sunny-fs/blob/master/overview/fsi-su.png)

![Par10](https://github.com/lteu/sunny-fs/blob/master/overview/par10-ratio.png)

![FSI](https://github.com/lteu/sunny-fs/blob/master/overview/fsi-ratio.png)

# General results

![Par10](https://github.com/lteu/sunny-fs/blob/master/overview/PAR10-20.04.2015.png)

![FSI](https://github.com/lteu/sunny-fs/blob/master/overview/FSI-20.04.2015.png)

# Ranker FS results

![Par10-ranker](https://github.com/lteu/sunny-fs/blob/master/overview/ranker-par10.png)

![FSI-ranker](https://github.com/lteu/sunny-fs/blob/master/overview/ranker-fsi.png)