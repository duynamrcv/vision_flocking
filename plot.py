import matplotlib.pyplot as plt
import numpy as np
import pickle
import random

from config import *

SAVE = True

focal = NUM_ROBOT-1
with open(FILE_NAME, 'rb') as file:
    data = pickle.load(file)
    
    # Plot path
    plt.figure(figsize=(8, 3))
    for i in range(NUM_ROBOT):
        path = data[i]['path']
        index = np.array([0,path.shape[0]/2, path.shape[0]-1])
        if i == focal:
            plt.plot(path[:,0], path[:,1], "-r", label="agent (focal)")
            plt.scatter(path[0,0], path[0,1], c="r", marker="s", zorder=2)
            plt.scatter(path[path.shape[0]//2,0], path[path.shape[0]//2,1], c="r", marker=">", zorder=2)
            plt.scatter(path[path.shape[0]-1,0], path[path.shape[0]-1,1], c="r", marker="o", zorder=2)
        else:
            plt.plot(path[:,0], path[:,1], "gray")
            plt.scatter(path[0,0], path[0,1], c="gray", marker="s")
            plt.scatter(path[path.shape[0]//2,0], path[path.shape[0]//2,1], c="gray", marker=">")
            plt.scatter(path[path.shape[0]-1,0], path[path.shape[0]-1,1], c="gray", marker="o")

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.axis('scaled')
    plt.legend()
    plt.tight_layout()
    if SAVE:
        file_name = "results/{}_{}.png".format(MODE,USE_VORONOI)
        plt.savefig(file_name)
    plt.show()