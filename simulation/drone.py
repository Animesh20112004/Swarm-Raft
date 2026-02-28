import numpy as np

class Drone:
    def __init__(self, drone_id, initial_pos, config):
        self.id = drone_id
        self.config = config
        
        self.true_pos = np.array(initial_pos, dtype=float)
        
        self.ins_pos = np.array(initial_pos, dtype=float)
        
        self.gnss_pos = np.zeros(3)
        
        self.r_gnss = config.get('R_GNSS', 1.0) 
        self.r_ins = config.get('R_INS', 0.1)
        self.sigma_d = config.get('sigma_d', 0.05)

    def update_ground_truth(self, new_pos):
        self.true_pos = np.array(new_pos)

    def sense_gnss(self, is_spoofed=False, bias=np.array([0,0,0])):
        noise = np.random.normal(0, self.r_gnss, 3)
        self.gnss_pos = self.true_pos + noise
        
        if is_spoofed:
            self.gnss_pos += bias
        return self.gnss_pos

    def update_ins(self, velocity_step):
        
        drift = np.random.normal(0, self.r_ins, 3)
        self.ins_pos += velocity_step + drift
        return self.ins_pos

    def get_range_to(self, other_drone_pos):
        """
        Simulates noisy distance measurement d_ij,k[cite: 136].
        Uses Euclidean distance + noise eta_ij,k[cite: 137].
        """
        true_dist = np.linalg.norm(self.true_pos - other_drone_pos)
        noise = np.random.normal(0, self.sigma_d)
        return true_dist + noise

    def reset_ins(self, corrected_pos):
        """Resets the INS state after a SwarmRaft recovery[cite: 188]."""
        self.ins_pos = np.array(corrected_pos)