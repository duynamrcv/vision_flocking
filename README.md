# Vision-Based Swarms in the Presence of Occlusions

This repository refactors the following article in Python:

F. Schilling, E. Soria, and D. Floreano, "**On the Scalability of Vision-based Drone Swarms in the Presence of Occlusions**," *IEEE Access*, vol. 10, pp. 1-14, 2022. [[**IEEE** *Xplore*](https://ieeexplore.ieee.org/abstract/document/9732989)] [[Citation](#citation)]

And the following [video](https://youtu.be/3-O85lB_DJQ) gives the explanation of the article.

## Installation
```
git clone git@github.com:duynamrcv/vision_flocking.git
```

## Run simulation
The current version anables some type of neighbor selection methods, to change the selection type or other configuration parameters, edit `config.py` file.

* **MODE**:
    * `metric`: robots in predefined distance are choose as neighbors.
    * `vision`: robots that vision distance and do not occluded are chose as neighbors.
* **USE_VORONOI**:
    * True: use voronoi to refine neigbor set
    * False: not use voronoi

To run the simulation, please run:
```
python3 main.py
```
The data will be saved in `*.txt` file. To view animation, please run:
```
python3 animation.py
```
Note that the parameter `export=True` is use to export video file, if not, set `export=False`.

## Results
| Vision-based neighbor selection | Vision-based Voronoi neighbor selection |
| :---:        |     :---:      |
|  <a href="results/vision_True.gif"><img src="results/vision_False.gif" alt="Vision-based Voronoi neighbor selection" width="100%" ></a>   | <a href="results/vision_False.gif"><img src="results/vision_True.gif" alt="Vision-based Voronoi neighbor selection" width="100%" ></a>    |

## Comparison
### Paths
| Vision-based neighbor selection | Vision-based Voronoi neighbor selection |
| :---:        |     :---:      |
|  <img src="results/vision_False.png" alt="Vision-based Voronoi neighbor selection" width="100%" >   | <img src="results/vision_True.png" alt="Vision-based Voronoi neighbor selection" width="100%" >    |

### Scalability
|  |  |
| :---:        |     :---:      |
|  <img src="results/number_order.png" alt="Vision-based Voronoi neighbor selection" width="100%" >   | <img src="results/number_neighbor.png" alt="Vision-based Voronoi neighbor selection" width="100%" >    |

### Noise
|  |  |
| :---:        |     :---:      |
|  <img src="results/noise_dis_order.png" alt="Vision-based Voronoi neighbor selection" width="100%" >   | <img src="results/noise_bea_order.png" alt="Vision-based Voronoi neighbor selection" width="100%" >    |