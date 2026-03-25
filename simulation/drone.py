import numpy as np

class Drone:
    def __init__(self, id, start_pos, config):
        self.id = id
        self.true_pos = np.array(start_pos, dtype=float)
        self.config = config
        self.ins_pos = np.copy(self.true_pos)

    def update_ins(self, velocity, dt):
        """Physical movement update with inertial drift."""
        # Realistic drift (Small random error in movement)
        drift = np.random.normal(0, 0.02, size=3)
        self.true_pos += (velocity * dt) + drift
        
        # What the drone 'thinks' its position is (INS)
        self.ins_pos = self.true_pos + np.random.normal(0, 0.05, size=3)

    def sense_gnss(self, bias=None):
        """Returns noisy GNSS position, optionally spoofed."""
        noise = np.random.normal(0, self.config['R_GNSS'], size=3)
        if bias is not None:
            return self.true_pos + bias + noise
        return self.true_pos + noise