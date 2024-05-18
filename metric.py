import matplotlib.pyplot as plt
import numpy as np
import pickle

from config import *

# with open(FILE_NAME, 'rb') as file:
#     data = pickle.load(file)
    
# Order metric
def computeMeanOder(data):
    length = data[0]['path'].shape[0]
    headings = []
    for iter in range(1,length):
        heading = 0
        for i in range(len(data)):
            heading += data[i]['path'][iter,2:4]/np.linalg.norm(data[i]['path'][iter,2:4])
        headings.append(heading)
    headings = np.linalg.norm(np.array(headings),axis=1)/len(data)
    return np.mean(headings)

# Number of neighbors
def computeNumberNeighbors(data):
    length = data[0]['path'].shape[0]
    num_neighbors = []
    for iter in range(1, length):
        num_neighbor = []
        for i in range(len(data)):
            num_neighbor.append(len(data[i]['neighbor'][iter]))
        num_neighbors.append(num_neighbor)
    num_neighbors = np.array(num_neighbors)
    return np.min(num_neighbors), np.mean(num_neighbors), np.max(num_neighbors)

title = "number"
dirs = ["50_0_0", "100_0_0", "150_0_0", "200_0_0"]
x_data = np.array([50, 100, 150, 200])
x_label = "Number of agent N"

methods = ["data_metric_False.txt", "data_vision_False.txt", "data_vision_True.txt"]
names = ["Metric", "Visual", "Our"]

# Plot order metric
fig = plt.figure(figsize=(5,3))
for i in range(len(methods)):
    method = methods[i]
    order = []
    for dir in dirs:
        path = "{}/{}".format(dir, method)
        # print(path)
        with open(path, 'rb') as file:
            data = pickle.load(file)
            order.append(computeMeanOder(data))
    order = np.array(order)
    print(order)
    plt.plot(range(x_data.shape[0]), order, "-o", label=names[i])

plt.xlabel(x_label)
plt.ylabel("Average order")
plt.xticks(range(x_data.shape[0]), x_data)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/{}_order.png".format(title))

# Plot number of neighbors
fig = plt.figure(figsize=(5,3))
for i in range(len(methods)):
    method = methods[i]
    number = []
    for dir in dirs:
        path = "{}/{}".format(dir, method)
        # print(path)
        with open(path, 'rb') as file:
            data = pickle.load(file)
            number.append(computeNumberNeighbors(data))
    number = np.array(number)
    print(number)
    plt.fill_between(range(x_data.shape[0]), number[:,0], number[:,2], alpha=0.3)
    plt.plot(range(x_data.shape[0]), number[:,1], "-o", label=names[i])

plt.xlabel(x_label)
plt.ylabel("Number of neigbors")
plt.xticks(range(x_data.shape[0]), x_data)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/{}_neighbor.png".format(title))

plt.show()