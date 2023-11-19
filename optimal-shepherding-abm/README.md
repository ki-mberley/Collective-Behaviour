# Optimal Shepherding - Agent-Based Model

This code is a reduced and corrected version of the [implementation of the ABM](https://github.com/arphysics/optimal-shepherding/tree/main/ABM_code) by Aditya Ranganathan which was written to explore the herding phenomenon via agent-based simulations. Results corresponding to this original implementation are described in the paper [Optimal shepherding and transport of a flock](https://www.semanticscholar.org/paper/Optimal-shepherding-and-transport-of-a-flock-Ranganathan-Heyde/f8f559f5ee1a5a9337130325dc3930d49a9b77c0) by Alexander Heyde, Aditya Ranganathan, Anupam Gupta, and Lakshminarayanan Mahadevan.

## Running the Code

The code to run the simulation is written in C++ using an object-oriented approach and can be found in the subdirectory `simulation`. Plotting is done using python and the corresponding code is contained in the subdirectory `plotting`. This repository already contains the files that you will get by following the steps below as examples.
 
### Running the Simulation

To run the simulation, carry out the following steps:

	cd simulation
	make
	./simulate

The `make`-command compiles the file `simulate.cpp`. Running the simulation with `./simulate` creates the files `data.txt` and `costdata.txt`. The former contains the positions of every agent and of the shepherd and the latter the value of the objective function at each timestep which is useful for analysis and debugging.

The file `params.txt` sets the parameters for the simulation and is designed such that editing the file does not require a new `make`-command before running a new simulation.

### Generating Plots and Videos

First of all, switch to the correct subdirectory and install the dependencies:

	cd ../plotting
 	mkdir plots
	pip install -r requirements.txt
	sudo apt install -y ffmpeg

Now run `trajectory_plotter.py` via `python3 trajectory_plotter.py` to create the plot `plotting/plots/output_plot.pdf`. This plot displays the trajectory of the agents and of the shepherd over time based on the data from `simulation/data.txt` and `simulation/params.txt`. It also shows snapshots of the agents and the shepherd at four times which include the initial and the final time. 

Next run `visualizer.py` via `python3 visualizer.py` to create the video `plotting/plots/output_movie.mp4`. This programm reads in the data from `simulation/data.txt` and `simulation/params.txt` and converts it to a stacked time series of scatter plots.
