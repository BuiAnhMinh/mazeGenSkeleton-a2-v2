The main script is mazeTester2.py.

There are five sample configuration files which specify the parameters used to run assignment 2.:

sampleConfig-1-1.json and sampleConfig-2-1.json read mazes from sampleMaze01.txt and sampleMaze02.txt files and solve them using the recursive solver.
sampleConfig-1-3.json and sampleConfig-2-3.json generates and solves the mazes using the recursive generator and solver.
sampleConfig-TaskBC.json uses the brute force approach to solve the maze in Task B.


To run the script, go to the same folder/directory that this README.txt file is located, and execute:

On Windows:
    python mazeTester2.py sampleConfig-1-1.json
On Unix, particularly core teaching servers:
    python3 mazeTester2.py sampleConfig-1-1.json


On the core teaching servers, matplotlib isn't installed, hence visualisation won't work.  Please run the visualisation on your own machines.

Please avoid modifying the provided files, apart from implementing the specified scripts (check the first line in each .py file).
If you must modify anything, please check in with the teaching team first.

Please note that the main differences between the configuration files for Task A versus Task B and C are:

* For Task A, we need the "solverEntranceIndex" key since it will specify the index of the entrance that the solver needs to focus on. 
  For task B and C, the configuration file should not include any entry for "solverEntranceIndex".

** For task B and C, the number of entrances and exits must be the same and the program needs to focus on finding paths
   between (entrance[0], exit[0]), (entrance[1], exit[1])...(entrance[k], exit[k])

*** For all tasks, it is now possible to read a maze from a file. 
If mazeFromFile = true, then the program expects to recieve a file name (in the same folder/directory) or a file path.
The maze files are structured as follows:

odd lines (#cols*2 - 1): cellWeight wallStatus cellWeight wallStatus ..... cellWeight
even lines (#cols): wallStatus wallStatus ...... wallStatus