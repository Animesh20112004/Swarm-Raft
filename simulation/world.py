import numpy as np
from simulation.drone import Drone

class SwarmWorld:
    def __init__(self, config):
        self.config = config
        self.n = config['n']
        self.drones = []
        self._setup_swarm()

    def _setup_swarm(self):
        """Spawns drones in a 6x6 meter random cluster."""
        for i in range(self.n):
            start_pos = np.array([
                np.random.uniform(-3, 3), 
                np.random.uniform(-3, 3), 
                0.0
            ])
            self.drones.append(Drone(i, start_pos, self.config))

    def generate_step(self, malicious_indices=None):
        dt = self.config['dt']
        for i, drone in enumerate(self.drones):
            # Base Swarm Velocity (Slow cruise North)
            velocity = np.array([0.0, 1.2, 0.0])
            
            # If spoofed, add a slow "Break Formation" drift
            if malicious_indices and i in malicious_indices:
                velocity += np.array([2.5, 0.8, 0.0]) 
                
            drone.update_ins(velocity, dt)

    def get_all_reports(self, attacked_indices=None):
        reports = []
        for i, drone in enumerate(self.drones):
            bias = self.config['spoof_bias'] if (attacked_indices and i in attacked_indices) else None
            reports.append(drone.sense_gnss(bias))
        return np.array(reports)

    def get_full_distance_matrix(self):
        n = len(self.drones)
        matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j: continue
                dist = np.linalg.norm(self.drones[i].true_pos - self.drones[j].true_pos)
                matrix[i, j] = dist + np.random.normal(0, self.config['sigma_d'])
        return matrix