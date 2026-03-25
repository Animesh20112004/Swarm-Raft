import pygame
import numpy as np
import time
import threading
from simulation.world import SwarmWorld
from simulation.bridge import SwarmRaftBridge

# --- Styling & Config ---
SCREEN_W, SCREEN_H = 1000, 800
CENTER = (SCREEN_W // 2, SCREEN_H // 2)
SCALE = 10.0 
WORLD_SPEED = 2.0
LERP_FACTOR = 0.1 

class SwarmRaftSim:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Consolas", 14)
        
        # Configuration
        self.config = {
            'n': 10, 'f': 4, 'R_GNSS': 0.4, 'sigma_d': 0.05, 
            'dt': 0.1, 'spoof_bias': np.array([30.0, 20.0, 0.0])
        }
        
        self.world = SwarmWorld(self.config)
        self.bridge = SwarmRaftBridge()

        # Camera States
        self.view_x, self.view_y = 0.0, 0.0
        self.grid_y = 0
        
        # Logic States
        self.active_attack = False
        self.attack_start_time = 0
        self.malicious_ids = []
        self.fault_flags = [False] * self.config['n']

    def handle_recovery(self):
        """The Consensus Trigger"""
        print("\n[CLI] T+2.0s: DRIFT DETECTED. EXECUTING CONSENSUS...")
        
        # 1. Get current reports (including spoofed coordinates)
        reports = self.world.get_all_reports(attacked_indices=self.malicious_ids)
        
        # 2. Get the FRESH distance matrix (the truth from the world)
        dist_matrix = self.world.get_full_distance_matrix()
        
        # 3. Call C-Core
        start_time = time.time()
        # Increased threshold to account for high-velocity drift noise
        recovered_pos, flags = self.bridge.run_swarmraft(reports, dist_matrix, threshold=5.0)
        
        # 4. PHYSICAL CORRECTION: This is what makes them snap back
        for i in range(self.config['n']):
            if flags[i]:
                # Force the drone back to the consensus-calculated truth
                self.world.drones[i].true_pos = recovered_pos[i]

        print(f"[CLI] Consensus Reached in {(time.time() - start_time)*1000:.2f}ms.")
        print(f"[CLI] {sum(flags)} nodes re-synced with swarm cluster.")
        
        # Reset attack state
        self.active_attack = False
        self.malicious_ids = []

    def run(self):
        while True:
            self.screen.fill((10, 10, 15))
            
            # Draw Background Grid
            self.grid_y = (self.grid_y + WORLD_SPEED) % 100
            for y in range(int(self.grid_y), SCREEN_H, 100):
                pygame.draw.line(self.screen, (20, 20, 40), (0, y), (SCREEN_W, y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    if not self.active_attack:
                        self.active_attack = True
                        self.attack_start_time = time.time()
                        self.malicious_ids = list(range(self.config['f']))
                        print(f"[CLI] ALERT: Nodes 0-{self.config['f']-1} breaking formation!")

            # Update Physics
            atk_list = self.malicious_ids if self.active_attack else None
            self.world.generate_step(malicious_indices=atk_list)

            # Auto-Recovery
            if self.active_attack and (time.time() - self.attack_start_time > 2.0):
                # We use a thread so the screen doesn't freeze during C-calculation
                threading.Thread(target=self.handle_recovery).start()

            # Camera Smoothing (Center on Honest Majority)
            honest_nodes = [d.true_pos for i, d in enumerate(self.world.drones) if i not in self.malicious_ids]
            target_x, target_y = np.mean(honest_nodes, axis=0)[:2] if honest_nodes else (0,0)
            
            self.view_x += (target_x - self.view_x) * LERP_FACTOR
            self.view_y += (target_y - self.view_y) * LERP_FACTOR

            # Draw Drones
            for i, d in enumerate(self.world.drones):
                sx = (d.true_pos[0] - self.view_x) * SCALE + CENTER[0]
                sy = (d.true_pos[1] - self.view_y) * SCALE + CENTER[1]
                
                # If the drone is currently drifting, make it RED
                color = (255, 50, 50) if i in self.malicious_ids else (0, 255, 120)
                pygame.draw.circle(self.screen, color, (int(sx), int(sy)), 6)
                
                # Name Tag
                tag = self.font.render(f"UAV-{i}", True, (200, 200, 200))
                self.screen.blit(tag, (sx + 8, sy - 8))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    SwarmRaftSim().run()