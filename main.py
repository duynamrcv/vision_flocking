
from robot import Robot
from config import *

import numpy as np
import random
import time
import pickle

if __name__ == "__main__":
    robots = []
    # Initialization
    for i in range(NUM_ROBOT):
        robot = Robot(i,
                      np.array([X_START-8*random.random(), -10.0*random.random()]),
                      np.zeros(2))
        robots.append(robot)
    
    compute_times = []
    iter = 0
    try:
        print("[INFO] Start")
        run = True
        iter = 0
        while run and iter < ITER_MAX:
            times = []
            for i in range(NUM_ROBOT):
                # compute velocity using nmpc
                start = time.time()
                control = robots[i].computeControl(robots)
                times.append(time.time()-start)
                robots[i].update(control, TIMESTEP)

            compute_times.append(times)
            iter += 1
            if iter % 10 == 0:
                print("Iteration {}".format(iter))

            # Reach terminal condition
            count = 0
            for i in range(NUM_ROBOT):
                if robots[i].position[0] > X_GOAL:
                    count += 1
            run = count < NUM_ROBOT
    finally:
        print("[INFO] Saving")
        # Saving
        with open(FILE_NAME, 'wb') as file:
            data = []
            for i in range(NUM_ROBOT):
                d = dict()
                d['path'] = np.array(robots[i].path)
                d['neighbor'] = robots[i].neighbor_sets
                data.append(d)
            pickle.dump(data, file)

        compute_times = np.array(compute_times)
        print("Average time: {:.6}s".format(compute_times.mean()))
        print("Max time: {:.6}s".format(compute_times.max()))   
        print("Min time: {:.6}s".format(compute_times.min()))