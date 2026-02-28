#ifndef SWARMRAFT_H
#define SWARMRAFT_H

#include <stdbool.h>

// Structure to match Python's NumPy array entries (x, y, z)
typedef struct {
    double x;
    double y;
    double z;
} Point3D;


//   Stage 1: Consistency Voting True => Drone is flagged as faulty

void verify_neighbors(
    int n, 
    Point3D* reports, 
    double* dist_matrix, 
    double threshold, 
    bool* fault_flags
);

//   Stage 2: Multilateration for drone position recovery

Point3D recover_position(
    int target_idx,
    int n,
    Point3D* reports,
    double* dist_matrix,
    bool* fault_flags,
    int max_iterations
);

#endif