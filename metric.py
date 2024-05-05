import matplotlib.pyplot as plt
import numpy as np
import pickle

from config import *

with open(FILE_NAME, 'rb') as file:
    data = pickle.load(file)
    
# Plot order metric
plt.figure(figsize=(6, 3))
length = data[0]['path'].shape[0]
headings = []
for iter in range(length):
    heading = 0
    for i in range(NUM_ROBOT):
        heading += data[i]['path'][iter,2:4]/np.linalg.norm(data[i]['path'][iter,2:4])
    headings.append(heading)
headings = np.linalg.norm(np.array(headings),axis=1)/NUM_ROBOT
plt.plot(np.arange(length), headings)

plt.xlabel("Time [s]")
plt.ylabel("Order")
plt.grid(True)
plt.tight_layout()
plt.show()