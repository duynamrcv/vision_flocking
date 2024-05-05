import matplotlib.pyplot as plt
import numpy as np
import pickle

from config import *

with open(FILE_NAME, 'rb') as file:
    data = pickle.load(file)
    
    # Plot path
    plt.figure(figsize=(10, 3))
    for i in range(NUM_ROBOT):
        path = data[i]['path']
        plt.plot(path[:,0], path[:,1])

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.axis('scaled')
    plt.tight_layout()
    plt.show()