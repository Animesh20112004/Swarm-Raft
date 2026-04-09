import numpy as np

def apply_spoofing(drones, f_count, offset=20.0):
    # Select f drones to spoof [cite: 298]
    indices = np.random.choice(len(drones), f_count, replace=False)
    for i in indices:
        drones[i].is_spoofed = True
        # Inject arbitrary bias [cite: 113]
        drones[i].reported_pos += np.random.uniform(offset, offset*2, size=3)