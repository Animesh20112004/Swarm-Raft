import numpy as np
import matplotlib.pyplot as plt
from simulation.world import SwarmWorld
from simulation.attacks import Adversary
from simulation.bridge import SwarmRaftBridge

def run_experiment(n, f, trials=100):
    config = {
        'n': n, 'f': f, 
        'R_GNSS': 0.5, 'R_INS': 0.1, 'sigma_d': 0.05, 'dt': 1.0, 
        'spoof_bias': np.array([20.0, 20.0, 0.0])
    }
    
    bridge = SwarmRaftBridge()
    recovered_errors = []
    raw_errors = []
    dynamic_threshold = 3 * config['R_GNSS'] + 0.5

    for _ in range(trials):
        world = SwarmWorld(config)
        adversary = Adversary(config)
        
        world.generate_step(k=1)
        dist_matrix = world.get_full_distance_matrix()
        
        # Scenario: Collect positions before they are attacked for the baseline
        true_positions = np.array([d.true_pos for d in world.drones])
        
        # Apply attacks
        _, attacked_dist = adversary.apply_attacks(world.drones, dist_matrix)
        reports = world.get_all_reports() # These are now spoofed
        
        # Baseline: Error of the spoofed reports without SwarmRaft
        raw_mae = np.mean(np.linalg.norm(true_positions - reports, axis=1))
        raw_errors.append(raw_mae)
        
        # SwarmRaft: Execute recovery with the dynamic threshold
        recovered, _ = bridge.run_swarmraft(reports, attacked_dist, threshold=dynamic_threshold)
        
        # Recovered Error
        rec_mae = np.mean(np.linalg.norm(true_positions - recovered, axis=1))
        recovered_errors.append(rec_mae)
        
    return np.mean(raw_errors), np.mean(recovered_errors)

# --- Run Scaling Test ---
swarm_sizes = [3, 5, 7, 9, 11, 13, 15, 17]
raw_results = []
rec_results = []

print("Running Monte Carlo trials...")
for n in swarm_sizes:
    f = n // 2  # Condition n >= 2f + 1
    raw, rec = run_experiment(n, f, trials=200)
    raw_results.append(raw)
    rec_results.append(rec)
    print(f"n={n}, f={f} | Raw: {raw:.2f}m | Recovered: {rec:.2f}m")

# --- Visualization matching Figure 2 ---
plt.figure(figsize=(10, 6))
plt.plot(swarm_sizes, raw_results, 'r--s', label='Raw / Spoofed Position Error')
plt.plot(swarm_sizes, rec_results, 'o-', color='orange', label='Recovered Position Error (SwarmRaft)')

plt.yscale('log')
plt.xlabel("Swarm size n")
plt.ylabel("Mean error (m, log scale)")
plt.title("Error Scaling with Swarm Size")
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.show()