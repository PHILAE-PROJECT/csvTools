# csvTools

Directory csvtools includes several tools to handle the csv files of the scanette project. Some of these tools also accept Agilkia JSON files as input, and are not specific to the scanette project.
The current tools are:
- *ProjectionCSV.py* : takes a csv trace, made up of several client sessions, and splits it into individual sessions, each stored in a csv file.
- *ExecuteTraceOpti.py* : plays all csv files of a given directory against the scanette mutants
- *ReduceTestSuite.py* : clusters the csv files of a given directory, based on abstractions of the events, and picks one csv file in each cluster
- *UniqueObjects.py* : changes the name of the `caisse` and `scan` objects so that their number is prefixed by the client number.

More documentation is provided in the headers of these python files. Most of these tools are associated to a GUI. 
`ReduceTestSuite_GUI.py` combines test suite reduction and evaluation on mutants.


## Examples

### Splitting a file
Let us split the csv file `1026-steps.csv` located in the `traces` directory

```
ProjectionCSV.py traces/1026-steps.csv
```

This will create a directory `traces/projectedTraces/1026-steps` where the 61 sessions are stored as csv files.

### Evaluating a csv file or a set of csv files against mutants

The following command must be executed in a directory which includes the `resources` subdirectory. 
*The python script must be modified* in such a way that variable `absolutePath` points to the directory storing `scanette.jar` and the mutants.
 
```
ExecuteTraceOpti.py traces/1026-steps.csv
```

The same command can be played on a directory including several csv files (here the 61 individual sessions of `1026-steps.csv`)

```
ExecuteTraceOpti.py traces/projectedTraces/1026-steps
```

You will notice that the individual sessions don't kill the same number of mutants as the original `1026-steps.csv` file.

In optimized mode, the program avoids executing mutants that have already been killed by a previous test case.
You can change it by modifying variable `optimizedMode`.

### Clustering csv test cases, and reducing the test suite

Script `ReduceTestSuite.py` takes as argument a directory with test cases stored as csv files, and an abstraction function. 
It applies the abstraction function to each of the test cases and clusters the test cases based on their abstraction.

```
ReduceTestSuite.py traces/projectedTraces/1026-steps OpNames_Seq_NoSt
```

Using abstraction function `OpNames_Seq_NoSt` produces 11 clusters. The program also copies 
one test case per abstraction into directory `traces/projectedTraces/1026-steps/reducedTS-Opnames_Seq_NoSt`.
If this directory already exists and is not empty, the program halts and does not copy the reduced test suite.

You can now evaluate this reduced test suite against the mutants:

```
ExecuteTraceOpti.py traces/projectedTraces/1026-steps/reducedTS-Opnames_Seq_NoSt
```

In this case, the reduced test suite kills 19 mutants.

The following abstraction functions are available:

```
	OpNames_Set
	OpNamesAndRet_Set
	OpNamesAndAbsRet_Set
	OpNames_Bag
	OpNamesAndRet_Bag
	OpNamesAndAbsRet_Bag
	OpNames_Seq
	OpNamesAndRet_Seq
	OpNamesAndAbsRet_Seq
	OpNames_Seq_NoSt
	OpNamesAndRet_Seq_NoSt
	OpNamesAndAbsRet_Seq_NoSt
```

Use them as the second argument of the ReduceTestSuite script.	It is also possible to activate the 
subsumption check, which deletes the clusters that are subsumed by a larger cluster. 
This is activated by an integer in the API or through the GUI. When subsumption is activated, an
appropriate function (subset, subbag, prefix, matchedBy) is selected depending on the initial abstraction function.

### Using unique objects

Script `UniqueObjects.py` changes the names of `caisse` and `scan` objects  of the csv or json file given 
as argument, so that their number is prefixed by the client number.
As a result, there can no longer exist interactions between sessions because they will not share objects.
If the argument is a directory, the transformation is applied to all csv files of the directory (json files are not supported). The GUI adds the option that 
the resulting sessions are grouped in a single file.

For example, the following command will transform file `1026-steps.csv` into `1026-steps-U.csv`.

```
UniqueObjects.py traces/1026-steps.csv
```
known bug: sometimes UniqueObjects.py falls into an infinite loop when processing a directory for the second time.
It then creates an enormous csv file. 



 


 