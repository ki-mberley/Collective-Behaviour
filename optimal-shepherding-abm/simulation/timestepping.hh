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

// run vicsek, cm attraction, hard repulsion force, and wall repulsion
void herding::sheep_step_no_dog() {
    // calculate herd CM
    avg_loc(x, y);

    for (int i = 0; i < num_agents; i++) {
        // viscek interaction
        double theta_vsk = viscek(i); // alignment angle calculated from vicsek
        double v_vsk[2] = {v * cos(theta_vsk), v * sin(theta_vsk)}; // take step according to vicsek alignment angle
        double xnext = alpha * v_vsk[0] * dt; // viscek x step forward
        double ynext = alpha * v_vsk[1] * dt; // viscek y step forward

        // hard sphere repulsion
        sheep_repulsor(i); // calculate hard sphere repulsion
        xnext += beta * ssrf[0] * dt; // sheep-sheep repulsion calculation x dir
        ynext += beta * ssrf[1] * dt; // sheep-sheep repulsion calculation y dir

        // CM attraction
        double theta_cm = sheep_attractor(i); // calculate orientation of CM attraction
        double v_cm[2] = {v * cos(theta_cm),v * sin(theta_cm)}; // take step towards center of mass
            
        // calculates distance between sheep and the CM of the herd
        double lambda2 = 0;
        double temp_delta = pow((x[i] - pos_avg[0]) * (x[i] - pos_avg[0]) + (y[i] - pos_avg[1]) * (y[i] - pos_avg[1]), lambda2);
        
        xnext += gamma * v_cm[0] * dt * temp_delta; // CM attraction in the x direction
        ynext += gamma * v_cm[1] * dt * temp_delta; // CM attraction in the y direction

        x2[i] = xnext + x[i]; // take step
        y2[i] = ynext + y[i]; // take step

        // fence repulsion
        if (fence == 1) {
            if (x2[i] > fmax_x) {
                x2[i] = fmax_x;
            } else if (y2[i] > fmax_y) {
                y2[i] = fmax_y;
            } else if (x2[i] < fmin_x) {
                x2[i] = fmin_x;
            } else if(y2[i] < fmin_y) {
                y2[i] = fmin_y;
            }
        }

        xnext = 0; // reset step size
        ynext = 0; // reset step size
    }
}


void herding::propogate_herd(int id, double v_dog_tmp, int time) {
    // propogate dog
    xd2 = xdogsf[id];
    yd2 = ydogsf[id];
    double xd = xdogs[id];
    double yd = ydogs[id];

    // temp variables
    double xnext;
    double ynext;
    double sd_rf[2];

    double dog_vel_angle = atan2(yd2 - yd, xd2 - xd); // calculate the dogs heading

    // sanity check to make sure dog step size isn't too big
    if ((yd2 - yd) * (yd2 - yd) + (xd2 - xd) * (xd2 - xd) > (v_dog_tmp * dt) * (v_dog_tmp * dt)) {
        printf("Dog moving too FAST!!! %d \n", time);
        cout << "xd2, yd2" << xd2 <<", "<< yd2 << " xd, yd" << xd << ", "<< yd <<endl;
    }

    double theta0 = 0; // temp variables to store the next timestep
  
    // loop over agents
    for (int i = 0; i < num_agents; i++) {
        // bring back xnext from initial vicsek, CM, hard-shell run
        xnext = x2[i] - x[i];
        ynext = y2[i] - y[i];
        
        // add in Dog repulsion
        dog_repulsor(sd_rf, dog_vel_angle, i);
        xnext += delta * sd_rf[0] * dt; // sSheep-dog repulsion calculation x dir
        ynext += delta * sd_rf[1] * dt; // sheep-dog repulsion calculation y dir

        // update positions of each sheep
        x2[i] = xnext + x[i];
        y2[i] = ynext + y[i];

        // update directions of sheep
        theta0 = atan2(ynext, xnext);
        theta2[i] = theta0;

        if (fence == 1) {
            if (xdogsf[id] > fmax_x) {
                xdogsf[id] = fmax_x;
            } else if (ydogsf[id] > fmax_y) {
                ydogsf[id] = fmax_y;
            } else if (xdogsf[id] < fmin_x) {
                xdogsf[id] = fmin_x;
            } else if(ydogsf[id] < fmin_y) {
                ydogsf[id] = fmin_y;
            }
        }
    }
}


void herding::test_propogate_sheep()
{
    double sd_rf[2];

    // loop over agents for dog movement
    for(int i = 0; i < num_agents; i++) {
        double xnext_test;
        double ynext_test;

        // dog repulsion
        dog_repulsor(sd_rf,dog_sample_angle, i);
        xnext_test = delta * sd_rf[0] * dt; // sheep-dog repulsion calculation x dir
        ynext_test = delta * sd_rf[1] * dt; // sheep-dog repulsion calculation y dir

        // update positions of each sheep
        x_test[i] = xnext_test + x2[i];
        y_test[i] = ynext_test + y2[i];
    }
}


void herding::first_round() {
    for (int id = 0; id < num_dogs; id++) {
        // set array to store results of cost function
        double min_cost = exp(100); // initial high value of cost function
        double max_cost = 0;        // initial high value of cost function
        double tmp_cost = 0;        // initial value for temp cost function variable

        double xd_f = xdogs[id]; // initialize & set value for "best" dog x motion
        double yd_f = ydogs[id]; // initialize & set value for "best" dog y motion
        double xd = xdogs[id];   // initialize & set value for "current" dog x motion
        double yd = ydogs[id];   // initialize & set value for "current" dog x motion

        // begin sampling loop
        for (int k = 0; k < sample_number; k++) {
            avg_loc(x, y); // sets the average position of sheep herd

            // pick a random angle
            dog_sample_angle = dog_range * (rand() / (double) RAND_MAX - 0.5);

            // pick a specific angle (dog speed dynamically set...v_dog_tmp)
            xd2 = xd + v_dog_tmp * cos(dog_sample_angle) * dt;
            yd2 = yd + v_dog_tmp * sin(dog_sample_angle) * dt;

            // hardcoded maximum distance between dog and sheep
            if (sqrt((xd2 - pos_avg[0]) * (xd2 - pos_avg[0]) + (yd2 - pos_avg[1]) * (yd2 - pos_avg[1])) < 5 * dog_dist_factor * ld) {
                // loop over agents for dog movement
                test_propogate_sheep();

                // calculate the cost function:
                cost_function(id);
                tmp_cost = cost_function_val[0]; // set tmp_cost to calculated cost_function value

                // chooses sample with best value for cost function
                if (tmp_cost <= min_cost) {
                    xd_f = xd2;
                    yd_f = yd2;
                    min_cost = tmp_cost; // set new cost function
                    sheep_spread_final = cost_function_val[1];
                    xcm_final = cost_function_val[2];
                    ycm_final = cost_function_val[3];
                }

                // set maximum cost value if tmp_cost somehow exceeds maximum cost...
                if (tmp_cost >= max_cost) max_cost = tmp_cost;

            } else { // if further than the max allowed distance, dog just propogates towards herd CM
                double tmp_angle_dog_herd = atan2(pos_avg[1] - yd, pos_avg[0] - xd);

                xd_f = xd + v_dog * cos(tmp_angle_dog_herd) * dt;
                yd_f = yd + v_dog * sin(tmp_angle_dog_herd) * dt;
            }
        }

        xdogsf[id] = xd_f;
        ydogsf[id] = yd_f;

        // fence repulsion
        if (fence == 1) {
            if (xdogsf[id] > fmax_x) {
                xdogsf[id] = fmax_x;
            } else if (ydogsf[id] > fmax_y) {
                ydogsf[id] = fmax_y;
            } else if (xdogsf[id] < fmin_x) {
                xdogsf[id] = fmin_x;
            } else if(ydogsf[id] < fmin_y) {
                ydogsf[id] = fmin_y;
            }
        }
    }
}

// simplified shepherd agent model based on "Simulating Single and Multiple Sheepdogs Guidance of a Sheep Swarm"
void herding::shepherd_agent_movement() {
    read_params_shepherd_ABM();
    for (int id = 0; id < num_dogs; id++) {
        avg_loc(x, y);

        double x_dog = xdogs[id];
        double y_dog = ydogs[id];

        double x_shepherding_behaviour = 0;
        double y_shepherding_behaviour = 0;

        int separated_sheep = -1;
        for (int i = 0; i < num_agents; i++) {
            // sheep i is too far away from the herd CM
            if (sqrt((x[i] - pos_avg[0]) * (x[i] - pos_avg[0]) + (y[i] - pos_avg[1]) * (y[i] - pos_avg[1])) > 3 * sheep_influence_radius * cbrt(num_agents * num_agents)) {
                separated_sheep = i;
                break;
            }
        }
        if (separated_sheep == -1) { // all sheep are close to the herd CM -> move to driving position
            double driving_pos_dir[2] = {pos_avg[0] - x_target, pos_avg[1] - y_target};
            double driving_pos_dir_len = sqrt(driving_pos_dir[0] * driving_pos_dir[0] + driving_pos_dir[1] * driving_pos_dir[1]);
            double x_driving_pos = pos_avg[0] + (driving_pos_dir[0] / driving_pos_dir_len) * shepherding_influence_radius;
            double y_driving_pos = pos_avg[1] + (driving_pos_dir[1] / driving_pos_dir_len) * shepherding_influence_radius;

            x_shepherding_behaviour = (x_driving_pos - x_dog) * driving_force_weight;
            y_shepherding_behaviour = (y_driving_pos - y_dog) * driving_force_weight;
        } else { // at least one sheep is too far away from the herd CM -> move to collecting position
            double collecting_pos_dir[2] = {x[separated_sheep] - pos_avg[0], y[separated_sheep] - pos_avg[1]};
            double collecting_pos_dir_len = sqrt(collecting_pos_dir[0] * collecting_pos_dir[0] + collecting_pos_dir[1] * collecting_pos_dir[1]);
            double x_collecting_pos = x[separated_sheep] + (collecting_pos_dir[0] / collecting_pos_dir_len) * shepherding_influence_radius;
            double y_collecting_pos = y[separated_sheep] + (collecting_pos_dir[1] / collecting_pos_dir_len) * shepherding_influence_radius;
 
            x_shepherding_behaviour = (x_collecting_pos - x_dog) * collecting_force_weight;
            y_shepherding_behaviour = (y_collecting_pos - y_dog) * collecting_force_weight;
        }
       
        double x_shepherd_repulsion_force = 0;
        double y_shepherd_repulsion_force = 0;
        double x_lcm = 0;
        double y_lcm = 0;
        int n_lcm = 0;
        for (int k = 0; k< num_dogs; k++) {
            double dist_id_k = sqrt((x_dog - xdogs[k]) * (x_dog - xdogs[k]) + (y_dog - ydogs[k]) * (y_dog - ydogs[k]));
            if (k != id && dist_id_k <= shepherd_influence_radius) {
                if (dist_id_k == 0) {
                    x_shepherd_repulsion_force += rand_float();
                    y_shepherd_repulsion_force += rand_float();
                } else {
                    x_shepherd_repulsion_force += (x_dog - xdogs[k]) / dist_id_k;
                    y_shepherd_repulsion_force += (y_dog - ydogs[k]) / dist_id_k;
                }
            }
            if (dist_id_k <= 3 * shepherd_influence_radius) {
                x_lcm += xdogs[k];
                y_lcm += ydogs[k];
                n_lcm += 1;
            }
        }
        double x_shepherd_repulsion = x_shepherd_repulsion_force * shepherd_repulsion_weight;
        double y_shepherd_repulsion = y_shepherd_repulsion_force * shepherd_repulsion_weight;
        if (n_lcm > 0) {
            x_lcm /= n_lcm;
            y_lcm /= n_lcm;
        }

        double x_shepherd_attraction = (x_lcm - x_dog) * shepherd_attraction_weight;
        double y_shepherd_attraction = (y_lcm - y_dog) * shepherd_attraction_weight; 
        
        xdogsf[id] = x_dog + v_dog * (x_shepherding_behaviour + x_shepherd_repulsion + x_shepherd_attraction) * dt;
        ydogsf[id] = y_dog + v_dog * (y_shepherding_behaviour + y_shepherd_repulsion + y_shepherd_attraction) * dt;
    
        // fence repulsion
        if (fence == 1) {
            if (xdogsf[id] > fmax_x) {
                xdogsf[id] = fmax_x;
            } else if (ydogsf[id] > fmax_y) {
                ydogsf[id] = fmax_y;
            } else if (xdogsf[id] < fmin_x) {
                xdogsf[id] = fmin_x;
            } else if(ydogsf[id] < fmin_y) {
                ydogsf[id] = fmin_y;
            }
        }
    } 

    xcm_final = pos_avg[0];
    ycm_final = pos_avg[1];
}
    

// propogate herd with optimal parameters
void herding::final_round(int time) {
    // propogate sheep using optimal dog parameters
     for (int id = 0; id < num_dogs; id++) {
        propogate_herd(id, v_dog_tmp, time);
    }

    // switch pointers for next dog-step
    double* s_x = x2; x2 = x; x = s_x;
    double* s_y = y2; y2 = y; y = s_y;
    double* s_theta = theta2; theta2 = theta; theta = s_theta;

    // switch pointers for dog
    double* s_xdogs = xdogsf; xdogsf = xdogs; xdogs = s_xdogs;
    double* s_ydogs = ydogsf; ydogsf = ydogs; ydogs = s_ydogs;
}


#endif
