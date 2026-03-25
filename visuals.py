import pygame
import numpy as np
import time
import threading
from simulation.world import SwarmWorld
from simulation.attacks import Adversary
from simulation.bridge import SwarmRaftBridge

# --- Constants & Colors ---
SCREEN_SIZE = 800
SCALE = 10  # Pixels per meter
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)     # True Position
RED = (255, 0, 0)       # Spoofed/Noisy
GOLD = (255, 215, 0)    # Recovered
GRAY = (100, 100, 100)

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("SwarmRaft Live Defense Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)

        # Swarm Logic
        self.config = {
            'n': 10, 'f': 4, 'R_GNSS': 0.5, 'R_INS': 0.1, 
            'sigma_d': 0.05, 'dt': 0.1, 'spoof_bias': np.array([15.0, 15.0, 0.0])
        }
        self.world = SwarmWorld(self.config)
        self.adversary = Adversary(self.config)
        self.bridge = SwarmRaftBridge()

        # State Control
        self.paused = False
        self.is_spoofed = False
        self.recovery_active = False
        self.last_spoof_time = 0
        self.recovered_pos = None
        self.fault_flags = [False] * self.config['n']

    def handle_recovery(self):
        """Runs the C-Core logic in a background thread to prevent lag."""
        print("\n[CLI] --- CONSENSUS TRIGGERED ---")
        reports = self.world.get_all_reports()
        dist_matrix = self.world.get_full_distance_matrix()
        
        # Apply attack to the data being processed
        _, attacked_dist = self.adversary.apply_attacks(self.world.drones, dist_matrix)
        
        start_time = time.time()
        self.recovered_pos, self.fault_flags = self.bridge.run_swarmraft(reports, attacked_dist, threshold=3.0)
        end_time = time.time()
        
        print(f"[CLI] Stage 1: {sum(self.fault_flags)} drones flagged as Byzantine.")
        print(f"[CLI] Stage 2: Multilateration complete in {(end_time - start_time)*1000:.2f}ms")
        print("[CLI] Results broadcasted to swarm. INS states reset.")
        self.recovery_active = True

    def run(self):
        running = True
        while running:
            self.screen.fill((20, 20, 20)) # Dark background
            
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # Pause/Play
                        self.paused = not self.paused
                        print(f"[CLI] System {'Paused' if self.paused else 'Resumed'}")
                    if event.key == pygame.K_s and not self.is_spoofed: # Spoof
                        self.is_spoofed = True
                        self.last_spoof_time = time.time()
                        print("[CLI] ALERT: GNSS Spoofing attack detected on f drones!")

            # 2. Physics & Logic Update
            if not self.paused:
                self.world.generate_step(k=1)
                
                # Check for automatic recovery (2 seconds after spoofing)
                if self.is_spoofed and (time.time() - self.last_spoof_time > 2.0) and not self.recovery_active:
                    threading.Thread(target=self.handle_recovery).start()

            # 3. Drawing
            self.draw_ui()
            reports = self.world.get_all_reports()
            
            for i, drone in enumerate(self.world.drones):
                # Convert coords to screen pixels
                true_px = (int(drone.true_pos[0] * SCALE + 100), int(drone.true_pos[1] * SCALE + 400))
                rep_px = (int(reports[i][0] * SCALE + 100), int(reports[i][1] * SCALE + 400))

                # Draw True Position (Green)
                pygame.draw.circle(self.screen, GREEN, true_px, 4)
                
                # Draw Reported Position (Red)
                pygame.draw.circle(self.screen, RED, rep_px, 4, 1)
                pygame.draw.line(self.screen, GRAY, true_px, rep_px, 1)

                # Draw Recovered Position (Gold Star)
                if self.recovery_active and self.recovered_pos is not None:
                    rec_px = (int(self.recovered_pos[i][0] * SCALE + 100), int(self.recovered_pos[i][1] * SCALE + 400))
                    pygame.draw.circle(self.screen, GOLD, rec_px, 6)
                    if self.fault_flags[i]:
                        pygame.draw.line(self.screen, GOLD, rep_px, rec_px, 2)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def draw_ui(self):
        controls = "SPACE: Pause/Play | S: Inject Spoof Attack"
        status = f"Status: {'PAUSED' if self.paused else 'RUNNING'} | Spoofed: {self.is_spoofed} | Shield: {self.recovery_active}"
        
        self.screen.blit(self.font.render(controls, True, WHITE), (20, 20))
        self.screen.blit(self.font.render(status, True, WHITE), (20, 45))

if __name__ == "__main__":
    App().run()