# Data preprocessing practice



## New York City Car crashes

This is the first data set. 
It contains data about car crashes in New York City. 
The goal of [this exercise](https://github.com/becodeorg/ANT-Theano-2-27/blob/main/4.machine_learning/projects/0.data_preprocessing/1.nyc_crashes.md) is to clean up the data using Pandas, and prepare it for machine learning.

In order to inspect the data and develop my cleaning process, I used a [Jupyter Notebook](NYC_Crashes.ipynb), which can be read to follow my thought process.
Then I collected all the steps I took in one **script** [crashes.py](crashes.py), that can be used to clean an arbitrary csv file (of the same format). 
I haven't built in any safety checks, so be careful not to overwrite any files.

```
python crash.py INPUT.csv OUTPUT.csv
```

Resulting datasets can be found in [RESULT_1000.csv](RESULT_1000.csv) and [RESULT_100000.csv](RESULT_100000.csv.xz).
The latter is compressed with `xz`, but can be imported just like that with Pandas. 


## New York City trees

Very similar to the first exercise, so less documented. 
Inpecting and experimentation is done in the [notebook](NYC_Trees.ipynb), the final script is called [trees.py](trees.py). 

```
python trees.py INPUT.csv OUTPUT.csv
```