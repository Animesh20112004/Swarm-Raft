#ifndef SWARMRAFT_H
#define SWARMRAFT_H

#include <stdbool.h>

typedef struct {
    double x;
    double y;
    double z;
} Point3D;


void verify_neighbors(
    int n, 
    Point3D* reports, 
    double* dist_matrix, 
    double threshold, 
    bool* fault_flags
);

Point3D recover_position(
    int target_idx,
    int n,
    Point3D* reports,
    double* dist_matrix,
    bool* fault_flags,
    int max_iterations
);

#endif