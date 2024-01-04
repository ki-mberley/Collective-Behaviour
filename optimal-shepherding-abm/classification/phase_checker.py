# import libraries
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import time
import os
import sys
sys.path.insert(0, '../plotting/')
from auxiliary_functions import *
from scipy.signal import savgol_filter

costdata = np.loadtxt("../simulation/costdata.txt") # info from costdata file (change function if any changes made to costdata)
parameters = np.loadtxt('../simulation/params.txt') # info from parameter file (change function when params changes)

# load info from parameter file
driving_on, x_target, y_target, vs, vd, ls, ld, fence, fmin_x, fmax_x, fmin_y, fmax_y, num_particles, ndogs, modder = load_params(parameters)
# load info from cost function data file
times, alpha_weight, dog_speed, fourth_moment, xcm, ycm, xd, yd = load_costdata(costdata)

#calculate the angle from the herd CM to the dog
angles = np.arctan2(yd-ycm, xd-xcm)%(2*np.pi)

# angle calculated based on the herd-dog 
angle_zero = np.arctan2(y_target-ycm, x_target-xcm)%(2*np.pi)

angles = angles-angle_zero
angles = angles%(2*np.pi)

filterd_angles = savgol_filter(angles, 3, 2)
derivative = np.gradient(filterd_angles)

x_zeros = []
zero_arrays = []

y_zeros = [filterd_angles[i] for i in zero_arrays] 
x_zeros = [times[i] for i in zero_arrays]

additive = np.zeros(len(times))
additive[:] = filterd_angles[:]

for k in range(len(times)):
    if filterd_angles[k]-filterd_angles[k-1]>np.pi:
        additive[k:] = additive[k:]-2*np.pi
    if filterd_angles[k-1]-filterd_angles[k]>np.pi:
        additive[k:] = additive[k:]+2*np.pi

#driving case, full circle measure -> indicator for closed driving
tmp_command = "tail -" +str(num_particles)+" ../simulation/data.txt > tmpdata.txt"
os.system(tmp_command)
tail_data = np.loadtxt('tmpdata.txt')

tmp_x = tail_data[:,2]
tmp_y = tail_data[:,3]
tmp_xd = tail_data[0,5]
tmp_yd = tail_data[0,6]

tmp_theta = np.arctan2(tmp_y-tmp_yd, tmp_x-tmp_xd)
tmp_theta2 = np.arctan2(y_target-ycm[-1], x_target-xcm[-1])
tmp_theta = tmp_theta-tmp_theta2
tmp_theta = tmp_theta%(2*np.pi)

# create distribution
dtheta = np.pi/2
tmp_axis = np.arange(0,2*np.pi, dtheta)
tmp_dist = np.zeros(np.int_(len(tmp_axis)-1))
angle_stepper = 0

for k in range(len(tmp_axis)-1):
  for p in tmp_theta:
    if p<tmp_axis[k+1]:
      if p>=tmp_axis[k]:
        tmp_dist[k] +=1

# tmp variable
car_closed = 1

for k in tmp_dist:
  if k ==0:
    car_closed = 0

# indicators:
indicator = np.abs(np.max(additive)-np.min(additive))

# new phase-checker for driving
if (x_target-xcm[-1])**2+(y_target-ycm[-1])**2 > (num_particles+num_particles/2)*ls:
  print("Uncontrolled")
  phase = 3
elif car_closed ==1:
    print('driving!')
    phase = 1
else:
  if indicator > 6*np.pi:
    print('mustering V2!')
    phase = 4
  elif indicator > 2*np.pi:
    print("mustering")
    phase = 2
  else: 
    print("droving")
    phase = 0

# print results to file 
file = open("phase_data_tmp.txt", "a")
stuff = str(num_particles) +  " " +  str(ls)+ " "+ str(ld)+ " "+ str(vs) + " "+ str(vd) + " "+ str(phase) +"\n"
file.write(stuff)

file.close()
