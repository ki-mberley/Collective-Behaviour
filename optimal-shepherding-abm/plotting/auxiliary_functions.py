# load libraries needed in functions
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import OrderedDict 

# prevents a warning from arising when saving still images for the ffmpeg movie
plt.rcParams.update({'figure.max_open_warning': 0})

'''
This file contains all the functions required for plotting and further analysis in python. )

------------------------------------------------FUNCTIONS BELOW---------------------'''

def colorator(theta):
    """
    Defines a color-scheme for plotting sheep headings. I.e., defines a 1:1 function between heading angle and color.
    Is used to check that neighboring particles (via Vicsek alignment) are of similar colors. 

    --------------
    param theta: angle corresponding to sheep heading
    --------------
    """

    t0 = theta
    t1 = theta-2*np.pi/3
    t2 = theta+2*np.pi/3
    return 0.45*(1+np.cos(t0)), 0.45*(1+np.cos(t1)), 0.45*(1+np.cos(t2))


def load_params(parameters):
    '''
    Loads parameters from a parameter file. Used for parsing data, plotting, and other python analysis. 
    Function is HARDCODED to associate specific lines in parameter file with specific variable.

    -----------
    param parameters: .txt file with parameters for C++ code
    -----------
    '''

    num_particles = int(parameters[1]) # number of particles 
    ndogs = int(parameters[2]) # number of dogs
    vs = parameters[5] # sheep speed
    vd = parameters[6] # dog speed
    ls = parameters[9] # sheep-sheep repulsion length scale
    ld = parameters[10] # dog-sheep repulsion length scale
    x_target = parameters[16] # herd target location x-axis
    y_target = parameters[17] # herd target location y-axis
    driving_on = parameters[30]
    fence = parameters[33] # whether there is a fence or not
    fmin_x = parameters[34] # position of left fence
    fmax_x = parameters[35] # position of right fence
    fmin_y = parameters[36] # position of bottom fence
    fmax_y = parameters[37] # position of top fence
    modder = int(parameters[-1]) # how often to plot

    return driving_on, x_target, y_target, vs, vd, ls, ld, fence, fmin_x, fmax_x, fmin_y, fmax_y, num_particles, ndogs, modder


def load_costdata(costdata):
    '''
    Loads the cost-function data into python for plotting and analysis. Note, this function is HARDCODED and depends on the C++
    print statement to the costdata text file. If costdata file is changed, this function MUST BE CHANGED!

    -----------
    param costdata: .txt file with evaluation of cost-function and related metrics at each timestep.
    -----------
    '''

    times = costdata[:,0]
    alpha_weight = costdata[:,1]
    dog_speed = costdata[:,2]
    fourth_moment = costdata[:,3]
    xcm = costdata[:,4]
    ycm = costdata[:,5]
    xd = costdata[:,6]
    yd = costdata[:,7]

    return times, alpha_weight, dog_speed, fourth_moment, xcm, ycm, xd, yd


def load_data(dat_field, num_particles):
    '''
    Loads the main simulation data into python for plotting and analysis. Note, this function is HARDCODED and depends on the C++
    print statement to data.txt file. DO NOT CHANGE dump to data.txt file--doing so would void many dependencies and require
    significant code changes.

    -----------
    param data_field: main .txt file with position and trajectory of all particles (herder and herded) at each timestep
    param num_particles: number of agents
    -----------
    '''

    # particles in this sample case
    xpart = dat_field[:,2] # data subframe of x positions for each particle at each timestep 
    ypart = dat_field[:,3] # data subframe of y positions for each particle at each timestep 
    thetapart = dat_field[:,4] # data subframe of orientations for each particle at each timestep 

    # creating a dog matrix
    x_dogs = dat_field[:,5::2] # data subframe of x positions for each herder at each timestep 
    y_dogs = dat_field[:,6::2] # data subframe of y positions for each herder at each timestep

    # set info on timesteps
    dat_times = dat_field[:,0] # data subframe of time values, includes repitition for each particle
    timesteps = int(len(dat_times)/num_particles) # calculate number of timesteps total
    times = np.arange(0,timesteps,1) # cleaned time array for plotting and analysis purposes

    return xpart, ypart, thetapart, x_dogs, y_dogs, dat_times, timesteps, times
  

def sanity_checks(dat_field, num_particles, ndogs, timesteps):
    '''
    This function conducts several sanity checks to ensure the results are sensible, in particular that the data 
    loaded into python for analysis and display agrees with what is expected from the C++ code. 

    Current sanity checks include: 

      *Checking that the number of sheep calculated from the data file equals the number of sheep in the param file
      *Checking that the number of dogs calculated from the data file equals the number of dogs in the param file

    -----------
    param data_field: main .txt file with position and trajectory of all particles (herder and herded) at each timestep
    param num_particles: number of agents listed in param file
    param ndogs: number of dogs listed in param file
    param timesteps: number of timesteps listed in param file
    -----------
    '''

    # check number of sheep
    particles = dat_field[:,1]
    tmp_count = int(np.max(particles) + 1)
    if tmp_count != num_particles: 
        print("Abort! Incorrect number of particles.")

    # check number of dogs
    tmp_count = int((np.shape(dat_field)[1]-5)/2)
    print("Looking at data & performing sanity checks...")

    if tmp_count != ndogs: 
        print("Ndogs, num_dogs = ", ndogs, tmp_count)
        print("Abort! Incorrect number of dogs.")

    print("There are ", num_particles, "sheep!")
    print("There are ", ndogs, "dogs!")
    print("There are", timesteps, "frames of dumped data!")


def plot_fence(L, x_target, y_target, ld):
    # built-in wall
    xwall = np.linspace(-L,y_target-0.5*ld,50);
    xt_array = [x_target for i in range(len(xwall))]
    ywall = np.linspace(x_target,L,50)
    yt_array = [y_target+0.5*ld for i in range(len(xwall))]

    return xwall, ywall, xt_array, yt_array


def make_movie():
  '''
  This function converts the images saved in a temp folder to an mp4 movie using ffmpeg. 
  '''

  # hardcoded name for the output movie file
  print("Making a movie! Movie will be called 'output_movie.mp4'") 
  
  # run ffmpeg
  os.system("ffmpeg -loglevel panic -y -r 15 -f image2 -s 1920x1080 -start_number 1 -i ./plots/plot%04d.png -vframes 1000 -vcodec libx264 -crf 10  -pix_fmt yuv420p plots/output_movie.mp4")
  
  # clear the saved images from temp folder
  print("Movie made...clearing individual plots")
  os.system('rm plots/plot*') # hardcoded temp folder name
  
  # open the created movie
  os.system("open plots/output_movie.mp4")
