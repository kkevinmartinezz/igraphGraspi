# graspi_igraph

Python-Igraph is a graph-based library contender for the library that works with the GraSPI package. 

This repository contains the implementation to test basic algorithm requirements that need to be met for this package to work similarly to GraSPI.
The basic algorithm requirements include:
  -  Construction of graphs
  -  Graph Filtering
  -  Determine the number of connected components
  -  Determine the shortest path from the bottom boundary to all black vertices until the white vertices are met
  -  Graph visualization

## Installation
Downloads needed can be found in requirements.txt
```
pip install igraph 
pip install matplotlib
```
  If there are any issues with installation, please visit: https://python.igraph.org/en/stable/

## Git Cloning Into Project 
If you wish to use this package the same exact way the repo is built, you will need to git clone this repo into your own project.

In order to do this you will need to do the following (based on using Pycharm):
1. Go to the main page of this repo.
2. Click on the green button that says "<> Code" in the top right.
3. A drop down window will appear.
4. click on "SSH".
5. copy the line of code.
6. Then open a new project in your IDE of choice (PyCharm was used for creating this REPO)
7. open a terminal.
8. enter the following command: git clone <paste line of code copied in step 5>.
9. This should import the entire repo. If not then you may need to activate GitHub addons into your IDE of choice.
## Testing from Command Line
Now that we have cloned the REPO lets talk about testing.

In this Github Repo, all the tests are in the test directory. Furthermore, within this directory are two more directories: 2D-testFile and 3D-testFile.
Inside these directories, some files hold information about either 2d or 3d graphs based on the directory name. 
When running from command lines you will need to know the complete pathname of the test file you are trying to run.

The command line input to run a graph creation will have the following format
```
python igraphGraspi/igraphGraspi/igraph_testing.py {total pathname of test file} {2d or 3d}
```
If you have the same test directories as this GitHub Repo you should be able to run the following command line argument to output a 2D 10x10 graph.
```
python igraphGraspi/igraphGraspi/igraph_testing.py igraphGraspi/tests/2D-testFile/testFile-10-2D.txt 2d

```
**Output of Command Line Input**
If the pathname is correct and it is properly stated whether it is a 2d or 3d graph creation, a pop-up window should appear with the visualization of the initial graph creation will appear. 
if you exit out of this pop-up window, then another will appear with the visualization of the filtered version of the same graph. 
If this doesn't occur then you either did not follow the pathname of the test-file correctly or did not state that the graph is either 2d or 3d. 
 
# Outputting Runtime and Memory data into CSV file
```
if __name__ == '__main__':
    # main()
csv_testing()
```
1. In the function above, comment out the main() and uncomment csv_testing()
2. Now since we want to get the total runtimes and memory usage of 5 testcases you will need to add all 5 2-D testcases in the tests/2D-testFile directory as the inputs in this order: 10x10, 50x50, 100x100, 500x500, 1000x1000.
3. Example command is as followed: igraphGraspi/igraph_testing.py tests/2D-testFile/testFile-10-2D.txt tests/2D-testFile/testFile-50-2D.txt tests/2D-testFile/testFile-100-2D.txt tests/2D-testFile/testFile-500-2D.txt tests/2D-testFile/testFile-1000-2D.txt
4. This will run tests for all of these testfiles and document the total memory and runtime usage of all of them in a file named Current_Test.csv.
5. This will take a while to run but when it is done make sure data has been documented in the Current_Test.csv file


