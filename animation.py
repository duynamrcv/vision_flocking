import matplotlib.pyplot as plt
import numpy as np
import pickle

from scipy import spatial
from config import *

percent = 0.3 
width = 0.05

def getCircle(x,y,r):
    theta = np.linspace( 0 , 2 * np.pi , 50 )   
    a = x + r * np.cos( theta )
    b = y + r * np.sin( theta )
    return a, b

def findFocalIndex(data):
    robots = []
    for i in range(NUM_ROBOT):
        robots.append(data[i]['path'][-1,:2])
    robots = np.array(robots)
    center = np.sum(robots,axis=0)/NUM_ROBOT
    focal = spatial.KDTree(robots).query(center)[1]
    return focal

with open(FILE_NAME, 'rb') as file:
    data = pickle.load(file)
    focal = findFocalIndex(data)

    plt.figure(figsize=(5, 5))
    for iter in range(data[focal]['path'].shape[0]):
        plt.cla()
        focal_pose = data[focal]['path'][iter,:]
        for i in range(NUM_ROBOT):
            if i == focal:
                a, b = getCircle(focal_pose[0], focal_pose[1], ROBOT_RADIUS)
                plt.plot(a, b, '-r')
                plt.arrow(focal_pose[0], focal_pose[1],
                          focal_pose[2]*percent, focal_pose[3]*percent,
                          width=width, color='r')
                a, b = getCircle(focal_pose[0], focal_pose[1], SENSING_RADIUS)
                plt.plot(a, b, '--k')
            elif i in data[focal]['neighbor'][iter]:
                pose = data[i]['path'][iter,:]
                a, b = getCircle(pose[0], pose[1], ROBOT_RADIUS)
                plt.plot(a, b, '-b')
                plt.arrow(pose[0], pose[1],
                          pose[2]*percent, pose[3]*percent,
                          width=width, color='b')
            else:
                pose = data[i]['path'][iter,:]
                a, b = getCircle(pose[0], pose[1], ROBOT_RADIUS)
                plt.plot(a, b, '-k')
                plt.arrow(pose[0], pose[1],
                          pose[2]*percent, pose[3]*percent,
                          width=width, color='k')

        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.axis('scaled')
        plt.xlim([focal_pose[0]-6.0, focal_pose[0]+6.0])
        plt.ylim([focal_pose[1]-6.0, focal_pose[1]+6.0])
        plt.tight_layout()
        plt.gcf().canvas.mpl_connect('key_release_event',
                                        lambda event:
                                        [exit(0) if event.key == 'escape' else None])
        plt.pause(0.001)
    plt.show()