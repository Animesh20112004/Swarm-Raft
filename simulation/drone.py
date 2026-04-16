import numpy as np
class Drone:
    def __init__(self, id, pos):
        self.id=id
        self.true_pos=np.array(posdtype=float)
        self.reported_pos=np.array(pos,dtype=float)
        self.is_spoofed=False
    def get_dist_noise(self,other_drone):
        dist=np.linalg.norm(self.true_pos-other_drone.true_pos)
        return dist+np.random.normal(0,0.1)