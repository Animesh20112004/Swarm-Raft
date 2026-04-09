#ifndef SWARMRAFT_H
#define SWARMRAFT_H

typedef struct {
    double x, y, z;
} Position;

// Interface for Python via ctypes
void verify_and_recover(
    int n, 
    Position* reported, 
    double* distance_matrix, 
    double threshold, 
    double epsilon, 
    int max_iter, 
    Position* out_verified, 
    int* out_faulty_flags
);

#endif