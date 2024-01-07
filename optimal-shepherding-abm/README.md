# Optimal Shepherding - Agent-Based Model

This code is a reduced, corrected, and extended version of the [implementation of the ABM](https://github.com/arphysics/optimal-shepherding/tree/main/ABM_code) by Aditya Ranganathan which was written to explore the herding phenomenon via agent-based simulations. Results corresponding to this original implementation are described in the paper [*Optimal shepherding and transport of a flock*](https://www.semanticscholar.org/paper/Optimal-shepherding-and-transport-of-a-flock-Ranganathan-Heyde/f8f559f5ee1a5a9337130325dc3930d49a9b77c0) by Alexander Heyde, Aditya Ranganathan, Anupam Gupta, and Lakshminarayanan Mahadevan.

## Running the Code

The code to run the simulation is written in C++ using an object-oriented approach and can be found in the subdirectory `simulation`. Plotting is done using Python and the corresponding code is contained in the subdirectory `plotting`.
 
### Running the Simulation

To run the simulation, carry out the following steps:

	cd simulation
	make
	./simulate

The `make`-command compiles the file `simulate.cc`. Running the simulation with `./simulate` creates the files `data.txt` and `costdata.txt`. The former contains the positions of every agent and of the shepherd and the latter the value of the objective function at each timestep which is useful for analysis and debugging.

The file `params.txt` sets the parameters for the simulation and is designed such that editing the file does not require a new `make`-command before running a new simulation. The subdirectory `simulation/example-params` contains the three exemplary parameter sets `driving.txt`, `droving.txt` and `mustering.txt` which lead to the emergence of the corresponding shepherding behaviours. 

By setting the value of `num_dogs` in `params.txt`, you can specify the number of shepherds. By setting the value of `fence` to `1`, you introduce a surrounding fence to the model.

If you want to remove the randomness from the model to make different simulation runs comparable, simply comment in line 12 and comment out line 13 in `simulate.cc`.

### Generating Plots and Videos

First of all, switch to the correct subdirectory and install the dependencies:

	cd ../plotting
 	mkdir plots
	pip install -r requirements.txt
	sudo apt install -y ffmpeg

Now run `trajectory_plotter.py` via `python3 trajectory_plotter.py` to create the plot `plotting/plots/output_plot.pdf`. This plot displays the trajectory of the agents and of the shepherd over time based on the data from `simulation/data.txt` and `simulation/params.txt`. It also shows snapshots of the agents and the shepherd at four times which include the initial and the final time. 

Next run `visualizer.py` via `python3 visualizer.py` to create the video `plotting/plots/output_movie.mp4`. This program reads in the data from `simulation/data.txt` and `simulation/params.txt` and converts it to a stacked time series of scatter plots.

### Classifying the Shepherding Behaviour

Again, start by changing to the correct subdirectory:

	cd ../classification

Now run `phase_checker.py` via `python3 phase_checker.py`. This will display the type of shepherding behaviour (`driving`, `mustering`, `droving` or `uncontrolled`) on the console.

### Running the Agent-based Shepherd Model for Comparison

The agent-based shepherd model can be executed analogously to our optimization-based model by carrying out the following steps:

	cd simulation
	make
	./simulate_shepherd_agent_model

The specific parameters for this model are contained in the file `params_shepherd_abm.txt`. Once again, editing this file does not require a new `make`-command before running a new simulation. 

If you want to remove the randomness from the model to make different simulation runs comparable, again simply comment in line 12 and comment out line 13 in `simulate_shepherd_agent_model.cc`.

Plots and videos for this alternative shepherding model can be created in the same way as described above.
