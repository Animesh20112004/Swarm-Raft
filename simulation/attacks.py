import numpy as np

class Adversary:
    def __init__(self, config):
        self.f = config.get('f', 2)
        self.spoof_bias = config.get('spoof_bias', np.array([50.0, 50.0, 0.0]))

    def apply_attacks(self, drones, dist_matrix):
        """
        Scenario 1: GNSS Spoofing
        Scenario 2: Ranging Tampering
        Scenario 3: Collusion
        """
        n = len(drones)
        faulty_indices = np.random.choice(n, self.f, replace=False)
        
        for idx in faulty_indices:
            drones[idx].sense_gnss(is_spoofed=True, bias=self.spoof_bias)
        
        for idx in faulty_indices:
            for other_idx in range(n):
                if idx == other_idx: continue
                distortion = np.random.uniform(5.0, 15.0) 
                dist_matrix[idx, other_idx] += distortion
                dist_matrix[other_idx, idx] += distortion

        return faulty_indices, dist_matrix