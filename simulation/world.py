import numpy as np
from .drone import Drone

class SwarmWorld:
    def __init__(self, config):
        self.config = config
        self.n = config.get('n', 6)
        self.dt = config.get('dt', 0.1)

        self.drones = []
        self._setup_swarm()

    def _setup_swarm(self):
        """Initializes drones at starting positions (e.g., a simple grid or line)."""
        for i in range(self.n):
            start_pos = [i * 10.0, 0.0, 10.0] 
            self.drones.append(Drone(i, start_pos, self.config))

    def generate_step(self, k):
        """
        Updates the true position of all drones for time step k.
        In this example, drones move in a simple forward trajectory with 
        slight random variation.
        """
        velocity = np.array([1.0, 0.2, 0.0]) * self.dt
        
        for drone in self.drones:
            new_true_pos = drone.true_pos + velocity
            drone.update_ground_truth(new_true_pos)
            drone.update_ins(velocity)
            
            drone.sense_gnss()

    def get_full_distance_matrix(self):
        """
        Computes the inter-drone distance matrix d_ij,k.
        This is the data the leader node will use for verification[cite: 86, 92].
        """
        matrix = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    matrix[i, j] = 0.0
                else:
                    matrix[i, j] = self.drones[i].get_range_to(self.drones[j].true_pos)
        return matrix

    def get_all_reports(self):
        """Collects reported (GNSS) positions from all nodes[cite: 87, 142]."""
        return np.array([d.gnss_pos for d in self.drones])