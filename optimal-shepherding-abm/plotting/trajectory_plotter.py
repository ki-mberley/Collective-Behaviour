# python3

# import libraries
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import time
from auxiliary_functions import *

import warnings
warnings.filterwarnings("ignore")

L = 10 # size of domain to plot

t0 = time.time()

dat_field = np.loadtxt('../simulation/data.txt') # x,y position data for herd and dogs
parameters = np.loadtxt('../simulation/params.txt') # info from parameter file (change function when params changes)

# load info from parameter file
driving_on, x_target, y_target, vs, vd, ls, ld, fence, fmin_x, fmax_x, fmin_y, fmax_y, num_particles, ndogs, modder = load_params(parameters)

# load info from data file
xpart, ypart, thetapart, x_dogs, y_dogs, dat_times, timesteps, times, = load_data(dat_field, num_particles)

sanity_checks(dat_field, num_particles, ndogs, timesteps)

# calculate mean sheep trajectory
xmeans = np.zeros(timesteps)
ymeans = np.zeros(timesteps)

# plot the trajectories
print('plotting trajectory')
alpha = 1
for i in range(timesteps):
    alpha = alpha -.9 / timesteps
    index = num_particles * i
    tmp_x = xpart[index: index+num_particles]
    tmp_y = ypart[index: index+num_particles]
    xmeans[i] = np.mean(tmp_x)
    ymeans[i] = np.mean(tmp_y)

def colored_line(x, y, z=None, linewidth=1, MAP='jet'):
    # this uses pcolormesh to make interpolated rectangles
    xl = len(x)
    [xs, ys, zs] = [np.zeros((xl, 2)), np.zeros((xl, 2)), np.zeros((xl, 2))]

    # z is the line length drawn or a list of vals to be plotted
    if z == None:
        z = [0]

    for i in range(xl - 1):
        # make a vector to thicken our line points
        dx = x[i + 1] - x[i]
        dy = y[i + 1] - y[i]
        perp = np.array([-dy, dx])
        unit_perp = (perp / np.linalg.norm(perp)) * linewidth

        # need to make 4 points for quadrilateral
        xs[i] = np.array([x[i], x[i] + unit_perp[0]]).flatten()
        ys[i] = np.array([y[i], y[i] + unit_perp[1]]).flatten()
        xs[i+1] = np.array([x[i+1], x[i+1] + unit_perp[0]]).flatten()
        ys[i+1] = np.array([y[i+1], y[i+1] + unit_perp[1]]).flatten()

        if len(z) == i + 1:
            z.append(z[-1] + (dx ** 2 + dy ** 2) ** 0.5)

        # set z values
        zs[i] = np.array([z[i], z[i]]).flatten()
        zs[i + 1] = np.array([z[i + 1], z[i + 1]]).flatten()

    return xs, ys, zs

# calculate dog trajectory at each time step
xdogs = x_dogs[::num_particles][:-1]
ydogs = y_dogs[::num_particles][:-1]

# calculate dog trajectory at each time step
xdogs = x_dogs[::num_particles][:-1]
ydogs = y_dogs[::num_particles][:-1]

# store variables
xs, ys, zs = colored_line(xmeans, ymeans, linewidth = .3)

# make the plots
fig, ax = plt.subplots(figsize = (15, 10))
ax.pcolormesh(xs, ys, zs, shading='gouraud', cmap='Blues', label = 'Sheep')

for i in range(ndogs):
    xd, yd, zd = colored_line(xdogs[:, i], ydogs[:, i], linewidth = .05)
    ax.pcolormesh(xd, yd, zd, shading='gouraud', cmap='Greys', label = 'Dogs')

ax.scatter(x_target, y_target, c = 'Orange', marker = 'D', s = 50, label = 'target')
if fence == 1:
    ax.hlines([fmin_y, fmax_y], fmin_x, fmax_x)
    ax.vlines([fmin_x, fmax_x], fmin_y, fmax_y)

alpha = 1
c_index = 0 # variable to select a color as a function of time

# set max time
maxtime = timesteps;

def plot_positions(ax, time, color):
    index = num_particles * time
    tmp_x = xpart[index: index + num_particles]
    tmp_y = ypart[index: index + num_particles]

    ax.scatter(tmp_x, tmp_y, c = color, s = 2, label = 'sheep at time '+ str(time))
    ax.scatter(x_dogs[index], y_dogs[index], c = color, s = 100, marker = '^', label = 'dog at time '+ str(time))


for time, color in zip(range(0, maxtime, maxtime // 3), ['Purple', 'Cyan', 'Red']):
    plot_positions(ax, time, color)

plot_positions(ax, maxtime - 1, 'Blue')

ax.legend()
plt.title('Trajectories over time')
plt.xlabel('x motion')
plt.ylabel('y motion')
plt.xlim(-L,L)
plt.ylim(-L,L)
plt.savefig('plots/output_plot.pdf')
