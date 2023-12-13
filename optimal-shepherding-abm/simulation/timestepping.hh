#ifndef TIMESTEPPING
#define TIMESTEPPING

#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

#include "herding.hh"
#include "forces.hh"
#include "cost_and_sampling.hh"

// Run vicsek, cm attraction, hard repulsion force, and wall repulsion
void herding::sheep_step_no_dog() {
    // Calculate herd CM
    avg_loc(x, y);

    for (int i = 0; i < num_agents; i++) {
        // Viscek interaction
        double theta_vsk = viscek(i); //alignment angle calculated from Vicsek
        double v_vsk[2] = {v * cos(theta_vsk), v * sin(theta_vsk)}; // Take step according to Vicsek alignment angle
        double xnext = alpha * v_vsk[0] * dt; // Viscek x step forward
        double ynext = alpha * v_vsk[1] * dt; // Viscek y step forward

        // Hard sphere repulsion
        sheep_repulsor(i); //Calculate hard sphere repulsion
        xnext += beta * ssrf[0] * dt; //Sheep-sheep repulsion calculation x dir
        ynext += beta * ssrf[1] * dt; //Sheep-sheep repulsion calculation y dir

        // CM attraction
        double theta_cm = sheep_attractor(i); // Calculate orientation of CM attraction
        double v_cm[2] = {v * cos(theta_cm),v * sin(theta_cm)}; // Take step towards center of mass
            
        //------------------temp code---------------------------
        //calculates distance between sheep and the CM of the herd...
        //TODO: put into a function and make dependent on a lambda parameter
        double lambda2 = 0;
        double temp_delta = pow((x[i] - pos_avg[0]) * (x[i] - pos_avg[0]) + (y[i] - pos_avg[1]) * (y[i] - pos_avg[1]), lambda2);

        //------------------end temp code-------------------------
        
        xnext += gamma * v_cm[0] * dt * temp_delta; // CM attraction in the x direction
        ynext += gamma * v_cm[1] * dt * temp_delta; // CM attraction in the y direction

        x2[i] = xnext + x[i]; // Take step
        y2[i] = ynext + y[i]; // Take step

        // Fence repulsion
        if (fence == 1) {
            if (x2[i] > fmax_x) {
                x2[i] = fmax_x;
            } else if (y2[i] > fmax_y) {
                y2[i] = fmax_y;
            } else if (x2[i] < fmin_x) {
                x2[i] = fmin_x;
            } else if(y2[i] > fmin_y) {
                y2[i] = fmin_y;
            }
        }

        xnext = 0; // Reset step size
        ynext = 0; // Reset step size
    }
}


void herding::propogate_herd(int id, double v_dog_tmp, int time) {
    // Propogate dog
    xd2 = xdogsf[id];
    yd2 = ydogsf[id];
    double xd = xdogs[id];
    double yd = ydogs[id];

    // Temp variables
    double xnext;
    double ynext;
    double sd_rf[2];

    double dog_vel_angle = atan2(yd2 - yd, xd2 - xd); //calculate the dogs heading

    // Sanity check to make sure dog step size isn't too big
    if ((yd2 - yd) * (yd2 - yd) + (xd2 - xd) * (xd2 - xd) > (v_dog_tmp * dt) * (v_dog_tmp * dt)) {
        printf("Dog moving too FAST!!! %d \n", time);
        cout << "xd2, yd2" << xd2 <<", "<< yd2 << " xd, yd" << xd << ", "<< yd <<endl;
    }

    double theta0 = 0; // Temp variables to store the next timestep
  
    // Loop over agents
    for (int i = 0; i < num_agents; i++) {
        // Bring back xnext from initial vicsek, CM, hard-shell run
        xnext = x2[i] - x[i];
        ynext = y2[i] - y[i];
        
        // Add in Dog repulsion
        dog_repulsor(sd_rf, dog_vel_angle, i);
        xnext += delta * sd_rf[0] * dt; // Sheep-dog repulsion calculation x dir
        ynext += delta * sd_rf[1] * dt; // Sheep-dog repulsion calculation y dir

        // Update positions of each sheep
        x2[i] = xnext + x[i];
        y2[i] = ynext + y[i];

        // Update directions of sheep
        theta0 = atan2(ynext, xnext);
        theta2[i] = theta0;
    }
}


void herding::test_propogate_sheep()
{
    double sd_rf[2];

    // Loop over agents for dog movement
    for(int i = 0; i < num_agents; i++) {
        double xnext_test;
        double ynext_test;

        // Dog repulsion
        dog_repulsor(sd_rf,dog_sample_angle, i);
        xnext_test = delta * sd_rf[0] * dt; // Sheep-dog repulsion calculation x dir
        ynext_test = delta * sd_rf[1] * dt; // Sheep-dog repulsion calculation y dir

        // Update positions of each sheep
        x_test[i] = xnext_test + x2[i];
        y_test[i] = ynext_test + y2[i];
    }
}


void herding::first_round() {
    // Set array to store results of cost function
    double min_cost = exp(100); //initial high value of cost function  
    double max_cost = 0; //initial high value of cost function
    double tmp_cost = 0; //initial value for temp cost function variable

    for (int id = 0; id < num_dogs; id++) {
        // Double rd_f[2];
        double xd_f = xdogs[id]; // Initialize & set value for "best" dog x motion
        double yd_f = ydogs[id]; // Initialize & set value for "best" dog y motion
        double xd = xdogs[id];   // Initialize & set value for "current" dog x motion
        double yd = ydogs[id];   // Initialize & set value for "current" dog x motion

        // Begin sampling loop
        for (int k = 0; k < sample_number; k++) {

            // Printf("Is the location checker doing it's job? \n");
            avg_loc(x, y); //sets the average position of sheep herd

            // Pick a random angle
            dog_sample_angle = dog_range * (rand() / (double) RAND_MAX - 0.5);

            // Pick a specific angle (dog speed dynamically set...v_dog_tmp)
            xd2 = xd + v_dog_tmp*cos(dog_sample_angle)*dt;
            yd2 = yd + v_dog_tmp*sin(dog_sample_angle)*dt;

            // Hardcoded maximum distance between dog and sheep
            if (sqrt((xd2 - pos_avg[0]) * (xd2 - pos_avg[0]) + (yd2 - pos_avg[1]) * (yd2 - pos_avg[1])) < 5 * dog_dist_factor * ld) { // Begin dog_dist_factor if
                // Loop over agents for dog movement
                test_propogate_sheep();

                // Calculate the cost function:
                cost_function(id);
                tmp_cost = cost_function_val[0]; // Set tmp_cost to calculated cost_function value

                // Dump the optimization results to a file
                // STILL NEED TO IMPLEMENT THIS!!!
                // fprintf(foptimize, "%d %d %f %f \n", jj, k, dog_sample_angle, tmp_cost);

                //Chooses sample with best value for cost function
                if (tmp_cost <= min_cost) {
                    xd_f = xd2;
                    yd_f = yd2;
                    min_cost = tmp_cost; // Set new cost function
                    sheep_spread_final = cost_function_val[1];
                    xcm_final = cost_function_val[2];
                    ycm_final = cost_function_val[3];
                }

                // Set maximum cost value if tmp_cost somehow exceeds maximum cost...
                if (tmp_cost >= max_cost) max_cost = tmp_cost;

            } else { // If further than the max allowed distance, dog just propogates towards herd CM
                double tmp_angle_dog_herd = atan2(pos_avg[1] - yd, pos_avg[0] - xd);

                printf("Dog-herd-angle: %f \n", tmp_angle_dog_herd);

                xd_f = xd + v_dog * cos(tmp_angle_dog_herd) * dt;
                yd_f = yd + v_dog * sin(tmp_angle_dog_herd) * dt;

                printf("crap \n");
            }

        }

        xdogsf[id] = xd_f;
        ydogsf[id] = yd_f;

        // Fence repulsion
        if (fence == 1) {
            if (xdogs[id] > fmax_x) {
                xdogs[id] = fmax_x;
            } else if (ydogs[id] > fmax_y) {
                ydogs[id] = fmax_y;
            } else if (xdogs[id] < fmin_x) {
                xdogs[id] = fmin_x;
            } else if(ydogs[id] > fmin_y) {
                ydogs[id] = fmin_y;
            }
        }
    }
}
    

// Propogate herd with optimal parameters
void herding::final_round(int time) {
        // Propogate sheep using optimal dog parameters
         for (int id = 0; id < num_dogs; id++) {
            propogate_herd(id, v_dog_tmp, time); 

            // Switch pointers for next dog-step
            double* s_x = x2; x2 = x; x = s_x;
            double* s_y = y2; y2 = y; y = s_y;
            double* s_theta = theta2; theta2 = theta; theta = s_theta;
        }

        // Switch pointers for dog
        double* s_xdogs = xdogsf; xdogsf = xdogs; xdogs = s_xdogs;
        double* s_ydogs = ydogsf; ydogsf = ydogs; ydogs = s_ydogs;
}


#endif

