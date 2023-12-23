#python3

#import libraries
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import time
import os
from auxiliary_functions import *


#set user defined parameters

L = 6 #size of domain to plot

t0 = time.time()

dat_field = np.loadtxt('../simulation/data.txt') #x,y position data for herd and dogs

# Load info from parameter file
parameters = np.loadtxt('../simulation/params.txt')
driving_on, x_target, y_target, vs, vd, ls, ld, fence, fmin_x, fmax_x, fmin_y, fmax_y, num_particles, ndogs, modder = load_params(parameters)

# Load info from data file
xpart, ypart, thetapart, x_dogs, y_dogs, dat_times, timesteps, times, = load_data(dat_field, num_particles)

sanity_checks(dat_field, num_particles, ndogs, timesteps)


def colored_line(x, y, lab, z=None, linewidth=1, MAP='jet'):
    # This uses pcolormesh to make interpolated rectangles
    xl = len(x)
    [xs, ys, zs] = [np.zeros((xl, 2)), np.zeros((xl, 2)), np.zeros((xl, 2))]

    # z is the line length drawn or a list of vals to be plotted
    if z == None:
        z = [0]

    for i in range(xl - 1):
        # Make a vector to thicken our line points
        dx = x[i + 1] - x[i]
        dy = y[i + 1] - y[i]
        perp = np.array( [-dy, dx] )
        unit_perp = (perp / np.linalg.norm(perp)) * linewidth

        # Need to make 4 points for quadrilateral
        xs[i] = np.array([x[i], x[i] + unit_perp[0] ]).flatten()
        ys[i] = np.array([y[i], y[i] + unit_perp[1] ]).flatten()
        xs[i+1] = np.array([x[i + 1], x[i + 1] + unit_perp[0] ]).flatten()
        ys[i+1] = np.array([y[i + 1], y[i + 1] + unit_perp[1] ]).flatten()

        if len(z) == i + 1:
            z.append(z[-1] + (dx ** 2 + dy ** 2) ** 0.5)
        # Set z values
        zs[i] = np.array([z[i], z[i] ]).flatten()
        zs[i+1] = np.array([z[i + 1], z[i + 1] ]).flatten()
        
    return xs, ys, zs

counterr = 0
for t in range(timesteps):
    if t % modder == 0:
        counterr += 1
        
        # Download particle data
        index = num_particles*t
        tmp_x = xpart[index: index + num_particles]
        tmp_y = ypart[index: index + num_particles]
        tmp_theta = thetapart[index: index + num_particles]

        # Calculate the angle between the target and the dog (ONLY FOR 1 DOG)
        tmp_target_angle = np.arctan2(y_target - y_dogs[index, 0], x_target - x_dogs[index, 0])

        # Set color info
        tmp_colors = tmp_theta - tmp_target_angle#%(2*np.pi) #colorator(tmp_theta)

        # Plot herd CM
        x_avg = np.average(tmp_x)
        y_avg = np.average(tmp_y)

        tmp_herd_dog_angle = (np.pi / 2 - np.arctan2(y_target - y_avg, x_target - x_avg))

        rot_x_center = x_avg
        rot_y_center = y_avg

        # Rotate positions about x_avg and y_avg
        tmp_x_2 = (tmp_x - rot_x_center) * np.cos(tmp_herd_dog_angle) - (tmp_y - rot_y_center) * np.sin(tmp_herd_dog_angle)
        tmp_y_2 = (tmp_y - rot_y_center) * np.cos(tmp_herd_dog_angle) + (tmp_x - rot_x_center) * np.sin(tmp_herd_dog_angle)

        # fig, (ax2, ax1) = plt.subplots(1, 2, figsize = (16, 8))
        # ax1.set_aspect('equal')
        # ax2.set_aspect('equal')
        fig, (ax) = plt.subplots(1, 1, figsize = (16, 8))
        ax.set_aspect('equal')
        title = 'System at time = ' + str(int(dat_times[index]))
        fig.suptitle(title)
        name = './plots/plot' + str(counterr).zfill(4)

        # Figure out the right size
        scale_sheep = 5 * np.std(tmp_x)
        scale_dog = 1.2 * np.sqrt((x_dogs[index, 0] - x_avg) ** 2 + (y_dogs[index, 0] - y_avg) ** 2) #hardcoded for 1 dog

        scale = np.max([scale_dog, scale_sheep])

        # removed the video on the right side
        """ 
        ## Clone view
        clone_view = 1

        if clone_view:
            # Generate color-map-------------------
            angle_array = np.linspace(-np.pi, np.pi, 500)
            # angle_array = [ii - tmp_target_angle for ii in angle_array]
            x_offset = scale-scale / 4
            y_offset = scale-scale / 4
            x_colors_p = scale / 5 * np.cos(angle_array)
            y_colors_p = scale / 5 * np.sin(angle_array)

            x_colors = x_colors_p * np.cos(tmp_herd_dog_angle) - y_colors_p * np.sin(tmp_herd_dog_angle) + x_offset
            y_colors = y_colors_p * np.cos(tmp_herd_dog_angle) + x_colors_p * np.sin(tmp_herd_dog_angle) + y_offset

            angle_colors = [colorator(p) for p in angle_array]
            ax1.scatter(x_colors, y_colors, color = angle_colors)


            #ax1.scatter(tmp_x_2, tmp_y_2, c = tmp_theta, marker = ".")
            ax1.scatter(tmp_x_2, tmp_y_2, c = [colorator(iii) for iii in tmp_theta], marker = ".")

            # Plot dogs
            for dd in range(ndogs):
                tag = "Dog" + str(dd)
                #plt.plot(x_dogs[index,dd],y_dogs[index,dd], 'x', label = tag)

                x_dogs_2 = (x_dogs[index, dd] - rot_x_center) * np.cos(tmp_herd_dog_angle) - (y_dogs[index, dd] - rot_y_center) * np.sin(tmp_herd_dog_angle)
                y_dogs_2 = (y_dogs[index, dd] - rot_y_center) * np.cos(tmp_herd_dog_angle) + (x_dogs[index, dd] - rot_x_center) * np.sin(tmp_herd_dog_angle)

                ax1.plot(x_dogs_2, y_dogs_2, 'kX', markersize = 10, label = tag)
            
            # Plot target
            x_target_2 = (x_target - rot_x_center) * np.cos(tmp_herd_dog_angle) - (y_target - rot_y_center) * np.sin(tmp_herd_dog_angle)
            y_target_2 = (y_target - rot_y_center) * np.cos(tmp_herd_dog_angle) + (x_target - rot_x_center) * np.sin(tmp_herd_dog_angle)

            ax1.plot(x_target_2, y_target_2, 'gD', markersize = 20, label = "Target")

            # Plot some shading in the clone view
            # Hardcoded for one dog
            hist_time = 500
            blah = t + 1
            if t > hist_time:
                early_timestep = blah - hist_time
            else:
                early_timestep = 0
            xdogs = x_dogs[::num_particles][early_timestep:blah]
            ydogs = y_dogs[::num_particles][early_timestep:blah]

            xdogs_clone = (xdogs - rot_x_center) * np.cos(tmp_herd_dog_angle) - (ydogs - rot_y_center) * np.sin(tmp_herd_dog_angle)
            ydogs_clone = (ydogs - rot_y_center) * np.cos(tmp_herd_dog_angle) + (xdogs - rot_x_center) * np.sin(tmp_herd_dog_angle)

            xd, yd, zd = colored_line(xdogs_clone, ydogs_clone, 1, linewidth = .02)

            #ax2.pcolormesh(xs, ys, zs, shading='gouraud', cmap='Blues', label = 'Sheep')
            ax1.pcolormesh(xd, yd, zd, shading='gouraud', cmap='Greys', label = 'Dogs', alpha = 0.2)


            #plt characteristics    
            #plt.legend()
            ax1.set_xlim(-1.5*scale,1.5*scale)
            ax1.set_ylim(-1.5*scale,1.5*scale)
            ax2.set_xlim(-L,3)
            ax2.set_ylim(-3,L)
        """

        # Drone view
        drone_view = 1

        if drone_view:
            blah = t+1
            xdogs = x_dogs[::num_particles][:blah]
            ydogs = y_dogs[::num_particles][:blah]

            for i in range(ndogs):
                xd, yd, zd = colored_line(xdogs[:, i], ydogs[:, i], 1, linewidth = .05)
                ax.pcolormesh(xd, yd, zd, shading='gouraud', cmap='Greys', label = 'Dogs', alpha = 0.2)

            tmp_herd_dog_angle = 0*np.arctan2(y_target-y_avg, x_target-x_avg)

            # Plots the center of mass
            ax.plot(x_avg,y_avg, 'r.', markersize = 3, label = "Herd CM") #herd CM

            angle_array = np.linspace(-np.pi, np.pi, 500)
            #angle_array = [ii - tmp_target_angle for ii in angle_array]
            x_offset = 1.75
            y_offset = 5.0
            x_colors_p = 0.75*np.cos(angle_array)
            y_colors_p = 0.75*np.sin(angle_array)

            x_colors = x_colors_p*np.cos(tmp_herd_dog_angle)-y_colors_p*np.sin(tmp_herd_dog_angle)+x_offset
            y_colors = y_colors_p*np.cos(tmp_herd_dog_angle)+x_colors_p*np.sin(tmp_herd_dog_angle)+y_offset

            angle_colors = [colorator(p) for p in angle_array]
            ax.scatter(x_colors, y_colors, color = angle_colors)


            # Plot the data
            #ax2.scatter(tmp_x, tmp_y, c = tmp_theta%(2*np.pi), marker = ".")
            ax.scatter(tmp_x, tmp_y, c = [colorator(iii) for iii in tmp_theta], marker = ".")

            # Make the box
            tmp_herd_dog_angle = (np.pi/2-np.arctan2(y_target, x_target))

            tmp_box_lines = np.linspace(-1,1, 100)
            tmp_box_zero = np.zeros(100)
            
            tmp_box_lines_x = tmp_box_lines+x_avg
            tmp_box_lines_y = tmp_box_zero+y_avg

            tmp_x_box_top = scale*((tmp_box_lines_x-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y+1-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_top = scale*((tmp_box_lines_y+1-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x-x_avg)*np.sin(tmp_herd_dog_angle))

            tmp_x_box_bot = scale*((tmp_box_lines_x-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y-1-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_bot = scale*((tmp_box_lines_y-1-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x-x_avg)*np.sin(tmp_herd_dog_angle))

            tmp_box_lines_y_2 = tmp_box_lines+y_avg
            tmp_box_lines_x_2 = tmp_box_zero+x_avg

            tmp_x_box_right = scale*((tmp_box_lines_x_2+1-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y_2-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_right = scale*((tmp_box_lines_y_2-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x_2+1-x_avg)*np.sin(tmp_herd_dog_angle))

            tmp_x_box_left = scale*((tmp_box_lines_x_2-1-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y_2-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_left = scale*((tmp_box_lines_y_2-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x_2-1-x_avg)*np.sin(tmp_herd_dog_angle))

            # ax2.plot(tmp_x_box_top+x_avg, tmp_y_box_top+y_avg, 'k--', alpha = 0.25)
            # ax2.plot(tmp_x_box_bot+x_avg, tmp_y_box_bot+y_avg, 'k--', alpha = 0.25)
            # ax2.plot(tmp_x_box_right+x_avg, tmp_y_box_right+y_avg, 'k--', alpha = 0.25)
            # ax2.plot(tmp_x_box_left+x_avg, tmp_y_box_left+y_avg, 'k--', alpha = 0.25)

            # Plot dogs
            for dd in range(ndogs):
                tag = "Dog" + str(dd)
                ax.plot(x_dogs[index,dd],y_dogs[index,dd], 'kX', markersize = 10, label = tag)
                
            # Plot the fence boundary
            if fence == 1:
                # xwall, ywall, xt_array, yt_array = plot_fence(L, x_target, y_target, ld)
                ax.hlines([fmin_y, fmax_y], fmin_x, fmax_x)
                ax.vlines([fmin_x, fmax_x], fmin_y, fmax_y)

            #Plot target
            ax.plot(x_target, y_target, 'gD', markersize = 20, label = "Target")

        fig.savefig(name)
    
    if t%modder ==0:
      print("Currently saving plot # ", t, "out of", timesteps )

t1 = time.time()

print("Total time to make and save plots is", t1-t0)

make_movie()





