import numpy as np
from simulation.drone import Drone
class SwarmWorld:
    def __init__(self,config):
        self.config=config
        self.n=config['n']
        self.drones=[]
        self.swarm_setup()
    def swarm_setup(self):
        cent_x,cent_y=0.0,0.0
        max_radius=0.5    
        for i in range(self.n):
            angle=np.random.uniform(0,(2*np.pi))
            r=max_radius*np.sqrt(np.random.uniform(0, 1))
            start_pos=np.array([cent_x+r*np.cos(angle),cent_y+r*np.sin(angle),0.0])
            self.drones.append(Drone(i,start_pos,self.config))
    def generate_step(self,mal_ind=None):
        dt=self.config['dt']
        for i,drone in enumerate(self.drones):
            velo=np.array([0.0,1.2,0.0])
            if mal_ind and i in mal_ind:
                velo=velo+np.array([2.5,0.8,0.0]) 
            drone.update_ins(velo, dt)
    def get_all_reports(self,attacked_indices=None):
        reports=[]
        for i,drone in enumerate(self.drones):
            bias=self.config['spoof_bias']if(attacked_indices is not None and i in attacked_indices)else None
            reports.append(drone.sense_gnss(bias))
        return np.array(reports)
    def get_full_distance_matrix(self):
        n=len(self.drones)
        matrix=np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                if i==j:continue
                dist=np.linalg.norm(self.drones[i].true_pos-self.drones[j].true_pos)
                matrix[i,j]=dist+np.random.normal(0,self.config['sigma_d'])
        return matrix