import numpy as np
import matplotlib.pyplot as plt
from simulation.world import SwarmWorld
from simulation.attacks import Adversary
from simulation.bridge import SwarmRaftBridge

def run_experiment(n, f, trials=100):
    config = {'n': n, 'f': f, 'R_GNSS': 0.5, 'R_INS': 0.1, 'sigma_d': 0.05, 'dt': 1.0, 
              'spoof_bias': np.array([20.0, 20.0, 0.0])}
    
    bridge = SwarmRaftBridge()
    errors = []

    for _ in range(trials):
        world = SwarmWorld(config)
        adversary = Adversary(config)
        
        world.generate_step(k=1)
        reports = world.get_all_reports()
        dist_matrix = world.get_full_distance_matrix()
        
        _, attacked_dist = adversary.apply_attacks(world.drones, dist_matrix)
        
        recovered, _ = bridge.run_swarmraft(reports, attacked_dist)
        
        true_positions = np.array([d.true_pos for d in world.drones])
        mae = np.mean(np.linalg.norm(true_positions - recovered, axis=1))
        errors.append(mae)
        
    return np.mean(errors)

swarm_sizes = [3, 5, 7, 9, 11, 13, 15, 17]
results = []
for n in swarm_sizes:
    f = n // 2  
    results.append(run_experiment(n, f))

plt.plot(swarm_sizes, results, marker='o', color='orange', label='SwarmRaft MAE')
plt.yscale('log')
plt.xlabel("Swarm Size (n)")
plt.ylabel("Mean Error (m, log scale)")
plt.title("Error Scaling with Swarm Size")
plt.grid(True, which="both", ls="-")
plt.show()