import numpy as np
from scipy.spatial import Delaunay

from config import *

class Robot():
    def __init__(self, index, position, velocity):
        self.index = index
        self.position = position
        self.velocity = velocity
        self.neighbor_set = []

        # For saving
        self.neighbor_sets = [self.neighbor_set]
        self.path = [np.concatenate([self.position, self.velocity])]

    def update(self, velocity, dt):
        norm_velocity = np.linalg.norm(velocity)
        if norm_velocity > VMAX:
            velocity = velocity/norm_velocity*VMAX

        self.velocity = velocity
        self.position = self.position + velocity*dt

        self.neighbor_sets.append(self.neighbor_set)
        self.path.append(np.concatenate([self.position, self.velocity]))

    def computeControl(self, robots):
        if MODE == "metric":
            self.neighbor_set = self.neighborMetric(robots)
        elif MODE == "vision":
            self.neighbor_set = self.neighborVision(robots)
        
        observed_robots = self.collectNeighborPosition(robots)
        vel = self.behaviorMigration() + self.behaviorSocial(observed_robots)
        return vel
    
    def collectNeighborPosition(self, robots):
        observed_robots = []
        for j in self.neighbor_set:
            pose = robots[j].position
            dis_noise = np.linalg.norm(pose-self.position)*(1+np.random.normal(0,EPS_DISTANCE,1)[0])
            ang_noise = np.arctan2(*(pose-self.position)[::-1]) + np.random.normal(0,EPS_BEARING,1)[0]
            observed_robots.append(np.array([dis_noise*np.cos(ang_noise),
                                             dis_noise*np.sin(ang_noise)]))
            # observed_robots.append(pose-self.position)
        return observed_robots

    def behaviorSocial(self, observed_robots):
        v_coh = 0.; v_sep = 0.
        if len(self.neighbor_set) == 0:
            return 0.
        for j in range(len(self.neighbor_set)):
            r_ij = observed_robots[j]
            v_coh += r_ij
            v_sep += r_ij/np.linalg.norm(r_ij)**2
        
        v_soc = W_coh/len(self.neighbor_set)*v_coh - W_sep*v_sep
        return v_soc
    
    def behaviorMigration(self):
        v_mig = W_mig*VREF*UREF
        return v_mig
    
    def neighborMetric(self, robots):
        metric_set = []
        for j in range(NUM_ROBOT):
            if j == self.index:
                continue
            d_ij = np.linalg.norm(robots[j].position - self.position)
            if(d_ij < SENSING_RADIUS):
                metric_set.append(j)
        return metric_set
    
    def neighborVision(self, robots):
        # Detect metric set with sorted distance
        metric_set = dict()
        for j in range(NUM_ROBOT):
            if j == self.index:
                continue
            d_ij = np.linalg.norm(robots[j].position - self.position)
            if(d_ij < SENSING_RADIUS):
                metric_set[j] = d_ij
        metric_set = dict(sorted(metric_set.items(), key=lambda item: item[1]))

        # Detect vision set
        vision_set = dict()
        for j in metric_set.keys():
            if not vision_set:
                vision_set[j] = robots[j].position
            else:
                r_ij = robots[j].position - self.position
                d_ij = metric_set[j]
                u_ij = r_ij/d_ij
                rhat_ij = ROBOT_RADIUS/d_ij

                is_occlusion = False
                for k in vision_set.keys():
                    r_ik = robots[k].position - self.position
                    d_ik = metric_set[k]
                    u_ik = r_ik/d_ik
                    rhat_ik = ROBOT_RADIUS/d_ik
                    if np.linalg.norm(u_ij-u_ik) < rhat_ij+rhat_ik:
                        is_occlusion = True
                        break
                if not is_occlusion:
                    vision_set[j] = robots[j].position
        if not USE_VORONOI:
            return list(vision_set.keys())
        else:
            if len(vision_set) < 3:
                return list(vision_set.keys())
            else:
                keys = list(vision_set.keys())
                points = list(vision_set.values())
                points = np.array(points)
                points = np.vstack([points, self.position])
                indptr_neigh, neighbours = Delaunay(points).vertex_neighbor_vertices
                voronoi_neigh = neighbours[indptr_neigh[points.shape[0]-1]:indptr_neigh[points.shape[0]]]
                vision_voronoi_set = [keys[j] for j in voronoi_neigh]
                # print(vision_voronoi_set)
                return vision_voronoi_set
