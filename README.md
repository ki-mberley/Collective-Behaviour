# Collective-Behaviour - Optimal Shepherding 

![output_movie](https://github.com/ki-mberley/Collective-Behaviour/assets/102147723/5a87f6ff-c0e0-4acd-b6fb-afc9ee4eb9eb)

## Project Description

*Shepherding behaviors* are a class of flocking behaviors in which one or more agents (called *shepherds*) try to control the motion of another group of agents (called *flock*) by exerting repulsive forces. A real-life example are sheepdogs guiding flocks of sheep. *Herding* denotes a special type of shepherding behavior in which the shepherds attempt to steer the flock from a starting point to a target.   

In the context of the course *Collective Behavior*, we investigated the problem of finding optimal herding strategies. Our work builds upon the paper [*Optimal Shepherding and Transport of a Flock*](https://www.semanticscholar.org/paper/Optimal-shepherding-and-transport-of-a-flock-Ranganathan-Heyde/f8f559f5ee1a5a9337130325dc3930d49a9b77c0) by A. Ranganathan, A. Heyde, A. Gupta, and L. Mahadevan. This paper models herding as an optimization problem for the shepherd using an agent-based approach and identifies three different herding strategies, namely *mustering*, *droving*, and *driving*.

## Goals

Our initial goal was to extend the [existing implementation](https://github.com/arphysics/optimal-shepherding/tree/main/ABM_code) of the agent-based model (ABM) to support more than one shepherd. We also wanted to investigate which herding strategies emerge in the case of multiple shepherds. 

As the project progressed, the comparison of our model to an existing shepherding algorithm for multiple shepherds emerged as an additional goal.

## Achievements

We started by identifying the parts of the existing implementation that were relevant to our project. While doing so, we corrected the encountered errors and organized the code files in subfolders to make the structure of the implementation easier to understand. 

Next, we extended the existing implementation with more than one shepherd by adjusting the objective function. We also added the possibility of having a surrounding fence to the model.

Lastly, we studied the effects of our extensions by testing different parameter values. We also implemented a basic version of the shepherding algorithm from the paper [*Simulating Single and Multiple Sheepdogs Guidance of a Sheep Swarm*](https://link.springer.com/chapter/10.1007/978-3-030-60898-9_3) and started comparing it to our implementation.

What remains to be done is to analyze our extensions in even more detail to find out which herding strategies emerge in the multiple shepherd scenario.

## Structure of this Repository

- `optimal-shepherding-abm` contains our reduced, corrected, and extended version of the existing ABM implementation. More details can be found in the `README` of this subdirectory.
- `presentation` contains the slides for our final presentation.
- `reports` contains the source codes and the prebuilt PDFs of our three reports.

## Group Members
[Franz Muszarsky](https://github.com/Franz0808)\
[Franziska Weber](https://github.com/franziskaweber)\
[Kimberley Frings](https://github.com/ki-mberley)
