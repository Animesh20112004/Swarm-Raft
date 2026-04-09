#include "swarmraft.h"
#include <math.h>
#include <stdlib.h>

void verify_and_recover(int n, Position* reported, double* dist_mat, double threshold, 
                        double epsilon, int max_iter, Position* verified, int* flags) {
    
    // Stage 1: Voting 
    for (int i = 0; i < n; i++) {
        int votes = 0;
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            double dx = reported[i].x - reported[j].x;
            double dy = reported[i].y - reported[j].y;
            double dz = reported[i].z - reported[j].z;
            double calc_dist = sqrt(dx*dx + dy*dy + dz*dz);
            
            if (fabs(calc_dist - dist_mat[i * n + j]) < threshold) votes++;
            else votes--;
        }
        flags[i] = (votes < 0) ? 1 : 0; // 1 = Faulty 
        verified[i] = reported[i];
    }

    // Stage 2: Multilateration Refinement [cite: 181, 307]
    for (int i = 0; i < n; i++) {
        if (flags[i]) {
            Position p = reported[i]; 
            for (int iter = 0; iter < max_iter; iter++) {
                double grad_x = 0, grad_y = 0, grad_z = 0;
                int anchor_count = 0;

                for (int j = 0; j < n; j++) {
                    if (flags[j]) continue; // Only use non-faulty anchors [cite: 174]
                    
                    double dx = p.x - verified[j].x;
                    double dy = p.y - verified[j].y;
                    double dz = p.z - verified[j].z;
                    double d = sqrt(dx*dx + dy*dy + dz*dz) + 1e-6;
                    double error = d - dist_mat[i * n + j];
                    
                    grad_x += error * (dx / d);
                    grad_y += error * (dy / d);
                    grad_z += error * (dz / d);
                    anchor_count++;
                }

                if (anchor_count < 3) break; // Fallback to INS if insufficient anchors [cite: 189]

                p.x -= 0.1 * grad_x; // Simple gradient descent step
                p.y -= 0.1 * grad_y;
                p.z -= 0.1 * grad_z;
            }
            
            double final_dev = sqrt(pow(p.x-reported[i].x,2) + pow(p.y-reported[i].y,2));
            if (final_dev > epsilon) verified[i] = p; // Replace if spoofing detected [cite: 274, 307]
        }
    }
}