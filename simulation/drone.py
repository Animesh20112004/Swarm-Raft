import numpy as np

class Drone:
    def __init__(self, id, pos):
        self.id = id
        self.true_pos = np.array(pos, dtype=float)
        self.reported_pos = np.array(pos, dtype=float)
        self.is_spoofed = False

    def get_noise_dist(self, other_drone):
        dist = np.linalg.norm(self.true_pos - other_drone.true_pos)
        return dist + np.random.normal(0, 0.1) # Noise sigma_d [cite: 136]