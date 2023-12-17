# Collective-Behaviour - Optimal Shepherding 

*Shepherding behaviors* are a class of flocking behaviors in which one or more agents (called *shepherds*) try to control the motion of another group of agents (called *flock*) by exerting repulsive forces. A real-life example are sheep dogs guiding flocks of sheep. *Herding* denotes a special type of shepherding behavior in which the shepherds attempt to steer the flock from a starting point to a target.   

In the context of the course *Collective Behavior*, we decided to investigate the problem of finding optimal herding strategies. To begin our work, we have chosen the paper titled *Optimal Shepherding and Transport of a Flock* by A. Ranganathan, A. Heyde, A. Gupta, and L. Mahadevan as a starting point. This paper models herding as an optimization problem for the shepherd using an agent-based approach.

For the first report we have successfully run the [existing implementation](https://github.com/arphysics/optimal-shepherding/tree/main/ABM_code) of the agent-based model (ABM) and used it to visualize the simulation with a plot and a video. We have also identified the parts of the implementation that are relevant for our project and pushed them to this GitHub repository. While doing so, we corrected the encountered errors and organized the code files in subfolders to make the structure of the implementation easier to understand. 

For the second report we extended the existing implementation with more than one shepherd and a fence. We also adapted the plot and the video to support this extension.

## Structure of this Repository

- `optimal-shepherding-abm` contains our reduced and corrected version of the existing ABM implementation. More details can be found in the `README` of this subdirectory.
- `references` contains the references that we have consulted for conducting our first report.
- `reports` contains the source codes and the prebuilt PDFs of our first and second reports.

## Next Steps

- For the [final report](https://github.com/ki-mberley/Collective-Behaviour/milestone/3) (due by January 08, 2024) we plan to test our model extensions with different parameters and to improve the implementation of these extensions. Additionally, we might implement an existing shepherding algorithm for multiple shepherds and compare its results to the ones of our model.

## Group Members
[Franz Muszarsky](https://github.com/Franz0808)\
[Franziska Weber](https://github.com/franziskaweber)\
[Kimberley Frings](https://github.com/ki-mberley)
