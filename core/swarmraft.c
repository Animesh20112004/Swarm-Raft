#include "swarmraft.h"
#include <math.h>

double get_dist(Point3D a, Point3D b) {
    return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2) + pow(a.z - b.z, 2));
}

void verify_neighbors(int n, Point3D* reports, double* dist_matrix, double threshold, bool* fault_flags) {
    for (int i = 0; i < n; i++) {
        int votes = 0;
        for (int j = 0; j < n; j++) {
            if (i == j) continue;

            double d_rep = get_dist(reports[i], reports[j]);
            double d_meas = dist_matrix[i * n + j];


            if (fabs(d_rep - d_meas) < threshold) {
                votes++;
            } else {
                votes--;
            }
        }
        
        fault_flags[i] = (votes < 0);
    }
}

Point3D recover_position(int target_idx, int n, Point3D* reports, double* dist_matrix, bool* fault_flags, int max_iterations) {
    Point3D p = reports[target_idx];
    double step_size = 0.1;

    for (int k = 0; k < max_iterations; k++) {
        double grad_x = 0, grad_y = 0, grad_z = 0;
        int anchors = 0;

        for (int j = 0; j < n; j++) {
            if (target_idx == j || fault_flags[j]) continue;

            double d_curr = get_dist(p, reports[j]);
            double d_meas = dist_matrix[target_idx * n + j];
            double err = d_curr - d_meas;

            if (d_curr > 0.001) {
                grad_x += err * (p.x - reports[j].x) / d_curr;
                grad_y += err * (p.y - reports[j].y) / d_curr;
                grad_z += err * (p.z - reports[j].z) / d_curr;
                anchors++;
            }
        }

        if (anchors < 3) break; 

        p.x -= step_size * grad_x;
        p.y -= step_size * grad_y;
        p.z -= step_size * grad_z;
    }
    return p;
}