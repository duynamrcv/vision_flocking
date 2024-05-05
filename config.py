import numpy as np

TIMESTEP = 0.1
ROBOT_RADIUS = 0.25
SENSING_RADIUS = 5.0
ITER_MAX = 50000
EPS_DISTANCE = 0.1          # m
EPS_BEARING = np.deg2rad(2) # rad

VREF = 1.0
UREF = np.array([1,0])
DREF = 1.0
VMAX = 1.5
  
W_sep = DREF**2/2
W_coh = 1.0
W_mig = 1.0

X_START = 0.0
X_GOAL = 30.

NUM_ROBOT = 50

MODE = "vision"     # metric, vision
FILE_NAME = "data_" + MODE + ".txt"